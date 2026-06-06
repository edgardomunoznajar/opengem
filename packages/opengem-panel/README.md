# opengem-panel

The **curation slice** (a minimal SSDD-002): turn raw vintage-store
`Observation`s into a model-ready **quarterly panel** that L3 (DynamicFactorMQ)
can fit.

It does three things and nothing else:

1. **Collect** a series as-of a vintage via `VintageView.iter_series`.
2. **Transform** raw levels into the modelling quantity — e.g. year-over-year
   growth (`gdp_yoy`, `cpi_yoy`) — and **resample** sub-quarterly data to
   quarterly.
3. **Align** every column on a common quarterly `PeriodIndex`, dropping
   incomplete rows.

```python
from opengem_panel import ColumnSpec, build_panel

view = store.at(date(2026, 6, 1))
panel = build_panel(view, [
    ColumnSpec("gdp_yoy", "US.BEA.NIPA.GDP_real.Q",   "yoy_q"),
    ColumnSpec("cpi_yoy", "US.BLS.CPI.headline_SA.M", "yoy_m_to_q"),
])
# -> pd.DataFrame indexed by PeriodIndex[Q], columns [gdp_yoy, cpi_yoy]
```

Vintage-correctness is inherited from the store: the panel only ever contains
data that was knowable as-of the view's vintage date.
