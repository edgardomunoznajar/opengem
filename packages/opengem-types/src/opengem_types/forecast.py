"""Forecast records — point and density."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from itertools import pairwise

from opengem_types.country import Country
from opengem_types.variable import Variable


@dataclass(frozen=True, slots=True)
class ForecastQuantiles:
    """Five-quantile representation of a density forecast."""

    p10: float
    p25: float
    p50: float
    p75: float
    p90: float

    def __post_init__(self) -> None:
        qs = [self.p10, self.p25, self.p50, self.p75, self.p90]
        for a, b in pairwise(qs):
            if a > b:
                raise ValueError(f"Quantiles must be monotone non-decreasing, got {qs}")


@dataclass(frozen=True, slots=True)
class Forecast:
    """A point forecast record (no density)."""

    run_id: str
    country: Country
    variable: Variable
    horizon_q: int  # quarters ahead; 1, 4, 8, 20
    forecast_for_period: date
    value: float


@dataclass(frozen=True, slots=True)
class DensityForecast:
    """A density forecast record with quantiles + variant decomposition."""

    run_id: str
    country: Country
    variable: Variable
    horizon_q: int
    forecast_for_period: date
    quantiles: ForecastQuantiles
    density_type: str = "mixture"  # 'mixture', 'normal', 'quantile'
    variant_weights: dict[str, float] = field(default_factory=dict)
