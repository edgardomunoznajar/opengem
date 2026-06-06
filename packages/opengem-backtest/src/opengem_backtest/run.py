"""End-to-end US pipeline: vintage store -> panel -> backtest -> final forecast.

Offline and store-agnostic: give it any vintage store containing the US GDP/CPI
series and it assembles the panel, backtests the L3 DFM against AR(1) and random
walk, and produces the final density forecast at the latest vintage.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

from opengem_panel import US_GDP_CPI_SPEC, build_panel

from opengem_backtest.leaderboard import leaderboard_rows
from opengem_backtest.replay import backtest_panel


@dataclass(frozen=True, slots=True)
class TargetResult:
    target: str
    leaderboard: list[dict]
    forecasts: list[Any]  # list[DensityForecast]
    n_origins: int


@dataclass(frozen=True, slots=True)
class RunResult:
    vintage_date: str
    panel_quarters: int
    base_period: str
    targets: list[TargetResult] = field(default_factory=list)

    def headline(self, target: str = "gdp_yoy", horizon: str = "1Q") -> dict | None:
        """DFM vs AR(1) vs RW CRPS for one (target, horizon), with a verdict."""
        tr = next((t for t in self.targets if t.target == target), None)
        if tr is None:
            return None
        rows = {r["model"]: r for r in tr.leaderboard if r["horizon"] == horizon}
        dfm, ar1, rw = rows.get("opengem_l3_dfm"), rows.get("ar1"), rows.get("random_walk")
        if not (dfm and ar1 and rw):
            return None
        return {
            "target": target,
            "horizon": horizon,
            "crps_dfm": dfm["crps"],
            "crps_ar1": ar1["crps"],
            "crps_rw": rw["crps"],
            "beats_ar1": dfm["crps"] <= ar1["crps"],
            "beats_rw": dfm["crps"] <= rw["crps"],
            "n": dfm["n"],
        }


def _final_forecast(panel: Any, target: str, horizons: tuple[int, ...]) -> list[Any]:
    from opengem_l3_dfm import DFMConfig
    from opengem_l3_dfm.fit import _last_period, fit_dfm

    from opengem_backtest.replay import DFM_SE_CAP_MULT

    cfg = DFMConfig(country="US", target=target, factors=1, factor_order=1, horizons_q=tuple(sorted(horizons)))
    return fit_dfm(panel, cfg, _last_period(panel), max_se_mult=DFM_SE_CAP_MULT)


def run_us_pipeline(
    store: Any,
    vintage_date: str,
    *,
    targets: tuple[str, ...] = ("gdp_yoy", "cpi_yoy"),
    horizons: tuple[int, ...] = (1, 4),
    min_train: int = 24,
    max_origins: int | None = None,
) -> RunResult:
    """Assemble the US panel as-of ``vintage_date``, backtest, and forecast."""
    view = store.at(date.fromisoformat(vintage_date))
    panel = build_panel(view, US_GDP_CPI_SPEC)
    base_period = str(panel.index[-1])

    target_results: list[TargetResult] = []
    for target in targets:
        records = backtest_panel(
            panel, target, horizons=horizons, min_train=min_train, max_origins=max_origins
        )
        board = leaderboard_rows(records, target)
        forecasts = _final_forecast(panel, target, horizons)
        n_origins = len({r.origin for r in records})
        target_results.append(TargetResult(target, board, forecasts, n_origins))

    return RunResult(
        vintage_date=vintage_date,
        panel_quarters=len(panel),
        base_period=base_period,
        targets=target_results,
    )
