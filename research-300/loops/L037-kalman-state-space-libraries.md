# L037 — Kalman/state-space libs: pyflux, sktime, statsmodels.tsa.statespace, KalmanNet

**Loop**: 037 / 300
**Phase**: 1 — Open-source landscape survey (state-space)
**Date**: 2026-06-06
**OPENGEM adoption grade**: **A for statsmodels.tsa.statespace**, everything else C or D

---

## TL;DR

`statsmodels.tsa.statespace` is the answer. Use it. Move on.

The four options under review:

1. **PyFlux** — Abandoned since 2017. Single maintainer (RJT1990) explicitly recognized statsmodels was eating its lunch. **Do not adopt.**
2. **sktime** — General-purpose time-series ML framework, BSD-3. Solid for the *meta* layer (ensemble, cross-validation, scoring) but **does not provide its own state-space backbone** — it wraps statsmodels for that. Useful as an ensemble combiner companion (L189). Not the Kalman library itself.
3. **statsmodels.tsa.statespace** — The pick. BSD-3. Cython Kalman filter. `DynamicFactorMQ` is NY Fed Nowcasting class (L032). `MLEModel` lets us subclass for arbitrary state-space models (MIDAS, factor-augmented, TVP). Chad Fulton maintains. **Production.**
4. **KalmanNet** — A neural-net-aided Kalman filter from Weizmann (Shlezinger lab). Cool research. **Not for OPENGEM.** Solves a problem (partially-known dynamics) that we don't have at our scope. Our state-space matrices come from named macro models, not from black-box dynamics. Wait for it to be a default in a major framework before we touch.

The expanded list of state-space + nowcast Python tools worth knowing about:

- `tinygp` — Gaussian processes; not state-space per se but adjacent.
- `dynamax` — JAX-based state-space and HMM. Active. Worth watching.
- `filterpy` — Roger Labbe's textbook companion. Pedagogical, not production.
- `simdkalman` — fast batched Kalman filter for many independent series. Niche.

But **none of these dethrone statsmodels for our use case**, which is: deep filtering with macroeconomic interpretation, mixed-frequency mixed-data, custom transition matrices, EM estimation.

## statsmodels.tsa.statespace in detail

The crown jewel of the Python time-series world. Lead author: Chad Fulton (NY Fed, also lead author of `DynamicFactorMQ`). Built on a Cython-compiled Kalman filter with a Python `MLEModel` interface for subclassing.

What it provides out of the box:

| Class | What it is | OPENGEM relevance |
|---|---|---|
| `MLEModel` | Generic state-space superclass | Backbone for custom models |
| `SARIMAX` | Seasonal ARIMA with exogenous | Baselines, V&V grid |
| `DynamicFactor` | Classic Stock-Watson DFM | Backup for `DynamicFactorMQ` |
| `DynamicFactorMQ` | Bok et al. NY Fed Nowcasting | **L3 workhorse** (L032) |
| `UnobservedComponents` | Local level / linear trend / cycle | Trend extraction, gap analysis |
| `VARMAX` | Vector ARMA with exogenous in state-space form | VAR with mixed-frequency exogenous |
| `RegressionResults` with `MLEModel` | Time-varying-parameter regression | TVP nowcast experiments |
| `KalmanFilter` | Low-level filter for custom dynamics | Custom adapters |

What it does well:

- **Missing-data handling**: Kalman filter handles missing observations naturally. Mixed-frequency works without preprocessing.
- **Custom models**: subclass `MLEModel`, define `__init__`, `update`, `transform_params`. The Fulton blog has the canonical walkthrough.
- **Diagnostics**: standardized residuals, Q-Q plots, ACF tests, Ljung-Box, Jarque-Bera — all built-in.
- **Speed**: Cython filter is fast enough for our daily-cadence-on-100-countries workload. Optional `simulation_smoother` for Bayesian variants.
- **Documentation**: among the best in the Python statistics world. Fulton's notebooks at chadfulton.com are gold.

What it does not do:

- Bayesian estimation (use PyMC, L036).
- Particle filters (use a niche package or hand-roll on top of `KalmanFilter`).
- Neural state-space (out of scope — use Nixtla, L044, for that).
- Stochastic-volatility filtering (gap; PyMC or Stan).

## PyFlux — why we skip

PyFlux (RJT1990, ~2 stars/year decay) was a 2017 attempt at unifying state-space, GAS, VAR, and ARIMA into one API. The maintainer is gone. Issue #3 ("statsmodels statespace models") was the founder essentially conceding that statsmodels covered the space better. Documentation lives at pyflux.readthedocs.io still, but the package will not install cleanly on modern Python (3.12+) due to dropped Cython compatibility and numpy ABI changes.

Verdict: **Do not depend on PyFlux. Do not vendor. Do not even read for inspiration — most of the patterns are now in statsmodels.**

## sktime — the meta layer, not the substrate

sktime is BSD-3, 9.8k stars, last release November 2025. It's the "scikit-learn of time series": unified API for forecasting / classification / regression / clustering / anomaly detection, with adapters to ~30+ underlying libraries (including statsmodels, Prophet, ARCH, Nixtla, XGBoost-as-forecaster, etc.).

For OPENGEM:

- **Useful as the ensemble combiner** (`EnsembleForecaster`, `StackingForecaster`, `MultiplexForecaster`). When we have multiple L3 variants (DFM, BVAR, ML), sktime's `temporal_train_test_split` + `evaluate` give us a CV harness with PIT, CRPS, MAE — directly mapped to our V&V matrix (R08).
- **Useful for backtesting**: `SlidingWindowSplitter`, `ExpandingWindowSplitter` match exactly what we want for vintage-correct backtests.
- **NOT useful as a state-space backend**: sktime defers to statsmodels for state-space. Don't add it as a dependency of `opengem-l3-dfm`; only of `opengem-l3-combiner`.

**Recommendation**: adopt sktime as a Block II dependency for the combiner / V&V harness, not as a primary state-space backend.

## KalmanNet — the research frontier

Paper: "KalmanNet: Neural Network Aided Kalman Filtering for Partially Known Dynamics" (Revach et al., 2022, IEEE TSP). Extension: "Recursive KalmanNet" (2025 EUSIPCO).

What it does: trains a small RNN inside the Kalman filter to learn the bits of the dynamics that you don't have a model for. Useful for: signal-processing problems where the physical model is roughly known but has un-modeled nonlinearities.

What it does for macroeconomic forecasting: **not much, yet**. Macro doesn't have "partially known dynamics" in the sense KalmanNet means. We have *fully unknown* dynamics that we *approximate* via VARs or DFMs. The "model mismatch" KalmanNet learns to fix is not the kind of mismatch we have.

Could it be useful eventually? Maybe as a way to learn structural-break corrections inside a DFM. But that's a research project, not a Block I or II adoption.

**Verdict**: D-grade. Cite the paper for completeness, don't depend, watch the literature.

## Other tools

### dynamax (JAX-based, watch this)

A JAX-native state-space and HMM library from Probabilistic Machine Learning Group (UW Madison + others). Apache-2.0. Implements Kalman filters, HMMs, SLDS, switching state-space models — in pure JAX, so GPU-friendly.

For OPENGEM: interesting for the longer-term JAX-everywhere story (cf. L036's NumPyro pick). Not adopting in Block I or II because we don't yet need GPU state-space. Watch for stability and maturity.

### filterpy

Roger Labbe's pedagogical companion to the "Kalman and Bayesian Filters in Python" book. Excellent for *learning*. Not production.

### simdkalman

Batched Kalman filter for thousands of independent univariate series. Niche but useful if we ever do per-country independent state-space modeling at scale.

## Companion choice in the L3 stack

```
                ┌─────────────────────────────────────────┐
                │  statsmodels.tsa.statespace             │ ← state-space core
                │  - DynamicFactorMQ (NY Fed Nowcast)    │
                │  - MLEModel custom (TVP, FAVAR, MIDAS) │
                │  - SARIMAX, UnobservedComponents       │
                └────────────────┬────────────────────────┘
                                 │
                                 ▼
                ┌─────────────────────────────────────────┐
                │  PyMC                                   │ ← Bayesian extensions
                │  - BVAR, BVAR-SV, hierarchical          │
                └────────────────┬────────────────────────┘
                                 │
                                 ▼
                ┌─────────────────────────────────────────┐
                │  sktime                                 │ ← meta-layer
                │  - EnsembleForecaster                   │
                │  - V&V matrix scoring                   │
                │  - CV harness                           │
                └─────────────────────────────────────────┘
```

## License audit

All three components are BSD-3 or Apache-2.0, drop-in compatible with our Apache-2.0 codebase.

## Verdict

**Grade A**: `statsmodels.tsa.statespace`. The Kalman library. Use everywhere.

**Grade C**: `sktime` as the meta-layer combiner. Adopt in Block II for V&V / ensemble.

**Grade D**: `pyflux`, `KalmanNet`. Don't touch.

## Citations

- statsmodels statespace: https://www.statsmodels.org/dev/statespace.html
- Fulton "Implementing state space models for Statsmodels": http://www.chadfulton.com/topics/implementing_state_space.html
- Fulton "State space modeling in Python": http://www.chadfulton.com/topics/state_space_python.html
- sktime: https://github.com/sktime/sktime
- KalmanNet paper (Revach et al., 2022, IEEE TSP): arXiv:2107.10043
- Recursive KalmanNet (2025): arXiv:2506.11639
- PyFlux (archive): https://pyflux.readthedocs.io/

## Related

- [[L032]] — NY Fed Nowcasting (`DynamicFactorMQ`)
- [[L035]] — statsmodels + BVAR ecosystem
- [[L036]] — Bayesian stack (PyMC for non-Gaussian extensions)
- [[L044]] — Nixtla (the ML/neural side, also includes ensemble)
- R14 — L3 architecture
