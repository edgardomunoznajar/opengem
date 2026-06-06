from __future__ import annotations

from datetime import date

import httpx
import pytest
from opengem_data_base import OutageError, RateLimitError, SchemaError
from opengem_data_ordra import ORDRAAdapter
from opengem_data_ordra.adapter import _parse_ordra_period
from opengem_types import SeriesId


def _client(payload: dict, status: int = 200) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, json=payload)

    return httpx.Client(transport=httpx.MockTransport(handler))


def _empty_client(status: int = 200) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, text="")

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_parse_period_quarterly() -> None:
    assert _parse_ordra_period("2026-Q2") == date(2026, 4, 1)
    assert _parse_ordra_period("2026Q3") == date(2026, 7, 1)


def test_parse_period_monthly_with_M() -> None:
    assert _parse_ordra_period("2026-M04") == date(2026, 4, 1)
    assert _parse_ordra_period("2026M04") == date(2026, 4, 1)


def test_parse_period_iso_short() -> None:
    assert _parse_ordra_period("2026-04") == date(2026, 4, 1)


def test_parse_period_iso_full() -> None:
    assert _parse_ordra_period("2026-04-28") == date(2026, 4, 28)


def test_parse_period_invalid() -> None:
    with pytest.raises(ValueError):
        _parse_ordra_period("garbage")


def test_pull_series_basic_with_vintages() -> None:
    """Two observations with their own VINTAGE_DATE dimension."""
    payload = {
        "data": {
            "dataSets": [
                {
                    "observations": {
                        # key index format: TIME:VINTAGE
                        "0:0": [100.0],
                        "0:1": [101.5],  # same observed period, later vintage
                        "1:1": [102.3],
                    }
                }
            ],
            "structures": [
                {
                    "dimensions": {
                        "observation": [
                            {
                                "id": "TIME_PERIOD",
                                "values": [{"id": "2026-Q1"}, {"id": "2026-Q2"}],
                            },
                            {
                                "id": "VINTAGE_DATE",
                                "values": [{"id": "2026-04-28"}, {"id": "2026-05-28"}],
                            },
                        ]
                    }
                }
            ],
        }
    }
    adapter = ORDRAAdapter(client=_client(payload))
    obs = list(adapter.pull_series(SeriesId("US.OECD.MEI.gdp_real.Q")))
    assert len(obs) == 3
    # Find the (2026-Q1, 2026-05-28) → 101.5 observation
    q1_revised = [
        o for o in obs if o.observed_at == date(2026, 1, 1) and o.vintage_at == date(2026, 5, 28)
    ]
    assert len(q1_revised) == 1
    assert q1_revised[0].value == 101.5


def test_pull_series_404_returns_empty() -> None:
    adapter = ORDRAAdapter(client=_empty_client(status=404))
    obs = list(adapter.pull_series(SeriesId("US.OECD.MEI.gdp_real.Q")))
    assert obs == []


def test_pull_series_429() -> None:
    adapter = ORDRAAdapter(client=_empty_client(status=429))
    with pytest.raises(RateLimitError):
        list(adapter.pull_series(SeriesId("US.OECD.MEI.gdp_real.Q")))


def test_pull_series_500() -> None:
    adapter = ORDRAAdapter(client=_empty_client(status=500))
    with pytest.raises(OutageError):
        list(adapter.pull_series(SeriesId("US.OECD.MEI.gdp_real.Q")))


def test_pull_series_400() -> None:
    adapter = ORDRAAdapter(client=_empty_client(status=400))
    with pytest.raises(SchemaError):
        list(adapter.pull_series(SeriesId("US.OECD.MEI.gdp_real.Q")))


def test_pull_series_unknown_series() -> None:
    adapter = ORDRAAdapter(client=_client({}))
    with pytest.raises(KeyError):
        list(adapter.pull_series(SeriesId("XX.OECD.MEI.NOPE.Q")))
