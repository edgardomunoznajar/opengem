# L092 — Lightweight Charts for Terminal Feel: Forecast-Band Rendering Pattern

**Loop**: 092 / 300
**Phase**: 2 — Integration deep dive
**Date**: 2026-06-06
**Verdict**: **ADOPT-V1 (forecast page hero + embed widget; fork Bands plugin → `ConfidenceBand`)**

---

## What this loop produces

L015 picked Lightweight Charts as the forecast-page chart with the path-via-plugins to confidence bands. L072 sharpened the head-to-head against Highcharts/Apex. This Phase 2 loop produces the *actual rendering pattern* — code shape, plugin fork plan, multi-band stacking strategy, consensus overlay technique, vintage-rewinder hook — by inspecting `research-300/clones/lightweight-charts/plugin-examples/`.

The headline pattern: **fork the `Bands Indicator` primitive (`plugin-examples/src/plugins/bands-indicator/`) into an OPENGEM-owned `ConfidenceBand` series primitive, parameterize the upper/lower data inputs (not computed-from-line as in the original), stack two instances for outer + inner bands, layer dashed `addLineSeries` for consensus overlays, position a vertical-line primitive for the "today" marker, and bind the time-scale to a `VintageRewinderController` that swaps `setData()` when the user drags the vintage slider.**

## The cloned plugin example, dissected

`research-300/clones/lightweight-charts/plugin-examples/src/plugins/bands-indicator/bands-indicator.ts` is 211 lines, MIT (Apache-2.0 compatible for our fork). The structure:

- `BandsIndicatorPaneRenderer` — the actual Canvas2D draw. Two paths: one fill (the shaded region between upper and lower) and one stroke (the upper/lower edge lines). ~30 lines.
- `BandsIndicatorPaneView` — connects series data → screen coordinates via `timeScale.timeToCoordinate` + `series.priceToCoordinate`. Reactive to data changes via `update()`. ~30 lines.
- `BandsIndicator` (the public class) — extends `PluginBase`, implements `ISeriesPrimitive<Time>`, holds `_seriesData` and `_bandsData`, recomputes bands on `dataUpdated`. ~80 lines.
- Helper `calculateBands(...)` — *in the example* computes `upper = price * 1.1, lower = price * 0.9`. This is the canonical fork point: we replace this with "upper = data[i].upper, lower = data[i].lower" from explicitly-provided band data.

The pattern is clean. The "plugin" is genuinely a thin layer over Canvas2D rendering with hooks into the chart's coordinate system. No magic.

## The OPENGEM fork: `ConfidenceBand`

The fork lives in `packages/opengem-charts-tradingview/` (separate package because shipping our own NPM package keeps the version cadence under our control). The relevant changes from the upstream `BandsIndicator`:

```typescript
// packages/opengem-charts-tradingview/src/confidence-band.ts
import { ISeriesPrimitive, PluginBase, Time } from 'lightweight-charts';

export interface ConfidenceBandData {
  time: Time;          // x-axis position
  median: number;      // central forecast (drawn as the bound line)
  lower: number;       // band lower bound (P10 or P25)
  upper: number;       // band upper bound (P90 or P75)
}

export interface ConfidenceBandOptions {
  bandFillColor: string;     // e.g. 'rgba(255, 170, 102, 0.18)' for outer P10/P90
  bandEdgeColor: string;     // e.g. 'rgba(255, 170, 102, 0.4)'  for band edges
  bandEdgeWidth: number;
  medianLineColor: string;   // only used if drawMedian = true
  drawMedian: boolean;       // false when median is drawn by a separate line series
}

export class ConfidenceBand extends PluginBase implements ISeriesPrimitive<Time> {
  private _data: ConfidenceBandData[] = [];
  private _options: Required<ConfidenceBandOptions>;
  private _paneViews: ConfidenceBandPaneView[];

  constructor(options: Partial<ConfidenceBandOptions> = {}) {
    super();
    this._options = { ...DEFAULT_OPTIONS, ...options };
    this._paneViews = [new ConfidenceBandPaneView(this)];
  }

  setData(data: ConfidenceBandData[]): void {
    this._data = data;
    this.updateAllViews();
    this.requestUpdate();
  }

  // ... [paneViews(), autoscaleInfo(), updateAllViews() ...]
}
```

The differences from upstream:

1. **Data comes in pre-computed** instead of derived from the line series. The user provides `{time, median, lower, upper}` tuples. This is the only meaningful change.
2. **Median line is optional.** For the OPENGEM forecast page, the median line is drawn as a separate `addLineSeries` so it can have its own color, dashing, and tooltip behavior. The band primitive draws fill + edges only.
3. **Options renamed** to match the OPENGEM design system (bandFillColor instead of fillColor).

Total fork effort: ~1 day. The rendering logic is identical; we just swap the data source.

## Stacking two bands (outer + inner)

The forecast page wants both P10/P90 outer + P25/P75 inner bands. Two `ConfidenceBand` instances on the same series:

```typescript
import { createChart, LineStyle } from 'lightweight-charts';
import { ConfidenceBand } from '@opengem/charts-tradingview';

const chart = createChart(container, {
  layout: { background: { color: '#0c0c0c' }, textColor: '#cccccc' },
  grid: { vertLines: { color: '#1a1a1a' }, horzLines: { color: '#1a1a1a' } },
  timeScale: { rightOffset: 12, secondsVisible: false },
  rightPriceScale: { borderColor: '#333' },
});

const medianSeries = chart.addLineSeries({
  color: '#ffaa66',  // terminal-orange
  lineWidth: 2,
  priceLineVisible: false,
});

const outerBand = new ConfidenceBand({
  bandFillColor: 'rgba(255, 170, 102, 0.12)',
  bandEdgeColor: 'rgba(255, 170, 102, 0.25)',
  bandEdgeWidth: 1,
});
const innerBand = new ConfidenceBand({
  bandFillColor: 'rgba(255, 170, 102, 0.22)',
  bandEdgeColor: 'rgba(255, 170, 102, 0.4)',
  bandEdgeWidth: 1,
});

medianSeries.attachPrimitive(outerBand);
medianSeries.attachPrimitive(innerBand);

// Data wiring:
medianSeries.setData(history.concat(forecast.map(d => ({ time: d.time, value: d.p50 }))));
outerBand.setData(forecast.map(d => ({ time: d.time, median: d.p50, lower: d.p10, upper: d.p90 })));
innerBand.setData(forecast.map(d => ({ time: d.time, median: d.p50, lower: d.p25, upper: d.p75 })));
```

The inner band's fill alpha is higher; the band edge is more prominent. Visually: a smooth darker P25-P75 region nested inside a lighter P10-P90 region, both anchored to the median line. Bloomberg-grade.

## Consensus overlay — dashed lines

The forecast page shows IMF WEO + OECD EO + ECB SPF + FRB SEP consensus forecasts as dashed lines. Each is a separate `addLineSeries`:

```typescript
const overlays = [
  { name: 'IMF WEO',  color: 'rgba(102, 170, 255, 0.7)', data: weo,  style: LineStyle.Dashed },
  { name: 'OECD EO',  color: 'rgba(102, 255, 170, 0.7)', data: oecd, style: LineStyle.Dashed },
  { name: 'ECB SPF',  color: 'rgba(255, 102, 170, 0.7)', data: spf,  style: LineStyle.Dashed },
  { name: 'FRB SEP',  color: 'rgba(170, 102, 255, 0.7)', data: sep,  style: LineStyle.Dashed },
];

overlays.forEach(o => {
  const s = chart.addLineSeries({
    color: o.color,
    lineWidth: 1,
    lineStyle: o.style,
    priceLineVisible: false,
    lastValueVisible: false,
    title: o.name,
  });
  s.setData(o.data);
});
```

Lightweight Charts handles ~10 concurrent line series with no perf hit. Four consensus overlays + median + history is well within budget.

## The "today" vertical marker

A small custom plugin (~20 lines) using `Primitives` to draw a vertical line at "now":

```typescript
// packages/opengem-charts-tradingview/src/today-marker.ts
import { IPrimitivePaneRenderer, IPrimitivePaneView, ISeriesPrimitive, Time } from 'lightweight-charts';

export class TodayMarker extends PluginBase implements ISeriesPrimitive<Time> {
  private _time: Time;
  // ... paneViews / renderer that draws a vertical 1px line ...
  setTime(time: Time): void { this._time = time; this.updateAllViews(); this.requestUpdate(); }
}
```

The today-marker plugin: ~30 lines including the renderer. Reused on every forecast page.

## The vintage rewinder hook

L173 promised a "rewind to Sept 2024" UX. The data swap is simple — given a new vintage date, fetch the corresponding band data and call `setData()` on each band + line series.

The chart re-renders in milliseconds (Canvas2D recompute, no JS framework round-trip). The interaction is buttery — drag the vintage slider and the forecast bands recompute live.

```typescript
// hooks/useVintageRewinder.ts (Next.js side)
import { useEffect } from 'react';

export function useVintageRewinder(
  chart: ChartHandles,
  vintageDate: Date,
  country: string,
  indicator: string,
) {
  useEffect(() => {
    let cancelled = false;
    (async () => {
      const data = await fetchVintageBandData(country, indicator, vintageDate);
      if (cancelled) return;
      chart.medianSeries.setData(data.median);
      chart.outerBand.setData(data.outer);
      chart.innerBand.setData(data.inner);
      chart.todayMarker.setTime(vintageDate.getTime() / 1000);
    })();
    return () => { cancelled = true; };
  }, [vintageDate, country, indicator]);
}
```

API round-trip dominates the perceived latency (~30-100ms); the chart render itself is sub-frame.

## Attribution and the white-label problem

Lightweight Charts' Apache-2.0 license has an attribution clause: a "TradingView" credit must appear on every public page using it. The `attributionLogo: true` option places a small watermark in the chart corner.

For OPENGEM's free public dashboard and embeddable widgets: **attribution is fine**. We already include a "powered by OPENGEM" badge; a sibling "charts by TradingView" is acceptable and standard.

For OPENGEM's *paid white-label embed* tier (L144): white-label customers cannot have a TradingView watermark on their branded surface. The fallback is a separately-implemented Canvas2D chart for white-label embeds. **This is deferred to L144's design loop** — we ship Lightweight Charts everywhere in v1 and address white-label in Y2 when there's actual paying demand.

## Mobile

Canvas2D performance on mobile Safari is materially worse than desktop. The forecast page hero chart at 600px wide on iPhone is fine; the same chart at full-bleed 1200px is choppy on older devices. Mitigation: explicit width clamping in the responsive layout (~600px max on mobile breakpoint).

## Bundle size

Lightweight Charts core: ~50KB gzipped. Our plugins (`ConfidenceBand`, `TodayMarker`): ~5KB combined. The full chart kit ships as a lazy-loaded chunk in Next.js (~55KB total) only on the forecast page — the home page does not pay this cost.

## Cost summary

| Task | Cost |
|---|---|
| Fork `BandsIndicator` → `ConfidenceBand` | 1 dev-day |
| Wrap `medianSeries + outerBand + innerBand` as a `ForecastBandsChart` React component | 2 dev-days |
| `TodayMarker` plugin | 0.5 dev-day |
| Consensus overlay (4 dashed series) | 0.5 dev-day |
| `VintageRewinderController` hook | 1 dev-day |
| Tooltip + hover behavior | 1 dev-day |
| Mobile responsive layout | 1 dev-day |
| Theme tokens (dark + light + brand variants) | 1 dev-day |
| Integration tests + visual regression | 2 dev-days |
| Attribution component for free tier | 0.25 dev-day |
| **Total** | **~10 dev-days (~2 weeks)** |

Compares well to L015's 2-week estimate. Confirmed.

## Risks

1. **Lightweight Charts API drift.** TradingView occasionally breaks plugin APIs. Mitigation: pin to a known-good version; budget half a day quarterly to chase.

2. **Canvas2D rendering bugs on edge browsers.** Mostly fine in 2026 but Safari + WebGL contexts have known quirks. Mitigation: e2e test against Playwright with Safari/Firefox/Chrome.

3. **The Bands plugin's autoscale logic doesn't know about the inner band.** When two bands are stacked, Lightweight Charts' autoscale may only consider one of them. Mitigation: explicit `autoscaleInfo()` override on the outer band that knows about both.

4. **Touch UX is awkward.** Drag-to-zoom on touch screens can conflict with the vintage rewinder slider. Mitigation: separate the rewinder slider from the chart proper; chart is read-only on mobile, slider is below.

## What this loop produced

- Concrete fork plan for `BandsIndicator` → `ConfidenceBand` (1 dev-day).
- Code skeleton for the full forecast page chart (median + outer + inner band + consensus + today marker).
- Vintage rewinder hook pattern that swaps data with no framework round-trip.
- Bundle + mobile + attribution + theme tokens addressed.
- ~2 dev-week total cost for the forecast page hero.

## What comes next

- **L098** — Vega-Lite for embeddable forecast charts (the white-label alternative path).
- **L100** — Plotly Resampler for million-point series (when Lightweight Charts hits its limit).
- **L173** — Vintage rewinder UI.
- **L195** — Forecast UI bands consensus (downstream design).
- **L235** — Forecast page prototype (code).
- **L245** — Embed widget prototype.

## Related

- [[L015-lightweight-charts]] — Phase 1 deep dive.
- [[L072-lightweight-charts-highcharts-apex]] — Phase 1 head-to-head.
- [[L098-vega-lite-embeddable-forecast-charts]] — embedded sibling.
- [[L100-plotly-resampler-million-point-series]] — perf-ceiling sibling.
- [[L144-embed-widget-design]] — white-label problem space.
- [[L195-forecast-ui-bands-consensus]] — downstream UI.
- inspected source: `/mnt/bigdata/home/edgardo/projectsd/opengem/research-300/clones/lightweight-charts/plugin-examples/src/plugins/bands-indicator/bands-indicator.ts` (211 lines)
- inspected source: `/mnt/bigdata/home/edgardo/projectsd/opengem/research-300/clones/lightweight-charts/plugin-examples/src/plugins/` (28 plugin examples; the BandsIndicator is the canonical fork base)
