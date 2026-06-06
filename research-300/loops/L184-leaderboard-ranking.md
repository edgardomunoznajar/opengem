# L184 — Leaderboard Ranking Algorithm

**Loop**: 184 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

Three candidate ranking algorithms are on the table. Pick one. Defend the choice against the "model-of-the-week" gaming problem — where a model that happens to win the latest cell jumps to #1 then crashes back next epoch.

R25 already specified one such algorithm (the OPENGEM Index v1.0). This loop sharpens it, considers two alternatives, and commits to the variant that ships.

## The three candidates

### Candidate A — OPENGEM Index v1.0 (R25 baseline)

Weighted-average pass rate across V&V matrix cells. For each cell `(variable, horizon)`, `p_pass` = fraction of Tier-V countries passing the cell's threshold. Aggregate via fixed weights `w_{v,h}`. Bootstrap CI over countries.

```
OPENGEM_Index = Σ_{v,h} w_{v,h} × p_pass(v, h)
```

- **Strength**: simple, transparent, weights are policy-disclosed.
- **Weakness**: discrete pass/fail loses information. A model 1% above threshold is treated identically to one 50% above.

### Candidate B — Rank-Sum Score (RSS)

For each `(country, variable, horizon)` cell, rank all competing forecasters by their primary metric (CRPS for continuous-density indicators, AUC for binary). Lower rank = better. Sum the ranks across cells, normalised by number of cells; the lower the normalised rank-sum, the higher the leaderboard position.

```
RSS(model) = (1 / |C|) × Σ_{c ∈ C} rank_c(model)
```

with `c` the cells in scope. Optional weighting by cell importance.

- **Strength**: nonparametric; immune to scale differences between cells; classic in meta-analysis (Friedman test).
- **Weakness**: throws away effect-size information (the gap from #1 to #2 might be huge or tiny); susceptible to noisy rankings when several models cluster near each other.

### Candidate C — Stacked Skill-Score (SSS)

For each cell, compute the *skill score* — the percent reduction in primary metric vs. a fixed baseline (AR(1) for continuous, no-information for binary):

```
SkillScore(model, cell) = 1 - metric(model, cell) / metric(baseline, cell)
```

Range `(-∞, 1]`. Then aggregate via fixed cell weights `w_{v,h}` and report the weighted mean with bootstrap CI.

```
SSS(model) = Σ_{v,h} w_{v,h} × mean_country[SkillScore(model, (country, v, h))]
```

- **Strength**: continuous; rewards size of improvement; standard in atmospheric and macro forecasting (Murphy 1988); benchmarked against an interpretable floor.
- **Weakness**: a single catastrophic cell can dominate (skill-score is unbounded below), and the baseline must be fairly chosen per cell.

## The "model-of-the-week" gaming problem

The pathology: a model that exploits idiosyncrasies of recent vintages can win the most recent quarter handily, dominate the leaderboard, then collapse next quarter. The leaderboard then looks volatile and the public loses faith.

Three sources of this problem:

1. **Short evaluation window.** Latest-quarter rankings have high variance.
2. **Cherry-pickable cells.** A model can be tuned to win one cell while losing all others.
3. **Single-number aggregation hides instability.**

## Defences applied to all three candidates

| Defence | What it does |
|---|---|
| **Rolling 12-quarter OOS window** | Every cell's primary metric is computed over the most recent 12 quarters (or all available if fewer), not the latest quarter only. A model that wins one quarter but lost six earns rank by the average. |
| **Cell-level publication is primary** | The aggregate index is *not* the headline. The dashboard's leaderboard page shows the per-cell table; the aggregate is a footer summary. |
| **Bootstrap CI requirement** | A model must be statistically distinguishable from #2 (95% CI non-overlap) to claim solo #1. Otherwise the leaderboard shows "tied at top". |
| **Epoch pinning** | The ranking algorithm itself is version-pinned per epoch. Changing it requires a new epoch and a 12-month parallel-publishing window (R25 §6). |
| **Minimum-cell-count rule** | A model is excluded from the aggregate index unless it scores on ≥75% of in-scope cells. Stops gaming where a model only competes where it knows it wins. |
| **MCS at top** | Per cell, compute Hansen-Lunde-Nason Model Confidence Set at α=0.10. The MCS members all get the "top" badge. No single winner is crowned unless the MCS is a singleton. |

## The pick: **Candidate C — Stacked Skill-Score, with R25's weight schedule**

Reasoning:

- **Information-preserving.** Discarding the gap between 1.5% below threshold and 50% below threshold (which Candidate A does) wastes signal. A 50%-better-than-AR(1) model on GDP-1Q is *not* equivalent to a 2%-better model.
- **Continuity.** Small improvements over time produce small index changes. No discontinuous jumps as a model crosses a threshold.
- **Benchmark-grounded.** Skill scores are interpretable in real units: "OPENGEM L3 BMA reduces CRPS by 28% vs AR(1) on GDP-1Q averaged over Tier-V Core."
- **Compatible with R25's weight schedule.** The cell weights from R25 §3.2 carry forward — they encode policy priority, not statistical optimality.

We keep the *cell-level* leaderboard as the primary published artefact. The SSS aggregate is the footer summary; it earns the "OPENGEM Index v2.0" name because it changes the formula from v1.0's pass-rate to skill-score.

### Treatment of the catastrophic-cell issue

Skill scores are bounded above at 1 but unbounded below. A model that catastrophically misses one cell (skill-score of -50, say) would dominate the aggregate. Two patches:

1. **Floor at -2.** Skill scores below -2 are clipped to -2 in the aggregate. The reader still sees the raw score on the cell-level leaderboard.
2. **Report median in parallel.** Beside the weighted-mean SSS, report the unweighted median skill-score across cells. The two together resist both selective wins (median resists) and catastrophic losses (weighted mean reveals).

## The leaderboard publishing schema

```json
{
  "schema": "opengem.leaderboard.v2",
  "epoch": "v2.0-2026Q3",
  "as_of": "2026-09-01T00:00:00Z",
  "country_set": "Tier-V Core (26 countries)",
  "evaluation_window": "2023-Q3..2026-Q2",
  "algorithm": {
    "name": "OPENGEM Index",
    "version": "2.0",
    "method": "Stacked Skill Score",
    "weights": { "GDP_4Q": 0.12, "CPI_4Q": 0.14, "...": "...etc..." },
    "floor": -2.0,
    "model_card_url": "https://opengem.org/models/leaderboard/v2.0"
  },
  "rankings": [
    {
      "rank": 1,
      "model": "OPENGEM L3 BMA",
      "sss_weighted_mean": 0.32,
      "sss_median": 0.28,
      "ci95": [0.27, 0.37],
      "cells_in_scope": 17,
      "cells_scored": 17,
      "tied_with": [],
      "badges": ["mcs-member-all-cells", "pit-pass-15-of-17"]
    },
    {
      "rank": 2,
      "model": "Equal-weighted ensemble",
      "sss_weighted_mean": 0.27,
      "sss_median": 0.22,
      "ci95": [0.22, 0.32],
      "cells_in_scope": 17,
      "cells_scored": 17,
      "tied_with": [],
      "badges": ["mcs-member-14-of-17"]
    },
    {
      "rank": 3,
      "model": "IMF WEO",
      "sss_weighted_mean": 0.18,
      "sss_median": 0.15,
      "ci95": [0.14, 0.22],
      "cells_in_scope": 10,
      "cells_scored": 10,
      "excluded_from_aggregate_for_cells": ["GDP_8Q", "CPI_8Q", "..."],
      "badges": []
    }
  ]
}
```

## The model-of-the-week gaming check

A *separate* dashboard panel publishes the "stability index": variance of a model's rank across the last 8 quarters. A model jumping from #5 to #1 to #4 to #2 has a high stability index and earns a "volatile" warning badge. The reader sees the badge next to the headline rank.

```
Model                    Rank   12Q SSS   Stability Index   Badge
OPENGEM L3 BMA            1     0.32      0.4 (stable)      ★ ★ ★
Equal-weighted ensemble   2     0.27      0.5 (stable)      ★ ★
Some-Shop-Macro Q3-2026   3     0.24      2.1 (volatile)    ⚠ volatile
```

## Ineligibility rules

A forecaster is *eligible* for the leaderboard only if:

1. It publishes density forecasts (not just points) — required for CRPS to work. WEO and OECD EO get a "point-only" badge and compete only on MAE/RMSE cells.
2. Its forecasts are timestamped, vintaged, and reproducible — the L186 envelope.
3. It commits to a vintage-archive policy (we keep its historical forecasts; it cannot retroactively edit them).

Without (1), it ranks on a subset; without (2)+(3), it ranks not at all.

## What this loop produced

- Three candidates compared.
- Pick: Stacked Skill Score with R25 weights, floor -2, median-and-mean reported.
- Defences against model-of-the-week.
- Leaderboard JSON schema v2 with stability index.

## What comes next

- **L185** — open backtest harness exposing the cell metrics this consumes.
- **L186** — reproducibility envelope guarding eligibility.
- **L200** — failure log surfaced next to rank changes.

## Related

- [[R25-leaderboard-algorithm]] — predecessor (v1.0); this loop is the v2.0 spec.
- [[L183-forecast-scoring]] — scoring tuples this ranks over.
- [[L185-backtest-harness-api]] — engine that produces inputs.
- [[L199-trust-signals]] — badge catalog cross-references.
- [[R24-backtest-engine]] — V&V matrix evaluation.
