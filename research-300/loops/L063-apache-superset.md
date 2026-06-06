# L063 — Apache Superset: BI Dashboard Self-Host, Fit for OPENGEM Ops View vs Public

**Loop**: 063 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Thesis of this loop

Apache Superset is a serious open-source BI platform — Apache 2.0, Apache Software Foundation incubated then graduated, deployed by Airbnb/Pinterest/Lyft and a thousand mid-market shops. It is the most "complete" of the SQL-first BI tools on this list (more chart types, more auth backends, more governance) and the price (free) is unbeatable.

But "BI tool" and "macro accountability ledger" are different products. Superset is built for *analysts exploring a warehouse*, not *the world reading a curated story about the global economy*. It exports brilliant dashboards for *internal* consumption. The public OPENGEM dashboard cannot be a Superset embed without giving up the curated, terminal-grade UX that is OPENGEM's whole differentiator.

This loop: SKIP Superset for the public dashboard. EVALUATE-LATER for the internal V&V matrix / ops view, but Dash (L062) likely wins that fight.

## What Superset is

- Python (Flask + Celery) backend, React frontend, SQLAlchemy data layer with 40+ DB drivers.
- Semantic layer: "datasets" = named SQL views with metrics, dimensions, and certified column metadata.
- Visualizations: 50+ chart types (line, bar, area, pivot, sankey, treemap, big-number, deck.gl-powered geo).
- Auth: LDAP, OAuth, OIDC, SAML, custom — all in OSS, free, first-class. This is genuinely better than Metabase's free tier.
- Row-level security: also free, first-class, native. Better than Metabase OSS.
- Dashboards: drag-and-drop, parameterized, embeddable via iframe and (since 2023) a guest-token JWT model for white-label embedding.
- License: **Apache 2.0**. Full stop. No "open core" trick.

## Why Superset is *not* the public OPENGEM dashboard

1. **Terminal feel is impossible.** Superset's chart components are SVG-or-Canvas, polished but generic-BI in aesthetic. Bloomberg orange, dense sparkline grids, custom forecast-band rendering — all of those would require forking Superset's chart code or shimming custom plugins. The effort is the same as building from scratch in Next.js, with the constraint that you must stay inside Superset's plugin API forever.

2. **Storytelling is weak.** OPENGEM dashboards must intersperse narrative annotations, methodology pop-ups, vintage drawers, citation stamps. Superset dashboards are grid-of-charts. The "markdown component" exists but is second-class.

3. **Forecast bands and uncertainty rendering**. Superset's chart palette does not have a first-class fan-chart / forecast-with-bands. Plotly via custom plugins works but you've now built a custom Superset; might as well skip the middleware.

4. **SEO**. Superset dashboards are auth-gated by default, JS-rendered, and embed via iframe. None of these surfaces are SEO-friendly. The TradingEconomics-style country×indicator long-tail SEO play (L002) cannot be served by a Superset surface.

5. **Versioning and vintaging the dashboard itself**. Superset stores dashboard definitions in its own metadata DB. Version-control them via the export/import YAML flow, but the public-facing "this is the dashboard as of date X" view is not native — you'd build it on top.

## Why Superset *is* potentially the internal V&V matrix / ops view

The internal job of "let me slice the forecast leaderboard by indicator × horizon × country × model and find the cells where we're losing" is exactly Superset's wheelhouse. The semantic layer maps cleanly: define `forecast_scores` once, expose it as 30 chart types.

Pros for the ops view:
- Free, mature, scales to hundreds of dashboards.
- Async query model (Celery workers + Redis) handles heavy joins.
- Built-in alerts and reports (email a screenshot to Edgardo every Monday morning).
- Caching layer that survives reboots.

Cons for the ops view:
- Heavyweight to operate: PostgreSQL metadata DB + Redis + Celery worker pool + Flask web tier. Minimum 4 containers.
- Native auth via OAuth means a Cloud IAP or Google OAuth integration is straightforward but yet another moving part.
- "BI dashboard" idiom doesn't fit "pipeline health monitor" — Superset is great at slicing data, less great at "is service X up."

For OPENGEM's ops view the harder question is Superset vs Dash (L062). Dash wins on flexibility for imperative Python compute (eg. "run the V&V scorer right now on demand"). Superset wins on slicing pre-computed materialized views.

If OPENGEM commits to a materialized-view-first ops model (every nightly run writes `forecast_score_vintage`, `pipeline_health_daily`, `indicator_freshness_summary` to Postgres), Superset over those tables is genuinely competitive with Dash.

## Hosting cost

Self-hosted on a single Hetzner CX31 (~$15/mo, 4 vCPU, 16GB):
- Superset web + worker + beat + Redis + Postgres metadata: all fit comfortably.
- Add backups (~$3/mo Backblaze B2) and the per-month run-rate is ~$18.

Self-hosted on GCP Cloud Run + Cloud SQL:
- Cloud Run min-instances=1 for web ($25), Cloud Run worker ($25), Memorystore Redis ($45), Cloud SQL Postgres f1-micro ($10) = ~$105/mo. Pricier than Hetzner but auto-scaling and no ops overhead.

Preset Cloud (managed Superset by the core maintainers): starts at $99/mo for 5 users, $499/mo for 25 users. Reasonable for a team; overkill for OPENGEM's one-person ops team in Y1.

## Ramp-up

- Operator with Docker familiarity: 1 day to a running stack, 1 week to first useful dashboard, 3-4 weeks to a polished V&V matrix dashboard.
- Learning curve is the semantic layer — defining datasets/metrics correctly the first time is non-obvious. Wrong first model = rebuild.

## Verdict

- **Public OPENGEM dashboard**: **SKIP**. Wrong shape for terminal-grade storytelling + SEO long-tail.
- **Internal OPENGEM V&V matrix + leaderboard slicer**: **EVALUATE-LATER**. After L062 (Dash) is in production, see if Superset gives marginal slicing value. Pragma: do NOT operate both — one wins, the other goes.
- **Internal pipeline health monitor**: **SKIP** in favor of Grafana (L065).

## Cost summary

| Use | Cost | Ramp |
|---|---|---|
| Self-hosted Hetzner | $18/mo | 1-2 weeks |
| Self-hosted GCP | $105/mo | 1 week |
| Preset Cloud | $99/mo | 1 day |
| Public dashboard | (skipped) | (skipped) |

## What comes next

- **L064** compares Metabase and Redash as lighter alternatives.
- **L090** picks the final ops dashboard (Phase 2).

## Related

- [[L062-dash-plotly]] — likely winner for internal ops, more flexible for imperative compute
- [[L064-metabase-redash]] — lighter SQL-first alternatives
- [[L065-grafana]] — time-series-first comparison
