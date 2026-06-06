# L230 — Long-Horizon Scenario Page (Y2030, Y2050)

**Loop**: 230 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The thesis of this loop

Macro forecasting beyond 5 years is *categorically different* from cyclical forecasting. The 2030 horizon is where demography starts to bite, sovereign-debt math becomes binding, climate adaptation costs become measurable, and AI productivity assumptions diverge. The 2050 horizon is where SSP-style scenario thinking is the *only honest* method — point forecasts are absurd, but conditional scenarios with explicit assumptions are decision-grade. **Every long-horizon investor (sovereign funds, pension funds, insurers, multilateral DFIs, climate-adaptation funds) lives on these scenarios.** Yet there is no public dashboard that integrates the IPCC SSPs, the IIASA SSP database, demographic UN WPP projections, IMF long-run debt trajectories, OECD long-run productivity projections, and IEA energy projections into a single, vintaged, comparable, interactive view.

OPENGEM's long-horizon page is the page that makes 2030 and 2050 macro *legible*. It is the page that, when Nadia (the SWF analyst) is sizing the fund's 30-year strategic-asset-allocation, becomes the reference. It is the page that, when Lin (the policy researcher) writes about debt sustainability under SSP3, embeds the chart. It is the page that, when Marcus (the FT journalist) writes about "what 2050 looks like under different climate paths," can pull a country grid in 30 seconds.

This loop **decides** the page structure (cross-cut by horizon + by scenario + by country), the SSP × DSA × demography integration, and the "compound scenario" tool that lets the user toggle multiple sub-scenarios.

## The five canonical scenarios (SSPs as spine)

The page uses the **IIASA SSPs** as the canonical scenario spine (decided in L222). For each SSP, OPENGEM publishes harmonized, country-level projections of:

- **Population** (from UN WPP, scenario-adjusted via Wittgenstein assumptions).
- **GDP** (from IIASA SSP database + OECD Long-Run + country DSA layer).
- **GDP per capita** (derived).
- **Energy demand** (IIASA SSP energy module + IEA STEPS / APS / NZE overlays).
- **Emissions** (IIASA + EDGAR baseline).
- **Carbon price** (NGFS scenarios + IIASA energy module).
- **Debt-to-GDP** (OPENGEM DSA forward-projected under each SSP's macro assumptions).
- **Inflation regime mean** (under demographic + energy + productivity assumptions).
- **Real interest rate path** (derived from savings-investment under demographic + productivity assumptions).

The five SSPs (recapped):
- **SSP1**: Sustainability (low mitigation challenge, low adaptation).
- **SSP2**: Middle of the Road (baseline).
- **SSP3**: Regional Rivalry (high challenge both).
- **SSP4**: Inequality.
- **SSP5**: Fossil-fueled development.

## Page structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ LONG-HORIZON SCENARIOS — Y2030, Y2050                                │
│ IPCC SSPs × IIASA × UN WPP × OPENGEM DSA + IEA energy.               │
└──────────────────────────────────────────────────────────────────────┘

[Selectors]
 [Horizon: 2030 / 2050 / 2100 ▼]  [Scenario: SSP1-5 ▼]  [Country: ALL ▼]

╔══════════════════════════════════════════════════════════════════════╗
║ CROSS-COUNTRY SCENARIO GRID                                           ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Horizon = 2050, Scenario = SSP2 (Baseline) ───────────────────────┐
│ Country │GDP/cap│Pop M│Energy │Emis Mt│CO2/cap│DGDP%│Real r%│Lab dep │
│         │ k$    │     │EJ     │ CO2   │ tCO2  │     │       │ratio   │
│ USA     │ 78    │ 375 │ 95    │ 4.2   │ 11.2  │ 135 │  1.8  │ 0.59   │
│ CHN     │ 32    │ 1300│ 175   │ 8.5   │  6.5  │ 100 │  2.5  │ 0.50   │
│ IND     │ 18    │ 1670│ 65    │ 3.8   │  2.3  │  85 │  3.5  │ 0.42   │
│ DEU     │ 65    │  81 │ 14    │ 0.5   │  6.2  │ 60  │  1.5  │ 0.65   │
│ JPN     │ 55    │ 105 │ 16    │ 0.7   │  6.7  │ 305 │  0.6  │ 0.95   │
│ NGA     │  6.0  │ 375 │  8    │ 0.6   │  1.6  │  60 │  4.0  │ 0.55   │
│ ETH     │  3.5  │ 210 │  4    │ 0.3   │  1.4  │  35 │  4.2  │ 0.50   │
│ BRA     │ 16    │ 220 │ 18    │ 1.4   │  6.4  │ 130 │  2.8  │ 0.48   │
│ ...                                                                  │
│                                                                      │
│ Sort by: GDP/cap / population / debt / emissions                     │
│ Filter by: country group / horizon-shift winners-losers              │
└─────────────────────────────────────────────────────────────────────┘

┌─ Scenario toggle reveal ───────────────────────────────────────────┐
│  Tap "SSP3" → grid re-renders with SSP3 numbers.                    │
│  Every cell shows Δ vs SSP2 baseline.                               │
│  Color encoding: green = better than baseline, red = worse           │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ PER-COUNTRY DETAIL                                                    ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Selected: India, all SSPs side by side ───────────────────────────┐
│                                                                     │
│ GDP per capita (PPP, k$, 2025-2100):                                │
│   2025  2030  2050  2075  2100                                      │
│ SSP1: 7.5   10    18    32    52     (sustainability rapid catchup) │
│ SSP2: 7.5   9.5   16    27    42     (middle of the road)           │
│ SSP3: 7.5   8.5   12    18    25     (regional rivalry, EM lag)     │
│ SSP4: 7.5   8.5   12    16    20     (inequality persists)          │
│ SSP5: 7.5   10.5  20    38    65     (fossil-fueled boom)           │
│                                                                     │
│ ┌─ GDP/cap line chart, 5 SSPs ─────────────────────────────────┐    │
│ │  Five lines diverging from 2025                              │    │
│ │  Spread at 2050: $8k between SSP1 and SSP4                   │    │
│ │  Spread at 2100: $45k between SSP4 and SSP5                  │    │
│ └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│ Population (M):                                                     │
│ SSP1: 1670 in 2050, peaks 1690 by 2055                              │
│ SSP2: 1670 in 2050, 1530 in 2100                                    │
│ SSP3: 1750 in 2050 (slower transition)                              │
│                                                                     │
│ Emissions (Mt CO2):                                                 │
│ SSP1: peaks ~2030 at 3.0 Gt, declines to 1.0 Gt by 2050             │
│ SSP2: peaks ~2040 at 4.0 Gt, declines to 3.0 Gt by 2050             │
│ SSP3: peaks ~2050 at 5.0 Gt                                          │
│ SSP5: peaks ~2070 at 6.5 Gt                                          │
│                                                                     │
│ Debt-to-GDP (OPENGEM DSA projection per SSP):                       │
│ SSP1: 65% in 2050 (sustainable, low rates support)                  │
│ SSP2: 85% in 2050 (manageable)                                       │
│ SSP3: 130% in 2050 (severe rate pressure + slow growth)              │
│                                                                     │
│ Real interest rate (long-run):                                      │
│ SSP1: 2.0% (high productivity, moderate savings)                    │
│ SSP2: 3.5%                                                           │
│ SSP3: 5.0% (high inflation, scarce capital)                         │
│ SSP5: 3.0% (fossil-fueled growth, abundant capital)                 │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ COMPOUND SCENARIO TOOL                                                ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Build a custom scenario ──────────────────────────────────────────┐
│ Pick sub-assumptions independently and see the composed projection: │
│                                                                      │
│  Population path:        [SSP2 ▼]                                    │
│  Productivity path:       [SSP5 ▼]                                    │
│  Climate / energy path:   [SSP1 ▼]                                    │
│  Debt-policy path:        [SSP2 ▼]                                    │
│  Trade-fragmentation path:[SSP3 ▼]                                    │
│                                                                      │
│  → OPENGEM computes the conditional projection                       │
│                                                                      │
│  Custom-scenario 2050 GDP/cap projections:                           │
│   USA: 92 (vs SSP2 baseline 78, +18%)                                │
│   IND: 18 (vs SSP2 baseline 16, +13%)                                │
│   ...                                                                │
│                                                                      │
│  Saved scenarios get a permalink for sharing.                        │
│  Methodology caveats: independence assumption flagged where weak     │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ SCENARIO RECONCILIATION                                               ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Compare OPENGEM-rebased vs other long-run forecasts ──────────────┐
│ Source              │ World GDP 2050│ China GDP 2050 │ Emissions   │
│ OPENGEM SSP2 (rebased)│ $190T       │ $35T           │ 60 Gt       │
│ IIASA SSP2 raw       │ $185T       │ $34T           │ 62 Gt       │
│ OECD Long-Run        │ $200T       │ $38T           │ 55 Gt       │
│ PwC 2050             │ $215T       │ $44T           │ n/a         │
│ McKinsey MGI         │ $195T       │ $36T           │ n/a         │
│                                                                     │
│ OPENGEM diff vs OECD: -5% world, -8% China                          │
│ Drivers of difference: OPENGEM more conservative on China           │
│   convergence rate post-2030 (demographic drag).                    │
└─────────────────────────────────────────────────────────────────────┘
```

## The compound-scenario tool — the "Bloomberg-killer" feature

The compound-scenario tool is unique. **No other dashboard lets you toggle population from SSP1, productivity from SSP5, climate from SSP3 independently**. Every other long-horizon source forces a coupled SSP. OPENGEM's tool:

1. Lets the user pick each sub-path independently.
2. Computes the composed projection using the OPENGEM long-run macro model.
3. Flags the **independence assumption caveat** wherever sub-paths are not actually independent (e.g., productivity and climate are correlated via R&D and clean-energy substitution; the tool warns).
4. Permits saving + sharing the custom scenario as a URL.

This is the *daily workflow* feature for a long-horizon investor — building a personalized scenario, running sensitivity, and embedding the result in a strategic-asset-allocation memo.

## Visualizations

- **Cross-country grid**: TanStack table with sortable / filterable columns. Color-coded vs SSP2 baseline when off-SSP2.
- **Per-country line chart**: small-multiple grid of 5 SSPs per variable.
- **Compound-scenario "sliders"**: dropdown per sub-path.
- **Sankey diagram** (optional, on-demand): showing emissions decomposition by sector and how decomposition shifts across SSPs.
- **Globe heatmap** (3D): GDP per capita 2050 by country, color-coded; rotatable.

## The vintaging discipline

Long-horizon scenarios are *especially* vulnerable to "moving the goalposts." OPENGEM commits to:

1. **Snapshot every IIASA refresh** with explicit vintage.
2. **Publish a "WHAT CHANGED" log** every time the OPENGEM-rebased SSP shifts.
3. **Never silently overwrite** a long-run number — if 2050 GDP-per-capita-USA was $76k in the 2024 vintage and is $78k in the 2026 vintage, both numbers stay queryable.
4. **Mark the "first published" date** on every projection cell.

This is the *accountability frame* for the page: in 2050, OPENGEM's track record on long-horizon scenarios is the receipt for our credibility.

## Data sources / adapter dependencies

| Input | Source | Adapter | Status |
|---|---|---|---|
| IIASA SSP database | IIASA | `opengem-data-iiasa` ⚠️ NOT YET BUILT | gap |
| UN WPP | UN Population Division | `opengem-data-unpop` ⚠️ NOT YET BUILT | gap |
| OECD Long-Run | OECD ORDRA | `opengem-data-ordra` extension | partial |
| IMF WEO long-run | IMF | `opengem-data-imf` extension | partial |
| IEA STEPS / APS / NZE | IEA World Energy Outlook | `opengem-data-iea-weo` ⚠️ NOT YET BUILT | gap |
| EDGAR emissions | EDGAR | `opengem-data-edgar` ⚠️ NOT YET BUILT | gap |
| NGFS scenarios | NGFS portal | `opengem-data-ngfs` ⚠️ NOT YET BUILT | gap |
| Wittgenstein Centre | Wittgenstein Centre | `opengem-data-witt` ⚠️ NOT YET BUILT | gap |
| OPENGEM DSA forward-projection | own | `opengem-dsa` (new package, see L224) | gap |
| Long-run productivity assumptions | OECD + various | per-source | partial |

**Identified gaps**: IIASA, UN Pop Div, IEA WEO, EDGAR, NGFS, Wittgenstein. This page is the **most upstream-dependent** of any in the batch — it consumes nearly every other long-horizon page's data. It is *deliberately* scoped as a Y2 milestone with a stub at v1 (SSP2 baseline rebased only).

## JSON contract — per-country, per-SSP, per-horizon

```json
{
  "country": "IND",
  "ssp": "ssp2",
  "horizon": 2050,
  "vintage": "2026-06-06",
  "projections": {
    "population_M": 1670,
    "gdp_per_capita_ppp_kusd": 16,
    "gdp_real_trillion_2020usd": 8.4,
    "energy_demand_EJ": 65,
    "emissions_CO2_Gt": 3.8,
    "emissions_per_capita_tCO2": 2.3,
    "debt_to_gdp_pct": 85,
    "real_interest_rate_pct": 3.5,
    "labor_dep_ratio": 0.42,
    "inflation_regime_long_run_pct": 4.5
  },
  "trajectory_by_horizon": {
    "2025": {"gdp_per_capita": 7.5, "population": 1450, "emissions_Gt": 2.8},
    "2030": {"gdp_per_capita": 9.5, "population": 1500, "emissions_Gt": 3.2},
    "2050": {"gdp_per_capita": 16, "population": 1670, "emissions_Gt": 3.8},
    "2075": {"gdp_per_capita": 27, "population": 1620, "emissions_Gt": 3.5},
    "2100": {"gdp_per_capita": 42, "population": 1530, "emissions_Gt": 2.5}
  },
  "delta_vs_ssp1": {"gdp_per_capita": -2, "emissions": +0.6, "population": +0},
  "delta_vs_ssp3": {"gdp_per_capita": +4, "emissions": -1.2, "population": -80},
  "first_published_date": "2024-09-12",
  "cite_this": "https://opengem.org/long-run/ind/ssp2/2050?v=2026-06-06"
}
```

## What this loop produced

- The five-SSP spine + IIASA / UN WPP / IEA WEO / NGFS integration plan.
- A cross-country grid + per-country small-multiple SSP comparison.
- The **compound scenario tool** that lets the user pick population from one SSP, productivity from another — a feature with no public equivalent.
- A vintaging discipline appropriate to long-horizon forecasting (snapshot, change log, never overwrite).
- Six major adapter gaps named.
- A v1 vs v2 scope decision: SSP2 baseline only at v1.

## What comes next

- The page is the *terminal* node for long-horizon work — it consumes L222 (climate-macro), L223 (demography), L224 (DSA).
- Phase 5 prototypes (L231+) start with the L211 + L213 + L218 pages as the highest-leverage v1 candidates.

## Related

- [[L001-vision-statement]]
- [[L222-climate-macro-link]] — SSP integration upstream
- [[L223-demography-long-run]] — population trajectories upstream
- [[L224-sovereign-debt-sustainability]] — DSA layer applied per SSP
- [[L221-energy-commodity]] — energy paths upstream
- [[L146-iconography-system]] — `globe`, `crystal-ball` (sparkles), `target`
