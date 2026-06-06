"""BEAAdapter — pulls NIPA observations from BEA's REST API."""

from __future__ import annotations

import logging
import os
from collections.abc import Iterator
from datetime import date

import httpx

from opengem_types import Observation, SeriesId

from opengem_data_base import Adapter, AuthError, OutageError, RateLimitError, SchemaError, retry
from opengem_data_bea.catalog import BEA_CATALOG

_log = logging.getLogger(__name__)

_BEA_BASE_URL = "https://apps.bea.gov/api/data"


class BEAAdapter(Adapter):
    """BEA NIPA adapter.

    Reads `BEA_API_KEY` from the environment unless an explicit key is passed.
    """

    source_id = "BEA"
    catalog = BEA_CATALOG

    def __init__(
        self,
        api_key: str | None = None,
        *,
        client: httpx.Client | None = None,
        base_url: str = _BEA_BASE_URL,
    ) -> None:
        super().__init__()
        key = api_key if api_key is not None else os.environ.get("BEA_API_KEY", "")
        if not key:
            raise AuthError("BEA_API_KEY not set; pass api_key= or set env var", source_id="BEA")
        self._api_key = key
        self._client = client if client is not None else httpx.Client(timeout=30.0)
        self._owns_client = client is None
        self._base_url = base_url

    def __enter__(self) -> BEAAdapter:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    @retry(max_attempts=4, base_delay=1.0)
    def pull_series(self, opengem_series_id: SeriesId) -> Iterator[Observation]:
        """Pull all historical observations for one series."""
        if opengem_series_id not in self.catalog:
            raise KeyError(f"SeriesId not in BEA catalog: {opengem_series_id}")

        _native, kwargs = self.catalog.native(opengem_series_id)
        line = int(kwargs["LineNumber"])

        params: dict[str, str] = {
            "UserID": self._api_key,
            "method": "GetData",
            "ResultFormat": "JSON",
            "Year": "ALL",
            **{k: v for k, v in kwargs.items()},
        }

        try:
            resp = self._client.get(self._base_url, params=params)
        except httpx.HTTPError as e:
            raise OutageError(f"BEA HTTP error: {e}", source_id=self.source_id) from e

        if resp.status_code == 429:
            raise RateLimitError(
                "BEA rate-limited", source_id=self.source_id, retry_after_seconds=60.0
            )
        if 500 <= resp.status_code < 600:
            raise OutageError(f"BEA 5xx: {resp.status_code}", source_id=self.source_id)
        if resp.status_code == 401 or resp.status_code == 403:
            raise AuthError(f"BEA auth failed: {resp.status_code}", source_id=self.source_id)

        try:
            payload = resp.json()
        except Exception as e:
            raise SchemaError(f"BEA non-JSON response: {e}", source_id=self.source_id) from e

        # BEA wraps errors in BEAAPI.Results.Error
        results = payload.get("BEAAPI", {}).get("Results", {})
        if isinstance(results, dict) and "Error" in results:
            err = results["Error"]
            err_desc = err.get("APIErrorDescription", "unknown")
            err_code = err.get("APIErrorCode", "?")
            # Some BEA errors are auth-related; treat 1, 2, 3 as such; rest as schema.
            if err_code in {"1", "2", "3"}:
                raise AuthError(f"BEA error {err_code}: {err_desc}", source_id=self.source_id)
            raise SchemaError(f"BEA error {err_code}: {err_desc}", source_id=self.source_id)

        data = results.get("Data", []) if isinstance(results, dict) else []
        if not isinstance(data, list):
            raise SchemaError("BEA Data field not a list", source_id=self.source_id)

        for row in data:
            try:
                row_line = int(row.get("LineNumber", "-1"))
            except ValueError:
                continue
            if row_line != line:
                continue
            time_period = row.get("TimePeriod", "")
            try:
                observed_at = _parse_bea_period(time_period)
            except ValueError:
                continue
            raw_val = row.get("DataValue")
            value = _parse_value(raw_val) if raw_val else None
            # BEA does not give us release dates per row; vintage = today
            # The caller (orchestrator) is expected to align this to the actual
            # release date when known via release-calendar metadata.
            yield Observation(
                series_id=opengem_series_id,
                observed_at=observed_at,
                vintage_at=date.today(),
                value=value,
                source=self.source_id,
                metadata={
                    "table": kwargs.get("TableName", ""),
                    "line": str(line),
                    "unit": str(row.get("CL_UNIT", "")),
                    "time_period": time_period,
                },
            )

    def health_check(self) -> bool:
        """Hit the BEA dataset-list endpoint as a cheap reachability probe."""
        params = {
            "UserID": self._api_key,
            "method": "GetDataSetList",
            "ResultFormat": "JSON",
        }
        try:
            resp = self._client.get(self._base_url, params=params, timeout=10.0)
        except httpx.HTTPError:
            return False
        return resp.status_code == 200


def _parse_bea_period(period: str) -> date:
    """BEA 'TimePeriod' strings: '2026Q1' / '2026M01' / '2026A' → first day."""
    period = period.strip()
    if not period:
        raise ValueError("empty period")
    if "Q" in period:
        year_str, q_str = period.split("Q")
        q = int(q_str)
        if q < 1 or q > 4:
            raise ValueError(f"bad quarter: {period}")
        return date(int(year_str), (q - 1) * 3 + 1, 1)
    if "M" in period:
        year_str, m_str = period.split("M")
        m = int(m_str)
        if m < 1 or m > 12:
            raise ValueError(f"bad month: {period}")
        return date(int(year_str), m, 1)
    # Annual: '2026'
    if period.isdigit():
        return date(int(period), 1, 1)
    raise ValueError(f"unrecognized BEA period: {period}")


def _parse_value(s: str) -> float | None:
    """BEA returns formatted strings like '23,500.123'. Strip commas; return None on '.'/'(D)'."""
    s = s.strip()
    if s in {"", "(D)", "(NA)", "."}:
        return None
    s = s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None
