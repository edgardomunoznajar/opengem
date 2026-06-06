# L224 — Sovereign Debt Sustainability Page

**Loop**: 224 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The thesis of this loop

Debt sustainability is the most *technically* mature of any forecasting framework — the IMF DSA (Debt Sustainability Analysis) has 25 years of methodology, the EU Fiscal Sustainability Report is public, the World Bank LIC DSA is open, Lin's CGD-style independent DSAs are published on GitHub. **Every output is a PDF. None of them are a clickable, queryable, vintaged dashboard.** Lin (the policy researcher) spends a third of her time re-keying IMF Article-IV DSA tables into spreadsheets to run sensitivity.

OPENGEM's debt-sustainability page does what every multilateral does internally: takes debt-to-GDP, primary balance, interest cost, and growth as inputs; runs forward-projection scenarios; reports the implied debt trajectory; and **stress-tests against named shock scenarios**. It is the page that becomes Lin's daily workflow — and the page that an LLM agent queries when asked "is Argentina's debt sustainable under a 200bp rate shock?"

This loop **decides** the page structure, the DSA-style projection engine (open-replication of IMF MAC DSA logic), the stress scenarios, and the comparison vs IMF / market expectations.

## The DSA engine

OPENGEM runs a per-country DSA every quarter (refreshed when IMF Art-IV or WEO data updates):

- **Inputs**: current debt-to-GDP (gross + net), interest cost / GDP, primary balance / GDP, real GDP growth, inflation, FX share of debt, average maturity, refinancing schedule.
- **Mechanics**: standard debt-dynamics identity `Δb = (r-g)/(1+g) · b - pb + sf`, where `b` = debt-to-GDP, `r` = effective interest rate, `g` = nominal GDP growth, `pb` = primary balance, `sf` = stock-flow adjustments (FX revaluation, contingent liabilities).
- **Scenarios**: baseline (IMF WEO assumptions), plus four stress scenarios — interest rate shock, growth shock, FX depreciation shock, primary balance shock — each with a named magnitude.
- **Output**: 5-year debt-to-GDP trajectory with confidence bands derived from forecast uncertainty in r, g, pb.

The engine is open-source code in `opengem-dsa` (new package). Anyone can replicate.

## Page structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ SOVEREIGN DEBT SUSTAINABILITY                                        │
│ DSA-style projection. Stress scenarios. Open replication.            │
└──────────────────────────────────────────────────────────────────────┘

[Selectors]
 [Country: ARG ▼]   [Horizon: 5y / 10y ▼]   [Vintage: latest ▼]

╔══════════════════════════════════════════════════════════════════════╗
║ HEADLINE PANEL                                                        ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Current snapshot ─────────────────────────────────────────────────┐
│ ARGENTINA                                                            │
│ Gross debt / GDP (2025):    96%                                      │
│ Net debt / GDP (2025):      89%                                      │
│ FX-denominated share:       72%                                      │
│ Average maturity:           5.8y                                     │
│ Effective interest rate:    7.2%                                     │
│ Primary balance / GDP:     -2.1% (2025), target 0.5% by 2027         │
│ Real GDP growth (2025):    -0.5%                                     │
│ Implied gross financing need 2026:    22% of GDP                     │
│                                                                       │
│ Sustainability label:      🔴 NOT SUSTAINABLE under baseline         │
│ Key stress sensitivities:  Rate shock (+100bp = +18pp by 2030)        │
│                            FX shock (-30% ARS = +20pp by 2030)        │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ DEBT TRAJECTORY CHART                                                 ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Debt-to-GDP projection (5-10y) ───────────────────────────────────┐
│  Y: 60% ... 180%                                                    │
│  X: 2020 (history) → 2035 (projection)                              │
│  Lines:                                                              │
│    ───── Historical (solid, to today)                               │
│    ─ ─   OPENGEM baseline (projection, dashed)                      │
│    ····  IMF WEO baseline (dotted, for comparison)                  │
│    ▒▒▒▒  P10/P90 confidence band (Monte Carlo over input uncert)    │
│    ▼▼    Debt restructuring events (2001, 2014, 2020 ARG examples)  │
│                                                                      │
│  Stress overlays (toggle):                                          │
│    ─ ─  Rate +100bp shock                                            │
│    ─ ─  Growth -2pp shock                                            │
│    ─ ─  FX -30% shock                                                │
│    ─ ─  Combined adverse shock                                       │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ STRESS SCENARIO PANEL                                                 ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Stress matrix ────────────────────────────────────────────────────┐
│ Scenario          │5y change│Peak yr│Peak DGDP│Refinancing risk     │
│ Baseline (IMF WEO)│+5pp     │ 2027  │ 101%    │ rising              │
│ Rate +100bp       │+13pp    │ 2030  │ 109%    │ severe              │
│ Growth -2pp       │+18pp    │ 2030  │ 114%    │ critical            │
│ FX -30%           │+20pp    │ 2028  │ 116%    │ critical            │
│ PB shock -2pp     │+11pp    │ 2030  │ 107%    │ severe              │
│ Combined adverse  │+45pp    │ 2030  │ 141%    │ insolvent           │
└─────────────────────────────────────────────────────────────────────┘

┌─ Refinancing schedule (next 60 months) ────────────────────────────┐
│  Stacked bar: principal due by quarter, by currency (USD / EUR / ARS)│
│  Annotations: cliff months requiring market access                  │
│  Hover bar → shows specific instrument + holder profile (multilat / │
│  bond / bilateral / domestic)                                        │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ FAN CHART ANALYSIS                                                    ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Monte Carlo fan chart ────────────────────────────────────────────┐
│  Y: debt-to-GDP                                                     │
│  X: t → t+10                                                        │
│  Fan: P5/P25/P50/P75/P95 from 10,000 Monte Carlo paths              │
│  Inputs to MC: stochastic r, g, pb sampled from country-specific    │
│   forecast distributions                                            │
│  Probability of debt-stabilizing path: 18%                          │
│  Probability of explosive path (>120% by 2030): 47%                 │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ CROSS-COUNTRY DSA GRID                                                ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Sortable grid ────────────────────────────────────────────────────┐
│ Country │ D/GDP│ Δ 5y │ DSA flag │ Worst-case stress │ Refin risk  │
│         │ now  │ proj │          │ peak D/GDP         │              │
│ JPN     │ 261% │ +5pp │ 🟢 stable│ 305%              │ low (domestic)│
│ ITA     │ 138% │ +3pp │ 🟡 watch │ 175%              │ moderate     │
│ USA     │ 122% │ +12pp│ 🟡 watch │ 165%              │ moderate     │
│ FRA     │ 113% │ +8pp │ 🟡 watch │ 148%              │ moderate     │
│ ESP     │ 105% │ +0pp │ 🟢 stable│ 138%              │ moderate     │
│ GBR     │ 99%  │ +6pp │ 🟡 watch │ 130%              │ moderate     │
│ ARG     │ 96%  │ +5pp │ 🔴 critical│ 141%            │ critical     │
│ EGY     │ 95%  │ -3pp │ 🔴 critical│ 130%            │ severe       │
│ BRA     │ 88%  │ +12pp│ 🟡 watch │ 121%              │ moderate     │
│ ZAF     │ 75%  │ +8pp │ 🟡 watch │ 105%              │ moderate     │
│ DEU     │ 64%  │ -4pp │ 🟢 stable│ 78%               │ low          │
│ ...                                                                  │
│ Sort by: D/GDP | 5y change | DSA flag | refinancing risk            │
└─────────────────────────────────────────────────────────────────────┘
```

## The IMF-comparison panel

Per country, the page shows OPENGEM's DSA projection alongside the IMF Art-IV / WEO projection — when they diverge, the page **flags the divergence** with a `⚠ disagree with IMF` lozenge. This is *the* feature for Lin: she needs to see "OPENGEM projects ARG debt to peak at 141% under combined adverse; IMF projects 118%. Difference attributable to: OPENGEM assumes 30% FX shock probability is 35%; IMF assumes 20%."

The disagreement is decomposable into:
- Different baseline growth assumption
- Different baseline inflation assumption
- Different effective interest rate assumption
- Different stress scenario probability

Each component contributes a transparent number to the headline disagreement. **This is the page's accountability moment** — it doesn't just publish a DSA, it publishes how it differs from the official DSA.

## The Monte Carlo fan-chart layer

For each country, the DSA engine runs 10,000 Monte Carlo paths sampling stochastically from forecast distributions of growth, real rate, primary balance, and FX. The result is a fan chart with explicit probabilities of (a) debt stabilization, (b) explosive trajectory, (c) hitting predefined distress thresholds. These are *quantified* statements: "47% probability debt exceeds 120% by 2030" — a phrase Lin can paste in a brief and defend.

## Data sources / adapter dependencies

| Input | Source | Adapter | Status |
|---|---|---|---|
| Debt-to-GDP (gross + net) | IMF Fiscal Monitor + WEO | `opengem-data-imf` | partial |
| FX share of debt | IMF WEO + BIS Sovereign Debt | `opengem-data-bis` + `opengem-data-imf` | partial |
| Maturity profile | IIF + national debt offices | `opengem-data-iif` ⚠️ NOT YET BUILT, per-country | gap |
| Effective interest rate | IMF Fiscal Monitor | `opengem-data-imf` | partial |
| Primary balance | IMF Fiscal Monitor | `opengem-data-imf` | partial |
| Real GDP growth | IMF WEO | `opengem-data-imf` | partial |
| FX rate | ECB / FRB | `opengem-data-frb` ✅, `opengem-data-ecb` ⚠️ | partial |
| IMF Article-IV DSAs | IMF Country Reports (PDF) | `opengem-data-imf-art4-extract` ⚠️ NOT YET BUILT | gap |
| EU Fiscal Sustainability Reports | European Commission | `opengem-data-ec-fsr` ⚠️ NOT YET BUILT | gap |
| LIC DSA framework | IMF / World Bank | `opengem-data-imf-lic-dsa` ⚠️ NOT YET BUILT | gap |

**Identified gaps**: IIF for maturity profiles, IMF Article-IV extractor (LLM-assisted PDF extraction), EU FSR, LIC DSA. The IMF Article-IV extractor is the *most leveraged* gap — it unlocks the comparison panel for all 190 IMF members.

## JSON contract — per-country DSA

```json
{
  "country": "ARG",
  "vintage": "2026-06-06",
  "current": {
    "gross_debt_to_gdp_pct": 96,
    "net_debt_to_gdp_pct": 89,
    "fx_share_pct": 72,
    "avg_maturity_y": 5.8,
    "eff_interest_rate_pct": 7.2,
    "primary_balance_pct_gdp": -2.1,
    "real_gdp_growth_pct": -0.5,
    "gross_financing_need_pct_gdp_2026": 22
  },
  "baseline_projection": {
    "horizon_years": 10,
    "debt_to_gdp_path": [96, 99, 101, 100, 99, 97, 96, 95, 94, 93, 92],
    "imf_weo_path_for_comparison": [96, 98, 100, 99, 97, 95, 93, 91, 89, 87, 85]
  },
  "stress_scenarios": {
    "rate_plus_100bp": {"path": [96, 100, 104, 106, 108, 109, 109, 108, 107, 106, 105], "peak_pct": 109, "peak_year": 2030},
    "growth_minus_2pp": {"path": [96, 101, 106, 110, 112, 114, 114, 113, 112, 110, 108], "peak_pct": 114, "peak_year": 2030},
    "fx_minus_30pct": {"path": [96, 116, 116, 115, 113, 111, 109, 107, 105, 103, 101], "peak_pct": 116, "peak_year": 2027},
    "pb_minus_2pp": {"path": [96, 100, 103, 105, 106, 107, 108, 108, 108, 107, 106], "peak_pct": 108, "peak_year": 2031},
    "combined_adverse": {"path": [96, 113, 125, 134, 139, 141, 141, 140, 138, 136, 133], "peak_pct": 141, "peak_year": 2030}
  },
  "monte_carlo": {
    "n_paths": 10000,
    "prob_debt_stabilizing_by_2030": 0.18,
    "prob_exceed_120pct_by_2030": 0.47,
    "p5_p50_p95_at_2030": [88, 109, 145]
  },
  "imf_comparison": {
    "imf_baseline_2030_pct": 95,
    "opengem_baseline_2030_pct": 97,
    "divergence_pct": 2,
    "drivers_of_divergence": [
      {"factor": "growth_assumption", "contribution_pct": +1.2},
      {"factor": "fx_assumption", "contribution_pct": +0.8}
    ]
  },
  "sustainability_label": "not_sustainable_baseline",
  "cite_this": "https://opengem.org/dsa/arg?v=2026-06-06"
}
```

## What this loop produced

- An open-source DSA engine following IMF MAC DSA methodology.
- Four named stress scenarios + a combined-adverse.
- A Monte Carlo fan chart with explicit probability statements.
- A direct comparison panel vs IMF Art-IV / WEO with decomposable divergence drivers.
- Four adapter gaps named (IIF, IMF Art-IV extractor, EC FSR, LIC DSA).

## What comes next

- **L216** sovereign risk (DSA composite feeds the risk score).
- **L212** stress test scenarios (DSA is the country-debt leg of stress tests).
- **L213** recession-prob (debt sustainability is an input).

## Related

- [[L001-vision-statement]]
- [[L216-sovereign-risk]] — DSA feeds sovereign risk composite
- [[L212-stress-test-scenarios]]
- [[L218-trade-balance-capital-flows]] — capital flows finance debt
- [[L211-shock-library]]
- [[L146-iconography-system]] — `landmark`, `gauge`, `alert-triangle`
