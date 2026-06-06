# L035 — statsmodels DFM + Bayesian VAR ecosystem: maturity, gaps, companion libs

**Loop**: 035 / 300
**Phase**: 1 — Open-source landscape survey (statsmodels and Bayesian VAR)
**Date**: 2026-06-06
**OPENGEM adoption grade**: **A for statsmodels DFM/state-space, B for VAR + BVAR companion stack**

---

## TL;DR

`statsmodels.tsa.statespace` is the **most production-ready open-source state-space framework in Python, period.** Chad Fulton (NY Fed) is the lead author. The Kalman filter is Cython, the API is sklearn-friendly, the `DynamicFactorMQ` class is — as established in L032 — the same NY-Fed nowcasting framework that everyone in central banking uses. **This is OPENGEM's L3 backbone, full stop.**

The frequentist VAR / VECM side (`statsmodels.tsa.vector_ar`) is solid for point forecasts but **does not include native Bayesian VAR**. For BVAR — which OPENGEM needs for the wider L3 ensemble — the recommended companion stack is:

1. **For hierarchical / conjugate prior BVAR (Giannone-Lenza-Primiceri style)**: use R's `BVAR` package (Kuschnig & Vashold 2021, JSS) via `rpy2`, OR build it ourselves from the published spec. There is **no equivalent maintained Python BVAR** with hierarchical priors at the GLP level.
2. **For more flexible Bayesian VAR with stochastic volatility, time-varying parameters**: use PyMC (L036). PyMC handles "any VAR is a BVAR" out of the box — sampling a BVAR(2) on 122 quarterly obs in 17 seconds per PyMC Labs benchmark.
3. **For "large BVAR" (à la Crump-Eusepi-Giannone-Qian-Sbordone 2021)**: `covbayesvar` on PyPI (Python port of the original MATLAB) plus a 4-star research repo `Allisterh/Large-BVAR-Python-codes-`. **Both are research-grade, not production-grade.** Maintain in a vendored fork if used.

So the stack is: **statsmodels for DFM and frequentist VAR + PyMC for Bayesian extensions + (optional) `bvar` R bridge for hierarchical priors**. Together these cover essentially the entire L3 layer.

## statsmodels.tsa as the base

`statsmodels` is a 20-year-old Python statistics library, BSD-3-Clause, ~10K+ GitHub stars, maintained by a stable group including Josef Perktold, Chad Fulton, Kevin Sheppard, Skipper Seabold, Brock Mendel, and others. The relevant submodules for OPENGEM:

| Submodule | What's in it | OPENGEM use |
|---|---|---|
| `tsa.arima_model`, `tsa.arima` | ARIMA, ARMAX, SARIMAX | Baseline forecasts for V&V matrix |
| `tsa.statespace` | Generic state-space framework, MLE estimation | Backbone for *everything* |
| `tsa.statespace.dynamic_factor_mq` | NY Fed Nowcast equivalent | **L3 DFM workhorse** (L032) |
| `tsa.statespace.varmax` | VARMAX (state-space VAR with exogenous) | Multivariate forecast experiments |
| `tsa.vector_ar.var_model` | Frequentist VAR with IRFs, FEVD, Granger causality | Multivariate baselines, ensemble members |
| `tsa.vector_ar.vecm` | Vector Error Correction Model, Johansen tests | Cointegrating analysis for long-run scenarios |
| `tsa.stattools` | Stationarity, autocorrelation, structural break tests | Pre-modeling diagnostics |
| `tsa.x13` | X-13 ARIMA-SEATS interface for seasonal adjustment | Production-grade SA for our adapters |
| `tsa.holtwinters` | Triple exponential smoothing | Bottom-rung baseline |

**Key maturity facts**:

- `statsmodels.tsa.statespace` is THE state-space library in Python. Heavy use by NY Fed (Fulton is staff), academic users, and production teams.
- The Kalman filter is in Cython — fast enough for daily / weekly cadence on hundreds of countries.
- Custom state-space models are supported via subclassing `MLEModel`. We can build *anything* (mixed-frequency MIDAS, factor-augmented VAR, time-varying parameters) on top.
- Documentation is good. Fulton's blog (chadfulton.com) has the canonical reference for state-space in Python.

## The Bayesian VAR gap

`statsmodels` has no native BVAR. This is the single biggest gap in the Python macro stack.

What people actually do:

1. **Roll their own with PyMC** (L036). For research, this is fine. For production, you write a lot of boilerplate (priors, sampling tuning, posterior summarization).

2. **Use R via `rpy2`**. The R BVAR ecosystem is mature:
   - **`bvar`** by Kuschnig & Vashold (JSS 2021), CRAN. Hierarchical priors à la GLP-2015. 57 GitHub stars, last release Feb 2024, FRED data included. **Solid.**
   - **`BGVAR`** by Boeck, Feldkircher, Huber (JSS 2022). 34 stars. GVAR (cross-country) with shrinkage. **The right tool for our L2 layer (see L038)**.
   - **`BVAR.jl`** in Julia and `BMR` in C++ exist but are less mature.
   - **`BEAR`** ECB toolbox (L041) is comprehensive but MATLAB.

3. **Use the few Python ports**:
   - **`covbayesvar`** on PyPI: covbayesvar is the Python port of "Large BVAR of the U.S. Economy" (Crump-Eusepi-Giannone-Qian-Sbordone 2021). Functions translated "one-to-one" from MATLAB. Research-grade.
   - **`Allisterh/Large-BVAR-Python-codes-`**: 4 stars on GitHub, "preliminary testing stage" per maintainer. Same MATLAB reference plus Lenza-Primiceri 2022 pandemic prior. Fragile.
   - There is no widely-used Python BVAR with the polish of the R `bvar` or the ECB BEAR.

## Recommended OPENGEM L3 stack

```
┌─────────────────────────────────────────────────────────┐
│            statsmodels.tsa (BSD-3-Clause)               │
│  ── statespace.DynamicFactorMQ  (L3 DFM workhorse)     │
│  ── statespace.MLEModel custom subclasses (MIDAS etc.) │
│  ── vector_ar.var_model         (frequentist VAR)      │
│  ── vector_ar.vecm              (VECM for long-run)    │
│  ── stattools, x13              (diagnostics + SA)     │
└─────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────┐
│              PyMC (Apache-2.0)                          │
│  ── BVAR with hierarchical priors                      │
│  ── BVAR-SV (stochastic volatility)                    │
│  ── BVAR-TVP (time-varying parameters)                 │
│  ── Posterior probability scenarios                    │
└─────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────┐
│        Optional: R via rpy2 for `bvar` / `BGVAR`        │
│  ── GLP-2015 hierarchical conjugate priors             │
│  ── Cross-country GVAR (L038)                          │
└─────────────────────────────────────────────────────────┘
```

For ML / neural forecasting, we add Nixtla (L044). For "lightweight ensemble combiner over all of these", we use a custom `opengem-l3-combiner` package built around the V&V matrix scoring (L189).

## Gaps and how we handle them

| Gap in statsmodels | OPENGEM coping strategy |
|---|---|
| No native BVAR | PyMC for flexible BVAR; R `bvar` via `rpy2` for hierarchical GLP |
| No native MIDAS regression | Build on `MLEModel`; Fulton's blog has an example |
| No native FAVAR | Build on `MLEModel` + `DynamicFactorMQ` factor extraction |
| No native local-linear-trend with intervention | `UnobservedComponents` covers basic; intervention via dummy regressors |
| No native fractional cointegration | Acceptable gap; not needed at our scope |
| Slow large-panel DFM EM | OK in batch mode. For real-time updating use `news` decomposition pattern from Fulton's notebook |
| No native quantile regression (for fan charts) | Use `statsmodels.regression.quantile_regression` |
| No state-space hierarchical Bayesian | This is what PyMC is for |

## Companion libraries to pin

```toml
[project.dependencies]
statsmodels = ">=0.14.0"          # state-space, DFM, VAR — production
numpy = ">=1.26"
pandas = ">=2.2"
scipy = ">=1.13"
pymc = ">=5.10"                   # BVAR with priors (L036)
arviz = ">=0.17"                  # posterior diagnostics
sktime = ">=0.30"                 # only for the meta-ensemble combiner
nixtla-statsforecast = ">=2.0"    # baselines + ETS + AutoARIMA (L044)
# Optional, behind feature flag:
rpy2 = ">=3.5"                    # R bridge for bvar / BGVAR
```

## What we should NOT use

- **PyFlux**. Abandoned circa 2017. Issue #3 ("statsmodels statespace models") on RJT1990/pyflux acknowledged statsmodels was eating its lunch even then. Don't import. Don't fork.
- **`MajesticKhan/Nowcasting-Python`** as a runtime dependency. Stale 2021. Read it for understanding only.
- **`covbayesvar`** for anything we ship to users. Maybe for one-off research. Vendor if needed.

## Verdict

**A-grade for statsmodels.tsa** (state-space + DFM). This is *the* substrate.

**B-grade for the BVAR companion stack** because of the gap: there is no first-class native Python hierarchical BVAR. PyMC fills most of it. R via rpy2 covers the rest.

The recommendation crystalizes: **L032's adoption of `DynamicFactorMQ` is the single most important pick from this whole block, and L035 says the framework that hosts it (`statsmodels.tsa`) is the supporting cast we also adopt without hesitation.**

## Citations

- `statsmodels.tsa` reference: https://www.statsmodels.org/stable/tsa.html
- Fulton blog "State space modeling in Python": http://www.chadfulton.com/topics/state_space_python.html
- Kuschnig, N. & Vashold, L. "BVAR: Bayesian Vector Autoregressions with Hierarchical Prior Selection in R." JSS 100(14), 2021. https://www.jstatsoft.org/article/view/v100i14
- Giannone, Lenza, Primiceri. "Prior Selection for Vector Autoregressions." *RES* 2015.
- Crump, R. K., Eusepi, S., Giannone, D., Qian, E., Sbordone, A. M. "A Large Bayesian VAR of the United States Economy." 2021.
- PyMC Labs BVAR tutorial: https://www.pymc-labs.com/blog-posts/bayesian-vector-autoregression
- `covbayesvar` PyPI: https://pypi.org/project/covbayesvar/
- PyMC BVAR example: https://www.pymc.io/projects/examples/en/latest/time_series/bayesian_var_model.html

## Related

- [[L032]] — NY Fed Nowcasting (where the DFM stack lives)
- [[L036]] — Bayesian stack pick (PyMC vs Stan vs numpyro)
- [[L037]] — Kalman/state-space lib recommendation
- [[L038]] — BGVAR for cross-country (L2)
- [[L041]] — Bank of England's Mumtaz-Blake handbook MATLAB code
- [[L044]] — Nixtla ensemble baselines
- R14 — L3 architecture (this is the build map)
