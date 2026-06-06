# L226 — Supply Chain Bottleneck Page

**Loop**: 226 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The thesis of this loop

Supply chain stress was *the* macro story of 2021-2023 and is structurally a permanent feature post-2018 (US-China tariffs, post-COVID re-shoring, Red Sea, Panama Canal, Strait of Hormuz). The data is excellent: NY Fed's **GSCPI** (Global Supply Chain Pressure Index, the canonical aggregate), IMF's **PortWatch** (port-by-port congestion daily), the **IMF Trade Tracker** (HS-code-level real-time flows via AIS data), Drewry container freight rates, Baltic Dry Index, CME Group ocean-freight futures. **All open or semi-open. None of them are integrated into a single dashboard.** NY Fed has a chart. IMF PortWatch has a portal nobody uses. Drewry sells PDFs.

OPENGEM's supply-chain page does what every operations economist now does in Excel: pulls GSCPI + PortWatch + IMF Trade Tracker + freight rates + AIS-derived port congestion, and renders a per-route, per-port, per-commodity bottleneck heatmap. It is the page that — when the Houthis attack a tanker in the Red Sea — becomes the *citable* receipt for "here are the seven routes most affected, here is the historical price-impact of similar disruptions."

This loop **decides** the page structure, the bottleneck heatmap visualization, the GSCPI integration with finer-grained signals, and the price-passthrough widget.

## The four panels

1. **Macro signal** — GSCPI level + decomposition (what's pressuring the index now).
2. **Bottleneck heatmap** — port-by-port and route-by-route congestion.
3. **Flow tracker** — IMF Trade Tracker, HS-code real-time flows.
4. **Price impact** — freight rates + implied CPI passthrough.

## Page structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ SUPPLY CHAIN BOTTLENECK                                              │
│ GSCPI + PortWatch + IMF Trade Tracker + freight rates                │
└──────────────────────────────────────────────────────────────────────┘

[Tabs]
 [Macro signal]  [Bottleneck heatmap]  [Flow tracker]  [Price impact]

╔══════════════════════════════════════════════════════════════════════╗
║ MACRO SIGNAL PANEL                                                    ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ GSCPI headline ───────────────────────────────────────────────────┐
│ Current GSCPI: +0.65σ (above-normal pressure)                       │
│ 30d Δ: +0.20σ    90d Δ: +0.45σ    1y Δ: +0.90σ                       │
│ Status lozenge: 🟠 ELEVATED                                         │
│ Last updated: 2026-06-04 (monthly release)                          │
│ Series since: 1997                                                  │
└─────────────────────────────────────────────────────────────────────┘

┌─ GSCPI time series (25y) ──────────────────────────────────────────┐
│  Y: -2σ ... +5σ                                                     │
│  X: 2000 → 2026                                                     │
│  Line: GSCPI level                                                  │
│  Annotations: 2008 GFC, 2020-21 COVID surge (peaked +4.3σ),         │
│   2022 China re-opening, 2023 Red Sea, 2026 Strait of Hormuz inc.   │
└─────────────────────────────────────────────────────────────────────┘

┌─ GSCPI decomposition ──────────────────────────────────────────────┐
│  GSCPI = z-PMI-supplier-delivery + z-Baltic-Dry + z-Harpex +        │
│   z-air-cargo-rates + z-PMI-backlogs + z-PMI-stocks-purchases       │
│                                                                      │
│  Current attribution:                                                │
│   Supplier delivery times (PMI):   +0.40 (slow delivery)             │
│   Baltic Dry Index:                +0.15 (dry-bulk firm)             │
│   Harpex container shipping:       +0.20 (container tight)           │
│   Air cargo rates (Drewry):        -0.05 (normal)                    │
│   PMI backlog of orders:           +0.20                             │
│   PMI stocks of purchases:         -0.25 (de-stocking)               │
│                                                                      │
│  Stacked-bar chart over time showing how decomposition shifts.       │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ BOTTLENECK HEATMAP                                                    ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ World map: ports as dots ─────────────────────────────────────────┐
│  Each dot = a major port (PortWatch coverage, ~200 ports)            │
│  Dot color: congestion index (z-score of dwell-time + queue depth)   │
│  Dot size: throughput volume                                         │
│                                                                      │
│  Hover dot: tooltip with port name, current dwell time, % vs normal  │
│  Click dot: opens detail panel with 24m history                      │
│                                                                      │
│  Chokepoint overlays:                                                │
│   - Suez / Bab el-Mandeb (Red Sea)                                   │
│   - Strait of Hormuz                                                 │
│   - Panama Canal                                                     │
│   - Strait of Malacca                                                │
│   - English Channel                                                  │
│   - Strait of Gibraltar                                              │
│                                                                      │
│  Each chokepoint highlighted with: current flow vs 5y mean, current  │
│   diversion (e.g., "Red Sea: -78% transits, +14d transit time")      │
└─────────────────────────────────────────────────────────────────────┘

┌─ Top-10 most-bottlenecked ports ───────────────────────────────────┐
│ Port             │ Country │ Dwell-time │ vs 5y │ Z   │ Trend     │
│ Salalah          │ OMN     │ 5.8 days   │ +124% │+3.4 │ ▲ worse    │
│ Djibouti         │ DJI     │ 4.4 days   │ +88%  │+2.6 │ ▲ worse    │
│ Aqaba            │ JOR     │ 3.9 days   │ +58%  │+2.2 │ ▲ worse    │
│ Singapore        │ SGP     │ 2.1 days   │ +28%  │+1.4 │ ▲ rising   │
│ Rotterdam        │ NLD     │ 1.8 days   │ +12%  │+0.8 │ ─          │
│ Long Beach       │ USA     │ 1.6 days   │ -8%   │-0.3 │ ▼ improving│
│ Shanghai         │ CHN     │ 1.3 days   │ -15%  │-0.6 │ ▼ improving│
│ ...                                                                  │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ FLOW TRACKER (IMF TRADE TRACKER)                                      ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Real-time bilateral flow ─────────────────────────────────────────┐
│  Pick: origin country, destination country, HS-code product         │
│  → Renders 24-month time series of monthly trade flow (AIS-derived) │
│                                                                      │
│  Example: USA imports of HS-85 (electronics) from CHN                │
│   - 2022-01: $34bn                                                   │
│   - 2024-01: $29bn (post-CHIPS Act decline)                          │
│   - 2026-01: $24bn (continued substitution to MEX/VNM/MYS)           │
│                                                                      │
│  Substitution panel: who is replacing this flow?                     │
│   - MEX imports of HS-85 to USA up $8bn over same period             │
│   - VNM imports of HS-85 to USA up $6bn                              │
│   - MYS imports of HS-85 to USA up $4bn                              │
└─────────────────────────────────────────────────────────────────────┘

┌─ Sankey diagram (alternative) ─────────────────────────────────────┐
│  Top flows by HS-2 commodity, last 12 months                         │
│  Source country → destination country, width = $value                │
│  Filter by HS code, year, region                                     │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ PRICE IMPACT PANEL                                                    ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Freight rate panel ───────────────────────────────────────────────┐
│ Index                  │ Current │ 30d │ 90d │ 1y  │ vs pre-COVID │
│ Baltic Dry Index (BDI) │ 1,420   │ +5% │ +12%│ -8% │ +25%          │
│ Harpex (container ch.) │ 2,180   │ +18%│ +35%│ +120%│ +135%         │
│ Drewry WCI (Shanghai-LA)│$3,840  │ +25%│ +60%│ +180%│ +180%         │
│ Drewry WCI (Sh-Rotter) │ $4,420  │ +35%│ +95%│ +250%│ +250%         │
│ Air cargo rate (HKG-EU)│ $5.20/kg│ -2% │ -5% │ +12%│ +25%           │
└─────────────────────────────────────────────────────────────────────┘

┌─ Implied CPI passthrough widget ───────────────────────────────────┐
│  Current freight rate stack vs 5y avg → estimated CPI impact         │
│  at 6-9 month lag (containerized goods passthrough):                │
│                                                                      │
│   USA goods CPI: +0.20pp at peak (8m forward)                        │
│   EUR goods CPI: +0.35pp (heavier exposure to Asia routes)           │
│   GBR goods CPI: +0.32pp                                             │
│   JPN goods CPI: +0.18pp                                             │
│   KOR goods CPI: +0.28pp                                             │
│                                                                      │
│  Methodology: Kalemli-Özcan et al. (2024) freight-CPI passthrough    │
│  Each country also gets shipping-exposure weight (TEU per GDP)       │
└─────────────────────────────────────────────────────────────────────┘
```

## The bottleneck heatmap as the headline

The PortWatch dataset is the *single most under-utilized open dataset* in macro. It tracks 200+ ports daily via AIS data (ship positions, dwell times, queue depth). The map renders:

- **Choropleth dots** for ports.
- **Arcs** for routes (volume-weighted line thickness).
- **Chokepoint highlights** for the six global maritime chokepoints, with current-status badges (normal / disrupted / closed).
- **Animated playback** showing port congestion over the past 24 months — a powerful pedagogical tool for "look at how COVID-21 port crisis compares to Red Sea-26."

The page is *the* receipt for the Red Sea diversion story: when shipping moves around the Cape of Good Hope, the map shows Suez transits collapsing, Cape transits surging, transit-time extension by route, freight-rate impact, and per-country CPI implication.

## The substitution panel — the deepest insight

When US imports from China fall in a category, the *interesting question* is who picks it up. The substitution panel automatically detects compensating flows:

1. Identify decline in flow A→B for HS-code X.
2. Search for offsetting increases in C→B, D→B, E→B for the same HS-code over the same window.
3. Score the substitution share.

This automates a question every macro analyst answers manually today: "how much of US-China decoupling is being absorbed by Mexico vs Vietnam vs Malaysia?" The page publishes the answer with a time series.

## Data sources / adapter dependencies

| Input | Source | Adapter | Status |
|---|---|---|---|
| GSCPI | NY Fed | `opengem-data-gscpi` ✅ (already in roster) | ready |
| GSCPI components (PMI, BDI, Harpex, Drewry) | underlying sources | per-source | partial |
| IMF PortWatch | IMF PortWatch | `opengem-data-portwatch` ✅ (already in roster) | ready |
| IMF Trade Tracker | IMF | `opengem-data-imf-tt` ⚠️ NOT YET BUILT | gap |
| AIS-derived port congestion | MarineTraffic API + PortWatch | `opengem-data-marinetraffic` ⚠️ NOT YET BUILT | gap |
| Baltic Dry Index | Baltic Exchange (mostly closed); FRED has aggregate | `opengem-data-frb` extension | partial |
| Harpex | Harper Petersen | `opengem-data-harpex` ⚠️ NOT YET BUILT | gap |
| Drewry | Drewry (closed); proxy via spot reports | `opengem-data-drewry-proxy` ⚠️ NOT YET BUILT | gap |
| PMI Supplier Deliveries | S&P Global PMI (closed) — proxy via ISM (US) | partial | gap |

**Identified gaps**: IMF Trade Tracker, MarineTraffic, Harpex, Drewry-proxy. GSCPI and PortWatch are already named in the roster — building those two unlocks the page at ~70% capability.

## JSON contract — port detail

```json
{
  "port": "Salalah",
  "country": "OMN",
  "vintage": "2026-06-06",
  "throughput_teu_30d": 415000,
  "dwell_time_days_current": 5.8,
  "dwell_time_days_5y_avg": 2.6,
  "dwell_time_z_score": 3.4,
  "delta_vs_30d_ago_pct": +12,
  "history_24m_dwell_days": [...],
  "ais_derived_queue_depth_ships": 41,
  "tagged_disruption_event": "red-sea-2024-2026",
  "cite_this": "https://opengem.org/supply-chain/port/salalah?v=2026-06-06"
}
```

## What this loop produced

- The four-panel layout: macro signal + bottleneck heatmap + flow tracker + price impact.
- A GSCPI decomposition that shows *which* component is driving pressure.
- A port-by-port AIS-derived congestion heatmap with chokepoint highlights.
- A substitution panel auto-detecting where decoupled flows are landing.
- A freight-CPI passthrough widget per country.
- Four adapter gaps named (IMF Trade Tracker, MarineTraffic, Harpex, Drewry-proxy).

## What comes next

- **L218** trade balance (sankey + bilateral matrix as upstream).
- **L228** conflict tracker (chokepoint security overlays).
- **L221** energy/commodity (route disruptions affect oil/gas freight).

## Related

- [[L001-vision-statement]]
- [[L218-trade-balance-capital-flows]]
- [[L221-energy-commodity]]
- [[L228-conflict-tracker]] — chokepoint conflict signals
- [[L225-alliances-sanctions]]
- [[L146-iconography-system]] — `ship`, `package`, `factory`
