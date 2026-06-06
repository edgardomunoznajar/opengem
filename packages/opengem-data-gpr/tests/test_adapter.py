from __future__ import annotations

from datetime import date

import httpx
import pytest

from opengem_types import SeriesId

from opengem_data_gpr import GPR_CATALOG, GPR_COUNTRIES, GPRAdapter


def _client_text(text: str, status: int = 200) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, text=text)

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_catalog_size() -> None:
    assert len(GPR_COUNTRIES) >= 40
    assert SeriesId("WORLD.GPR.GPR.global.M") in GPR_CATALOG
    assert SeriesId("US.GPR.GPR.country.M") in GPR_CATALOG
    assert SeriesId("RU.GPR.GPR.country.M") in GPR_CATALOG


def test_pull_global_basic() -> None:
    csv = "month,GPR,GPRH\n1985-01,89.5,90.0\n2022-02,250.1,251.0\n"
    adapter = GPRAdapter(client=_client_text(csv))
    obs = list(adapter.pull_series(SeriesId("WORLD.GPR.GPR.global.M")))
    assert len(obs) == 2
    by_date = {o.observed_at: o.value for o in obs}
    assert by_date[date(1985, 1, 1)] == 89.5
    assert by_date[date(2022, 2, 1)] == 250.1


def test_pull_country_wide_csv() -> None:
    csv = "month,GPR_US,GPR_RU,GPR_CN\n2022-01,120.0,180.5,95.0\n2022-02,125.0,200.0,98.5\n"
    adapter = GPRAdapter(client=_client_text(csv))
    obs = list(adapter.pull_series(SeriesId("RU.GPR.GPR.country.M")))
    assert len(obs) == 2
    by_date = {o.observed_at: o.value for o in obs}
    assert by_date[date(2022, 1, 1)] == 180.5
    assert by_date[date(2022, 2, 1)] == 200.0


def test_pull_country_missing_column_silent() -> None:
    """If the requested country isn't a column, we yield nothing."""
    csv = "month,GPR_US\n2022-01,120.0\n"
    adapter = GPRAdapter(client=_client_text(csv))
    obs = list(adapter.pull_series(SeriesId("RU.GPR.GPR.country.M")))
    assert obs == []


def test_pull_unknown_series_rejected() -> None:
    adapter = GPRAdapter(client=_client_text(""))
    with pytest.raises(KeyError):
        list(adapter.pull_series(SeriesId("XX.GPR.GPR.X.M")))
