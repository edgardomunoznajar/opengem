# L164 — Supply-Chain Pulse Map

**Loop**: 164 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The decision

**Pick: 2D world map with three stacked layers: (a) port congestion choropleth-of-ports, (b) trade-flow arcs, (c) GSCPI dial in the top-right.**

The supply chain story doesn't fit in a single layer. It's bottlenecks (ports), flows (trade arcs), and a single composite (GSCPI). Three layers, one map.

## The three layers

### Layer 1 — Port congestion (choropleth-of-ports)

```
   Port congestion (PortWatch + IMF PortWatch API)
   Color: vessel-wait-time z-score vs port's 12mo baseline
   Size: vessel throughput

   • Long Beach    🔴 +2.4σ   (~25k TEU/day)
   • Rotterdam     🟡 +1.1σ
   • Shanghai      🟢 -0.2σ
   • Singapore     🟢 +0.3σ
```

Ports rendered as bubbles sized by throughput, colored by congestion z-score. Diverging palette (L148): cool = uncongested, hot = congested.

Hover a port: tooltip with name, country, current wait time, baseline, top inbound/outbound origins.

### Layer 2 — Trade-flow arcs (BACI + UN Comtrade deltas)

```
   Top trade flows by Δ-volume YoY
   Arc color: positive (growth) green | negative (decline) red
   Arc thickness: absolute change magnitude
```

Toggleable. Off by default to avoid clutter. When on:
- Arcs between origin/destination country pairs
- Top 50 pairs by absolute Δ-volume
- Hover → tooltip with: pair, product category, Δ-volume, previous baseline, source

Use cases:
- "Show me top declining trade pairs over the last quarter"
- "Show me US-China trade decoupling visually"

### Layer 3 — GSCPI dial

```
   ┌──────────────────────┐
   │  Global Supply Chain  │
   │  Pressure Index       │
   │                       │
   │       1.4σ            │
   │      ┃┃┃┃┃            │
   │     ▴               │
   │ -3   0  +3            │
   │  z-score              │
   │                       │
   │  Direction: rising    │
   │  ─╱╱─                 │
   └──────────────────────┘
   anchored top-right of map
   width: ~280px
```

The Federal Reserve Bank of New York's Global Supply Chain Pressure Index. We pull it directly from the NY Fed API (free, public).

Components: a current-value dial, a 5-year sparkline, a "direction" badge. Click → routes to `/indicator/gscpi` for the full chart.

## The composite map

```
   ┌────────────────────────────────────────────────────┐
   │  Supply-chain pulse  ────────  GSCPI dial          │
   │                                                     │
   │    [ Map with port bubbles, optional arcs ]        │
   │                                                     │
   │     ⚓  ⚓⚓     ⚓                                  │
   │       ⚓   ⚓⚓     ⚓⚓                              │
   │            ⚓⚓⚓⚓⚓                                 │
   │                  ⚓⚓⚓                              │
   │                                                     │
   │  ────────────────────────────────────────────────  │
   │  Ticker: recent port events                         │
   │  09:42 LBX queue spike (+12% over 7d)              │
   │  09:31 Suez transit delay reported                  │
   └────────────────────────────────────────────────────┘
```

## Filters

```
   Region:  [ Global ▼ ] | Pacific | Atlantic | Indo-Pacific | Mediterranean
   Window:  [ 24h ▼ ]   | 7d | 30d | 90d
   Product: [ All ▼ ]   | Containers | Bulk | Tankers | Auto
   Layer:   ☑ Ports  ☐ Arcs  ☑ GSCPI dial
```

## Region presets

- **Pacific**: West Coast US + East Asia
- **Atlantic**: East Coast US + Northwest Europe
- **Indo-Pacific**: South Asia + ASEAN + Australia
- **Mediterranean**: South EU + North Africa + Suez choke

Selecting a region zooms the map and filters port set to relevant ones.

## Drilldown — port detail

Clicking a port bubble opens a drawer:

```
   ┌──────────────────────────────────┐
   │  ✕  Port of Long Beach            │
   │  ────────────────────────────    │
   │                                    │
   │  Throughput (24h): 25k TEU         │
   │  Vessel wait time: 4.2 days        │
   │  Z-score: +2.4σ (highly congested) │
   │                                    │
   │  12-month wait sparkline:          │
   │  ─╱╲╱─╲─╱╲╱──╲─                    │
   │                                    │
   │  Inbound: CHN 38%, KOR 12%, JPN 8% │
   │  Outbound: USA-domestic            │
   │                                    │
   │  News:                             │
   │  • Truck driver shortage cited     │
   │  • Rail strike risk Apr-May         │
   │                                    │
   │  [Open port page →]                │
   └──────────────────────────────────┘
```

## Forecast layer

Toggle "Show forecast." When on, port bubbles encode 30-day forecast of congestion (not current). Forecast comes from OPENGEM's port-time-series model (a small VAR per port). Uncertainty shown via bubble outline:

```
   ⚪ ← thick outline = high uncertainty
   🔴 ← thin outline = high confidence
```

This is the killer feature — a forward-looking supply chain map, not just a current-state one.

## The "what's stressing my supply chain" tool

For paid-tier users: enter a product category and a destination country. The map highlights:
- Origin countries that ship that product
- Ports that handle it
- Chokes between origin and destination

A "route stress score" appears in the top-right.

## Chokes

A small panel lists the active chokes:

```
   Active chokepoint status
   ────────────────────────
   Suez Canal      ✓ normal
   Panama Canal    ⚠ low water (Apr-May)
   Strait of Hormuz ✓ normal
   Strait of Malacca ✓ normal
   Bosporus         ✓ normal
   Bab-el-Mandeb   🚨 elevated (Houthi)
```

Each row is clickable → choke detail with traffic stats and recent events.

## URL contract

```
/supply-chain
/supply-chain?layers=ports,arcs&region=pacific&window=7d
/supply-chain?focus=port:lbx
/supply-chain?asof=2024-03-15
```

## Animation mode

"Animate" button plays 30 days of port congestion as 30 daily frames. Each frame stamps the date. Bubble colors morph.

Exportable as GIF (per L155 — this is the format of choice for supply chain content).

## The data sources

| Layer | Source | License | Refresh |
|---|---|---|---|
| Port congestion | IMF PortWatch | open | daily |
| Vessel positions | MarineTraffic AIS (free tier) | free | every 6h |
| Trade flows | UN Comtrade + BACI | CC-BY | monthly |
| GSCPI | NY Fed | public | monthly |
| Choke status | OPENGEM editorial + ACLED | mixed | event-driven |
| News | GDELT + Lloyd's List feeds | mixed | hourly |

## Editorial annotations

The map supports the same editorial overlay as L163 — labeled events: "Suez blockage 2021," "Houthi attacks 2023-2024," "Panama drought 2024." Curated by OPENGEM editorial.

## Tile in country page

Each country page (L123) for a major maritime nation shows a mini supply-chain tile: status of their primary ports + GSCPI mini-dial. Click → opens this page focused on that country's region.

## Mobile

At <640px:
- Map shrinks to a smaller bubble plot
- GSCPI dial moves below the map
- Trade arcs forced off
- Port ticker becomes a list below

## Implementation

- Library: D3 + topojson for the base map
- Port bubbles: D3 `geoPath` with size-encoded circles
- Arcs: D3 `geoInterpolate` bezier paths
- GSCPI dial: custom React component
- Animation: D3 transition over time series
- Server endpoint: `/api/supply-chain/snapshot?window=24h&region=pacific&layers=ports,arcs`
- Cache: 30min for ports, hourly for arcs, monthly for GSCPI

## Performance

- Initial map render: ~2 seconds on a mid laptop
- Animation playback: 30 frames in 10 seconds (cached server-side as a pre-rendered sequence)
- Bundle: ~140KB JS for the supply-chain mode (above the baseline)

## What we won't ship

- 3D ports / 3D vessels. The 2D layered map already conveys everything.
- Live vessel positions for every ship. Too much data, too little signal.
- Container-level tracking. Lloyd's List sells that; we don't compete on that.
- Trucking / rail network in V1. Maritime-focused at launch; ground modes V2.
