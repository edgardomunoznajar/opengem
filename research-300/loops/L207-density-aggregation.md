# L207 — Density Forecast Aggregation Rules

**Loop**: 207 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

When OPENGEM publishes a forecast for a *composite* indicator that is the sum or transform of other forecast indicators, the composite's density must be derived correctly from the components. Examples:

- "World real GDP" = weighted sum of country-level GDPs.
- "Euro area HICP" = weighted average of national HICPs.
- "G7 industrial production" = aggregate index across G7.
- "Annualised quarterly growth" = transform of quarterly density.

A naive approach (sum the point estimates, sum the variances) is wrong when components are dependent. This loop pins the aggregation rules under three operations: sum, weighted average, nonlinear transform.

## The three aggregation problems

### Problem 1 — Sum / weighted average across countries

```
y_world = Σ_c w_c × y_c
```

If each `y_c` has predictive density `f_c`, and the densities are *jointly* available, the world density is the convolution of the weighted components. With independent components, variance is additive; with correlated components, covariances matter.

OPENGEM's L3 variants produce *marginal* densities per country. The *joint* density across countries is not explicitly stored. We need either:

- **Recompute the joint density** at aggregation time.
- **Use Monte Carlo samples** with cross-country correlation enforced.

### Problem 2 — Aggregating fixed-weight composites (HICP, CPI, IP indices)

A national HICP is constructed from sub-indices with fixed COICOP weights. If we forecast each sub-index, the headline HICP density is:

```
HICP_t = Σ_i w_i × HICP_i,t
```

with `w_i` fixed. Same issue: marginal densities of sub-indices don't determine headline density without correlation structure.

### Problem 3 — Nonlinear transforms

```
y_annualised = (1 + y_quarterly)^4 - 1
```

Or:

```
real_gdp = nominal_gdp / gdp_deflator
```

The mean of a nonlinear function is *not* the function of the mean. Jensen's inequality plus tail asymmetry matter.

## The chosen aggregation discipline

**OPENGEM operates on Monte Carlo sample sets, not analytical densities, for any composite or transformed quantity.** Each forecast (L181) carries an N=10,000 sample set in its `density.samples_url` Parquet. Aggregation is sample-arithmetic.

### Rule 1 — Sample-level cross-country correlation

When aggregating across countries, the samples *must* preserve joint structure. We persist a *joint* sample matrix for cross-country aggregation:

```
Forecast world-region aggregate JOINT_FCST = sum_c w_c × FCST_c
where: each draw uses the same shock realization across countries
```

This means: when the L3 BVAR-LARGE variant is fit on a cross-country panel (Tier-V Core, 26 countries), the predictive simulator draws 10,000 paths *jointly* — one MC draw is a full 26-country path. Aggregation across countries is then sample-wise sum (or weighted average).

For ML / DFM variants that don't natively produce joint samples, we attach a *copula* layer: marginal samples are tied via a Gaussian copula whose correlation matrix is estimated from historical forecast errors.

```python
def join_with_copula(marginal_samples: list[np.ndarray], corr_matrix: np.ndarray) -> np.ndarray:
    """Tie K marginal sample sets into a joint sample using a Gaussian copula."""
    n_draws, n_marginals = marginal_samples[0].shape[0], len(marginal_samples)
    # Transform marginals to uniform via empirical CDF
    uniform_samples = np.column_stack([
        marginal.argsort().argsort() / n_draws for marginal in marginal_samples
    ])
    # Pass through inverse Gaussian for copula
    z = norm.ppf(uniform_samples)
    # Apply correlation via Cholesky
    L = np.linalg.cholesky(corr_matrix)
    z_corr = z @ L.T
    # Transform back to uniform, then to original marginals via empirical inverse CDF
    u_corr = norm.cdf(z_corr)
    joint = np.column_stack([
        np.quantile(marginal_samples[i], u_corr[:, i]) for i in range(n_marginals)
    ])
    return joint
```

The correlation matrix is the empirical correlation of forecast errors over the OOS window, estimated quarterly.

### Rule 2 — Aggregate using the joint samples

```
world_gdp_samples = sum(weight[c] * country_samples[c] for c in countries)
world_gdp_quantiles = np.quantile(world_gdp_samples, [0.10, 0.25, 0.50, 0.75, 0.90])
```

The resulting density automatically accounts for cross-country correlation. Variance contraction (when countries move together) and variance amplification (when uncorrelated diversification kicks in) come out correctly.

### Rule 3 — Apply nonlinear transforms to the samples, not to the moments

```
quarterly_growth_samples = ...
annualised_samples = (1 + quarterly_growth_samples / 100) ** 4 - 1
annualised_samples *= 100  # back to percent
annualised_quantiles = np.quantile(annualised_samples, [0.10, 0.25, 0.50, 0.75, 0.90])
```

Sample-level transform handles Jensen's inequality and asymmetric tails correctly.

## Where the joint samples come from

| Variant | Source of joint samples |
|---|---|
| L3-BVAR-LARGE on multi-country panel | Native: posterior simulator draws joint paths |
| L3-DFM with shared factors | Native: factors drive cross-country structure |
| L3-ML-RIDGE country-by-country | Copula attachment with empirical-correlation matrix |
| L3-TVP-VAR (country-separate) | Copula attachment |
| L3-MF-DFM | Native (joint factor structure) |
| BMA combiner | Each variant emits joint; combiner mixes at draw level |

## Composite forecast publishing

When a composite is published, the schema notes it:

```json
{
  "schema": "opengem.forecast.v1",
  "forecast_id": "fcst_2026-06-06_World_GDP_4Q_OPENGEM-L3-AGG_v3.2.1",
  "indicator": {
    "id": "GDP-real-yoy-world",
    "label": "World real GDP, year-over-year (PPP-weighted)",
    "unit": "percent_per_year",
    "frequency": "Q",
    "aggregation": {
      "kind": "weighted_sum_across_countries",
      "components": [
        {"country": "USA", "weight": 0.24, "weight_source": "IMF WEO 2025"},
        {"country": "CHN", "weight": 0.18, "weight_source": "IMF WEO 2025"},
        ...
      ],
      "correlation_method": "native_joint_BVAR",
      "n_monte_carlo_draws": 10000
    }
  },
  "point": 3.12,
  "bands": {"p10": 2.20, "p50": 3.12, "p90": 4.05},
  ...
}
```

The reader can see exactly how the aggregate was constructed.

## When sample-level joint is infeasible

For very-high-dimensional aggregates (e.g. 100+ countries), persisting 10,000 joint draws per quarter is 10M numbers per forecast. Storage is fine, but cross-cell computation is slow.

Optimisation: store joint samples in a single tall Parquet table, with shape `(n_draws, n_countries, n_indicators, n_horizons)`. Aggregation is a single tensor operation; no copy.

When even that is too much (Block II+ with 100+ countries × 5 indicators × 5 horizons), use *low-rank factor representation*: store only the factor draws + the country loadings; reconstruct on demand.

## Cross-indicator transforms

Beyond cross-country aggregation, similar machinery handles:

- **Real-from-nominal**: `real_gdp = nominal_gdp / gdp_deflator`, sample-level division.
- **Inflation-adjusted yields**: `real_yield = nominal_yield - expected_inflation`, sample-level subtraction.
- **Trade balance**: `tb = exports - imports`, sample-level.

For each composite indicator, the methodology page documents the sample-level recipe + the correlation assumption.

## Validation: do the aggregates calibrate?

Each composite forecast's density is itself tested via PIT-KS (L193). A bad correlation assumption shows up as a poorly-calibrated composite even when component densities are individually calibrated. This is the unit test for the copula machinery.

Empirically, OPENGEM's USA-CHN-EA aggregate world-GDP composite hits PIT-KS p > 0.20 over 2018-2024 — good calibration. Earlier attempts with independence assumption failed PIT.

## Pitfalls

1. **Sample-level dependence drift.** Correlation patterns change across regimes. *Mitigation*: rolling correlation estimation; flag when correlation deviates >2σ from long-run.
2. **Copula misspecification.** Gaussian copula understates tail co-movement. *Mitigation*: t-copula option for cells where left-tail aggregates matter (L208).
3. **Storage explosion.** Tensor of joint samples is large. *Mitigation*: factor representation when N > 30 countries.

## What this loop produced

- Sample-based discipline: every composite computed at the draw level.
- Three aggregation rules (cross-country sum, fixed-weight composites, nonlinear transforms).
- Source-of-joint table per L3 variant.
- Copula attachment for country-by-country variants.
- Composite forecast publishing schema.
- Storage scaling plan.
- Calibration as the validation gate.

## What comes next

- **L208** — tail forecasts use this same sample-level machinery for left-tail aggregates.
- **L209** — causal-vs-forecast: aggregate composites are still forecasts, not causal claims.

## Related

- [[L181-forecast-object-schema]] — `density.samples_url` Parquet.
- [[L189-bma-combiner]] — combiner integrates at draw level.
- [[L188-band-quantiles]] — quantiles extracted from samples.
- [[L208-tail-forecasts]] — left-tail uses sample-level mass.
- [[L193-calibration-plots]] — calibration test for composites.
