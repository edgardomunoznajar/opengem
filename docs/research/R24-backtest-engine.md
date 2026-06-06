# R24 — Backtest Engine Design

| Field | Value |
|---|---|
| Document ID | OG1-RES-024 |
| Revision | A (2026-05-24) |
| Date | 2026-05-24 |
| Status | **Detailed design for SSDD-007 v2 backtest engine.** |
| Authority | FR-BCT-001/002, R08 V&V matrix, R16 reproducibility |

---

## 1. Job

The Backtest Engine evaluates OPENGEM's forecast accuracy against the V&V matrix (R08), using vintage-correct data. It produces the public leaderboard and the per-release V&V scorecard.

## 2. Three modes

### 2.1 Mode A — Rolling-origin pseudo-real-time replay (Tier-V)

For each `(country, variable, horizon, vintage_t)`:
- Set the model's "current time" to `vintage_t`.
- Pull the data vintage that was available at `vintage_t`.
- Run the L3 pipeline against that vintage.
- Forecast at horizon `h`.
- Compare forecast to the *eventually-revised* value of the target (i.e., the value as published 2+ years later, treated as ground truth).
- Compute per-cell metrics (CRPS, RMSE, DM-vs-benchmark, PIT).

Equivalent in pseudocode:

```python
for country in tier_v_core:
    for variable in [GDP, CPI, UR, POLRATE]:
        for h in [1, 4, 8, 20]:
            for vintage_t in vintages_2014_to_present_minus_2y:
                vintage_data = vintage_archive.at(vintage_t)
                forecast = opengem.l3.forecast(country, variable, h, vintage_data)
                actual   = latest_revised.value(country, variable, t + h*quarter)
                metrics  = score(forecast, actual)
                store(country, variable, h, vintage_t, metrics)
```

This is the workhorse mode. Runs weekly on the latest data; runs nightly on a sample for drift detection.

### 2.2 Mode B — Benchmark same-vintage comparison

For each `(country, variable, horizon, vintage_t)` cell against a same-vintage benchmark:
- Pull benchmark's forecast that was published at `vintage_t` (or within a release lag tolerance).
- Compare OPENGEM's same-`vintage_t` forecast to the benchmark.
- Compute pairwise metrics: Diebold-Mariano with HLN small-sample correction.

Benchmarks: AR(1), RW, WEO, OECD EO, forward curve (for policy rates).

### 2.3 Mode C — CI guard on PR

When a PR is opened that touches `model/` or `combiner/`:
- Replay a subset of mode A (random 200 vintage-cells).
- Compare new branch's metrics to main branch.
- Fail if any cell degrades >5% on its primary metric.
- Comment on the PR with the comparison table.

## 3. Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                  Backtest Engine (SSDD-007)                       │
│                                                                    │
│  ┌────────────────────┐  ┌─────────────────────────┐              │
│  │  Vintage Replayer  │─▶│  L3 Pipeline (frozen    │              │
│  │  - resolves at_t   │  │   for the replay run)   │              │
│  │  - feeds data      │  │  → forecast (density)   │              │
│  └────────────────────┘  └────────────┬────────────┘              │
│                                        │                          │
│                                        ▼                          │
│                              ┌──────────────────────┐             │
│                              │ Metric Engine        │             │
│                              │  - CRPS              │             │
│                              │  - RMSE / MAE        │             │
│                              │  - Log score         │             │
│                              │  - DM (HLN-corrected)│             │
│                              │  - PIT KS test       │             │
│                              │  - MCS               │             │
│                              └──────────┬───────────┘             │
│                                         │                         │
│                  ┌──────────────────────┼───────────────────────┐ │
│                  ▼                      ▼                       ▼ │
│        ┌────────────────┐  ┌────────────────┐    ┌────────────┐  │
│        │  vv_results    │  │  leaderboard   │    │  PR-CI     │  │
│        │  table         │  │  materialized  │    │  report    │  │
│        │  (cell, value, │  │  view          │    │            │  │
│        │   pass/fail)   │  │  (weekly)      │    │            │  │
│        └────────────────┘  └────────────────┘    └────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

## 4. Components

### 4.1 Vintage Replayer

```python
class VintageReplayer:
    def __init__(self, vintage_archive: VintageArchive):
        self.archive = vintage_archive

    def at(self, t: date) -> VintageView:
        """Return the data as it was known on date t — i.e., latest vintage
        whose vintage_at <= t per series_id."""
        return VintageView(self.archive, t)

class VintageView:
    """A read-only snapshot of the data as it was at a given date.
    Filters raw_observation by vintage_at <= self.t."""

    def get_series(self, series_id: str) -> pd.Series:
        """Latest observed values per period as of self.t."""
        return self.archive.latest_per_period(series_id, as_of=self.t)
```

### 4.2 Metric Engine

```python
def crps(forecast_density: Density, actual: float) -> float:
    """Continuous Ranked Probability Score — for mixture densities."""
    # Closed form for Gaussian mixtures; numerical otherwise
    ...

def diebold_mariano(losses_a: np.ndarray, losses_b: np.ndarray,
                     correction: str = "HLN") -> tuple[float, float]:
    """DM stat and p-value. Default Harvey-Leybourne-Newbold correction."""
    ...

def pit_test(pit_values: np.ndarray, test: str = "KS", alpha: float = 0.05) -> tuple[bool, float]:
    """KS test for U[0,1] uniformity. Returns (pass, p_value)."""
    ...

def model_confidence_set(loss_matrix: np.ndarray, alpha: float = 0.10,
                          bootstrap: str = "stationary") -> set[int]:
    """Hansen-Lunde-Nason MCS. Returns indices of models in the set at confidence 1-alpha."""
    ...
```

### 4.3 Cell Evaluator

```python
@dataclass
class CellEvaluation:
    cell_id: str               # 'C-01' etc.
    evaluation_run: str
    observed_value: dict       # metric: value
    threshold: dict            # threshold spec
    passed: bool
    evaluated_at: datetime
    sample_size: int

def evaluate_cell(cell_spec: CellSpec, replayer: VintageReplayer,
                   forecast_archive: ForecastArchive) -> CellEvaluation:
    """Evaluate a single V&V matrix cell over the OOS window."""
    # 1. Pull all (vintage_t, forecast, actual) triples for cell's scope
    # 2. Compute metrics
    # 3. Compare to threshold
    # 4. Return CellEvaluation
    ...
```

### 4.4 Leaderboard Materializer

```sql
CREATE MATERIALIZED VIEW leaderboard AS
WITH latest_run AS (
    SELECT MAX(evaluation_run) AS run_id FROM vv_results
)
SELECT
    cell_id, variable, horizon, country_set, benchmark,
    observed_value, threshold, passed,
    DENSE_RANK() OVER (PARTITION BY cell_id ORDER BY 
        CAST(observed_value->>'primary_metric' AS NUMERIC)) AS rank_in_cell
FROM vv_results
WHERE evaluation_run = (SELECT run_id FROM latest_run);

REFRESH MATERIALIZED VIEW leaderboard;
```

Refreshed weekly via Dagster.

## 5. Performance budget

Mode A (full Tier-V Core × variables × horizons × vintages 2014–present):
- 26 countries × 4 variables × 4 horizons × ~48 vintages = ~20k cells per V&V matrix run
- ~5 ms per cell evaluation (CRPS + DM + PIT) = ~100s
- Plus L3 re-forecasting at each vintage: ~10k full-pipeline runs × ~30 s each = ~3.3 days *naively*

Optimizations:
- **Cache L3 forecasts per `(vintage_t, country, variable, horizon)`** — these don't depend on which V&V cell we're evaluating.
- **Re-use posteriors across horizons** — V1/V2/V3 produce all horizons in one pass.
- **Parallelize across countries** — Dagster fans out.

Realistic: ~4 hours for a full Mode A run on the baseline VM. Weekly cadence is comfortable.

For Mode C (PR CI): 200-cell random sample → ~3 min, no L3 re-fit (uses cached forecast archive). Fast enough for PR CI.

## 6. Reliability and provenance

Every backtest run records:
- `code_sha` of the backtest engine.
- `code_sha` of the L3 pipeline used.
- Set of `(vintage_hash)` tuples replayed.
- `evaluation_run_id` = canonical hash of the above.

The replay-and-diff CI (R16) covers the backtest engine too: nightly, a random V&V cell is re-evaluated and bytes compared to stored result.

## 7. What goes on the public leaderboard

A simple, honest table refreshed weekly:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ OPENGEM Tier-V Public Leaderboard — Refreshed 2026-05-24                     │
├──────────────────────────────────────────────────────────────────────────────┤
│ Cell  Variable    Horiz  Benchmark      OPENGEM    BMK     Δ      Pass/Fail  │
├──────────────────────────────────────────────────────────────────────────────┤
│ C-01  GDP-real    1Q     AR(1) (CRPS)   83% win   100%    +83 pp  ✓ ≥80%    │
│ C-02  GDP-real    1Q     own (PIT KS)   82% pass  -       -       ✓ ≥80%    │
│ C-03  GDP-real    4Q     WEO (DM)       58% n.w.  -       -       ✓ ≥50%    │
│ C-08  CPI-head    1Q     AR(1) (CRPS)   69% win   100%    +69 pp  ✓ ≥65%    │
│ C-10  CPI-head    4Q     WEO (DM)       37% n.w.  -       -       ✗ <40%    │
│ C-17  Recession   12m    Bauer-Mertens  0.87 AUC  0.89    -0.02   ✓ ≥0.85   │
│ ...                                                                          │
└──────────────────────────────────────────────────────────────────────────────┘
```

Cell-level click-through shows the per-country breakdown.

## 8. Bottom line

Backtest is the heart of OPENGEM's accountability claim. The engine is **mechanical**: cells defined in code, replay is deterministic, metrics are textbook, results are stored. The leaderboard *is* the V&V matrix evaluated weekly. No drama, no judgment calls, no hidden tuning.

---

*End of R24 Rev A.*
