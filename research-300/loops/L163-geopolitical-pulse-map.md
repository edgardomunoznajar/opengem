# L163 — Geopolitical Pulse Map

**Loop**: 163 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The decision

**Default: 2D Mercator-corrected choropleth. 3D globe is the secondary "showcase" view, picker-toggled.**

Reasoning:
- 2D choropleths are faster to read for comparative magnitude.
- 2D is also lighter (no WebGL), accessible on low-end devices, easier to screenshot.
- 3D globes are visually striking but harder to scan ("where's Mongolia again?").
- We ship both; the default is 2D.

L071 will weigh in on the 3D implementation. For this artifact: design both modes.

## The data

The pulse map is driven by GDELT 2.0's Goldstein scale + tone aggregations, plus our derived Geopolitical Pressure Index (GPI):

- **GDELT events** (last 24h, 7d, 30d windows): event counts per country
- **Goldstein scale**: -10 (extreme conflict) → +10 (extreme cooperation), averaged per country
- **Tone score**: news sentiment, averaged
- **GPI composite**: our weighted blend (defined in L030, scored in L191)

The map encodes GPI as the primary signal.

## 2D choropleth — the default view

```
   Geopolitical pulse, last 24h
   ──────────────────────────────────────────────
                       ┌──────────────────────┐
                       │                       │
                       │      [world map]      │
                       │       2D-projected    │
                       │       Equal Earth     │
                       │                       │
                       │  ▣ ░░░░ ▥ ▣▣ ░ ▥▥    │
                       │     (color-encoded)   │
                       └──────────────────────┘
   Color scale (diverging): cool → calm, hot → stressed
       ▢▢▢▢▢▢▢▢▢▢▢
      -3 -2 -1  0 +1 +2 +3   Goldstein-z (last 24h)

   Click a country: drilldown panel
```

Projection: **Equal Earth** (Šavrič / Patterson / Jenny, 2018). Equal-area, low distortion, modern. Not Mercator (which lies about Greenland).

Boundaries: Natural Earth admin-0 boundaries at 1:50m scale.

Coloring: divergent palette from L148 (RdBu-equivalent), centered on 0.

## Drilldown on click

Clicking a country opens a panel (drawer per L150/151):

```
   ┌────────────────────────────────────┐
   │  ✕  Türkiye                         │
   │  ────────────────────────────────   │
   │                                      │
   │  GPI (24h):     -1.4   stressed     │
   │  Goldstein:     -2.1                 │
   │  Event count:   234                  │
   │  Top sources:                        │
   │   • Anadolu (TR)                     │
   │   • Reuters                          │
   │                                      │
   │  Top event types:                    │
   │   • Diplomatic statement (98)        │
   │   • Border incident (32)             │
   │                                      │
   │  Latest events:                      │
   │   • 13:00 — TR-SY border tension     │
   │   • 11:42 — TCMB rate decision       │
   │                                      │
   │  [Go to Türkiye country page →]      │
   └────────────────────────────────────┘
```

## Layer panel

Top-right of the map: layer toggles.

```
   [▢ Conflict  ▢ Trade  ▢ Sanctions  ▢ Elections  ▢ Alliances]
   Time window: [24h ▼]   [Animate ▶]
```

- Conflict: ACLED + GDELT cameo events
- Trade: trade flows (BACI deltas, port congestion)
- Sanctions: OpenSanctions deltas
- Elections: calendar overlay
- Alliances: BIS-style alliance arcs

Multiple layers stack with reduced opacity.

## Time window

```
   [ 24h ] [ 7d ] [ 30d ] [ 90d ] [ Custom ]
```

The "Animate" button plays a 10-second sequence showing the GPI evolution over the selected window. Frames at daily intervals. Each frame stamps the date in the corner.

This is the GIF-exportable form (L155).

## 3D globe — the showcase mode

Toggle "Globe" in the top-right.

Renders as a Three.js globe with the same choropleth but wrapped on a sphere:

```
                 ─.─
              ╱╱─. ─╲╲
            ╱     . ─ ╲
           │     . ─   │
            ╲    . ─  ╱
              ╲─. ─╱╱
                 ─
        rotates with cursor drag
        scroll-to-zoom
        click-to-focus
```

- Library: `globe.gl` (which wraps Three.js) — handles the WebGL pipeline.
- Performance: animated rotation throttled to 30fps; rotates pause on hover.
- Click a country: globe rotates to face it, then opens the drilldown panel.
- Animated arcs: for the "alliances" layer, draws bezier arcs between countries.

The globe is gorgeous for screenshots and demo videos. It's the lousier work surface.

## Layered events on the globe

Events render as glowing dots above the surface:
- Conflict events: red dots, intensity = severity
- Trade events: amber arcs, opacity = volume change
- Diplomatic events: blue dots
- Elections: flag-emoji billboards above the country

Dots fade over 10s if not refreshed.

## The "ticker" strip

Below the map (both 2D and 3D), a live ticker of the latest GDELT events:

```
   ┌──────────────────────────────────────────────────────────┐
   │ 13:42 TR · diplomatic statement on cross-border tensions │
   │ 13:38 RUS · CB intervention in fx markets                │
   │ 13:31 USA · Senate hearing on AI regulation              │
   │ 13:28 CHN · trade ministry comments on tariffs           │
   └──────────────────────────────────────────────────────────┘
```

Scrolling autoplay (pauses on hover). Each item is clickable → news drawer.

## Color legend

A diverging swatch below the map with clear "more cooperative" → "more stressed" labels. The scale is fixed (not relative to current view) so global comparisons are stable across time.

## Performance

2D mode:
- TopoJSON of admin-0 boundaries: ~120KB gzipped at 1:50m
- Render: SVG path per country
- Hover/click: native DOM events
- Bundle: ~80KB JS for the 2D mode

3D mode:
- globe.gl + Three.js: ~600KB JS
- Texture: lazy-loaded after toggle
- Frame budget: 16ms target on a mid laptop, 33ms on mobile

3D mode is gated behind a click — never autoloaded.

## Accessibility

Color encoding has alt:
- Hovering or focusing a country reads the value: "Türkiye, GPI minus 1.4, stressed."
- A "table view" toggle renders the same data as a sortable accessible table.
- A "high contrast" toggle uses an alternative diverging palette tuned for tritan vision.

## URL contract

```
/pulse?window=24h&layers=conflict,sanctions&mode=2d
/pulse?window=7d&mode=globe&focus=tur
/pulse?asof=2025-09-15T18:00:00Z   ← time machine (L173)
```

`asof` enables historical replay — landing on the pulse map as it appeared on a specific date.

## Streaming refresh

The 24h window auto-refreshes every 5 minutes via SSE or polling. The map smoothly updates colors. A small indicator in the corner: "live · refreshed 30s ago." Disabled by default on mobile to save battery; toggleable.

## Country page integration

Each country page (L123) includes a "Pulse summary" tile at the top, mini-globe focused on the country. Click → opens the full pulse map focused on this country.

## Editorial overlay

A "Editorial pulses" toggle layers OPENGEM editorial annotations: named events (e.g., "G7 summit"), labeled bands (e.g., "Iran-Israel tension period"). Curated, not user-submitted.

This is the analyst-friendly layer — gives the map a narrative spine.

## Implementation

- Library 2D: D3 + `topojson-client` for projection
- Library 3D: `globe.gl` + Three.js
- Both modes share a data store; only the renderer differs
- Server endpoint: `/api/pulse?window=24h&layers=...` returns GeoJSON + per-country score
- Cache: 5min TTL on 24h window, 30min on 7d, hourly on 30d

## What we won't ship

- 3D globe by default. Too heavy for "pop the dashboard, glance, leave."
- "Hot zones" auto-highlighted with red flashing — looks alarmist and unprofessional.
- Twitter/X firehose layer. The signal is too dirty without LLM filtering, and we're not running that for free at this scale.
- Country-pair bilateral relationship graph. It's a feature for L225, not the pulse map.
