"""fit_dfm — DynamicFactorMQ wrapper that emits OPENGEM Forecast records.

This is the L3 backbone. Per L031–L045 deep-dives, we wrap
`statsmodels.tsa.statespace.DynamicFactorMQ` rather than re-implementing
the NY Fed Nowcasting framework. `pip install statsmodels` and you have
Chad Fulton's native Python implementation of Bok et al. 2017.

We add an OPENGEM-shaped layer that:

1. Accepts an OPENGEM ``DFMConfig`` instead of statsmodels-shaped kwargs.
2. Returns ``DensityForecast`` records (5-quantile) per requested horizon.
3. Propagates a ``run_id`` (a short hash of config + data shape + library
   version) so the forecast is reproducible from its identifiers.

Heavy dependencies (numpy, pandas, statsmodels, scipy) are imported lazily
so that downstream consumers of this package don't pay the import cost
until they actually fit.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import asdict
from datetime import date
from typing import TYPE_CHECKING, Any

from opengem_types import (
    Country,
    DensityForecast,
    ForecastQuantiles,
    Variable,
)

from opengem_l3_dfm.config import DFMConfig

if TYPE_CHECKING:
    import pandas as pd


def _import_pandas() -> Any:
    import pandas as pd

    return pd


def _import_dfm_class() -> Any:
    from statsmodels.tsa.statespace.dynamic_factor_mq import DynamicFactorMQ

    return DynamicFactorMQ


def _import_statsmodels_version() -> str:
    import statsmodels

    return statsmodels.__version__


def _run_id(cfg: DFMConfig, panel_shape: tuple[int, int], lib_version: str) -> str:
    """Stable hash of (config, panel shape, statsmodels version).

    Same config + same data shape + same statsmodels version → same run_id.
    Different anything → different run_id. Good enough for vintage cataloguing.
    """
    blob = repr((asdict(cfg), panel_shape, lib_version)).encode()
    return hashlib.sha256(blob).hexdigest()[:16]


def fit_dfm(
    panel: "pd.DataFrame",
    cfg: DFMConfig,
    base_period: date,
) -> list[DensityForecast]:
    """Fit a DynamicFactorMQ on `panel` and emit one DensityForecast per horizon.

    Parameters
    ----------
    panel : pandas DataFrame
        Index is ``pd.PeriodIndex`` (quarterly) or ``pd.DatetimeIndex`` aligned
        to quarter-ends. Columns are series codes — one column per OPENGEM
        series being used as model input. The ``cfg.target`` column must exist.
    cfg : DFMConfig
        Declarative config.
    base_period : date
        Last period in the training window (anchor for horizon arithmetic).

    Returns
    -------
    list[DensityForecast]
        One record per requested horizon. Each contains five quantiles
        derived from the predicted mean ± standard error of the target
        column at the appropriate forecast step.
    """
    pd = _import_pandas()
    DynamicFactorMQ = _import_dfm_class()
    sm_version = _import_statsmodels_version()

    if cfg.target not in panel.columns:
        raise ValueError(f"target {cfg.target!r} not in panel columns {list(panel.columns)}")
    if panel.empty:
        raise ValueError("panel is empty; cannot fit DFM")

    # Statsmodels expects float64 columns; coerce.
    train = panel.astype(float)
    if len(train) < 2 * cfg.factor_order + 4:
        raise ValueError(
            f"too few observations to fit factor_order={cfg.factor_order} "
            f"({len(train)} rows)"
        )

    model = DynamicFactorMQ(
        train,
        factors=cfg.factors,
        factor_orders=cfg.factor_order,
    )

    results = model.fit(disp=False)

    max_horizon = max(cfg.horizons_q)
    f = results.get_forecast(steps=max_horizon)
    mean_path: "pd.DataFrame" = f.predicted_mean
    se_path: "pd.DataFrame" = f.se_mean

    if cfg.target not in mean_path.columns:
        raise RuntimeError(
            f"DFM did not emit forecast for target {cfg.target!r}; "
            f"got columns {list(mean_path.columns)}"
        )

    rid = _run_id(cfg, train.shape, sm_version)
    country = Country(cfg.country)
    variable = Variable(cfg.target)

    out: list[DensityForecast] = []
    for h in cfg.horizons_q:
        if h > len(mean_path):
            continue
        # Index by integer step (0..max_horizon-1)
        row_idx = h - 1
        mu = float(mean_path[cfg.target].iloc[row_idx])
        se = float(se_path[cfg.target].iloc[row_idx])
        # Forecast period is base_period + h quarters.
        forecast_for = _add_quarters(base_period, h)
        quantiles = _normal_quantiles(mu, se)
        out.append(
            DensityForecast(
                run_id=rid,
                country=country,
                variable=variable,
                horizon_q=h,
                forecast_for_period=forecast_for,
                quantiles=quantiles,
                density_type="normal",
                variant_weights={"opengem_l3_dfm_v0.1": 1.0},
            )
        )

    return out


def _normal_quantiles(mu: float, se: float) -> ForecastQuantiles:
    """Five quantiles assuming a Gaussian forecast distribution.

    Edge case: if se is 0 or nan, fall back to a degenerate distribution
    (all quantiles equal to mu).
    """
    if not math.isfinite(se) or se <= 0:
        return ForecastQuantiles(p10=mu, p25=mu, p50=mu, p75=mu, p90=mu)
    # Standard-normal quantile multipliers for 10/25/50/75/90.
    z = {"p10": -1.2816, "p25": -0.6745, "p50": 0.0, "p75": 0.6745, "p90": 1.2816}
    return ForecastQuantiles(
        p10=mu + z["p10"] * se,
        p25=mu + z["p25"] * se,
        p50=mu + z["p50"] * se,
        p75=mu + z["p75"] * se,
        p90=mu + z["p90"] * se,
    )


def _add_quarters(d: date, n: int) -> date:
    """Add n quarters to the quarter-end date d."""
    # Map a date to (year, quarter), then march n quarters forward.
    q = (d.month - 1) // 3
    total = d.year * 4 + q + n
    new_year, new_q = divmod(total, 4)
    # End-of-quarter month: 3, 6, 9, 12.
    end_month = (new_q + 1) * 3
    # Use day=28 to avoid month-end ambiguity; callers treat this as anchor.
    return date(new_year, end_month, 28)


def fit_us_gdp(
    store: Any,
    vintage_date: str,
) -> list[DensityForecast]:
    """Convenience entry point — the v0.5 milestone forecast call.

    Parameters
    ----------
    store : opengem_vintage.VintageStore-shaped object
        Anything with a ``load_panel(country, codes, vintage)`` method that
        returns a pandas DataFrame keyed by quarter and columned by series code.
    vintage_date : str
        ISO-8601 vintage date string, e.g. "2026-06-06".

    Returns
    -------
    list[DensityForecast]
        Forecasts at horizons (1, 4, 8, 20) quarters ahead.
    """
    cfg = DFMConfig(
        country="US",
        target="gdp_yoy",
        factors=2,
        factor_order=1,
        horizons_q=(1, 4, 8, 20),
        series_codes=(
            "gdp_yoy",
            "cpi_yoy",
            "unemployment",
            "industrial_production_yoy",
            "retail_sales_yoy",
        ),
    )
    panel = store.load_panel(
        country=cfg.country,
        codes=cfg.series_codes,
        vintage=vintage_date,
    )
    base_period = _last_period(panel)
    return fit_dfm(panel, cfg, base_period)


def _last_period(panel: "pd.DataFrame") -> date:
    """Return the last period in the panel as a date."""
    idx = panel.index
    if hasattr(idx[-1], "to_timestamp"):
        ts = idx[-1].to_timestamp(how="end")
    else:
        ts = idx[-1]
    return date(ts.year, ts.month, ts.day if hasattr(ts, "day") else 28)
