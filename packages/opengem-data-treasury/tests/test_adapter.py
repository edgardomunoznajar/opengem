from __future__ import annotations

from datetime import date

import httpx
import pytest

from opengem_types import SeriesId

from opengem_data_base import OutageError, RateLimitError, SchemaError
from opengem_data_treasury import TreasuryAdapter


def _paginated_client(pages: list[dict]) -> httpx.Client:
    """A MockTransport that returns successive pages based on the page[number] param."""
    state = {"idx": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        page_num = int(request.url.params.get("page[number]", "1"))
        state["idx"] = page_num - 1
        if page_num > len(pages):
            return httpx.Response(200, json={"data": [], "meta": {"total-pages": len(pages)}})
        return httpx.Response(200, json=pages[page_num - 1])

    return httpx.Client(transport=httpx.MockTransport(handler))


def _client_status(status: int, body: str = "") -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, text=body)

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_pull_series_basic() -> None:
    pages = [
        {
            "data": [
                {"record_date": "2026-04-28", "avg_interest_rate_amt": "4.21"},
                {"record_date": "2026-04-29", "avg_interest_rate_amt": "4.18"},
            ],
            "meta": {"total-pages": 1},
        }
    ]
    adapter = TreasuryAdapter(client=_paginated_client(pages))
    obs = list(adapter.pull_series(SeriesId("US.TREAS.YIELDS.10Y.D")))
    assert len(obs) == 2
    assert obs[0].observed_at == date(2026, 4, 28)
    assert obs[0].value == 4.21


def test_pull_series_paginates() -> None:
    pages = [
        {
            "data": [{"record_date": "2026-04-28", "avg_interest_rate_amt": "4.21"}],
            "meta": {"total-pages": 2},
        },
        {
            "data": [{"record_date": "2026-04-29", "avg_interest_rate_amt": "4.18"}],
            "meta": {"total-pages": 2},
        },
    ]
    adapter = TreasuryAdapter(client=_paginated_client(pages))
    obs = list(adapter.pull_series(SeriesId("US.TREAS.YIELDS.10Y.D")))
    assert len(obs) == 2


def test_pull_series_unknown() -> None:
    adapter = TreasuryAdapter(client=_paginated_client([]))
    with pytest.raises(KeyError):
        list(adapter.pull_series(SeriesId("US.TREAS.NOPE.NA.D")))


def test_pull_series_429() -> None:
    adapter = TreasuryAdapter(client=_client_status(429))
    with pytest.raises(RateLimitError):
        list(adapter.pull_series(SeriesId("US.TREAS.YIELDS.10Y.D")))


def test_pull_series_500() -> None:
    adapter = TreasuryAdapter(client=_client_status(500))
    with pytest.raises(OutageError):
        list(adapter.pull_series(SeriesId("US.TREAS.YIELDS.10Y.D")))


def test_pull_series_400() -> None:
    adapter = TreasuryAdapter(client=_client_status(400, "bad params"))
    with pytest.raises(SchemaError):
        list(adapter.pull_series(SeriesId("US.TREAS.YIELDS.10Y.D")))
