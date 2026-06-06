from __future__ import annotations

from datetime import date

import httpx
import pytest
from opengem_data_base import OutageError, RateLimitError, SchemaError
from opengem_data_bis import BIS_CATALOG, BIS_CBPOL_COUNTRIES, BISAdapter
from opengem_data_bis.adapter import _parse_bis_period
from opengem_types import SeriesId


def _client(payload: dict, status: int = 200) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, json=payload)

    return httpx.Client(transport=httpx.MockTransport(handler))


def _client_status(status: int) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, text="")

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_catalog_size_at_least_40() -> None:
    assert len(BIS_CBPOL_COUNTRIES) >= 40
    assert len(BIS_CATALOG) >= 40


def test_us_in_catalog() -> None:
    assert SeriesId("US.BIS.CBPOL.policy_rate.D") in BIS_CATALOG


def test_parse_period() -> None:
    assert _parse_bis_period("2026-04-28") == date(2026, 4, 28)
    assert _parse_bis_period("2026-04") == date(2026, 4, 1)


def test_pull_series_basic() -> None:
    payload = {
        "data": {
            "dataSets": [
                {"observations": {"0:0": [5.50], "0:1": [5.50], "0:2": [5.25]}}
            ],
            "structures": [
                {
                    "dimensions": {
                        "observation": [
                            {
                                "id": "TIME_PERIOD",
                                "values": [
                                    {"id": "2026-04-26"},
                                    {"id": "2026-04-27"},
                                    {"id": "2026-04-28"},
                                ],
                            }
                        ]
                    }
                }
            ],
        }
    }
    adapter = BISAdapter(client=_client(payload))
    obs = list(adapter.pull_series(SeriesId("US.BIS.CBPOL.policy_rate.D")))
    assert len(obs) == 3
    by_date = {o.observed_at: o.value for o in obs}
    assert by_date[date(2026, 4, 26)] == 5.50
    assert by_date[date(2026, 4, 28)] == 5.25


def test_pull_series_404_empty() -> None:
    adapter = BISAdapter(client=_client_status(404))
    obs = list(adapter.pull_series(SeriesId("US.BIS.CBPOL.policy_rate.D")))
    assert obs == []


def test_pull_series_429() -> None:
    adapter = BISAdapter(client=_client_status(429))
    with pytest.raises(RateLimitError):
        list(adapter.pull_series(SeriesId("US.BIS.CBPOL.policy_rate.D")))


def test_pull_series_500() -> None:
    adapter = BISAdapter(client=_client_status(500))
    with pytest.raises(OutageError):
        list(adapter.pull_series(SeriesId("US.BIS.CBPOL.policy_rate.D")))


def test_pull_series_400() -> None:
    adapter = BISAdapter(client=_client_status(400))
    with pytest.raises(SchemaError):
        list(adapter.pull_series(SeriesId("US.BIS.CBPOL.policy_rate.D")))


def test_pull_series_unknown() -> None:
    adapter = BISAdapter(client=_client({}))
    with pytest.raises(KeyError):
        list(adapter.pull_series(SeriesId("XX.BIS.CBPOL.policy_rate.D")))
