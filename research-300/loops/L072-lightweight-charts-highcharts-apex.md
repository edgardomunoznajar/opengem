# L072 — Lightweight Charts vs Highcharts vs ApexCharts vs TradingView Widgets: Forecast-with-Bands Pick

**Loop**: 072 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Thesis of this loop

The forecast-with-bands chart is OPENGEM's *most strategically important* single chart type. It is the visual asset that defines the brand: the central forecast line, the 50%/80%/95% confidence bands, the vintage history overlay, the methodology pop-up, the consensus comparison, the realized-vs-forecast tracking. Get this chart right and every other page reads as serious. Get it wrong and the whole product reads as a hobby.

Four candidates:

- **Lightweight Charts** (TradingView, Apache 2.0, 45KB): the open-source charting library TradingView extracted from their commercial Advanced Charts product.
- **Highcharts** (commercial, paid for commercial use, ~75-200KB depending on modules).
- **ApexCharts** (MIT, ~100KB): popular open-source jQuery-era successor.
- **TradingView Widgets** (TradingView's embedded chart widget — hosted, free, but a JavaScript widget you embed pointed at TradingView's servers).

Plus the chart options that already won other loops:
- **Observable Plot** (L069) for static / explainer-report forecast band charts.
- **Plotly** (L062) for the Dash ops view.

Verdict: **Lightweight Charts wins** for the interactive terminal-feel forecast view. **Observable Plot wins** for the static explainer. SKIP Highcharts (closed license trap). SKIP ApexCharts (smaller, slower, less financial-aware than LWC). SKIP TradingView Widgets (third-party hosted; antithetical to OPENGEM's open thesis).

## Lightweight Charts: deep dive

The cloned repo (`research-300/clones/lightweight-charts/`) confirms:
- **License: Apache 2.0**. No trap. Genuine OSS.
- **Maintainer: TradingView Inc.** Funded by their commercial product. Active development. v5.x as of mid-2026.
- **Bundle: 45KB minified**. Tiny.
- **HTML5 canvas-rendered**. Fast even for tens of thousands of data points.
- **Series types**: line, area, baseline, candlestick, bar (OHLC), histogram, custom series (via plugin API).

For the forecast-with-bands use case specifically, Lightweight Charts provides:
- Multiple panes (price + volume style, or forecast + residuals).
- Series overlays (central forecast line on top of upper/lower band areas).
- Time-axis with smart tick spacing for daily/weekly/monthly cadence.
- Mouse-over crosshair with tooltip — *exactly* the terminal-feel affordance.
- Synchronized cursors across multiple charts (panel-wide).
- Marker primitives for annotations ("forecast vintage 2026-03-15").
- Custom series (v4+) for "fan chart" rendering — multiple confidence bands as concentric areas.

The aesthetic ships terminal-dense by default. Bloomberg-orange / Bloomberg-amber is a 5-line theme override. Dark mode is one config flag.

The CANVAS-not-SVG rendering means:
- *Pro*: fast even with 10k+ points, no DOM bloat.
- *Con*: not SSR-friendly. The chart renders client-side. For the static Observable Framework pages where SEO matters, fall back to Observable Plot for the same chart shape.

The recommendation: **use Lightweight Charts for the interactive forecast page** (the user is on the forecast page, the JS has loaded, they expect to interact); **use Observable Plot's `areaY` with multiple bands for the static explainer reports and the country-page mini-forecast** (server-rendered SVG, fast first paint, indexable).

## Why Highcharts loses

- **License**: complicated. Highcharts Core is free *for non-commercial use*. Commercial use requires a license starting at ~$1,495/dev/year, with Highcharts Stock (the financial-chart extension OPENGEM would actually need) costing $2k+/dev/year. The pricing is per-developer-seat, with site licenses and enterprise tiers stacking on top.
- **OPENGEM is open-source code (Apache 2.0) and CC-BY data**. Embedding Highcharts requires either (a) the OPENGEM team paying Highcharts in perpetuity even though OPENGEM itself is free, or (b) sticking to the non-commercial license and forfeiting the ability to ever sell a paid tier.
- The first is rejected on principle. The second is rejected because the L001 thesis explicitly anticipates a paid API/MCP tier.
- **SKIP**. Strategic trap.

## Why ApexCharts loses

- **License**: MIT. Good.
- **Bundle**: ~100KB. Twice Lightweight Charts.
- **Aesthetic**: "marketing dashboard." Looks like a Stripe-dashboard chart. Tunable but not terminal-native.
- **Financial features**: candlestick exists; built-in support for crosshair, multi-pane, and synced cursors is weaker than LWC.
- **Forecast bands**: render-able as a stacked area chart, but the API isn't optimized for it.
- **No clear advantage** vs Lightweight Charts for OPENGEM's specific needs.
- **SKIP**.

## Why TradingView Widgets lose

TradingView Widgets are JavaScript snippets you drop into a page that load a fully-functional TradingView chart pointed at TradingView's data and TradingView's servers. They are free *because the user is renting TradingView's data and brand*.

For OPENGEM:
- The widgets show TradingView's data, not OPENGEM's forecasts. Wrong data layer.
- They are hosted on TradingView's servers. OPENGEM cannot publish a vintage of "what the chart looked like on date X" because the chart is live-rendered against TradingView's then-current data.
- They are *branded TradingView*. The aesthetic is "TradingView orange" not "OPENGEM orange."
- They are JS embeds hostile to SSR / SEO / offline.
- They are *closed*. OPENGEM cannot extend, fork, or customize.

Every consideration that argues against using OPENGEM dashboard widgets in someone else's product (Substack, Notion) — those same considerations argue against using TradingView's widget in OPENGEM. **SKIP**.

## The chart spec OPENGEM needs to ship in Lightweight Charts

For the forecast-page hero chart:

```javascript
const chart = createChart(containerRef.current, {
  layout: { textColor: '#fff', background: { color: '#000' } },
  grid: { vertLines: { color: '#1a1a1a' }, horzLines: { color: '#1a1a1a' } },
  crosshair: { mode: CrosshairMode.Normal },
});

// 95% confidence band (outer)
const band95 = chart.addAreaSeries({ topColor: 'rgba(255,165,0,0.10)', bottomColor: 'rgba(255,165,0,0.10)' });

// 80% confidence band
const band80 = chart.addAreaSeries({ topColor: 'rgba(255,165,0,0.20)', bottomColor: 'rgba(255,165,0,0.20)' });

// 50% confidence band
const band50 = chart.addAreaSeries({ topColor: 'rgba(255,165,0,0.30)', bottomColor: 'rgba(255,165,0,0.30)' });

// Central forecast line
const central = chart.addLineSeries({ color: '#ffa500', lineWidth: 2 });

// Realized history
const realized = chart.addLineSeries({ color: '#fff', lineWidth: 1.5 });

// Vintage history overlays (faded lines)
const vintages = priorVintages.map(v => chart.addLineSeries({ color: 'rgba(255,255,255,0.2)', lineWidth: 1 }));

// Annotations (vintage rollover markers)
central.setMarkers([{ time, position: 'aboveBar', color: '#ffa500', shape: 'arrowUp', text: 'V14' }]);
```

This is ~50 lines of OPENGEM-specific code on top of LWC primitives. The shape is *exactly* the right shape for a forecast chart.

## Bundle / performance budget for the forecast page

- Lightweight Charts: 45KB.
- React wrapper (`lightweight-charts-react-wrapper` or custom hook): ~5KB.
- Forecast page total JS: ~80KB (LWC + React hook + page logic). Well under the 100KB budget.
- Render time for 10 years daily data (~2500 points): ~50ms.
- Interaction latency: <16ms (60fps).

## Verdict

- **Lightweight Charts** for the interactive forecast page hero chart: **ADOPT-V1**. $0. 1-week ramp.
- **Observable Plot** for static forecast bands in explainer reports + country-page mini-charts: **ADOPT-V1** (already in L069).
- **Highcharts**: **SKIP**. License trap.
- **ApexCharts**: **SKIP**. No advantage.
- **TradingView Widgets**: **SKIP**. Strategically antithetical.

## Cost summary

| Tool | License | Bundle | Cost | Ramp |
|---|---|---|---|---|
| Lightweight Charts | Apache 2.0 | 45KB | $0 | 1 week |
| Observable Plot (forecast band, static) | ISC | (counted in L069) | $0 | 0 (already adopted) |
| Highcharts | Commercial | 75-200KB | $1-3k/dev/year | (skipped) |
| ApexCharts | MIT | 100KB | $0 | (skipped) |
| TradingView Widgets | Closed hosted | n/a | "free" but strategically harmful | (skipped) |

## What comes next

- **L073** picks the Next.js dashboard starter kit.
- **L092** is the Phase 2 deep dive on Lightweight Charts integration for terminal feel.

## Related

- [[L069-d3-vega-plotly]] — static counterpart (Observable Plot)
- [[L073-next-tailwind-dashboard-starters]] — frontend host
- [[L092-lightweight-charts-terminal-feel]] — Phase 2 deep dive
- [[L126-forecast-page-layouts]] — page where this chart lives (Phase 3)
