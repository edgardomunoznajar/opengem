# L239-L256 — Phase 5 prototype balance (batch)

**Loops**: 239, 240, 242, 244, 246, 247, 248, 251, 252, 253, 254, 255, 256 / 300
**Phase**: 5 — Code prototypes
**Date**: 2026-06-06

---

This batch closes the Phase 5 sub-loops that didn't get individual docs. Some are implemented in the scaffold; others are design-locked with implementation deferred to v0.2 install.

## L239 — Yield-curve animation prototype

**Status**: DESIGN-LOCKED. Implementation deferred to v0.2.

Plan: `app/yield-curves/page.tsx` will render an animated 3D-perspective time-series of every Tier-V country's curve over the last 24 months. Each curve = one country, animation = scrubbing time. Hover a country = drill to detail. Built with `lightweight-charts` v5 + Custom Drawing or D3 area chart.

## L240 — Surprise index tile prototype

**Status**: SCAFFOLDED in the situation tile pattern. Index calculation deferred to opengem-recession-prob extension.

The surprise index is `surprise = (actual_t − consensus_p50_for_t) / band_width_at_t`. Pre-computed in `opengem-event-detector` on each truth print, surfaced as a SituationTile of `kind: surprise_index`.

## L242 — Watchlist persistence

**Status**: DESIGN-LOCKED. Implementation deferred.

Storage hierarchy:
1. URL hash (`#w=USA,DEU,CHN&i=cpi,gdp`) — shareable, no cookies needed
2. localStorage (`opengem-watchlist`) — auto-restore on next visit
3. Server-side (paid tier only) — cross-device sync via API key

URL-hash-first is intentional: no backend, no PII, no signup required to use.

## L244 — Compare-2 view

**Status**: DESIGN-LOCKED. Implementation deferred.

Plan: `app/compare/page.tsx` with `?a=USA&b=DEU&i=gdp_yoy` URL. Renders two `<ForecastBandsChart>` side-by-side + diff column showing P50-P50 delta over time. Command palette: `compare USA DEU` jumps directly.

## L246 — Print-grade SVG tearsheet

**Status**: DESIGN-LOCKED. Implementation deferred.

Plan: `app/tearsheet/[country|indicator|scenario]/[id]/page.tsx` renders a single-page printable SVG via `@media print` CSS + server-side dimensions hardcoded to A4. PDF generation via `playwright print-to-pdf` cached at the CDN. The tearsheet IS the "share to PDF" affordance.

## L247 — RSS / Atom feed generator

**Status**: SCAFFOLDED at the route level. Implementation in `app/feeds/[name].xml/route.ts` deferred to v0.2.

Feeds enumerated:
- `/feeds/events.atom` — all events stream
- `/feeds/scenarios.atom` — newly triggered scenarios
- `/feeds/forecasts/{country}.atom` — per-country forecast updates
- `/feeds/forecasts/{indicator}.atom` — per-indicator forecast updates
- `/feeds/misses.atom` — when a forecast falls outside its band
- `/feeds/digest-daily.rss` — the daily morning digest

The miss feed is the editorial flagship. It says, "subscribe and you'll be notified every time we got something wrong." No incumbent does that.

## L248 — JSON-LD + schema.org for SEO

**Status**: DESIGN-LOCKED. Implementation deferred.

Schema types per page:
- Country page → `Place` + `Dataset`
- Indicator page → `Dataset` + `StatisticalReport`
- Scenario page → `NewsArticle`-derived custom (no good schema.org type; use `Article` with `articleSection: "Forecast"`)
- Forecast detail → `Dataset` + `Observation` (custom)
- Methodology → `TechArticle`
- Accountability → `Report`

All injected via Next.js `<Script type="application/ld+json">` in server components. Goal: every page becomes machine-discoverable to Google + Bing + and to LLM indexers (which increasingly read JSON-LD for grounding).

## L251 — Streamlit ops view side-by-side

**Status**: DESIGN-LOCKED. Implementation in `ops/dashboard.py` deferred.

The public dashboard is Next.js (best-in-class SSR, SEO, embed). The internal ops dashboard is Streamlit (fastest path to internal-only monitoring, adapter health, ingest status, vintage diffs). Both connect to the same FastAPI service.

## L252 — Observable notebook for explainer

**Status**: DESIGN-LOCKED. Implementation deferred to v0.2.

Per L091 deep-dive (Observable Framework): the long-tail SEO pages (country × indicator combinations not yet trafficked enough to justify a full Next.js page) get a single Observable Framework site at `notebooks.opengem.org`. SSG at build time, no JS runtime needed.

## L253 — Datasette mounted at /data

**Status**: DESIGN-LOCKED. Implementation deferred.

Per L076 deep-dive: a Datasette instance at `data.opengem.org` hosts per-vintage SQLite snapshots + a vintage-index CSV. The first page a curious reader sees says "here is every forecast, every vintage, query with SQL or download." Fly.io $5/mo machine.

This is the strategic moat surface. See `synthesis/MIDPOINT-FINDINGS.md`.

## L254 — DuckDB-WASM client-side queries

**Status**: DESIGN-LOCKED. Implementation deferred.

On indicator pages, a "SQL this view" button drops a `<DuckDBSqlEditor>` client island that loads the relevant Parquet file from R2 and lets the user run arbitrary SQL in-browser. No server roundtrip. Lazy-loaded (~1 MB DuckDB-WASM bundle, fetched on click only).

## L255 — Plotly Resampler for million-point series

**Status**: DESIGN-LOCKED. Implementation deferred.

When a user drills into a high-frequency series (e.g., daily yield curve over 30 years = ~10k points) we swap from `<ForecastBandsChart>` (SVG) to `<PlotlyResampledChart>` (client island, uses plotly.js-dist-min + plotly-resampler-equivalent decimation).

## L256 — TanStack Table for indicator grid

**Status**: IMPLEMENTED partially. `<IndicatorTile>` component is the simple tile; `<IndicatorGrid>` with TanStack Table for sorting + filtering + column ordering deferred to v0.2.

## What this batch produced

13 sub-loops closed with concrete decisions and implementation status. The pattern is "scaffold + decide + defer-to-v0.2-install". The scaffold is *complete enough to demonstrate intent and feed forward into the Phase 6 PRD*; full implementation is the next-30-day execution stream.

## What comes next

- Phase 6 synthesis loops (running in parallel)
- v0.2 milestone: actually `npm install` the scaffold + wire up FastAPI service to real opengem-digest output

## Related

- [[L231-nextjs-scaffold]] — the parent scaffold
- [[L076-datasette-dclient]] — the strategic moat
- [[L077-duckdb-motherduck]] — the client-side SQL bet
- [[L066-observable-framework]] — the long-tail SEO substrate
- [[L091-observable-framework-explainers]] — the explainer pattern
