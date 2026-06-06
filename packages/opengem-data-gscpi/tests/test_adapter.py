from __future__ import annotations

from datetime import date

import httpx
import pytest
from opengem_data_base import OutageError
from opengem_data_gscpi import GSCPIAdapter
from opengem_data_gscpi.adapter import GSCPI_SERIES_ID
from opengem_types import SeriesId


def _client_text(text: str, status: int = 200) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, text=text)

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_pull_series_basic_csv() -> None:
    csv = "Date,GSCPI\n1997-09,0.0\n1997-10,0.12\n2022-01,4.31\n2026-04,-0.5\n"
    adapter = GSCPIAdapter(client=_client_text(csv))
    obs = list(adapter.pull_series(GSCPI_SERIES_ID))
    assert len(obs) == 4
    by_date = {o.observed_at: o.value for o in obs}
    assert by_date[date(1997, 9, 1)] == 0.0
    assert by_date[date(2022, 1, 1)] == 4.31
    assert by_date[date(2026, 4, 1)] == -0.5


def test_pull_series_handles_us_dates() -> None:
    csv = "Date,GSCPI\n04/01/2026,-0.5\n"
    adapter = GSCPIAdapter(client=_client_text(csv))
    obs = list(adapter.pull_series(GSCPI_SERIES_ID))
    assert len(obs) == 1
    assert obs[0].observed_at == date(2026, 4, 1)
    assert obs[0].value == -0.5


def test_pull_series_missing_value() -> None:
    csv = "Date,GSCPI\n2026-04,NA\n2026-05,.\n"
    adapter = GSCPIAdapter(client=_client_text(csv))
    obs = list(adapter.pull_series(GSCPI_SERIES_ID))
    assert len(obs) == 2
    assert all(o.value is None for o in obs)


def test_pull_series_rejects_wrong_series() -> None:
    adapter = GSCPIAdapter(client=_client_text("Date,GSCPI\n"))
    with pytest.raises(KeyError):
        list(adapter.pull_series(SeriesId("XX.NYFED.GSCPI.X.M")))


def test_pull_series_outage() -> None:
    adapter = GSCPIAdapter(client=_client_text("", status=503))
    with pytest.raises(OutageError):
        list(adapter.pull_series(GSCPI_SERIES_ID))
