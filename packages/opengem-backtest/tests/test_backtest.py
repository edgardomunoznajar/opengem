"""Integration: rolling-origin backtest + leaderboard over a synthetic panel.

Fits the real L3 DFM at each origin, so this is marked integration. Kept small
(few origins) for speed.
"""

from __future__ import annotations

import math

import pytest
from opengem_backtest import backtest_panel, leaderboard_rows


def _panel():
    pd = pytest.importorskip("pandas")
    idx = pd.period_range("2010Q1", periods=44, freq="Q")
    g, c = [2.0], [1.5]
    for i in range(1, 44):
        g.append(0.70 * g[-1] + 0.6 + 0.3 * math.sin(i / 2.0))
        c.append(0.60 * c[-1] + 0.8 + 0.2 * math.cos(i / 3.0))
    return pd.DataFrame({"gdp_yoy": g, "cpi_yoy": c}, index=idx)


@pytest.mark.integration
def test_backtest_panel_scores_three_models():
    pytest.importorskip("statsmodels")
    panel = _panel()
    records = backtest_panel(
        panel, "gdp_yoy", horizons=(1, 4), min_train=30, max_origins=5
    )
    assert records, "expected scored forecasts"

    models = {r.model for r in records}
    assert models == {"opengem_l3_dfm", "ar1", "random_walk"}

    for r in records:
        assert math.isfinite(r.crps) and r.crps >= 0
        assert math.isfinite(r.point)
        assert 0.0 <= r.pit <= 1.0
        assert r.quantiles[0.10] <= r.quantiles[0.90]


@pytest.mark.integration
def test_leaderboard_rows_ranked_by_crps():
    pytest.importorskip("statsmodels")
    panel = _panel()
    records = backtest_panel(panel, "gdp_yoy", horizons=(1, 4), min_train=30, max_origins=5)
    rows = leaderboard_rows(records, "gdp_yoy")
    assert rows
    # each row has the consumer-facing shape
    for row in rows:
        assert set(row) >= {"rank", "model", "indicator", "horizon", "crps", "pit", "hit_rate", "n", "mae"}
        assert row["indicator"] == "gdp_yoy"
    # within a horizon, rank 1 has the lowest CRPS
    for h in {row["horizon"] for row in rows}:
        hr = sorted((r for r in rows if r["horizon"] == h), key=lambda r: r["rank"])
        assert hr[0]["crps"] == min(r["crps"] for r in hr)
        assert [r["rank"] for r in hr] == list(range(1, len(hr) + 1))
