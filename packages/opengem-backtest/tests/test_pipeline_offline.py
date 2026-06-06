"""Offline end-to-end: store -> panel -> backtest -> forecast -> publish.

Proves the whole US pipeline composes without any network, on a synthetic store.
The real-data run (scripts/first_us_forecast.py) is the same code path fed FRED
discovery data instead of this synthetic store.
"""

from __future__ import annotations

import math
import sqlite3
import tempfile
from datetime import date, datetime
from pathlib import Path

import pytest
from opengem_backtest.persist import forecast_records
from opengem_backtest.run import run_us_pipeline
from opengem_types import Observation, SeriesId, SeriesMeta
from opengem_vintage import SQLiteVintageStore

GDP_SID = "US.BEA.NIPA.GDP_real.Q"
CPI_SID = "US.BLS.CPI.headline_SA.M"


def _q(n: int, y0: int = 2005) -> list[date]:
    out, y, m = [], y0, 1
    for _ in range(n):
        out.append(date(y, m, 1))
        m += 3
        if m > 12:
            m, y = 1, y + 1
    return out


def _m(n: int, y0: int = 2005) -> list[date]:
    out, y, m = [], y0, 1
    for _ in range(n):
        out.append(date(y, m, 1))
        m += 1
        if m > 12:
            m, y = 1, y + 1
    return out


def _build_store() -> SQLiteVintageStore:
    s = SQLiteVintageStore(":memory:")
    s.initialize()
    s.register_source("BEA", "Bureau of Economic Analysis")
    s.register_source("BLS", "Bureau of Labor Statistics")
    for sid, src, kind, freq in [(GDP_SID, "BEA", "gdp_real", "Q"), (CPI_SID, "BLS", "cpi_headline", "M")]:
        s.register_series(SeriesMeta(series_id=SeriesId(sid), source=src, description=src,
                                     unit="index", frequency=freq, country="US", variable_kind=kind))
    vintage = date(2025, 1, 15)
    lvl, gdp = 100.0, []
    for i, d in enumerate(_q(80)):
        lvl *= 1.0 + 0.010 + 0.004 * math.sin(i / 3.0)
        gdp.append(Observation(series_id=SeriesId(GDP_SID), observed_at=d, vintage_at=vintage, value=lvl, source="BEA"))
    s.write_batch(gdp, "BEA", datetime(2025, 1, 15, 12, 0))
    lvl, cpi = 100.0, []
    for j, d in enumerate(_m(240)):
        lvl *= 1.0 + 0.0025 + 0.0015 * math.sin(j / 9.0)
        cpi.append(Observation(series_id=SeriesId(CPI_SID), observed_at=d, vintage_at=vintage, value=lvl, source="BLS"))
    s.write_batch(cpi, "BLS", datetime(2025, 1, 15, 12, 5))
    return s


@pytest.mark.integration
def test_us_pipeline_end_to_end_and_publish():
    pytest.importorskip("statsmodels")
    store = _build_store()
    try:
        result = run_us_pipeline(store, "2025-01-15", horizons=(1, 4), min_train=30, max_origins=6)
    finally:
        store.close()

    assert result.panel_quarters > 30
    assert {t.target for t in result.targets} == {"gdp_yoy", "cpi_yoy"}
    for tr in result.targets:
        assert tr.leaderboard
        assert len(tr.forecasts) >= 1

    head = result.headline("gdp_yoy", "1Q")
    assert head is not None
    assert math.isfinite(head["crps_dfm"]) and math.isfinite(head["crps_ar1"])
    assert isinstance(head["beats_ar1"], bool)

    # publish -> queryable forecasts table
    recs: list[dict] = []
    for tr in result.targets:
        recs += forecast_records(tr.forecasts, vintage_id="2025-01-15", base_period=result.base_period)
    assert recs and all("bands" in r and "point" in r for r in recs)

    datasette = pytest.importorskip("opengem_datasette")
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "snap.db"
        datasette.snapshot_to_sqlite(out, vintage=date(2025, 1, 15), forecasts=recs)
        conn = sqlite3.connect(str(out))
        n = conn.execute("SELECT COUNT(*) FROM forecasts").fetchone()[0]
        sample = conn.execute("SELECT country, indicator, horizon, point, p10, p90 FROM forecasts LIMIT 1").fetchone()
        conn.close()
    assert n == len(recs)
    assert sample[0] == "US" and sample[4] <= sample[3] <= sample[5]  # p10 <= point <= p90
