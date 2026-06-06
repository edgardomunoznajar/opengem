# L065 — Grafana: Time-Series-First Dashboard, Plugin Ecosystem, Free OSS vs Cloud

**Loop**: 065 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Thesis of this loop

Grafana is the *single most successful* open-source dashboard tool of the last decade. It owns the SRE/devops/observability bucket completely, has a serious push into BI-adjacent territory (since the 9.x and 10.x lines added richer chart types and the explore UI), and ships an open plugin model that lets any datasource integrate in days.

For OPENGEM, Grafana is the obvious right tool for *one specific slot*: the operational monitoring of pipeline health, ingestion freshness, API latency, MCP throughput, error budgets. It is also tempting to lean on Grafana for the V&V matrix view but that is *outside* its sweet spot and the wrong call.

This loop: ADOPT-V1 for ops/observability monitoring. SKIP for public dashboard. SKIP for the V&V matrix (Dash L062 wins there).

## What Grafana is

- Apache 2.0 licensed core (was AGPL briefly; 2.0 since 2021).
- Single Go binary, runs anywhere, scales by adding instances behind a load balancer.
- Datasource plugins for Prometheus (native), InfluxDB (native), Postgres (native), MySQL, BigQuery (commercial plugin by Grafana Labs, but the open `simpod-json-datasource` works for read-only API queries), Loki, Tempo, Elasticsearch, OpenTelemetry, CloudWatch, Stackdriver, plus 100+ community plugins.
- Alerting: first-class, with provisioning via YAML files, integration with PagerDuty/Slack/email/webhooks.
- Annotations: first-class. A pipeline event (deploy, schema change, forecast vintage rollover) becomes a vertical line across every chart — exactly the affordance OPENGEM's ops view wants for "we deployed at 14:23, did anything break?"
- Dashboards as code: JSON model, version-controlled, deployable via the Grafana provisioning API or Grafana Operator (k8s).

## Grafana Cloud free tier (2026)

The 2026 free tier is genuinely generous and unchanged in its basic structure from 2024:
- 10,000 active metric series (Prometheus / Mimir backend).
- 50 GB logs (Loki).
- 50 GB traces (Tempo).
- 50 GB profiles (Pyroscope).
- 500 VUh of k6 load testing.
- 3 users, 14-day retention.

For OPENGEM's Y1 ops footprint — maybe 200 active series (one per indicator × adapter health), <10 GB logs/mo — the free tier covers it entirely. Practical cost: **$0/mo through Y1**.

Past 10k series or 14 days retention, Grafana Cloud Pro starts at $0.016 per series per month and $0.50/GB-month of logs at 30-day retention. For a typical 50k-series macro ops footprint with 30-day retention: roughly $30-60/mo. Cheap.

## Plugin ecosystem reality

- **BigQuery plugin** (Grafana Labs official): commercial. Free tier exists but production usage requires an entitlement (~$50/mo per stack). Workaround: use the JSON datasource against your own API, which is free and works fine for slow-cadence macro data.
- **JSON / Infinity datasource** (community, free, MIT): read any JSON HTTP endpoint as a Grafana datasource. This is the *escape hatch* — for OPENGEM, every indicator can be exposed via the OPENGEM JSON API and Grafana renders it for free.
- **Postgres / TimescaleDB native datasource**: free, fast, what you want for the bulk of the ops view.
- **Plotly panel** (community): drop a Plotly chart into Grafana. Useful for the rare chart type Grafana doesn't ship.
- **Polystat / Stat / Geomap panels**: native, capable, fine for the "current value with sparkline" panel that OPENGEM's ops view needs everywhere.

## Where Grafana shines for OPENGEM

1. **Pipeline health**. Every adapter writes a heartbeat to Postgres or pushes a metric. Grafana renders the "is everything green" tile grid. 30 minutes of work.
2. **Ingestion freshness**. Each series has a `last_value_ts` column. Grafana shows the staleness heatmap. Color-coded.
3. **API + MCP latency / throughput**. Prometheus middleware in FastAPI; Grafana renders p50/p95/p99. Standard.
4. **Annotation timeline**. Deploys, schema migrations, forecast vintage rollovers — annotations across all charts.
5. **Alerting**. "If any indicator is more than 7 days stale and was supposed to update daily, page Edgardo." Standard.
6. **Public status page** (Y2-Y3): a public Grafana with the ops view exposed read-only is the "we publish our reliability" angle of the broader transparency thesis. Grafana supports anonymous read-only public dashboards.

## Where Grafana loses for OPENGEM

1. **Not a country page**. The Bloomberg-style indicator+sparkline+forecast-band grid for a country is *not* Grafana's job. Grafana is heatmaps + time series + numeric stats. The narrative density of a country page belongs in the Next.js surface.
2. **Not the V&V matrix**. The matrix is "indicator × horizon × model × vintage → score color." Grafana's `state-timeline` and `heatmap` panels approximate but lose the per-cell drill-down behavior. Dash (L062) wins.
3. **Not the forecast leaderboard**. The leaderboard is a sortable, filterable, drill-down-able grid. AG-Grid in Next.js (L070) wins.
4. **Not the storytelling**. Annotations are the closest Grafana gets to narrative; it's not enough.

## Hosting cost

- **Grafana OSS self-hosted on Hetzner CX11 (~$4/mo)**: trivially sufficient. Add Postgres (existing) and you're done.
- **Grafana OSS on Cloud Run with Postgres backend**: ~$15/mo.
- **Grafana Cloud free**: $0/mo through Y1, scales to ~$50/mo at modest growth.

Recommendation: **start on Grafana Cloud free**. It's $0, the data backend is Mimir/Loki/Tempo which you don't have to operate, and the upgrade path is trivial. If Grafana Labs becomes obnoxious about pricing in Y2-Y3, migrate to self-hosted OSS in a weekend.

## Ramp-up

- Day 1: Grafana Cloud account, Prometheus scrape config, first dashboard.
- Day 2: Postgres datasource, first ingestion freshness panel.
- Week 1: Full ops view (pipeline health + freshness + latency).
- Week 2: Alerting + Slack webhook integration.

This is the *fastest* OPENGEM gets a useful ops dashboard, by a wide margin.

## Verdict

- **Public OPENGEM dashboard**: **SKIP**.
- **Internal OPENGEM ops view (pipeline + ingestion + API)**: **ADOPT-V1**. $0/mo on Grafana Cloud free. 1-2 weeks ramp.
- **Internal V&V matrix**: **SKIP** in favor of Dash (L062).
- **Public status page (Y2-Y3)**: **EVALUATE-LATER**. Grafana anonymous-read mode is good but a hand-built Next.js status page may tell the story better.

## Cost summary

| Use | Cost | Ramp |
|---|---|---|
| Grafana Cloud free (Y1) | $0/mo | 1 week |
| Grafana OSS self-host | $4/mo | 2 weeks |
| Grafana Cloud Pro (scale) | ~$50/mo | 1 day to migrate |
| Public dashboard | (skipped) | (skipped) |

## What comes next

- **L066** evaluates Observable Framework, the static-build alternative that may actually win the public dashboard.
- **L090** consolidates the ops dashboard decision (Phase 2).

## Related

- [[L062-dash-plotly]] — V&V matrix
- [[L090-grafana-vs-custom]] — final ops dashboard decision
- [[L103-fastapi-prometheus]] — the metric source feeding Grafana
