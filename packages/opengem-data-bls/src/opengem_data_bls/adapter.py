"""BLSAdapter — BLS Public Data API v2."""

from __future__ import annotations

import logging
import os
from collections.abc import Iterator
from datetime import date

import httpx
from opengem_data_base import Adapter, AuthError, OutageError, RateLimitError, SchemaError, retry
from opengem_types import Observation, SeriesId

from opengem_data_bls.catalog import BLS_CATALOG

_log = logging.getLogger(__name__)

_BLS_BASE_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"


class BLSAdapter(Adapter):
    """BLS adapter using the v2 Public Data API."""

    source_id = "BLS"
    catalog = BLS_CATALOG

    def __init__(
        self,
        api_key: str | None = None,
        *,
        client: httpx.Client | None = None,
        base_url: str = _BLS_BASE_URL,
        start_year: int = 1990,
    ) -> None:
        super().__init__()
        # API key is optional for BLS — without it, max 3 years per request.
        self._api_key = api_key if api_key is not None else os.environ.get("BLS_API_KEY")
        self._client = client if client is not None else httpx.Client(timeout=30.0)
        self._owns_client = client is None
        self._base_url = base_url
        self._start_year = start_year

    def __enter__(self) -> BLSAdapter:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    @retry(max_attempts=4, base_delay=1.0)
    def pull_series(self, opengem_series_id: SeriesId) -> Iterator[Observation]:
        if opengem_series_id not in self.catalog:
            raise KeyError(f"SeriesId not in BLS catalog: {opengem_series_id}")
        native, _kwargs = self.catalog.native(opengem_series_id)

        payload: dict[str, object] = {
            "seriesid": [native],
            "startyear": str(self._start_year),
            "endyear": str(date.today().year),
        }
        if self._api_key:
            payload["registrationkey"] = self._api_key

        try:
            resp = self._client.post(self._base_url, json=payload)
        except httpx.HTTPError as e:
            raise OutageError(f"BLS HTTP error: {e}", source_id=self.source_id) from e

        if resp.status_code == 429:
            raise RateLimitError(
                "BLS rate-limited", source_id=self.source_id, retry_after_seconds=60.0
            )
        if 500 <= resp.status_code < 600:
            raise OutageError(f"BLS 5xx: {resp.status_code}", source_id=self.source_id)

        try:
            data = resp.json()
        except Exception as e:
            raise SchemaError(f"BLS non-JSON response: {e}", source_id=self.source_id) from e

        status = data.get("status")
        if status == "REQUEST_NOT_PROCESSED":
            msgs = data.get("message", [])
            if any("invalid" in str(m).lower() and "key" in str(m).lower() for m in msgs):
                raise AuthError(f"BLS auth: {msgs}", source_id=self.source_id)
            raise SchemaError(f"BLS not processed: {msgs}", source_id=self.source_id)

        if status != "REQUEST_SUCCEEDED":
            raise SchemaError(
                f"BLS unexpected status {status!r}: {data.get('message')}", source_id=self.source_id
            )

        results = data.get("Results", {})
        series_blocks = results.get("series", [])
        if not isinstance(series_blocks, list):
            raise SchemaError("BLS Results.series not a list", source_id=self.source_id)

        for block in series_blocks:
            for row in block.get("data", []):
                try:
                    observed_at = _parse_bls_period(row["year"], row["period"])
                except (KeyError, ValueError):
                    continue
                raw_val = row.get("value")
                value: float | None
                if raw_val in (None, "", "."):
                    value = None
                else:
                    try:
                        value = float(raw_val)
                    except ValueError:
                        value = None
                yield Observation(
                    series_id=opengem_series_id,
                    observed_at=observed_at,
                    vintage_at=date.today(),
                    value=value,
                    source=self.source_id,
                    metadata={
                        "bls_id": native,
                        "period_name": row.get("periodName", ""),
                        "footnotes": ";".join(str(f) for f in row.get("footnotes", []) if f),
                    },
                )


def _parse_bls_period(year: str, period: str) -> date:
    """BLS period codes: M01..M12 (monthly), Q01..Q04 (quarterly), A01 (annual), S01..S03 (semiannual)."""
    y = int(year)
    if period.startswith("M"):
        m = int(period[1:])
        if 1 <= m <= 12:
            return date(y, m, 1)
        if m == 13:  # M13 = annual average
            return date(y, 1, 1)
    if period.startswith("Q"):
        q = int(period[1:])
        if 1 <= q <= 4:
            return date(y, (q - 1) * 3 + 1, 1)
    if period.startswith("A"):
        return date(y, 1, 1)
    if period.startswith("S"):
        s = int(period[1:])
        if 1 <= s <= 2:
            return date(y, (s - 1) * 6 + 1, 1)
    raise ValueError(f"Unrecognized BLS period: {year} {period}")
