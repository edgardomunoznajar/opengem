from __future__ import annotations

from datetime import date

import httpx
import pytest
from opengem_data_base import AuthError, OutageError, RateLimitError, SchemaError
from opengem_data_bls import BLSAdapter
from opengem_data_bls.adapter import _parse_bls_period
from opengem_types import SeriesId


def _client_returning(payload: dict, status: int = 200) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, json=payload)

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_parse_period_monthly() -> None:
    assert _parse_bls_period("2026", "M01") == date(2026, 1, 1)
    assert _parse_bls_period("2026", "M12") == date(2026, 12, 1)


def test_parse_period_quarterly() -> None:
    assert _parse_bls_period("2026", "Q03") == date(2026, 7, 1)


def test_parse_period_annual_aggregator_m13() -> None:
    assert _parse_bls_period("2026", "M13") == date(2026, 1, 1)


def test_parse_period_invalid() -> None:
    with pytest.raises(ValueError):
        _parse_bls_period("2026", "X99")


def test_pull_series_parses_basic() -> None:
    payload = {
        "status": "REQUEST_SUCCEEDED",
        "Results": {
            "series": [
                {
                    "seriesID": "CUSR0000SA0",
                    "data": [
                        {"year": "2026", "period": "M04", "value": "320.5", "periodName": "April"},
                        {"year": "2026", "period": "M03", "value": "319.2", "periodName": "March"},
                    ],
                }
            ]
        },
    }
    adapter = BLSAdapter(api_key="test-key", client=_client_returning(payload))
    obs = list(adapter.pull_series(SeriesId("US.BLS.CPI.headline_SA.M")))
    assert len(obs) == 2
    values = sorted(o.value for o in obs)  # type: ignore[type-var]
    assert values == [319.2, 320.5]


def test_pull_series_handles_missing_value() -> None:
    payload = {
        "status": "REQUEST_SUCCEEDED",
        "Results": {
            "series": [
                {
                    "seriesID": "CUSR0000SA0",
                    "data": [{"year": "2026", "period": "M04", "value": ".", "periodName": "April"}],
                }
            ]
        },
    }
    adapter = BLSAdapter(api_key="test-key", client=_client_returning(payload))
    obs = list(adapter.pull_series(SeriesId("US.BLS.CPI.headline_SA.M")))
    assert len(obs) == 1
    assert obs[0].value is None


def test_pull_series_rejects_unknown_series_id() -> None:
    adapter = BLSAdapter(api_key="test-key", client=_client_returning({}))
    with pytest.raises(KeyError):
        list(adapter.pull_series(SeriesId("US.BLS.NOPE.NA.M")))


def test_pull_series_429() -> None:
    adapter = BLSAdapter(api_key="test-key", client=_client_returning({}, status=429))
    with pytest.raises(RateLimitError):
        list(adapter.pull_series(SeriesId("US.BLS.CPI.headline_SA.M")))


def test_pull_series_500() -> None:
    adapter = BLSAdapter(api_key="test-key", client=_client_returning({}, status=500))
    with pytest.raises(OutageError):
        list(adapter.pull_series(SeriesId("US.BLS.CPI.headline_SA.M")))


def test_pull_series_invalid_key_envelope() -> None:
    payload = {
        "status": "REQUEST_NOT_PROCESSED",
        "message": ["Invalid registration key."],
    }
    adapter = BLSAdapter(api_key="test-key", client=_client_returning(payload))
    with pytest.raises(AuthError):
        list(adapter.pull_series(SeriesId("US.BLS.CPI.headline_SA.M")))


def test_pull_series_request_not_processed_other() -> None:
    payload = {
        "status": "REQUEST_NOT_PROCESSED",
        "message": ["Series does not exist for series CUSR000XXXX."],
    }
    adapter = BLSAdapter(api_key="test-key", client=_client_returning(payload))
    with pytest.raises(SchemaError):
        list(adapter.pull_series(SeriesId("US.BLS.CPI.headline_SA.M")))


def test_pull_series_without_api_key_allowed() -> None:
    payload = {
        "status": "REQUEST_SUCCEEDED",
        "Results": {"series": [{"seriesID": "X", "data": []}]},
    }
    adapter = BLSAdapter(api_key=None, client=_client_returning(payload))
    obs = list(adapter.pull_series(SeriesId("US.BLS.CPI.headline_SA.M")))
    assert obs == []
