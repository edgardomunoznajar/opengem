# L096 — Iceberg Vintage-Store Migration Cost: When TimescaleDB Hits the Ceiling

**Loop**: 096 / 300
**Phase**: 2 — Integration deep dive
**Date**: 2026-06-06
**Verdict**: **DEFER (TimescaleDB through Y1-Y2; Iceberg migration plan baked Y2; concrete ceiling triggers documented)**

---

## What this loop converts

L078 surveyed the lakehouse formats and recommended TimescaleDB through Y1. This Phase 2 loop converts the "stay on Timescale" recommendation into:

1. **Concrete ceiling triggers** — quantitative thresholds at which TimescaleDB is no longer the right tool.
2. **Migration cost estimate** — what an Iceberg cutover would actually cost, in dev-weeks and operational risk.
3. **The dual-write transition plan** — how we ship Iceberg without an outage.
4. **What we do *now* (Y1) to keep the migration cheap later** — the schema discipline + Parquet-archival pattern.

The answer: TimescaleDB through Y1 at minimum and probably Y2; Iceberg migration becomes economic past 500GB compressed + 5B rows + multi-engine read access becoming product-driving. We start Parquet archival to R2 immediately so the Iceberg migration is a metadata-layer add rather than a full data rewrite.

## What TimescaleDB does well at OPENGEM scale

Reading `packages/opengem-vintage/src/opengem_vintage/store.py`, the vintage store abstraction is clean: `register_source`, `register_series`, `write_batch`, `at(vintage_at)` returning a `VintageView`. The implementation today is SQLite for dev + TimescaleDB for prod. The schema discipline is:

- `observations(series_id, observed_at, value, vintage_at, source_id, batch_id, ingested_at)` — the primary fact table.
- Indexes on `(series_id, observed_at, vintage_at DESC)` for fast "latest as-of vintage" queries.
- Hypertable partitioning by `observed_at` quarterly.
- Compression policy applied to chunks older than 1 year (~15-20x size reduction).

At Y1 scale (~300M rows, ~50GB uncompressed, ~3GB compressed): TimescaleDB handles this on a $30/mo Hetzner box with sub-100ms queries for all read patterns. There is no reason to move.

## The five ceiling triggers

We migrate to Iceberg only when *at least two* of these triggers fire:

### Trigger 1 — Compressed storage exceeds 500GB

Past 500GB, TimescaleDB single-node operations get expensive: backups take hours, replicas take days to seed, vertical-scale upgrades hit hardware limits past 64GB RAM machines.

OPENGEM's trajectory: ~3GB compressed today, ~15GB at Y2, ~50GB at Y3, ~150GB at Y5 with full 200-country × 200-indicator × 10-vintage history. Likely Y6+ to trigger.

### Trigger 2 — Active row count exceeds 5B

Past 5B rows, hypertable chunk count grows large enough that the planner overhead starts to matter, and the catalog operations (`pg_class` scans, etc.) get slow.

OPENGEM's trajectory: ~300M rows at Y1, ~1B at Y2, ~3B at Y3, ~10B at Y5. Likely Y4+ to trigger.

### Trigger 3 — Multi-engine read becomes product-driving

If we ever need Trino, Spark, Snowflake, BigQuery, or any non-Postgres engine to query the canonical store directly, Iceberg is the answer. TimescaleDB only speaks Postgres-wire.

OPENGEM's trajectory: today we publish Parquet exports for non-Postgres consumers (the `data.opengem.org` Datasette + the DuckDB-WASM Parquet snapshots). This indirection is fine. The trigger fires only if a major-revenue paid customer asks for a real-time direct query from their Snowflake warehouse.

### Trigger 4 — Read-write contention exceeds Postgres lock budget

Past a few writes per second sustained, TimescaleDB's MVCC + autovacuum starts to thrash. We currently write in batches at hourly cadence — extremely low write QPS.

OPENGEM's trajectory: write QPS grows linearly with adapter count + ingestion cadence. Stays under 1 QPS through Y3 in current plans. Likely never triggers under our roadmap.

### Trigger 5 — Versioned-snapshot governance becomes regulatory

If OPENGEM ever needs immutable, audit-grade time-travel snapshots (e.g. for a regulatory or research-reproducibility certification), Iceberg's native snapshot model is more defensible than Timescale's WAL-based point-in-time recovery.

OPENGEM's trajectory: the L186 reproducibility envelope works fine with Parquet archival; regulatory pressure unlikely under our Apache-2.0+CC-BY-4.0 model.

**Pragmatic forecast**: at our current growth rate, the realistic earliest trigger date is **Y3 (mid-2029)**. We do not need Iceberg before then.

## What the migration actually costs

Suppose Y3 the triggers fire. Migration cost:

| Phase | Task | Cost |
|---|---|---|
| **Pre-migration prep** | Dual-write infrastructure (Postgres + Parquet append) | 4 dev-weeks |
| | Iceberg metadata layer setup (Nessie or AWS Glue catalog) | 2 dev-weeks |
| | Parquet schema normalization across years (column type alignment) | 3 dev-weeks |
| | Query engine selection (Trino vs DuckDB-on-Iceberg vs Spark) | 1 dev-week |
| **Cutover** | Backfill historical data from Timescale → Iceberg | 2 dev-weeks |
| | Shadow read mode (read from both, compare results) | 3 dev-weeks |
| | Read traffic migration (per-endpoint cutover) | 2 dev-weeks |
| | Write traffic migration | 2 dev-weeks |
| **Post-migration** | Timescale decommission + monitoring | 1 dev-week |
| | Cost monitoring + tuning | ongoing |
| **Total** | | **~20 dev-weeks (~5 months)** |

That is *real* engineering cost — five months of one-person focused work. The trigger thresholds above are calibrated so that we cross them only when the operational pain of staying on Timescale exceeds those five months.

## The "keep migration cheap" Y1 discipline

Even though migration is years away, we do three things now to keep the future migration cheap:

### Discipline 1 — Parquet archival from day one

Every nightly vintage-store write also emits a Parquet snapshot to `s3://opengem-vintage/` (R2 in our case) organized by source × year × month:

```
r2://opengem-vintage/
  source=bea/year=2026/month=06/day=06/batch=abc123.parquet
  source=bls/year=2026/month=06/day=06/batch=def456.parquet
  source=gpr/year=2026/month=06/day=06/batch=ghi789.parquet
  ...
```

The Parquet column schema matches the canonical vintage-store schema exactly: `series_id, observed_at, value, vintage_at, source_id, batch_id, ingested_at`. This is the same schema we will eventually hand to Iceberg. When the day comes, we add an Iceberg metadata layer over the existing Parquet files — no data rewrite needed.

Cost today: a `polars`/`duckdb`-based exporter at the end of each Dagster batch. ~2 dev-days to build. Ongoing R2 storage cost: $0.015/GB-month × growing.

### Discipline 2 — Single source of truth for schema

The schema is defined once in `opengem-types` and serialized identically to:
- TimescaleDB tables.
- Parquet column definitions.
- Pydantic models on the API surface.
- OpenBB provider Fetcher Data classes (L082).

When the migration day comes, the Iceberg table schema is generated from the same `opengem-types` source. No schema drift.

### Discipline 3 — Avoid Timescale-specific features in the read path

The read path uses only standard Postgres SQL (window functions, `WHERE vintage_at <= X`, common-table-expressions). We do not use Timescale-specific functions like `time_bucket()`, `first()`, `last()` in the API endpoints. Continuous aggregates are an *internal* materialized-view pattern only; they don't leak to API consumers.

This means the read path is portable: when migration happens, we re-implement the read against Iceberg + DuckDB or Trino with the same SQL. The API contract doesn't change.

## What Iceberg gives us when we eventually migrate

The Y3+ promises:

1. **Multi-engine read.** DuckDB, Trino, Spark, Snowflake, BigQuery all read the same Iceberg tables. Future paid customers querying from their preferred warehouse: zero engineering on our side.

2. **Time-travel native.** `SELECT * FROM forecasts FOR VERSION AS OF '2026-06-06'` is one line. Versioned snapshots are first-class. The L186 reproducibility envelope becomes simpler.

3. **Schema evolution.** Adding columns, renaming columns, deprecating columns all work without rewriting historical data. Postgres ALTER TABLE on a 10B-row hypertable is multiple hours; Iceberg is metadata-only.

4. **Petabyte scaling.** Iceberg + Parquet + S3 scales to petabytes without operational complexity changes. Single-node Postgres does not.

5. **Cost reduction.** Iceberg + R2 + DuckDB at 100GB-1TB scale is $20-100/mo. Timescale Cloud at the same scale is $500-2000/mo. Self-hosted Postgres+TimescaleDB on Hetzner is competitive (~$100-300/mo) but operational burden is higher.

## Why not Delta Lake

Delta Lake is closely tied to Databricks. The open spec (`delta-rs`, `delta-lake`) is real, but the ecosystem gravity around Databricks-specific extensions makes long-term betting on Delta-without-Databricks risky. OPENGEM will never adopt Databricks (cost, vendor lock-in, AGPL contamination concerns with Databricks' open-source stack history). **Delta Lake is SKIP.**

## Why not Hudi

Apache Hudi is the third lakehouse format. It optimizes for upsert-heavy workloads (slowly-changing-dimension patterns). OPENGEM's vintage data is append-only — no upserts. Hudi's strengths don't apply. **Hudi is SKIP.**

## Why not Apache DataFusion?

DataFusion is a query engine, not a storage format. It runs on top of Parquet or Iceberg. We adopt it if/when DuckDB becomes insufficient at our query scale (no obvious horizon). For now: not in scope.

## Risks of staying on Timescale longer

1. **Trigger underestimation.** If our growth outpaces estimates (e.g. ACLED+OpenSanctions full ingestion takes us to 1B rows by Y2 instead of Y3), we hit triggers earlier. Mitigation: monthly growth-tracking dashboard panel in Grafana; trigger thresholds re-evaluated quarterly.

2. **Sudden licensing shift in TimescaleDB.** Timescale Inc. has shown willingness to relicense (TSL vs Apache mix). Mitigation: stay on community-edition Apache features only; if TSL features become free-tier blocked, move sooner.

3. **Operational fragility at 500GB+.** Backups, replicas, vertical-scale upgrades all get harder. Mitigation: the Parquet archival pattern means we always have a portable backup; worst case we restore from Parquet into a fresh Timescale instance.

## Risks of migrating to Iceberg

1. **Multi-engine read becomes a vendor surface to maintain.** If we wire Trino and DuckDB and Snowflake-Iceberg-connector all to the same tables, every customer-facing engine becomes a support burden. Mitigation: pick one primary read engine (DuckDB) and document the others as "best-effort."

2. **Iceberg metadata catalog lock-in.** AWS Glue, Nessie, Project Iceberg's REST catalog are all options. The catalog choice has stickiness. Mitigation: choose Nessie (open-source, vendor-neutral) over Glue (AWS-specific).

3. **The "5-month migration" cost is real.** That is half a year of engineering opportunity cost. Mitigation: trigger thresholds calibrated to ensure migration only happens when staying becomes more expensive.

## Cost summary

| Item | Y1 cost | Y2 cost | Y3 cost (migration year) | Y4+ cost |
|---|---|---|---|---|
| TimescaleDB hosting | $30/mo | $80/mo | $150/mo (during cutover) | $0/mo (decommissioned) |
| R2 Parquet archival | $1/mo | $5/mo | $20/mo | $50-200/mo |
| Iceberg/Nessie catalog | $0 | $0 | $30/mo | $50-100/mo |
| Migration engineering | $0 | $0 | **~5 dev-months** | $0 |
| Ongoing Iceberg ops | $0 | $0 | $0 (Y3 second half) | $50/mo |

Y1 status: **TimescaleDB + Parquet archive at ~$31/mo**.

## What this loop produced

- Five concrete ceiling triggers with quantitative thresholds.
- Realistic migration date: Y3 at earliest, possibly Y4.
- 20-dev-week migration cost estimate.
- Three Y1 disciplines that keep migration cheap (Parquet archival, single schema source, portable SQL).
- Delta Lake and Hudi explicitly rejected.
- Total Y1 operating cost: ~$31/mo for vintage storage.

## What comes next

- **L097** — Dagster asset graph (where the Parquet archive job lives).
- **L186** — Reproducibility envelope (consumer of vintage snapshots).
- **L275** — Cost projection (this is one input).

## Related

- [[L077-duckdb-motherduck]] — DuckDB as the query engine over Iceberg eventually.
- [[L078-iceberg-delta-parquet]] — Phase 1 lakehouse survey.
- [[L094-duckdb-local-first-analytics]] — sibling pattern using Parquet.
- [[L097-dagster-fully-exploit]] — orchestration sibling.
- [[L186-reproducibility-envelope]] — downstream consumer.
- inspected source: `/mnt/bigdata/home/edgardo/projectsd/opengem/packages/opengem-vintage/src/opengem_vintage/store.py` (canonical vintage-store interface).
