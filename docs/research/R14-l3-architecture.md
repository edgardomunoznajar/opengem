# R14 — L3 Workhorse Layer Architecture

| Field | Value |
|---|---|
| Document ID | OG1-RES-014 |
| Revision | A (2026-05-24) |
| Date | 2026-05-24 |
| Status | **Detailed architecture for SSDD-005 v2 (L3).** |
| Authority | R03 §5.1, master-doc v2.0 §5.5 |

---

## 1. The job

L3 is the **baseline forecast producer**. Given the OPENGEM data foundation, it produces density forecasts (P10/P50/P90 or full density grid) for each (Tier-V country, variable, horizon) cell. It does so via a small ensemble of variant models, combined by BMA over their rolling-window predictive log scores.

## 2. The variants

Each variant is a self-contained forecasting model. The combiner combines their density forecasts; the variants do not interact during fitting.

### 2.1 V1 — Mixed-Frequency Dynamic Factor Model (DFM)

**Reference**: Banbura, Giannone, Reichlin (2010); Banbura, Modugno (2014).

**Structure**: state-space model with latent common factors driving observed series at mixed frequencies. Kalman filter / smoother for state extraction. Forecasts from extrapolating latent state forward.

**Strengths**: short-horizon nowcasting; robust to data revisions; principled treatment of mixed-frequency data (monthly indicators inform quarterly target).

**Weaknesses**: linear factor structure; struggles in regime shifts; density forecasts assume Gaussian innovations (often mis-calibrated for fat tails).

**Implementation**: `statsmodels` `DynamicFactor` or custom NumPyro state-space; use Bayesian filtering for posterior on latent states; sample from predictive distribution.

**Cadence**: re-fit monthly on rolling 20-year window; nowcast updates daily as covariate data arrives.

### 2.2 V2 — DFM + ML residual

**Reference**: Coulombe et al. (2022/2024); various recent ML-for-macro papers.

**Structure**: V1 produces a baseline forecast; an ML model (LightGBM or random forest) predicts the *residual* (actual − V1 forecast) from a rich feature set including:
- V1's own forecast and uncertainty
- Wider information surface covariates (GSCPI, GPR, GDELT tone, term spread, equity returns, FX, etc.)
- Lagged residuals of V1
- Calendar features

**Strengths**: captures nonlinearities and interactions V1 misses; large feature space; well-validated by recent literature.

**Weaknesses**: ML residual density is harder to characterize (typically need quantile regression or bootstrap); risk of overfitting on small macro samples.

**Implementation**: `lightgbm` with quantile objective for density (`alpha=0.1, 0.5, 0.9`) producing P10/P50/P90 residual corrections; OR random forest with conformalized prediction intervals.

**Cadence**: re-fit monthly with cross-validated hyperparameters.

### 2.3 V3 — Large BVAR with Minnesota natural-conjugate prior

**Reference**: Banbura, Giannone, Reichlin (2010); Giannone, Lenza, Primiceri (2015).

**Structure**: VAR(p) with up to 20–30 variables per country, Minnesota prior with shrinkage estimated via marginal likelihood. Closed-form posterior — no MCMC needed.

**Strengths**: classical Bayesian benchmark; well-calibrated densities (Gaussian-conditional); fast to estimate; long horizons reasonable.

**Weaknesses**: linear; structural breaks degrade calibration.

**Implementation**: Python (`pybvar` or custom); 20 variables × p=4 lags; standard Minnesota hyperparameters.

**Cadence**: monthly re-estimation.

### 2.4 V4 (optional) — Time-Varying Parameter VAR with Stochastic Volatility

**Reference**: D'Agostino, Gambetti, Giannone (2013); Primiceri (2005).

**Structure**: VAR with parameters and innovation variances both evolving as random walks. Captures Great-Moderation-type structural shifts.

**Strengths**: handles regime shifts better than fixed-coefficient BVAR.

**Weaknesses**: slow to estimate (Gibbs sampling); fewer variables tractable.

**Implementation**: NumPyro or `tvp_var` package; 6–8 variables × p=2.

**Cadence**: monthly; optional in first IOC release; revisit at v0.4 if V1+V2+V3 BMA is under-calibrated for inflation.

## 3. The combiner

BMA over the variants, weighted by rolling-window predictive log scores:

```
weight_i(t) = exp(log_score_i(t-W..t-1)) / sum_j exp(log_score_j(t-W..t-1))
```

With W = 24 months. Density at horizon h:

```
p(y_{t+h} | data_{≤t}) = sum_i weight_i(t) · p_i(y_{t+h} | data_{≤t})
```

Implementation: a mixture-of-densities object. Sampling for downstream Monte Carlo via inverse-CDF of mixture.

Empirically: equal weights are competitive (R03 §2.1); BMA tends to slightly outperform under structural stability. Reasonable default.

## 4. Per-variable specialization

Different variables benefit from different L3 variant emphases:

| Variable | Variant emphasis | Rationale |
|---|---|---|
| GDP-real | V1 + V2 (V3 fallback) | DFM strong for short-horizon; ML residual handles nonlinearity in recession regimes |
| CPI-headline | V2 + V3 + V4 (when built) | Inflation is the hardest cell (R01); needs all variants |
| Unemployment | V1 + V2 | Persistence + nonlinearity |
| Policy rate | V3 only at 1Q (curve-anchored at longer horizons) | Avoid pretending to forecast policy when curve already prices it |

The combiner can be variable-specific (different weight calculations per variable), which is recommended at v0.4+.

## 5. Density representation

OPENGEM stores forecasts as **structured densities**, not just point estimates. Per `(run_id, country, variable, horizon)`:

```json
{
  "run_id": "20260524-q2-2026-vintage",
  "country": "US",
  "variable": "gdp_real",
  "horizon": "4Q",
  "p10": 0.012,
  "p25": 0.018,
  "p50": 0.024,
  "p75": 0.030,
  "p90": 0.038,
  "density_type": "mixture",
  "variants": {
    "v1_dfm":  {"weight": 0.42, "mean": 0.023, "stddev": 0.008, "kind": "normal"},
    "v2_ml":   {"weight": 0.35, "mean": 0.025, "stddev": 0.011, "kind": "quantile"},
    "v3_bvar": {"weight": 0.23, "mean": 0.022, "stddev": 0.009, "kind": "normal"}
  }
}
```

This allows the dashboard to show fan charts directly and the MCP layer to expose either point, density, or per-variant detail per consumer choice.

## 6. Feature stack for V2

V2's ML residual ingests a rich feature stack. At IOC (US-only):

| Feature group | Examples |
|---|---|
| V1 internals | V1 forecast, V1 stddev, V1 factor scores |
| Macro lags | GDP lags 1..8, CPI lags 1..8, unemployment lags 1..4 |
| Financial markets | 10y, 3m, 10y-3m spread, equity returns 1m/3m, VIX, BAA-10y spread, dollar index |
| Supply chain | GSCPI, freight indices, PortWatch (US ports), inventory/sales |
| Geopolitical | GPR-US, GPR-global, sanction-count change |
| Media | GDELT GKG US average tone (rolling 30d), news-attention shares (rolling 90d) |
| Calendar | Quarter, year, post-NBER recession flag, business cycle phase |
| Vintage features | release lag, revision since prior vintage |

~50 features at IOC; grows at Tier-V Extended to ~80 with country-specific local features.

## 7. Cadence summary

| Activity | Frequency | Cost |
|---|---|---|
| Adapter ingestion | Daily | Trivial |
| V1 DFM Kalman update | Daily | <1 min |
| V2 ML residual scoring | Daily | <1 min |
| V3 BVAR re-fit | Monthly | ~10 min |
| V4 TVP-VAR re-fit (when built) | Monthly | ~1 h |
| V2 ML re-train | Monthly | ~10 min |
| BMA weight refresh | Weekly | <1 min |
| Full backtest | Weekly | ~30 min |

All within the master-doc v2.0 NFR-PRF-003 budget.

## 8. Testing

**Unit**: per-variant function tests with golden fixtures (synthetic data with known DGP).

**Integration**: full pipeline on a single quarter of historical data → produces a forecast.

**Property**: PIT uniformity on synthetic samples drawn from known DGPs (calibration sanity).

**Statistical (regression)**: each PR runs full vintage replay 2014–most-recent; CI fails if any V&V cell from R08 §3 degrades by >5% from main.

## 9. Open questions

1. **NumPyro vs. statsmodels for V1**: NumPyro gives proper Bayesian uncertainty quantification; statsmodels is simpler. Decide at SAD time.
2. **Variant inclusion criterion**: does V4 add enough to justify its cost? Decide after Phase 3 MVP probe (R18 §6.4).
3. **Heteroskedasticity in V2 residual**: should V2 be quantile-regressed or homoskedastic-LightGBM? Pilot both at IOC.
4. **Cross-country pooled L3**: Block II might pool L3 across Tier-V countries for shrinkage. Defer.

## 10. Bottom line

L3 is **three variants + a combiner**, totaling ~2k lines of Python at IOC including tests. The architecture is well-supported by the recent forecasting literature (Coulombe, Banbura-Giannone, Rossi-Sekhposyan). The MVP probe in R18 Phase 3 will validate that this works on US data before scaling to the Tier-V Core.

---

*End of R14 Rev A.*
