from __future__ import annotations

from datetime import date
from pathlib import Path

import httpx
import pytest
from opengem_data_base import OutageError, RateLimitError, SchemaError
from opengem_data_frb import FRBAdapter
from opengem_data_frb.adapter import _parse_frb_period
from opengem_types import SeriesId

FIXTURES = Path(__file__).parent / "fixtures"


def _client_text(text: str, status: int = 200) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, text=text)

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_parse_period_daily() -> None:
    assert _parse_frb_period("2026-04-28") == date(2026, 4, 28)


def test_parse_period_monthly() -> None:
    assert _parse_frb_period("2026-04") == date(2026, 4, 1)


def test_parse_period_annual() -> None:
    assert _parse_frb_period("2026") == date(2026, 1, 1)


def test_parse_period_invalid() -> None:
    with pytest.raises(ValueError):
        _parse_frb_period("not-a-date")


def test_pull_series_parses_fixture() -> None:
    text = (FIXTURES / "dgs10_sample.csv").read_text()
    adapter = FRBAdapter(client=_client_text(text))
    obs = list(adapter.pull_series(SeriesId("US.FRB.H15.DGS10.D")))
    # 4 data rows; one has ND value -> None
    assert len(obs) == 4
    values = [o.value for o in obs]
    assert values[0] == 4.21
    assert values[2] is None  # ND
    assert values[3] == 4.22


def test_pull_series_unknown_series() -> None:
    adapter = FRBAdapter(client=_client_text(""))
    with pytest.raises(KeyError):
        list(adapter.pull_series(SeriesId("US.FRB.NOPE.NA.D")))


def test_pull_series_429() -> None:
    adapter = FRBAdapter(client=_client_text("", status=429))
    with pytest.raises(RateLimitError):
        list(adapter.pull_series(SeriesId("US.FRB.H15.DGS10.D")))


def test_pull_series_500() -> None:
    adapter = FRBAdapter(client=_client_text("", status=500))
    with pytest.raises(OutageError):
        list(adapter.pull_series(SeriesId("US.FRB.H15.DGS10.D")))


def test_pull_series_400() -> None:
    adapter = FRBAdapter(client=_client_text("Bad params", status=400))
    with pytest.raises(SchemaError):
        list(adapter.pull_series(SeriesId("US.FRB.H15.DGS10.D")))
