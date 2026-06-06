# L014 — Finos Perspective: The Live Indicator Grid

**Loop**: 014 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## The repo at a glance

- **GitHub**: [github.com/finos/perspective](https://github.com/finos/perspective)
- **Stars**: ~10.9k, ~1.3k forks. Smaller than OpenBB/Qlib, larger than every "BI grid" alternative.
- **License**: **Apache 2.0**. Clean for OPENGEM redistribution. The trust line: maintained under the OpenJS Foundation; was originally JPM Treasury and is now a FINOS project (Fintech Open Source Foundation, the financial-services FOSS body).
- **Primary language**: C++ (the streaming query engine), with WASM compile target + TypeScript + Python + Rust bindings.
- **Last commit**: June 5, 2026. Active. Released the 3.x line throughout 2024-2026.
- **Maintainers**: Texodus / Andrew Stein and a small but consistent FINOS contributor pool. Not a one-person project — corporate sponsorship gives it predictable cadence.

## What it actually is

Perspective is **a streaming pivot/grid component for the browser, plus a Python WebSocket server**. The architecture has three layers:

1. **C++ core query engine** — a columnar, in-memory database with an `ExprTK`-derived expression language. Compiled to WASM for the browser and to native for Python/Node.
2. **Apache Arrow as wire format** — every update flows in as Arrow tables. This is the right choice — Arrow lets the same bytes round-trip from Python pipelines (pyarrow) through DuckDB/Polars without serialization tax.
3. **Custom Element UI (`<perspective-viewer>`)** — framework-agnostic Web Components: a pivot grid, 10+ chart types (line, bar, area, scatter, heatmap, treemap, sunburst, candlestick, etc.), filter/sort/group config persisted as JSON in the URL.

The killer move is that the same C++ engine runs in three places (browser via WASM, JupyterLab widget, Python WebSocket server), so you can prototype in a notebook, then move the same view config to a production dashboard without touching JS.

## Could OPENGEM use this for the live indicator grid?

**Yes — and it's probably the right call for one specific page (the indicator grid), not the right call for the whole dashboard.** Here's the breakdown.

### Where Perspective fits like a glove

- **The country-card × indicator-card grid (L161, L162)**. 200 countries × ~30 indicators × multiple horizons = ~30k cells with hover-to-spark, sortable, filterable, group-by-region. This is *exactly* the workload Perspective was designed for. No other open-source library does pivot-grid-of-financial-tiles as cleanly.
- **The "compare-2 mode" (L129)**. Group-by-country with side-by-side indicator comparison is a one-config-line in Perspective.
- **The methodology overlay (L172) and watchlist (L130)**. Both need a sortable/filterable grid that survives a reload. Perspective's URL-encoded view config is the right primitive.
- **The forecast leaderboard (L133, L184)**. Sortable by CRPS, log-score, hit rate, with group-by-model and filter-by-horizon. Perspective does this without writing chart code.

### Where Perspective does NOT fit

- **The forecast page chart (L195)**. Lightweight Charts (L015) is purpose-built for time-series with bands; Perspective's chart types are pivot-grid-derived and don't have a native "shaded forecast band with consensus overlay" idiom. Wrong tool.
- **The geopolitical pulse map (L163)**. globe.gl / Kepler.gl (L071, L101) own this; Perspective has no geo layer.
- **The narrative report (L198)**. Markdown + MDX, not a grid.

### Streaming model

Updates flow as Arrow tables over WebSocket from a Python server (`perspective-python` ships a `PerspectiveStarletteHandler` for FastAPI). On the browser side, you subscribe a `<perspective-viewer>` to a `Table` and call `table.update(arrow_bytes)` — the viewer recomputes incrementally. Benchmarked rows-per-second is in the millions on commodity laptops; for OPENGEM's *macro cadence* (daily-to-monthly releases — sub-Hz updates) this is overkill capacity, which is fine: capacity headroom is free.

### Bundle cost

WASM bundle is in the few-MB range (the docs are coy about exact numbers; the 3.x line shrank it materially). For a dashboard that's already shipping Plotly + Lightweight Charts + maybe globe.gl, a Perspective add is ~2–4 MB of additional gzipped JS+WASM. Acceptable if scoped to specific pages (the indicator grid, the leaderboard) and *lazy-loaded* with dynamic imports. **Hard rule: do not put `<perspective-viewer>` in the global app shell.**

### Browser support

Requires WebAssembly + ES2020 + (effectively) Chrome / Firefox / Safari current. No IE; no old Edge. For OPENGEM's audience (analysts on modern browsers, mobile via PWA), this is fine. Note that mobile Safari's WASM perf is materially worse than desktop Chrome — the indicator grid on iPhone will need a "lite" fallback (TanStack Table — L070).

## Cost-benefit

| Action | Cost (dev-weeks) | Benefit |
|---|---|---|
| Adopt Perspective for indicator grid + leaderboard pages | 2 (initial integration) + 0.5/quarter (version chase) | Eliminates a ~3-week hand-built grid + sort/filter + URL-state effort |
| Adopt Perspective for forecast page | N/A | Wrong tool — use Lightweight Charts |
| Bolt Perspective WebSocket server onto FastAPI backend | 1 | Live grid updates; mostly unnecessary at macro cadence |
| Ship Perspective only as static JSON download (skip WebSocket) | 0.5 | Simplest pattern; trade off live-updates for shipping speed |

**Recommendation**: ship Perspective for the indicator grid and the leaderboard, lazy-loaded, on a `/grid` and `/leaderboard` route. Skip the WebSocket server in v1; reload-on-poll is fine for monthly-release data. Add WebSocket in v2 when we have an Events stream (L127, L170) where it actually matters.

## Surprise of the loop

**Perspective ships as a Web Component, which means we can drop it into Next.js, Astro, plain HTML, Substack-embed iframe, or a static-site Datasette page without rewrites.** That portability is the unsung win. Every other "rich grid" lib (AG-Grid, TanStack, MUI DataGrid) is locked to a framework. Perspective's Custom Element wrapper is what makes the *embeddable widget* roadmap (L111, L144, L245) tractable. Single sourcetech across app + embed.

## What this loop produced

- Repo metadata + architecture summary.
- Page-by-page fit verdict (indicator grid + leaderboard = YES; forecast page + map + narrative = NO).
- WASM bundle / mobile-fallback note.
- WebSocket-vs-static decision deferred to v2.

## What comes next

- **L015** — Lightweight Charts: the time-series chart tool for the forecast page.
- **L070** — TanStack Table + AG Grid for fallback / non-WASM path.
- **L099** — Phase 2 deep dive: TanStack Table for Pro-grade grids — comparison head-to-head.
- **L111** — Embeddable widget design: Perspective's Custom Element advantage matters here.
- **L161 / L162** — Country/indicator-card grid: home of Perspective.

## Related

- [[L001-vision-statement]] — "terminal-grade view of the world economy" needs a grid that can hold 30k cells.
- [[L013-backtrader-vectorbt-zipline]] — Plotly subplot idioms for the forecast page; complement to Perspective for the grid.
- [[L015-lightweight-charts]] — the forecast-chart half of the visual stack.
- [[L070-tanstack-aggrid]] — fallback / direct competitor analysis.
- [[L161-country-card-grid]] / [[L162-indicator-card-grid]] — actual home pages.
