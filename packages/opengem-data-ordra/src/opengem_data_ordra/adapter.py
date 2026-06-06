"""ORDRAAdapter — OECD ORDRA via the SDMX 2.1 API at sdmx.oecd.org.

Note: ORDRA is a Tier-1 strategic source; vintage_at is *read from the API row*
rather than set to today. Each release-month carries its own snapshot.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from datetime import date

import httpx

from opengem_types import Observation, SeriesId

from opengem_data_base import Adapter, OutageError, RateLimitError, SchemaError, retry
from opengem_data_ordra.catalog import ORDRA_CATALOG

_log = logging.getLogger(__name__)

_OECD_SDMX_BASE = "https://sdmx.oecd.org/public/rest/data"


class ORDRAAdapter(Adapter):
    """OECD ORDRA SDMX adapter.

    Uses generic JSON output from the OECD SDMX 2.1 endpoint. The MEI:revisions
    dataflow includes a ``VINTAGE_DATE`` dimension per observation; we map that
    to ``Observation.vintage_at``.
    """

    source_id = "OECD-ORDRA"
    catalog = ORDRA_CATALOG

    def __init__(
        self,
        *,
        client: httpx.Client | None = None,
        base_url: str = _OECD_SDMX_BASE,
        dataflow: str = "OECD.SDD.NAD,DSD_NAMAIN1@DF_QNA,1.0",
    ) -> None:
        super().__init__()
        self._client = client if client is not None else httpx.Client(timeout=60.0)
        self._owns_client = client is None
        self._base_url = base_url
        self._dataflow = dataflow

    def __enter__(self) -> ORDRAAdapter:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    @retry(max_attempts=4, base_delay=2.0)
    def pull_series(self, opengem_series_id: SeriesId) -> Iterator[Observation]:
        if opengem_series_id not in self.catalog:
            raise KeyError(f"SeriesId not in ORDRA catalog: {opengem_series_id}")
        _native, kwargs = self.catalog.native(opengem_series_id)
        country = kwargs["country"]
        subject = kwargs["subject"]
        measure = kwargs["measure"]
        frequency = kwargs["frequency"]

        # SDMX 2.1 query format: <dataflow>/<key>?...
        # MEI key: <FREQUENCY>.<LOCATION>.<SUBJECT>.<MEASURE>
        key = f"{frequency}.{country}.{subject}.{measure}"
        url = f"{self._base_url}/{self._dataflow}/{key}"

        params = {
            "format": "jsondata",
            "dimensionAtObservation": "AllDimensions",
        }
        try:
            resp = self._client.get(url, params=params, headers={"Accept": "application/vnd.sdmx.data+json;version=1.0.0"})
        except httpx.HTTPError as e:
            raise OutageError(f"ORDRA HTTP: {e}", source_id=self.source_id) from e

        if resp.status_code == 429:
            raise RateLimitError("ORDRA rate-limit", source_id=self.source_id)
        if resp.status_code == 404:
            # Empty series; not an error
            return
        if 500 <= resp.status_code < 600:
            raise OutageError(f"ORDRA 5xx: {resp.status_code}", source_id=self.source_id)
        if resp.status_code >= 400:
            raise SchemaError(
                f"ORDRA {resp.status_code}: {resp.text[:200]}", source_id=self.source_id
            )

        try:
            doc = resp.json()
        except Exception as e:
            raise SchemaError(f"ORDRA non-JSON: {e}", source_id=self.source_id) from e

        # SDMX-JSON 1.0.0 structure: data.dataSets[0].observations
        # keyed by dimension index tuple like "0:0:0:0"
        data_sets = doc.get("data", {}).get("dataSets", [])
        if not data_sets:
            return
        observations = data_sets[0].get("observations", {})

        # Time dimension values are indexed in structure.dimensions.observation
        structure = doc.get("data", {}).get("structures", [{}])[0]
        obs_dims = structure.get("dimensions", {}).get("observation", [])
        time_dim_values = []
        vintage_dim_values = []
        for d in obs_dims:
            d_id = d.get("id", "")
            if d_id in {"TIME_PERIOD", "TIME"}:
                time_dim_values = [v.get("id", "") for v in d.get("values", [])]
            elif d_id in {"VINTAGE_DATE", "VINTAGE_PERIOD", "REPORTING_DATE"}:
                vintage_dim_values = [v.get("id", "") for v in d.get("values", [])]

        for key_str, vals in observations.items():
            indices = key_str.split(":")
            try:
                time_idx = int(indices[-2]) if vintage_dim_values else int(indices[-1])
                time_str = time_dim_values[time_idx] if time_dim_values else ""
                observed_at = _parse_ordra_period(time_str)
            except (ValueError, IndexError):
                continue
            # Vintage: read from vintage dimension if present, else use today
            vintage_at = date.today()
            if vintage_dim_values:
                try:
                    v_idx = int(indices[-1])
                    v_str = vintage_dim_values[v_idx]
                    vintage_at = _parse_ordra_period(v_str)
                except (ValueError, IndexError):
                    pass
            # Vintage must be >= observed
            if vintage_at < observed_at:
                vintage_at = observed_at
            value_raw = vals[0] if vals else None
            value: float | None
            if value_raw is None:
                value = None
            else:
                try:
                    value = float(value_raw)
                except (TypeError, ValueError):
                    value = None
            yield Observation(
                series_id=opengem_series_id,
                observed_at=observed_at,
                vintage_at=vintage_at,
                value=value,
                source=self.source_id,
                metadata={"subject": subject, "measure": measure, "country": country},
            )


def _parse_ordra_period(s: str) -> date:
    """ORDRA period strings: '2026-Q1', '2026-04', '2026', or '2026-04-28'."""
    if not s:
        raise ValueError("empty")
    s = s.replace("-Q", "Q").replace("-M", "M")
    if "Q" in s:
        y_str, q_str = s.split("Q")
        y, q = int(y_str), int(q_str)
        if q < 1 or q > 4:
            raise ValueError(s)
        return date(y, (q - 1) * 3 + 1, 1)
    if "M" in s:
        y_str, m_str = s.split("M")
        return date(int(y_str), int(m_str), 1)
    parts = s.split("-")
    if len(parts) == 3:
        return date(int(parts[0]), int(parts[1]), int(parts[2]))
    if len(parts) == 2:
        return date(int(parts[0]), int(parts[1]), 1)
    if len(parts) == 1 and parts[0].isdigit():
        return date(int(parts[0]), 1, 1)
    raise ValueError(f"unrecognized ORDRA period: {s}")
