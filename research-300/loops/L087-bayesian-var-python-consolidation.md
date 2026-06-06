# L087 — Bayesian VAR Python Stack Consolidation: statsmodels vs PyMC vs BayesianStats

**Loop**: 087 / 300
**Phase**: 2 — Integration deep dive
**Date**: 2026-06-06
**Verdict**: **ADOPT-V1 (PyMC for Bayesian variants + statsmodels for classical VAR + `bayesianStats` REJECTED)**

---

## What this loop answers

L035 surveyed the statsmodels DFM + BVAR ecosystem; L036 surveyed the PyMC/Stan/NumPyro Bayesian stack; L041 looked at the Bank of England BVAR toolkits. The Phase 2 question is *pick one stack* for OPENGEM's BVAR component of the L3 ensemble, so we are not gluing three half-implementations together.

The answer: **PyMC for posterior-sampled BVAR variants (BVAR, BVAR-SV, hier-BVAR), statsmodels for classical-frequentist VAR/VARMAX as a baseline, and the `bayesianStats` package rejected.** Three reasons follow.

## The three candidates as code

### statsmodels.tsa.api.VAR / VARMAX

- BSD-3-Clause.
- Production-grade, used by every macroeconomist who's touched Python.
- Frequentist OLS estimation; ships standard impulse-response functions, FEVDs, Granger causality.
- **Does not ship native Bayesian estimation.** There are community PRs for Minnesota-prior BVAR (still open as of 2026), but the canonical path inside statsmodels is OLS.
- Excellent for the classical VAR/VARMAX baseline and the Cholesky-IRF stress test layer.
- Mixed-frequency: VARMAX supports it; pure VAR does not.

### PyMC (pymc-devs/pymc, plus pymc-experimental for state-space)

- Apache-2.0.
- Modern, active development (5.x line through 2026), backed by PyMC Labs.
- The `pymc_experimental.statespace` module added a `BayesianVARMAX` and `BayesianStructuralTimeSeries` class line in 2024-2025. These are the canonical Python paths for fully Bayesian VAR with hierarchical priors, stochastic volatility, and time-varying parameters.
- Posterior sampling via NUTS (HMC), variational inference (ADVI), or SMC. NUTS is the default; ADVI is the fallback for high-dim problems.
- First-class probabilistic forecasting via `sample_posterior_predictive`. Outputs full predictive densities with arbitrary quantiles — exactly what the OPENGEM accountability ledger wants.
- Plays cleanly with `arviz` for posterior diagnostics, with the LOO/WAIC info criteria, with calibration plotting.
- Extensible: user-defined priors, structural identification schemes, regime-switching extensions are all idiomatic PyMC code.

### "bayesianStats" — what's actually behind that name

`bayesianStats` does not exist as a named PyPI package as of mid-2026. The closest matches are:

- **`bayes-statsmodels`** — a community fork attempting Bayesian extensions to statsmodels. Last commit 2022, ~30 stars, single maintainer. Dead.
- **`bayesianlearn`** — an unrelated educational package.
- **`bayesian-statistics`** — a textbook companion, not a forecasting library.

L036's reference to "bayesianStats" likely came from a survey-paper grouping rather than a real package. **Rejected by virtue of not existing as a maintained library.** If the originating reference was to one of the variants above, the verdict is the same: stale, single-maintainer, not production-grade.

(If a new actively-maintained `bayesianStats` package appears later, we re-evaluate. But not for v1.)

## The four-layer BVAR roadmap

OPENGEM's BVAR component of the L3 ensemble is not one model — it's a tiered family. The tier structure:

### Tier 1 — Classical VAR baseline (statsmodels)

The boring baseline. Fit a VAR(p) on the same panel the DFM uses, no Bayesian priors, OLS. Used for:

- The "no priors" reference that every other BVAR variant must beat in the V&V matrix.
- The Cholesky-IRF stress test layer that every L210 counterfactual scenario uses.
- The teaching artifact in the methodology pop-up ("here's what a classical VAR says, vs. what our Bayesian variants say, vs. what consensus says").

**Cost**: ~1 dev-week. The model already works; we wrap it in our adapter pattern.

### Tier 2 — Minnesota-prior BVAR (PyMC)

The workhorse Bayesian VAR. Minnesota prior (Litterman 1986) with shrinkage hyper-parameters from data via empirical Bayes or fixed defaults from the literature. Implemented as a PyMC model:

```python
import pymc as pm
import numpy as np

def make_minnesota_bvar(y, p=4, lam1=0.2, lam2=0.5, lam3=1.0, lam4=100.0):
    """Minnesota-prior BVAR(p).
    lam1: overall tightness
    lam2: cross-equation tightness
    lam3: lag decay
    lam4: constant looseness
    """
    n, k = y.shape  # n obs, k variables
    with pm.Model() as model:
        # Build the prior precision matrix per Litterman's Minnesota rule
        prior_sd = _minnesota_sd(k, p, lam1, lam2, lam3, lam4)
        beta = pm.Normal("beta", mu=_minnesota_mean(k, p), sigma=prior_sd, shape=(k*p + 1, k))
        sigma = pm.LKJCholeskyCov("sigma", n=k, eta=1.0, sd_dist=pm.HalfNormal.dist(sigma=1.0))
        L = pm.expand_packed_triangular(k, sigma)
        for t in range(p, n):
            mu_t = _build_var_mean(beta, y, t, p)
            pm.MvNormal(f"y_t{t}", mu=mu_t, chol=L, observed=y[t])
    return model

with make_minnesota_bvar(panel_array, p=4) as model:
    trace = pm.sample(2000, tune=1000, chains=4, target_accept=0.95)
    forecasts = pm.sample_posterior_predictive(trace, var_names=["y_future"])
```

The `_minnesota_sd` helper encodes the Litterman rule: own-lag tightness `lam1 / l^lam3` for variable `i` lag `l`; cross-equation tightness `lam1 * lam2 / l^lam3 * sigma_i / sigma_j`; constant variance `lam1 * lam4`. This is canonical from any Bayesian VAR textbook.

**Cost**: ~2 dev-weeks for the model + ~1 dev-week for tuning hyper-priors + ~1 dev-week for the forecast wrapper. ~4 weeks total.

### Tier 3 — BVAR with stochastic volatility (BVAR-SV, PyMC)

Macro time series have time-varying volatility (the Great Moderation, the COVID shock, regime shifts). BVAR-SV adds a stochastic-volatility process on the residual covariance. Implemented via `pymc_experimental.statespace.BayesianVARMAX` with a `StochasticVolatility` extension, or hand-coded as:

```python
with pm.Model() as model:
    # log-volatility process per equation
    h0 = pm.Normal("h0", mu=0, sigma=1, shape=k)
    rho = pm.Beta("rho", alpha=20, beta=1.5, shape=k)
    sigma_h = pm.HalfNormal("sigma_h", sigma=0.2, shape=k)
    h = pm.AR("h", rho=rho, sigma=sigma_h, init_dist=pm.Normal.dist(mu=h0, sigma=1.0), shape=(n, k))
    
    # VAR coefficients with Minnesota prior (as above)
    beta = pm.Normal("beta", ...)
    
    # Likelihood with time-varying covariance
    for t in range(p, n):
        sigma_t = pm.math.exp(h[t] / 2) * base_corr_matrix
        mu_t = _build_var_mean(beta, y, t, p)
        pm.MvNormal(f"y_t{t}", mu=mu_t, cov=sigma_t, observed=y[t])
```

Sampling cost: ~10x slower than classical VAR. For ~10-variable panels and ~25-year quarterly histories, NUTS takes ~30-60 minutes on a single CPU.

**Cost**: ~3 dev-weeks. The model code is ~50% reused from Tier 2; the SV process is the increment.

### Tier 4 — Hierarchical BVAR across countries (hier-BVAR, PyMC)

For cross-country forecasts, we share information across countries via a hierarchical prior on VAR coefficients: country-level coefficients are drawn from a global distribution whose parameters are themselves estimated. This is the natural Bayesian framing of "borrow strength from US data when forecasting Czechia."

```python
with pm.Model() as model:
    # Global hyper-priors on VAR coefficient distribution
    mu_beta = pm.Normal("mu_beta", mu=0, sigma=1, shape=coef_shape)
    sigma_beta = pm.HalfNormal("sigma_beta", sigma=0.5, shape=coef_shape)
    
    # Per-country coefficients drawn from global
    beta = pm.Normal("beta", mu=mu_beta, sigma=sigma_beta, shape=(n_countries, *coef_shape))
    
    # Per-country residual covariance
    for c in range(n_countries):
        ...  # standard BVAR likelihood per country with beta[c]
```

Sampling cost: scales roughly linearly in number of countries. For ~20 countries, ~2-4 hours on CPU; ~30 minutes with PyMC's `nutpie` JAX backend on GPU.

**Cost**: ~3-4 dev-weeks. Including model spec, identification of hyper-priors, calibration vs single-country baselines, V&V matrix scoring.

## Why this stack, not the alternatives

### Why not Stan (cmdstanpy)?

Stan is the canonical Bayesian-modeling DSL. Many of the BVAR-SV / hier-BVAR models above have published Stan implementations. *But*: shipping a Stan dependency requires installing the CmdStan binary, which is a 200MB+ compile dependency that's awkward in Docker images and a friction point for contributors. PyMC ships as a pure-Python package; PyTensor (PyMC's autograd) is a normal pip dependency. **For a single-person dev team, Python-native wins.**

If we ever need a model that's better-supported in Stan than PyMC (e.g. the Chan-Eisenstat 2018 hierarchical TVP-VAR-SV — written in Stan first), we add Stan as an optional dependency for that one model. Not the default.

### Why not NumPyro?

NumPyro is JAX-based, ~5-10x faster than PyMC for many Bayesian VAR variants, and uses identical NUTS sampling. Strong contender. Why we don't pick it as the primary:

- JAX has a steeper installation tax (CUDA matching is fragile), especially on contributor laptops.
- PyMC's ecosystem (arviz, posterior-predictive sampling, calibration tooling) is more mature for forecasting use.
- PyMC has a `nutpie` JAX backend we can enable for the heavy hier-BVAR runs — getting most of the NumPyro speed without committing the codebase to JAX semantics.

If a future loop discovers we're bound by sampling speed (PyMC NUTS too slow), we revisit. For v1, the speed is OK.

### Why not BVAR in R (`BVAR`, `bvars`)?

R's BVAR ecosystem is older and arguably more mature for some niche variants. But: R-Python interop via `rpy2` is a known source of pain (subprocess management, GC interactions). Our dashboard, our adapters, our forecast pipeline are all Python-native. Adding R is a force multiplier on dependency complexity for marginal model variety.

### Why not BGVAR R package (L038)?

L038 already concluded: BGVAR is excellent for global VAR estimation but requires R, and the marginal benefit over a Python-native hier-BVAR is modest. The cross-country information-pooling story is similar; the Python implementation is more practical for our integration. **L038 verdict deferred to PyMC hier-BVAR as the substitute.** Confirmed here.

## Integration with the L3 ensemble

The four tiers feed into the L3 BMA combiner as four ensemble members:

```
L3 ensemble members:
  - statsmodels DFM (DynamicFactorMQ) — L086
  - statsmodels VAR (classical baseline) — this loop, Tier 1
  - PyMC BVAR Minnesota — this loop, Tier 2
  - PyMC BVAR-SV — this loop, Tier 3
  - PyMC hier-BVAR — this loop, Tier 4
  - Nixtla statsforecast baselines (AutoARIMA, AutoETS, Theta, RW) — L044
  - Nixtla mlforecast (LightGBM) — L044
  - neuralforecast NHITS (Block II experimental) — L088
  → BMA combiner produces final P10/P50/P90 — L189
```

Each member writes its forecast to the vintage store under its own `model_id`. The BMA combiner reads all of them and weights by historical CRPS.

## Cost summary

| Tier | Cost | Cumulative |
|---|---|---|
| Tier 1 — Classical VAR wrapper | 1 dev-week | 1 |
| Tier 2 — Minnesota BVAR | 4 dev-weeks | 5 |
| Tier 3 — BVAR-SV | 3 dev-weeks | 8 |
| Tier 4 — Hier-BVAR | 4 dev-weeks | 12 |
| V&V matrix scoring across all tiers | 1 dev-week | 13 |
| Methodology card text + Bayesian credible-band rendering | 1 dev-week | 14 |
| **Total `opengem-l3-bvar` v0.1.0** | | **~14 dev-weeks** |

That's larger than the DFM port (L086, ~10 weeks). Justified: BVAR is the single most-extensible piece of the L3 stack. Tier 4 hier-BVAR is the bedrock for the cross-country comparison story that distinguishes OPENGEM from country-by-country incumbents.

## Risks

1. **NUTS sampling diverges.** A poorly-conditioned posterior triggers PyMC divergences. Mitigation: standard remedies (reparameterize, non-centered priors, increase `target_accept` to 0.95+), automated divergence-rate alerting in CI.

2. **Computational scaling on hier-BVAR.** 20+ countries × 4 chains × 2000 samples = real CPU time. Mitigation: PyMC's `nutpie` JAX backend; cache fitted parameters across forecast vintages so re-fit happens monthly, not daily.

3. **Prior sensitivity.** Bayesian forecasts are only as good as the priors. Mitigation: publish prior-sensitivity bands alongside point forecasts; run informal-prior vs reference-prior comparison on every Tier-V country and surface the disagreement.

4. **Identification of structural shocks.** Cholesky identification is a strong assumption. Mitigation: ship Cholesky as default; offer sign-restriction identification as a methodology-pop-up alternative for users who want to test it.

## What this loop produced

- Confirmed PyMC as the Bayesian stack, statsmodels as the classical baseline.
- Rejected `bayesianStats` (does not exist as a maintained package).
- Four-tier BVAR roadmap with concrete model spec for each tier.
- Cost: ~14 dev-weeks total for the full BVAR suite.
- Integration plan with the L3 ensemble.

## What comes next

- **L088** — neuralforecast for L3: the deep-learning experimental layer.
- **L189** — BMA combiner.
- **L204** — TVP-VAR (a Tier 5 extension if we want time-varying parameters).
- **L208** — Tail forecasts (left-tail GDP fan charts from BVAR-SV).

## Related

- [[L035-statsmodels-bvar-ecosystem]] — Phase 1 statsmodels survey.
- [[L036-bayesian-stack-pymc-stan-numpyro]] — Phase 1 PyMC vs Stan vs NumPyro.
- [[L038-bgvar-r-package]] — Phase 1 R BGVAR (superseded by PyMC hier-BVAR).
- [[L041-boe-bvar-toolkits]] — Phase 1 BoE Bayesian toolkit reference.
- [[L086-nyfed-nowcasting-reuse-vs-rewrite]] — DFM sibling.
- [[L088-neuralforecast-l3-layer]] — DL sibling.
- [[L189-bma-combiner]] — downstream combiner.
- [[L204-tvp-var]] — Tier 5 extension.
- [[L208-tail-forecasts]] — BVAR-SV consumer.
