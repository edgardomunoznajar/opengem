"""build_panel — assemble a quarterly panel from a vintage-store view.

The transforms are deliberately few and explicit. Each `ColumnSpec` names an
output column, the store series to read, and one of a small set of transforms:

    yoy_q        quarterly levels  -> year-over-year % growth (x / x[-4] - 1)
    yoy_m_to_q   monthly levels    -> quarterly mean, then yoy % growth
    level_q      sub-quarterly     -> quarterly mean (kept as a level)
    level_q_last sub-quarterly     -> quarterly last observation (kept as a level)

Everything aligns on a common quarterly PeriodIndex; rows with any missing
column are dropped so the result is a dense panel ready for DynamicFactorMQ.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import TYPE_CHECKING, Any, Literal

from opengem_vintage.store import VintageView

if TYPE_CHECKING:
    import pandas as pd

Transform = Literal["yoy_q", "yoy_m_to_q", "level_q", "level_q_last"]


@dataclass(frozen=True, slots=True)
class ColumnSpec:
    """One output column of the panel."""

    column: str
    series_id: str
    transform: Transform


# The canonical first US panel: real-GDP growth + headline-CPI inflation, both
# year-over-year, quarterly. Matches the two-series panel the L3 DFM is proven on.
US_GDP_CPI_SPEC: list[ColumnSpec] = [
    ColumnSpec("gdp_yoy", "US.BEA.NIPA.GDP_real.Q", "yoy_q"),
    ColumnSpec("cpi_yoy", "US.BLS.CPI.headline_SA.M", "yoy_m_to_q"),
]


def _import_pandas() -> Any:
    import pandas as pd

    return pd


def _collect(view: VintageView, series_id: str) -> tuple[list[date], list[float]]:
    """Pull (observed_at, value) pairs for one series, skipping nulls."""
    dates: list[date] = []
    values: list[float] = []
    for obs in view.iter_series(series_id):
        if obs.value is None:
            continue
        dates.append(obs.observed_at)
        values.append(float(obs.value))
    return dates, values


def _to_quarterly(pd: Any, dates: list[date], values: list[float], how: str) -> Any:
    """Build a quarter-indexed Series ('mean' or 'last' within each quarter)."""
    s = pd.Series(values, index=pd.to_datetime(dates)).sort_index()
    resampled = s.resample("QE").last() if how == "last" else s.resample("QE").mean()
    resampled.index = resampled.index.to_period("Q")
    return resampled


def _apply_transform(pd: Any, dates: list[date], values: list[float], transform: Transform) -> Any:
    if transform == "yoy_q":
        q = _to_quarterly(pd, dates, values, how="last")
        return 100.0 * (q / q.shift(4) - 1.0)
    if transform == "yoy_m_to_q":
        q = _to_quarterly(pd, dates, values, how="mean")
        return 100.0 * (q / q.shift(4) - 1.0)
    if transform == "level_q":
        return _to_quarterly(pd, dates, values, how="mean")
    if transform == "level_q_last":
        return _to_quarterly(pd, dates, values, how="last")
    raise ValueError(f"unknown transform: {transform!r}")


def build_panel(view: VintageView, specs: list[ColumnSpec]) -> pd.DataFrame:
    """Assemble a dense quarterly panel from a vintage view.

    Parameters
    ----------
    view : VintageView
        An as-of snapshot of the vintage store.
    specs : list[ColumnSpec]
        One spec per output column.

    Returns
    -------
    pandas.DataFrame
        Index is a quarterly ``PeriodIndex``; one column per spec; rows with any
        missing value dropped.

    Raises
    ------
    ValueError
        If a series has no observations in the view, or the assembled panel is
        empty after alignment.
    """
    pd = _import_pandas()
    columns: dict[str, Any] = {}
    for spec in specs:
        dates, values = _collect(view, spec.series_id)
        if not dates:
            raise ValueError(f"no observations for series {spec.series_id!r} in this vintage view")
        columns[spec.column] = _apply_transform(pd, dates, values, spec.transform)

    panel = pd.DataFrame(columns).dropna(how="any")
    if panel.empty:
        raise ValueError("assembled panel is empty after alignment (insufficient overlapping history)")
    return panel
