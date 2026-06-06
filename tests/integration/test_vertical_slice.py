"""End-to-end vertical slice: BEA adapter → vintage store → as-of query → BLS + FRB join.

This is the smallest demonstration that the architecture composes: an adapter
yields Observations conforming to opengem-types; the vintage store accepts them
and computes a deterministic vintage_hash; the as-of query returns the right
values.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import date, datetime

import httpx
import pytest
from opengem_data_bea import BEAAdapter
from opengem_data_bls import BLSAdapter
from opengem_data_frb import FRBAdapter
from opengem_types import SeriesId, SeriesMeta
from opengem_vintage import SQLiteVintageStore


def _mock_bea_client(rows: list[dict]) -> httpx.Client:
    payload = {"BEAAPI": {"Results": {"Data": rows}}}

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload)

    return httpx.Client(transport=httpx.MockTransport(handler))


def _mock_bls_client(series_id: str, rows: list[dict]) -> httpx.Client:
    payload = {
        "status": "REQUEST_SUCCEEDED",
        "Results": {"series": [{"seriesID": series_id, "data": rows}]},
    }

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload)

    return httpx.Client(transport=httpx.MockTransport(handler))


def _mock_frb_client(csv_body: str) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=csv_body)

    return httpx.Client(transport=httpx.MockTransport(handler))


@pytest.fixture()
def store() -> SQLiteVintageStore:
    s = SQLiteVintageStore(":memory:")
    s.initialize()
    s.register_source("BEA", "Bureau of Economic Analysis")
    s.register_source("BLS", "Bureau of Labor Statistics")
    s.register_source("FRB", "Federal Reserve Board")

    # Register all series we'll use
    for sid, src, kind, freq in [
        ("US.BEA.NIPA.GDP_real.Q", "BEA", "gdp_real", "Q"),
        ("US.BLS.CPI.headline_SA.M", "BLS", "cpi_headline", "M"),
        ("US.FRB.H15.DGS10.D", "FRB", "yield_10y", "D"),
    ]:
        s.register_series(
            SeriesMeta(
                series_id=SeriesId(sid),
                source=src,
                description=f"{src} {kind}",
                unit="various",
                frequency=freq,
                country="US",
                variable_kind=kind,
            )
        )
    yield s
    s.close()


def test_three_adapter_end_to_end_roundtrip(store: SQLiteVintageStore) -> None:
    """Pull from BEA + BLS + FRB; persist; query; assert correct values back."""

    # 1) BEA: GDP real
    bea = BEAAdapter(
        api_key="k",
        client=_mock_bea_client(
            [
                {"LineNumber": "1", "TimePeriod": "2026Q1", "DataValue": "23,612.5", "CL_UNIT": "Level"},
                {"LineNumber": "1", "TimePeriod": "2025Q4", "DataValue": "23,500.1", "CL_UNIT": "Level"},
            ]
        ),
    )
    bea_obs = list(bea.pull_series(SeriesId("US.BEA.NIPA.GDP_real.Q")))
    assert len(bea_obs) == 2
    # Adapters stamp vintage_at = date.today() for live pulls; pin it to the pull
    # date so the as-of query below is deterministic regardless of the calendar.
    bea_obs = [replace(o, vintage_at=date(2026, 5, 24)) for o in bea_obs]
    bea_snap = store.write_batch(bea_obs, "BEA", datetime(2026, 5, 24, 6, 0))
    assert bea_snap.observation_count == 2

    # 2) BLS: CPI
    bls = BLSAdapter(
        api_key=None,
        client=_mock_bls_client(
            "CUSR0000SA0",
            [
                {"year": "2026", "period": "M04", "value": "320.5", "periodName": "April"},
                {"year": "2026", "period": "M03", "value": "319.2", "periodName": "March"},
            ],
        ),
    )
    bls_obs = list(bls.pull_series(SeriesId("US.BLS.CPI.headline_SA.M")))
    assert len(bls_obs) == 2
    bls_obs = [replace(o, vintage_at=date(2026, 5, 24)) for o in bls_obs]
    bls_snap = store.write_batch(bls_obs, "BLS", datetime(2026, 5, 24, 6, 5))

    # 3) FRB: 10y yield (CSV)
    frb_csv = (
        "FRB H.15 header\n"
        "another row\n"
        "third\n"
        "Time Period,DGS10\n"
        "2026-05-20,4.22\n"
        "2026-05-21,4.18\n"
        "2026-05-22,4.21\n"
    )
    frb = FRBAdapter(client=_mock_frb_client(frb_csv))
    frb_obs = list(frb.pull_series(SeriesId("US.FRB.H15.DGS10.D")))
    assert len(frb_obs) == 3
    frb_obs = [replace(o, vintage_at=date(2026, 5, 24)) for o in frb_obs]
    frb_snap = store.write_batch(frb_obs, "FRB", datetime(2026, 5, 24, 6, 10))

    # 4) Each snapshot has a distinct vintage_hash
    hashes = {bea_snap.vintage_hash, bls_snap.vintage_hash, frb_snap.vintage_hash}
    assert len(hashes) == 3

    # 5) As-of query: GDP at end of May reflects the latest vintage
    view = store.at(date(2026, 5, 30))
    gdp_q1 = view.latest_value("US.BEA.NIPA.GDP_real.Q", date(2026, 1, 1))
    assert gdp_q1 == 23612.5

    cpi_apr = view.latest_value("US.BLS.CPI.headline_SA.M", date(2026, 4, 1))
    assert cpi_apr == 320.5

    y10 = view.latest_value("US.FRB.H15.DGS10.D", date(2026, 5, 22))
    assert y10 == 4.21

    # 6) iter_series returns ordered series for one series
    gdp_series = list(view.iter_series("US.BEA.NIPA.GDP_real.Q"))
    assert [o.observed_at for o in gdp_series] == [date(2025, 10, 1), date(2026, 1, 1)]


def test_vintage_replay_two_releases_of_same_period(store: SQLiteVintageStore) -> None:
    """A later release of the same period should NOT overwrite the earlier vintage."""

    # First release of 2026Q1 GDP on 2026-04-28: advance estimate
    bea1 = BEAAdapter(
        api_key="k",
        client=_mock_bea_client(
            [{"LineNumber": "1", "TimePeriod": "2026Q1", "DataValue": "23,612.5"}]
        ),
    )
    obs1 = list(bea1.pull_series(SeriesId("US.BEA.NIPA.GDP_real.Q")))
    # Override vintage_at since BEA adapter uses date.today()
    obs1 = [replace(o, vintage_at=date(2026, 4, 28)) for o in obs1]
    store.write_batch(obs1, "BEA", datetime(2026, 4, 28, 14, 0))

    # Second release (revision): 2nd estimate on 2026-05-28 revises Q1
    bea2 = BEAAdapter(
        api_key="k",
        client=_mock_bea_client(
            [{"LineNumber": "1", "TimePeriod": "2026Q1", "DataValue": "23,650.8"}]
        ),
    )
    obs2 = list(bea2.pull_series(SeriesId("US.BEA.NIPA.GDP_real.Q")))
    obs2 = [replace(o, vintage_at=date(2026, 5, 28)) for o in obs2]
    store.write_batch(obs2, "BEA", datetime(2026, 5, 28, 14, 0))

    # As of late April: see the advance estimate
    v_apr = store.at(date(2026, 4, 30))
    assert v_apr.latest_value("US.BEA.NIPA.GDP_real.Q", date(2026, 1, 1)) == 23612.5

    # As of late May: see the revised value
    v_may = store.at(date(2026, 5, 30))
    assert v_may.latest_value("US.BEA.NIPA.GDP_real.Q", date(2026, 1, 1)) == 23650.8
