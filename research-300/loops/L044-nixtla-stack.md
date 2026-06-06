# L044 — Nixtla stack: statsforecast, neuralforecast, hierarchicalforecast, mlforecast for OPENGEM L3 ensemble

**Loop**: 044 / 300
**Phase**: 1 — Open-source landscape survey (Nixtla / modern Python forecasting)
**Date**: 2026-06-06
**OPENGEM adoption grade**: **A for statsforecast + mlforecast + hierarchicalforecast in L3 ensemble; B for neuralforecast as Block II experiment; D for TimeGPT (closed)**

---

## TL;DR

The Nixtla stack is **the modern Python forecasting ecosystem, and it's surprisingly well-suited to OPENGEM's L3 layer**. Four open-source libraries under Apache-2.0, all actively maintained as of mid-2026, all with `.fit() / .predict()` sklearn-compatible APIs, all with strong probabilistic forecasting support:

| Library | What it does | Stars | Last release | OPENGEM use |
|---|---|---|---|---|
| **statsforecast** | Classical models (AutoARIMA, AutoETS, Theta, MSTL, TBATS, GARCH, baselines) | 4.8k | v2.0.3 Oct 2025 | **L3 baselines + ensemble members** |
| **mlforecast** | ML-based forecasting (LightGBM, XGBoost, anything sklearn-compatible) | 1.2k | v1.0.31 Mar 2026 | **L3 ML variant** |
| **neuralforecast** | Deep-learning forecasting (NHITS, NBEATS, TFT, TimesNet, iTransformer, PatchTST, TimeLLM, 30+ models) | 4.1k | v3.1.9 May 2026 | Block II experiment |
| **hierarchicalforecast** | Hierarchical reconciliation (BottomUp, TopDown, MinTrace, ERM) | 744 | v1.5.1 Mar 2026 | **Cross-country / cross-aggregate reconciliation** |

The TimeGPT product (closed-source, API-only) is **out of scope**. We do not depend on it.

The big finding: **statsforecast alone gives us 5–6 high-quality baseline forecasters for our V&V matrix** (AutoARIMA, AutoETS, Theta, RW, Seasonal Naive, MSTL) with 10–20x speedups vs equivalent pmdarima / R-forecast. These are exactly the "bottom-rung" baselines our V&V matrix needs to demonstrate that the L3 DFM / BVAR variants are actually adding value. **Adopt as `opengem-l3-baselines`.**

Pair with `mlforecast` for the ML side (LightGBM forecaster as one ensemble member) and `hierarchicalforecast` for cross-country reconciliation (e.g. when the EU aggregate forecast needs to be coherent with the sum of member-state forecasts).

`neuralforecast` is the more speculative Block II adoption. The 30+ models are real and mostly well-implemented, but deep-learning forecasting in macro is **still not reliably better than DFM / BVAR baselines** for the horizons we care about (1Q–4Q). We treat it as an experiment.

## Why Nixtla matters

Three reasons:

1. **Unified `.fit() / .predict()` API across all four libraries** with the same long-format input (`unique_id`, `ds`, `y`). Switch model classes with one line of code. Critical for our V&V matrix where we want to compare 10+ models side-by-side without 10 different APIs.

2. **Performance**: statsforecast is 20× faster than pmdarima, 1.5× faster than R-forecast. mlforecast and neuralforecast scale to Spark/Ray/Dask. For our Tier-V cross-country backtests across ~130 series × 17 V&V cells × ~10 years vintage history, this matters.

3. **Probabilistic forecasting first-class**: every library supports prediction intervals out of the box. mlforecast adds Conformal Prediction. neuralforecast supports DeepAR + NHITS native quantile output. hierarchicalforecast adds Normality, Bootstrap, PERMBU, Conformal probabilistic methods.

All four are Apache-2.0. All maintained by the Nixtla team plus open community. PyMC Labs's biggest competitor in the Python forecasting space — but PyMC is more on the *Bayesian model authoring* side and Nixtla is more on the *industrial forecasting* side. They complement.

## statsforecast — the L3 baselines

The killer feature: **Auto-anything**. AutoARIMA, AutoETS, AutoCES, AutoTheta — pick the best model for each series automatically using the same heuristics as the R `forecast` package but 20× faster.

For OPENGEM's V&V matrix, the baselines we need are:

- **Random Walk** (the trivial baseline) — `Naive`
- **Seasonal Naive** — `SeasonalNaive`
- **AR(1) / ARIMA(1,1,0)** — `AutoARIMA(max_p=1, max_d=1, max_q=0)`
- **Theta** — `AutoTheta` (the surprise winner of the M3 competition)
- **ETS state-space** — `AutoETS` (Hyndman et al.)
- **MSTL** — multi-seasonal-trend-LOESS (for series with both weekly and annual seasonality)
- **TBATS** — exponential smoothing with multiple seasonalities

These get us 5–7 baseline forecasters for free. The V&V matrix per R08 requires that our L3 DFM beat AR(1) and Random Walk; statsforecast provides those baselines in a standardized way. **A-grade.**

## mlforecast — the ML ensemble member

mlforecast wraps any sklearn-compatible regressor (LightGBM, XGBoost, CatBoost, scikit-learn linear models, Keras with sklearn API) into a time-series forecasting framework with:

- Auto-generated lag features
- Lag transformations (rolling mean, std, etc.)
- Date features (day of week, month, quarter, etc.)
- Static covariates (per-country variables)
- Distributed training via Dask / Ray / Spark
- Conformal prediction intervals

For OPENGEM:

- **One LightGBM ensemble member** as an L3 variant. Built per-series or globally with `unique_id` differentiation.
- Cross-country pooling pattern (per L203) is natural here: train one LightGBM across all Tier-V countries with country as a categorical, get a global pooled model. Then ensemble with single-country variants for the BMA combiner (L189).
- **A-grade** for one ensemble member; not the whole L3 layer.

## hierarchicalforecast — the cross-aggregate reconciliation

The reconciliation problem: if we forecast EU aggregate GDP and each EU member state separately, the sum of member-state forecasts will not equal the aggregate forecast. Hierarchical reconciliation methods reconcile the two so coherence holds.

Methods implemented:

- **BottomUp**: take only the lowest-level forecasts; sum up.
- **TopDown**: take only the top forecast; allocate down via historical proportions.
- **MiddleOut**: choose a middle level; reconcile in both directions.
- **MinTrace**: Wickramasuriya et al.'s MinT — optimal under MSE-minimizing assumption.
- **ERM**: empirical risk minimization.
- **Probabilistic** versions of all the above: Normality, Bootstrap, PERMBU, Conformal.

For OPENGEM:

- **Critical** for the EU aggregate consistency story. Without it, our EU GDP forecast and the sum of our 27-member-state forecasts are inconsistent.
- Useful for **regional aggregates** (G7, G20, BRICS+, ASEAN, EM) where we want internally-consistent narrative.
- Useful for **temporal reconciliation**: quarterly forecasts should sum to annual forecasts; daily nowcasts should aggregate to weekly.

**A-grade.** Adopt as `opengem-l3-reconcile`.

## neuralforecast — the speculative Block II

30+ models including the best-known ones from time-series deep-learning literature:

- **NHITS** (Challu et al. 2023, AAAI). Block-wise neural forecast.
- **NBEATS, NBEATSx** (Oreshkin et al. ICLR 2020). The seminal pure-DL forecasting model.
- **TFT** (Lim et al. 2021). Temporal Fusion Transformer.
- **PatchTST** (Nie et al. 2023). Patch-based transformer.
- **iTransformer** (Liu et al. 2024). Inverted transformer (variates as tokens).
- **TimesNet, BiTCN, TSMixer, DLinear, NLinear, StemGNN**: variants and ablations.
- **DeepAR**: Salinas et al. probabilistic autoregressive.
- **TimeLLM**: LLM-based time series forecasting.

For OPENGEM:

- **Block II experiment**: try NHITS + DeepAR on our Tier-V GDP nowcasting target. Compare to `DynamicFactorMQ` baseline. If it beats by >5% on CRPS, add as an ensemble member. If not, deprioritize.
- The literature has been mixed: most papers showing big DL gains use benchmark datasets that have heavy seasonality and lots of data. Macro time series have weak seasonality (after SA) and short history. The DL advantage often evaporates.
- **B-grade**. Worth a single sprint; don't bet the L3 layer on it.

## TimeGPT — out of scope

The TimeGPT product (Nixtla's commercial offering — pre-trained foundation model for time series, ~100B data points, accessed via paid API) is:

- Closed source (only the SDK is Apache-2.0).
- API-only — requires Nixtla account + paid subscription.
- Trained on data we don't control or audit.

This violates **two** OPENGEM principles: open-source code, and accountable provenance ("every forecast is a named model with a named methodology"). The TimeGPT forecast can be characterized as "a foundation-model black box," which is the opposite of what we promise.

**D-grade**. Cite as a competitor; don't depend.

## License compatibility

All four open-source libraries are Apache-2.0. Drop-in compatible.

## OPENGEM L3 ensemble — the build map

```
                    ┌──────────────── L3 Ensemble ────────────────┐
                    │                                              │
                    │  ┌─────────────────────────────────────┐    │
                    │  │ statsmodels DFM (L032 backbone)     │    │  Core nowcast
                    │  │  - DynamicFactorMQ                  │    │
                    │  └─────────────────────────────────────┘    │
                    │                                              │
                    │  ┌─────────────────────────────────────┐    │
                    │  │ PyMC BVAR / BVAR-SV / hier-BVAR     │    │  Bayesian variants
                    │  └─────────────────────────────────────┘    │
                    │                                              │
                    │  ┌─────────────────────────────────────┐    │
                    │  │ Nixtla statsforecast (baselines)    │    │  Auto-everything baselines
                    │  │  - AutoARIMA, AutoETS, AutoTheta    │    │
                    │  │  - RW, SeasonalNaive, MSTL          │    │
                    │  └─────────────────────────────────────┘    │
                    │                                              │
                    │  ┌─────────────────────────────────────┐    │
                    │  │ Nixtla mlforecast (LightGBM)        │    │  ML variant
                    │  │  - Pooled cross-country             │    │
                    │  └─────────────────────────────────────┘    │
                    │                                              │
                    │  ┌─────────────────────────────────────┐    │
                    │  │ (optional) neuralforecast (NHITS)   │    │  DL variant (Block II)
                    │  └─────────────────────────────────────┘    │
                    │                                              │
                    │  ┌─────────────────────────────────────┐    │
                    │  │ Combiner: BMA over variants         │    │  Output
                    │  │ (PyMC for posterior weights)        │    │
                    │  └─────────────────────────────────────┘    │
                    │                                              │
                    │  ┌─────────────────────────────────────┐    │
                    │  │ Nixtla hierarchicalforecast         │    │  Cross-aggregate reconciliation
                    │  │  - EU aggregate ⇔ member states     │    │
                    │  └─────────────────────────────────────┘    │
                    └──────────────────────────────────────────────┘
                                                  │
                                                  ▼
                                       ┌──────────────────┐
                                       │ V&V scoring      │
                                       │ (forecast_eval   │
                                       │   from BoE L041) │
                                       └──────────────────┘
```

## Risks

1. **API drift across Nixtla majors.** statsforecast 1.x → 2.x had breaking changes. Pin minor versions. Quarterly upgrade cycle.

2. **Cross-library compatibility.** Each Nixtla library has its own version cadence. Pinning all four to compatible versions is a real maintenance task.

3. **statsforecast doesn't ship DFM.** They explicitly say "20× faster than pmdarima" but not "20× faster than statsmodels DFM" because they don't compete on DFM. We still use statsmodels for DFM.

4. **mlforecast LightGBM determinism.** LightGBM with multi-threading is non-deterministic. We need to pin `num_threads=1` for reproducible backtests. Performance hit.

5. **neuralforecast GPU footprint.** Most models train fine on CPU but with significant time penalty. For our scale (~130 series), CPU is OK at Block I. Block III may need GPU.

6. **hierarchicalforecast reconciliation noise.** Reconciliation can hurt forecast accuracy slightly while gaining coherence. We need to A/B test which reconciliation method works for each aggregate level.

## Verdict

**Grade A** for `statsforecast` + `mlforecast` + `hierarchicalforecast`. Adopt as Block I/II core of the L3 layer alongside statsmodels + PyMC.

**Grade B** for `neuralforecast`. Sprint experiment in Block II.

**Grade D** for `TimeGPT`. Cite; don't depend.

## Citations

- statsforecast: https://github.com/Nixtla/statsforecast
- mlforecast: https://github.com/Nixtla/mlforecast
- neuralforecast: https://github.com/Nixtla/neuralforecast
- hierarchicalforecast: https://github.com/Nixtla/hierarchicalforecast
- HierarchicalForecast paper: arXiv:2207.03517
- TimeGPT product: https://www.nixtla.io/
- Nixtla SDK: https://github.com/Nixtla/nixtla (Apache-2.0 SDK; closed-source model)
- Challu et al. (NHITS, AAAI 2023)
- Oreshkin et al. (NBEATS, ICLR 2020)

## Related

- [[L032]] — NY Fed Nowcasting (the spec; we use statsmodels DFM)
- [[L035]] — statsmodels + BVAR ecosystem (the substrate)
- [[L036]] — PyMC (the Bayesian companion)
- [[L045]] — Replication packages
- [[L189]] — BMA combiner over L3 variants
- [[L201]] — Hyperparameter sweep tracking (Hydra + MLflow / W&B OSS alt)
- [[L202]] — Ensemble weighting via stacking
- [[L207]] — Density forecast aggregation rules
- R14 — L3 architecture (where this whole stack lives)
