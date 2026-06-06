# L222 — Climate-Macro Link Page

**Loop**: 222 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The thesis of this loop

Climate is the *longest-tailed* macro variable on the dashboard. It is the only indicator where the *physical* path is partly known decades in advance (cumulative CO2, sea-level rise, temperature anomaly) while the *macro* impact is wildly uncertain (NDC compliance, carbon-price evolution, stranded assets, agricultural shock frequency). The data is generally open — IPCC SSPs, IIASA SSP database, NOAA/ECMWF temperature, EM-DAT disaster database, PCAF (Partnership for Carbon Accounting Financials) carbon footprints, NGFS climate scenarios — but **the macro-finance translation layer is nowhere consolidated for non-specialists**. Every CB now publishes "transition risk" reports. Insurance regulators publish stress tests. None of it is *one page*.

OPENGEM's climate-macro page is the page that makes a long-horizon scenario *clickable*. It is the page where Lin (the policy researcher) finds the per-country physical-risk score for her IMF Article-IV commentary; the page where Marcus (the FT journalist) embeds the "implied 2050 carbon-price-path" chart; the page where Damian (the YouTuber) finds a single arresting climate-vs-GDP chart for his year-end recap. It is *not* a climate research page — there are better ones — it is the **macro-link** page, focused on what climate does to GDP, CPI, FX, and sovereign credit on 5y/30y/2050 horizons.

This loop **decides** the SSP integration, the physical risk scoring per country, the transition risk indicators (PCAF + NGFS), and the long-horizon scenario UI.

## The five SSPs as the spine

The IPCC SSPs (Shared Socioeconomic Pathways) are the canonical 2014-defined narrative pathways for 21st-century socioeconomic development:

| SSP | Name | Narrative |
|---|---|---|
| **SSP1** | Sustainability | Low challenges to mitigation + adaptation |
| **SSP2** | Middle of the Road | Median challenges, business-as-usual baseline |
| **SSP3** | Regional Rivalry | High mitigation + adaptation challenges |
| **SSP4** | Inequality | Low mitigation, high adaptation challenges |
| **SSP5** | Fossil-fueled Development | High mitigation, low adaptation challenges |

The IIASA SSP database publishes harmonized macro projections per country for each SSP — population, GDP, energy demand, emissions, food demand — out to 2100. OPENGEM **integrates IIASA SSPs as the canonical long-horizon scenario set** (more on this page in L230, but the spine starts here).

## Page structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ CLIMATE-MACRO LINK                                                   │
│ Physical risk + transition risk + IPCC SSPs.                         │
└──────────────────────────────────────────────────────────────────────┘

[Major view tabs]
 [Country physical risk]  [Country transition risk]  [SSP projections]  [Climate-cost stack]

╔══════════════════════════════════════════════════════════════════════╗
║ COUNTRY PHYSICAL RISK                                                 ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Headline card grid (cross-country, sortable) ─────────────────────┐
│ Country │ Phys Risk│ Heat   │ Flood  │ Cyclone│ Drought│ Score note  │
│         │ score    │ z-score│ z-score│ z-score│ z-score│             │
│ IND     │ 78/100   │ +2.1   │ +1.4   │ +1.5   │ +2.0   │ 🔴 extreme  │
│ BGD     │ 76/100   │ +1.8   │ +2.4   │ +1.9   │ +0.8   │ 🔴 extreme  │
│ PAK     │ 72/100   │ +2.0   │ +1.8   │ +0.6   │ +2.2   │ 🔴 extreme  │
│ EGY     │ 69/100   │ +2.1   │ +0.5   │ +0.0   │ +1.9   │ 🟠 high     │
│ NGA     │ 65/100   │ +1.4   │ +1.0   │ +0.0   │ +1.8   │ 🟠 high     │
│ MEX     │ 58/100   │ +1.1   │ +0.8   │ +1.3   │ +1.5   │ 🟠 high     │
│ USA     │ 42/100   │ +0.8   │ +0.6   │ +1.0   │ +1.2   │ 🟡 moderate │
│ DEU     │ 28/100   │ +0.4   │ +0.6   │ -0.5   │ +0.2   │ 🟢 low      │
│ ...                                                                  │
│ Sort: composite / heat / flood / cyclone / drought                   │
└─────────────────────────────────────────────────────────────────────┘

┌─ World map (choropleth) ───────────────────────────────────────────┐
│  Color: physical risk score, green→red                              │
│  Toggle: total / decomposed by hazard type                          │
└─────────────────────────────────────────────────────────────────────┘

┌─ EM-DAT disaster history (per country) ────────────────────────────┐
│  Stacked-area chart of disaster counts by type, 25y                 │
│  Reveals trend: e.g., PAK floods doubled per decade                 │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ COUNTRY TRANSITION RISK                                               ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Headline grid ────────────────────────────────────────────────────┐
│ Country │ Trans Risk│ Fossil │ Carbon│ NDC      │ Stranded │ Score│
│         │ score     │ % GDP  │ price │ ambition │ assets   │ note │
│ SAU     │ 88/100    │ 38%    │ $0    │ low      │ $0.6T    │ 🔴   │
│ RUS     │ 78/100    │ 22%    │ $0    │ low      │ $0.4T    │ 🔴   │
│ NGA     │ 72/100    │ 9%     │ $0    │ low      │ $0.1T    │ 🟠   │
│ AUS     │ 65/100    │ 11%    │ $35   │ mid      │ $0.2T    │ 🟠   │
│ USA     │ 52/100    │ 6%     │ $0    │ mid      │ $0.6T    │ 🟠   │
│ DEU     │ 38/100    │ 4%     │ €85   │ high     │ $0.05T   │ 🟡   │
│ FRA     │ 35/100    │ 3%     │ €85   │ high     │ $0.04T   │ 🟡   │
│ ...                                                                  │
│ Bottom: countries leading transition (Denmark, Sweden) get a 🟢      │
└─────────────────────────────────────────────────────────────────────┘

┌─ PCAF financed-emissions panel ────────────────────────────────────┐
│  Major banks (per country, top 5) financed-emissions tons / $ lent  │
│  Stranded-asset estimate by sector (oil + gas + coal + utilities)   │
│  Bank disclosure quality score (PCAF score 1-5)                     │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ SSP PROJECTIONS                                                       ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Country GDP projection under each SSP ────────────────────────────┐
│  Five lines (one per SSP), 2025-2100                                 │
│  Reference: IIASA OECD growth model + country-specific climate damage│
│  Spread at 2050: SSP1 +X% / SSP2 baseline / SSP5 -Y%                 │
│  Click a year (e.g., 2050) → opens cross-country GDP-shift table     │
└─────────────────────────────────────────────────────────────────────┘

┌─ Carbon price trajectory by SSP ───────────────────────────────────┐
│  Implied global carbon price, $/tCO2, 2025-2100                      │
│  SSP1: rises to $150 by 2050, $300 by 2100                           │
│  SSP2: rises to $80 by 2050, $130 by 2100                            │
│  SSP3: stays low ($30 by 2050)                                       │
│  Toggle: NGFS scenarios as overlay (Orderly, Disorderly, Hot House)  │
└─────────────────────────────────────────────────────────────────────┘

┌─ Emissions trajectory by SSP ──────────────────────────────────────┐
│  Stacked area: emissions by sector (energy, industry, transport,    │
│   agriculture, land use) for selected SSP                            │
│  Country selector: filter to one country                            │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ CLIMATE-COST STACK                                                    ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Per-country cumulative cost stack 2025-2050 ──────────────────────┐
│  Stacked bar showing for each country:                              │
│   - Physical damage cost ($ of GDP)                                 │
│   - Mitigation investment ($ of GDP)                                │
│   - Adaptation investment ($ of GDP)                                │
│   - Stranded-asset writedowns ($ of GDP)                            │
│                                                                      │
│  Per-SSP comparison: SSP1 highest mitigation, SSP3 highest damage   │
│  Reveals the "no free lunch" — every SSP has cost, different mix    │
└─────────────────────────────────────────────────────────────────────┘
```

## Physical risk methodology

Per-country physical risk score (0-100) is a weighted composite of:

- **Heat exposure** (population-weighted days above 32°C, projected 2030-2050)
- **Flood exposure** (population in 100-year floodplain, projected)
- **Cyclone exposure** (population in projected cyclone tracks)
- **Drought exposure** (agricultural-land-weighted projected drought weeks)
- **Sea-level exposure** (coastal population <10m elevation)
- **Wildfire exposure** (forest-cover-weighted projected fire days)

Weights derived from EM-DAT historical damage-per-population data, validated against IPCC AR6 regional projections. The composite is calibrated such that the *average* high-risk EM country is 70-80, the average DM is 30-40.

## Transition risk methodology

Per-country transition risk score (0-100) is a weighted composite of:

- **Fossil-fuel exposure** (fossil-fuel-related GDP share)
- **Carbon-price gap** (current carbon price vs IPCC 2°C-aligned implied price)
- **NDC ambition** (UNFCCC NDC commitments vs IPCC 2°C trajectory)
- **Stranded-asset exposure** ($ of fossil-fuel reserves valued at 2°C path)
- **Clean-energy share** (renewables share of generation + investment trajectory)
- **Carbon intensity of GDP** (tCO2 / $ of GDP)

## How OPENGEM uses the IIASA SSP database — the integration

The IIASA SSP database is the canonical source for country-level SSP projections. OPENGEM's pipeline:

1. **Ingests** the latest SSP database release (CSV, ~50k rows per scenario × country × year × variable).
2. **Joins** to OPENGEM's own country reference.
3. **Reweights** the country aggregates against OPENGEM's near-term forecasts (2025-2030) so the SSP trajectory starts from a *current* baseline rather than the IIASA 2010-2020 anchor.
4. **Publishes** the harmonized projection as OPENGEM-SSP, with a "rebased: yes" lozenge.
5. **Updates** when IIASA refreshes (~every 2 years) and republishes with vintage.

The page makes the rebasing **fully transparent** — there's a toggle to show "IIASA raw" vs "OPENGEM-rebased" with the divergence explained.

## Data sources / adapter dependencies

| Input | Source | Adapter | Status |
|---|---|---|---|
| IPCC SSPs | IIASA SSP database | `opengem-data-iiasa` ⚠️ NOT YET BUILT | gap |
| EM-DAT disasters | CRED EM-DAT | `opengem-data-emdat` ⚠️ NOT YET BUILT | gap |
| Temperature anomaly | NOAA + Berkeley Earth | `opengem-data-noaa` ⚠️ NOT YET BUILT | gap |
| Flood risk projections | Aqueduct (WRI) | `opengem-data-aqueduct` ⚠️ NOT YET BUILT | gap |
| Carbon prices | EU ETS (ICE), RGGI, CCA, China ETS | `opengem-data-ets` ⚠️ NOT YET BUILT | gap |
| NDC tracker | Climate Action Tracker / UNFCCC | `opengem-data-cat` ⚠️ NOT YET BUILT | gap |
| PCAF financed-emissions | PCAF database + bank disclosures | `opengem-data-pcaf` ⚠️ NOT YET BUILT | gap |
| Fossil-fuel reserves | Carbon Tracker + Rystad (Rystad closed) | `opengem-data-carbontracker` ⚠️ NOT YET BUILT | gap |
| Emissions by country | EDGAR + UNFCCC | `opengem-data-edgar` ⚠️ NOT YET BUILT | gap |
| NGFS scenarios | NGFS Phase IV portal | `opengem-data-ngfs` ⚠️ NOT YET BUILT | gap |

**Identified gaps**: This page is *entirely* gap-blocked. Eight to ten new adapters are required. The climate-macro page is therefore *deliberately scoped as a v2 milestone* — at launch, we publish a stub with SSP2 baseline rebased only, and grow the page as each adapter ships.

## JSON contract — per-country physical risk

```json
{
  "country": "IND",
  "vintage": "2026-06-06",
  "physical_risk": {
    "composite_score": 78,
    "hazard_zscores": {
      "heat": 2.1,
      "flood": 1.4,
      "cyclone": 1.5,
      "drought": 2.0,
      "sea_level": 1.7,
      "wildfire": 0.3
    },
    "label": "extreme",
    "historical_em_dat_disasters_25y": {
      "flood": 64,
      "cyclone": 22,
      "drought": 12,
      "earthquake": 4,
      "wildfire": 0
    }
  },
  "transition_risk": {
    "composite_score": 49,
    "fossil_pct_gdp": 5,
    "current_carbon_price_tco2": 5,
    "ipcc_2c_implied_price_tco2": 80,
    "carbon_price_gap_tco2": 75,
    "ndc_ambition": "mid",
    "stranded_assets_estimate_usd_bn": 80,
    "label": "moderate"
  },
  "ssp_projections": {
    "gdp_2050_pct_change_vs_baseline": {
      "ssp1": +5.0,
      "ssp2": 0.0,
      "ssp3": -8.0,
      "ssp4": -4.0,
      "ssp5": -3.0
    }
  },
  "cite_this": "https://opengem.org/climate/ind?v=2026-06-06"
}
```

## What this loop produced

- The five-SSP spine + IIASA integration + OPENGEM-rebasing strategy.
- A physical-risk score and a transition-risk score per country, with hazard-by-hazard decomposition.
- The "climate-cost stack" view that prices physical + mitigation + adaptation + stranded-asset costs as % of GDP per SSP.
- Ten adapter gaps named — this page is heavy with future work.
- A v1 vs v2 scope decision: only SSP2 rebased ships at v1; the rest grow page-by-page.

## What comes next

- **L230** long-horizon scenario page (the 2030/2050 view that this page feeds).
- **L228** conflict tracker (climate-driven conflict overlay).
- **L221** energy/commodity (carbon prices link).

## Related

- [[L001-vision-statement]]
- [[L230-long-horizon-scenarios]] — primary downstream consumer
- [[L221-energy-commodity]] — carbon prices ↔ ETS data
- [[L223-demography]] — SSP population trajectories feed demography
- [[L228-conflict-tracker]] — climate-driven displacement, conflict triggers
- [[L146-iconography-system]] — `flame`, `globe`, `alert-triangle`
