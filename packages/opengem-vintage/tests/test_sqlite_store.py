from __future__ import annotations

from datetime import date, datetime

import pytest

from opengem_types import Observation, SeriesId, SeriesMeta

from opengem_vintage import SQLiteVintageStore


def _meta(sid: str) -> SeriesMeta:
    return SeriesMeta(
        series_id=SeriesId(sid),
        source="BEA",
        description="Real GDP",
        unit="bil chained",
        frequency="Q",
        country="US",
        variable_kind="gdp_real",
        source_native_id="T10101.L1",
    )


def _obs(sid: str, observed: date, vintage: date, value: float | None) -> Observation:
    return Observation(
        series_id=SeriesId(sid),
        observed_at=observed,
        vintage_at=vintage,
        value=value,
        source="BEA",
    )


@pytest.fixture()
def store() -> SQLiteVintageStore:
    s = SQLiteVintageStore(":memory:")
    s.initialize()
    s.register_source("BEA", "Bureau of Economic Analysis", "https://apps.bea.gov/api/data")
    s.register_series(_meta("US.BEA.NIPA.GDP_real.Q"))
    yield s
    s.close()


def test_initialize_idempotent() -> None:
    s = SQLiteVintageStore(":memory:")
    s.initialize()
    s.initialize()  # second call must not error
    s.close()


def test_write_batch_basic(store: SQLiteVintageStore) -> None:
    obs = [
        _obs("US.BEA.NIPA.GDP_real.Q", date(2026, 1, 1), date(2026, 4, 28), 23500.0),
    ]
    snap = store.write_batch(obs, source_id="BEA", pulled_at=datetime(2026, 4, 28, 14, 0))
    assert snap.observation_count == 1
    assert snap.vintage_hash.startswith("sha256:")


def test_vintage_view_returns_latest_known(store: SQLiteVintageStore) -> None:
    # Three releases of the same reference period
    obs1 = _obs("US.BEA.NIPA.GDP_real.Q", date(2026, 1, 1), date(2026, 4, 28), 23500.0)
    obs2 = _obs("US.BEA.NIPA.GDP_real.Q", date(2026, 1, 1), date(2026, 5, 28), 23510.0)
    obs3 = _obs("US.BEA.NIPA.GDP_real.Q", date(2026, 1, 1), date(2026, 6, 28), 23520.0)
    store.write_batch([obs1], "BEA", datetime(2026, 4, 28))
    store.write_batch([obs2], "BEA", datetime(2026, 5, 28))
    store.write_batch([obs3], "BEA", datetime(2026, 6, 28))

    # As of 2026-04-30 → first vintage only
    v_apr = store.at(date(2026, 4, 30))
    assert v_apr.latest_value("US.BEA.NIPA.GDP_real.Q", date(2026, 1, 1)) == 23500.0

    # As of 2026-05-29 → second vintage
    v_may = store.at(date(2026, 5, 29))
    assert v_may.latest_value("US.BEA.NIPA.GDP_real.Q", date(2026, 1, 1)) == 23510.0

    # As of 2026-07-01 → third vintage
    v_jul = store.at(date(2026, 7, 1))
    assert v_jul.latest_value("US.BEA.NIPA.GDP_real.Q", date(2026, 1, 1)) == 23520.0


def test_vintage_view_before_any_release_returns_none(store: SQLiteVintageStore) -> None:
    obs = _obs("US.BEA.NIPA.GDP_real.Q", date(2026, 1, 1), date(2026, 4, 28), 23500.0)
    store.write_batch([obs], "BEA", datetime(2026, 4, 28))

    v_early = store.at(date(2026, 4, 27))
    assert v_early.latest_value("US.BEA.NIPA.GDP_real.Q", date(2026, 1, 1)) is None


def test_write_batch_atomic_on_duplicate(store: SQLiteVintageStore) -> None:
    """Writing the same (series, observed_at, vintage_at) twice must not corrupt the store."""
    obs = _obs("US.BEA.NIPA.GDP_real.Q", date(2026, 1, 1), date(2026, 4, 28), 23500.0)
    store.write_batch([obs], "BEA", datetime(2026, 4, 28))
    # Same primary key — ON CONFLICT DO NOTHING
    store.write_batch([obs], "BEA", datetime(2026, 4, 28))

    v = store.at(date(2026, 5, 1))
    assert v.latest_value("US.BEA.NIPA.GDP_real.Q", date(2026, 1, 1)) == 23500.0


def test_iter_series_ordered(store: SQLiteVintageStore) -> None:
    obs = [
        _obs("US.BEA.NIPA.GDP_real.Q", date(2025, 10, 1), date(2026, 1, 30), 23200.0),
        _obs("US.BEA.NIPA.GDP_real.Q", date(2026, 1, 1), date(2026, 4, 28), 23500.0),
        _obs("US.BEA.NIPA.GDP_real.Q", date(2026, 4, 1), date(2026, 7, 28), 23700.0),
    ]
    store.write_batch(obs, "BEA", datetime(2026, 7, 28))

    v = store.at(date(2026, 8, 1))
    series = list(v.iter_series("US.BEA.NIPA.GDP_real.Q"))
    assert len(series) == 3
    assert [o.observed_at for o in series] == sorted(o.observed_at for o in series)
