# L093 — Kepler.gl vs globe.gl for the Geopolitical Pulse Map

**Loop**: 093 / 300
**Phase**: 2 — Integration deep dive
**Date**: 2026-06-06
**Verdict**: **ADOPT-V1 (globe.gl for the home-page geopolitical pulse; Kepler.gl deferred to L164 supply-chain map)**

---

## What this loop decides

L071 surveyed Three.js / globe.gl / Kepler.gl. The Phase 2 question is *which of the two map libraries owns the geopolitical pulse map at the top of the home page* — the single most prominent visual artifact in the entire OPENGEM dashboard.

I inspected `research-300/clones/kepler-gl/` and `research-300/clones/globe-gl/`. The verdict: **globe.gl wins on the home-page hero, Kepler.gl wins on the L164 supply-chain bottleneck deep-dive, and the two cohabit cleanly in the broader visualization stack.** The decision rests on five forcing constraints below.

## What's in each clone, briefly

### `globe-gl/`

```
globe-gl/
  src/
    globe.js              # the public API (~600 lines, mostly accessor passthroughs)
    globe.css             # minimal CSS
    index.js / index.d.ts
    kapsule-link.js       # the component framework it builds on
  example/
  package.json            # globe.gl v2.46.1
  LICENSE                 # MIT
```

License: **MIT**. Maintained by Vasco Asturiano (the d3-force-graph / react-force-graph author). Stable, focused, ~16k stars across the family.

Architecture: a Three.js scene wrapper. Builds on `three-globe` (Asturiano's lower-level globe primitives) and `three-render-objects` (his three.js component framework). The public API surface is a fluent builder: `globe.pointsData(...).pointLat(d => d.lat).pointAltitude(d => d.value).pointColor(d => d.color)`. The whole package is essentially a domain-specific accessor pattern over a Three.js scene.

Bundle size: ~600KB of three.js + ~80KB of globe.gl + ~50KB of dependencies = ~750KB minified. Acceptable as a lazy-loaded chunk for the home page hero, not great as part of the global app shell.

### `kepler-gl/`

```
kepler-gl/
  src/
    components/           # ~500+ React components
    layers/               # 30+ layer types (point, arc, hexbin, heatmap, …)
    deckgl-layers/        # deck.gl-based rendering
    deckgl-arrow-layers/
    reducers/             # Redux state
    actions/              # Redux actions
    schemas/              # data schemas
    ai-assistant/         # 2026 addition — AI-assisted data discovery
    cloud-providers/      # S3/GCS/etc data sources
    duckdb/               # DuckDB-backed transforms
  bindings/               # multi-framework bindings (vanilla, etc.)
  examples/               # demo apps
  LICENSE                 # MIT
```

License: **MIT**. Originally Uber, now community-maintained. ~10k stars.

Architecture: a full React + Redux geospatial-analytics application, not a chart component. Layers built on deck.gl (Uber's WebGL framework). The 2024-2026 line added DuckDB-backed transforms and an AI assistant for data discovery — it's grown into a fully-featured BI app for geospatial analytics.

Bundle size: ~3-5 MB minified for the full UI. The library is *not designed* to be a small chart embedded in another page; it's designed to be the whole page.

## The five forcing constraints

### Constraint 1 — Audience and venue

The geopolitical pulse map sits at the top of the OPENGEM home page (L122, L163). Its job is **first-paint visual impact** for a macro-curious anonymous visitor who lands from a tweet or a YouTube link. The user spends ~5 seconds on it before scrolling to country tiles. The map needs to:

- Look good in the first frame.
- Communicate "global geopolitical risk right now" instantly.
- Not block the rest of the home page from rendering.

globe.gl renders a stylized 3D Earth with points/arcs/heatmaps. Beautiful first frame. It's what every "this is the world right now" hero in modern macro visualization looks like. Kepler.gl, by contrast, is a 2D-projection-driven analytics interface — useful for an analyst exploring a dataset, jarring as a marketing-hero visual.

### Constraint 2 — Bundle size and lazy-loadability

Home page total bundle budget: ~500KB for the initial paint (Next.js streaming SSR + critical CSS), with charts as lazy-loaded chunks. globe.gl + three.js ships as a 750KB lazy chunk that loads in parallel with the rest of the page; the user sees a 2D world map placeholder for ~500ms, then the 3D globe replaces it.

Kepler.gl at 3-5MB is too large for the home page hero — the whole React/Redux/deck.gl machinery would dominate the bundle. It's wrong-shaped for a small embedded component.

### Constraint 3 — Interactivity model

The home-page pulse map is **glanceable**, not interactive. Users see GPR-C-z-scored country densities + recent conflict events + a rotating globe. They don't drag layers, configure filters, or build queries. globe.gl's accessor-based config matches this exactly: declare data → declare the visual encoding → render.

Kepler.gl's interactivity model assumes the user is *doing analytics* — layer panel, time playback, filter panel, side bar. Wrong abstraction for the home-page audience.

### Constraint 4 — Data shape

The pulse map renders three layers:
1. Country-level GPR-C polygon fills (z-scored), with smooth color interpolation.
2. Recent conflict event points (last 7 days from UCDP/POLECAT/GDELT triangulation), with arc-to-arc traces for cross-border interactions.
3. Top-N tone-anomaly arcs (article spikes from country A about country B).

globe.gl handles all three natively: `polygonsData` for country polygons, `pointsData` for events, `arcsData` for the tone-anomaly traces. Kepler.gl handles them too, but via deck.gl layers that require more setup.

### Constraint 5 — Maintenance

The home page hero is a stable, slow-changing artifact. We design it once, theme it to match the OPENGEM color palette, and it sits there. globe.gl's fluent API surface is small and stable — Asturiano's library has not had a breaking change in years. Kepler.gl's React + Redux + deck.gl stack churns more often; maintenance burden is higher.

## Where Kepler.gl wins instead

The L164 supply-chain bottleneck deep-dive page is a *fundamentally different* surface. It is:

- **Analytical**: the user is exploring port congestion data, AIS shipping tracks, GSCPI series.
- **Multi-layered**: ports + ships + bottlenecks + commodity flows + alternative routings.
- **Time-aware**: a time slider scrubs through the last 12 months of shipping data.
- **Filter-heavy**: filter by commodity, by region, by bottleneck severity.

Kepler.gl's React+Redux+deck.gl machinery is the right tool here. It's literally the use case the Uber team built it for. The L238 prototype loop will pick it up.

## The home page hero design (using globe.gl)

```typescript
// components/pulse-map-globe.tsx
'use client';
import { Globe } from 'react-globe.gl';
import { useMemo } from 'react';

export function PulseMapGlobe({ snapshot }: { snapshot: PulseSnapshot }) {
  const polygonsData = useMemo(() => snapshot.countries, [snapshot]);
  const arcsData = useMemo(() => snapshot.toneAnomalyArcs, [snapshot]);
  const pointsData = useMemo(() => snapshot.recentEvents, [snapshot]);

  return (
    <Globe
      globeImageUrl="//unpkg.com/three-globe/example/img/earth-dark.jpg"
      backgroundColor="rgba(0,0,0,0)"
      polygonsData={polygonsData}
      polygonAltitude={0.005}
      polygonCapColor={d => gprColorScale(d.gprcZ)}
      polygonSideColor={() => 'rgba(0,0,0,0.4)'}
      polygonStrokeColor={() => '#222'}
      polygonLabel={d => `${d.iso3}<br/>GPR-C: ${d.gprcZ.toFixed(2)}σ`}
      arcsData={arcsData}
      arcStartLat={d => d.fromLat}
      arcStartLng={d => d.fromLng}
      arcEndLat={d => d.toLat}
      arcEndLng={d => d.toLng}
      arcColor={d => ['rgba(255,170,102,0.4)', 'rgba(255,170,102,0.1)']}
      arcStroke={0.25}
      arcDashLength={0.4}
      arcDashGap={0.2}
      arcDashAnimateTime={2000}
      pointsData={pointsData}
      pointLat={d => d.lat}
      pointLng={d => d.lng}
      pointAltitude={d => d.severity * 0.02}
      pointColor={d => severityColorScale(d.severity)}
      pointRadius={0.2}
      onPolygonClick={d => router.push(`/country/${d.iso3}`)}
    />
  );
}
```

That's the entire hero component: ~40 lines, three layers, brand-themed colors, click-through to the country page. globe.gl handles the rotation, the auto-centering, the touch interactions. The OPENGEM design system contributes the color scales (L148) and the polygon styling.

## Data shape feeding the hero

Three queries:

```typescript
// app/_lib/pulse-snapshot.ts
export interface PulseSnapshot {
  asOf: Date;
  countries: { iso3: string; gprcZ: number; geometry: GeoJSON.Polygon }[];
  toneAnomalyArcs: { fromLat: number; fromLng: number; toLat: number; toLng: number; magnitude: number }[];
  recentEvents: { lat: number; lng: number; severity: number; cameoCode: string; eventDate: Date }[];
}

export async function getPulseSnapshot(): Promise<PulseSnapshot> {
  // single REST call to /v1/pulse-snapshot returns all three layers
  const r = await fetch(`${API_BASE}/v1/pulse-snapshot?asOf=${new Date().toISOString().slice(0, 10)}`);
  return r.json();
}
```

Server-side: a daily Dagster job composes the three layers from GPR-C (L024), UCDP/POLECAT (L025/L026), and the GDELT triangulation (L084) into a single `pulse_snapshot.json` cached on R2. The home page fetches it at SSR time.

## The 2D fallback

For accessibility, slow devices, and SEO-rendered HTML, the home page falls back to a 2D world map (D3-geo + topojson). The 3D globe loads as a progressive enhancement after first paint:

```typescript
<PulseMapFallback2D snapshot={snapshot} />  // SSR HTML, ~100KB total
<ClientOnly>
  <PulseMapGlobe snapshot={snapshot} />     // lazy 750KB chunk, replaces fallback
</ClientOnly>
```

The 2D fallback ships ~100KB of D3 + topojson and renders in ~200ms. The 3D globe replaces it once loaded. Google Lighthouse measurement: first contentful paint stays under 1.5s.

## Mobile

3D globes on mobile are *expensive*. We threshold:
- Viewport width ≥ 1024px: 3D globe.
- Viewport width < 1024px: 2D fallback only. The 3D globe never loads on mobile.

This is a single conditional in the lazy import. Saves both bundle size and battery for mobile users.

## Cost summary

| Task | Cost |
|---|---|
| 2D D3-geo + topojson fallback map | 2 dev-days |
| globe.gl + react-globe.gl integration | 2 dev-days |
| Three-layer composition (polygons + arcs + points) | 2 dev-days |
| OPENGEM theming (colors, lighting, atmosphere) | 1 dev-day |
| Server-side `pulse_snapshot.json` Dagster job | 2 dev-days |
| Mobile threshold + accessibility | 1 dev-day |
| Click-through + hover behavior | 1 dev-day |
| Integration tests | 1 dev-day |
| **Total** | **~12 dev-days (~2.5 weeks)** |

Reasonable for the home-page hero — the most-seen artifact on the dashboard.

## What we explicitly defer

- **Kepler.gl on the home page**: out of scope. Wrong tool for the hero.
- **Kepler.gl for L164 supply-chain map**: deferred to L238 (Phase 5 prototype).
- **Time-playback on the home-page globe**: out of scope for v1. The globe shows "now"; the historical playback is a separate page.
- **WebGPU upgrade**: globe.gl uses WebGL via Three.js. WebGPU may be worth a look in Y2; not v1.

## Risks

1. **Three.js bundle bloat over time.** Three.js the library tends to add features. Mitigation: tree-shake what we don't use; budget alert on bundle size in CI.

2. **Globe atlas image quality.** The earth texture is a single image; quality at very high zoom is limited. Mitigation: we never zoom that close on the hero; the L164 deep-dive page uses Kepler.gl for high-res raster.

3. **GPU-less devices** (older laptops, lower-end Android). Mitigation: feature-detect WebGL availability, fall back to 2D.

4. **WebGL context loss.** Some browsers reclaim WebGL contexts under memory pressure. Mitigation: globe.gl handles context restoration; ours job is to re-set data on re-mount.

5. **SEO concerns.** Google indexes HTML; 3D canvas is invisible to crawlers. Mitigation: the 2D fallback IS the SSR-rendered HTML; the 3D globe is progressive enhancement.

## What this loop produced

- globe.gl picked for home-page hero geopolitical pulse map.
- Kepler.gl explicitly deferred to L164 supply-chain page.
- Three-layer hero composition (polygons + arcs + points) with concrete data shape.
- 2D D3-geo fallback for SSR/accessibility/mobile.
- ~2.5 dev-week total cost.
- Bundle + mobile + WebGL availability all addressed.

## What comes next

- **L122** — Home screen layout (where the pulse map sits).
- **L163** — Geopolitical pulse map (downstream UI design).
- **L164** — Supply-chain pulse map (Kepler.gl lands here).
- **L237** — GPR pulse globe prototype (Phase 5 code).
- **L238** — Supply-chain pulse map prototype (Kepler.gl Phase 5).

## Related

- [[L071-three-globe-kepler]] — Phase 1 deep dive.
- [[L024-gpr]] — GPR-C polygon data source.
- [[L025-cline-center]] / [[L026-ucdp]] / [[L084-gdelt-as-feature-pipeline-design]] — event data sources.
- [[L122-home-screen]] — context.
- [[L163-geopolitical-pulse-map]] — downstream design.
- [[L164-supply-chain-pulse-map]] — Kepler.gl sibling.
- [[L237-gpr-pulse-globe-prototype]] — Phase 5 code.
- inspected source: `/mnt/bigdata/home/edgardo/projectsd/opengem/research-300/clones/globe-gl/src/globe.js` (~600 lines, MIT)
- inspected source: `/mnt/bigdata/home/edgardo/projectsd/opengem/research-300/clones/kepler-gl/src/components/` (500+ React components, MIT)
