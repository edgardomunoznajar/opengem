from __future__ import annotations

from datetime import date

import httpx
import pytest

from opengem_types import SeriesId

from opengem_data_base import OutageError, RateLimitError, SchemaError
from opengem_data_census import CensusAdapter
from opengem_data_census.adapter import _parse_census_period


def _client(payload: list, status: int = 200) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, json=payload)

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_parse_period_monthly() -> None:
    assert _parse_census_period("2026-04") == date(2026, 4, 1)


def test_parse_period_daily() -> None:
    assert _parse_census_period("2026-04-28") == date(2026, 4, 28)


def test_parse_period_invalid() -> None:
    with pytest.raises(ValueError):
        _parse_census_period("garbage")


def test_pull_series_basic() -> None:
    payload = [
        ["cell_value", "time_slot_id", "error_data", "data_type_code", "time", "category_code"],
        ["123456", "1", "false", "TI", "2026-03", "0"],
        ["124000", "2", "false", "TI", "2026-04", "0"],
    ]
    adapter = CensusAdapter(api_key=None, client=_client(payload))
    obs = list(adapter.pull_series(SeriesId("US.CENSUS.M3.inventories_total.M")))
    assert len(obs) == 2
    assert obs[0].observed_at == date(2026, 3, 1)
    assert obs[0].value == 123456.0


def test_pull_series_missing_value() -> None:
    payload = [
        ["cell_value", "time"],
        ["", "2026-03"],
        ["null", "2026-04"],
    ]
    adapter = CensusAdapter(api_key=None, client=_client(payload))
    obs = list(adapter.pull_series(SeriesId("US.CENSUS.M3.inventories_total.M")))
    assert len(obs) == 2
    assert all(o.value is None for o in obs)


def test_pull_series_unknown() -> None:
    adapter = CensusAdapter(api_key=None, client=_client([]))
    with pytest.raises(KeyError):
        list(adapter.pull_series(SeriesId("US.CENSUS.NOPE.NA.M")))


def test_pull_series_429() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, text="rate limit")

    adapter = CensusAdapter(api_key=None, client=httpx.Client(transport=httpx.MockTransport(handler)))
    with pytest.raises(RateLimitError):
        list(adapter.pull_series(SeriesId("US.CENSUS.M3.inventories_total.M")))


def test_pull_series_500() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="boom")

    adapter = CensusAdapter(api_key=None, client=httpx.Client(transport=httpx.MockTransport(handler)))
    with pytest.raises(OutageError):
        list(adapter.pull_series(SeriesId("US.CENSUS.M3.inventories_total.M")))


def test_pull_series_bad_schema() -> None:
    payload = [["cell_value"], ["1"]]  # missing 'time' column
    adapter = CensusAdapter(api_key=None, client=_client(payload))
    with pytest.raises(SchemaError):
        list(adapter.pull_series(SeriesId("US.CENSUS.M3.inventories_total.M")))
