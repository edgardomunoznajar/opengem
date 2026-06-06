# L100 — Plotly Resampler for million-point series

**Loop**: 100 / 300
**Phase**: 2 — Deep dives
**Date**: 2026-06-06
**Verdict**: ADOPT-V2 (lazy-loaded, single page)

---

## The decision

Plotly Resampler is **not** the default forecast chart (that's Lightweight Charts per L015 + the SVG-pure path per L098). It's the **chosen renderer for a single specialized page**: the "deep chart" view where a user wants a million daily observations of, e.g., the US Treasury yield curve or BIS REER per country since 1985.

For that view, the math is brutal:
- BIS REER monthly since 1985 = 480 points per country × 22 Tier-V = 10,560 points
- Daily yield curve at 11 maturities since 1985 = 14,640 × 11 = 161,040 points
- High-frequency intraday derivatives (not core OPENGEM but useful in cross-asset overlays) = millions

Plotly + plotly-resampler downsamples on the fly using a LTTB (largest-triangle-three-buckets) or MinMaxLTTB algorithm, preserving visual fidelity while shipping only ~1k visible points per pan/zoom level. This is the only library where "1M points + smooth interaction" is solved out of the box.

## Why ADOPT-V2 not V1

- **Bundle weight**: plotly.js-dist-min is ~1.4 MB gzipped. The whole forecast page should be under 100 KB JS gzipped (per L267 perf budget). Plotly cannot ship eagerly.
- **Most pages don't need it**: a forecast page typically shows 4 years × quarterly = 16 points. SVG-pure handles it; Lightweight Charts handles 4-decade daily.
- **The deep-chart use case is the long-tail page**: researcher mode, not the default browse path.

## The mount pattern

```tsx
// app/deep-chart/[id]/page.tsx
import dynamic from "next/dynamic";

const PlotlyResampledChart = dynamic(
  () => import("@/components/charts/PlotlyResampledChart"),
  {
    ssr: false,
    loading: () => <div className="tile h-96">loading 1.4MB chart engine…</div>,
  }
);

export default async function DeepChartPage({ params }: Props) {
  const { id } = await params;
  const series = await getDeepSeries(id);
  return <PlotlyResampledChart series={series} />;
}
```

The dynamic import + `ssr: false` ensures Plotly is fetched only when this page is visited. Server components on every other page never ship Plotly to the client.

## The component (sketch)

```tsx
"use client";
import { useEffect, useRef } from "react";
import Plotly from "plotly.js-dist-min";

interface Props {
  series: Array<{ t: string; v: number }>;
}

export default function PlotlyResampledChart({ series }: Props) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!ref.current) return;
    Plotly.newPlot(ref.current, [{
      type: "scattergl",  // WebGL accelerated
      x: series.map(p => p.t),
      y: series.map(p => p.v),
      mode: "lines",
      line: { color: "#f59e0b", width: 1 },
    }], {
      paper_bgcolor: "#16161a",
      plot_bgcolor: "#16161a",
      font: { family: "JetBrains Mono", color: "#a1a1aa", size: 11 },
      xaxis: { gridcolor: "#27272a" },
      yaxis: { gridcolor: "#27272a" },
      margin: { l: 40, r: 8, t: 8, b: 28 },
    }, {
      responsive: true,
      displayModeBar: false,  // we add our own toolbar
    });
    return () => { Plotly.purge(ref.current!); };
  }, [series]);
  return <div ref={ref} className="h-96" />;
}
```

Server-side downsampling (a separate concern): the FastAPI service exposes `/v1/deep-series/{id}?level=overview|detail` so the client doesn't fetch raw 1M points either; we ship the right resolution for the zoom level.

## Why not just use uPlot, dygraphs, ECharts WebGL?

- **uPlot** is faster and lighter (~50 KB) but its API is far rougher and the WebGL build still requires manual downsampling.
- **dygraphs** is the legacy gold standard but no WebGL; falls over at ~500k points.
- **ECharts** is excellent and has WebGL but bundle is ~1 MB and the API is heavier than Plotly's; minimal saving for major theming work.

For OPENGEM's *one deep-chart use case*, Plotly Resampler's downsample-on-pan UX is best-in-class and worth the lazy-loaded bundle.

## What this loop produced

- The "lazy import on a single page" pattern for Plotly
- The boundary: default forecast = SVG-pure; interactive forecast = Lightweight Charts; deep chart = Plotly+Resampler
- The server-side downsample endpoint contract `/v1/deep-series/{id}?level=overview|detail`
- Rejection of uPlot/dygraphs/ECharts for this specific niche

## What comes next

- Phase 2 close. Phase 6 final synthesis (L300) gets to integrate the chart-rendering decision tree.

## Related

- [[L015-lightweight-charts]] — the interactive default
- [[L098-vega-lite-embeds]] — the embedded-renderer decision
- [[L069-d3-vega-altair-plotly]] — the survey
- [[L267-lighthouse-perf-budget]] (within L266-270 batch) — the budget this lives under
