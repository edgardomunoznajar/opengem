"""TreasuryAdapter — US Treasury FiscalData REST API."""

from __future__ import annotations

import logging
from collections.abc import Iterator
from datetime import date

import httpx

from opengem_types import Observation, SeriesId

from opengem_data_base import Adapter, OutageError, RateLimitError, SchemaError, retry
from opengem_data_treasury.catalog import TREASURY_CATALOG

_log = logging.getLogger(__name__)

_TREAS_BASE_URL = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service"


class TreasuryAdapter(Adapter):
    """Treasury FiscalData adapter. No auth required."""

    source_id = "TREAS"
    catalog = TREASURY_CATALOG

    def __init__(
        self,
        *,
        client: httpx.Client | None = None,
        base_url: str = _TREAS_BASE_URL,
        page_size: int = 1000,
    ) -> None:
        super().__init__()
        self._client = client if client is not None else httpx.Client(timeout=30.0)
        self._owns_client = client is None
        self._base_url = base_url
        self._page_size = page_size

    def __enter__(self) -> TreasuryAdapter:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    @retry(max_attempts=4, base_delay=1.0)
    def pull_series(self, opengem_series_id: SeriesId) -> Iterator[Observation]:
        if opengem_series_id not in self.catalog:
            raise KeyError(f"SeriesId not in Treasury catalog: {opengem_series_id}")
        _native, kwargs = self.catalog.native(opengem_series_id)

        endpoint = kwargs["endpoint"]
        value_field = kwargs["value_field"]
        date_field = kwargs["date_field"]
        flt = kwargs.get("filter", "")

        params: dict[str, str | int] = {
            "fields": f"{date_field},{value_field}",
            "format": "json",
            "page[size]": self._page_size,
            "page[number]": 1,
            "sort": date_field,
        }
        if flt:
            params["filter"] = flt

        page = 1
        while True:
            params["page[number]"] = page
            try:
                resp = self._client.get(self._base_url + endpoint, params=params)
            except httpx.HTTPError as e:
                raise OutageError(f"Treasury HTTP: {e}", source_id=self.source_id) from e

            if resp.status_code == 429:
                raise RateLimitError("Treasury rate-limit", source_id=self.source_id)
            if 500 <= resp.status_code < 600:
                raise OutageError(
                    f"Treasury 5xx: {resp.status_code}", source_id=self.source_id
                )
            if resp.status_code >= 400:
                raise SchemaError(
                    f"Treasury {resp.status_code}: {resp.text[:200]}", source_id=self.source_id
                )

            try:
                doc = resp.json()
            except Exception as e:
                raise SchemaError(f"Treasury non-JSON: {e}", source_id=self.source_id) from e

            for row in doc.get("data", []):
                date_str = row.get(date_field, "")
                val_str = row.get(value_field, "")
                try:
                    observed_at = date.fromisoformat(date_str)
                except (TypeError, ValueError):
                    continue
                value: float | None
                if val_str in (None, "", "null"):
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
                    metadata={"endpoint": endpoint},
                )

            # Pagination
            meta = doc.get("meta", {})
            total_pages = int(meta.get("total-pages", 1))
            if page >= total_pages:
                break
            page += 1
