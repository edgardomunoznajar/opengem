# L090 — Grafana vs Custom for Operational Dashboards: The Pick

**Loop**: 090 / 300
**Phase**: 2 — Integration deep dive
**Date**: 2026-06-06
**Verdict**: **ADOPT-V1 (Grafana for ops + custom Next.js for public; Streamlit owns the *authoring* surface separately)**

---

## What this loop closes

L065 named Grafana as the obvious ops-monitoring tool and noted it as wrong for the V&V matrix view. L089 picked Next.js for the public surface and Streamlit for the scenario-authoring surface. This loop closes the *fourth* surface — operational monitoring (pipeline health, ingestion freshness, API/MCP latency, error budgets) — and confirms Grafana wins by a wide margin against any custom build.

The forcing question: with a one-person team and three frontends already on the table (Next.js, Observable Framework, Streamlit), is adding a fourth (Grafana) defensible?

Yes. Because Grafana is not a "fourth frontend" in any meaningful sense. It is an **observability appliance** with a published HTTP UI that costs zero engineering days to maintain and gives back something a custom build cannot match: alerting + 100+ datasource plugins + annotation timeline + community-blessed SRE practice. Below is the case in five parts.

## The four-surface taxonomy

| Surface | Audience | What it serves | Tool |
|---|---|---|---|
| Public dashboard (interactive) | Anonymous millions | Country/indicator/forecast/leaderboard pages | **Next.js** (L089) |
| Public dashboard (long-tail) | Anonymous millions | Country × indicator × explainer pages | **Observable Framework** (L091) |
| Ops authoring | Internal engineers + scenario author | Scenario sweeps, V&V matrix review, vintage management | **Streamlit** (L089) |
| Ops monitoring | Internal engineers + public status page | Pipeline health, ingestion freshness, API latency, alerting | **Grafana** (this loop) |

Each surface has a distinct audience, distinct latency budget, distinct interaction model. None of them is the right tool for the other three's problem.

## Why Grafana wins ops monitoring

### 1. Native time-series first

OPENGEM's ops data is *all* time series: API requests/second, ingestion freshness per series, adapter latency, error counts, MCP throughput, R2 bytes/month, vintage write rate. Grafana was built for this exact shape. Prometheus + Grafana is the standard SRE pattern and is so well-known it disappears from the architecture conversation.

A custom Next.js ops view would have to rebuild: time-series query DSL, panel layout system, refresh primitives, annotation timeline, alert configuration UI, threshold-based color coding. Each piece is 2-4 weeks. Grafana ships all of it.

### 2. Alerting

The single most important ops feature is "wake Edgardo if the BLS adapter has been silent for 25 hours." Grafana's alerting model (rules in YAML, integration with PagerDuty / Slack / email / SMS / webhook) is mature, battle-tested, debuggable, and free. Building alerting into a custom view from scratch is a multi-month side quest that always ends in "we should have just used Grafana."

### 3. Public status page (Y2-Y3 deliverable)

OPENGEM's broader accountability thesis ("publishes its mistakes") extends to publishing pipeline health. The Y2 deliverable is a public status page at `https://status.opengem.org` showing real-time adapter health, ingestion freshness per source, recent incidents, and uptime history. Grafana supports anonymous read-only public dashboards out of the box. A custom build of "status page" is itself a multi-week project (see e.g. statuspage.io's $99/mo product).

### 4. Annotation timeline

Every deploy, every schema migration, every forecast-vintage rollover gets annotated as a vertical line across every panel in every dashboard. When a metric moves at 14:23, the annotation at 14:22 explains why. Grafana's annotation model is first-class. Reproducing it in a custom build is ~3 weeks of feature work.

### 5. Free tier covers Y1 entirely

Grafana Cloud free tier (2026): 10K active metric series, 50 GB logs/traces, 14-day retention, 3 users. OPENGEM Y1 needs roughly 200 active series (one per indicator × adapter health), ~5 GB logs/mo, single-user. We are at 2% of the free tier budget. Past Y1, Grafana Cloud Pro is $0.016/series/month, putting OPENGEM at maybe $30-60/mo at Y2 scale. Negligible.

### 6. Plugin ecosystem covers our data sources

- **Postgres / TimescaleDB native** for the vintage store and the ops-metrics tables.
- **Prometheus native** for FastAPI middleware-emitted metrics.
- **JSON / Infinity** (community, MIT) for any REST endpoint, including our own API.
- **Loki** for structured logs.

We never hit a "Grafana can't read this" wall. We do not pay for the BigQuery commercial plugin — we use the JSON datasource against our cached aggregates.

## Why not custom

A custom Next.js ops view would offer:
- Visual continuity with the public dashboard.
- One less tool to learn.
- More control over the look.

Against:
- ~12 dev-weeks to build the time-series query, panel layout, refresh, alerting, annotation timeline equivalents.
- Ongoing maintenance forever — every new metric type needs a new panel kind.
- No public status page; build that separately.
- No SRE community knowledge transfer (every senior infra engineer knows Grafana; nobody knows OPENGEM's custom ops view).

The trade is **~12 weeks of dev time + perpetual maintenance vs. ~3 days of Grafana setup**. Even if the OPENGEM team grew, custom would not win this trade.

## The Grafana setup we ship

### Phase 5 ops setup (in `deploy/grafana/`)

```
deploy/grafana/
  README.md
  dashboards/
    pipeline-health.json          # one row per adapter, RAG status
    ingestion-freshness.json       # staleness heatmap by series
    api-latency.json               # p50/p95/p99 over time
    mcp-throughput.json            # MCP server tool calls
    vintage-rollover.json          # vintage write rate + size
    public-status.json             # for /status anonymous public mirror
  datasources/
    postgres-vintage.yaml          # TimescaleDB datasource for vintage store
    prometheus-fastapi.yaml        # FastAPI metrics middleware
    json-opengem-api.yaml          # JSON datasource for our own REST API
    loki-logs.yaml                 # structured logs
  alerts/
    adapter-stale.yaml             # any adapter > 25h since heartbeat
    api-p99-latency.yaml           # API p99 > 1s
    vintage-write-fail.yaml        # vintage write failures
    free-tier-budget.yaml          # Grafana series count approaching limit
```

Dashboards live in JSON, version-controlled in `deploy/grafana/`. Grafana provisioning loads them on container restart. Adding a new dashboard is a PR. This is exactly the "dashboards as code" pattern Grafana has standardized.

### Where it runs

- **Y1**: Grafana Cloud free tier. Login at `grafana.com`. Zero infra.
- **Y2**: Same, possibly bumped to Pro for retention + series count.
- **Y3+**: Optionally self-host Grafana OSS in a Cloud Run container if Grafana Cloud's pricing becomes uncompetitive. The dashboards JSON is portable.

### Metrics pipeline

FastAPI middleware emits Prometheus metrics; Grafana Cloud's hosted Prometheus scrapes them via a Push gateway (since we're outbound-only from Cloud Run). Postgres / TimescaleDB exposes its native query interface to Grafana directly. Adapter heartbeats write to a `adapter_heartbeats` table that Grafana queries every 30 seconds.

Total wiring: ~3 days for the Y1 launch dashboards.

## The V&V matrix question

L065 noted: "Grafana is not the V&V matrix tool — Dash wins there." This loop reconfirms. The V&V matrix is:
- A 5-D matrix (indicator × horizon × model × vintage × scoring rule)
- Color-coded per-cell drilldown
- Heavy interactive filtering and sorting
- Used by 1-3 internal engineers to audit forecast performance

This is *Streamlit ops authoring* territory (L089), not Grafana monitoring territory. The V&V matrix lives in a Streamlit app with PerformanceForecast + Plotly + a row-level drilldown UI; the *ops monitoring* of "did the V&V scoring job run today" lives in Grafana.

This is the correct split. Don't conflate "matrix view of forecasts" with "monitoring of the system that produces the matrix."

## Free vs Enterprise

Grafana OSS is Apache 2.0 — fully redistributable, no contamination. Grafana Cloud free tier covers Y1. Grafana Enterprise is a paid add-on with RBAC, audit logs, fine-grained permissions, single sign-on integrations, premium plugins. OPENGEM does not need Enterprise at Y1-Y3. The OSS surface plus the free Cloud tier is sufficient.

## What this also handles for free

By picking Grafana, we get for free:

- **The on-call story**: PagerDuty integration is two clicks.
- **The incident review story**: annotations across panels at incident-start and incident-end produce a one-page incident timeline automatically.
- **The "is the MCP server up" story**: a simple uptime panel with a 200-response check.
- **The cost-tracking story**: panels showing R2 bytes used, BigQuery bytes scanned, Cloud Run instance-hours — all sources Grafana can read.
- **The capacity-planning story**: 30-day trend lines on every metric flag scaling issues before they bite.

None of these would land in a custom build for months.

## Risks

1. **Grafana Cloud pricing changes.** Same risk as any SaaS dependency. Mitigation: dashboards as code; self-host fallback is a Cloud Run container with the same JSON dashboards.

2. **The "ops view depends on Grafana JS" makes embedding awkward.** Mitigation: not a problem because the public status page can be a Grafana anonymous-public dashboard at `status.opengem.org`. Embeddable Grafana panels are well-supported.

3. **The visual style differs from the public dashboard.** Mitigation: this is fine — ops is internal, audience is engineers, terminal-density different from public, no design-language consolidation needed.

4. **Onboarding new engineers requires learning Grafana.** Mitigation: standard SRE knowledge, available everywhere.

## Cost summary

| Item | Y1 cost | Y2 cost |
|---|---|---|
| Grafana Cloud subscription | $0/mo | ~$30/mo |
| Initial dashboard build | 3 dev-days | (one-time) |
| Per-new-dashboard cost | ~30 min | (ongoing) |
| Migration to self-host (if ever) | 1 dev-week (one-time) | N/A |

## What this loop produced

- Confirmed Grafana as the ops-monitoring tool, with the **four-surface taxonomy** (public-interactive Next.js + public-static Observable + internal-authoring Streamlit + ops-monitoring Grafana) as the canonical OPENGEM frontend architecture.
- Listed the 6 dashboards we ship in Phase 5.
- Y1 operating cost: $0/mo. Y2: ~$30/mo.
- Reaffirmed: V&V matrix lives in Streamlit, not Grafana.

## What comes next

- **L091** — Observable Framework for explainer reports.
- **L120** — Live demo + onboarding flow (front door).
- **L265** — Telemetry + privacy-respecting analytics (Plausible/Umami) for public-side analytics, distinct from Grafana's internal ops view.
- **L285** — Accountability ledger page (which uses the public Grafana status page as evidence).

## Related

- [[L065-grafana]] — Phase 1 deep dive.
- [[L089-streamlit-vs-nextjs-dashboard-frontend]] — companion frontend picks.
- [[L091-observable-explainer-reports]] — third frontend.
- [[L265-telemetry-privacy-analytics]] — public-side analytics.
- [[L285-accountability-ledger]] — public-status-page consumer.
