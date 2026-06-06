# L015 — TradingView Lightweight Charts: Forecast Bands and Consensus Overlay

**Loop**: 015 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## The repo at a glance

- **GitHub**: [github.com/tradingview/lightweight-charts](https://github.com/tradingview/lightweight-charts)
- **Stars**: ~16.1k. Far ahead of d3-financial-chart and react-stockcharts; the de facto open-source TradingView-style chart.
- **License**: **Apache 2.0** — *with an attribution clause*. You must display a "TradingView" attribution link on any public page using it. The `attributionLogo` chart option satisfies the requirement automatically.
- **Primary language**: TypeScript.
- **Last commit**: June 2026. Active. Backed by TradingView itself, who use it for their own free/light charts.
- **Bundle size**: among the smallest in the category — "close to static images" (per docs). Practical ballpark: ~40–60 KB gzipped for the core. There is no WASM.
- **Renderer**: HTML5 Canvas. No SVG, no WebGL. Excellent perf for 50k–200k point series; degrades above ~500k points without server-side downsampling (see L100, L255 — Plotly Resampler analog).
- **Browser support**: ES2020 baseline. Chrome / Firefox / Safari / Edge current; everything mobile post-2020.

## What it actually is

A focused, opinionated, deliberately small charting library for financial time series. The team's design constraint is "the smallest financial chart that's still production-grade." That means a tight series-type list (Area, Bar, Baseline, Candlestick, Histogram, Line), a strict time-scale model, an `addSeries` / `setData` / `update` API surface, and no fancy multi-axis-multi-panel composition out of the box. Everything beyond the core six series types is delivered via **plugins** (custom series + primitives), introduced in version 4.1.

## The forecast-bands question

OPENGEM's forecast page (L195) needs to render, at minimum:

1. A central point forecast (P50) — solid line.
2. A confidence band (P10–P90, or P5–P95) — shaded region.
3. (optional) A 50% inner band (P25–P75) — darker shaded region.
4. A consensus overlay — IMF WEO / OECD EO / ECB SPF / FRB SEP — dashed lines or shaded ribbon.
5. A vertical "today" marker separating realized from forecast.
6. A history of revisions, faded — vintage lines (L173 vintage rewinder).

### What Lightweight Charts ships out of the box

- Line series — central forecast: solved.
- Area series — single shaded region from baseline. Not directly a "band between two lines."
- Baseline series — area with two different fills above/below a reference value. Not a band.
- Histogram — irrelevant here.

So out of the box, **there's no built-in confidence band**. But:

### Plugin path (the actual answer)

The plugin example library includes:

- **Bands Indicator primitive** — draws a filled area band surrounding a base line series. This is the closest fit: "central line + envelope" is exactly the P10/P50/P90 shape.
- **HLC Area Series** — plots high/low/close with shaded area between close and the H/L. Designed for OHLC, but the *rendering pattern* (two boundary series + interior fill) is identical to a confidence band. We can fork this plugin and rename `high/low` → `upper/lower`, `close` → `median`. ~1 day of work.
- **Brushable Area Series** — interactive area for "what-if" cursor.

For multi-band (P10/P90 outer + P25/P75 inner), we'd stack two band plugin instances with different opacities. Tested pattern in the community; production-ready.

### Consensus overlay

Multiple `addLineSeries` calls with custom dashed `lineStyle` — solved trivially. The library handles 10+ concurrent line series well.

### Vintage rewinder (L173)

The library supports `setVisibleRange` / `setVisibleLogicalRange` programmatically. For the "rewind to Sept 2024" UX we set the chart visible range, swap in a different vintage's data, and re-render. No special support needed; works at canvas-native speeds.

### Vertical "today" line

Custom plugin (`Primitives` API) — about 20 lines of TypeScript. Several open-source examples exist in the plugin-examples repo.

## The attribution clause

The Apache 2.0 + attribution model is *unusual* but not legally onerous. We must show a TradingView credit somewhere on each public page using the library. The default `attributionLogo: true` option places a small TradingView watermark in the corner of every chart. This is acceptable for:

- The public dashboard (where it's already standard for "powered by" footers).
- Embeddable widgets (we already plan to include a "powered by OPENGEM" badge — add a "charts by TradingView" sibling).
- Substack syndication and YouTube b-roll (L113) — TradingView attribution travels along, which is fine.

For the *paid white-label embed* tier (L144), this is mildly awkward. White-label customers want only their own brand visible. There's no commercial license available that drops the attribution. **Workaround**: white-label embeds use a different chart library (e.g. self-rendered SVG via D3, or our own Canvas2D layer). For the free dashboard, Lightweight Charts is correct.

## Comparison head-to-head with the alternatives

| Library | License | Bundle | Series types | Bands native | Mobile | Verdict |
|---|---|---|---|---|---|---|
| **Lightweight Charts** | Apache 2.0 + attribution | ~50 KB | 6 core + plugins | Via Bands primitive plugin | Excellent | Pick for forecast page |
| **Plotly.js** | MIT | ~3 MB (full) / ~1 MB (slim) | 40+ | Yes (`fill='tonexty'`) | Good | Pick for ops view / one-off exploration |
| **Highcharts** | Commercial / Non-commercial free | ~200 KB | Many | Yes (arearange) | Excellent | License-incompatible with OPENGEM's open thesis |
| **ApexCharts** | MIT | ~300 KB | Many | Yes (rangeArea) | Good | Heavier, less crisp |
| **Recharts** | MIT | ~140 KB | Many | Manual via `Area` between datasets | OK | React-only; design isn't financial-chart-grade |
| **D3 + custom** | BSD | varies | Build it | Build it | Build it | Highest ceiling, highest cost |

Lightweight Charts wins on **bundle size**, **canvas performance**, **financial-chart visual idiom**, and **license compatibility (with attribution accepted)**. Plotly wins on **range of chart types** and **ease of mixing chart kinds in one figure** — which is why we use both: Plotly for ops/exploration and the JSON-block-per-chart distribution wedge (L065), Lightweight Charts for the production forecast page and the embeddable widget.

## Cost-benefit

| Action | Cost | Benefit |
|---|---|---|
| Use Lightweight Charts on forecast page + indicator page + embed widget | 2 weeks initial + maintenance | Production-grade forecast bands, small bundle, fast |
| Fork Bands Indicator plugin → ConfidenceBand plugin | 1 day | Custom band styling matched to OPENGEM palette (L148) |
| Build a SeriesOverlay wrapper for consensus comparison | 3 days | Idiomatic API for our analysts |
| Build a VintageRewinder controller | 3 days | Powers L173 vintage time machine |
| Build a "PoweredBy" attribution component | 0.5 day | Centralizes the legal hook |
| Build white-label alternative chart for paid embeds | 2–3 weeks (deferred to v2) | Required for paid white-label tier (L144) |

## Surprise of the loop

**The plugin system is genuinely good and well-documented, but you have to know to look for it.** The README and the marketing site emphasize "six series types" as if that's the ceiling. The actual ceiling is "six built-in series plus a clean plugin API for anything else." Anyone evaluating Lightweight Charts who stops at the README will incorrectly conclude "no bands, no good." The right way to think about Lightweight Charts is *as a canvas-rendering and time-scale runtime*, with plugins as the rest.

## What this loop produced

- Repo metadata + attribution-clause flag.
- Concrete forecast-page render plan: central line + Bands plugin + dashed consensus + vertical today + vintage swap.
- Plugin path to confidence bands (Bands Indicator + HLC Area fork pattern).
- Head-to-head comparison with Plotly / Highcharts / ApexCharts / Recharts / D3.
- White-label embed caveat: needs alt chart for paid tier.

## What comes next

- **L092** — Phase 2 deep dive on Lightweight Charts implementation patterns.
- **L195** — Forecast UI: chart + bands + consensus overlay (this loop's downstream).
- **L173** — Vintage time machine: uses Lightweight Charts data swap.
- **L144** — Embed widget design: confronts the white-label attribution wall.
- **L235** — Prototype: forecast page with bands (Phase 5 code).

## Related

- [[L001-vision-statement]] — "bands, consensus overlays, one-click drilldown" is this loop's mandate.
- [[L013-backtrader-vectorbt-zipline]] — Plotly idioms for the *other* charts; Lightweight Charts for the *forecast* chart.
- [[L014-finos-perspective]] — pivot/grid component, complement on the indicator-grid pages.
- [[L173-vintage-rewinder]] — the vintage time machine UX.
- [[L195-forecast-ui-bands-consensus]] — downstream design loop.
- [[L235-forecast-page-prototype]] — code prototype.
