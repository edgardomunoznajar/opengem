"""Tests for opengem-panel.build_panel.

Synthetic series with constant growth give closed-form yoy values:
  - GDP at 1%/quarter  -> yoy = 100*(1.01**4 - 1)  = 4.060401 %
  - CPI at 0.5%/month  -> yoy = 100*(1.005**12 - 1) = 6.167781 %
"""

from __future__ import annotations

from datetime import date, datetime

import pytest
from opengem_panel import ColumnSpec, build_panel
from opengem_types import Observation, SeriesId, SeriesMeta
from opengem_vintage import SQLiteVintageStore

GDP_SID = "US.BEA.NIPA.GDP_real.Q"
CPI_SID = "US.BLS.CPI.headline_SA.M"
VINTAGE_AT = date(2025, 1, 15)


def _quarter_starts(n: int, start_year: int = 2022) -> list[date]:
    out = []
    y, m = start_year, 1
    for _ in range(n):
        out.append(date(y, m, 1))
        m += 3
        if m > 12:
            m = 1
            y += 1
    return out


def _month_starts(n: int, start_year: int = 2022) -> list[date]:
    out = []
    y, m = start_year, 1
    for _ in range(n):
        out.append(date(y, m, 1))
        m += 1
        if m > 12:
            m = 1
            y += 1
    return out


@pytest.fixture()
def store() -> SQLiteVintageStore:
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
                series_id=SeriesId(sid),
                source=src,
                description=f"{src} {kind}",
                unit="index",
                frequency=freq,
                country="US",
                variable_kind=kind,
            )
        )

    # 12 quarters of GDP at 1%/quarter
    gdp_obs = [
        Observation(
            series_id=SeriesId(GDP_SID),
            observed_at=d,
            vintage_at=VINTAGE_AT,
            value=100.0 * (1.01**i),
            source="BEA",
        )
        for i, d in enumerate(_quarter_starts(12))
    ]
    s.write_batch(gdp_obs, "BEA", datetime(2025, 1, 15, 12, 0))

    # 36 months of CPI at 0.5%/month
    cpi_obs = [
        Observation(
            series_id=SeriesId(CPI_SID),
            observed_at=d,
            vintage_at=VINTAGE_AT,
            value=100.0 * (1.005**j),
            source="BLS",
        )
        for j, d in enumerate(_month_starts(36))
    ]
    s.write_batch(cpi_obs, "BLS", datetime(2025, 1, 15, 12, 5))
    yield s
    s.close()


def test_build_panel_yoy_values_and_shape(store: SQLiteVintageStore) -> None:
    view = store.at(date(2025, 1, 15))
    panel = build_panel(
        view,
        [
            ColumnSpec("gdp_yoy", GDP_SID, "yoy_q"),
            ColumnSpec("cpi_yoy", CPI_SID, "yoy_m_to_q"),
        ],
    )

    assert list(panel.columns) == ["gdp_yoy", "cpi_yoy"]
    # yoy needs 4 prior quarters; 12 quarters -> 8 dense rows
    assert len(panel) == 8
    assert str(panel.index.freqstr).startswith("Q")
    assert not panel.isna().any().any()

    # closed-form yoy from constant growth
    assert panel["gdp_yoy"].iloc[-1] == pytest.approx(100.0 * (1.01**4 - 1), rel=1e-9)
    assert panel["cpi_yoy"].iloc[-1] == pytest.approx(100.0 * (1.005**12 - 1), rel=1e-6)


def test_build_panel_is_vintage_correct(store: SQLiteVintageStore) -> None:
    # A view from before any data was knowable yields no observations -> ValueError.
    early = store.at(date(2021, 1, 1))
    with pytest.raises(ValueError):
        build_panel(early, [ColumnSpec("gdp_yoy", GDP_SID, "yoy_q")])


def test_build_panel_rejects_unknown_transform(store: SQLiteVintageStore) -> None:
    view = store.at(date(2025, 1, 15))
    with pytest.raises(ValueError):
        build_panel(view, [ColumnSpec("x", GDP_SID, "not_a_transform")])  # type: ignore[arg-type]
