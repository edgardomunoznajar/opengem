# L183 — Forecast Scoring: Canonical Tuple per Indicator Class

**Loop**: 183 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

Pick the canonical scoring tuple per indicator class. Different indicator classes want different primary metrics. A one-size-fits-all rule (e.g. "everything is scored by CRPS") gives the wrong answer for discrete or bounded indicators. This loop fixes the mapping.

## The candidate metrics

| Metric | What it measures | Strength | Weakness |
|---|---|---|---|
| **CRPS** (Continuous Ranked Probability Score) | Distance between forecast CDF and observation | Proper scoring rule; rewards both calibration and sharpness; bounded; interpretable in units of the variable | Less sensitive than log-score to tail behaviour; CRPS of zero only at point mass |
| **Log score** (negative log predictive density) | -log f(y) at the realised y | Proper; the only *local* proper scoring rule; severely penalises overconfident tails | Unbounded (single tail miss can dominate); fragile with discrete densities |
| **PIT** (Probability Integral Transform) | Uniformity of u_t = F_t(y_t) under H0 of correct conditional density | Diagnostic for calibration; visualisable as PIT histogram | Not a single score; needs a uniformity test (KS, Berkowitz) |
| **MAE** | mean abs(y - point) | Robust; interpretable | Point-only; ignores density |
| **RMSE** | sqrt(mean (y - point)²) | Classical; penalises large errors | Point-only; sensitive to outliers; not proper for densities |
| **Hit-rate** | fraction y ∈ [P10, P90] | Coverage check | Single coarse number; ignores width |
| **AUC / Brier** | for binary/probability indicators (recession) | Standard for binary classification | Inappropriate for continuous indicators |
| **Diebold-Mariano** | Pairwise comparison test | Tells you whether one forecast is *significantly* better than another | Not a score itself; only relative |

## The canonical tuple

A scoring tuple is `(primary_metric, calibration_test, robustness_check, comparison_test, headline_metric)`. The first four are the technical artefacts; the fifth is what the dashboard headline shows non-technical readers.

| Indicator class | Primary | Calibration | Robustness | Comparison | Headline |
|---|---|---|---|---|---|
| **Continuous, density** (GDP growth, CPI YoY, UR, policy rate, BoP %GDP) | **CRPS** | PIT-KS | MAE | DM-HLN | "vs AR(1) CRPS win-rate" |
| **Continuous, point-only** (legacy benchmarks that don't publish densities; consensus, WEO) | MAE | n/a | RMSE | DM-HLN | "MAE" |
| **Binary/probability** (recession-12m, banking-stress, sovereign-default-12m) | **Log-score** | Reliability diagram | Brier | DM | "AUC vs Bauer-Mertens" |
| **Bounded [0,1]** (PMI normalised, business-conditions index) | **CRPS** | PIT-KS | MAE | DM-HLN | "vs AR(1) CRPS win-rate" |
| **Count / non-negative** (initial-claims, bankruptcy filings) | Log-score (negative binomial pred density) | PIT (randomised) | MAE | DM | "vs AR(1) RMSE" |
| **Categorical** (recession state classifier, regime label) | **Log-score** + Brier | Reliability per class | Accuracy | DM | "multinomial log-loss" |

### The headline canonical tuple, stated once

> **For the dominant indicator class (continuous density forecasts) the canonical scoring tuple is `(CRPS, PIT-KS, MAE, DM-HLN)` with the headline metric being the CRPS win-rate against AR(1).**

This is the answer the V&V matrix (R08) is graded against; this is the leaderboard ordering rule (L184); this is what the dashboard chart hover renders next to each forecast.

## Why CRPS as the workhorse

Three reasons:

1. **Proper.** No model can game it by tilting its density. Honest probabilistic forecasts get a lower CRPS than dishonest ones in expectation.
2. **Interpretable.** CRPS for a point mass at the realised value is zero. For a wider density, CRPS grows linearly in the standard deviation. Readers can compare CRPS in *units of the variable* — a CRPS of 0.4 percentage points on a CPI forecast has a directly intuitive meaning, where a log-score number does not.
3. **Robust.** Unlike log-score, CRPS does not blow up on single tail-miss observations. With ~40 forecasts per `(country, variable, horizon)` cell over the V&V window, CRPS converges to a stable estimate. Log-score in the same regime can be dominated by one bad observation.

We *also* compute log-score and report it (for power-users who want the calibration-of-tails signal); but CRPS is the primary, the ranking metric, and the leaderboard ordering rule.

## Why PIT-KS not Berkowitz

Berkowitz tests are more powerful when the alternative is a specific parametric mis-specification (e.g. wrong variance). PIT-KS makes a weaker assumption (uniform vs. anything) but is easier to communicate. Calibration is reported via:

1. **PIT histogram per `(country, variable, horizon)`** — visualisable directly (L193).
2. **KS p-value** with the null that PIT values are U[0,1].
3. **Pass/fail boolean** at α=0.05 for the V&V matrix.

A failed PIT-KS does not invalidate the forecast (the forecast still has a CRPS), but it shows up on the dashboard with a "calibration: warning" badge and a pointer to the methodology note.

## Why DM-HLN

The Diebold-Mariano test compares loss-differential paths between two forecasters. The Harvey-Leybourne-Newbold (HLN) small-sample correction matters because our OOS windows per cell are not huge (typically 40-150 observations). Reporting:

- DM stat with HLN correction.
- Two-sided p-value.
- "Not worse" verdict at α=0.10 (more permissive than typical because we are comparing against high-quality competitors like WEO).

For pairwise model-vs-model on the same cell we also compute the Model Confidence Set (MCS, Hansen-Lunde-Nason 2011) at α=0.10. The MCS gives a *set* of models that cannot be statistically distinguished from the best — that set is the leaderboard's "tied at top" badge.

## Hit-rate as the consumer-facing back-up

For non-technical readers, the dashboard chart hover shows: "OPENGEM's forecast bands have covered the actual outcome **82% of the time** at the 80% nominal level over 2014-2025." This is the hit-rate. It is *consumer-facing* and *not* the primary metric. The technical scoring lives in CRPS+PIT+DM; the human-friendly badge lives in hit-rate.

## Implementation contract

```python
# packages/opengem-scoring/src/opengem_scoring/canonical.py

CANONICAL_TUPLES: dict[IndicatorClass, ScoringTuple] = {
    IndicatorClass.CONTINUOUS_DENSITY: ScoringTuple(
        primary="crps",
        calibration="pit_ks",
        robustness="mae",
        comparison="dm_hln",
        headline="crps_vs_ar1_winrate",
    ),
    IndicatorClass.BINARY_PROB: ScoringTuple(
        primary="log_score",
        calibration="reliability_diagram",
        robustness="brier",
        comparison="auc_diff",
        headline="auc_vs_bauer_mertens",
    ),
    IndicatorClass.CONTINUOUS_POINT: ScoringTuple(
        primary="mae",
        calibration=None,
        robustness="rmse",
        comparison="dm_hln",
        headline="mae",
    ),
    IndicatorClass.COUNT: ScoringTuple(
        primary="log_score",
        calibration="randomised_pit_ks",
        robustness="mae",
        comparison="dm",
        headline="rmse_vs_ar1",
    ),
    IndicatorClass.CATEGORICAL: ScoringTuple(
        primary="log_score",
        calibration="reliability_per_class",
        robustness="accuracy",
        comparison="dm",
        headline="log_loss",
    ),
}

def score_forecast(fcst: ForecastV1, observed: float | int | str) -> CellScore:
    cls = classify_indicator(fcst.indicator)
    tup = CANONICAL_TUPLES[cls]
    primary = METRICS[tup.primary](fcst.density, observed)
    calib = METRICS[tup.calibration](fcst.density, observed) if tup.calibration else None
    robust = METRICS[tup.robustness](fcst.point, observed)
    return CellScore(primary=primary, calibration=calib, robustness=robust)
```

## What this loop produced

- Five-by-five table mapping indicator class to scoring tuple.
- Headline canonical tuple for the dominant class.
- Reasoning for CRPS over log-score in the primary slot.
- Implementation contract as a Python dataclass mapping.

## What comes next

- **L184** — leaderboard ranking algorithm that consumes these scores.
- **L193** — PIT plot publication per cell.

## Related

- [[R08-vv-matrix-detail]] — V&V matrix grades against these tuples.
- [[R24-backtest-engine]] — engine computes these metrics.
- [[L184-leaderboard-ranking]] — ranking rule.
- [[L193-calibration-plots]] — PIT publication.
- [[L199-trust-signals]] — calibration badge sourcing.
