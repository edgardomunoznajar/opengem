"""opengem-backtest — rolling-origin replay, scoring, and baselines.

Public API:
    crps_from_quantiles, crps_gaussian, mae, rmse, pit_value  (metrics)
    ar1_density, random_walk_density                          (baselines)
    backtest_panel, ScoredForecast                            (replay)
    leaderboard_rows                                          (leaderboard)
"""

from opengem_backtest.baselines import ar1_density, random_walk_density
from opengem_backtest.leaderboard import leaderboard_rows
from opengem_backtest.metrics import crps_from_quantiles, crps_gaussian, mae, pit_value, rmse
from opengem_backtest.replay import ScoredForecast, backtest_panel

__all__ = [
    "ScoredForecast",
    "ar1_density",
    "backtest_panel",
    "crps_from_quantiles",
    "crps_gaussian",
    "leaderboard_rows",
    "mae",
    "pit_value",
    "random_walk_density",
    "rmse",
]
__version__ = "0.1.0"
