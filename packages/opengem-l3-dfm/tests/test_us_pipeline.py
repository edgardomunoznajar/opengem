"""Integration: fit_us_gdp end-to-end through store -> panel -> DFM.

Proves the wiring gap is closed — fit_us_gdp builds a real panel from a vintage
store via opengem_panel and fits a real DynamicFactorMQ. Synthetic series carry
genuine variation so the factor model is identifiable.
"""

from __future__ import annotations

import math
from datetime import date, datetime

import pytest
from opengem_types import Observation, SeriesId, SeriesMeta
from opengem_vintage import SQLiteVintageStore

GDP_SID = "US.BEA.NIPA.GDP_real.Q"
CPI_SID = "US.BLS.CPI.headline_SA.M"


def _q_starts(n: int, y0: int = 2015) -> list[date]:
    out, y, m = [], y0, 1
    for _ in range(n):
        out.append(date(y, m, 1))
        m += 3
        if m > 12:
            m, y = 1, y + 1
    return out


def _m_starts(n: int, y0: int = 2015) -> list[date]:
    out, y, m = [], y0, 1
    for _ in range(n):
        out.append(date(y, m, 1))
        m += 1
        if m > 12:
            m, y = 1, y + 1
    return out


@pytest.fixture()
def us_store() -> SQLiteVintageStore:
    s = SQLiteVintageStore(":memory:")
    s.initialize()
    s.register_source("BEA", "Bureau of Economic Analysis")
    s.register_source("BLS", "Bureau of Labor Statistics")
    for sid, src, kind, freq in [
        (GDP_SID, "BEA", "gdp_real", "Q"),
        (CPI_SID, "BLS", "cpi_headline", "M"),
    ]:
        s.register_series(
            SeriesMeta(
                series_id=SeriesId(sid), source=src, description=f"{src} {kind}",
                unit="index", frequency=freq, country="US", variable_kind=kind,
            )
        )
    vintage = date(2025, 1, 15)

    # 40 quarters of GDP with time-varying growth (a real cycle, not a constant)
    gdp_level, gdp_obs = 100.0, []
    for i, d in enumerate(_q_starts(40)):
        g = 0.010 + 0.004 * math.sin(i / 3.0)
        gdp_level *= 1.0 + g
        gdp_obs.append(Observation(series_id=SeriesId(GDP_SID), observed_at=d,
                                   vintage_at=vintage, value=gdp_level, source="BEA"))
    s.write_batch(gdp_obs, "BEA", datetime(2025, 1, 15, 12, 0))

    cpi_level, cpi_obs = 100.0, []
    for j, d in enumerate(_m_starts(120)):
        infl = 0.0025 + 0.0015 * math.sin(j / 9.0)
        cpi_level *= 1.0 + infl
        cpi_obs.append(Observation(series_id=SeriesId(CPI_SID), observed_at=d,
                                   vintage_at=vintage, value=cpi_level, source="BLS"))
    s.write_batch(cpi_obs, "BLS", datetime(2025, 1, 15, 12, 5))
    yield s
    s.close()


@pytest.mark.integration
def test_fit_us_gdp_end_to_end(us_store: SQLiteVintageStore) -> None:
    pytest.importorskip("statsmodels")
    from opengem_l3_dfm import fit_us_gdp

    out = fit_us_gdp(us_store, "2025-01-15")

    assert len(out) >= 1
    horizons = {f.horizon_q for f in out}
    assert horizons <= {1, 4, 8, 20}
    for f in out:
        assert str(f.country) == "US"
        assert str(f.variable) == "gdp_yoy"
        q = f.quantiles
        assert q.p10 <= q.p25 <= q.p50 <= q.p75 <= q.p90
        assert math.isfinite(q.p50)
