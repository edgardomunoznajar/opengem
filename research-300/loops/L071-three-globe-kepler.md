# L071 — Three.js + globe.gl + Kepler.gl: Geopolitical Pulse 3D Map

**Loop**: 071 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Thesis of this loop

The OPENGEM geopolitical pulse page needs a 3D Earth, color-coded by an index (Caldara-Iacoviello GPR, our own composite, or a chosen geopolitical risk series), with arcs for cross-border events (conflict, sanction, trade-flow change), point markers for breaking events, and a time-slider for the past N weeks.

The three contenders:

- **Three.js**: the underlying WebGL 3D engine. You build everything from primitives. Maximum control, maximum effort.
- **globe.gl** (Vasco Asturiano): a Three.js-based React component specifically for spherical globe visualizations. Hexagon/heatmap/arc/labels/rings layers. MIT.
- **Kepler.gl** (Uber/Vis.gl): a deck.gl-based geospatial analytics tool. 2D-first with a recent 3D mode. Massive feature set, massive bundle. MIT.

Verdict: **globe.gl wins** for the geopolitical pulse page. **Three.js stays** as the escape hatch for custom layers. **Kepler.gl is wrong shape** — it's an analytical tool you embed, not a custom 3D dashboard primitive.

## globe.gl: the recommended pick

- **License**: MIT.
- **Maintainer**: Vasco Asturiano (also `three-globe`, `react-globe.gl`, `react-force-graph`). Healthy and prolific.
- **Bundle**: ~600KB gzipped (includes Three.js dependencies). Big, but loaded once and cached.
- **API**: declarative. `Globe()`.`pointsData([...])`.`arcsData([...])`.`polygonsData([...])`. Method-chaining.
- **Layers**:
  - Points (markers): color, altitude, size — perfect for breaking events.
  - Arcs (origin → destination paths over the globe): color gradient, stroke width, animation — perfect for trade flows, refugee movements, sanctions events.
  - Polygons (country boundaries): color-coded by indicator — choropleth on a sphere.
  - Rings (animated pulses): "something just happened here" — perfect for event-feed integration.
  - Hexbin (aggregated heat): density. Useful for conflict-event clustering (ACLED).
  - Labels: country names, city names, custom event labels.
  - HTML overlays: pop-up tooltips, info panels.
- **React component**: `react-globe.gl` ships a `<Globe />` React wrapper. Drop-in for a Next.js page.
- **Performance**: handles 10k-100k points and 1k-5k arcs smoothly on a recent desktop. Mobile is more limited (~5k points smoothly).
- **3D primitive support**: native — it *is* a 3D globe.

The cloned `globe-gl` repo (`research-300/clones/globe-gl/`) confirms the library is small, focused, and actively maintained. The `example/` directory has ~30 reference implementations including world-population, conflict-events, and air-traffic — all directly analogous to OPENGEM's intended use.

## Why globe.gl beats Kepler.gl for OPENGEM

Kepler.gl is brilliant for what it does: drop a CSV with lat/lng on a map and instantly get a fully-configured analytical UI with layers, filters, time-playback, side-panel — Uber's data scientists' main viz tool. But:

1. **It's a *tool*, not a *library*.** Kepler ships a full UI: side panel, layer manager, configuration drawer. You can hide them but you're swimming against the framework. OPENGEM wants *one* custom 3D component embedded in a custom React layout — globe.gl gives you that directly; Kepler gives you a tool you have to hide most of.

2. **Bundle is enormous.** Kepler + deck.gl + the UI is 2-3 MB gzipped. globe.gl is 600KB. For a public dashboard page targeting fast loads, this matters.

3. **3D globe mode is recent and second-class.** Kepler's primary mode is 2D map (Mapbox). The globe mode was added later, less polished, less customizable.

4. **Branding/aesthetic.** Kepler looks like Kepler. globe.gl is themable from scratch — black background, custom country-fill colors, custom arc colors, custom typography. Bloomberg-orange achievable.

5. **State management.** Kepler uses Redux internally and exposes a Redux-action API for programmatic control. globe.gl uses imperative chained calls (`globe.pointsData([...]).pointAltitude(d => ...).pointColor(d => ...)`). The chained API is simpler for an embedded component.

Kepler *does* have advantages — better at "I have 10M points and need to filter them in real time" — but OPENGEM's geopolitical pulse isn't 10M points. It's hundreds of countries × dozens of arcs at any given time-slice. globe.gl handles this trivially.

## Why Three.js raw is *not* the default

Building a globe from raw Three.js means:
- Loading a sphere mesh, applying an Earth texture (NASA Blue Marble is the typical choice), setting up lighting.
- Projecting lat/lng to 3D coordinates yourself.
- Drawing arcs (a great-circle path in 3D) requires real math.
- Picking (mouse-over country detection) requires raycasting with polygon boundaries.
- Animation loops and timelines need wiring.

globe.gl is *exactly* this code, productized. The maintainer (Asturiano) has been iterating it for 6+ years. Re-implementing it is ~6 weeks of work for a maybe-better result. Skip.

Three.js stays in the OPENGEM stack as the escape hatch — when globe.gl can't do something (e.g., a custom shader effect for the "pulse" animation), drop down to Three.js for that specific feature. Three.js is a peer dependency of globe.gl, so it's already in the bundle.

## Cost / performance budget

For the geopolitical pulse page:
- globe.gl bundle: 600KB gzipped. Loaded on this page only via dynamic import (`const Globe = dynamic(() => import('react-globe.gl'), { ssr: false })`).
- Initial render: ~200ms on desktop, ~600ms on mobile.
- Frame rate with 1000 points + 200 arcs: 60fps desktop, 30fps mobile.
- Memory: ~100MB sustained.

Hosting cost: zero. It's all client-side.

## Ramp-up

- Day 1: install `react-globe.gl`, drop in a Next.js page, see a globe with country polygons.
- Week 1: color-coded choropleth by GPR index, mouse-over tooltips.
- Week 2: arcs for event flows, animated rings for breaking events.
- Week 3: time-slider integration, vintage selection, tearsheet export.
- Week 4: polish, theming to Bloomberg-orange terminal aesthetic.

A 1-month project for a competent React+Three.js dev. Significantly less if the dev already knows globe.gl.

## What about a 2D map fallback?

A 2D world map (D3-geo + topojson + Plot.geo, see L069) is the *correct* default for the home screen's small geo widget, the country-page locator, and the choropleth view. globe.gl is for the *flagship* geopolitical pulse page only. The 2D version is ~30 lines of Plot.

## What about Mapbox / MapLibre?

- **Mapbox GL JS**: now paid-tier for production usage. Hard skip.
- **MapLibre GL JS**: free OSS fork of pre-paid Mapbox. Great for street-level / mid-zoom interactive maps. Not the right tool for a country-level world view, but useful for any city-zoom features (e.g., port-watch port-by-port pages). EVALUATE-LATER for the port-page surface.

## Verdict

- **globe.gl + react-globe.gl** for the geopolitical pulse page: **ADOPT-V1**. ~$0/mo. 1-month ramp.
- **Three.js** as the escape hatch under globe.gl: **ADOPT-V1**. No extra cost (already a dep).
- **Kepler.gl**: **SKIP** as the primary; **EVALUATE-LATER** only for a one-off internal exploratory page if a contributor wants it.
- **MapLibre GL JS**: **EVALUATE-LATER** for port-page / city-zoom views.
- **Mapbox GL JS**: **SKIP**. Paid.
- **D3-geo + Plot.geo** for all 2D world maps: **ADOPT-V1** (covered in L069).

## Cost summary

| Tool | Cost | Ramp |
|---|---|---|
| globe.gl + react-globe.gl | $0 | 1 month |
| Three.js | $0 (transitive) | as-needed |
| MapLibre GL JS | $0 | 1 week per page |
| Mapbox GL JS | (skipped) | (skipped) |
| Kepler.gl | (skipped) | (skipped) |

## What comes next

- **L072** picks the forecast-band charting library.
- **L101** is the Phase 2 deep dive on globe.gl integration patterns.

## Related

- [[L069-d3-vega-plotly]] — D3-geo + Plot for 2D maps, complementary
- [[L101-globe-gl-3d-pattern]] — Phase 2 deep dive
- [[L021-gdelt-ingestion]] — GDELT event stream feeds the arcs and rings
- [[L022-acled-conflict-data]] — ACLED feeds the hexbin density layer
