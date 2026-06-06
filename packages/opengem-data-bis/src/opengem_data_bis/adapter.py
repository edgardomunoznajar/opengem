"""BISAdapter — BIS Data Portal SDMX 2.1 API."""

from __future__ import annotations

import logging
from collections.abc import Iterator
from datetime import date

import httpx

from opengem_types import Observation, SeriesId

from opengem_data_base import Adapter, OutageError, RateLimitError, SchemaError, retry
from opengem_data_bis.catalog import BIS_CATALOG

_log = logging.getLogger(__name__)

_BIS_BASE_URL = "https://stats.bis.org/api/v2/data/dataflow"
_BIS_AGENCY = "BIS"
_BIS_CBPOL_FLOW = "WS_CBPOL_D"
_BIS_FLOW_VERSION = "1.0"


class BISAdapter(Adapter):
    """BIS Data Portal CBPOL adapter."""

    source_id = "BIS"
    catalog = BIS_CATALOG

    def __init__(
        self,
        *,
        client: httpx.Client | None = None,
        base_url: str = _BIS_BASE_URL,
    ) -> None:
        super().__init__()
        self._client = client if client is not None else httpx.Client(timeout=30.0)
        self._owns_client = client is None
        self._base_url = base_url

    def __enter__(self) -> BISAdapter:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    @retry(max_attempts=4, base_delay=1.0)
    def pull_series(self, opengem_series_id: SeriesId) -> Iterator[Observation]:
        if opengem_series_id not in self.catalog:
            raise KeyError(f"SeriesId not in BIS catalog: {opengem_series_id}")
        _native, kwargs = self.catalog.native(opengem_series_id)
        key = kwargs["key"]

        url = f"{self._base_url}/{_BIS_AGENCY}/{_BIS_CBPOL_FLOW}/{_BIS_FLOW_VERSION}/{key}"
        try:
            resp = self._client.get(
                url,
                headers={"Accept": "application/vnd.sdmx.data+json;version=1.0.0"},
                params={"format": "jsondata"},
            )
        except httpx.HTTPError as e:
            raise OutageError(f"BIS HTTP: {e}", source_id=self.source_id) from e

        if resp.status_code == 429:
            raise RateLimitError("BIS rate-limit", source_id=self.source_id)
        if resp.status_code == 404:
            return  # empty series
        if 500 <= resp.status_code < 600:
            raise OutageError(f"BIS 5xx: {resp.status_code}", source_id=self.source_id)
        if resp.status_code >= 400:
            raise SchemaError(
                f"BIS {resp.status_code}: {resp.text[:200]}", source_id=self.source_id
            )

        try:
            doc = resp.json()
        except Exception as e:
            raise SchemaError(f"BIS non-JSON: {e}", source_id=self.source_id) from e

        # SDMX-JSON 1.0
        data_sets = doc.get("data", {}).get("dataSets", [])
        if not data_sets:
            return
        observations = data_sets[0].get("observations", {})
        structure = doc.get("data", {}).get("structures", [{}])[0]
        time_values: list[str] = []
        for d in structure.get("dimensions", {}).get("observation", []):
            if d.get("id", "") in {"TIME_PERIOD", "TIME"}:
                time_values = [v.get("id", "") for v in d.get("values", [])]
                break

        for key_str, vals in observations.items():
            indices = key_str.split(":")
            try:
                time_idx = int(indices[-1])
                t_str = time_values[time_idx] if time_values else ""
                observed_at = _parse_bis_period(t_str)
            except (ValueError, IndexError):
                continue
            value_raw = vals[0] if vals else None
            value: float | None
            try:
                value = float(value_raw) if value_raw is not None else None
            except (TypeError, ValueError):
                value = None
            yield Observation(
                series_id=opengem_series_id,
                observed_at=observed_at,
                vintage_at=date.today(),
                value=value,
                source=self.source_id,
                metadata={"country": kwargs["country"]},
            )


def _parse_bis_period(s: str) -> date:
    """BIS period strings: '2026-04-28' (daily) or '2026-04' (monthly) or '2026' (annual)."""
    if not s:
        raise ValueError("empty")
    parts = s.split("-")
    if len(parts) == 3:
        return date(int(parts[0]), int(parts[1]), int(parts[2]))
    if len(parts) == 2:
        return date(int(parts[0]), int(parts[1]), 1)
    if len(parts) == 1 and parts[0].isdigit():
        return date(int(parts[0]), 1, 1)
    raise ValueError(f"unrecognized BIS period: {s}")
