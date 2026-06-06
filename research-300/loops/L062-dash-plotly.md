# L062 — Dash (Plotly): When To Choose vs Streamlit, Enterprise Patterns, License, Cost

**Loop**: 062 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Thesis of this loop

Dash is "Streamlit for grown-ups who learned the hard way that script-rerun does not scale." It is a reactive Flask app with a React frontend, a callback-graph model, and a Plotly chart layer baked in. It is the *right* tool for the band of dashboard problems where (a) the audience is internal, (b) you want Python on the backend, and (c) you have outgrown Streamlit's rerun model but cannot stomach building a React app.

OPENGEM does not sit in that band. The public dashboard belongs in React/Next.js. But Dash deserves a hard look as the **operations dashboard** (internal monitoring of adapter health, pipeline status, V&V matrix, forecast leaderboards consumed by the OPENGEM team itself) — exactly the use case where Grafana is too time-series-narrow and Streamlit too laggy.

## What Dash is, technically

- A Python library that emits a React app at runtime. Flask serves it.
- Components are declarative (`html.Div`, `dcc.Graph`, `dcc.Dropdown`); behavior is wired via `@app.callback` decorators that name input/output component IDs.
- Reactivity is callback-graph based — a change to input `X` triggers callback `f(X) -> Y`, which updates output `Y`. No rerun-the-whole-script. This is the structural advantage over Streamlit.
- Plotly is the default chart layer. Other libs (Mapbox, Cytoscape, AG-Grid via `dash-ag-grid`) are first-class via official component packages.
- Async support via the `dash-extensions` ecosystem and (since 2024) native async callbacks.

License: **MIT** for Dash core, Plotly.js itself is MIT, and the official component packages are MIT. Dash Enterprise — the commercial layer — is closed-source, paid, and bundles SSO, role-based access, app marketplace, kubernetes deploys, and the "Design Kit." OSS Dash is genuinely capable; Dash Enterprise is for fortune-500-style needs OPENGEM does not have at V1.

## Where Dash beats Streamlit

1. **Concurrency**. The callback model means many users can hit one Flask process and the server only computes what each callback needs. The bottleneck shifts from "single script" to "individual callback compute." Behind gunicorn with N workers, a Dash app handles 500-2000 concurrent users on a 4-vCPU box for typical macro dashboards.
2. **State**. `dcc.Store` is honest browser-side state; component state survives partial updates. Streamlit's `st.session_state` is a leaky abstraction over the rerun model.
3. **Composable layouts**. Dash callbacks compose. Streamlit's "everything is global" mental model breaks down at ~20 widgets; Dash scales to hundreds.
4. **Embedding**. Dash apps can be embedded as iframes, and there is a "snapshot" pattern for static HTML exports. Still iframe-shaped, but cleaner.

## Where Dash loses

1. **Boilerplate**. The `Input`/`Output`/`State` callback signature is more verbose than Streamlit's "just write code." A 10-line Streamlit app is a 40-line Dash app.
2. **Theming**. Dash Bootstrap Components, Dash Mantine, and Dash AG-Grid each have their own theming model. The "no opinion" approach means you cobble; the result is rarely as polished as a hand-tuned Tailwind app. Bloomberg-density requires real CSS work.
3. **Mobile**. Dash apps are not mobile-first. They can be made responsive but the default templates are desktop-grid.
4. **SEO**. Same story as Streamlit — JS-rendered, no SSR by default, hostile to crawlers.

## Enterprise patterns worth stealing (even if OPENGEM never buys Dash Enterprise)

- **App registry pattern**: One Flask process hosts many Dash apps mounted at sub-paths (`/dashboard/inflation`, `/dashboard/gdp`). OPENGEM's ops view should do this for the indicator-by-indicator monitoring page.
- **Background callback pattern** (via Celery + Redis): Long-running computations don't block the user; the UI shows progress and updates when done. This is the right pattern for the forecast V&V matrix where re-scoring takes seconds-to-minutes.
- **Snapshot pattern**: Take a Dash app and freeze it to static HTML for distribution. Half-step toward Observable Framework's static-build philosophy.
- **`dash-bootstrap-components` grid system**: 12-column responsive grid that just works. Steal the layout pattern for the ops view.

## License and cost

- **Dash core**: MIT, free, forever.
- **Plotly.js**: MIT.
- **Plotly Resampler** (third-party, for million-point time-series): MIT.
- **Dash Enterprise**: Closed, ~$15-30k/year minimum based on industry hearsay; pricing is hand-shake-only and aimed at F500 buyers. **OPENGEM does not need this.**

Hosting cost for an internal ops Dash app:
- 2-vCPU Cloud Run with min-instances=1: ~$25-50/mo.
- 4-vCPU Fly.io machine with Redis sidecar: ~$60-120/mo.
- Behind Cloud IAP / Tailscale for auth: ~$10/mo additional for ID layer.

Practical floor for OPENGEM's ops view: **~$40/mo**.

## Ramp-up

- Python dev with Flask experience: 1 week to a basic ops view, 3-4 weeks to a polished one.
- The "callback graph debugging" learning curve is the steepest part. Dash DevTools (2.x+) reveal the graph; before you have it visualized, mysterious callback failures eat days.

## When OPENGEM picks Dash specifically

The OPENGEM operations dashboard — the internal "is the pipeline healthy, are forecasts up to date, has any country page gone stale, is the V&V matrix passing" — wants:

- Python backend (the OPENGEM core IS Python).
- Multiple concurrent ops users (Edgardo + collaborators).
- Charts that update independently (callback model wins).
- Auth (Cloud IAP or Tailscale, no need for Dash Enterprise SSO).
- Density (12-column grid, dense KPI cards).

This is exactly Dash's sweet spot. Grafana (L065) is too time-series-narrow for a V&V matrix that wants tables + tile grids + textual overlays. Superset (L063) is too "BI" for an ops view that wants imperative Python compute. Streamlit (L061) is too laggy under load. Dash threads the needle.

## Verdict

- **Public OPENGEM dashboard**: **SKIP**. Same SSR/SEO/embedding gaps as Streamlit; React/Next.js wins.
- **Internal OPENGEM ops dashboard (pipeline health, V&V matrix, leaderboard QA)**: **ADOPT-V1**. ~$40/mo, 1-2 weeks ramp.
- **Dash Enterprise**: **SKIP** forever. Not the right shape of buyer.

## Cost summary

| Use | Cost | Ramp |
|---|---|---|
| Internal ops dashboard | $40/mo | 2 weeks |
| Public dashboard | (skipped) | (skipped) |

## What comes next

- **L063** evaluates Superset as a self-host BI alternative for the ops view.
- **L065** evaluates Grafana, the time-series-first comparison point.

## Related

- [[L061-streamlit]] — why script-rerun model is wrong for public surfaces
- [[L065-grafana]] — alternative ops-monitoring stack, time-series-narrow
- [[L090-grafana-vs-custom]] — final ops-dashboard decision (Phase 2)
