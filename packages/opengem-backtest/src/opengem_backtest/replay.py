"""Rolling-origin backtest over a quarterly panel.

At each origin quarter ``t`` (from ``min_train`` onward) we train every model on
the data available through ``t`` and forecast ``h`` quarters ahead, then score
the forecast against the realized actual ``panel[target][t+h]``.

Models scored:
  - ``opengem_l3_dfm`` — the L3 DynamicFactorMQ (multivariate, uses the panel)
  - ``ar1``            — AR(1) on the target history
  - ``random_walk``    — random walk (no drift) on the target history

Every model is scored the same way: its five reported quantiles -> CRPS via the
quantile-integral form. This keeps the comparison model-agnostic and fair.

NOTE on vintage discipline: this first cut replays over a *single* assembled
panel (one vintage view), so "actuals" are the values in that view, not the
fully-revised-later values. True vintage-correct backtesting replays the store
at each origin's own vintage; that is a documented next step (SSDD-007 full).
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from opengem_backtest.baselines import ar1_density, random_walk_density
from opengem_backtest.metrics import crps_from_quantiles, gaussian_quantiles, pit_value

if TYPE_CHECKING:
    import pandas as pd

# A forecaster: (train_panel, target_column, horizons) -> {horizon: {level: value}}
Forecaster = Callable[["pd.DataFrame", str, Sequence[int]], dict[int, dict[float, float]]]


@dataclass(frozen=True, slots=True)
class ScoredForecast:
    """One model's forecast at one (origin, horizon), scored against the actual."""

    model: str
    origin: str
    horizon_q: int
    target: str
    point: float
    quantiles: dict[float, float] = field(default_factory=dict)
    actual: float = 0.0
    crps: float = 0.0
    abs_error: float = 0.0
    pit: float = 0.0


def _fq_to_dict(fq: Any) -> dict[float, float]:
    return {0.10: fq.p10, 0.25: fq.p25, 0.50: fq.p50, 0.75: fq.p75, 0.90: fq.p90}


def dfm_forecaster(train: pd.DataFrame, target: str, horizons: Sequence[int]) -> dict[int, dict[float, float]]:
    """Fit the L3 DynamicFactorMQ once and return target quantiles per horizon."""
    from opengem_l3_dfm import DFMConfig
    from opengem_l3_dfm.fit import _last_period, fit_dfm

    cfg = DFMConfig(country="US", target=target, factors=1, factor_order=1, horizons_q=tuple(sorted(horizons)))
    out = fit_dfm(train, cfg, _last_period(train))
    return {f.horizon_q: _fq_to_dict(f.quantiles) for f in out}


def ar1_forecaster(train: pd.DataFrame, target: str, horizons: Sequence[int]) -> dict[int, dict[float, float]]:
    dens = ar1_density(train[target].to_numpy(), horizons)
    return {h: gaussian_quantiles(mu, sigma) for h, (mu, sigma) in dens.items()}


def random_walk_forecaster(train: pd.DataFrame, target: str, horizons: Sequence[int]) -> dict[int, dict[float, float]]:
    dens = random_walk_density(train[target].to_numpy(), horizons)
    return {h: gaussian_quantiles(mu, sigma) for h, (mu, sigma) in dens.items()}


DEFAULT_MODELS: dict[str, Forecaster] = {
    "opengem_l3_dfm": dfm_forecaster,
    "ar1": ar1_forecaster,
    "random_walk": random_walk_forecaster,
}


def backtest_panel(
    panel: pd.DataFrame,
    target: str,
    *,
    horizons: Sequence[int] = (1, 4),
    min_train: int = 24,
    max_origins: int | None = None,
    models: dict[str, Forecaster] | None = None,
) -> list[ScoredForecast]:
    """Rolling-origin backtest. Returns one ScoredForecast per (model, origin, horizon)."""
    models = models or DEFAULT_MODELS
    n = len(panel)
    if target not in panel.columns:
        raise ValueError(f"target {target!r} not in panel columns {list(panel.columns)}")
    target_vals = panel[target].to_numpy()

    origins = list(range(min_train - 1, n - 1))
    if max_origins is not None:
        origins = origins[-max_origins:]

    records: list[ScoredForecast] = []
    for t in origins:
        usable_h = [h for h in horizons if t + h < n]
        if not usable_h:
            continue
        train = panel.iloc[: t + 1]
        origin_label = str(panel.index[t])
        for name, forecaster in models.items():
            try:
                forecasts = forecaster(train, target, usable_h)
            except Exception:
                continue
            for h in usable_h:
                q = forecasts.get(h)
                if not q:
                    continue
                actual = float(target_vals[t + h])
                point = float(q[0.50])
                records.append(
                    ScoredForecast(
                        model=name,
                        origin=origin_label,
                        horizon_q=h,
                        target=target,
                        point=point,
                        quantiles=q,
                        actual=actual,
                        crps=crps_from_quantiles(q, actual),
                        abs_error=abs(point - actual),
                        pit=pit_value(q, actual),
                    )
                )
    return records
