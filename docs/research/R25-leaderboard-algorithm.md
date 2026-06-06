# R25 — Leaderboard Ranking Algorithm

| Field | Value |
|---|---|
| Document ID | OG1-RES-025 |
| Revision | A (2026-05-24) |
| Date | 2026-05-24 |
| Status | **Specification of the leaderboard ranking algorithm per POL-09 ("leaderboard ranking algorithm shall itself be open and version-pinned per leaderboard epoch").** |
| Authority | POL-09, FR-PUB-001 |

---

## 1. Principle

The leaderboard ranking algorithm is **itself a model**. It has its own model card, its own version pin, its own rationale. POL-09 requires this.

## 2. Two distinct rankings

OPENGEM publishes two leaderboards, not one:

### 2.1 Cell-level leaderboard

For each V&V cell, OPENGEM and named benchmarks are ranked by their metric on that cell:

```
Cell C-01 — GDP-real 1Q CRPS (Tier-V Core, evaluation window 2014-2025)
─────────────────────────────────────────────────────────────────────
Rank  Model                            Mean CRPS  Win rate vs AR(1)
─────────────────────────────────────────────────────────────────────
1     OPENGEM L3 BMA                   0.0042     83%
2     OPENGEM L3 V2 (DFM+ML)           0.0044     78%
3     Equal-weighted ensemble          0.0046     74%
4     OPENGEM L3 V1 (DFM)              0.0048     68%
5     AR(1)                            0.0058     50%
6     Random walk                      0.0062     45%
```

This is per-cell, transparent, no aggregate-of-aggregates.

### 2.2 Overall ranking ("OPENGEM Index")

A single aggregate score is also published for those who want a one-number summary. **The aggregation algorithm is itself the publicly disclosed and version-pinned model.**

## 3. The aggregation algorithm — OPENGEM Index v1.0

### 3.1 Inputs

Per `(country, variable, horizon)`:
- OPENGEM's primary metric value for that cell.
- Threshold for that cell from the V&V matrix.
- `passed` (boolean).

### 3.2 Cell weights

Each `(variable, horizon)` cell has a weight `w_{v,h}` reflecting *priority* of accuracy on that cell:

| Variable | 1Q | 4Q | 8Q | 20Q |
|---|---|---|---|---|
| GDP-real | 0.10 | 0.12 | 0.06 | 0.02 |
| CPI-headline | 0.10 | 0.14 | 0.06 | 0.02 |
| Unemployment | 0.06 | 0.08 | 0.04 | — |
| Policy rate | 0.06 | 0.04 | — | — |
| Recession-prob 12m | — | — | — | 0.10 |

Sum = 1.00. Rationale:
- 4Q-ahead carries highest weights because it's the most operationally relevant horizon.
- 20Q low weight because nobody is reliably accurate at 5y.
- Recession-probability gets a single horizon (12m) but reasonable weight because it's the discrete-action cell.

Weights are pinned per leaderboard epoch. Changing them requires a new epoch and an explicit rationale.

### 3.3 Country aggregation

For each cell `(v, h)`, OPENGEM's performance is summarized as:
- `p_pass(v, h)` = proportion of Tier-V countries that pass the cell's threshold.

### 3.4 Score

```
OPENGEM_Index = sum_{v, h} w_{v,h} * p_pass(v, h)
```

Range: [0, 1]. Higher is better. Reported with 95% bootstrap CI (bootstrap over countries).

### 3.5 Benchmark scores

Same formula applied to each benchmark (AR(1), RW, WEO, OECD EO):
- For naive benchmarks (AR(1), RW): pass = beats own threshold (here defined trivially as "this is the benchmark").
- For judgmental benchmarks (WEO, OECD EO): pass = corresponding cell's threshold against them.

This produces a row per system:

```
System                  Index    95% CI         W cells pass / total
────────────────────────────────────────────────────────────────────
OPENGEM L3 BMA          0.72    [0.68, 0.76]   13 / 17 cells
Equal-weighted ensemble 0.69    [0.65, 0.73]   12 / 17 cells
IMF WEO                 0.61    [0.57, 0.65]   10 / 17 cells (estim.)
OECD EO                 0.59    [0.55, 0.63]   10 / 17 cells (estim.)
AR(1)                   0.32    [0.28, 0.36]    5 / 17 cells
Random walk             0.28    [0.24, 0.32]    4 / 17 cells
```

## 4. The algorithm's model card

```yaml
# leaderboard_models/opengem_index_v1.0.yaml
algorithm: OPENGEM Index
version: 1.0
epoch: 2026-05-24..(next change)
rationale: |
  Weighted-average pass rate across V&V matrix cells, with weights pinned
  by the program owner to reflect operational priority. Bootstrap CI over
  countries within Tier-V Core.
weights:
  GDP-real:    {1Q: 0.10, 4Q: 0.12, 8Q: 0.06, 20Q: 0.02}
  CPI-head:    {1Q: 0.10, 4Q: 0.14, 8Q: 0.06, 20Q: 0.02}
  Unemployment:{1Q: 0.06, 4Q: 0.08, 8Q: 0.04}
  Policy_rate: {1Q: 0.06, 4Q: 0.04}
  Recession_12m: {12m: 0.10}
bootstrap_iterations: 1000
country_set: Tier-V Core (26 countries)
benchmarks_compared: [AR(1), RW, IMF WEO, OECD EO]
known_limitations:
  - "Cells are not independent; bootstrap may slightly overstate precision"
  - "Inflation-cell weights are arguably too high; sensitivity analysis published quarterly"
  - "Weight choice is a values judgment; not statistical optimum"
sensitivity_analysis:
  - "Per-weight sensitivity reported quarterly: ±0.1 on each weight"
  - "Robust ranking: OPENGEM beats AR(1) under all weight perturbations to date"
ranking_method: "Pointwise; ties broken by 95% CI overlap"
```

## 5. Why this design

Three principles:

1. **No hidden tuning.** Weights are policy decisions, explicitly documented.
2. **No single-number-only.** The cell-level leaderboard is the primary artifact; the aggregate index is supplementary.
3. **Reproducible.** Anyone can recompute the index from the V&V results table.

## 6. Epoch transitions

When the algorithm changes (e.g., weights are updated, new cells added):

- A new epoch begins with version v2.0 (or v1.1 for minor revisions).
- Both the old and new index are computed in parallel for 12 months.
- After 12 months, the old epoch is retired; both remain queryable historically.
- Rationale for change is published as a `LEADERBOARD-CHANGE-NOTE.md` document.

This is similar to how stock indices handle methodology revisions (S&P 500 reconstitution).

## 7. Anti-gaming

The algorithm should not be tunable to make OPENGEM look good. Defenses:

- **Cell-level thresholds are externally referenced** (AR(1), RW, WEO, OECD EO) — we can't change those.
- **Weights are public and rationale-documented** — any tuning is visible.
- **Sensitivity analysis is published** — readers see whether OPENGEM's ranking is robust to weight choice.
- **Cross-validation across epochs** — historical Index value at the same cells is recoverable; tampering shows up.

## 8. Future revisions

Likely epoch-2 changes (when reached):

- Re-weight inflation cells if 8-quarter track record shows it's systematically the hardest cell.
- Add Tier-V Extended cells once those countries have ≥8 quarters of vintage-correct OOS.
- Add Situation Subsystem GPR-nowcast cell if/when that endpoint is built and scored.

## 9. Public computation harness

The Index is computed by a public Python script:

```bash
opengem leaderboard compute --epoch v1.0
# Reads from vv_results table; produces leaderboard CSV + bootstrap CIs
```

Anyone can run it against the public `vv_results` snapshot and get identical numbers.

## 10. Bottom line

The OPENGEM Index is a *transparent, version-pinned, sensitivity-tested* aggregation of cell-level V&V results. It is the closest thing to a single number that does not pretend to be one. The cell-level leaderboard remains the primary artifact; the index serves the "rank me at a glance" use case without hiding what's underneath.

---

*End of R25 Rev A.*
