# opengem-l3-dfm

OPENGEM L3 forecast backbone — a thin wrapper around `statsmodels.tsa.statespace.DynamicFactorMQ`.

Per L031–L045 of the 300-loop research round, this is the **pivotal cost-collapse #2**:
the NY Fed Nowcasting framework (Bok et al. 2017) is implemented natively in Python by
Chad Fulton (NY Fed staff economist, lead author of `statsmodels.statespace`). Block I's
biggest design risk — building the L3 forecast backbone — collapses to `pip install statsmodels`.

This package adds an OPENGEM-shaped wrapper that:

- Loads vintage-correct panels from `opengem-vintage`
- Fits a DynamicFactorMQ model on a configured spec
- Emits OPENGEM `Forecast` / `DensityForecast` records with proper provenance
- Plays nice with Dagster (one asset per country × indicator × horizon)

## License

Apache-2.0. The upstream `statsmodels` dependency is BSD-3-Clause, compatible.

## Quick start

```python
from opengem_l3_dfm import fit_us_gdp

forecast = fit_us_gdp(store, vintage_date="2026-06-06")
print(forecast.value, forecast.quantiles)
```

See `tests/` for a complete fixture-driven example without a real store.

## See also

- L032 — NY Fed Nowcasting reuse-vs-rewrite decision
- L035 — statsmodels DFM + BVAR ecosystem
- L181 — forecast object schema
- L189 — BMA combiner contract
