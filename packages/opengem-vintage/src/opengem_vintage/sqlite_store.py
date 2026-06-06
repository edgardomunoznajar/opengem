"""SQLite-backed VintageStore — for tests and local exploration.

Implements the same logical schema as the Postgres version, without TimescaleDB
partitioning. Uses sqlite3 from the stdlib — no extra dependencies.
"""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterable, Iterator
from datetime import date, datetime

from opengem_types import Observation, SeriesId, SeriesMeta, VintageSnapshot

from opengem_vintage.store import VintageStore, VintageView


class SQLiteVintageStore(VintageStore):
    """SQLite-backed vintage store. Suitable for tests and prototypes.

    Pass `:memory:` for in-process testing, or a file path for a local DB.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self._conn = sqlite3.connect(
            db_path, detect_types=sqlite3.PARSE_DECLTYPES, isolation_level=None
        )
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._conn.execute("PRAGMA journal_mode = WAL")

    def initialize(self) -> None:
        cur = self._conn.cursor()
        cur.executescript(
            """
            CREATE TABLE IF NOT EXISTS source (
                source_id  TEXT PRIMARY KEY,
                name       TEXT NOT NULL,
                base_url   TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS series_meta (
                series_id        TEXT PRIMARY KEY,
                source_id        TEXT NOT NULL REFERENCES source(source_id),
                description      TEXT,
                unit             TEXT,
                frequency        TEXT NOT NULL,
                country          TEXT NOT NULL,
                variable_kind    TEXT NOT NULL,
                source_native_id TEXT,
                created_at       TEXT NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS raw_observation (
                series_id   TEXT NOT NULL REFERENCES series_meta(series_id),
                observed_at TEXT NOT NULL,
                vintage_at  TEXT NOT NULL,
                value       REAL,
                metadata    TEXT,
                PRIMARY KEY (series_id, observed_at, vintage_at)
            );

            CREATE INDEX IF NOT EXISTS idx_raw_obs_series_observed
                ON raw_observation (series_id, observed_at, vintage_at DESC);

            CREATE TABLE IF NOT EXISTS vintage_snapshot (
                vintage_hash      TEXT PRIMARY KEY,
                pulled_at         TEXT NOT NULL,
                source_id         TEXT NOT NULL REFERENCES source(source_id),
                series_count      INTEGER NOT NULL,
                observation_count INTEGER NOT NULL,
                manifest          TEXT NOT NULL
            );
            """
        )

    def register_source(self, source_id: str, name: str, base_url: str | None = None) -> None:
        self._conn.execute(
            "INSERT OR IGNORE INTO source (source_id, name, base_url) VALUES (?, ?, ?)",
            (source_id, name, base_url),
        )

    def register_series(self, meta: SeriesMeta) -> None:
        self._conn.execute(
            """
            INSERT OR IGNORE INTO series_meta
              (series_id, source_id, description, unit, frequency, country,
               variable_kind, source_native_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(meta.series_id),
                meta.source,
                meta.description,
                meta.unit,
                meta.frequency,
                meta.country,
                meta.variable_kind,
                meta.source_native_id,
            ),
        )

    def write_batch(
        self,
        observations: Iterable[Observation],
        source_id: str,
        pulled_at: datetime,
    ) -> VintageSnapshot:
        obs_list = list(observations)
        snapshot = VintageSnapshot.from_observations(obs_list, source_id, pulled_at)

        try:
            self._conn.execute("BEGIN")
            for o in obs_list:
                self._conn.execute(
                    """
                    INSERT INTO raw_observation
                      (series_id, observed_at, vintage_at, value, metadata)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT (series_id, observed_at, vintage_at) DO NOTHING
                    """,
                    (
                        str(o.series_id),
                        o.observed_at.isoformat(),
                        o.vintage_at.isoformat(),
                        o.value,
                        json.dumps(o.metadata) if o.metadata else None,
                    ),
                )
            self._conn.execute(
                """
                INSERT OR IGNORE INTO vintage_snapshot
                  (vintage_hash, pulled_at, source_id, series_count,
                   observation_count, manifest)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    snapshot.vintage_hash,
                    snapshot.pulled_at.isoformat(),
                    snapshot.source_id,
                    snapshot.series_count,
                    snapshot.observation_count,
                    json.dumps(snapshot.manifest),
                ),
            )
            self._conn.execute("COMMIT")
        except Exception:
            self._conn.execute("ROLLBACK")
            raise

        return snapshot

    def at(self, vintage_at: date) -> VintageView:
        return _SQLiteVintageView(self._conn, vintage_at)

    def close(self) -> None:
        try:
            self._conn.close()
        except sqlite3.ProgrammingError:
            pass

    def __enter__(self) -> SQLiteVintageStore:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


class _SQLiteVintageView(VintageView):
    def __init__(self, conn: sqlite3.Connection, as_of: date) -> None:
        self._conn = conn
        self._as_of_iso = as_of.isoformat()

    def iter_series(self, series_id: str | SeriesId) -> Iterator[Observation]:
        sid = str(series_id)
        # Latest vintage <= as_of, per observed_at
        cur = self._conn.execute(
            """
            WITH latest AS (
                SELECT series_id, observed_at, MAX(vintage_at) AS vintage_at
                FROM raw_observation
                WHERE series_id = ? AND vintage_at <= ?
                GROUP BY series_id, observed_at
            )
            SELECT r.series_id, r.observed_at, r.vintage_at, r.value, r.metadata,
                   COALESCE(sm.source_id, '?') AS source_id
            FROM raw_observation r
            JOIN latest l USING (series_id, observed_at, vintage_at)
            LEFT JOIN series_meta sm ON sm.series_id = r.series_id
            ORDER BY r.observed_at ASC
            """,
            (sid, self._as_of_iso),
        )
        for row in cur:
            series_id_str, observed_iso, vintage_iso, value, metadata_json, source = row
            yield Observation(
                series_id=SeriesId(series_id_str),
                observed_at=date.fromisoformat(observed_iso),
                vintage_at=date.fromisoformat(vintage_iso),
                value=value,
                source=source,
                metadata=json.loads(metadata_json) if metadata_json else {},
            )

    def latest_value(self, series_id: str | SeriesId, observed_at: date) -> float | None:
        sid = str(series_id)
        cur = self._conn.execute(
            """
            SELECT value FROM raw_observation
            WHERE series_id = ? AND observed_at = ? AND vintage_at <= ?
            ORDER BY vintage_at DESC LIMIT 1
            """,
            (sid, observed_at.isoformat(), self._as_of_iso),
        )
        row = cur.fetchone()
        return row[0] if row else None
