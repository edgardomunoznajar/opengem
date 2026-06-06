"""Write a self-contained OPENGEM vintage snapshot to SQLite.

The output database has four canonical tables:

- ``observations`` — raw upstream-agency observations
- ``forecasts``   — published forecasts at this vintage
- ``scenarios``   — currently-triggered scenarios
- ``misses``      — historically-scored forecasts that fell outside their 80% band

Plus a ``meta`` table with the vintage timestamp, git_sha, container_digest, etc.

The schema is intentionally flat and SQL-queryable from the Datasette UI; no JSON
columns where columnar would do. Datasette + DuckDB-WASM client-side then operate
over this without surprises.

Per L076 / MIDPOINT-FINDINGS finding #1.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterable, Mapping
from dataclasses import asdict, is_dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


# Canonical schema. We use the same column order as Datasette renders, so the
# UI is readable without a custom view.
_DDL_OBSERVATIONS = """
CREATE TABLE observations (
    series_id     TEXT NOT NULL,
    observed_at   TEXT NOT NULL,    -- ISO date
    vintage_at    TEXT NOT NULL,
    value         REAL,
    source        TEXT NOT NULL,
    country       TEXT,
    metadata_json TEXT,
    PRIMARY KEY (series_id, observed_at, vintage_at)
);
CREATE INDEX idx_obs_country ON observations(country);
CREATE INDEX idx_obs_source ON observations(source);
"""

_DDL_FORECASTS = """
CREATE TABLE forecasts (
    vintage_id           TEXT NOT NULL,
    model_id             TEXT NOT NULL,
    model_card_url       TEXT,
    country              TEXT NOT NULL,
    indicator            TEXT NOT NULL,
    horizon              TEXT NOT NULL,
    base_period          TEXT NOT NULL,
    scoring_period       TEXT NOT NULL,
    point                REAL NOT NULL,
    p10                  REAL NOT NULL,
    p50                  REAL NOT NULL,
    p90                  REAL NOT NULL,
    weo                  REAL,
    oecd_eo              REAL,
    frb_sep              REAL,
    ecb_spf              REAL,
    git_sha              TEXT,
    container_digest     TEXT,
    data_lockfile_hash   TEXT,
    generated_at         TEXT NOT NULL,
    miss_log_url         TEXT,
    badges               TEXT,
    PRIMARY KEY (vintage_id, country, indicator, horizon)
);
CREATE INDEX idx_fc_country ON forecasts(country);
CREATE INDEX idx_fc_indicator ON forecasts(indicator);
CREATE INDEX idx_fc_horizon ON forecasts(horizon);
"""

_DDL_SCENARIOS = """
CREATE TABLE scenarios (
    slug                  TEXT PRIMARY KEY,
    name                  TEXT NOT NULL,
    description           TEXT,
    trigger_summary       TEXT,
    probability           REAL NOT NULL,
    triggered_at          TEXT NOT NULL,
    affected_countries    TEXT NOT NULL,   -- space-separated ISO-3
    affected_indicators   TEXT NOT NULL,   -- space-separated codes
    methodology_url       TEXT,
    narrative_block       TEXT
);
"""

_DDL_MISSES = """
CREATE TABLE misses (
    vintage_id     TEXT NOT NULL,
    country        TEXT NOT NULL,
    indicator      TEXT NOT NULL,
    horizon        TEXT NOT NULL,
    base_period    TEXT NOT NULL,
    scoring_period TEXT NOT NULL,
    forecast       REAL NOT NULL,
    p10            REAL,
    p90            REAL,
    actual         REAL NOT NULL,
    miss           REAL NOT NULL,
    out_of_band    INTEGER NOT NULL,
    why            TEXT,
    postmortem_url TEXT,
    PRIMARY KEY (vintage_id, country, indicator, horizon)
);
CREATE INDEX idx_miss_country ON misses(country);
CREATE INDEX idx_miss_indicator ON misses(indicator);
"""

_DDL_META = """
CREATE TABLE meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""

_ALL_DDL = [
    _DDL_OBSERVATIONS,
    _DDL_FORECASTS,
    _DDL_SCENARIOS,
    _DDL_MISSES,
    _DDL_META,
]


def snapshot_to_sqlite(
    out_path: str | Path,
    *,
    vintage: date,
    observations: Iterable[Any] = (),
    forecasts: Iterable[Any] = (),
    scenarios: Iterable[Any] = (),
    misses: Iterable[Any] = (),
    extra_meta: Mapping[str, str] | None = None,
) -> Path:
    """Write the four canonical tables to a fresh SQLite database.

    Each iterable yields records (dataclasses, dicts, or namedtuples). Unknown
    fields are silently skipped; missing required fields raise ``ValueError``.

    Returns the path of the written file.
    """
    out_path = Path(out_path)
    if out_path.exists():
        out_path.unlink()

    conn = sqlite3.connect(str(out_path))
    try:
        conn.executescript("".join(_ALL_DDL))

        _insert_observations(conn, observations)
        _insert_forecasts(conn, forecasts)
        _insert_scenarios(conn, scenarios)
        _insert_misses(conn, misses)
        _insert_meta(conn, vintage, extra_meta or {})

        conn.commit()
    finally:
        conn.close()

    return out_path


def _as_dict(rec: Any) -> Mapping[str, Any]:
    if isinstance(rec, Mapping):
        return rec
    if is_dataclass(rec):
        return asdict(rec)
    if hasattr(rec, "_asdict"):
        return rec._asdict()
    raise TypeError(f"unsupported record type {type(rec).__name__}")


def _iso_or_none(v: Any) -> str | None:
    if v is None:
        return None
    if isinstance(v, (date, datetime)):
        return v.isoformat()
    return str(v)


def _flat_dict(v: Any) -> str | None:
    if v is None:
        return None
    if isinstance(v, str):
        return v
    import json

    return json.dumps(v, sort_keys=True, default=str)


def _insert_observations(conn: sqlite3.Connection, recs: Iterable[Any]) -> None:
    rows = []
    for rec in recs:
        d = _as_dict(rec)
        sid = d.get("series_id")
        if not sid:
            raise ValueError(f"observation missing series_id: {d!r}")
        meta = d.get("metadata") or {}
        rows.append((
            str(sid),
            _iso_or_none(d.get("observed_at")),
            _iso_or_none(d.get("vintage_at")),
            d.get("value"),
            d.get("source", "unknown"),
            (meta or {}).get("country"),
            _flat_dict(meta),
        ))
    if rows:
        conn.executemany(
            "INSERT INTO observations VALUES (?, ?, ?, ?, ?, ?, ?)",
            rows,
        )


def _insert_forecasts(conn: sqlite3.Connection, recs: Iterable[Any]) -> None:
    rows = []
    for rec in recs:
        d = _as_dict(rec)
        bands = d.get("bands") or {}
        consensus = d.get("consensus_overlay") or {}
        prov = d.get("provenance") or {}
        badges = d.get("badges") or []
        if isinstance(badges, (list, tuple)):
            badges_str = " ".join(badges)
        else:
            badges_str = str(badges)
        rows.append((
            d["vintage_id"],
            d["model_id"],
            d.get("model_card_url"),
            d["country"],
            d["indicator"],
            d["horizon"],
            d["base_period"],
            d["scoring_period"],
            float(d["point"]),
            float(bands.get("p10", d["point"])),
            float(bands.get("p50", d["point"])),
            float(bands.get("p90", d["point"])),
            consensus.get("weo"),
            consensus.get("oecd_eo"),
            consensus.get("frb_sep"),
            consensus.get("ecb_spf"),
            prov.get("git_sha"),
            prov.get("container_digest"),
            prov.get("data_lockfile_hash"),
            prov.get("generated_at") or datetime.now(timezone.utc).isoformat(),
            d.get("miss_log_url"),
            badges_str,
        ))
    if rows:
        conn.executemany(
            "INSERT INTO forecasts VALUES "
            "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows,
        )


def _insert_scenarios(conn: sqlite3.Connection, recs: Iterable[Any]) -> None:
    rows = []
    for rec in recs:
        d = _as_dict(rec)
        rows.append((
            d["slug"],
            d["name"],
            d.get("description"),
            d.get("trigger_summary"),
            float(d["probability"]),
            d["triggered_at"],
            " ".join(d.get("affected_countries") or ()),
            " ".join(d.get("affected_indicators") or ()),
            d.get("methodology_url"),
            d.get("narrative_block"),
        ))
    if rows:
        conn.executemany(
            "INSERT INTO scenarios VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows,
        )


def _insert_misses(conn: sqlite3.Connection, recs: Iterable[Any]) -> None:
    rows = []
    for rec in recs:
        d = _as_dict(rec)
        forecast = float(d["forecast"])
        actual = float(d["actual"])
        miss = actual - forecast
        p10 = d.get("p10")
        p90 = d.get("p90")
        out_of_band = 0
        if p10 is not None and p90 is not None:
            out_of_band = 1 if (actual < p10 or actual > p90) else 0
        rows.append((
            d["vintage_id"],
            d["country"],
            d["indicator"],
            d["horizon"],
            d["base_period"],
            d["scoring_period"],
            forecast,
            p10,
            p90,
            actual,
            miss,
            out_of_band,
            d.get("why"),
            d.get("postmortem_url"),
        ))
    if rows:
        conn.executemany(
            "INSERT INTO misses VALUES "
            "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows,
        )


def _insert_meta(
    conn: sqlite3.Connection,
    vintage: date,
    extra: Mapping[str, str],
) -> None:
    base = {
        "vintage_date": vintage.isoformat(),
        "snapshot_generated_at": datetime.now(timezone.utc).isoformat(),
        "license_code": "Apache-2.0",
        "license_data": "CC-BY-4.0",
        "attribution": "OPENGEM (opengem.org)",
        "schema_version": "1",
    }
    base.update(extra)
    conn.executemany(
        "INSERT OR REPLACE INTO meta(key, value) VALUES (?, ?)",
        list(base.items()),
    )


def write_metadata(out_path: str | Path, *, vintage: date) -> Path:
    """Emit a Datasette metadata.yaml beside the snapshot.

    Datasette uses this YAML for table descriptions, license, example queries,
    and per-column descriptions. We hand-craft it because the default Datasette
    UX of "raw tables with no context" undersells the open ledger.
    """
    out_path = Path(out_path)
    yaml = _METADATA_YAML.format(vintage=vintage.isoformat())
    out_path.write_text(yaml)
    return out_path


_METADATA_YAML = """\
title: OPENGEM — Public Macro-Accountability Ledger
description_html: |
    <p>Every forecast OPENGEM has ever published, vintaged and queryable.
    Every backtest with every cell of the V&amp;V matrix open.
    Every miss with a post-mortem linked.</p>
    <p>Apache-2.0 (code) / CC-BY-4.0 (data). Cite as
    <em>OPENGEM (opengem.org), vintage {vintage}</em>.</p>
license: CC-BY-4.0
license_url: https://creativecommons.org/licenses/by/4.0/
source: OPENGEM
source_url: https://opengem.org
databases:
  opengem:
    title: OPENGEM vintage {vintage}
    description: |
      The OPENGEM public ledger as of {vintage}. Forecasts are vintage-stamped;
      misses are scored against truth and surfaced in the `misses` table with a
      post-mortem URL when one exists.
    tables:
      observations:
        title: Vintage-correct observations from upstream agencies
        description: |
          Raw observations as published by BEA, BLS, FRB, Treasury, Census,
          OECD ORDRA, BIS, ECB, IMF SDMX 3.0, World Bank, and the Cline Center
          POLECAT release. Each row is keyed by (series_id, observed_at,
          vintage_at).
        license: CC-BY-4.0
        queries:
          us_gdp_recent:
            sql: |
              select observed_at, value
              from observations
              where series_id = 'USA.BEA.gdp_yoy.country.Q'
              order by observed_at desc
              limit 24
            title: Last 24 quarters of US GDP YoY
      forecasts:
        title: OPENGEM forecast records at this vintage
        description: |
          One row per (country × indicator × horizon). P10/P50/P90 bands are
          mandatory. Consensus columns (WEO, OECD EO, FRB SEP, ECB SPF) are
          populated when those forecasters publish at compatible cadence.
        queries:
          tier_v_gdp_4q:
            sql: |
              select country, point, p10, p90, weo, oecd_eo
              from forecasts
              where indicator = 'gdp_yoy' and horizon = '4Q'
              order by country
            title: Tier-V GDP 4Q forecasts side-by-side with consensus
      scenarios:
        title: Currently-triggered scenarios
        description: |
          Each scenario has a machine-checkable trigger summary, a probability,
          and a list of affected countries and indicators. Open the
          `methodology_url` for the full spec.
      misses:
        title: Historical forecast misses
        description: |
          Every forecast that scored outside its 80% band. The `postmortem_url`
          column links to the human-written analysis at the same URL the
          original forecast lived on. This is the publication discipline.
        queries:
          biggest_misses_recent:
            sql: |
              select vintage_id, country, indicator, horizon, miss, postmortem_url
              from misses
              where out_of_band = 1
              order by abs(miss) desc
              limit 50
            title: Biggest misses by magnitude
      meta:
        title: Vintage metadata
        description: |
          Vintage date, snapshot generation timestamp, license, schema version.
"""
