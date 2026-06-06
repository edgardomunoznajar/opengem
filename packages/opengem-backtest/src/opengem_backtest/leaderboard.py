"""Aggregate scored forecasts into leaderboard rows.

A row matches the shape the API (`/v1/leaderboard`) and the dashboard consume:
``{rank, model, indicator, horizon, crps, pit, hit_rate, n, mae}``.

Definitions (all empirical over the backtest's out-of-sample origins):
  - ``crps``      mean CRPS (primary metric, lower is better)
  - ``mae``       mean absolute error of the point (p50)
  - ``hit_rate``  share of actuals inside the 80% band [p10, p90]  (target 0.80)
  - ``pit``       share of actuals inside the 50% band [p25, p75]  (target 0.50)
  - ``n``         number of scored origins
Rows are ranked by CRPS within each (indicator, horizon).
"""

from __future__ import annotations

from collections.abc import Sequence

from opengem_backtest.replay import ScoredForecast


def _horizon_label(h: int) -> str:
    return f"{h}Q"


def leaderboard_rows(records: Sequence[ScoredForecast], indicator: str) -> list[dict]:
    """Aggregate per (model, horizon) and rank by CRPS within each horizon."""
    groups: dict[tuple[str, int], list[ScoredForecast]] = {}
    for r in records:
        groups.setdefault((r.model, r.horizon_q), []).append(r)

    rows: list[dict] = []
    for (model, horizon), recs in groups.items():
        n = len(recs)
        mean_crps = sum(r.crps for r in recs) / n
        mean_mae = sum(r.abs_error for r in recs) / n
        hit80 = sum(1 for r in recs if r.quantiles[0.10] <= r.actual <= r.quantiles[0.90]) / n
        hit50 = sum(1 for r in recs if r.quantiles[0.25] <= r.actual <= r.quantiles[0.75]) / n
        rows.append(
            {
                "model": model,
                "indicator": indicator,
                "horizon": _horizon_label(horizon),
                "horizon_q": horizon,
                "crps": round(mean_crps, 4),
                "mae": round(mean_mae, 4),
                "hit_rate": round(hit80, 3),
                "pit": round(hit50, 3),
                "n": n,
            }
        )

    # rank by CRPS within each horizon
    rows.sort(key=lambda r: (r["horizon_q"], r["crps"]))
    by_h: dict[int, int] = {}
    for row in rows:
        h = row["horizon_q"]
        by_h[h] = by_h.get(h, 0) + 1
        row["rank"] = by_h[h]
    return rows
