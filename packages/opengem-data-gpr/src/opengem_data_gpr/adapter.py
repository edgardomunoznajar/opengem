"""GPRAdapter — Caldara-Iacoviello Geopolitical Risk Index."""

from __future__ import annotations

import csv
import io
import logging
from collections.abc import Iterator
from datetime import date

import httpx

from opengem_types import Observation, SeriesId

from opengem_data_base import Adapter, OutageError, RateLimitError, SchemaError, retry
from opengem_data_gpr.catalog import GPR_CATALOG

_log = logging.getLogger(__name__)

_GPR_GLOBAL_URL = "https://www.matteoiacoviello.com/gpr_files/data_gpr_export.csv"
_GPR_COUNTRY_URL = "https://www.matteoiacoviello.com/gpr_files/data_gpr_country.csv"


class GPRAdapter(Adapter):
    """Caldara-Iacoviello GPR adapter.

    Two CSV files cover global and country-specific indexes. We fetch one,
    parse, and yield observations for the requested SeriesId.
    """

    source_id = "GPR"
    catalog = GPR_CATALOG

    def __init__(
        self,
        *,
        client: httpx.Client | None = None,
        global_url: str = _GPR_GLOBAL_URL,
        country_url: str = _GPR_COUNTRY_URL,
    ) -> None:
        super().__init__()
        self._client = client if client is not None else httpx.Client(timeout=30.0)
        self._owns_client = client is None
        self._global_url = global_url
        self._country_url = country_url

    def __enter__(self) -> GPRAdapter:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    @retry(max_attempts=4, base_delay=1.0)
    def pull_series(self, opengem_series_id: SeriesId) -> Iterator[Observation]:
        if opengem_series_id not in self.catalog:
            raise KeyError(f"SeriesId not in GPR catalog: {opengem_series_id}")
        _native, kwargs = self.catalog.native(opengem_series_id)
        kind = kwargs["kind"]
        country = kwargs["country"]

        url = self._global_url if kind == "global" else self._country_url

        try:
            resp = self._client.get(url)
        except httpx.HTTPError as e:
            raise OutageError(f"GPR HTTP: {e}", source_id=self.source_id) from e

        if resp.status_code == 429:
            raise RateLimitError("GPR rate-limit", source_id=self.source_id)
        if 500 <= resp.status_code < 600:
            raise OutageError(f"GPR 5xx: {resp.status_code}", source_id=self.source_id)
        if resp.status_code >= 400:
            raise SchemaError(f"GPR {resp.status_code}", source_id=self.source_id)

        if kind == "global":
            yield from _parse_gpr_global(resp.text, opengem_series_id, self.source_id)
        else:
            yield from _parse_gpr_country(resp.text, opengem_series_id, country, self.source_id)


def _parse_date(s: str) -> date:
    """GPR uses 'YYYY-MM' or '01jan1985' style. We handle ISO and FRED-ish."""
    s = s.strip()
    if "-" in s:
        parts = s.split("-")
        if len(parts) == 2:
            return date(int(parts[0]), int(parts[1]), 1)
        if len(parts) == 3:
            return date(int(parts[0]), int(parts[1]), int(parts[2]))
    if "/" in s:
        parts = s.split("/")
        if len(parts) == 3:
            m, d, y = parts
            return date(int(y), int(m), 1)
    raise ValueError(f"unrecognized GPR period: {s}")


def _parse_gpr_global(text: str, sid: SeriesId, source_id: str) -> Iterator[Observation]:
    reader = csv.DictReader(io.StringIO(text))
    for row in reader:
        date_str = row.get("month") or row.get("Month") or row.get("DATE") or row.get("date") or ""
        # Column names vary; the recent index column is typically 'GPR' or 'GPRH'
        val_str = (
            row.get("GPR")
            or row.get("gpr")
            or row.get("GPRH")
            or row.get("GPRC")
            or ""
        )
        if not date_str:
            continue
        try:
            observed_at = _parse_date(date_str)
        except ValueError:
            continue
        value = _safe_float(val_str)
        yield Observation(
            series_id=sid,
            observed_at=observed_at,
            vintage_at=date.today(),
            value=value,
            source=source_id,
            metadata={"row_date": date_str},
        )


def _parse_gpr_country(
    text: str, sid: SeriesId, country: str, source_id: str
) -> Iterator[Observation]:
    """Country GPR CSV is wide-format: month, AR, BR, ..., column per country."""
    reader = csv.DictReader(io.StringIO(text))
    fieldnames = reader.fieldnames or []
    # Find the country column — case-insensitive match on column name
    col = None
    candidates = (
        f"GPR_{country}",
        f"gpr_{country}",
        f"GPR_{country.upper()}",
        country,
        country.upper(),
    )
    for c in candidates:
        if c in fieldnames:
            col = c
            break
    if col is None:
        # Try fuzzy match — any field containing the ISO code
        for f in fieldnames:
            if country.upper() in f.upper():
                col = f
                break
    if col is None:
        return  # country not present in CSV
    date_field = None
    for cand in ("month", "Month", "DATE", "date"):
        if cand in fieldnames:
            date_field = cand
            break
    if date_field is None:
        return

    for row in reader:
        date_str = row.get(date_field, "")
        val_str = row.get(col, "")
        if not date_str:
            continue
        try:
            observed_at = _parse_date(date_str)
        except ValueError:
            continue
        value = _safe_float(val_str)
        yield Observation(
            series_id=sid,
            observed_at=observed_at,
            vintage_at=date.today(),
            value=value,
            source=source_id,
            metadata={"country": country},
        )


def _safe_float(s: str) -> float | None:
    s = s.strip() if s else s
    if not s or s in (".", "NA", "ND", "null"):
        return None
    try:
        return float(s)
    except ValueError:
        return None
