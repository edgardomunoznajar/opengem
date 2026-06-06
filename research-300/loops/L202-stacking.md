# L202 — Ensemble Weighting via Stacking

**Loop**: 202 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

BMA over L3 variants (L189) is the IOC combiner. Stacking is the alternative. Stacking treats the variant outputs as inputs to a *meta-learner* trained on held-out data: instead of weights derived from rolling log-scores, weights (or arbitrary functions of variant predictions) are learned by regression / classification on a held-out fold.

This loop pins the methodology, the implementation footprint, the trade-off against BMA, and the path to ship stacking in epoch 2 (post-IOC).

## What stacking is

Given K variant predictive densities `f_k(y | I_t)` for k = 1..K, stacking learns weights `w` by solving a meta-regression on held-out data:

```
ŵ = argmin_w Σ_t L( y_t, Σ_k w_k × f_k(y | I_t) )
```

with `L` a loss function. Common choices:

- **Stacking with log-score loss**: `L = -log Σ_k w_k f_k(y_t)`. Recovers BMA-like updates but trained on holdout.
- **Stacking with CRPS loss**: `L = CRPS(Σ_k w_k F_k, y_t)`. Directly optimises the leaderboard metric.
- **Generalised stacking**: learn `f_meta(y | f_1, ..., f_K)` via a flexible model (Gaussian Process, gradient boosting on the K variant moments, etc.).

Weights are constrained to the simplex (Σ w_k = 1, w_k ≥ 0) for interpretability, or unconstrained for arbitrary mixing (then no longer a strict probability mixture; requires re-normalising at the density level).

## Stacking vs BMA

| Property | BMA (L189) | Stacking (this loop) |
|---|---|---|
| Weight derivation | Rolling log-score, exponential softmax | Optimisation on held-out OOS fold |
| Loss function | Log score (implicit) | Chosen explicitly (typically CRPS) |
| Calibration | Mixture inherits calibration if components are calibrated | Held-out optimisation can degrade tail calibration |
| Robustness to bad variant | Floor at 5% (L189) | Risk of overfitting to dominant variant if floor not enforced |
| Direct optimisation of leaderboard metric | No (optimises log-score) | Yes (if CRPS loss chosen) |
| Compute | Cheap (closed-form weights) | Moderate (one numerical optimisation per cell per cadence) |
| Interpretability | "How much OOS log-score does each variant earn?" | "Weights learned to minimise CRPS on holdout" |

The literature (Hall-Mitchell 2007; Geweke-Amisano 2011; Pauwels et al. 2019) generally finds stacking with CRPS loss outperforms BMA in macro forecasting when (a) there are 3+ variants with meaningful diversity and (b) the holdout window is ≥ 30 observations.

## Implementation

Per V&V matrix cell `(country, indicator, horizon)`, the stacking pipeline is:

```python
def stacking_weights(
    variants: list[Variant],
    train_oos_window: tuple[date, date],
    holdout_oos_window: tuple[date, date],
    loss: str = "crps",
    constraint: str = "simplex",
) -> dict[str, float]:
    """
    Learn stacking weights on holdout data.

    Train_window: variants' predictive densities + realised outcomes (training fold).
    Holdout_window: variants' predictive densities + realised outcomes (held-out fold).
    """
    # 1. Pull variant predictive densities + realised outcomes at each scoring period
    train_data = pull_variant_predictions(variants, train_oos_window)
    holdout_data = pull_variant_predictions(variants, holdout_oos_window)

    # 2. Define the meta-objective
    def objective(w):
        mixture = sum(w[k] * train_data.densities[k] for k in range(len(variants)))
        return sum(CRPS(mixture, train_data.realised[t]) for t in train_data.t) / len(train_data.t)

    # 3. Constrained optimisation (SLSQP for simplex)
    result = minimize(
        objective,
        x0=np.ones(len(variants)) / len(variants),
        method="SLSQP",
        constraints=[
            {"type": "eq", "fun": lambda w: w.sum() - 1.0},  # Σw = 1
        ],
        bounds=[(0.05, 0.95)] * len(variants),  # floor at 5%, ceiling at 95%
    )

    weights = {variants[k].id: result.x[k] for k in range(len(variants))}

    # 4. Evaluate on holdout for sanity
    holdout_crps = ...  # for reporting

    return StackingResult(weights=weights, holdout_crps=holdout_crps, train_crps=result.fun)
```

The optimiser runs in ~30 seconds per cell on the baseline VM. Full Tier-V Core × 17 cells × 26 countries = ~440 optimisations per re-fit. Fits in 2 hours of compute, run quarterly.

## Why the simplex constraint

Unconstrained weights produce mixtures that:

- May not be densities (negative weights → non-density mixtures).
- Are harder to interpret ("the BVAR variant has weight 1.3 and the DFM variant has weight -0.4" reads poorly to non-experts).
- Risk extreme overfit on small holdouts.

Simplex weights stay interpretable and admit honest "the mixture is 41% BVAR, 34% DFM, 25% ridge" framing.

## The holdout split rule

Per cell:

| Fold | Years | Use |
|---|---|---|
| Train OOS | 2014-2019 | Stacking weight learning |
| Holdout OOS | 2020-2023 | Verify weights generalize |
| Production OOS | 2024-present | Leaderboard scoring |

Critical: the leaderboard scoring window must *not* overlap the stacking training fold. Otherwise we leak signal. The L184 leaderboard window is sliced to 2024+ only when stacking weights have been learned on 2014-2019.

When a new year of OOS data accumulates (2025 done; 2026 starts):

1. The train OOS window stays fixed at 2014-2019.
2. The holdout extends (2020-2024 now).
3. The production OOS window expands by one year.

Annual cadence; no continuous retuning.

## Calibration of stacked densities

Stacked mixtures inherit calibration if and only if components are calibrated *on the train fold*. A poorly-calibrated component being weighted highly can degrade overall PIT.

Defence: after weight learning, immediately re-run PIT-KS on the stacked density on the holdout fold. If PIT-KS fails on the holdout but passed on the train, we have overfitting. In that case, increase the floor on each weight (e.g. floor=0.10 instead of 0.05) and re-optimise.

## Comparison to BMA in expected production

Plausible weight set on a sample cell (USA GDP-4Q):

| Variant | BMA weight (rolling log-score) | Stacking weight (CRPS loss, holdout) |
|---|---|---|
| L3-DFM | 0.41 | 0.38 |
| L3-ML-RIDGE | 0.34 | 0.42 |
| L3-BVAR-LARGE | 0.25 | 0.20 |
| Holdout CRPS | 0.0042 | 0.0040 |

Stacking shifts weight away from BVAR (which is calibrated but tail-heavy) toward Ridge (which has lower CRPS on the holdout). ~5% improvement on the headline metric. Worth shipping.

## The version-pinning

Stacking weights are versioned per cell per epoch, written to the same weights store as BMA:

```json
{
  "schema": "opengem.stacking_weights.v1",
  "cell": {"country": "USA", "indicator": "GDP-real-yoy", "horizon_q": 4},
  "epoch": "v2.1-2026Q4",
  "computed_at": "2026-10-01T00:00:00Z",
  "method": "stacking_crps_simplex",
  "train_window": "2014-Q1..2019-Q4",
  "holdout_window": "2020-Q1..2023-Q4",
  "loss_function": "crps",
  "constraints": {"simplex": true, "floor": 0.05, "ceiling": 0.95},
  "variants": [
    {"id": "L3-DFM-v1.2", "weight": 0.38, "holdout_solo_crps": 0.0047},
    {"id": "L3-ML-RIDGE-v1.4", "weight": 0.42, "holdout_solo_crps": 0.0046},
    {"id": "L3-BVAR-LARGE-v2.0", "weight": 0.20, "holdout_solo_crps": 0.0051}
  ],
  "stacked_holdout_crps": 0.0040,
  "stacked_holdout_pit_ks_pvalue": 0.36,
  "weights_sha256": "sha256:..."
}
```

## Shipping path

| Phase | Deliverable | Timeline |
|---|---|---|
| Phase 0 — IOC | BMA only (L189). | ✓ Block I |
| Phase 1 — Comparison | In parallel to production BMA, stacking is computed offline on Tier-V Core. Holdout CRPS published as research artefact. | Q3 2026 |
| Phase 2 — Shadow ship | Stacked density published *alongside* BMA density. Dashboard shows toggle "BMA / Stacking". User study + audit. | Q4 2026 |
| Phase 3 — Production switch | If stacking holdout CRPS beats BMA on ≥75% of cells, leaderboard ranking switches to stacked. BMA archived as the comparison baseline. | Q1 2027 |

## What this loop produced

- Methodology: stacking with CRPS loss + simplex constraint.
- Comparison table BMA vs stacking.
- Implementation sketch (~50 LOC core).
- Holdout split rule with no leaderboard leak.
- Weight schema.
- Three-phase shipping path to ship in epoch v2.1.

## What comes next

- **L207** — density aggregation rules across multiple variables.
- **L189** — BMA companion.

## Related

- [[L189-bma-combiner]] — IOC combiner.
- [[L184-leaderboard-ranking]] — leaderboard at risk of leak.
- [[L201-hyperparameter-sweep-tracking]] — sweep history feeds stacking candidate pool.
- [[L207-density-aggregation]] — companion problem.
- [[R14-l3-architecture]] — variants.
- [[R24-backtest-engine]] — backtest engine that produces holdout predictions.
