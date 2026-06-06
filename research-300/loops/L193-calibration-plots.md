# L193 — Calibration Plot per Indicator × per Horizon

**Loop**: 193 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

For every V&V matrix cell (`country` × `indicator` × `horizon`), publish a calibration plot — specifically a Probability Integral Transform (PIT) histogram. This loop specifies the plot format, the per-cell URL scheme, the threshold-marking rules, and the supporting reliability diagram for binary indicators.

Calibration is the "is the uncertainty honest?" question. A point forecast that hits the mean is not enough; the *bands* must cover the actual outcome at the nominal rate (80% bands should contain the truth 80% of the time). The PIT plot is the visual proof.

## The PIT plot

For a probabilistic forecast `F_t(y)` of variable `y_t`, the PIT value is:

```
u_t = F_t(y_t)
```

If the forecast distribution is correctly calibrated, `u_t ~ U[0,1]`. Plot the histogram of `u_t` over the OOS window. A flat histogram = good calibration. Patterns indicate failure modes:

- **U-shape**: forecasts are too narrow (too many realisations land in extreme quantiles).
- **Hump in middle**: forecasts are too wide (most realisations land near the median).
- **Left skew**: forecasts are biased high (more left-quantile realisations).
- **Right skew**: forecasts are biased low.

## Plot specification

Each cell's PIT plot is published with:

```
URL:    https://opengem.org/calibration/{cell_id}/{country}/{indicator}/{horizon}
        (e.g. /calibration/C-03/USA/GDP-real-yoy/4Q)
Format: SVG (vector) + PNG (raster) + JSON data block (machine-readable)
```

The SVG renders:

1. **20 equally-spaced bins** over [0, 1].
2. **Y-axis**: bin frequency, normalised so a perfectly flat distribution gives bars at height 1.
3. **X-axis**: PIT value.
4. **Reference line**: horizontal at y=1 (perfect calibration).
5. **Confidence bands**: 90% binomial CI around y=1, computed from sample size N. Bars within bands = consistent with uniformity.
6. **Headline statistic in caption**: "PIT-KS p-value = 0.42 (uniform; pass at α=0.05). N = 168 observations."

The 90% CI is the eye-test rule: if all 20 bars stay inside the CI envelope, calibration is fine. Bars poking outside indicate a specific bin's miscalibration.

## Example plot annotations

```
PIT calibration — USA Real GDP YoY, 4Q-ahead (cell C-03)
Evaluation window: 2014-Q1..2025-Q4, N=168 OOS forecasts

  1.5 │                              
      │     ┌──┐    ┌──┐  ┌──┐       
  1.0 ┼─────┤  ├────┤  ├──┤  ├──── (perfect calibration reference)
      │     │  │    │  │  │  │       
  0.5 │     │  │    │  │  │  │       
      │     │  │    │  │  │  │       
  0.0 └─────┴──┴────┴──┴──┴──┴──── 
       0           0.5            1.0

  PIT-KS p-value = 0.42  (uniform; pass at α=0.05)
  Mean of PIT = 0.51  (no systematic bias)
  Variance of PIT = 0.084  (close to uniform 1/12 = 0.083)
```

## Machine-readable JSON

The same plot is available as JSON for LLM grounding:

```json
{
  "schema": "opengem.pit_plot.v1",
  "cell_id": "C-03",
  "country": "USA",
  "indicator": "GDP-real-yoy",
  "horizon_q": 4,
  "evaluation_window": "2014-Q1..2025-Q4",
  "n_observations": 168,
  "pit_values": [...],  // length N=168
  "histogram": {
    "n_bins": 20,
    "bin_edges": [0.00, 0.05, 0.10, ..., 0.95, 1.00],
    "counts": [9, 8, 7, ..., 8, 9],
    "expected_count_per_bin": 8.4,
    "ci90_per_bin": [3, 14]
  },
  "tests": {
    "ks_statistic": 0.062,
    "ks_pvalue": 0.42,
    "ks_pass_alpha_005": true,
    "berkowitz_pvalue": 0.38,
    "mean_pit": 0.51,
    "var_pit": 0.084
  },
  "verdict": "calibrated",
  "verdict_badge": "pit-passed",
  "model_card_url": "https://opengem.org/methodology/vv-matrix/C-03"
}
```

The same JSON is the resource the LLM-narrative pipeline (L198) fetches when explaining calibration.

## Reliability diagrams for binary indicators

For recession-12m (cell C-18) and any other binary-probability cell, the PIT is not informative. Instead we publish a **reliability diagram**:

- Bin predicted probabilities into 10 deciles.
- For each decile, plot the *mean predicted probability* vs. the *empirical event rate*.
- Diagonal line = perfect reliability.

```
Reliability — USA Recession-12m (cell C-18)
Evaluation window: 1968-Q1..2025-Q4, N=232 forecasts

  1.0 │                            ●
      │                       ●  /
  0.8 │                  ●  /  
      │             ●  /         
  0.6 │       ●  /                  diagonal = perfectly calibrated
      │   ●  /                       
  0.4 │   /                          
      │/  ●                            
  0.2 │   ●                            
      │                              
  0.0 └────────────────────────────►
       0.0   0.2   0.4   0.6   0.8   1.0
                  predicted prob

  Brier score = 0.082  (vs naive 0.18; skill = 54%)
  Expected Calibration Error = 0.04  (well-calibrated; pass at ECE < 0.05)
```

The reliability diagram + Brier + ECE is the canonical triple for binary cells.

## Per-cell publication: how this scales

There are 17 V&V cells × 26 Tier-V Core countries = ~442 calibration plots at IOC. Per-cell publication scales by:

1. **Static generation.** Each plot is rendered by the backtest engine (R24) on its weekly cadence and uploaded as SVG + PNG + JSON to S3.
2. **CDN-fronted.** Plots are served from a CDN (Cloudfront / Cloudflare) with weekly cache invalidation.
3. **Aggregate page first.** The dashboard's "calibration overview" page shows a grid of 17 cells × 26 countries as small multiples (each ~80 px square sparkline-style PIT). Click a tile to drill into the full SVG.

Total disk: ~6 MB of SVG + ~24 MB of PNG + ~3 MB of JSON per weekly snapshot. Trivial.

## What to do when calibration fails

A failed PIT-KS does not invalidate the forecast — but it triggers downstream actions:

1. **Badge**: forecast carries a "calibration: warning" badge (L199).
2. **Methodology page note**: the cell's methodology page automatically appends a "currently miscalibrated" alert at the top.
3. **Issue in the backlog**: the engine opens a GitHub issue tagged `calibration-fail-{cell_id}-{country}-{horizon}` with a link to the PIT plot.
4. **Quarterly review**: the maintainer reviews calibration-failed cells quarterly; if a fix is not actionable, the cell publishes the failed PIT plot transparently.

The failure is *not* hidden. The transparency is the whole point.

## Drift detection

Beyond static calibration, we monitor PIT *drift*. Each weekly run records the rolling-12-quarter PIT-KS p-value as a time series. A trend of decreasing p-value (calibration degrading) earns a "drift" badge and triggers a retraining cycle.

## Cross-cell calibration heatmap

For at-a-glance review, the dashboard's calibration overview shows a heatmap of PIT-KS p-values:

```
            GDP-1Q  GDP-4Q  GDP-2Y  CPI-1Q  CPI-4Q  UR-4Q  POL-4Q
USA        ■ 0.42  ■ 0.31  ■ 0.18  ■ 0.55  ■ 0.41  ■ 0.62  ■ 0.71
GBR        ■ 0.38  ■ 0.28  ■ 0.21  ■ 0.49  ■ 0.34  ■ 0.58  ■ 0.66
DEU        ■ 0.45  ■ 0.33  ■ 0.19  ■ 0.51  ■ 0.39  ■ 0.60  ■ 0.68
JPN        ■ 0.51  ■ 0.42  ▢ 0.04  ■ 0.62  ▢ 0.03  ■ 0.55  ■ 0.61
... (continues for 26 countries)
```

Filled green tiles ■ = calibration pass; empty red tiles ▢ = fail. Click any tile → full PIT plot.

## What this loop produced

- PIT plot specification (20-bin, CI envelope, KS test).
- JSON contract for machine-readable PIT data.
- Reliability diagrams for binary indicators (Brier + ECE).
- Per-cell publication strategy (442 plots, CDN-served).
- Heatmap UX for cross-cell overview.
- Failure handling: badge + alert + tracked issue + transparent publication.

## What comes next

- **L194** — coverage page that hosts the heatmap.
- **L199** — calibration badges feed trust signals.

## Related

- [[R08-vv-matrix-detail]] — PIT-KS is the calibration test in the V&V matrix.
- [[R24-backtest-engine]] — engine that computes PIT values.
- [[L183-forecast-scoring]] — scoring tuple specifies PIT-KS.
- [[L194-coverage-page]] — heatmap host.
- [[L199-trust-signals]] — badge consumer.
- [[L200-failure-log]] — calibration failures get posted.
