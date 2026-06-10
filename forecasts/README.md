# OPENGEM public forecast track record

This directory is the project's **public, dated, ex-ante forecast record**.
Each file is named `YYYY-MM-DD-<scope>.json` where the date is the day the
forecast was generated and committed. The git history of this public
repository is the timestamp: a forecast counts only if its commit predates
the official data release it forecasts.

## The rules (fixed in advance)

1. **Ex ante or it doesn't count.** Every forecast is committed before the
   first official release of the value it predicts. Forecasts are never
   edited after commit; corrections go in a new dated file.
2. **Density, not points.** Forecasts publish p10/p50/p90 (and the full
   parametric density in the JSON), so they can be scored by CRPS and PIT,
   not just absolute error.
3. **Scored against named baselines.** Every model forecast is accompanied
   by AR(1) and random-walk baselines fitted on the same panel. The bar is
   the V&V matrix in `docs/research/R08-vv-matrix-detail.md`; the headline
   IOC cell is *GDP-1Q: beat AR(1) and RW by mean CRPS*.
4. **Resolution.** When the official estimate is released, the outcome and
   scores are committed alongside the forecast (`*-resolved.json`), using
   the first official release (advance estimate) and, separately, the
   latest vintage — both are reported.
5. **Misses stay up.** The record is append-only. Losing cells are reported
   with the same prominence as winning ones.

## Record

| Forecast date | Scope | Target | Scoring period | p50 | [p10, p90] | Resolves on (approx.) | Outcome |
|---|---|---|---|---|---|---|---|
| 2026-06-06 | US | GDP yoy | 2026Q2 | **2.67%** | [0.87, 4.47] | ~2026-07-30 (BEA advance) | pending |
| 2026-06-06 | US | CPI yoy | 2026Q2 | **2.74%** | [1.80, 3.69] | ~2026-07-14 (BLS June CPI) | pending |
| 2026-06-06 | US | GDP yoy | 2027Q1 | 2.86% | [0.23, 5.49] | ~2027-04-29 | pending |
| 2026-06-06 | US | CPI yoy | 2027Q1 | 2.86% | [1.07, 4.64] | ~2027-04-13 | pending |

## How these were produced

Model: `opengem-l3-dfm` (statsmodels `DynamicFactorMQ`) fit on a real
261-quarter US panel (1960Q2–2026Q1), curated by `opengem-panel`, scored by
`opengem-backtest`. Reproduction: `scripts/first_us_forecast.py` (requires a
FRED API key for the data pull; raw data is not redistributed here).

Backtest at publication (rolling-origin, 24 origins, latest-vintage
actuals — see the single-vintage caveat in `STATE-OF-REALITY.md`):

| GDP yoy 1Q | mean CRPS | median CRPS | MAE |
|---|---|---|---|
| **OPENGEM L3 DFM** | **1.380** | **0.398** | **1.716** |
| AR(1) | 1.553 | 0.405 | 1.743 |
| Random walk | 1.717 | 0.428 | 1.918 |

Honest mix elsewhere: AR(1) wins CPI-1Q mean CRPS; the DFM wins CPI-4Q and
the GDP-4Q median. Full numbers in each forecast's JSON.
