# L098 — Vega-Lite for embeddable forecast charts

**Loop**: 098 / 300
**Phase**: 2 — Deep dives
**Date**: 2026-06-06
**Verdict**: ADOPT-V2 (not v1; the embed SDK ships SVG-pure first)

---

## The decision

OPENGEM uses **TradingView Lightweight Charts** for the interactive forecast page (L015 / L092 picks). For *embeddable forecasts* — the tiles dropped into blog posts, Substacks, and YouTube descriptions — the question is: keep the SVG-pure path, or migrate to Vega-Lite?

**Recommendation**: SVG-pure (current `embed.js` at ~3 KB) for v0 → v1. Add Vega-Lite as an **opt-in renderer** at v1.5 for `data-renderer="vega"` embeds. Never make Vega-Lite the default.

## Why not Vega-Lite as default

- **Bundle weight**: Vega-Lite + Vega + Vega-loader ≈ 220 KB gzipped. The current embed.js is 3 KB. For a blog with 5 OPENGEM tiles, that's a 73× cost-per-tile hit. Negligible for one tile; visible for a wall of tiles in a country dashboard embed.
- **JSON-grammar overkill** for a single forecast chart: P10/P50/P90 band + consensus overlay + actual dots is 30 lines of SVG. Vega-Lite would need a similarly-sized spec PLUS the runtime.
- **Discoverability vs control**: Vega-Lite is great when a host wants to compose multiple OPENGEM charts; it's overkill for a single tile.

## Why ADOPT-V2 (eventually)

- **Republishable specs**: a Vega-Lite spec IS the chart. We can publish `chart.vg.json` per forecast, and academics can fork it directly in Observable or open it in Voyager.
- **Multi-chart composition**: when a blog wants "GDP + CPI + Unemp side-by-side for USA," Vega-Lite's `hconcat` is shorter than three SVG embeds.
- **Theming**: Vega-Lite has a real theming layer that supports OPENGEM's "Ledger Amber" palette via a single config block, vs hand-tuning SVG fills per chart.
- **Accessibility**: Vega-Lite renders ARIA labels and Plot-grade keyboard nav for free; SVG-pure requires manual effort per chart.

## The hybrid: per-embed renderer selection

```html
<!-- v0/v1 default — 3 KB inline SVG -->
<div data-opengem
     data-kind="forecast"
     data-country="USA"
     data-indicator="gdp_yoy"
     data-size="banner"></div>

<!-- v1.5 opt-in — fancy multi-chart compose, paid for in bundle weight -->
<div data-opengem
     data-renderer="vega"
     data-spec="https://opengem.org/specs/usa-gdp-cpi-unemp.vg.json"></div>
```

The SDK auto-loads the Vega-Lite renderer lazily only when at least one `data-renderer="vega"` node is present. Hosts pay weight only when they ask.

## What we publish at `/specs/`

For every chart on the dashboard, a corresponding `<entity>.vg.json` spec at `https://opengem.org/specs/...`. Three benefits:
1. Academics can fork in Observable / Vega Editor / Voyager.
2. Subscribers to the `/feeds/forecasts.atom` feed can render in any Vega-Lite-aware reader.
3. LLM agents can read the spec to understand the chart structure for narrative generation.

The spec generation is mechanical — a small `opengem-charts` package that emits Vega-Lite JSON from a Forecast object.

## Comparison summary

| Renderer | Bundle | Use case | Verdict |
|---|---|---|---|
| Inline SVG (current) | 3 KB | Single-tile embeds | ADOPT-V1 (default) |
| Lightweight Charts | 45 KB | Interactive forecast page | ADOPT-V1 (in dashboard) |
| Vega-Lite | 220 KB | Multi-chart compose, academic fork | ADOPT-V2 (opt-in lazy) |
| Plotly Resampler | 1.5 MB | Million-point series | ADOPT-V2 (per L100) |
| Observable Plot | 80 KB | Long-tail SEO pages | ADOPT-V1 (in `notebooks.opengem.org`) |

## What this loop produced

- The default-renderer pick (SVG-pure inline) preserved
- Vega-Lite as opt-in v1.5 renderer
- The `/specs/<entity>.vg.json` publication discipline (academics + LLM grounding)
- The `opengem-charts` package as the spec emitter

## What comes next

- L099 — TanStack Table for Pro grids (complement: tables, not charts)
- L100 — Plotly Resampler decision

## Related

- [[L069-d3-vega-altair-plotly]] — the survey that informed this
- [[L015-lightweight-charts]] — the interactive-chart default
- [[L091-observable-framework-explainer-reports]] — Vega-Lite on the explainer subdomain
- [[L245-embed-widget]] — the SDK design this guides
