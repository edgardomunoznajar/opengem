# L189 — Combiner: BMA over L3 Variants

**Loop**: 189 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

The L3 workhorse layer carries multiple model variants — DFM, ML-residual (ridge / gradient boost), large BVAR, sometimes a TVP-VAR or MF-DFM. The combiner produces a single density per `(country, indicator, horizon, vintage)` that the dashboard publishes.

R99 §2.2 commits: "BMA over L3 variants." This loop pins the mathematical contract and the implementation footprint. It does not re-litigate the BMA choice (see L202 for the stacking alternative under consideration for v2.0).

## The mathematical contract

Let `f_k(y | I_t)` be the predictive density from model variant `k ∈ {1, …, K}` conditional on the information set `I_t` at vintage time `t`. The BMA predictive density is:

```
f_BMA(y | I_t) = Σ_k w_k(t) × f_k(y | I_t)
```

with weights `w_k(t)` normalised so Σ w_k = 1, w_k ≥ 0. The combiner is a finite mixture; if each component is Gaussian (the common case), the result is a Gaussian mixture, with closed-form moments and quantiles obtainable by numerical inversion.

The weights are *time-varying*. They reflect the rolling log-score performance of each variant over a recent window:

```
w_k(t) ∝ exp( Σ_{s=t-W..t-1} log f_k(y_s | I_s) )
```

This is the canonical posterior-update formula under the "model averaging" interpretation with equal prior on each variant. `W` is the window length — we default to 40 quarters (10 years) for stable variants and 20 quarters (5 years) for newer variants. Window length is a per-indicator policy choice, version-pinned per combiner epoch.

## The variants in scope at IOC

Per R03 / R14, the L3 layer ships with three variants at Initial Operating Capability:

1. **L3-DFM** — Dynamic Factor Model on a large `(country, frequency)` panel (Stock-Watson, Forni-Hallin-Lippi tradition). Strength: nowcast + 1Q. Weakness: drifts at longer horizons.
2. **L3-ML-RIDGE** — Ridge regression on engineered features (lags, BVAR-implied factors, term spreads, GSCPI, GPR). Strength: 4Q. Weakness: opaque coefficients.
3. **L3-BVAR-LARGE** — Bayesian VAR with Minnesota-style prior on 30-40 variables, per Banbura-Giannone-Reichlin. Strength: 2Y + structural coherence. Weakness: compute-heavy.

Variants 4-5 (added in Block II per R21):

4. **L3-TVP-VAR** — Time-Varying Parameter VAR (Primiceri 2005, Cogley-Sargent 2001), only when warranted by data (L204).
5. **L3-MF-DFM** — Mixed-Frequency DFM for the nowcast horizon specifically (L205).

The combiner does not include L1 (US semi-structural) or L2 (BGVAR) in the variant set. Those serve different jobs (narrative + scenario, respectively); they do not enter the BMA average.

## The weight estimation procedure

For each `(country, indicator, horizon)`:

```python
def bma_weights(
    log_scores_history: np.ndarray,  # shape (K variants, T past quarters)
    window: int = 40,
    floor: float = 0.05,
) -> np.ndarray:
    """Return BMA weights w_k. Latest W observations only."""
    recent = log_scores_history[:, -window:]
    summed = recent.sum(axis=1)
    # Numerical-stable softmax
    shifted = summed - summed.max()
    raw = np.exp(shifted)
    raw /= raw.sum()
    # Floor to prevent zero-weighting: keeps "humility" for cold model
    raw = raw + floor
    raw /= raw.sum()
    return raw
```

The **floor of 5% per variant** is the key implementation choice. Without it, a recently-poor-performing variant can have its weight crushed to zero, and then never recover even if it would have been the right model for a future regime. The floor preserves a minimum probability of resurrection. In ensemble-learning vocabulary, the floor is regularisation against weight collapse.

## Numerical conditions for mixing Gaussian components

A Gaussian-mixture predictive density:

```
f(y) = Σ_k w_k × N(y; μ_k, σ_k²)
```

Moments:

```
E[y]    = Σ_k w_k × μ_k
Var[y]  = Σ_k w_k × (σ_k² + μ_k²) - (E[y])²
```

Variance has two terms: the within-component variance (Σ w_k σ_k²) and the between-component variance (the spread of means around their average). When variants disagree, the BMA density widens. This is *correct* — disagreement is uncertainty.

Quantiles are obtained by numerical inversion of the mixture CDF:

```python
def mixture_quantile(weights, means, sds, q):
    def cdf(y):
        return sum(w * norm.cdf(y, m, s) for w, m, s in zip(weights, means, sds))
    return brentq(lambda y: cdf(y) - q, lo, hi)
```

This is fast: O(K) per CDF evaluation, ~20 iterations of Brent's method. We cache the quantile vector on the forecast object so the dashboard never re-computes.

## When the components are non-Gaussian

Some L3 variants emit non-Gaussian predictives (e.g. a ML model that returns sample draws directly, or a stochastic-volatility BVAR with t-distributed errors). The combiner handles this by:

1. Drawing N=10,000 samples from each component.
2. Mixture-sampling with the BMA weights: draw component k with probability w_k, then draw y from f_k.
3. The resulting empirical sample is the BMA predictive density.

Quantiles come from the empirical CDF; CRPS computes against the empirical sample. This is slower per call but a single forecast costs ~0.1 second, so the cost is negligible against the operational cadence.

## Implementation footprint

```
packages/opengem-combiner/
├── pyproject.toml
├── src/opengem_combiner/
│   ├── __init__.py
│   ├── bma.py                  # BMA weight computation
│   ├── mixture.py              # Gaussian mixture maths
│   ├── sampling.py             # Empirical mixture for non-Gaussian
│   ├── weights_store.py        # Persistent weight cache (per cell)
│   └── epoch.py                # Epoch pinning per L184/R25
├── tests/
│   ├── test_bma_weights.py
│   ├── test_mixture_moments.py
│   ├── test_quantile_inversion.py
│   ├── test_weight_floor.py
│   ├── test_replay_determinism.py
│   └── data/                   # Fixture log-score histories
└── docs/
    └── methodology.md
```

Expected size at IOC: ~800 LOC, ~250 lines of tests. Single dev-week to write; the maths is classical; the work is glue, not invention.

## The weights' own provenance

BMA weights are themselves an *artefact* that needs versioning. Per cell `(country, indicator, horizon)` we store:

```json
{
  "schema": "opengem.bma_weights.v1",
  "cell": {"country": "USA", "indicator": "GDP-real-yoy", "horizon_q": 4},
  "epoch": "2026-Q2",
  "computed_at": "2026-04-01T00:00:00Z",
  "window_quarters": 40,
  "log_score_floor": 0.05,
  "variants": [
    {"id": "L3-DFM-v1.2", "weight": 0.41, "log_score_sum": -38.2},
    {"id": "L3-ML-RIDGE-v1.4", "weight": 0.34, "log_score_sum": -38.9},
    {"id": "L3-BVAR-LARGE-v2.0", "weight": 0.25, "log_score_sum": -39.7}
  ],
  "weights_sha256": "sha256:..."
}
```

This artefact is referenced from the forecast.v1 `density.components[].model_id`. A reader can ask "why was DFM weighted 41%?" and follow the chain back to the log-score history.

## Combiner cadence

Weights are recomputed **monthly** for each cell — at the start of each month, using the prior month's log-score updates. Weekly updates are noisy; monthly is the right operating rhythm. We re-publish weights immediately to the weights store; in-flight forecasts use the latest weights at the moment of forecast generation.

Epoch boundaries (e.g. annual, or when a new variant is added) trigger a full recomputation with explicit version bump.

## What this loop produced

- The BMA mathematical contract restated.
- Weight estimation with explicit 5% floor.
- Gaussian-mixture moment formulas.
- Non-Gaussian fallback via empirical sampling.
- Implementation footprint (~800 LOC).
- Weight provenance schema.
- Monthly recomputation cadence.

## What comes next

- **L202** — stacking as an alternative weight-learner.
- **L207** — density-aggregation rules across multiple components and indicators.
- **L201** — sweep tracking when tuning the floor / window.

## Related

- [[R14-l3-architecture]] — variants this combines.
- [[L181-forecast-object-schema]] — `density.components` reflects the BMA mixture.
- [[L202-stacking]] — alternative learner.
- [[L207-density-aggregation]] — multi-variable aggregation.
- [[R25-leaderboard-algorithm]] — epoch policy.
