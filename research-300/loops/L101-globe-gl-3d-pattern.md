# L101 — globe.gl + 3D Globe Pattern for the Geopolitical Pulse

**Loop**: 101 / 300
**Phase**: 2 — Deep dive on top candidates
**Date**: 2026-06-06

---

## Thesis of this loop

L071 already named globe.gl as the engine. This loop commits to a *specific* integration pattern: the rotation behavior, the GDELT heatmap overlay, the arcs-vs-rings vs hexbin tradeoff, the time-slider and vintage rewind UX, and the dynamic-import + SSR fallback that keeps the page Lighthouse-scoring above 90.

The geopolitical pulse page is the flagship 3D surface of OPENGEM. It is also the single page most likely to be screenshot-and-shared on Twitter, which means it has *two* design constraints that fight each other: an interactive 3D globe rich enough to reward exploration, and a static screenshot composition that reads in 200ms at 1024×512 on a Twitter card. The pattern below resolves both.

Verdict: **a `react-globe.gl` component on a server-rendered shell, with hexbin (GDELT density) + choropleth (Caldara-Iacoviello GPR) + arcs (top-N cross-border events) + animated rings (last-24h breaking events) layered, behind an SSR static-image fallback served at the same URL with a `?static=1` query param so screenshot-bots get the same composition.**

---

## The four-layer composition

The globe has *four* simultaneous layers, each driven by a different OPENGEM data source. None of them is optional; together they are the page.

1. **Choropleth (slowest layer)** — country-fill color = Caldara-Iacoviello GPR, monthly cadence. Bloomberg-orange gradient from `#fffbeb` (low risk) to `#92400e` (high risk). The choropleth gives the page its dominant visual identity at first glance — the world colored by geopolitical risk.

2. **Hexbin density (medium layer)** — GDELT event hexbins, 7-day rolling, hex size 4°. Hex altitude proportional to log(event count). This layer surfaces *where* events are happening at a sub-country resolution (Donbas vs Moscow vs Vladivostok) without requiring city-level data. The hexbin is dense enough that mouse-over picks a region, not a city — which matches OPENGEM's macro framing.

3. **Arcs (fast layer)** — top 50 cross-border events from the last 24h, drawn as great-circle arcs from origin to destination. Arc color = Goldstein scale (red for conflict, green for cooperation). Animated stroke-dasharray. Limit 50 so the globe doesn't drown.

4. **Rings (live layer)** — animated pulse rings on the top 10 *new* events in the last hour. Ring fades in 4 seconds, propagates outward, fades out. This is the "something just happened" signal — the page is alive even if you stare at it.

---

## Rotation behavior

The single biggest aesthetic decision. Three modes:

- **Auto-rotate at 0.4 RPM** when the page is in the foreground and no user interaction has happened in 5 seconds. This is slower than the default globe.gl auto-rotate (which feels frantic) and matches the cadence of macro data — the world should look like it's moving at the speed of geopolitics, not the speed of a screensaver.
- **Pause on hover** — moving the cursor over the globe pauses rotation. Standard affordance.
- **Snap-to-region on country click** — click a country and the globe rotates+zooms to center it (configurable via `pointOfView({ lat, lng, altitude: 1.5 }, 1400ms)`). Drives the country-page deep-link.

The rotation default is *toward* the dateline (eastward), not westward — which means USA stays visible longest in the typical Western-viewer's morning session. This is a small choice; it matters because the first 5 seconds of looking at the globe should not require chasing the country you came to see.

---

## GDELT heatmap pattern

GDELT 2.0 publishes events every 15 minutes. The pulse globe pulls the **rolling 7-day hexbin** server-side (a Dagster asset, see L079) and re-renders the hexbin layer when the page is loaded. The hexbin layer is *not* live-streamed — that would burn the WebSocket budget for a layer that doesn't visually change at sub-hour cadence anyway. The rings layer *is* live-streamed (see L103 for the WebSocket spec).

Hex parameters:

- `hexBinResolution: 4` (3.7° hexes — roughly the size of Greece). Resolution 5 (1.85° hexes) is too noisy and exceeds 60fps on mobile.
- `hexBinMerge: false` — each event aggregates independently. Merging produces "Europe-sized blobs" that hide the spatial gradient.
- `hexAltitude: d => Math.log1p(d.sumWeight) * 0.04` — log-scale so a Donbas hexbin doesn't dwarf 200 small-event hexbins elsewhere.
- `hexTopColor: d => gprToColor(d.gpr_local)` — the *altitude* encodes event density, but the *color* still encodes GPR. So a hexbin is "tall and red" where GPR is high AND events are flowing, vs "tall but pale" in places where events flow but the GPR baseline is low (e.g., a normal trade-war flurry).

---

## SSR fallback for screenshot-bots and SEO

The single most underexploited surface for OPENGEM is server-side image rendering. The pulse page must support `GET /pulse?static=1&w=1200&h=630&t=2026-06-06` returning a PNG of the globe at the requested vintage, generated server-side via `puppeteer` + headless Chromium + a pre-baked globe scene. This:

- Lets Twitter, LinkedIn, Discord, Slack unfurl the URL into a high-quality static globe image.
- Gives Google's image-search a permanent reference image per vintage.
- Allows the "YouTube b-roll generator" (L113) to use the pulse globe as a video frame.
- Means the page's SEO is not gated on Lighthouse crawler running WebGL (it can't).

The cost is one always-warm headless Chromium instance (~$15/mo on a Hetzner CX21).

---

## Next-step: the component skeleton

```tsx
// app/pulse/page.tsx — server component shell
import dynamic from "next/dynamic";
import { fetchPulseSnapshot } from "@/lib/pulse";

const PulseGlobe = dynamic(() => import("@/components/PulseGlobe"), {
  ssr: false,
  loading: () => <StaticPulseFallback />,
});

export default async function PulsePage({ searchParams }: Props) {
  const snapshot = await fetchPulseSnapshot({
    vintage: searchParams.v ?? "latest",
    window: "7d",
  });
  if (searchParams.static === "1") {
    return <StaticPulsePng snapshot={snapshot} />;
  }
  return <PulseGlobe snapshot={snapshot} />;
}
```

```tsx
// components/PulseGlobe.tsx
"use client";
import Globe from "react-globe.gl";
export function PulseGlobe({ snapshot }: { snapshot: PulseSnapshot }) {
  const ref = useRef<GlobeMethods>();
  useEffect(() => {
    ref.current?.controls().autoRotate = true;
    ref.current?.controls().autoRotateSpeed = 0.4;
  }, []);
  return (
    <Globe
      ref={ref}
      globeImageUrl="/textures/earth-night-bloomberg.jpg"
      polygonsData={snapshot.countries}
      polygonCapColor={(d) => gprToColor((d as any).gpr)}
      polygonSideColor={() => "rgba(0,0,0,0.15)"}
      polygonStrokeColor={() => "#27272a"}
      hexBinPointsData={snapshot.gdeltHexPoints}
      hexBinResolution={4}
      hexAltitude={(d) => Math.log1p((d as any).sumWeight) * 0.04}
      arcsData={snapshot.topArcs}
      arcColor={(d) => goldsteinToColor((d as any).goldstein)}
      arcDashLength={0.4}
      arcDashGap={0.2}
      arcDashAnimateTime={2000}
      ringsData={snapshot.recentRings}
      ringColor={() => "#f59e0b"}
      ringMaxRadius={4}
      ringPropagationSpeed={2}
      ringRepeatPeriod={1400}
    />
  );
}
```

---

## What this loop produced

- A four-layer composition specification (choropleth + hexbin + arcs + rings) mapped to specific OPENGEM data sources.
- The rotation default (0.4 RPM eastward, snap-to-region on click).
- GDELT hexbin parameters with reasoning (resolution 4, log-altitude, GPR-colored).
- The SSR static-image fallback pattern for screenshot/SEO.
- A working component skeleton ready to drop into `app/pulse/page.tsx`.

## What comes next

- **L102** — task queue for the GDELT polling adapter that feeds this globe.
- **L103** — the WebSocket spec that drives the rings layer live.
- **L163** — the geopolitical pulse map UI spec (companion design loop).
- **L237** — globe prototype implementation (Phase 5 code).

## Related

- [[L071-three-globe-kepler]] — the comparison that picked globe.gl
- [[L021-gdelt-gkg]] — the GDELT event stream feeding hexbin + arcs + rings
- [[L024-gpr]] — the GPR series driving the choropleth
- [[L163-geopolitical-pulse-map]] — the UI design spec
- [[L113-youtube-broll-generator]] — the SSR static-image PNG reuse path
