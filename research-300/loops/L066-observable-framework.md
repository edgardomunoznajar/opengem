# L066 — Observable Framework: The Static-Site Builder For Data Apps

**Loop**: 066 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Thesis of this loop

Observable Framework is the *most strategically aligned* dashboard tool surveyed in this Phase 1 sweep, and possibly the single most important discovery of the open-source landscape. It is a static-site generator for data apps — meaning the output is plain HTML/JS/CSS that can be deployed to GitHub Pages, S3+CloudFront, or Cloudflare Pages for ~$0/mo, *while still being a real interactive dashboard* with interactive charts, dropdowns, filters, and live data.

The architectural trick is **data loaders**: precomputed JSON/Parquet/CSV snapshots baked at build time. Every chart reads from a static file the browser fetches; every "interactive" filter is JS over already-fetched data. The result is genuinely instant, genuinely cheap, genuinely SEO-able.

This is *exactly* the architecture OPENGEM's public dashboard wants for the long tail (country × indicator pages, scenario explainer reports, methodology pages). And the explainer-report use case (per the Phase 0 vision) is Observable Framework's literal sweet spot.

This loop: **ADOPT-V1** for explainer reports + long-tail SEO pages. **EVALUATE-LATER** for the main dashboard surface (competes with Next.js + Tremor — both are good).

## What Observable Framework is

- Open source (**ISC license**, basically MIT-equivalent), maintained by Observable (the company behind observablehq.com).
- CLI tool: `observable build` produces a static site, `observable preview` runs a local dev server with hot reload.
- Authoring: Markdown files (`.md`) with embedded JavaScript code blocks. The JS runs in the browser. The Markdown becomes HTML.
- Data loaders: scripts in any language (Python, R, Bash, Node, etc.) that run at build time and emit static files. The dashboard reads the static files; the loader script can hit BigQuery, Postgres, or any API at build time.
- Components: D3, Observable Plot (a high-level grammar-of-graphics on top of D3 by Mike Bostock — the author of D3), htl (tagged template HTML), JS modules. All composable.
- Theming: CSS variables, dark mode, a configurable theme system. Less polished than Tremor; more polished than Datasette.
- Deployment: any static host. Observable Cloud is a paid hosted option but completely optional.

## Why this is strategically aligned with OPENGEM

1. **Numbers come with their own report card.** Observable Framework's data-loader architecture makes "publish the data alongside the chart" *the default* — every chart's underlying data is a static JSON/Parquet on the same domain, downloadable, citable. The OWID-style "click-through to download the data" trust signal is built in for free.

2. **Vintaging is git-natural.** The site is a static build. The build output is committed to a `dist/` branch (or republished to S3 with a vintage prefix `v/2026-06-06/`). The vintage URL is permanent. Linking to "this is the dashboard as it appeared on 2026-06-06" is *trivial* — the vintage is just another git tag.

3. **SEO works.** Static HTML, server-side rendered at build time. Every country page, every indicator page, every scenario page is a real URL with real HTML. TradingEconomics's SEO moat (the country×indicator long-tail matrix) becomes attackable.

4. **Cheap forever.** $0/mo on GitHub Pages or Cloudflare Pages. ~$5/mo on S3+CloudFront. Costs are *traffic*, not compute — and the traffic costs scale linearly, not super-linearly like a Streamlit/Dash deploy.

5. **Embedded distribution.** Static JS bundles are embeddable in Substack, Medium, anywhere. The "JSON-block-per-chart" affordance from the vision statement is a 10-line Observable component.

6. **Build-time data loaders unify the ingestion + presentation stack.** A loader script can call the OPENGEM Python adapter library, return a Parquet, and the chart reads it. No separate API tier needed for the public dashboard. (The API tier still exists for paid customers and MCP; the public dashboard is *static* and doesn't depend on it.)

7. **Observable Plot is the right chart grammar.** Plot is the modern successor to Vega-Lite, designed by the D3 author. Forecast bands, area-with-bands, sparklines, stacked-area-with-annotations — all 5-line components. See L069 for a deeper Plot vs Vega-Altair vs Plotly comparison.

## Where Observable Framework loses

1. **Not real-time.** Built once, deployed, served. The "live ticker" effect requires either a build-and-deploy every N minutes (cheap for daily-cadence OPENGEM data; impractical for sub-minute) or a small client-side JS polling layer. For OPENGEM's daily/weekly/monthly cadence, this is *fine*. For a real-time intraday feed, this is wrong (but OPENGEM is explicitly not a real-time intraday product per L001).

2. **Interactive cross-page state is awkward.** Each page is independent. A "watchlist" across pages requires localStorage + a small JS layer. Doable; not as ergonomic as a React app.

3. **Auth is bring-your-own.** Static sites have no auth. The free public dashboard is happy with that; the paid-tier features (API throughput, MCP throughput, branded tearsheets) live elsewhere.

4. **Build times grow with data volume.** A site with 200 countries × 50 indicators × 10 years of data has 100k chart-equivalents. Build time can hit 30+ minutes if every chart re-loads. The mitigation is incremental builds, but Framework's incremental support is OK-not-great as of mid-2026.

5. **The "I want a React component library" itch.** Observable doesn't ship a shadcn-style component library. The aesthetic is custom-CSS-or-die. The polished examples (`examples/api`, `examples/eia`) show it's *possible* to look terminal-grade, but it's CSS work.

## Specimen inspection

The cloned repo (`research-300/clones/observable-framework/`) ships ~40 example projects under `examples/`. Notable for OPENGEM:

- `examples/eia` — Energy Information Administration dashboard. Forecast charts, time-series with annotations, area-with-bands. Directly analogous to OPENGEM's energy indicators.
- `examples/api` — pulling data from an API at build time. Direct template for the OPENGEM Python adapter integration.
- `examples/datawrapper-api` — composing with an external chart service.
- `examples/loader-postgres` — Postgres-backed data loader. Template for OPENGEM's TimescaleDB integration.
- `examples/hotel-bookings` — multi-chart dashboard with cross-filtering. Layout template.
- `examples/geotiff` — geo data. Relevant for the geopolitical pulse map (though L071 has it living in globe.gl).

## Hosting cost

- **GitHub Pages**: $0/mo. Bandwidth limit is 100GB/mo soft cap, fine for Y1.
- **Cloudflare Pages**: $0/mo for free tier, unlimited bandwidth. Recommended.
- **S3 + CloudFront**: $5-15/mo at typical Y1 traffic.
- **Observable Cloud**: paid, optional. Skip until there's a reason.

## Ramp-up

- A competent JS+Python dev: 1 day to a running site, 1 week to the first useful page (country page), 4-6 weeks to a polished multi-page site with shared layout, navigation, and 200+ generated pages.
- The Markdown+JS authoring model is fast once internalized; the *first* page takes a day, the next 50 take an hour each because they're templated.

## Verdict

- **OPENGEM explainer reports / methodology pages**: **ADOPT-V1**. Perfect fit. $0/mo. 2-week ramp.
- **OPENGEM long-tail country×indicator SEO pages**: **ADOPT-V1**. Templated static builds. The TradingEconomics moat-attack lives here.
- **OPENGEM main dashboard (homepage, terminal-grade live view)**: **EVALUATE-LATER**. Competes with Next.js + Tremor (L073). Decision likely: Observable Framework for the *long-tail static* pages, Next.js for the *interactive terminal* surface. Both, not one.
- **Vintaging the dashboard itself**: **ADOPT-V1**. The git-tag-as-vintage pattern is the right one.

## Cost summary

| Use | Cost | Ramp |
|---|---|---|
| Cloudflare Pages | $0/mo | 2 weeks |
| GitHub Pages | $0/mo | 2 weeks |
| S3+CloudFront | $5-15/mo | 2 weeks |
| Observable Cloud | (skipped) | (skipped) |

## What comes next

- **L067** evaluates Evidence.dev, the SQL-first analytics builder with similar static-site DNA.
- **L091** dives deeper on Observable Framework for explainer reports specifically (Phase 2).

## Related

- [[L069-d3-vega-plotly]] — Observable Plot is the natural chart grammar inside Framework
- [[L073-next-tailwind-dashboard-starters]] — competes (and complements) Observable for the interactive surface
- [[L091-observable-explainer-reports]] — Phase 2 deep dive
- [[L095-datasette-public-ledger]] — sister-strategy public-ledger surface
