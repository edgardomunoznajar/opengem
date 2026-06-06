# L064 — Metabase / Redash: SQL-First Dashboards, Free Tier, Hosting

**Loop**: 064 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Thesis of this loop

Metabase and Redash are the *commodity* end of the SQL-first BI market. They both let an analyst point at a database, write SQL, save a chart, drop the chart on a dashboard, and share a URL. Metabase is the live one; Redash is the zombie (Databricks-acquired in 2020, has not shipped a meaningful release since the 26.x line in 2024, sits in maintenance mode).

For OPENGEM, the question is not "is Metabase good" — it is good. The question is *whether SQL-first BI ever wins a slot in the OPENGEM stack*. The answer is "maybe one, for the casual-glance internal data exploration use case, but it competes hard with just dropping a Datasette (L076) on Postgres."

This loop: SKIP Redash. EVALUATE-LATER Metabase as a lightweight casual-query layer for non-Edgardo collaborators. Neither is the public dashboard.

## Metabase

- Java backend, React frontend, MIT-licensed open core ("Metabase OSS"), with paid "Pro" ($500/mo minimum, 2026 pricing) and "Enterprise" tiers for SSO, sandboxing, advanced caching, audit logs.
- Genuinely easy. The "Question Builder" lets non-SQL people drag and click their way to charts that aren't embarrassing. This is the differentiator vs Superset.
- Embedded dashboards are good but the *signed embedding* (the way you serve a customer-specific dashboard from your own app) is Pro-tier only. This caps OPENGEM's white-label embedding play if Metabase is the backend.
- 25+ DB drivers; PostgreSQL/BigQuery/Snowflake/MySQL all native and battle-tested.
- Caching is good in OSS, great in Pro.
- Auth: Google OAuth and SAML are OSS-free; granular permissions and row-level security are Pro-only.

OPENGEM's macro-scenario data is stored in TimescaleDB / Postgres today (per the broader repo). Pointing Metabase at it takes 10 minutes. The first dashboard takes another hour. The first *useful* dashboard takes a week, mostly to build the right materialized views.

## Redash

- Python (Flask + Celery) backend, Angular frontend, **BSD-2-Clause** licensed (very permissive).
- 35+ data sources via custom adapters.
- SQL-first, no query builder for non-SQL users — this is by design.
- Status: stalled. Latest meaningful release is 26.3.0 (March 2024). Databricks does not invest in Redash beyond keeping the lights on for existing customers. Community fork (`getredash/redash` mainline) gets a security patch every 4-6 months but no feature work.
- Do not adopt new Redash deployments in 2026. The pure-OSS replacement is Metabase OSS; the more powerful replacement is Superset.

## Why neither is the public dashboard

Same reasons as Superset (L063), more so:
- Aesthetics: stock BI. Metabase actively *avoids* terminal density in favor of breathable corporate dashboards. Bloomberg-orange is impossible without forking.
- Forecast bands: not a first-class chart type. Workarounds exist (custom JS visualization, or rendering Plotly into an embed) but you've left Metabase-land.
- SEO: auth-gated. The public-embedding model serves auth-bypass JWT links, not SEO-indexable HTML.
- Vintaging: dashboard definitions live in Metabase's internal Postgres. Version-controlled via export YAML but no native "as-of" view.
- Storytelling: Metabase has a "text card" — better than Superset's markdown, worse than Evidence.dev's markdown-first model.

## Where Metabase OSS *might* belong in OPENGEM

The internal collaborator who is *not* Edgardo and who wants to ask "what was Brazil's CPI YoY in March 2025 vintage" without learning SQL — Metabase serves them. Browser, login with Google, type the question, see a number. The friction floor matters because the second human onto the project will not learn the OPENGEM Python codebase to answer a one-off question.

But this is exactly the niche Datasette (L076) fills with even less ceremony, while *also* doubling as the public read-only data publishing layer. So Metabase competes against Datasette for the casual-internal-query slot, and Datasette has the strategic story (it's also the public surface) that Metabase does not.

## Hosting cost

- **Metabase OSS, self-hosted on Hetzner CX21 (~$8/mo)**: comfortable for a single-team usage. Bundled H2 metadata DB is fine for <10 users; promote to external Postgres at scale. Practical floor: $10/mo all-in.
- **Metabase Cloud**: starts at $85/mo for 5 users, scales linearly. Reasonable for teams.
- **Metabase Pro** (for signed embedding): $500/mo minimum. Forecast embedding into customer Substack via Metabase = $500/mo permanent overhead. Same outcome via Observable Framework (L066) or a custom React widget = free.
- **Redash self-hosted**: similar profile to Metabase, ~$10/mo. But again, do not adopt new in 2026.

## Ramp-up

- Metabase: 1 day to a running stack, 1 day to first chart. Fastest of all BI tools surveyed.
- Redash: same, but you're investing in a dead-end stack.

## Verdict

- **Redash**: **SKIP**. Dead.
- **Metabase OSS for internal one-off queries by non-Edgardo collaborators**: **EVALUATE-LATER**. Compete-test against Datasette (L076). Datasette likely wins because of strategic alignment with the public-ledger story.
- **Metabase Pro for white-label embedding**: **SKIP**. The cost is too high relative to a custom React widget.
- **Metabase as public OPENGEM dashboard**: **SKIP**. Wrong aesthetic; no terminal density.

## Cost summary

| Use | Cost | Ramp |
|---|---|---|
| Metabase OSS self-host | $10/mo | 2 days |
| Metabase Cloud | $85/mo | 1 hour |
| Metabase Pro | $500/mo | 1 hour |
| Redash | (skipped) | (skipped) |

## What comes next

- **L065** evaluates Grafana for the *time-series-shaped* slice of internal monitoring (different shape from BI).
- **L076** evaluates Datasette as the read-only public-ledger publishing layer that may also serve internal queries.

## Related

- [[L063-apache-superset]] — heavier, more capable alternative
- [[L076-datasette]] — the more strategic substitute for casual internal queries
- [[L067-evidence-dev]] — SQL+markdown competitor at the *public* end
