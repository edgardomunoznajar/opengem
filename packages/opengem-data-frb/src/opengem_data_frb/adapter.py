"""FRBAdapter — pulls H.15, G.17, H.6 from the FRB DataDownload Program CSV interface."""

from __future__ import annotations

import csv
import io
import logging
from collections.abc import Iterator
from datetime import date

import httpx

from opengem_types import Observation, SeriesId

from opengem_data_base import Adapter, OutageError, RateLimitError, SchemaError, retry
from opengem_data_frb.catalog import FRB_CATALOG

_log = logging.getLogger(__name__)

_FRB_DDP_URL = "https://www.federalreserve.gov/datadownload/Output.aspx"


class FRBAdapter(Adapter):
    """FRB Board DDP adapter.

    No API key required. Returns CSV; we parse it ourselves to keep the package
    dependency-light (no pandas required for ingestion).
    """

    source_id = "FRB"
    catalog = FRB_CATALOG

    def __init__(
        self,
        *,
        client: httpx.Client | None = None,
        base_url: str = _FRB_DDP_URL,
        from_date: date = date(1990, 1, 1),
    ) -> None:
        super().__init__()
        self._client = client if client is not None else httpx.Client(timeout=30.0)
        self._owns_client = client is None
        self._base_url = base_url
        self._from = from_date

    def __enter__(self) -> FRBAdapter:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    @retry(max_attempts=4, base_delay=1.0)
    def pull_series(self, opengem_series_id: SeriesId) -> Iterator[Observation]:
        if opengem_series_id not in self.catalog:
            raise KeyError(f"SeriesId not in FRB catalog: {opengem_series_id}")
        _native, kwargs = self.catalog.native(opengem_series_id)
        release = kwargs["release"]
        series = kwargs["series"]

        params = {
            "rel": release,
            "series": series,
            "from": self._from.strftime("%m/%d/%Y"),
            "to": date.today().strftime("%m/%d/%Y"),
            "filetype": "csv",
            "label": "include",
            "layout": "seriescolumn",
        }

        try:
            resp = self._client.get(self._base_url, params=params)
        except httpx.HTTPError as e:
            raise OutageError(f"FRB HTTP error: {e}", source_id=self.source_id) from e

        if resp.status_code == 429:
            raise RateLimitError("FRB rate-limited", source_id=self.source_id)
        if 500 <= resp.status_code < 600:
            raise OutageError(f"FRB 5xx: {resp.status_code}", source_id=self.source_id)
        if resp.status_code >= 400:
            raise SchemaError(
                f"FRB unexpected {resp.status_code}: {resp.text[:200]}", source_id=self.source_id
            )

        yield from _parse_frb_csv(resp.text, opengem_series_id, self.source_id)


def _parse_frb_csv(text: str, sid: SeriesId, source_id: str) -> Iterator[Observation]:
    """Parse the FRB DDP CSV format.

    DDP CSVs have ~6 header rows, then `Time Period,<series_id>` row, then data rows.
    We seek the row that starts with 'Time Period' and treat everything after as data.
    """
    reader = csv.reader(io.StringIO(text))
    header_seen = False
    for row in reader:
        if not row:
            continue
        if not header_seen:
            if row[0].strip() == "Time Period":
                header_seen = True
            continue
        if len(row) < 2:
            continue
        period_str = row[0].strip()
        val_str = row[1].strip()
        try:
            observed_at = _parse_frb_period(period_str)
        except ValueError:
            continue
        value: float | None
        if val_str in ("", "ND", "NA", "."):
            value = None
        else:
            try:
                value = float(val_str)
            except ValueError:
                value = None
        yield Observation(
            series_id=sid,
            observed_at=observed_at,
            vintage_at=date.today(),
            value=value,
            source=source_id,
            metadata={"raw_period": period_str},
        )


def _parse_frb_period(s: str) -> date:
    """FRB period strings: '2026-04-28' (daily) or '2026-04' (monthly) or '2026' (annual)."""
    if not s:
        raise ValueError("empty period")
    parts = s.split("-")
    if len(parts) == 3:
        return date(int(parts[0]), int(parts[1]), int(parts[2]))
    if len(parts) == 2:
        return date(int(parts[0]), int(parts[1]), 1)
    if len(parts) == 1 and parts[0].isdigit():
        return date(int(parts[0]), 1, 1)
    raise ValueError(f"unrecognized FRB period: {s}")
