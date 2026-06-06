# L041 — Bank of England Bayesian VAR toolkits + BoE staff working papers with code

**Loop**: 041 / 300
**Phase**: 1 — Open-source landscape survey (BoE + adjacent)
**Date**: 2026-06-06
**OPENGEM adoption grade**: **A for `forecast_evaluation` MIT-licensed Python lib, B for CCBS Applied Bayesian Econometrics handbook code, C for everything else**

---

## TL;DR

The Bank of England's open-source posture is **uneven but more useful than people realize**. Two specific things stand out:

1. **`bank-of-england/forecast_evaluation`** (MIT, v0.1.9 June 2026, 25 stars). A Python package implementing every forecast-evaluation test we need for the V&V matrix: Diebold-Mariano, Mincer-Zarnowitz, revision predictability (weak efficiency), Blanchard-Leigh strong efficiency, rolling fluctuation tests, RMSE/MAE/MedAE, density forecasts via PIT, hedgehog plots, radar plots, and an **interactive dashboard for exploration**. **This is a literal A-grade adoption** — we don't need to build any of it ourselves.

2. **CCBS "Applied Bayesian Econometrics for Central Bankers" handbook by Andrew Blake and Haroon Mumtaz (2017 update)** — book + MATLAB code zip. **The most-pedagogical, most-well-tested BVAR/TVP-VAR/DFM teaching codebase in central banking.** Mumtaz also maintains his own code page (`sites.google.com/site/hmumtaz77/code`) with extensions. The MATLAB → Python translation is straightforward; many of these models are now in PyMC or statsmodels but the *spec* is in the handbook.

The headline BoE models (COMPASS, MAPS, EASE, the Suite of Models) are **not open**. They were the operational central-organising model from 2011–onward (COMPASS replaced BEQM in 2011, MAPS is the modeling toolkit, EASE is the UI for forecast production). Working Paper 471 (2013) describes them in detail; the code is internal. We will not get COMPASS as a deliverable.

Other small BoE open repos (`MachineLearningCrisisPrediction`, `Shapley_regressions`, `InterpretableMLWorkflow`, `occupationcoder`, `boeCharts`, `FanChartsInR`, `ledgerrecogniser`) are niche. We cherry-pick where useful.

**The biggest finding from this loop**: `bank-of-england/forecast_evaluation` is the missing piece for OPENGEM's V&V matrix machinery. We adopt it directly.

## forecast_evaluation in detail

| Field | Value |
|---|---|
| Repo | https://github.com/bank-of-england/forecast_evaluation |
| License | MIT |
| Language | Python |
| Latest release | v0.1.9 (June 4, 2026) |
| Stars | 25 |
| Author | BoE forecasting team |

What it implements:

**Statistical tests**:
- Diebold-Mariano (point-forecast accuracy comparison)
- Mincer-Zarnowitz (bias / efficiency regression on outcome)
- Revision predictability (weak-form efficiency)
- Blanchard-Leigh (strong efficiency, multivariate)
- Correlation tests between revisions and forecast errors
- Rolling-window fluctuation tests (Giacomini-Rossi)

**Accuracy metrics**:
- RMSE, MAE, MedAE
- For density forecasts: PIT, log-score, CRPS

**Visualization**:
- Hedgehog plots (forecast paths vs realizations across vintages)
- Outturn revisions
- Forecast error distributions
- Radar plots
- Vintage accuracy plots
- Rolling accuracy plots

**Data objects**:
- `ForecastData` for point forecasts
- `DensityForecastData` for distribution forecasts

**Interactive dashboard** for exploration.

For OPENGEM, this is **everything our V&V matrix needs at the operational level**. Per R08, the 17-cell V&V matrix uses CRPS, PIT, MAE, RMSE, and DM tests across our forecast variants. `forecast_evaluation` ships all of these in a tested, documented, MIT-licensed Python package, written by the BoE forecasting team for exactly this use case.

**Action**: pin as a dependency of `opengem-vv` (our V&V matrix package). Use the visualization layer for the dashboard's "track-record" page (L134, L259). Use the interactive dashboard internally for our weekly forecast review.

## CCBS Applied Bayesian Econometrics handbook

Andrew Blake (BoE) and Haroon Mumtaz (Queen Mary, formerly BoE) wrote the canonical pedagogical handbook on applied Bayesian econometrics for central bankers. Published by the Centre for Central Banking Studies (CCBS), updated 2017. Free PDF on the BoE website.

What's in it:

- **Chapter 1**: Bayesian basics + Gibbs sampling for linear regression.
- **Chapter 2**: Bayesian VARs (Minnesota, NIW, SSVS priors).
- **Chapter 3**: Time-varying parameter VARs (Cogley-Sargent style).
- **Chapter 4**: Dynamic factor models.
- **Chapter 5**: Time-varying DFM.
- **Chapter 6**: Stochastic volatility.
- **Chapter 7**: Mixed-frequency.

All chapters come with **MATLAB code in a chapter-organized zip**. Mumtaz maintains additional code at `sites.google.com/site/hmumtaz77/code` with extensions and updates beyond the published handbook.

For OPENGEM:

- The handbook is the **best reading list** for understanding the BVAR / TVP-VAR / DFM family in operational central-banking terms.
- The MATLAB code is a **spec**, not an implementation we adopt. Many of these models are now in PyMC (BVAR, TVP-VAR, stoch-vol), statsmodels (DFM), or BGVAR (panel BVAR).
- For any new model in our L3 layer, the handbook chapter is the first stop: "what does the operational central-banking literature say about this?"

**Action**: Make the handbook a required reading item for the project. Translate one BVAR Mumtaz example to PyMC as a Block II exercise (proves we understand the math).

## BoE's other repos

| Repo | What it is | OPENGEM use |
|---|---|---|
| `MachineLearningCrisisPrediction` | Crisis prediction with ML | Could complement Bauer-Mertens recession-prob; pull patterns |
| `Shapley_regressions` | Stat inference on ML / non-parametric models | Useful for explaining ML forecast contributions |
| `InterpretableMLWorkflow` | Generic IML workflow | Reference for model-card construction |
| `occupationcoder` | Occupation code assignment for job titles | Out of scope |
| `boeCharts` | ggplot2 chart themes | Reference for our chart styling; not Python-relevant |
| `FanChartsInR` | Fan chart drawing in R | Reference for our fan-chart UX (L208) |
| `ledgerrecogniser` | OCR for historical ledger data | Out of scope |

The MachineLearningCrisisPrediction repo is worth a deeper look — it ships Python code for the ML-based crisis-prediction work from BoE working papers, and is a candidate complement to our Bauer-Mertens probit recession-probability tile.

## The MAPS / COMPASS / EASE situation

Bank of England Working Paper 471 (Burgess, Fernández Corugedo, Groth, Harrison, Monti, Theodoridis, Waldron, 2013) describes the forecasting platform:

- **COMPASS**: structural central-organising model. Smets-Wouters lineage. Replaced BEQM in 2011.
- **Suite of Models**: parallel forecasts that "fill the gaps" — BVARs, DSGEs, ML.
- **MAPS**: macroeconomic modeling toolkit (MATLAB).
- **EASE**: forecast production UI.

**None of these are open.** The 2013 working paper is the most we get. As of 2026, BoE has been quietly piloting new structural modeling work (post-Bernanke-Reinhart "Macroeconomy at the Crossroads" review), some of which may surface as new staff working papers.

**Pattern matching**: BoE is more open than the ECB and IMF on *evaluation* (forecast_evaluation, working papers with code), less open than NY Fed on *forecasting models themselves*. We work with what's there.

## Staff Working Paper 756 (2018) — Bayesian VARs

Bank of England Staff Working Paper 756 "Bayesian vector autoregressions" reviews BVAR methodology for central bankers. Companion to the Mumtaz handbook. **No code in the WP itself**, but it's the right place to read for "what does a BoE-style operational BVAR look like." Useful reading list, not adoption.

## License compatibility

- `forecast_evaluation`: MIT — drop-in compatible with Apache-2.0.
- CCBS handbook code: implicit academic licensing. We don't redistribute; we reference. The patterns are public.
- BoE individual repos: MIT or Apache-2.0 per repo. No blockers.

## Risks

1. **`forecast_evaluation` is small** (25 stars, BoE-internal use). The maintainer activity is good (release in June 2026) but the bus-factor is one team. Mitigation: vendor a snapshot; track upstream; contribute back.

2. **CCBS code is MATLAB**. Translation effort if we want to vendor anything. Mitigation: don't vendor; use the math, write our own in PyMC.

3. **BoE could deprecate `forecast_evaluation`**. Same as any small open repo. Mitigation: maintain our own fork if it stalls.

4. **Mumtaz site stability**. Google Sites pages are not the most stable hosting. Mitigation: download a snapshot of the code we care about.

## Verdict

**Grade A**: `bank-of-england/forecast_evaluation`. Adopt directly into `opengem-vv` package. This is the surprise win of the loop — a piece of operational central-bank Python that we don't have to write.

**Grade B**: CCBS handbook (Blake & Mumtaz 2017) + Mumtaz example code. Required reading + pattern source. Translate one example as a Block II exercise.

**Grade C**: `MachineLearningCrisisPrediction`. Cherry-pick for the recession-probability tile if a Block II pattern surfaces.

**Grade D**: Everything else (COMPASS, MAPS, EASE — closed; small repos — niche).

## Citations

- `bank-of-england/forecast_evaluation`: https://github.com/bank-of-england/forecast_evaluation
- Blake, A. & Mumtaz, H. "Applied Bayesian Econometrics for Central Bankers." CCBS Handbook 4 (updated 2017). https://www.bankofengland.co.uk/ccbs/applied-bayesian-econometrics-for-central-bankers-updated-2017
- Mumtaz code page: https://sites.google.com/site/hmumtaz77/code
- Bank of England Staff Working Paper 756 (2018): "Bayesian vector autoregressions." https://www.bankofengland.co.uk/working-paper/2018/bayesian-vector-autoregressions
- Bank of England Working Paper 471 (2013): "The Bank of England's forecasting platform: COMPASS, MAPS, EASE and the suite of models." https://www.bankofengland.co.uk/working-paper/2013/the-boes-forecasting-platform-compass-maps-ease-and-the-suite-of-models
- BoE GitHub org: https://github.com/bank-of-england

## Related

- [[L032]] — NY Fed Nowcasting (parallel A-grade adoption)
- [[L034]] — Dynare + IRIS (COMPASS lineage)
- [[L035]] — statsmodels BVAR ecosystem
- [[L036]] — PyMC for translating Mumtaz examples
- [[L038]] — BGVAR (BoE-adjacent Vienna ecosystem)
- [[L134]] — Track-record page (uses `forecast_evaluation` viz)
- [[L185]] — Open backtest harness API
- [[L259]] — Track-record open ledger page
- R08 — V&V matrix detail (where `forecast_evaluation` plugs in)
