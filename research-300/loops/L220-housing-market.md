# L220 — Housing Market Page

**Loop**: 220 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The thesis of this loop

Housing is the *largest* asset class in any developed economy (US residential RE ≈ $50T, more than the entire US stock market). It is the *most cyclical* fundamental driver of recessions (every postwar US recession except 2001 was preceded by housing weakness). It is the *most local* — the national average hides 10x divergence across MSAs and provinces. And the open data is shockingly good but shockingly fragmented: BIS Property Prices (PPS) for ~60 countries with comparable methodology, FHFA + Case-Shiller for the US, ONS for the UK, Eurostat for the EU, BoJ for Japan.

OPENGEM's housing page does for housing what the labor page does for labor — US-deep, cross-country-comparable, with affordability and mortgage-rate joins that *no* free dashboard combines today. Bloomberg's housing page is ugly. Redfin / Zillow are MSA-level only and US-only. The Fed's Z.1 has the household balance sheet but no per-MSA prices. **The opening is wide.**

This loop **decides** the page structure, the affordability index methodology, the mortgage-rate cross-country comparison, and the construction-permits leading indicator.

## The four panels

The page is organized around four panels, each addressing a different macro question:

1. **Prices** — where prices are now, where they came from, regional dispersion.
2. **Affordability** — price-to-income, price-to-rent, mortgage-payment-to-income.
3. **Mortgage rates** — current rates, term structure (15/30y fixed, ARM), spread vs sovereign.
4. **Construction & supply** — permits, starts, completions, months-of-supply, inventory.

Each panel has a **US-deep** mode and a **cross-country** mode.

## Page structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ HOUSING MARKET                                                       │
│ BIS Property Prices + FHFA + Case-Shiller + national equivalents.    │
└──────────────────────────────────────────────────────────────────────┘

[Major view tabs]
 [Prices]  [Affordability]  [Mortgage rates]  [Construction & supply]  [Country drilldown]

[Selectors]
 [Country: ALL ▼]   [Region: National / MSA / Region ▼]   [Real / Nominal ▼]   [Vintage ▼]

╔══════════════════════════════════════════════════════════════════════╗
║ PRICES PANEL                                                          ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Headline cards (cross-country, sortable) ─────────────────────────┐
│ Country │ Real HPI YoY │ Nom HPI YoY │ Δ Real 12m │ Vintage  │ Note │
│ USA     │ +2.1%        │ +5.4%       │ +1.8pp     │ Case-Shil│ ▲    │
│ DEU     │ -2.5%        │ +0.3%       │ -4.2pp     │ Destatis │ ▼    │
│ GBR     │ -0.8%        │ +1.9%       │ -3.1pp     │ ONS      │ ▼    │
│ AUS     │ +5.0%        │ +8.1%       │ +6.4pp     │ ABS      │ ▲▲▲  │
│ CAN     │ +1.2%        │ +4.5%       │ -0.3pp     │ Teranet  │ ─    │
│ FRA     │ -2.1%        │ +0.4%       │ -3.5pp     │ INSEE    │ ▼    │
│ JPN     │ +0.5%        │ +1.7%       │ +0.2pp     │ BoJ      │ ─    │
│ NLD     │ +1.5%        │ +4.5%       │ +0.8pp     │ Eurostat │ ▲    │
│ KOR     │ -3.4%        │ +0.2%       │ -5.1pp     │ KAB      │ ▼▼   │
│ ESP     │ +2.0%        │ +5.5%       │ +1.2pp     │ INE      │ ▲    │
│ ... 50+                                                              │
└─────────────────────────────────────────────────────────────────────┘

┌─ Real HPI time series (10y), multi-country overlay ────────────────┐
│  Y: HPI rebased to 100 at 2015                                       │
│  X: 2015 → 2026                                                      │
│  Multi-line: USA, DEU, GBR, AUS, CAN selected by default             │
│  Toggle: real / nominal                                              │
│  Annotations: Fed/ECB/BoE rate cycles, COVID                         │
└─────────────────────────────────────────────────────────────────────┘

┌─ US MSA-level heatmap ─────────────────────────────────────────────┐
│  Map of US, color = MSA-level Case-Shiller / FHFA YoY                │
│  Hover: MSA tooltip                                                  │
│  Click: opens MSA detail page                                        │
│  Top movers list: largest 12m gainers / losers                       │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ AFFORDABILITY PANEL                                                   ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Affordability index, cross-country ───────────────────────────────┐
│ Country │ P/I ratio │ P/R ratio │ Mortg pay/Inc │ z-vs-long-mean │
│ USA     │ 4.8       │ 22.1      │ 31%           │ +1.8σ           │
│ AUS     │ 8.1       │ 31.4      │ 42%           │ +2.4σ ⚠ extreme │
│ CAN     │ 6.5       │ 29.2      │ 38%           │ +2.0σ           │
│ GBR     │ 5.1       │ 21.0      │ 28%           │ +0.9σ           │
│ DEU     │ 4.4       │ 27.3      │ 25%           │ +0.4σ           │
│ FRA     │ 5.8       │ 26.1      │ 30%           │ +1.1σ           │
│ ESP     │ 4.0       │ 19.5      │ 24%           │ +0.5σ           │
│ JPN     │ 3.4       │ 17.2      │ 18%           │ -0.3σ           │
│ ...                                                                  │
│ Composite affordability z-score (sum of three) →                     │
│   Extreme overvaluation flag at z > +2.0 (AUS, CAN)                  │
└─────────────────────────────────────────────────────────────────────┘

┌─ US MSA affordability scatter ─────────────────────────────────────┐
│  X = median home price, Y = median mortgage-payment as % of income   │
│  Each dot = one MSA                                                  │
│  San Francisco, San Jose, Honolulu in upper-right (extreme)          │
│  Detroit, Pittsburgh, Cleveland in lower-left (affordable)           │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ MORTGAGE RATES PANEL                                                  ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Current mortgage rates, cross-country ────────────────────────────┐
│ Country │ 30y fix│ 15y fix │ 5/1 ARM │ Spread vs sovereign │ Trend  │
│ USA     │ 6.85%  │ 6.20%   │ 6.15%   │ +260bp vs UST10     │ ▼ -25bp│
│ GBR     │ 4.75%  │ 4.40%   │ 4.10%   │ +85bp vs Gilt10     │ ▼ -15bp│
│ DEU     │ 3.85%  │ 3.55%   │ 3.40%   │ +135bp vs Bund10    │ ─      │
│ FRA     │ 4.10%  │ 3.80%   │ 3.65%   │ +115bp vs OAT10     │ ─      │
│ NLD     │ 4.05%  │ 3.75%   │ 3.60%   │ +130bp vs DSL10     │ ▼ -5bp │
│ AUS     │ 6.50%  │ N/A     │ 6.20%   │ +245bp vs ACG10     │ ▼      │
│ CAN     │ N/A    │ N/A     │ 5.75%   │ (5y reset standard) │ ▼      │
│ JPN     │ 1.65%  │ N/A     │ 0.85%   │ +50bp vs JGB10      │ ▲ +10bp│
│ KOR     │ 4.80%  │ N/A     │ 4.55%   │ +220bp vs KTB10     │ ▼      │
│ ...                                                                  │
│ Note: typical national fixed-term differs (US=30y, CAN=5y, NLD=10y) │
└─────────────────────────────────────────────────────────────────────┘

┌─ US mortgage spread vs UST10 time series (15y) ────────────────────┐
│  Reveals 2008/2020 stress periods (spread blowout) vs normal (~160bp)│
│  Current: +260bp — well above the 2010-2019 average                  │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ CONSTRUCTION & SUPPLY PANEL                                           ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ US monthly construction stats ────────────────────────────────────┐
│  Permits         starts        completions       under construction │
│  1.42M (SAAR)    1.36M         1.51M             1.65M               │
│  Δ 12m: -3.2%   -1.8%         +2.1%             -0.5%               │
│                                                                      │
│  Months of supply (existing): 4.1 (balanced threshold 6)             │
│  Months of supply (new): 8.3 (oversupplied)                          │
│  Inventory: 1.3M existing + 0.45M new                                │
└─────────────────────────────────────────────────────────────────────┘

┌─ Permits as leading indicator (12m-ahead correlation) ─────────────┐
│  Scatterplot: permits-12m-ago vs starts-now (high correlation 0.78) │
│  Permits is the leading edge: 12m before starts, 18-24m before HPI  │
│  Current implied: permits slowdown → starts slowdown → HPI deceler  │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ COUNTRY DRILLDOWN VIEW                                                ║
╚══════════════════════════════════════════════════════════════════════╝

  Per-country: full price + affordability + mortgage + supply view.
  US adds MSA-level detail.
  EU adds Eurostat region-level (NUTS-2) detail.
  GBR adds local-authority detail (ONS).
```

## Affordability methodology

The composite affordability z-score is computed per country:

```
z_affordability = z(price_to_income) + z(price_to_rent) + z(mortgage_payment_to_income)
```

normalized against the country's own 20-year history. The threshold convention:

- `z > +2.0` → "extreme overvaluation" (flagged with `alert-triangle`)
- `z > +1.0` → "stretched" lozenge
- `-0.5 ≤ z ≤ +0.5` → "balanced"
- `z < -1.0` → "undervalued / depressed" (lozenge)

These thresholds are *not* one-size-fits-all — Australia, where structural undersupply has kept affordability elevated for decades, gets a country-specific historical anchor. The methodology pop-up explains.

## The leading-indicator insight

Construction permits lead starts by ~12 months and lead house price changes by 18-24 months. The page surfaces this *as a feature*: a small panel says "US permits implied -1.5pp HPI YoY in 18 months" based on the rolling-regression of permits → HPI. **This is a forecast, not a description**, and it's vintaged like every other OPENGEM forecast.

## Data sources / adapter dependencies

| Input | Source | Adapter | Status |
|---|---|---|---|
| BIS Property Prices (60 countries) | BIS Statistical Warehouse | `opengem-data-bis` ⚠️ NOT YET BUILT | gap |
| US FHFA HPI | FHFA API | `opengem-data-fhfa` ⚠️ NOT YET BUILT | gap |
| US Case-Shiller | S&P Dow Jones (via FRED) | `opengem-data-frb` extension | partial |
| US MSA prices | FHFA + Case-Shiller MSA | `opengem-data-fhfa` | gap |
| US permits/starts/completions | Census Bureau (M3) | `opengem-data-census` ✅ | ready |
| US existing-home sales / inventory | NAR | `opengem-data-nar` ⚠️ NOT YET BUILT | gap |
| US new-home sales | Census | `opengem-data-census` | ready |
| US 30y mortgage rate | Freddie Mac PMMS | `opengem-data-freddie` ⚠️ NOT YET BUILT | gap |
| UK ONS | ONS API | `opengem-data-ons` ⚠️ NOT YET BUILT | gap |
| EU Eurostat HPI | Eurostat | `opengem-data-eurostat` ⚠️ NOT YET BUILT | gap |
| Japan BoJ HPI | BoJ | `opengem-data-boj` ⚠️ NOT YET BUILT | gap |
| Mortgage rates (cross-country) | ECB MIR + BoE Bankstats + various | mixed | gap |
| Affordability inputs (income, rent) | OECD ORDRA + national stats | `opengem-data-ordra` ✅ + others | partial |

**Identified gaps**: BIS, FHFA, NAR, Freddie Mac, ONS, Eurostat, BoJ adapters. The housing page is data-heavy and has the *most* adapter gaps of any page in this batch.

## JSON contract — country headline

```json
{
  "country": "USA",
  "vintage": "2026-06-06",
  "headline": {
    "real_hpi_yoy_pct": 2.1,
    "nominal_hpi_yoy_pct": 5.4,
    "delta_12m_pp": +1.8,
    "source_series": "case-shiller-national"
  },
  "affordability": {
    "price_to_income_ratio": 4.8,
    "price_to_rent_ratio": 22.1,
    "mortgage_payment_to_income_pct": 31,
    "composite_z_score": +1.8,
    "label": "stretched"
  },
  "mortgage_rates": {
    "rate_30y_fixed_pct": 6.85,
    "rate_15y_fixed_pct": 6.20,
    "spread_vs_ust10_bp": 260,
    "30d_change_bp": -25
  },
  "supply": {
    "permits_thousands_saar": 1420,
    "starts_thousands_saar": 1360,
    "months_of_supply_existing": 4.1,
    "months_of_supply_new": 8.3
  },
  "leading_indicator_forecast": {
    "implied_hpi_yoy_in_18m_pct": +0.6,
    "method": "rolling regression of permits → HPI"
  },
  "cite_this": "https://opengem.org/housing/usa?v=2026-06-06"
}
```

## What this loop produced

- The four-panel structure: prices + affordability + mortgage rates + construction.
- US MSA-level depth + cross-country comparability via BIS PPS.
- A defined affordability composite z-score with named thresholds.
- A construction-as-leading-indicator forecast panel.
- Ten+ adapter gaps named — the largest of any single page.

## What comes next

- **L222** climate-macro page (physical risk affects regional housing).
- **L211** shock library (housing-shock IRFs).
- **L213** recession-prob (housing as input).

## Related

- [[L001-vision-statement]]
- [[L215-financial-conditions-index]] — RE-price z-score is an FCI input
- [[L213-recession-probability]] — housing leads recessions
- [[L219-labor-market]] — parallel structure (US-deep + cross-country)
- [[L146-iconography-system]] — `home`, `landmark`, `alert-triangle`
