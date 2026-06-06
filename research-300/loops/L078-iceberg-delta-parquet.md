# L078 — Iceberg / Delta Lake / Parquet for Vintage Storage at Scale, When to Migrate From TimescaleDB

**Loop**: 078 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Thesis of this loop

OPENGEM today uses TimescaleDB (Postgres-backed time-series) as the canonical storage tier (per the broader repo). That is the correct choice for Y0-Y1: the schema fits time-series natively, the SQL is real Postgres SQL, the operational model is one box. But there is a *scale ceiling* and a *vintage-evolution ceiling* past which the open lakehouse formats (Iceberg, Delta Lake, Hudi) start to look genuinely attractive.

This loop frames the migration question. The verdict: **stay on TimescaleDB through Y1**. **EVALUATE-LATER** Iceberg for Y2-Y3 when (a) vintage history exceeds ~500GB or (b) multi-engine read access becomes a goal. **SKIP Delta Lake** unless OPENGEM adopts Databricks (it won't). **ADOPT-V1** for Parquet-on-S3 as the *archival/export* tier alongside Postgres regardless.

## The vintage-storage problem OPENGEM has

The OPENGEM data model has these load-bearing facts:

1. *Every indicator series has a vintage history.* CPI for Brazil for 2023-Q1 was first published at value V0 on date D0, then revised to V1 on D1, then V2 on D2. OPENGEM's read-API must serve "as of D1.5 the value was V1."
2. *Every forecast has a vintage.* A forecast made on D0 of CPI for 2024-Q1 has a value; the same forecast remade on D1 with new data has a different value. The leaderboard scores both vintages against the eventual realization.
3. *Every scenario has a vintage.* When the scenario tree is rebuilt, the old version remains accessible for V&V scoring.

This is roughly *10× the row count* of a non-vintaged time-series. Brazil CPI has, say, 20 years of monthly history (240 rows in a non-vintaged store). If we capture every revision (~6 revisions per release × 240 = ~1500 rows). Times 200 countries × 100 indicators = ~30M rows. Times forecast×model×horizon (~10k forecasts/day × 365 days × 5 years) = 18M forecast rows. Plus scenarios. Plus backtests. Reasonable Y1 row count: 100-300M rows. Reasonable Y3 row count: 2-5B rows.

TimescaleDB handles 5B rows but it needs care — hypertable partitioning, compression policy, retention policy, careful indexing. Beyond ~5B rows on a single-node Timescale install, the operational cost rises sharply.

## TimescaleDB: where we are today

- **License**: Apache 2.0 (community edition); some advanced features (continuous aggregates with retention, advanced compression) are TSL-licensed but free up to certain limits. The pure-AGPL fork is also viable.
- **Strengths**: Real Postgres. Real SQL. Hypertables auto-partition by time. Native compression (10-20× reduction). Built-in continuous aggregates for materialized views over time-windows.
- **Operational reality**: ~$30-100/mo for a Hetzner box that handles 500GB-1TB of compressed data. ~$200-500/mo on a managed Timescale Cloud install with backups + HA.
- **Vintage modeling**: a `vintage_date` column + a row-per-revision pattern works. Queries like "give me CPI for Brazil as of vintage date X" are a standard `WHERE vintage_date <= X` filter with a `ROW_NUMBER() OVER (PARTITION BY series ORDER BY vintage_date DESC)`.

**Verdict for the canonical OPENGEM store through Y1: stay on Timescale.** It is sufficient, fast, well-understood, and cheap.

## When Iceberg starts to win

Apache Iceberg is the *open table format* that handles ACID transactions over Parquet files in object storage. The core promise: a directory of Parquet files plus a metadata layer that makes them look like a database table to any query engine (Spark, Trino, DuckDB, Snowflake, BigQuery via Iceberg connector, etc).

Iceberg's killer features for vintage storage at scale:

1. **Snapshot history is first-class.** Iceberg's metadata model tracks every commit; a snapshot is a tag. "Give me the table as of snapshot S" is native. *This is exactly the vintage affordance OPENGEM needs.*
2. **Partition evolution.** As OPENGEM grows, the optimal partition scheme will change (today by country×year; tomorrow by country×month or by indicator×year). Iceberg lets you change the partitioning *without rewriting historical data*. Delta Lake historically required a full table rewrite for this.
3. **Hidden partitioning.** Iceberg automatically maps query predicates to partitions. Writers don't have to know the partitioning to query efficiently.
4. **Multi-engine.** Read the same table from DuckDB, Trino, Spark, Snowflake (via external table), BigQuery (via Iceberg federation). OPENGEM's analytical jobs in Python (DuckDB) and a researcher's ad-hoc Trino query against the public lakehouse are the *same data*.
5. **Open format, vendor-neutral.** Apache 2.0. AWS S3, Google Cloud Storage, R2 — any object store.

The migration trigger for OPENGEM:

- Vintage history >500GB → operational cost on Timescale rises faster than on Iceberg.
- Multi-engine read becomes a goal (public researchers wanting to Spark / Trino over the lakehouse).
- Analytical workload starts to dominate the Postgres traffic — Iceberg + a query engine like DuckDB or StarRocks beats Postgres for analytical aggregations.

For Y2-Y3, when (probably) all three triggers fire, the migration is roughly:
1. Spark or PyIceberg job that streams Postgres → Parquet → Iceberg.
2. Keep Postgres for the transactional / curated tier; Iceberg for the analytical / archival tier.
3. Update Datasette to pull from Iceberg snapshots via DuckDB.

## Delta Lake: a non-starter for OPENGEM

- **Licensed**: Apache 2.0 (Delta Lake core), but the *innovation* lives in Databricks-proprietary extensions (Delta Lake UniForm, Delta Sharing protocol, Photon).
- **Strengths**: Excellent if you're on Databricks. Strong streaming ingestion (Delta Live Tables). Mature change-data-capture story.
- **Weaknesses for OPENGEM**:
  - The ecosystem optimization is *for* Databricks. Outside Databricks, Iceberg has better multi-engine support.
  - Partition evolution is weaker (was historically full-rewrite; UniForm helps but you're back to Databricks-leaning territory).
  - Delta Sharing (the "share Delta tables across organizations" protocol) is interesting but a closed ecosystem effort.
- **OPENGEM is not on Databricks** and will not be. The cost shape doesn't fit (Databricks pricing is for $1M+ ARR data teams).

**SKIP Delta Lake.**

## Parquet (and the Parquet-on-S3 archive tier)

Whatever the table format above, OPENGEM should be writing **Parquet files to S3** as the *archive and export tier* from Y0. The reasons:

1. **Free download substrate.** A user wants the raw OPENGEM data? Point them at `s3://opengem-public/forecasts/v$VINTAGE.parquet`. They open it in DuckDB / Polars / pandas. They have what we have.
2. **DuckDB-WASM browser query target.** L077 covers this.
3. **Long-term archival.** Parquet is open, columnar, compressed (~5-10× vs raw CSV), and supported by every analytical engine.
4. **Iceberg's storage format is Parquet.** When OPENGEM migrates to Iceberg in Y2-Y3, the Parquet files are already where they need to be — just add the Iceberg metadata layer.

The cost: at typical Y1 sizes (~50-200GB compressed), S3 storage is ~$1-5/mo plus egress. Trivial.

The Y1 plan: nightly job dumps the OPENGEM Timescale tables to Parquet on S3, partitioned by vintage_date / country / indicator. Users download the Parquet directly. DuckDB-WASM queries it in-browser. Datasette serves SQLite snapshots derived from the same data for the row-level browse experience.

## Hudi: the third format, also a SKIP

Apache Hudi (Uber, 2017) is the third open lakehouse format. Strengths: best CDC story, fast upserts. Weaknesses: smallest ecosystem outside Uber/AWS, less natural for OPENGEM's vintage model. **SKIP** — Iceberg covers OPENGEM's needs.

## The cost ramp

| Phase | Canonical store | Archive tier | Cost |
|---|---|---|---|
| Y0-Y1 (current) | TimescaleDB | Parquet on S3 nightly | $30-100/mo |
| Y2 (200GB+) | TimescaleDB | Parquet on S3 nightly | $80-200/mo |
| Y2.5 (500GB+) | TimescaleDB + Iceberg (analytical) | Iceberg on S3 | $200-500/mo |
| Y3+ (1TB+) | Iceberg primary, Postgres for curated/served subset | Iceberg on S3 | $300-800/mo |

The migration is gradual, additive, and never forces a rip-and-replace.

## Ramp-up

- Y1 Parquet export: 1 week to a nightly job.
- Y2-Y3 Iceberg migration: 4-6 weeks (build streaming ingestion, retro-fill historical, update Datasette + DuckDB code paths to read Iceberg snapshots).

## Verdict

- **TimescaleDB as canonical Y0-Y1 store**: **ADOPT-V1** (already in use).
- **Parquet on S3 as the archival/export tier from Y0**: **ADOPT-V1**. $5-10/mo.
- **Iceberg as the Y2-Y3 analytical tier**: **EVALUATE-LATER**. Migrate when vintage > 500GB or multi-engine is needed.
- **Delta Lake**: **SKIP**.
- **Hudi**: **SKIP**.

## Cost summary

| Tier | Cost (Y1) | Cost (Y3) | Ramp |
|---|---|---|---|
| TimescaleDB | $30-100/mo | $150-300/mo | already running |
| Parquet on S3 | $5-10/mo | $20-50/mo | 1 week |
| Iceberg (Y2+) | — | $100-300/mo | 4-6 weeks migration |

## What comes next

- **L079** evaluates Dagster / Prefect / Airflow / Temporal for orchestration.
- **L096** is the Phase 2 deep dive on Iceberg vintage-store migration cost.

## Related

- [[L077-duckdb-motherduck]] — analytical engine reading Parquet/Iceberg
- [[L076-datasette]] — Datasette serving snapshots derived from same data
- [[L096-iceberg-vintage-store-migration]] — Phase 2 cost analysis
