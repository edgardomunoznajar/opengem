# L036 — Bayesian stack for macro: Stan + cmdstanpy + bayes_mvs + pymc + numpyro

**Loop**: 036 / 300
**Phase**: 1 — Open-source landscape survey (Bayesian)
**Date**: 2026-06-06
**OPENGEM adoption grade**: **A for PyMC** (pick), **B for cmdstanpy fallback**

---

## TL;DR

**Pick PyMC.** Specifically: PyMC 6.x as primary, with `nutpie` / `numpyro` JAX samplers for performance-critical BVAR-SV and TVP models. Keep CmdStanPy in the toolbox for a small set of canonical Stan models (especially for replicating published papers where the authors shipped `.stan` files).

Reasoning:

1. **PyMC is Apache-2.0**, runs natively in Python, has a thriving ecosystem (PyMC Labs, NumFOCUS), and is at v6.0.1 as of May 2026. It's the standard for "I want to write a Bayesian model in 50 lines and have it just work."
2. **NumPyro is BSD-3-Clause**, lives in JAX-land, is the fastest sampler we can plug into PyMC (PyMC's JAX backend uses NumPyro NUTS). For GPU sampling at scale, ~11× ESS/sec vs CPU PyMC, ~4× vs JAX-on-CPU.
3. **Stan via CmdStanPy** is the most published, most replicated PPL — Stan papers ship `.stan` files, and we want to be able to re-run them. CmdStanPy is BSD-3, actively maintained (v1.3.0, v2.0 in the pipeline), thin wrapper over the CmdStan C++ binary.
4. **bayes_mvs** (in scipy.stats) is not in scope — it's a univariate posterior summary tool for mean/variance/stdev, not a PPL. Useful as a quick reference but irrelevant for our L3 needs.
5. **NumPyro standalone** vs. **PyMC + JAX backend**: the API of PyMC is more pleasant, and PyMC gets the same speed by delegating to NumPyro. Default to PyMC; reach for NumPyro directly only when you need a tight JAX integration.

The killer use case for OPENGEM: **hierarchical Bayesian VAR across countries**. PyMC handles this natively. Stan handles it but with more boilerplate. NumPyro handles it but with a steeper learning curve. PyMC is the right pick for the "L3 layer that humans can read and maintain at personal scale."

## What each tool is

### PyMC (the pick)

- Apache-2.0. 9.6k stars. v6.0.1 May 2026. PyTensor backend (formerly Theano fork) with C and JAX compilation paths.
- API: write models as Python context managers (`with pm.Model() as m:`), priors and likelihoods as namespace objects, sampling as one-liner.
- Coverage: 1000+ priors / likelihoods, MCMC (NUTS, HMC, Metropolis), VI (ADVI, FullRankADVI), SMC, gradient-based MAP.
- Production: PyMC Labs is the commercial sponsor, NumFOCUS is the non-profit backing. Used at PyMC Labs, BCG, banks, and academia.
- Examples gallery has BVAR, hierarchical BVAR across multiple countries, and a real macroeconomic case study (US GDP + term spread).

### NumPyro

- BSD-3-Clause. JAX-native. Lighter syntax than PyMC for the same model.
- Speed: NumPyro NUTS is the JAX standard. Used as a sampler backend by PyMC, Pyro, Stan-via-JAX (less common).
- API: composable effects. Models are pure Python functions decorated with `numpyro.sample` calls.
- For OPENGEM: useful for our most-computational models (large BVAR-SV, TVP-VAR with many countries). The PyMC team's pattern is "write in PyMC, sample with NumPyro" — get the API + the speed.

### Stan + CmdStanPy

- Stan: BSD-3. Mature, the canonical PPL of the 2010s, written by the Stan Development Team (Gelman, Carpenter, et al).
- CmdStanPy: BSD-3, v1.3.0, v2.0 coming. Thin Python wrapper over CmdStan C++ binary. Subprocess-based — clean separation, but requires CmdStan installation.
- Strengths: production-grade compiler, the best diagnostics in the business, the most-published PPL. Many seminal BVAR and DSGE papers ship Stan code.
- Weakness vs. PyMC: requires C++ toolchain. Slower to iterate on small models. Less Pythonic.
- For OPENGEM: keep CmdStanPy in the dev environment specifically for replicating published papers. Don't write new models in Stan unless we have to.

### Other (out of scope)

- **PyStan**: deprecated in favor of CmdStanPy as of 2022. Don't use.
- **Pyro**: PyTorch-based PPL. Larger surface, more deep-learning-y. Overkill for macro VAR.
- **scipy.stats.bayes_mvs**: posterior summaries for mean/var/stdev under fixed priors. Not a PPL. Irrelevant.
- **TensorFlow Probability**: too tied to TF; not our stack.
- **Edward2**: subsumed into TFP. Not maintained as separate.

## Benchmarks that matter

From the PyMC Labs vs Stan benchmark (Feb 2026):

- Stan starts strong on small models, slightly slower than PyMC on largest CPU dataset.
- CmdStanPy beats PyMC on small datasets (small subprocess overhead). PyMC wins on large datasets (better vectorization).
- PyMC + JAX on GPU: ~11× ESS/sec vs CPU PyMC, ~4× vs JAX on CPU.
- All produce statistically equivalent estimates — no accuracy tradeoff.

From the Tang trivial Python PPL comparison: NumPyro is consistently the fastest for the benchmarked linear regressions; PyMC and Stan are close to each other; Pyro is slower.

## What OPENGEM should use

### Default for L3 BVAR (Block II)

```python
import pymc as pm
import numpy as np

with pm.Model() as bvar:
    # Minnesota-style prior on coefficients
    coefs = pm.Normal("coefs", 0, sigma=minnesota_sigma(n_vars, n_lags))
    sigma = pm.LKJCholeskyCov("sigma", n=n_vars, eta=2)
    # ... AR structure on residuals
    pm.MvNormal("y", mu=pred, chol=chol, observed=panel.values)
    trace = pm.sample(2000, tune=1000, nuts_sampler="numpyro")
```

Three lines for the sampler choice. The `nuts_sampler="numpyro"` argument switches to JAX-NUTS without rewriting the model — exactly the API we want.

### Scenario probability synthesis (Block II)

For combining "L3 ensemble probabilities" with "scenario triggers from the rule engine," PyMC's `Mixture` and `Bernoulli` priors give us a clean hierarchical model where each scenario pack has a prior firing probability, modified by evidence (event detectors).

### Reproducibility of published papers (Block II + III)

Whenever we adopt a published model (e.g. Lenza-Primiceri 2022 pandemic prior), we install their `.stan` file via CmdStanPy and replicate exactly. Cite the paper, ship the `.stan`, attach to the model card.

### Production caveats

- **PyMC's default sampler (NUTS-C / NUTS-PyTensor) is fine for small models** (BVAR on ~10 vars, 100+ obs). For our larger panels and TVP models, switch to NumPyro backend.
- **GPU is a Block III concern**, not Block I. The CPU JAX backend is already 2–3× faster than the default — that's the bulk of the gain available before GPUs.
- **PyMC versioning is unstable across major versions** (PyMC 3 → 4 was a big break, PyMC 5 → 6 less so but still real). Pin the version. Test the upgrade path.

## License compatibility

- PyMC: Apache-2.0. Drop-in compatible with OPENGEM Apache-2.0.
- NumPyro: BSD-3-Clause. Compatible.
- CmdStanPy: BSD-3-Clause. Compatible.
- Stan engine: BSD-3-Clause. Compatible.
- ArviZ (posterior diagnostics, always paired with PyMC): Apache-2.0. Compatible.

No license blocker.

## What we should not adopt

- **TFP**: tied to TensorFlow. Out of stack.
- **Edward / Edward2**: subsumed. Out.
- **PyStan**: deprecated. Use CmdStanPy.
- **Pyro**: too DL-oriented. Out.

## Risks

1. **PyMC API drift.** Already burned the community on PyMC 3 → 4. The 5 → 6 migration was kinder but still required code edits. Pin the major version in `pyproject.toml` and budget for upgrades quarterly.

2. **NumPyro learning curve.** Composable-effects syntax is alien to people coming from PyMC or Stan. Mitigation: stick to the PyMC API and use NumPyro only as a sampler backend.

3. **MCMC failures on small panels.** Hierarchical BVAR across countries can have divergences when one country has very short data. Mitigation: per-country adapter checks, partial-pooling fallback.

4. **JAX install footprint.** The full JAX+CUDA stack is large. For Block I, CPU-only JAX is enough. GPU is a Block III problem.

5. **CmdStan toolchain.** CmdStanPy needs C++. Friction for Mac M-series ARM. Mitigation: provide a Docker image for replication.

## Verdict

**Grade A for PyMC.** This is the right pick for OPENGEM's L3 Bayesian needs and for any hierarchical scenario-probability work. Pair with NumPyro as a JAX backend for performance-critical models.

**Grade B for CmdStanPy.** Use for paper replication, not new model authoring.

**Skip everything else** in this loop's scope.

## Citations

- PyMC: https://github.com/pymc-devs/pymc (Apache-2.0)
- NumPyro: https://github.com/pyro-ppl/numpyro (BSD-3)
- CmdStanPy: https://github.com/stan-dev/cmdstanpy (BSD-3)
- PyMC Labs Stan benchmark (Feb 2026): https://www.pymc-labs.com/blog-posts/pymc-stan-benchmark
- Ingram MCMC comparison: https://martiningram.github.io/mcmc-comparison/
- PyMC BVAR example: https://www.pymc.io/projects/examples/en/latest/time_series/bayesian_var_model.html
- "PyMC: a modern, and comprehensive probabilistic programming framework in Python" PMC10495961

## Related

- [[L035]] — statsmodels + BVAR ecosystem (the substrate)
- [[L037]] — Kalman state-space libraries
- [[L038]] — BGVAR (cross-country, where PyMC's hierarchical BVAR shines)
- [[L189]] — BMA combiner over L3 variants (PyMC use case)
- [[L197]] — Scenario probability synthesis (PyMC use case)
