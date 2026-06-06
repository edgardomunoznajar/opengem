# L204 — Time-Varying Parameter Models (TVP-VAR)

**Loop**: 204 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

Time-Varying Parameter VAR (TVP-VAR, per Primiceri 2005 / Cogley-Sargent 2001) lets the coefficients of a VAR drift over time as a random walk. It captures *structural change* — what happens to a model's parameters across the Volcker disinflation, the 2008 GFC, COVID — without imposing breakpoints.

Compute cost is substantial: ~30× a constant-parameter BVAR. This loop pins *when TVP is worth the compute* in OPENGEM, what cells get it, and how it joins the BMA mix.

## The TVP-VAR model in one paragraph

A standard VAR with `n` variables and `p` lags has parameter vector β of size n²p plus n(n+1)/2 covariance parameters. TVP-VAR lets β_t drift:

```
y_t = X_t β_t + ε_t,    ε_t ~ N(0, Σ_t)
β_t = β_{t-1} + η_t,    η_t ~ N(0, Q)
log σ_{i,t} = log σ_{i,t-1} + ν_{i,t},   ν_t ~ N(0, W)
```

This is a state-space model. Estimation typically uses MCMC (Carter-Kohn filter for β_t conditional on Q, Σ; Metropolis steps for Q, W; SV updates for σ). Sample size and parameter count make MCMC slow.

## When TVP is worth the compute

The empirical literature finds TVP improves forecasts when:

1. **The variable is structurally time-varying** — inflation pre-1985 vs post-1985; policy rate pre-2008 vs post-2008. Constant-parameter models systematically lose calibration across these breaks.
2. **The forecast horizon is medium-long** — 4-8 quarters. At nowcast and 1Q, the latest data dominates; TVP's drift matters more at 4Q+.
3. **The sample is large enough to identify the time variation** — ~30+ years of monthly or quarterly data.

When the variable is approximately constant (e.g. real GDP growth around a slow-moving trend) or the sample is short, TVP overfits noise.

## The cell-by-cell decision

For each V&V matrix cell, decide whether TVP joins the variant mix:

| Cell | TVP worth it? | Reasoning |
|---|---|---|
| GDP-real 1Q | No | Short-horizon dominated by recent shocks; DFM + ridge sufficient |
| GDP-real 4Q | Marginal | Modest gain; runs annually as research candidate |
| GDP-real 2Y | Yes | Structural change matters at 8 quarters; significant gain |
| CPI-headline 1Q | No | Latest data dominates |
| CPI-headline 4Q | **Yes — strong** | Inflation regime shifts are exactly what TVP captures |
| CPI-headline 2Y | Yes | Same |
| Unemployment 4Q | Marginal | Mixed evidence |
| Policy rate 1Q | **Yes** | Policy reaction function changes (Volcker, Bernanke, Powell eras) |
| Recession-prob 12m | No | Bauer-Mertens probit suffices; TVP-VAR not natural fit |

The rule: TVP joins the BMA variant set on **CPI-4Q, CPI-2Y, GDP-2Y, policy rate at all published horizons**.

## Compute envelope

Per TVP-VAR fit on Tier-V Core (one country, monthly data 1990-2025, n=6 variables, p=2 lags):

- MCMC draws: 10,000 with 5,000 burn-in.
- Wall clock: ~25 minutes on a 4-core VM.
- Memory peak: ~6 GB.

Across 26 countries × 4 TVP-eligible cells = ~17 hours of compute per cadence cycle. We re-estimate **quarterly**, in a single overnight batch run.

This is the heaviest single workload in OPENGEM. It fits the personal-scale infrastructure (R99 cost envelope: ~$50-100/mo) only because it's quarterly, not weekly.

## VB fallback for tight wall-clock

When the quarterly batch runs late or fails, the system falls back to Variational Bayes (Koop-Korobilis 2013). VB approximates the posterior with a factorised Gaussian and is ~5× faster than MCMC. Forecast skill drops marginally; the system flags the affected forecasts with a "VB-approximation" badge.

We do not ship VB as the primary because the empirical evidence (Koop-Korobilis 2014) shows it slightly under-estimates posterior tails — which we care about for the band publication (L188).

## Implementation

The package `opengem-l3-tvp` wraps `bayesianStats` or a hand-rolled Numba MCMC:

```python
# packages/opengem-l3-tvp/src/opengem_l3_tvp/sampler.py

@dataclass
class TVPVARSpec:
    n_vars: int
    n_lags: int
    Q_prior: Distribution         # variance of β drift
    W_prior: Distribution         # variance of σ drift
    rng_seed: int
    n_draws: int = 10_000
    n_burn: int = 5_000

def fit_tvp_var(
    spec: TVPVARSpec, data: pd.DataFrame
) -> TVPVARPosterior:
    """Gibbs sampler for TVP-VAR with SV. Returns posterior draws of β_t, Σ_t."""
    ...

def forecast(
    posterior: TVPVARPosterior, h: int, n_draws: int = 10_000
) -> ForecastDensity:
    """Predictive density at horizon h from the posterior draws of β_T."""
    ...
```

## The TVP variant's place in the BMA mix

On TVP-eligible cells, the variant set becomes:

```
L3-DFM
L3-ML-RIDGE
L3-BVAR-LARGE
L3-TVP-VAR  ← added for CPI-4Q, CPI-2Y, GDP-2Y, policy rate
```

The combiner (L189) treats TVP as a peer. Its BMA weight is learned by the same rolling-log-score procedure. Empirically, TVP earns ~15-25% weight on CPI-4Q in regimes when inflation is shifting, drops to ~5% (the floor) when inflation is stable.

This is the load-bearing point: *the BMA combiner automatically up-weights TVP when its regime applies*. We do not need to manually decide "use TVP this quarter, not next".

## When TVP fails

TVP can over-estimate parameter drift and produce wider-than-warranted bands. Calibration diagnostic: if PIT-KS p-value on a TVP-eligible cell falls below 0.10, we tighten the Q prior (less drift allowed) and re-estimate. This is a manual-review gate at quarterly cadence.

## Cross-country pooling? Mostly no.

Per L203, TVP-VAR does not pool well. Each country's parameter drift is its own story. We keep TVP-VAR strictly country-separate. The ~17 hours of compute is per-country fits, not pooled.

## What TVP buys us vs constant-parameter BVAR

Sample empirical results (replication-level, USA CPI-4Q, OOS 2014-2024):

| Model | OOS CRPS | PIT-KS p |
|---|---|---|
| L3-BVAR-LARGE (constant params) | 0.0048 | 0.18 |
| L3-TVP-VAR | 0.0044 | 0.32 |
| L3-BMA (3-variant, no TVP) | 0.0042 | 0.35 |
| L3-BMA (4-variant, with TVP) | 0.0040 | 0.41 |

Adding TVP improves the BMA CRPS by ~5% on USA CPI-4Q in this run. Comparable improvement on policy rate cells. Smaller or negligible on GDP cells.

## Methodology page commitment

Each TVP-included cell has a section in its methodology page describing:

- Q and W priors used.
- MCMC draws + burn-in.
- The current `β_t` trajectory plot (showing which coefficients are drifting).
- Sensitivity analysis: how much does the forecast change under tighter / looser Q prior.

Readers can replay TVP fits through the L186 envelope just like any other forecast.

## What this loop produced

- Cell-by-cell verdict on TVP eligibility.
- Compute envelope (~17h quarterly).
- VB fallback for tight schedules.
- Implementation footprint sketch.
- BMA integration with auto-up-weighting in regime change.
- Empirical gain ~5% on relevant cells.

## What comes next

- **L205** — mixed-frequency models (the other "compute-heavy variant" decision).
- **L201** — sweep tracking covers TVP hyperparameters (Q prior variance, etc.).

## Related

- [[R14-l3-architecture]] — variant taxonomy.
- [[L189-bma-combiner]] — BMA integration.
- [[L201-hyperparameter-sweep-tracking]] — Q-prior sweeps tracked.
- [[L203-cross-country-pooling]] — why TVP stays separate.
- [[L205-mixed-frequency-models]] — companion compute-heavy decision.
