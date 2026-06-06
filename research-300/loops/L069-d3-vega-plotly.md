# L069 — D3 + Vega-Altair + Plotly: Which Library Wins Each OPENGEM Chart Family

**Loop**: 069 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Thesis of this loop

This is the chart-library shootout for OPENGEM. The candidates are the three dominant open-source families:

- **D3.js** (Mike Bostock, 2011): low-level DOM/SVG manipulation. Maximum flexibility, maximum effort. BSD-3 license.
- **Vega / Vega-Lite / Vega-Altair** (UW IDL, 2014-2018): declarative grammar of graphics, JSON specs. Vega-Altair is the Python binding for Vega-Lite. BSD-3.
- **Plotly.js / Plotly Express** (Plotly, 2012): high-level interactive scientific charts on top of D3 + WebGL. MIT.

A fourth candidate that *deserves to be on the list*: **Observable Plot** (Mike Bostock, 2021) — the spiritual successor to D3, the API D3's author wishes he had built first. ISC. Comes bundled with Observable Framework (L066) but works standalone.

OPENGEM does not need to pick one — it needs to pick the *right one for each chart family*. The verdict:

- **Line / area / area-with-bands / sparkline / multi-vintage overlay**: **Observable Plot**. ADOPT-V1.
- **Geo (choropleth, points-on-map)**: **D3-geo + topojson** for static, **globe.gl** for 3D (see L071). ADOPT-V1.
- **Table-with-sparklines (Bloomberg grid)**: **AG-Grid** or **TanStack Table** with embedded sparkline renderers (see L070). ADOPT-V1.
- **Forecast band chart with hover-vintage**: **TradingView Lightweight Charts** (see L072) for the dense terminal-feel chart; **Observable Plot** for the embedded explainer.
- **One-off custom (Sankey, network graph, scenario tree)**: **D3 + custom code**. ADOPT-V2.
- **Plotly anywhere**: **EVALUATE-LATER**, mostly as a fallback inside the Dash ops view (L062).

## Chart family × library matrix

| Chart family | OPENGEM examples | Winner | Why |
|---|---|---|---|
| Line, multi-series | Indicator history, vintage overlay | Observable Plot | Declarative, composable, works in static builds |
| Area with confidence bands | Forecast fan chart | Observable Plot (static) / Lightweight Charts (interactive) | Plot's `areaY` with `y1`/`y2` is 5 lines |
| Sparkline | KPI cards, grid cells | Observable Plot | `plot({marks: [lineY(d), axisY({label:null})], width: 100, height: 30})` |
| Choropleth (world / country) | Geopolitical risk map | D3-geo + topojson + Plot | Battle-tested, atlas of every projection |
| Points-on-map / arcs | Trade flows, conflict events | globe.gl (3D), D3-geo (2D) | See L071 |
| Bar / stacked bar | Composition decompositions | Observable Plot | Same composable grammar |
| Heatmap | V&V matrix (model × horizon × indicator) | Observable Plot | `cell` mark |
| Scatter w/ regression | Indicator-vs-indicator | Observable Plot | Composable `dot` + `linearRegressionY` |
| Sankey / chord | Trade flow decomposition | D3-sankey (raw) | No grammar covers this well |
| Network graph | Citation graph, model dependency | D3-force / Cytoscape.js | Imperative, fine |
| Scenario tree | Forecast scenario branches | D3 + custom | Custom enough that grammar doesn't help |
| Candlestick / OHLC | Price series (commodities, FX) | Lightweight Charts | Native to the library |
| Table-with-cells | Forecast leaderboard | AG-Grid + Observable Plot in cells | See L070 |

## Why Observable Plot wins the line/area/sparkline workhorse band

Observable Plot is the most strategically important chart library for OPENGEM. Concretely:

1. **Declarative.** A chart is a JSON-spec-equivalent JavaScript expression. Easy to template across countries × indicators.
2. **Composable.** `Plot.areaY()` + `Plot.lineY()` + `Plot.ruleX()` + `Plot.text()` stack on one plot. Forecast band + central path + vintage rules + annotation — five lines.
3. **Faceting.** `facet: { x: "country" }` makes the small-multiple grid free. The "show me CPI for G7" page is one `Plot.plot()` call.
4. **Statistical transforms baked in**: `Plot.binX`, `Plot.windowY`, `Plot.linearRegressionY`. The grammar handles 80% of econ charts without a separate transform layer.
5. **SSR-friendly.** Plot can render to SVG strings server-side at build time. Observable Framework uses this. The result is real HTML in the page source, no client-side execution needed for the static view. SEO wins.
6. **MIT-ish license (ISC).** Free forever.
7. **One author (Mike Bostock).** Means a coherent design, fast bug fixes, and a clean evolutionary trajectory. The risk: Bostock could bus-factor it; but the codebase is small enough that any of us could fork-and-maintain.

The alternative for the same band is Vega-Altair / Vega-Lite. It's *also* declarative, *also* grammar-of-graphics, *also* MIT-ish (BSD-3). The differences:

- Vega-Lite specs are JSON; Plot specs are JS expressions. JSON is more portable; JS is more composable.
- Vega has a richer transform layer (selection, brushing, cross-filter); Plot is leaner.
- Vega's Python binding (Altair) is genuinely first-class for Python-shaped teams. Plot's Python ecosystem doesn't exist (it's JS only).

For OPENGEM's chart authoring model (JS at the leaf in Observable Framework + React component wrappers in Next.js), Plot wins. If OPENGEM had a Python-notebook authoring model, Altair would win.

## Why D3 directly for geo

D3-geo + topojson is the *canonical* atlas of map projections, country boundary handling, and projection math. Every other JS map lib eventually reduces to D3-geo for projections; using it directly avoids one layer of indirection.

For the OPENGEM choropleth (a flat world map color-coded by indicator value), D3-geo + Natural Earth topojson + Observable Plot's `geo` mark is the right path. ~30 lines for a clean choropleth. The 3D version lives in globe.gl (L071).

## Why Plotly is not the workhorse but stays as a fallback

Plotly's strengths:
- Out-of-the-box zoom/pan/hover/legend.
- WebGL for million-point series via `scattergl` (and `plotly-resampler` for billion).
- First-class Dash integration (L062).
- Rich chart vocabulary including all the statistical types.

Plotly's weaknesses for OPENGEM specifically:
- Bundle size (~3.5 MB unminified, ~1 MB gzipped). Big for a static dashboard targeting fast loads.
- Default aesthetic is "scientific" rather than "terminal." Tunable but takes effort.
- Composability is weaker than Plot's grammar. You build a Plotly chart by setting properties; you build a Plot chart by composing marks.
- SSR is awkward (Plotly is fundamentally a client-side renderer).

Plotly's *role* in OPENGEM:
- The Dash ops view (L062) uses Plotly natively. Keep it there.
- Plotly-resampler for the rare million-point series (L100).
- Plotly as the embed format for tearsheets exported as standalone HTML — Plotly's offline HTML export is a clean self-contained file.

## Bundle / performance budget

For the static public dashboard target of <100KB initial JS payload per page (a hard discipline goal):

- Observable Plot: ~80KB gzipped.
- D3 (only the bits you import): ~30-60KB for typical chart subset.
- Lightweight Charts: ~45KB.
- Plotly.js full bundle: ~1MB gzipped. Use only inside the Dash ops view, never on public.

The math: a country page with 6 Plot charts + 1 Lightweight Charts forecast view = ~130KB JS. With code splitting and lazy load of the forecast widget, the above-fold is ~80KB. Fast.

## Verdict

- **Observable Plot** for line/area/area-with-bands/sparkline/bar/heatmap/scatter/faceted small-multiples: **ADOPT-V1**.
- **D3 + topojson** for geo: **ADOPT-V1**.
- **D3 (raw)** for one-off custom (Sankey, scenario tree, network): **ADOPT-V2**.
- **Vega-Altair**: **EVALUATE-LATER** for Python-authored notebooks that export to embedded charts. Lose to Plot for JS-first authoring.
- **Plotly** in the public dashboard: **SKIP** (bundle size + aesthetic).
- **Plotly** in the Dash ops view: **ADOPT-V1** (it's the native chart library there).
- **Plotly-resampler** for million-point series: **ADOPT-V2** when needed.

## Cost summary

| Library | License | Bundle | Use | Ramp |
|---|---|---|---|---|
| Observable Plot | ISC | 80KB | Public workhorse | 1 week |
| D3 | BSD-3 | 30-60KB | Geo + custom | 2 weeks |
| Plotly.js | MIT | 1MB | Dash ops only | 1 week |
| Vega-Altair | BSD-3 | n/a | Python notebooks | 2 weeks |

## What comes next

- **L070** picks the data grid library.
- **L071** picks the 3D/geo viz library.
- **L072** picks the forecast-band charting library.

## Related

- [[L066-observable-framework]] — Plot lives natively here
- [[L100-plotly-resampler-million-points]] — Phase 2 on the million-point edge case
- [[L098-vega-lite-embeddable-charts]] — Phase 2 on the alternative
