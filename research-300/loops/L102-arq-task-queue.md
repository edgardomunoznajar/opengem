# L102 — Arq for Adapter Scheduling (and Why Not Asynq, Celery, or "Just Dagster")

**Loop**: 102 / 300
**Phase**: 2 — Deep dive on top candidates
**Date**: 2026-06-06

---

## Thesis of this loop

Dagster (L079) is the right tool for *asset-shaped* work: ingest a series, version it, produce a forecast, score it. It is *not* the right tool for *task-shaped* work: poll GDELT every 15 minutes and emit Server-Sent Events to the live ticker, debounce a flurry of user-triggered backtests, retry a failed Resend email send, fan out a Discord alert to 200 channels. These are short, ephemeral, often user-triggered, often deadline-sensitive jobs that want a queue, not an asset graph.

This loop picks the task queue. The four candidates: Asynq (Go), Celery (Python), Arq (Python async), or "just extend Dagster sensors and ops for everything." The winner has to be Python (the OPENGEM stack is Python adapters + Next.js frontend + Postgres + Dagster + FastAPI), has to be async (because most of OPENGEM's adapter code is `httpx`-based and burns I/O, not CPU), has to be operationally cheap for a one-person team, and has to coexist gracefully with Dagster without confusing the lineage story.

Verdict: **Arq.** Redis-backed, async-native, ~600 lines of source code, runs in a single worker process, the operational footprint is "Redis you already have for caching + one extra Python process." Asynq is great but it's Go (wrong language for OPENGEM). Celery is the obvious default and the wrong default — it's sync-first, heavy, and the "I want to retry this `httpx.get` if Cloudflare returned 503" experience is worse than Arq's. And "just Dagster" mis-shapes work that shouldn't be an asset.

---

## Asynq — wrong language

Asynq is the best-in-class Go task queue: Redis-backed, typed payloads, web UI, retries with exponential backoff, scheduled tasks, unique jobs (prevent duplicates), task groups, priority queues. If OPENGEM were a Go shop it would be the obvious pick.

OPENGEM isn't a Go shop. Adopting Asynq means adopting Go for the worker layer, which means splitting the team's Python knowledge across two runtimes for no obvious win. The adapters that Asynq would orchestrate (GDELT polling, World Bank SDMX fetches, FRED CSV downloads) are all Python today, all using `httpx` + `pydantic` + `pandas`. Switching them to Go to use Asynq's typed payload story is a six-week migration with negative ROI.

**SKIP**. Right tool, wrong language.

---

## Celery — the obvious default, but the wrong default in 2026

Celery is the Python community's default task queue. It is also the *legacy* Python task queue — it predates `async/await`, predates `httpx`, predates the modern type-checked Python ecosystem.

What's still good about Celery:

- Battle-tested for fifteen years. Every weird edge case has been hit and documented.
- Huge ecosystem: Flower for monitoring, integrations with Django/Flask/FastAPI, every broker supported (Redis, RabbitMQ, SQS, even Kafka).
- "Periodic tasks" via Celery Beat solves cron-style scheduling.

What hurts Celery for OPENGEM in 2026:

- **Async support is bolted-on.** Celery 5.x has *some* async support but it's not the happy path. The canonical Celery worker forks processes (`prefork` pool), runs sync code, and blocks on I/O. Running `httpx`-based async adapters under Celery means either threading or `gevent`, both of which have sharp edges around contextvars and structured logging.
- **The worker is heavy.** A Celery worker process is ~120MB resident, runs at least one child per concurrency slot, and the supervisor + beat + flower combo is at least three processes on the box. For OPENGEM's actual workload (a few hundred jobs/hour at v1, peaking at maybe 50k/hour with full distribution flywheel), this is overkill.
- **The retry/back-off story is verbose.** `@task(autoretry_for=..., retry_kwargs={'max_retries': 5, 'countdown': 60}, retry_backoff=True)` works but every adapter has to opt in to this with its own decorator config. Arq has saner defaults.
- **Operational surface is large.** Flower has had real CVEs. Beat as a singleton scheduler has been a foot-gun in production for years.

Celery is the right answer if your team is 10+ engineers, your task volume is 10M/day, and you need every broker. For OPENGEM it's a 1000x oversized tool.

**SKIP** as the v1 pick. Revisit at Y3 if scale demands it (which is unlikely — by Y3 we should be scaling adapters horizontally, not deepening the queue).

---

## "Just extend Dagster" — wrong shape for ephemeral tasks

Dagster has sensors, schedules, and runs. You *can* express "poll GDELT every 15 minutes" as a Dagster schedule that materializes an asset. You *can* express "send Discord alert" as a Dagster op.

You *shouldn't*. Two reasons:

1. **Asset graphs are for things you can rematerialize.** A Discord alert is not an asset; it's a side effect that fires once and is gone. Modeling it as an asset corrupts the lineage story. If your asset graph contains "discord-alert-2026-06-06T13:42:00", every reproducibility envelope and every backtest harness has to deal with that asset, even though it's not data.

2. **Dagster runs are expensive.** A Dagster run is ~1.5 seconds of orchestration overhead (a database row in `runs`, telemetry events, the run-launcher heartbeat). For a 200ms GDELT poll that produces a metric, this is 7.5x overhead. For a queue-shaped workload that's wrong.

The right rule: **Dagster owns assets (vintaged data). Arq owns tasks (ephemeral side effects + user-triggered jobs).** Dagster *sensors* can enqueue Arq jobs when an asset changes; Arq jobs can write back to a Dagster-managed Postgres table that triggers asset rematerialization. The two cooperate; they don't subsume each other.

---

## Arq — the recommended pick

Arq (from samuelcolvin, the same person who built pydantic) is the async-native Python task queue. Key properties:

- **Redis-backed** — OPENGEM already runs Redis for caching and rate limiting; the queue piggybacks on it.
- **Async-native** — task functions are `async def`. They `await httpx.get(...)` directly. No threadpool tricks.
- **Small** — ~600 lines of source. The entire architecture is readable in an afternoon.
- **Operational footprint** — one `arq worker.WorkerSettings` process. Add a second for redundancy. That's the whole deployment.
- **Cron-style scheduling** — `cron(hour={0, 6, 12, 18})` decorator. No separate "beat" daemon.
- **Retries with exponential backoff** — `@retry(retries=5)` decorator with sane defaults.
- **Result storage in Redis** — `await job.result()` from anywhere.
- **Typed via pydantic v2** — payloads are `BaseModel` subclasses; deserialization errors are caught at enqueue time.
- **Healthchecks** — `arq healthcheck` for k8s/Cloud Run probes.

What Arq lacks vs Celery: priority queues (workaround: separate worker pools per priority), task chord/group primitives (workaround: `asyncio.gather` in a parent job), Flower-style UI (workaround: a tiny FastAPI dashboard if needed; usually `arq queue_size` over Redis CLI suffices).

For OPENGEM's workload these workarounds are fine. We don't need 200 priority levels; we need "low-latency user-triggered jobs" and "best-effort polling jobs." Two worker pools handle that.

---

## The integration contract: Dagster + Arq + FastAPI

```
┌─────────────────────┐  enqueues  ┌──────────────┐
│  Dagster sensors    │ ─────────► │  Arq queues  │
│  + Dagster schedules│            │  (Redis)     │
└─────────────────────┘            └──────┬───────┘
                                          │ dequeue + execute
                                          ▼
                                   ┌──────────────┐
                                   │ Arq workers  │
                                   │ (Python      │
                                   │  async)      │
                                   └──────┬───────┘
                                          │ writes back
       ┌──────────────────┐               │
       │  FastAPI WS      │ ◄─────────────┤ (via Postgres NOTIFY)
       │  + SSE streams   │               │
       │  (live ticker)   │               │
       └──────────────────┘               │
       ┌──────────────────┐               │
       │  Postgres        │ ◄─────────────┘
       │  (jobs_log,      │
       │   metric_cache)  │
       └──────────────────┘
```

Three queues, named by SLA:

- `realtime` — user-triggered: vintage rewinds, custom backtests, embed-rendering, MCP tool invocations under load. Target: 200ms p50, 2s p99.
- `polling` — every-15-minute GDELT, every-hour FRED, every-day World Bank. Target: 1 minute p99.
- `notifications` — Discord/Telegram alerts, Resend emails, Stripe webhook reactions. Target: 10s p99.

Each queue is its own Arq `WorkerSettings`. One container per queue (three containers total). Single Redis instance. Single Postgres for results.

---

## Next-step: the worker skeleton

```python
# adapters/worker.py
from arq import cron, Worker
from arq.connections import RedisSettings
import httpx
import structlog

log = structlog.get_logger()

async def poll_gdelt(ctx, window_minutes: int = 15) -> dict:
    """Poll GDELT 2.0 events, write to Postgres, broadcast to WS subscribers."""
    async with httpx.AsyncClient(timeout=30) as client:
        url = f"http://data.gdeltproject.org/gdeltv2/lastupdate.txt"
        r = await client.get(url)
        latest = r.text.strip().split("\n")[0].split()[-1]
        ev_url = latest.replace(".CSV.zip", ".export.CSV.zip")
        events = await fetch_and_parse(client, ev_url)
        await persist_events(ctx["pg"], events)
        await ctx["ws_broker"].broadcast({"type": "gdelt_tick", "n": len(events)})
        return {"events": len(events), "vintage": latest}

async def send_discord_alert(ctx, channel_id: str, payload: dict) -> None:
    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://discord.com/api/v10/channels/{channel_id}/messages",
            headers={"Authorization": f"Bot {ctx['discord_token']}"},
            json=payload,
            timeout=10,
        )

class PollingWorker:
    functions = [poll_gdelt]
    cron_jobs = [cron(poll_gdelt, minute={0, 15, 30, 45})]
    redis_settings = RedisSettings.from_dsn("redis://redis:6379/2")
    max_jobs = 20

class NotificationsWorker:
    functions = [send_discord_alert]
    redis_settings = RedisSettings.from_dsn("redis://redis:6379/3")
    max_jobs = 100
```

---

## What this loop produced

- A verdict: Arq, with reasoning against the three alternatives.
- The three-queue topology (realtime / polling / notifications) with SLAs.
- The Dagster + Arq + FastAPI integration contract diagram.
- A worker skeleton ready for `adapters/worker.py`.

## What comes next

- **L103** — the FastAPI WebSocket spec that Arq writes back into.
- **L114** — Discord/Telegram bot uses the `notifications` queue.
- **L109** — Stripe webhooks land via `notifications` queue.

## Related

- [[L079-dagster-prefect-airflow-temporal]] — Dagster owns assets, Arq owns tasks
- [[L021-gdelt-gkg]] — the canonical polling-queue customer
- [[L103-fastapi-websocket]] — Arq writes events that the WS broadcasts
- [[L109-stripe-magic-link]] — Stripe webhook handlers run as Arq jobs
- [[L114-discord-telegram-alerts]] — alert fanout runs via notifications queue
