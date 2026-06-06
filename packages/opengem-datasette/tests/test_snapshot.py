"""Tests for opengem-datasette snapshot export."""

from __future__ import annotations

import sqlite3
from datetime import date
from pathlib import Path

import pytest
from opengem_datasette import snapshot_to_sqlite, write_metadata


@pytest.fixture
def vintage_dir(tmp_path: Path) -> Path:
    return tmp_path


def test_snapshot_creates_all_tables(vintage_dir: Path):
    out = snapshot_to_sqlite(vintage_dir / "snap.db", vintage=date(2026, 6, 6))
    conn = sqlite3.connect(out)
    try:
        tables = {
            r[0]
            for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
        assert tables == {"observations", "forecasts", "scenarios", "misses", "meta"}
    finally:
        conn.close()


def test_snapshot_meta_populated(vintage_dir: Path):
    out = snapshot_to_sqlite(
        vintage_dir / "snap.db",
        vintage=date(2026, 6, 6),
        extra_meta={"git_sha": "abc123"},
    )
    conn = sqlite3.connect(out)
    try:
        kv = dict(conn.execute("SELECT key, value FROM meta"))
    finally:
        conn.close()
    assert kv["vintage_date"] == "2026-06-06"
    assert kv["license_code"] == "Apache-2.0"
    assert kv["license_data"] == "CC-BY-4.0"
    assert kv["git_sha"] == "abc123"


def test_snapshot_inserts_observations(vintage_dir: Path):
    obs = [
        {
            "series_id": "USA.BEA.gdp_yoy.country.Q",
            "observed_at": "2024-12-31",
            "vintage_at": "2026-06-06",
            "value": 2.3,
            "source": "BEA",
            "metadata": {"country": "USA"},
        },
        {
            "series_id": "USA.BEA.gdp_yoy.country.Q",
            "observed_at": "2025-03-31",
            "vintage_at": "2026-06-06",
            "value": 2.5,
            "source": "BEA",
            "metadata": {"country": "USA"},
        },
    ]
    out = snapshot_to_sqlite(
        vintage_dir / "snap.db", vintage=date(2026, 6, 6), observations=obs
    )
    conn = sqlite3.connect(out)
    try:
        rows = list(
            conn.execute(
                "SELECT series_id, observed_at, value, country FROM observations "
                "ORDER BY observed_at"
            )
        )
    finally:
        conn.close()
    assert len(rows) == 2
    assert rows[0][0] == "USA.BEA.gdp_yoy.country.Q"
    assert rows[0][2] == 2.3
    assert rows[0][3] == "USA"


def test_snapshot_inserts_forecasts(vintage_dir: Path):
    forecasts = [
        {
            "vintage_id": "2026-06-06-1200Z",
            "model_id": "opengem-l3-dfm-bma-v0.4",
            "model_card_url": "https://opengem.org/model-cards/v0.4",
            "country": "USA",
            "indicator": "gdp_yoy",
            "horizon": "4Q",
            "base_period": "2026-Q2",
            "scoring_period": "2027-Q2",
            "point": 1.9,
            "bands": {"p10": 0.8, "p50": 1.9, "p90": 3.0},
            "consensus_overlay": {"weo": 2.2, "oecd_eo": 2.1, "frb_sep": 2.0},
            "provenance": {
                "git_sha": "abc",
                "data_lockfile_hash": "sha256:deadbeef",
                "generated_at": "2026-06-06T12:00:00Z",
            },
            "miss_log_url": "https://opengem.org/misses/usa-gdp",
            "badges": ["ensemble-of-N", "high-coverage"],
        }
    ]
    out = snapshot_to_sqlite(
        vintage_dir / "snap.db", vintage=date(2026, 6, 6), forecasts=forecasts
    )
    conn = sqlite3.connect(out)
    try:
        row = conn.execute(
            "SELECT country, indicator, point, p10, p90, weo, badges FROM forecasts"
        ).fetchone()
    finally:
        conn.close()
    assert row[0] == "USA"
    assert row[1] == "gdp_yoy"
    assert row[2] == 1.9
    assert row[3] == 0.8
    assert row[4] == 3.0
    assert row[5] == 2.2
    assert "ensemble-of-N" in row[6]


def test_snapshot_inserts_scenarios(vintage_dir: Path):
    sc = [
        {
            "slug": "us-recession-2026h2",
            "name": "US recession 2026 H2",
            "description": "term-spread trigger",
            "trigger_summary": "10y-3m below -50bp for 8 weeks",
            "probability": 0.34,
            "triggered_at": "2026-06-04T13:22:00Z",
            "affected_countries": ["USA", "CAN", "MEX"],
            "affected_indicators": ["gdp_yoy", "unemployment"],
            "methodology_url": "https://opengem.org/methodology/us-rec",
        }
    ]
    out = snapshot_to_sqlite(
        vintage_dir / "snap.db", vintage=date(2026, 6, 6), scenarios=sc
    )
    conn = sqlite3.connect(out)
    try:
        row = conn.execute(
            "SELECT slug, probability, affected_countries FROM scenarios"
        ).fetchone()
    finally:
        conn.close()
    assert row[0] == "us-recession-2026h2"
    assert row[1] == 0.34
    assert "USA" in row[2]


def test_snapshot_inserts_misses_with_out_of_band_flag(vintage_dir: Path):
    misses = [
        {
            "vintage_id": "2025-Q1",
            "country": "USA",
            "indicator": "gdp_yoy",
            "horizon": "4Q",
            "base_period": "2025-Q1",
            "scoring_period": "2026-Q1",
            "forecast": 1.4,
            "p10": 0.6,
            "p90": 2.2,
            "actual": 2.6,
            "why": "model under-weighted services consumption",
            "postmortem_url": "https://opengem.org/postmortem/usa-gdp-2025q1",
        },
        {
            "vintage_id": "2025-Q2",
            "country": "USA",
            "indicator": "cpi_yoy",
            "horizon": "1Q",
            "base_period": "2025-Q2",
            "scoring_period": "2025-Q3",
            "forecast": 2.5,
            "p10": 2.0,
            "p90": 3.0,
            "actual": 2.7,  # inside band
            "why": "—",
        },
    ]
    out = snapshot_to_sqlite(
        vintage_dir / "snap.db", vintage=date(2026, 6, 6), misses=misses
    )
    conn = sqlite3.connect(out)
    try:
        rows = list(
            conn.execute(
                "SELECT indicator, miss, out_of_band FROM misses ORDER BY indicator"
            )
        )
    finally:
        conn.close()
    # cpi_yoy first alphabetically
    assert rows[0][0] == "cpi_yoy"
    assert rows[0][2] == 0  # inside band
    assert rows[1][0] == "gdp_yoy"
    assert rows[1][2] == 1  # outside band
    # miss = actual - forecast
    assert abs(rows[1][1] - (2.6 - 1.4)) < 1e-9


def test_snapshot_overwrites_existing_file(vintage_dir: Path):
    p = vintage_dir / "snap.db"
    snapshot_to_sqlite(p, vintage=date(2026, 6, 6))
    first_mtime = p.stat().st_mtime
    snapshot_to_sqlite(p, vintage=date(2026, 6, 7))
    # File replaced, so size or mtime change; at minimum the meta differs.
    conn = sqlite3.connect(p)
    try:
        kv = dict(conn.execute("SELECT key, value FROM meta"))
    finally:
        conn.close()
    assert kv["vintage_date"] == "2026-06-07"


def test_write_metadata_yaml(vintage_dir: Path):
    p = vintage_dir / "metadata.yaml"
    out = write_metadata(p, vintage=date(2026, 6, 6))
    assert out == p
    text = p.read_text()
    assert "OPENGEM" in text
    assert "2026-06-06" in text
    assert "CC-BY-4.0" in text


def test_cli_demo_emits_snapshot(tmp_path, monkeypatch):
    """The CLI demo mode produces a valid snapshot from bundled fixtures."""
    from opengem_datasette.cli import main as cli_main

    out_db = tmp_path / "demo.db"
    rc = cli_main(["--vintage", "demo", "--out", str(out_db)])
    assert rc == 0
    assert out_db.exists()
    conn = sqlite3.connect(out_db)
    try:
        tables = {
            r[0]
            for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
    finally:
        conn.close()
    assert "forecasts" in tables
    assert "meta" in tables
