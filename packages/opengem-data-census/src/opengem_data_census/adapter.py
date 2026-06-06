"""CensusAdapter — US Census Bureau timeseries API."""

from __future__ import annotations

import logging
import os
from collections.abc import Iterator
from datetime import date

import httpx
from opengem_data_base import Adapter, OutageError, RateLimitError, SchemaError, retry
from opengem_types import Observation, SeriesId

from opengem_data_census.catalog import CENSUS_CATALOG

_log = logging.getLogger(__name__)

_CENSUS_BASE_URL = "https://api.census.gov/data"


class CensusAdapter(Adapter):
    """Census Bureau timeseries adapter.

    API key is optional but recommended (`CENSUS_API_KEY` env var) for higher limits.
    """

    source_id = "CENSUS"
    catalog = CENSUS_CATALOG

    def __init__(
        self,
        api_key: str | None = None,
        *,
        client: httpx.Client | None = None,
        base_url: str = _CENSUS_BASE_URL,
    ) -> None:
        super().__init__()
        self._api_key = api_key if api_key is not None else os.environ.get("CENSUS_API_KEY")
        self._client = client if client is not None else httpx.Client(timeout=30.0)
        self._owns_client = client is None
        self._base_url = base_url

    def __enter__(self) -> CensusAdapter:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    @retry(max_attempts=4, base_delay=1.0)
    def pull_series(self, opengem_series_id: SeriesId) -> Iterator[Observation]:
        if opengem_series_id not in self.catalog:
            raise KeyError(f"SeriesId not in Census catalog: {opengem_series_id}")
        _native, kwargs = self.catalog.native(opengem_series_id)

        dataset = kwargs["dataset"]
        data_type = kwargs["data_type_code"]
        category = kwargs["category_code"]
        sa = kwargs["seasonally_adj"]

        params: dict[str, str] = {
            "get": "cell_value,time_slot_id,error_data",
            "data_type_code": data_type,
            "category_code": category,
            "seasonally_adj": sa,
            "time": "from+2000-01",
        }
        if self._api_key:
            params["key"] = self._api_key

        try:
            resp = self._client.get(f"{self._base_url}/{dataset}", params=params)
        except httpx.HTTPError as e:
            raise OutageError(f"Census HTTP: {e}", source_id=self.source_id) from e

        if resp.status_code == 429:
            raise RateLimitError("Census rate-limit", source_id=self.source_id)
        if 500 <= resp.status_code < 600:
            raise OutageError(f"Census 5xx: {resp.status_code}", source_id=self.source_id)
        if resp.status_code >= 400:
            raise SchemaError(
                f"Census {resp.status_code}: {resp.text[:200]}", source_id=self.source_id
            )

        try:
            doc = resp.json()
        except Exception as e:
            raise SchemaError(f"Census non-JSON: {e}", source_id=self.source_id) from e

        if not isinstance(doc, list) or len(doc) < 1:
            raise SchemaError("Census payload not a non-empty list", source_id=self.source_id)

        header = doc[0]
        # Census header is something like ["cell_value", "time_slot_id", "error_data",
        # "data_type_code", "time", "category_code", "seasonally_adj"]
        idx = {name: i for i, name in enumerate(header)}
        if "cell_value" not in idx or "time" not in idx:
            raise SchemaError(f"Census missing fields in header: {header}", source_id=self.source_id)

        for row in doc[1:]:
            time_str = row[idx["time"]]
            val_str = row[idx["cell_value"]]
            try:
                observed_at = _parse_census_period(time_str)
            except ValueError:
                continue
            value: float | None
            if val_str in (None, "", "null", "."):
                value = None
            else:
                try:
                    value = float(val_str)
                except ValueError:
                    value = None
            yield Observation(
                series_id=opengem_series_id,
                observed_at=observed_at,
                vintage_at=date.today(),
                value=value,
                source=self.source_id,
                metadata={"data_type": data_type, "category": category},
            )


def _parse_census_period(s: str) -> date:
    """Census time strings: '2026-04' (monthly) or '2026' (annual) or '2026-04-28' (daily)."""
    if not s:
        raise ValueError("empty")
    parts = s.split("-")
    if len(parts) == 3:
        return date(int(parts[0]), int(parts[1]), int(parts[2]))
    if len(parts) == 2:
        return date(int(parts[0]), int(parts[1]), 1)
    if len(parts) == 1 and parts[0].isdigit():
        return date(int(parts[0]), 1, 1)
    raise ValueError(f"unrecognized Census period: {s}")
