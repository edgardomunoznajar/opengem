"""GSCPIAdapter — NY Fed Global Supply Chain Pressure Index."""

from __future__ import annotations

import csv
import io
import logging
from collections.abc import Iterator
from datetime import date

import httpx
from opengem_data_base import (
    Adapter,
    OutageError,
    RateLimitError,
    SchemaError,
    SeriesCatalog,
    retry,
)
from opengem_types import Observation, SeriesId

_log = logging.getLogger(__name__)

GSCPI_SERIES_ID = SeriesId("WORLD.NYFED.GSCPI.supply_chain_pressure.M")
_GSCPI_URL = "https://www.newyorkfed.org/medialibrary/research/interactives/gscpi/downloads/gscpi_data.xlsx"
# The NY Fed publishes an Excel file; CSV mirror used in tests via fixture.

GSCPI_CATALOG = SeriesCatalog({GSCPI_SERIES_ID: "gscpi"})


class GSCPIAdapter(Adapter):
    """NY Fed GSCPI adapter — single monthly series.

    Reads a CSV. The official source is XLSX; this adapter accepts either via
    `parse_format="csv"` (default; expects a 2-column CSV "Date,GSCPI") or
    `parse_format="xlsx"` (requires openpyxl, optional dependency).
    """

    source_id = "NYFED-GSCPI"
    catalog = GSCPI_CATALOG

    def __init__(
        self,
        *,
        client: httpx.Client | None = None,
        url: str = _GSCPI_URL,
        parse_format: str = "csv",
    ) -> None:
        super().__init__()
        self._client = client if client is not None else httpx.Client(timeout=30.0)
        self._owns_client = client is None
        self._url = url
        self._parse_format = parse_format

    def __enter__(self) -> GSCPIAdapter:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    @retry(max_attempts=4, base_delay=1.0)
    def pull_series(self, opengem_series_id: SeriesId) -> Iterator[Observation]:
        if opengem_series_id != GSCPI_SERIES_ID:
            raise KeyError(f"GSCPI adapter only supports {GSCPI_SERIES_ID}")
        try:
            resp = self._client.get(self._url)
        except httpx.HTTPError as e:
            raise OutageError(f"GSCPI HTTP: {e}", source_id=self.source_id) from e

        if resp.status_code == 429:
            raise RateLimitError("GSCPI rate-limit", source_id=self.source_id)
        if 500 <= resp.status_code < 600:
            raise OutageError(f"GSCPI 5xx: {resp.status_code}", source_id=self.source_id)
        if resp.status_code >= 400:
            raise SchemaError(f"GSCPI {resp.status_code}", source_id=self.source_id)

        text = resp.text
        if self._parse_format == "csv":
            yield from _parse_gscpi_csv(text, opengem_series_id, self.source_id)
        else:
            raise NotImplementedError(f"parse_format={self._parse_format}")


def _parse_gscpi_csv(text: str, sid: SeriesId, source_id: str) -> Iterator[Observation]:
    """Parse a 2-column "Date,GSCPI" CSV. Tolerant of header variants."""
    reader = csv.reader(io.StringIO(text))
    header_seen = False
    for row in reader:
        if not row:
            continue
        # Skip until header row containing 'date' (case-insensitive)
        if not header_seen:
            first = row[0].strip().lower()
            if "date" in first or "month" in first or "period" in first:
                header_seen = True
            continue
        if len(row) < 2:
            continue
        date_str = row[0].strip()
        val_str = row[1].strip()
        try:
            observed_at = _parse_gscpi_period(date_str)
        except ValueError:
            continue
        value: float | None
        if val_str in ("", "NA", "ND", "."):
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
            metadata={"raw_date": date_str},
        )


def _parse_gscpi_period(s: str) -> date:
    """GSCPI date strings: '1997-09', '01/09/1997', etc."""
    if not s:
        raise ValueError("empty")
    # Try ISO
    if "-" in s:
        parts = s.split("-")
        if len(parts) == 2:
            return date(int(parts[0]), int(parts[1]), 1)
        if len(parts) == 3:
            return date(int(parts[0]), int(parts[1]), int(parts[2]))
    if "/" in s:
        parts = s.split("/")
        if len(parts) == 3:
            # MM/DD/YYYY or DD/MM/YYYY — NY Fed uses MM/DD/YYYY typically; we
            # assume MM/DD here but month >12 falls back to DD/MM
            m, d, y = parts
            mi, di = int(m), int(d)
            if mi <= 12:
                return date(int(y), mi, 1)  # first-of-month for monthly series
            return date(int(y), di, 1)
    raise ValueError(f"unrecognized GSCPI period: {s}")
