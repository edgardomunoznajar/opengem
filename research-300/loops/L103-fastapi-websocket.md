# L103 — FastAPI + WebSocket Streaming for the Live Ticker

**Loop**: 103 / 300
**Phase**: 2 — Deep dive on top candidates
**Date**: 2026-06-06

---

## Thesis of this loop

The OPENGEM home screen has a live ticker — a Bloomberg-style scroll of "USA CPI YoY 3.2% (▲ 0.1)" entries interleaved with "GDELT event burst: Donbas" and "scenario `oil_shock_2026` triggered" notices. The ticker is the page's metabolism: when it's moving, the site feels alive; when it's frozen, the site feels abandoned.

The naive implementation is "poll `/api/ticker` every 5 seconds from the client." That is wrong for three reasons: it scales the server's database with `N_users × 1 / 5s` reads even when nothing is changing; it adds 5 seconds of latency to every event; and it makes the page feel like a polling app rather than a streaming app. The right implementation is server-pushed events over a long-lived connection.

This loop picks the protocol (WebSocket vs SSE), the framework (FastAPI's built-in WS support vs alternatives), the message envelope, the auth model, the back-pressure and reconnect strategy, and the integration with Arq (L102) so that an Arq job can fan-out a single event to all connected subscribers in <50ms.

Verdict: **FastAPI WebSocket endpoint at `/ws/ticker`, with a Redis Pub/Sub fan-out, a typed `TickerEvent` envelope, JWT-based optional auth (anonymous allowed, gated to read-only public stream), exponential-backoff reconnect on the client, and a parallel `GET /v1/events?since=...` SSE endpoint for the embed SDK which can't easily use WS through corporate proxies.** WS for the main app, SSE for embeds and the MCP server.

---

## WebSocket vs Server-Sent Events: pick both

The default debate: WS is bidirectional and binary-capable; SSE is unidirectional, text-only, and dies less often through proxies. For OPENGEM:

- The **main dashboard** wants WS because the user might `subscribe`/`unsubscribe` to specific country/indicator channels dynamically. That requires client→server messages.
- The **embed SDK** (L111) and **third-party MCP clients** want SSE because (a) it works through HTTP/1.1 keep-alive without WS upgrade negotiation, (b) it sails through Substack iframe CSP without trouble, (c) it auto-reconnects with `EventSource` semantics, and (d) it's stateless on the server side (just a long-lived HTTP response).

We ship both. They share a Redis Pub/Sub backend, so a single Arq job publishes once and every connected client (WS or SSE) sees it. The protocols are interchangeable from the consumer's perspective; only the framing differs.

---

## The event envelope

Every event has the same shape, regardless of which channel it goes out on. This is the single most important design decision in the entire loop — if the envelope is consistent, every downstream consumer (dashboard JS, embed SDK, MCP server, Discord bot, RSS generator) can be written against one schema.

```typescript
type TickerEvent = {
  id: string;              // monotonic ULID — used for resumption
  ts: string;              // ISO 8601 UTC
  kind: "indicator_update" | "forecast_revision" | "scenario_trigger"
      | "event_burst" | "miss_logged" | "heartbeat";
  country?: string;        // ISO-3
  indicator?: string;      // canonical slug
  payload: Record<string, unknown>;
                           // shape varies by kind, see schemas/ticker-event.json
  vintage_id?: string;     // for indicator_update and forecast_revision
  provenance_url?: string; // canonical OPENGEM URL for this event
};
```

Two non-obvious choices:

1. **`id` is a ULID, not a UUID**. ULIDs sort lexicographically by timestamp, so a client can resume with `?since=01HV…` without the server needing to maintain a separate "event sequence" table. The Redis Pub/Sub channel keeps the last 5000 events in a sorted set keyed by ULID, so reconnecting clients catch up in one Redis call.

2. **`heartbeat` is a first-class kind**. Every 25 seconds the server emits `{kind: "heartbeat"}` so that browser tabs, mobile screens, and corporate proxies don't silently kill the connection. Heartbeats are also the only event that does *not* get logged to the canonical event stream — they're transient.

---

## The FastAPI WebSocket endpoint

```python
# api/streams/ticker.py
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from redis.asyncio import Redis
from .auth import optional_user

router = APIRouter()

@router.websocket("/ws/ticker")
async def ticker_ws(
    ws: WebSocket,
    since: str | None = Query(None, description="ULID to resume from"),
    countries: str | None = Query(None, description="comma-sep ISO-3 filter"),
    indicators: str | None = Query(None, description="comma-sep indicator slugs"),
    user=Depends(optional_user),
):
    await ws.accept()
    sub_countries = set(countries.split(",")) if countries else None
    sub_indicators = set(indicators.split(",")) if indicators else None
    redis: Redis = ws.app.state.redis

    # 1. Catch-up — replay since `since`
    if since:
        events = await redis.zrangebylex("ticker:log", f"({since}", "+")
        for raw in events[-500:]:
            await ws.send_text(raw)

    # 2. Subscribe — live forwarding via Redis Pub/Sub
    pubsub = redis.pubsub()
    await pubsub.subscribe("ticker:channel")
    try:
        async for msg in pubsub.listen():
            if msg["type"] != "message":
                continue
            ev = json.loads(msg["data"])
            if sub_countries and ev.get("country") not in sub_countries:
                continue
            if sub_indicators and ev.get("indicator") not in sub_indicators:
                continue
            await ws.send_text(msg["data"])
    except WebSocketDisconnect:
        pass
    finally:
        await pubsub.unsubscribe("ticker:channel")
```

Notes:

- **Subscription filters are server-side**, not client-side. A user watching only USA + EUR pays for one read from Redis; the server filters out the 95% of events that don't match before sending across the wire. This matters for mobile data plans.
- **`Query` parameters, not subsequent WS messages**, drive the subscription. This makes the connection URL "self-describing" — you can paste a WS URL into a curl command and see what's being subscribed.
- **No per-user state on the server**. The connection holds a `pubsub` object and some local sets. If the server restarts, the client reconnects with `since=` and catches up. No session table, no Redis-stored per-user subscription.

---

## The SSE counterpart

```python
@router.get("/v1/events")
async def ticker_sse(
    since: str | None = None,
    countries: str | None = None,
    indicators: str | None = None,
):
    async def gen():
        # identical filter + replay logic; emits "data: <json>\n\n" frames
        ...
    return StreamingResponse(gen(), media_type="text/event-stream")
```

Identical filter logic. The framing is `data: <json>\n\n` with `id: <ulid>` so `EventSource.lastEventId` Just Works.

---

## Back-pressure and slow-consumer handling

When a client can't keep up — bad mobile network, paused tab, slow proxy — the server *must not* spend memory queuing events for them. The rule: **if `ws.send_text` blocks for more than 2 seconds, drop the connection**. The client will reconnect with `since=lastSeenUlid` and catch up. This trades a tiny replay cost (≤500 events from Redis) for bounded server memory.

FastAPI's WS doesn't have a built-in send timeout, so wrap with `asyncio.wait_for(ws.send_text(payload), timeout=2.0)`.

---

## Auth model

The ticker is *public* — anonymous WS connections allowed, no key required. The MCP throughput tier and the Pro tier get higher event-rate limits (the public anonymous stream is throttled to 60 events/minute *per IP*, which is comfortably above the realistic event rate but stops abuse). Pro keys lift the throttle.

JWT in the `Sec-WebSocket-Protocol` header (a common trick) or as a `?key=` query param. The optional dependency `optional_user` returns `None` for anonymous, a `User` object for authenticated; the rate-limit middleware reads from that.

---

## Next-step: the client skeleton

```typescript
// lib/ticker-client.ts
export class TickerClient {
  private ws: WebSocket | null = null;
  private lastId: string | null = null;
  private backoffMs = 500;

  constructor(
    private url: string,
    private onEvent: (e: TickerEvent) => void,
    private filter: { countries?: string[]; indicators?: string[] } = {}
  ) {}

  connect() {
    const q = new URLSearchParams();
    if (this.lastId) q.set("since", this.lastId);
    if (this.filter.countries) q.set("countries", this.filter.countries.join(","));
    if (this.filter.indicators) q.set("indicators", this.filter.indicators.join(","));
    this.ws = new WebSocket(`${this.url}?${q}`);
    this.ws.onmessage = (m) => {
      const ev = JSON.parse(m.data) as TickerEvent;
      this.lastId = ev.id;
      if (ev.kind !== "heartbeat") this.onEvent(ev);
    };
    this.ws.onclose = () => {
      setTimeout(() => this.connect(), this.backoffMs);
      this.backoffMs = Math.min(this.backoffMs * 2, 30_000);
    };
    this.ws.onopen = () => { this.backoffMs = 500; };
  }
}
```

---

## What this loop produced

- Verdict: ship both WS and SSE behind a shared Redis Pub/Sub fan-out.
- A `TickerEvent` envelope schema with ULID resumption.
- A FastAPI WebSocket endpoint skeleton with server-side filtering.
- An SSE counterpart for embeds and MCP.
- A back-pressure rule (2s send timeout → drop) that keeps memory bounded.
- A client reconnect strategy with `since=` resumption.

## What comes next

- **L127** — the event stream UI design uses this protocol.
- **L131** — alerts UX wires push notifications off the same stream.
- **L111** — embed SDK v2 consumes the SSE counterpart for the "live tile" mode.

## Related

- [[L102-arq-task-queue]] — Arq jobs `redis.publish("ticker:channel", ...)`
- [[L127-event-stream]] — the UI design for the ticker
- [[L131-alerts-ux]] — alerts are a per-user filter on the same protocol
- [[L111-embed-widgets-v2]] — SSE-mode embed becomes "live tile"
- [[L108-mcp-server-contract]] — `subscribe_events` MCP tool wraps the SSE stream
