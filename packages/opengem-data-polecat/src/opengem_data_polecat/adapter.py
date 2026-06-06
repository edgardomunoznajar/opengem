"""POLECATAdapter — pulls Harvard Dataverse POLECAT releases and aggregates.

Per L021–L030 finding (POLECAT = 95% ACLED substitute; CC0 license):

- Source: Harvard Dataverse, dataset 10.7910/DVN/UMVKMS (Cline Center POLECAT).
- Cadence: weekly release as a gzipped TSV.
- Schema: PLOVER-coded events with ISO country code, event_date, quad_class
  (verbal-coop / material-coop / verbal-conflict / material-conflict), and a
  Goldstein-Scale-equivalent score per row.

The adapter pulls the latest release, aggregates to country-month, and yields
Observation rows compatible with the rest of OPENGEM's data plane.

License: CC0 raw, CC-BY-4.0 derived.
"""

from __future__ import annotations

import csv
import gzip
import io
import logging
from collections import defaultdict
from collections.abc import Iterator
from datetime import date

import httpx

from opengem_types import Observation, SeriesId

from opengem_data_base import Adapter, OutageError, RateLimitError, SchemaError, retry
from opengem_data_polecat.catalog import POLECAT_CATALOG

_log = logging.getLogger(__name__)

# Harvard Dataverse "latest release" endpoint for POLECAT. Cline Center publishes
# weekly increments; the latest URL serves the consolidated current archive.
_POLECAT_DATASET_DOI = "10.7910/DVN/UMVKMS"
_POLECAT_LATEST_URL = (
    "https://dataverse.harvard.edu/api/access/datafile/:persistentId"
    f"?persistentId=doi:{_POLECAT_DATASET_DOI}/LATEST&format=original"
)

# PLOVER quad_class codes
_QUAD_VERBAL_COOP = 1
_QUAD_MATERIAL_COOP = 2
_QUAD_VERBAL_CONFLICT = 3
_QUAD_MATERIAL_CONFLICT = 4


class POLECATAdapter(Adapter):
    """POLECAT adapter — country-month composites from raw events."""

    source_id = "POLECAT"
    catalog = POLECAT_CATALOG

    def __init__(
        self,
        *,
        client: httpx.Client | None = None,
        latest_url: str = _POLECAT_LATEST_URL,
    ) -> None:
        super().__init__()
        self._client = client if client is not None else httpx.Client(
            timeout=120.0,
            follow_redirects=True,
        )
        self._owns_client = client is None
        self._latest_url = latest_url
        # Cache the parsed monthly aggregates per (country, kind) — pulled once
        # per adapter run because the source is a single weekly archive.
        self._cache: dict[str, dict[date, float]] | None = None

    def __enter__(self) -> POLECATAdapter:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    @retry(max_attempts=3, base_delay=2.0)
    def _fetch_archive(self) -> bytes:
        try:
            resp = self._client.get(self._latest_url)
        except httpx.HTTPError as e:
            raise OutageError(f"POLECAT HTTP: {e}", source_id=self.source_id) from e
        if resp.status_code == 429:
            raise RateLimitError("POLECAT rate-limit", source_id=self.source_id)
        if 500 <= resp.status_code < 600:
            raise OutageError(f"POLECAT 5xx: {resp.status_code}", source_id=self.source_id)
        if resp.status_code >= 400:
            raise SchemaError(f"POLECAT {resp.status_code}", source_id=self.source_id)
        return resp.content

    def _ensure_parsed(self) -> dict[str, dict[date, float]]:
        if self._cache is not None:
            return self._cache
        raw = self._fetch_archive()
        text = _decompress(raw)
        self._cache = _aggregate(text)
        return self._cache

    @retry(max_attempts=2, base_delay=1.0)
    def pull_series(self, opengem_series_id: SeriesId) -> Iterator[Observation]:
        if opengem_series_id not in self.catalog:
            raise KeyError(f"SeriesId not in POLECAT catalog: {opengem_series_id}")
        _native, kwargs = self.catalog.native(opengem_series_id)
        country = kwargs["country"]
        kind = kwargs["kind"]
        key = f"{country}|{kind}"

        aggregates = self._ensure_parsed()
        if key not in aggregates:
            return

        today = date.today()
        for month, value in sorted(aggregates[key].items()):
            yield Observation(
                series_id=opengem_series_id,
                observed_at=month,
                vintage_at=today,
                value=value,
                source=self.source_id,
                metadata={
                    "country": country,
                    "kind": kind,
                    "source_attribution": "Cline Center POLECAT (Harvard Dataverse)",
                    "doi": _POLECAT_DATASET_DOI,
                },
            )


def _decompress(raw: bytes) -> str:
    """POLECAT archive is typically gzipped TSV. Some releases are plain TSV."""
    if raw[:2] == b"\x1f\x8b":  # gzip magic
        return gzip.decompress(raw).decode("utf-8", errors="replace")
    return raw.decode("utf-8", errors="replace")


def _aggregate(text: str) -> dict[str, dict[date, float]]:
    """Stream the TSV and bin events to (country, kind) monthly aggregates.

    PLOVER fields used:
        country_iso3 — country code, normalize to ISO-3 alpha
        event_date  — YYYY-MM-DD
        quad_class  — 1..4
        goldstein   — Goldstein-Scale-equivalent score, in [-10, +10]

    Output:
        {"USA|event_count": {date(2024,1,1): 312.0, date(2024,2,1): 287.0, ...}, ...}
    """
    reader = csv.DictReader(io.StringIO(text), delimiter="\t")
    out: dict[str, dict[date, float]] = defaultdict(lambda: defaultdict(float))

    for row in reader:
        iso3 = _normalize_iso(row.get("country_iso3") or row.get("iso3") or row.get("country") or "")
        if not iso3:
            continue
        dstr = (row.get("event_date") or row.get("date") or "").strip()
        if not dstr:
            continue
        try:
            d = date.fromisoformat(dstr[:10])
        except ValueError:
            continue
        month_anchor = d.replace(day=1)
        try:
            quad = int(row.get("quad_class") or row.get("quad") or 0)
        except ValueError:
            quad = 0
        try:
            goldstein = float(row.get("goldstein") or row.get("goldstein_scale") or 0.0)
        except ValueError:
            goldstein = 0.0

        out[f"{iso3}|event_count"][month_anchor] += 1
        out[f"{iso3}|goldstein_weighted"][month_anchor] += goldstein
        if quad == _QUAD_MATERIAL_CONFLICT:
            out[f"{iso3}|material_conflict"][month_anchor] += 1
        elif quad == _QUAD_VERBAL_CONFLICT:
            out[f"{iso3}|verbal_conflict"][month_anchor] += 1

    # Convert nested defaultdicts to plain dicts so downstream tests can compare
    # with equality directly.
    return {k: dict(v) for k, v in out.items()}


def _normalize_iso(s: str) -> str:
    """POLECAT typically uses ISO-3 alpha. Handle a few common aliases."""
    s = s.strip().upper()
    if len(s) == 3 and s.isalpha():
        return s
    return ""
