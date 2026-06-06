# L080 — Monte Carlo + Copula + Scenario-Tree Open-Source Libs for the Scenario Engine

**Loop**: 080 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Thesis of this loop

The OPENGEM scenario engine is the *intellectually most interesting* surface in the product. It is where forecasts become *scenarios* — bundles of joint paths through indicator space, with explicit dependence structure (copulas), explicit branch-pruning logic (scenario trees), and explicit uncertainty propagation (Monte Carlo).

The open-source library landscape for this is *good but fragmented*. No single library covers every shape OPENGEM needs. The correct strategy is *deliberately polyglot*: pick three core libs that cover the surface, write a thin OPENGEM-owned abstraction layer that hides the polyglot from the rest of the system.

The libraries surveyed:
- **chaospy** — uncertainty quantification, copulas, polynomial chaos expansion.
- **pomegranate** — probabilistic graphical models (Bayesian networks, HMMs, mixtures).
- **Squiggle** — DSL for probabilistic estimation (QURI/Effective Altruism community).
- **PyMC / Stan / numpyro** — full Bayesian inference.
- **scipy.stats + copulae + copulas** — base distributions and copula libraries.

Verdict matrix:
- **chaospy**: **ADOPT-V1** for the copula + Monte Carlo workhorse.
- **scipy.stats + copulas (sdv-dev/copulas)**: **ADOPT-V1** for base distributions and elliptical/Archimedean copulas.
- **pomegranate**: **EVALUATE-LATER** for the scenario-tree / Bayesian network layer.
- **PyMC**: **ADOPT-V2** for the rare full-Bayesian fit (vintage-specific revisions of the methodology).
- **Squiggle**: **SKIP** the language; **STEAL the UX**. The Squiggle notation is good for *human-eyeball* sanity checks of the model OPENGEM internally codes in Python.

## chaospy — the workhorse

- **License**: MIT.
- **Author**: Jonathan Feinberg (post-doc at Simula). Maintained, well-documented.
- **Scope**: uncertainty quantification toolbox. Built around polynomial chaos expansion (PCE) but provides a clean distribution + copula + quadrature + sampling API.
- **Key capabilities for OPENGEM**:
  - 80+ named univariate distributions (normal, t, beta, gamma, mixture).
  - Joint distributions via dependency structures — including copulas (Clayton, Gumbel, Frank, t, normal, plus the structural ones from Nataf and Rosenblatt transformations).
  - Sobol' and Halton low-discrepancy sequences (better than naive MC at the same sample count).
  - PCE for *fast* uncertainty quantification — fit a polynomial surrogate to a model, sample 10,000 from the surrogate for the price of 100 model evaluations.
  - Sensitivity analysis (Sobol' indices, total-effect indices) baked in.
- **Integration with the OPENGEM stack**: pure-Python, numpy-native, plays nicely with statsmodels and scipy.
- **Why this matters for OPENGEM**: the V&V matrix wants honest sensitivity numbers ("how much does the GPR composite assumption affect the CPI-Brazil-3M forecast"). chaospy's Sobol' indices answer this directly.

## scipy.stats + copulas — the base

scipy.stats covers the textbook univariate distributions. The `copulas` library (sdv-dev/copulas, MIT) provides:
- Gaussian copula.
- t-copula (heavier tails — critical for macro joint distributions where Gaussian under-prices joint crashes).
- Archimedean copulas (Clayton, Gumbel, Frank).
- Vine copulas (multivariate via pair-copula construction).

For OPENGEM's "give me joint scenarios where EM currencies, sovereign spreads, and commodity prices co-move correctly" job, t-copulas and vine copulas are the right family. chaospy + copulas together cover this.

## pomegranate — Bayesian networks and scenario trees

- **License**: Apache 2.0.
- **Author**: Jacob Schreiber (UW). Active development; the 2024 rewrite (`pomegranate.distributions` over PyTorch) is the modern API.
- **Scope**: Bayesian networks, hidden Markov models, mixtures, factor graphs.
- **Why for OPENGEM**: the *scenario tree* affordance — "if Brazil's CPI surprises high, then BRL weakens; if BRL weakens, then commodity prices in BRL terms drift up; if commodity prices drift up, then Brazil's trade balance shifts" — is a Bayesian network. Pomegranate provides the structure-learning + inference algorithms.
- **Tradeoff**: the PyTorch rewrite is fast but Has been settling. Versions can be unstable. The Y1 OPENGEM scenario tree may be small enough that a custom implementation is simpler.
- **EVALUATE-LATER**: revisit at Y2 when the scenario tree exceeds ~50 nodes and benefits from a real BN inference engine.

## PyMC / Stan / numpyro — Bayesian inference

- **PyMC**: Apache 2.0, Python-native, JAX backend (PyMC 5+).
- **Stan / cmdstanpy**: BSD-3, separate language, fast.
- **numpyro**: Apache 2.0, JAX-native, fastest for HMC.

OPENGEM does Bayesian work for the *deep* methodology layer — fitting time-varying-parameter models, hierarchical priors on country-specific coefficients, posterior-predictive scoring. For Y1 most of this can be `statsmodels` and `scikit-learn`; full Bayesian fits are *Y2-Y3* when methodology rigor goes up a notch.

**ADOPT-V2**: PyMC for the rare full-Bayesian fits, called from the scenario engine when the methodology demands it.

## Squiggle — the UX to steal

Squiggle is a probabilistic-estimation DSL from QURI (Quantified Uncertainty Research Institute). The syntax looks like:

```
incomeAt2050 = 50k to 200k
yearsToRetirement = 25 to 40
savingsRate = beta(2, 5) * 0.5
```

The reader instantly understands the *shape* of every parameter. A reader of an OPENGEM scenario model doesn't have to parse `scipy.stats.lognorm(s=0.4, scale=1e5)`.

For OPENGEM the Squiggle *language* is wrong (it's a separate runtime, JS-based, doesn't integrate with the OPENGEM Python core). But the *notation* is right. The scenario-page methodology pop-up should show the scenario in Squiggle-like notation:

```
brazil_cpi_2026Q4_growth = 3% to 6%   # 90% CI
brazil_currency_2026Q4_pct_change = -8% to +5%   # 90% CI, t-copula correlated with cpi at rho=-0.35
brazil_trade_balance_2026Q4_pctgdp = -1.2 to +0.8   # 90% CI, Gaussian copula with currency at rho=+0.4
```

This is the "human readable model" affordance OPENGEM should ship. The implementation behind it is chaospy + scipy.stats + copulas in Python; the *display* is Squiggle-flavored notation. **STEAL the UX, SKIP the runtime.**

## Other libraries surveyed and rejected

- **ergo** (Salt-Mining/Ought): an LLM-assisted probabilistic estimation tool. Interesting research direction. **SKIP** for V1; revisit if the MCP server gains a "draft a scenario for me" tool.
- **scenarioGen / sklearn-based synthetic data generators**: tabular synthetic data, wrong shape for OPENGEM scenarios.
- **Pyro / GPyTorch**: deep probabilistic modeling. **SKIP** until OPENGEM has a deep-model methodology pack.
- **statsforecast / neuralforecast (Nixtla)**: covered in L044 — these are the *forecasting* layer, not the *scenario* layer.
- **bambi**: regression DSL on top of PyMC. Nice for analysts who want formula syntax. **EVALUATE-LATER** as a developer-experience win.

## The OPENGEM scenario engine architecture

Pulling this together, here is the V1 stack:

1. **Scenario manifest** (YAML or JSON): names the variables, declares their univariate distributions (in scipy.stats vocabulary), declares the copula structure (which variables are jointly distributed by what copula family with what parameters), declares the policy assumptions.
2. **chaospy + copulas + scipy.stats** at the runtime: sample N=10,000-100,000 joint draws from the declared joint distribution.
3. **Forecast model layer** (separate, not part of this loop): for each joint draw, run the underlying econometric / ML forecast model to produce a path through indicator space.
4. **Aggregation layer**: bundle the N paths into a *scenario distribution* over the indicator space at each horizon.
5. **V&V scoring**: when realizations arrive, score the scenario distribution against the realization using CRPS, log-score, calibration, sharpness.
6. **Display layer**: Squiggle-flavored notation for the manifest; Observable Plot for the distribution viz; Lightweight Charts for the forecast band.

## Cost / performance reality

- All libraries above are CPU-bound, single-machine. A typical OPENGEM scenario with 20 variables and N=50,000 joint draws runs in 2-30 seconds depending on the model layer.
- For nightly rebuild of all scenarios across all countries × all indicators × all horizons: 1-4 hours of CPU on a single 16-core machine.
- Cost: ~$15-50/mo for a Hetzner CPX31 dedicated to scenario rebuild.
- Storage of materialized scenarios: ~5-20 GB Parquet on S3, $1-2/mo.

## Ramp-up

- Week 1: chaospy + copulas + scipy.stats wired into a minimal "joint sample" function with 5 variables.
- Week 2: scenario manifest YAML loader + validator.
- Week 3: full scenario for one country×one horizon×one model.
- Week 4: parallelize across countries; nightly job.
- Week 5: V&V scoring integration.
- Week 6: Squiggle-flavored display generator.

A 6-week sprint to a V1 scenario engine.

## Verdict

- **chaospy**: **ADOPT-V1**. Workhorse.
- **scipy.stats + copulas**: **ADOPT-V1**. Base distributions and copulas.
- **pomegranate**: **EVALUATE-LATER** for Bayesian-network scenario trees.
- **PyMC**: **ADOPT-V2** for occasional full-Bayesian fits.
- **Squiggle (language)**: **SKIP**.
- **Squiggle (notation as display UX)**: **ADOPT-V1**. Steal the syntax.
- **ergo / bambi**: **EVALUATE-LATER**.
- **scenarioGen / sdv tabular**: **SKIP**.

## Cost summary

| Tool | License | Cost | Use | Ramp |
|---|---|---|---|---|
| chaospy | MIT | $0 | UQ + Sobol' + sampling | 1 week |
| scipy.stats | BSD-3 | $0 | Univariate distributions | 0 (existing) |
| copulas (sdv-dev) | MIT | $0 | Copula families | 3 days |
| pomegranate (Y2+) | Apache 2.0 | $0 | Bayesian networks | 2-3 weeks |
| PyMC (Y2+) | Apache 2.0 | $0 | Full Bayesian fits | 2-3 weeks |
| Compute (Hetzner CPX31) | n/a | $15-50/mo | Nightly scenario rebuild | 1 day |

## What comes next

- **L081** (Phase 2) begins the deep-dive series on the top 10 Phase 1 candidates.
- **L125** (Phase 3) is the scenario-page layout candidates.

## Related

- [[L072-lightweight-charts-highcharts-apex]] — forecast-band display
- [[L069-d3-vega-plotly]] — distribution viz via Observable Plot
- [[L044-nixtla-statsforecast-neuralforecast]] — point-forecast layer beneath
- [[L125-scenario-page-layouts]] — Phase 3 page design
