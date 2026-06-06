from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import httpx
import pytest
from opengem_data_base import AuthError, OutageError, RateLimitError, SchemaError
from opengem_data_bea import BEAAdapter
from opengem_data_bea.adapter import _parse_bea_period, _parse_value
from opengem_types import SeriesId

FIXTURES = Path(__file__).parent / "fixtures"


def _client_returning(payload: dict, status: int = 200) -> httpx.Client:
    """Build an httpx.Client whose every request returns the canned payload."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, json=payload)

    transport = httpx.MockTransport(handler)
    return httpx.Client(transport=transport)


# ---------------- parse helpers ----------------


def test_parse_period_quarterly() -> None:
    assert _parse_bea_period("2026Q1") == date(2026, 1, 1)
    assert _parse_bea_period("2024Q4") == date(2024, 10, 1)


def test_parse_period_monthly() -> None:
    assert _parse_bea_period("2026M03") == date(2026, 3, 1)
    assert _parse_bea_period("2026M12") == date(2026, 12, 1)


def test_parse_period_annual() -> None:
    assert _parse_bea_period("2026") == date(2026, 1, 1)


@pytest.mark.parametrize("bad", ["", "2026Q5", "2026M13", "garbage"])
def test_parse_period_invalid(bad: str) -> None:
    with pytest.raises(ValueError):
        _parse_bea_period(bad)


def test_parse_value_basic() -> None:
    assert _parse_value("23,500.123") == 23500.123
    assert _parse_value("0.5") == 0.5
    assert _parse_value("(D)") is None
    assert _parse_value("(NA)") is None
    assert _parse_value(".") is None
    assert _parse_value("garbage") is None


# ---------------- adapter behavior ----------------


def test_init_without_key_raises() -> None:
    with pytest.raises(AuthError, match="BEA_API_KEY"):
        BEAAdapter(api_key="")


def test_pull_series_parses_fixture() -> None:
    payload = json.loads((FIXTURES / "gdp_real_response.json").read_text())
    client = _client_returning(payload)

    adapter = BEAAdapter(api_key="test-key", client=client)
    obs = list(adapter.pull_series(SeriesId("US.BEA.NIPA.GDP_real.Q")))

    # Two GDP rows in the fixture (LineNumber=1); PCE row (LineNumber=2) filtered out
    assert len(obs) == 2
    assert obs[0].observed_at == date(2025, 10, 1)
    assert obs[0].value == 23500.123
    assert obs[1].observed_at == date(2026, 1, 1)
    assert obs[1].value == 23612.508


def test_pull_series_rejects_unknown_series_id() -> None:
    adapter = BEAAdapter(api_key="test-key", client=_client_returning({}))
    with pytest.raises(KeyError):
        list(adapter.pull_series(SeriesId("US.BEA.NIPA.NOT_REAL.Q")))


def test_pull_series_handles_429() -> None:
    client = _client_returning({}, status=429)
    adapter = BEAAdapter(api_key="test-key", client=client)
    with pytest.raises(RateLimitError):
        # retry will exhaust attempts; but base delay 0 keeps test fast
        # We don't want long retries, so directly call the underlying via no-retry path
        # is tricky; instead test that the wrapper eventually raises.
        list(adapter.pull_series(SeriesId("US.BEA.NIPA.GDP_real.Q")))


def test_pull_series_handles_500() -> None:
    client = _client_returning({}, status=500)
    adapter = BEAAdapter(api_key="test-key", client=client)
    with pytest.raises(OutageError):
        list(adapter.pull_series(SeriesId("US.BEA.NIPA.GDP_real.Q")))


def test_pull_series_handles_auth_failure() -> None:
    client = _client_returning({}, status=401)
    adapter = BEAAdapter(api_key="test-key", client=client)
    with pytest.raises(AuthError):
        list(adapter.pull_series(SeriesId("US.BEA.NIPA.GDP_real.Q")))


def test_pull_series_handles_bea_error_envelope() -> None:
    payload = {
        "BEAAPI": {
            "Results": {
                "Error": {"APIErrorCode": "4", "APIErrorDescription": "Unknown TableName"}
            }
        }
    }
    client = _client_returning(payload)
    adapter = BEAAdapter(api_key="test-key", client=client)
    with pytest.raises(SchemaError, match="Unknown TableName"):
        list(adapter.pull_series(SeriesId("US.BEA.NIPA.GDP_real.Q")))
