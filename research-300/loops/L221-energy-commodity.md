# L221 — Energy / Commodity Page

**Loop**: 221 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The thesis of this loop

Commodities are *the* macro accelerator: oil moves CPI everywhere, gas moves Europe, coal moves Asia, electricity moves manufacturing, food moves EM social stability, metals move construction. **And the open data is unusually rich** — EIA STEO for the US, IEA for OECD, Our World in Data for clean charts, World Bank Pink Sheet for benchmarks, IMF Primary Commodity Price System for everything else. The only thing genuinely closed is the *futures term structure* — but CME publishes settlement prices with a 24h delay, which is *exactly* the cadence OPENGEM operates on.

OPENGEM's energy/commodity page is the page that becomes the *citable commodity reference* — the page Marcus (the FT journalist) embeds when oil pops 5%, the page Damian (the YouTuber) screenshots in a "what's moving" thumbnail, the page Nadia (the SWF analyst) opens at 7am to scan inventory and term structure.

This loop **decides** the page structure (six commodity sub-pages + cross-commodity overview), the inventory + term-structure visualizations, and how to render shock-passthrough impact.

## The six commodity tracks

The page is organized around six sub-tracks, each a "first-class commodity":

1. **Oil** — WTI, Brent, OPEC basket; OPEC production; US strategic petroleum reserve; inventories (EIA weekly); futures term structure; refinery margins.
2. **Natural gas** — Henry Hub, TTF (Europe), JKM (Asia); storage levels; LNG flows; winter-summer spread.
3. **Coal** — Newcastle thermal, Rotterdam, API4/2; China imports.
4. **Electricity** — wholesale prices (PJM, CAISO, ERCOT, EPEX, Nord Pool); peak-hour vs base-load spreads.
5. **Food** — wheat, corn, soybeans, rice, sugar, coffee; USDA WASDE; FAO Food Price Index.
6. **Metals** — copper, aluminum, iron ore, gold, silver, nickel, lithium; LME inventories; smelter margins.

Each track has its own panel with: current price, term structure, inventory, historical comparison, and a "macro passthrough" widget showing implied CPI / GDP impact.

## Page structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ ENERGY / COMMODITY                                                   │
│ Oil • Gas • Coal • Electricity • Food • Metals                       │
└──────────────────────────────────────────────────────────────────────┘

[Track tabs]
 [Overview]  [Oil]  [Gas]  [Coal]  [Electricity]  [Food]  [Metals]

╔══════════════════════════════════════════════════════════════════════╗
║ OVERVIEW                                                              ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Master grid: every commodity, every benchmark ────────────────────┐
│ Commodity      │ Benchmark │ Spot     │ Δ 1d  │ Δ 30d │ Δ 1y  │YTD │
│ Crude oil      │ Brent     │ $82.45/b │ +0.8% │ +5.1% │ -3.4% │+11%│
│ Crude oil      │ WTI       │ $78.10/b │ +0.9% │ +5.3% │ -4.0% │+10%│
│ Nat gas (US)   │ Henry Hub │ $3.12/MMBtu│-1.1%│ -8.5% │+22% │-12% │
│ Nat gas (EU)   │ TTF       │ €38.40   │+0.5%│ -3.1% │+45%  │-8%  │
│ Nat gas (Asia) │ JKM       │ $12.30/MMBtu│+0.2%│-2.5% │+18% │-5%  │
│ Coal           │ Newcastle │ $135/t   │+0.0%│ +3.2% │-15%  │+8%  │
│ Power (US PJM) │ DA peak   │ $48/MWh  │+5.0%│+12%   │+22%  │+18% │
│ Wheat          │ CBOT SRW  │ $6.42/bu │+0.3%│+4.5%  │-12%  │+7%  │
│ Corn           │ CBOT      │ $4.85/bu │+0.5%│+2.1%  │-8%   │+5%  │
│ Soybeans       │ CBOT      │ $11.20/bu│+0.4%│+1.8%  │-10%  │+3%  │
│ Copper         │ LME 3M    │ $9420/t  │+1.2%│+8.5%  │+15%  │+22% │
│ Aluminum       │ LME 3M    │ $2580/t  │+0.5%│+3.1%  │+5%   │+8%  │
│ Iron ore       │ Tianjin   │ $112/t   │-0.8%│-5.4%  │-18%  │-10% │
│ Gold           │ LBMA AM   │ $2380/oz │+0.4%│+2.1%  │+18%  │+15% │
│ Silver         │ LBMA      │ $32.50/oz│+0.8%│+5.4%  │+24%  │+19% │
│ ... 30+ more                                                         │
└─────────────────────────────────────────────────────────────────────┘

┌─ Heatmap: 30d performance by commodity × benchmark ────────────────┐
│  Grid: rows = commodities, cols = benchmarks                        │
│  Color: -10% (red) → 0 (white) → +10% (green)                       │
│  Reveals "which commodity complex is moving" at a glance            │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ OIL TRACK                                                             ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Spot price chart (5y) ────────────────────────────────────────────┐
│  Lines: Brent, WTI, OPEC basket                                     │
│  Annotations: OPEC+ cuts, US SPR releases, geopol events            │
└─────────────────────────────────────────────────────────────────────┘

┌─ Term structure (Brent) ───────────────────────────────────────────┐
│  Y: $/barrel                                                         │
│  X: Front month → 24 months out                                      │
│  Lines: today / 1w ago / 1m ago / 1y ago                             │
│  Label: BACKWARDATION (tight market) or CONTANGO (oversupplied)      │
│  Current 1m-12m spread: -$1.20 (backwardation, but mild)             │
└─────────────────────────────────────────────────────────────────────┘

┌─ US weekly inventory (EIA) ────────────────────────────────────────┐
│  Bar chart: crude inventory by week, last 52 weeks                  │
│  Reference band: 5-year mean ±1σ                                    │
│  Current: 432Mb (within band, slightly above 5y average)            │
│  Strategic Petroleum Reserve: 365Mb (recovering from 2022 draw)     │
└─────────────────────────────────────────────────────────────────────┘

┌─ OPEC+ production tracker ─────────────────────────────────────────┐
│  Stacked bar by member country, last 24m                            │
│  Quota vs actual production divergence flagged                      │
│  Compliance heatmap (which countries are over/under their quota)    │
└─────────────────────────────────────────────────────────────────────┘

┌─ Macro passthrough widget ─────────────────────────────────────────┐
│  Current Brent at $82.45 vs 1y ago $85.36  →  Δ -3.4%                │
│  Implied 12m CPI impact (Kilian-Murphy-style passthrough):           │
│   - USA: -0.10pp                                                     │
│   - EUR: -0.16pp (higher pass-through due to fuel tax structure)     │
│   - DEU: -0.18pp                                                     │
│   - JPN: -0.22pp (import dependence)                                 │
│   - IND: -0.12pp                                                     │
│  [Link to full IRF on L211 shock library]                            │
└─────────────────────────────────────────────────────────────────────┘
```

```
╔══════════════════════════════════════════════════════════════════════╗
║ GAS TRACK                                                             ║
╚══════════════════════════════════════════════════════════════════════╝

  Three benchmarks: Henry Hub / TTF / JKM
  Storage panel: US, EU, China (where reported), Japan LNG inventory
  Winter-summer spread: a single number that prices the next winter risk
  LNG flow map: top 10 flows (US→EU, US→Asia, Qatar→Asia, etc.)
  Annual planner: which months historically tight (Jan-Feb), which loose
```

```
╔══════════════════════════════════════════════════════════════════════╗
║ ELECTRICITY TRACK                                                     ║
╚══════════════════════════════════════════════════════════════════════╝

  Wholesale price by market: PJM, CAISO, ERCOT, NYISO, MISO, EPEX (DE,
   FR, IT, ES), Nord Pool, AEMO, JEPX
  Day-ahead vs real-time spread
  Peak-hour vs base-load spread (tells about renewables share)
  Capacity factor by source: coal, gas, nuclear, wind, solar, hydro
  Carbon price (EU ETS, RGGI, CCA)
```

```
╔══════════════════════════════════════════════════════════════════════╗
║ FOOD TRACK                                                            ║
╚══════════════════════════════════════════════════════════════════════╝

  FAO Food Price Index (composite + 5 sub-indices)
  Per-commodity: wheat, corn, soy, rice, sugar, coffee, cocoa, palm oil
  USDA WASDE stocks/use ratios
  Cross-country bread / staple inflation (sub-component of CPI)
  EM social-stability score: real food inflation as % of consumer basket
```

```
╔══════════════════════════════════════════════════════════════════════╗
║ METALS TRACK                                                          ║
╚══════════════════════════════════════════════════════════════════════╝

  LME 3M prices: copper, aluminum, lead, zinc, nickel, tin
  Iron ore: Tianjin 62%fe (China import benchmark)
  LME stockpiles by metal
  Gold/silver/PGMs: separate "monetary metals" sub-panel
  Critical minerals: lithium, cobalt, rare earths (USGS + Benchmark)
  China copper smelter TC/RCs (treatment charges) — leading indicator
```

## The "macro passthrough widget" — every track gets one

Each commodity track ends with a **macro passthrough widget** that shows the implied CPI/GDP impact of the current price level vs 1y ago, per country. The math is the same IRF the shock library publishes (L211) but applied to the *actual* current shock rather than a canonical one. So a +12% Brent move over 12m → +0.12pp US CPI implied at 12m horizon, +0.20pp EU CPI implied, etc.

This is the *single feature* that turns a commodity dashboard into a macro forecasting tool. Bloomberg has commodity prices; OPENGEM has commodity prices *plus* the implied macro impact, vintaged, with the methodology linked.

## Inventory + term structure as the killer combination

The combination of **inventory level** (where are we relative to 5y mean?) and **term structure** (is the curve in backwardation or contango?) is the *most predictive* commodity-state diagnostic. A market in backwardation with low inventories is set up for a price spike. A market in contango with high inventories is bearish. **No free dashboard shows these two side-by-side per commodity.** OPENGEM does. The widget displays a 2×2 quadrant chart:

```
                          TERM STRUCTURE
                  Backwardation      Contango
              ┌─────────────────┬─────────────────┐
   Low        │   TIGHT MARKET  │   ROLL-YIELD    │
INVENTORY     │   (bullish)     │   (mixed)       │
              ├─────────────────┼─────────────────┤
   High       │   STORAGE SHIFT │   OVERSUPPLIED  │
              │   (mixed)       │   (bearish)     │
              └─────────────────┴─────────────────┘
```

Each commodity gets a dot. Where it sits in the quadrant tells you the regime. Drag handle lets the user adjust their "low/high inventory" threshold.

## Data sources / adapter dependencies

| Input | Source | Adapter | Status |
|---|---|---|---|
| Oil spot (Brent, WTI) | EIA + ICE settle (1d lag) | `opengem-data-eia` ⚠️ NOT YET BUILT | gap |
| Oil futures term structure | CME settle (1d lag) | `opengem-data-cme` ⚠️ NOT YET BUILT | gap |
| US weekly oil inventory | EIA Petroleum Status Weekly | `opengem-data-eia` | gap |
| OPEC production | OPEC monthly + IEA OMR + JODI | `opengem-data-opec` ⚠️ NOT YET BUILT, `opengem-data-iea` ⚠️ | gap |
| Natural gas (US Henry Hub) | EIA + CME | `opengem-data-eia`, `opengem-data-cme` | gap |
| EU TTF | ICE settle | `opengem-data-ice` ⚠️ NOT YET BUILT | gap |
| Asia JKM | S&P Platts (closed); proxy via cargoes data | `opengem-data-plats-proxy` ⚠️ NOT YET BUILT | gap |
| Coal | argus, IHS (closed); proxy via spot indices | proxy adapter | gap |
| Electricity | PJM, CAISO, ERCOT public + EPEX + Nord Pool + AEMO | per-ISO adapters | gap |
| Food prices | FAO FPI + USDA WASDE + CBOT settle | `opengem-data-fao` ⚠️ NOT YET BUILT, `opengem-data-usda` ⚠️ NOT YET BUILT | gap |
| Metals | LME settle (closed, 24h delay tier), CME futures | `opengem-data-lme` ⚠️ NOT YET BUILT, `opengem-data-cme` | gap |
| World Bank Pink Sheet | WB Pink Sheet | `opengem-data-wb` extension | partial |
| IMF Primary Commodity | IMF | `opengem-data-imf` extension | partial |

**Identified gaps**: EIA, IEA, CME, ICE, FAO, USDA, LME, OPEC. Energy/commodity is the *most adapter-intensive* page in this batch.

## JSON contract — per-commodity headline

```json
{
  "commodity": "crude_oil",
  "benchmark": "brent",
  "vintage": "2026-06-06",
  "spot": {"price": 82.45, "currency": "USD", "unit": "barrel"},
  "changes": {"1d_pct": +0.8, "30d_pct": +5.1, "1y_pct": -3.4, "ytd_pct": +11},
  "term_structure": {
    "front_month_price": 82.45,
    "month_12_price": 81.20,
    "spread_1m_12m": -1.25,
    "regime": "backwardation_mild"
  },
  "inventory": {
    "us_crude_stocks_mb": 432,
    "vs_5y_mean_z": +0.3,
    "spr_mb": 365
  },
  "macro_passthrough": {
    "implied_12m_cpi_impact_pp": {"USA": -0.10, "EUR": -0.16, "JPN": -0.22, "IND": -0.12},
    "implied_12m_gdp_impact_pp": {"USA": +0.05, "EUR": +0.08, "JPN": +0.10, "IND": +0.06},
    "passthrough_model": "kilian-murphy-svar"
  },
  "cite_this": "https://opengem.org/commodity/oil/brent?v=2026-06-06"
}
```

## What this loop produced

- Six commodity tracks + an overview view.
- The 2×2 inventory × term-structure quadrant as a regime classifier.
- A macro-passthrough widget on every track translating commodity moves into per-country CPI/GDP impact.
- The biggest adapter-gap list of any single page (EIA, IEA, CME, ICE, FAO, USDA, LME, OPEC).

## What comes next

- **L211** shock library (oil shock IRF feeds the passthrough widget).
- **L222** climate-macro (carbon prices link here).
- **L226** supply chain (commodity flows overlay).

## Related

- [[L001-vision-statement]]
- [[L211-shock-library]] — oil shock IRF
- [[L226-supply-chain-bottleneck]]
- [[L222-climate-macro-link]]
- [[L218-trade-balance-capital-flows]]
- [[L146-iconography-system]] — `zap`, `flame`, `factory`
