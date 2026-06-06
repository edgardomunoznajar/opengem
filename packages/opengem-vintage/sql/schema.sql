-- OPENGEM vintage-correct storage schema (PostgreSQL + TimescaleDB)
-- Apply via: psql -f sql/schema.sql

-- Extensions
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Sources catalog
CREATE TABLE IF NOT EXISTS source (
    source_id     TEXT PRIMARY KEY,
    name          TEXT NOT NULL,
    base_url      TEXT,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Series catalog
CREATE TABLE IF NOT EXISTS series_meta (
    series_id          TEXT PRIMARY KEY,
    source_id          TEXT NOT NULL REFERENCES source(source_id),
    description        TEXT,
    unit               TEXT,
    frequency          TEXT NOT NULL,
    country            TEXT NOT NULL,
    variable_kind      TEXT NOT NULL,
    source_native_id   TEXT,
    created_at         TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Raw observations — vintage hypertable
CREATE TABLE IF NOT EXISTS raw_observation (
    series_id     TEXT NOT NULL REFERENCES series_meta(series_id),
    observed_at   DATE NOT NULL,
    vintage_at    DATE NOT NULL,
    value         DOUBLE PRECISION,
    metadata      JSONB,
    PRIMARY KEY (series_id, observed_at, vintage_at)
);

-- TimescaleDB hypertable on vintage_at (release dates flow through time)
SELECT create_hypertable(
    'raw_observation',
    'vintage_at',
    if_not_exists => TRUE,
    create_default_indexes => TRUE
);

CREATE INDEX IF NOT EXISTS idx_raw_obs_series_observed
    ON raw_observation (series_id, observed_at, vintage_at DESC);

-- Vintage snapshot manifest
CREATE TABLE IF NOT EXISTS vintage_snapshot (
    vintage_hash       TEXT PRIMARY KEY,
    pulled_at          TIMESTAMPTZ NOT NULL,
    source_id          TEXT NOT NULL REFERENCES source(source_id),
    series_count       INTEGER NOT NULL,
    observation_count  INTEGER NOT NULL,
    manifest           JSONB NOT NULL
);

-- Audit: forecasts table not in this package; lives in opengem-l3 / opengem-vv
