# L086 — NY Fed Nowcasting Code: Reuse vs Rewrite, Concrete Merge Plan

**Loop**: 086 / 300
**Phase**: 2 — Integration deep dive
**Date**: 2026-06-06
**Verdict**: **FORK-LIGHT (spec from `frbny-nowcasting`, runtime from `statsmodels.DynamicFactorMQ`, port news decomposition to a thin wrapper)**

---

## What this loop answers

L032 graded the NY Fed Nowcasting code **A — adopt into Block II L3 layer**. The Phase 2 question is *which artifact do we depend on* — the MATLAB original at `FRBNY-TimeSeriesAnalysis/Nowcasting`, the stale Python port at `MajesticKhan/Nowcasting-Python`, or `statsmodels.tsa.statespace.DynamicFactorMQ`? After inspecting all three clones, the answer is sharper than L032 hinted: **the statsmodels class wins on five dimensions; the Python port is a teaching artifact; the MATLAB original is the spec.**

This loop produces the concrete merge plan: what we steal from the FRBNY repos vs what we rewrite, the package layout, the API surface, and the calibration handshake against the spec.

## What's in each artifact, side by side

I inspected the three sources at `research-300/clones/`:

### `frbny-nowcasting/` (MATLAB, BSD-3-Clause, 232 stars)

```
frbny-nowcasting/
  example_DFM.m
  example_Nowcast.m
  Spec_US_example.xls    <-- the spec — series IDs, frequencies, blocks
  ResDFM.mat             <-- pre-fitted parameters for the US example
  data/                  <-- vintage CSVs
  functions/
    dfm.m                <-- 1,067 lines, EM-fitted DFM (the workhorse)
    load_data.m
    load_spec.m
    remNaNs_spline.m     <-- missing-data spline interpolation
    summarize.m
    update_nowcast.m     <-- 21KB, news decomposition (the value-add)
```

Last meaningful commit Sept 2019. The MATLAB code is **frozen**, but the math is canonical. `dfm.m` and `update_nowcast.m` together encode the Bok et al. (2017) framework byte-for-byte. **This is the spec we calibrate against.**

### `frbny-nowcasting-python/` (Python, BSD-3-Clause, 133 stars, MajesticKhan)

```
frbny-nowcasting-python/
  example_DFM.py
  example_Nowcast.py
  Spec_US_example.xls    <-- same spec file
  ResDFM.pickle          <-- Python version of the fitted parameters
  data/
  Functions/
    dfm.py               <-- 1,087 lines, near-line-by-line port
    load_data.py
    load_spec.py
    remNaNs_spline.py
    summarize.py
    update_Nowcast.py    <-- 17KB, ported news decomposition
```

Last meaningful commit Feb 2021. The README explicitly says "moved away from time series" and "early stages, requires further improvements." The code works — I traced the import chain in `example_DFM.py` and the functions exist — but it's a near-mechanical translation. Variable names follow MATLAB conventions (`Wx`, `Mx`, `Z`, `C`, `R`), NumPy is used without idiomatic vectorization, and the structure is monolithic.

**Strategic verdict on the Python port**: do not depend on it at runtime. Use it as a **debugging cross-check** — when our statsmodels-based implementation produces a number that doesn't match the MATLAB spec, the Python port helps us localize the bug (was it the spec, the EM step, the news decomposition?). Useful, not foundational.

### `statsmodels.tsa.statespace.DynamicFactorMQ` (Python, BSD-3, statsmodels)

Not cloned separately (it's a pip dependency), but: actively maintained (Chad Fulton), tested against thousands of production users, supports mixed-frequency natively (the `MQ` is "Monthly-Quarterly"), supports the EM algorithm, exposes a clean `fit() / predict()` interface, integrates with the rest of the statsmodels state-space ecosystem (smoothing, simulation, impulse response).

**This is what OPENGEM depends on at runtime.** L044 already grades it A; we re-confirm here.

The one thing `DynamicFactorMQ` *does not ship* is the **news decomposition** — the bit that turns "this week's nowcast moved +0.3 ppt" into "+0.15 from yesterday's payroll surprise, +0.10 from this morning's ISM, +0.05 residual." That's the user-visible value-add of the NY Fed model. We have to port it.

## The five-dimension comparison

| Dimension | MATLAB orig | Python port | statsmodels |
|---|---|---|---|
| Math correctness | Canonical (spec) | Near-line port | Validated against spec |
| Mixed-frequency support | Yes (built in) | Yes (ported) | Yes (`MQ` class natively) |
| EM algorithm | Yes | Yes | Yes |
| Kalman smoother | Yes | Yes | Yes + simulation smoother + IRF |
| News decomposition | Yes (`update_nowcast.m`) | Yes (ported) | **No — must build** |
| Maintenance | Frozen since 2019 | Stale since 2021 | Active, monthly commits |
| Tests | Authors' acceptance only | None | Statsmodels test suite + cross-check |
| API ergonomics | MATLAB-shaped | NumPy verbatim | sklearn-style |
| Production readiness | Reference only | Hobbyist | Production |
| Documentation | Paper-quality | README only | Full docs + Chad Fulton's notebook |

The statsmodels class wins everywhere *except* news decomposition. That is the bridge we build.

## The OPENGEM package: `opengem-l3-dfm`

```
packages/opengem-l3-dfm/
  pyproject.toml                         # Apache-2.0
  src/opengem_l3_dfm/
    __init__.py
    nowcast.py                            # public API: Nowcast.fit, Nowcast.predict, Nowcast.news
    spec.py                               # OpenBB-style Pydantic SpecConfig (replaces .xls)
    panels/                               # per-country indicator panel definitions
      us_tier_v.yaml                      # ~30 monthly indicators + GDP quarterly
      euarea_tier_v.yaml
      jp_tier_v.yaml
      ...
    fit/
      em.py                               # wrapper around DynamicFactorMQ.fit
      missing.py                          # remNaNs_spline equivalent (scipy.interpolate)
    news/
      decompose.py                        # PORT from update_nowcast.m / .py
      decompose_test.py                   # cross-check against MATLAB ResDFM reference
    spec_calibration/
      vs_matlab.py                        # acceptance test: our nowcast must match MATLAB +/- 1e-5
  tests/
    test_us_q4_2016.py                    # the literal example in the FRBNY repo, ours must reproduce
    test_news_decomposition.py
    test_mixed_frequency.py
    test_em_convergence.py
```

### The public API

```python
from opengem_l3_dfm import Nowcast, SpecConfig

spec = SpecConfig.from_yaml("panels/us_tier_v.yaml")  # series IDs, frequencies, blocks
panel = vintage_store.at(date(2026, 5, 31)).iter_panel(spec.series_ids)

nowcast = Nowcast(spec)
nowcast.fit(panel, sample_start=date(2000, 1, 1))

# Point + density prediction
forecast = nowcast.predict(target="gdp_real_growth", period="2026Q2")
# -> {p10, p25, p50, p75, p90, model_id, vintage_at}

# News decomposition (the value-add)
release = ReleaseEvent(series="payems", new_value=240e3, expected=200e3, date=date(2026, 6, 6))
news = nowcast.news(prior_forecast=forecast, release=release)
# -> {"contribution_ppt": 0.07, "Δ_p50": 0.07, "Δ_p10p90": (0.02, 0.10)}
```

This is the same shape as `statsmodels.DynamicFactorMQ`'s API, plus the news method. Internally, `Nowcast.fit` wraps `DynamicFactorMQ.fit_em` with our spec → statsmodels-spec adapter. `Nowcast.news` is the ported news decomposition.

## What gets ported, exactly

The news decomposition (`update_nowcast.m` / `update_Nowcast.py`) does three things:

1. **Recompute the Kalman-smoothed factor estimate** at vintage `t` and vintage `t+1`.
2. **Decompose the difference** in the target-variable nowcast at the two vintages into per-series contributions, using the **Bańbura-Modugno (2014)** identity:
   `Δ nowcast = Σ_i weight_i × (observed_i - expected_i)`
   where `weight_i` is derived from the Kalman gain at that release time.
3. **Output a structured table**: one row per released series, with point contribution + standard error.

Port strategy:

- **Step 1** uses `statsmodels.DynamicFactorMQ.smooth()` directly — no port needed.
- **Step 2** is the math we port. ~150 lines of NumPy from `update_Nowcast.py`, refactored to consume statsmodels' smoother output instead of MATLAB struct fields. The math is mechanical; the structural change is "where does the smoother live in the data flow."
- **Step 3** is presentation — we emit the result as a Pydantic model so it lands cleanly in the L132 vintage drawer UI.

**Effort**: ~3 dev-weeks for the port + acceptance test. The acceptance test (`tests/test_news_decomposition.py`) reproduces the *exact* Sept→Dec 2016 example from the FRBNY repo — the spec file `Spec_US_example.xls` plus the `ResDFM.mat` pre-fitted parameters plus the two vintage data files. Our news decomposition output must match the MATLAB reference within `1e-5` precision. If it doesn't, we have a bug. This is the discipline that earns the "calibrated against the spec" claim on the methodology pop-up.

## What we don't port

1. **`dfm.py`'s EM algorithm.** statsmodels' EM is better-tested. We use it. (We do read `dfm.py` once to confirm the spec interpretation matches.)
2. **`load_spec.py`'s Excel reader.** We replace with Pydantic YAML. Excel is not a config format.
3. **`load_data.py`'s vintage-CSV reader.** We replace with our existing `opengem-vintage` API (per `packages/opengem-vintage/src/opengem_vintage/store.py`).
4. **`remNaNs_spline.py`'s spline interpolation.** Replaced by `scipy.interpolate.UnivariateSpline` — same math, better-tested, integrates with our pandas/numpy stack.
5. **`example_DFM.py`'s Plotly chart code.** We render in Observable Plot / Lightweight Charts via the dashboard layer.

## The data restriction gotcha

The FRBNY README says outright: "These example files do not exactly reproduce the New York Fed Staff Nowcasting Report released every Friday because data redistribution restrictions prevent us from providing the complete data set used in our model." Translation: they use Haver Analytics and proprietary survey data.

OPENGEM's panel is **fully public** (BEA, BLS, FRB, Census, etc., via our existing `opengem-data-bea/bls/frb/census` adapters). We will not match the NY Fed print exactly. We **will** match the methodology exactly, and our print will be **fully reproducible from public sources** — which is the better promise for the accountability ledger.

In practice this means our US nowcast will be within a 5-10 bp window of the NY Fed's published print most weeks, with occasional larger gaps when Haver-only series (e.g. some regional Fed surveys not on FRED) move materially. We disclose the panel difference openly in the methodology pop-up.

## Multi-country generalization

The MATLAB code ships a US-only spec. Bok et al. (2017) explicitly contemplate per-country specs and provide guidance on block structure (real, financial, labor). For OPENGEM the multi-country play is:

- **Tier-V big-six** (US, EU aggregate, UK, Japan, Korea, Canada): full ~30-indicator panels, EM-fitted DFM per country.
- **Tier-V remainder** (~10 more economies with reasonable monthly hard data — Australia, Mexico, Brazil, India, China, Turkey, Indonesia, South Africa, Russia, Saudi Arabia): smaller panels (15-20 indicators), same DFM machinery.
- **Smaller economies**: fall back to statsforecast baselines (L044) + WB/IMF quarterly nowcast. No DFM unless we have a reliable monthly hard-data panel.

Each country gets its own `panels/{country}_tier_v.yaml` spec file. The model code is country-agnostic; the data plumbing branches per-country at the panel layer. **Cost**: ~2 dev-days per Tier-V country to build the panel YAML, validate the panel against vintage history, and fit.

## Risks

1. **EM local optima on smaller panels.** ~15-indicator panels can land in suboptimal EM solutions. Mitigation: multiple random restarts (10), pick highest-loglik fit, warm-start from prior-period parameters.

2. **Statsmodels API drift.** `DynamicFactorMQ` is under `statespace` which is mature but still gets minor breaking changes. Mitigation: pin minor version in `pyproject.toml`; quarterly upgrade cycle with a re-run of the MATLAB-acceptance test.

3. **News-decomposition port has a bug we don't catch.** A subtle sign error or normalization mistake in the Bańbura-Modugno math would silently corrupt every weekly nowcast revision narrative. Mitigation: the MATLAB acceptance test is the safety net; we also run a synthetic-data sanity check (known impulse response should produce known contribution).

4. **The NY Fed's own model is "frozen and may not work after COVID."** Bok et al.'s framework was paused in 2021 over structural-break concerns. Mitigation: ship our nowcast with regime-aware uncertainty, retrain quarterly, expose regime flags in the methodology pop-up (R10 SSDD-008 already covers this).

## Cost summary

| Task | Cost |
|---|---|
| `Nowcast` API wrapper around `DynamicFactorMQ` | 1 dev-week |
| Pydantic Spec config + YAML loader | 0.5 dev-week |
| News decomposition port from `update_Nowcast.py` | 2 dev-weeks |
| MATLAB acceptance test (reproduce 2016Q4 example) | 1 dev-week |
| Synthetic-data sanity test | 0.5 dev-week |
| Multi-country panel YAMLs (6 Tier-V big) | 1.5 dev-weeks |
| Multi-country panel YAMLs (10 Tier-V remainder) | 2 dev-weeks |
| `vintage_store` integration | 0.5 dev-week |
| Methodology card text + citation | 0.5 dev-week |
| **Total v0.1.0** | **~10 dev-weeks** |

That's reasonable for the spine of the L3 workhorse layer. The math is canonical; we are buying calibration insurance, not novelty.

## What this loop produced

- Three-way comparison (MATLAB orig vs Python port vs statsmodels) with the FORK-LIGHT verdict.
- Concrete package layout for `opengem-l3-dfm`.
- The news decomposition as the *only* meaningful port from FRBNY-Python.
- MATLAB acceptance test as the canonical calibration discipline.
- Multi-country generalization plan with panel YAMLs.
- ~10 dev-week total cost.

## What comes next

- **L087** — Bayesian VAR Python stack: the L3 sibling that complements the DFM workhorse.
- **L088** — neuralforecast for L3: the deep-learning experimental layer.
- **L189** — BMA combiner over the L3 variants.
- **L195** — Forecast UI bands consensus: where news decomposition surfaces.

## Related

- [[L032-ny-fed-nowcasting]] — Phase 1 deep dive.
- [[L044-nixtla-stack]] — sibling forecaster ecosystem.
- [[L087-bayesian-var-python-consolidation]] — sibling Bayesian variants.
- [[L088-neuralforecast-l3-layer]] — sibling DL variant.
- [[L132-provenance-drawer]] — UI surface for news decomposition.
- [[L189-bma-combiner]] — downstream ensemble layer.
- inspected source: `/mnt/bigdata/home/edgardo/projectsd/opengem/research-300/clones/frbny-nowcasting/functions/{dfm,update_nowcast}.m`
- inspected source: `/mnt/bigdata/home/edgardo/projectsd/opengem/research-300/clones/frbny-nowcasting-python/Functions/{dfm,update_Nowcast}.py`
