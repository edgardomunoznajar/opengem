# L077 — DuckDB + Motherduck for Analytical Workloads, DuckDB-WASM in the Browser

**Loop**: 077 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Thesis of this loop

DuckDB is the single most important infrastructure upgrade open-source analytics has had in the past five years. It is to OLAP what SQLite was to OLTP: an in-process columnar query engine that ships as a single binary, runs anywhere (CLI, library, WASM), and competes head-to-head with Snowflake / BigQuery / ClickHouse on single-node workloads up to terabytes.

For OPENGEM, DuckDB is the natural answer to three otherwise-awkward questions:

1. *How does the static dashboard let users query the data without a backend?* → DuckDB-WASM in the browser, querying a Parquet file served as a static asset. No server. No DB connection. Sub-second queries on millions of rows.
2. *How do we score V&V across millions of forecast×realization pairs nightly?* → DuckDB in the Python pipeline, against Parquet on S3. Faster and cheaper than Postgres for analytical aggregations.
3. *How do we hand a downloadable forecast bundle to a researcher?* → A single Parquet file. They open it in DuckDB / Polars / pandas / R. Anyone can re-run the analysis.

Verdict: **ADOPT-V1** for all three. **EVALUATE-LATER** for Motherduck specifically (it solves a problem OPENGEM mostly doesn't have, but the pricing changes in early 2026 made it less attractive).

## DuckDB (the OSS core)

- **License**: MIT.
- **Maintainer**: DuckDB Labs (Hannes Mühleisen, Mark Raasveldt et al). Healthy, well-funded.
- **Form factors**:
  - CLI binary (`duckdb my.db`).
  - Python library (`pip install duckdb`).
  - Node.js, Rust, Java, R, Go bindings.
  - **DuckDB-WASM** (the browser/JS build, ~5MB gzipped).
- **Capabilities**:
  - Full SQL (PostgreSQL-flavored dialect, with extensions for things like `unnest`, `pivot`, `lambdas`).
  - Reads CSV, Parquet, JSON, Arrow, Iceberg, Delta Lake, MotherDuck cloud, HTTPS URLs.
  - Writes CSV, Parquet, Arrow.
  - Window functions, CTEs, recursive CTEs.
  - Built-in time-series functions (`time_bucket`, `date_trunc`, `interval`).
  - Geo extensions (`spatial` module — H3, PostGIS-like).
  - JSON extension (`json_extract`, JSON path).
  - Polars-zero-copy interop.

The performance is genuinely shocking the first time. A 100M row Parquet file aggregated by a key takes ~3-5 seconds on a laptop. Postgres on the same data takes minutes.

## DuckDB-WASM in the browser: the killer affordance

DuckDB-WASM is a WebAssembly build that runs DuckDB *in the user's browser*. The JS API is:

```javascript
import * as duckdb from '@duckdb/duckdb-wasm';
const db = await duckdb.makeBundle();
await db.registerFileURL('forecasts.parquet', 'https://data.opengem.org/forecasts.parquet');
const result = await db.query('SELECT country, AVG(forecast_value) FROM forecasts WHERE indicator = ? GROUP BY 1', ['CPI_YOY']);
```

For OPENGEM, this enables the following genuinely novel affordances:

1. **The "fork this query" button**. On any chart, the user clicks a button and gets a SQL editor pre-populated with the query that generated the chart, running against the same Parquet file. They edit the query and see the chart change. *Zero backend*.

2. **The "filter your forecast bundle" page**. Download a 500MB OPENGEM Parquet of all G20 country indicators 1990-2026; the page lets the user filter to "just the indicators they care about" and re-download the slice. The filter runs in the browser.

3. **The "compare two countries" page**. Pre-fetched Parquet of both countries; DuckDB-WASM joins them client-side. No server query needed.

4. **The "DIY V&V matrix" page**. A power user wants to score forecasts their own way? Drop their scoring SQL into the browser-side editor; DuckDB-WASM runs it on the OPENGEM Parquet. The barrier to "fork the analysis" drops to a SQL query.

These affordances are precisely the *open-substrate* dimension of L001's vision. They are deliverable today with ~50 lines of JS + the DuckDB-WASM bundle.

The 5MB DuckDB-WASM bundle is the cost. It's loaded once per session and cached. For the pages where it's used, that's a reasonable price.

## DuckDB in the OPENGEM Python pipeline

OPENGEM's modeling layer is Python. DuckDB integrates as a Python library; the typical pattern:

```python
import duckdb
con = duckdb.connect(':memory:')
con.execute("INSTALL httpfs; LOAD httpfs;")
df = con.execute("""
    SELECT country, vintage, AVG(score) as avg_score
    FROM 'https://opengem-vintages.s3.amazonaws.com/forecasts_2026_*.parquet'
    WHERE indicator = 'CPI_YOY'
    GROUP BY 1, 2
""").df()
```

This is dramatically faster than the equivalent Postgres + pandas pattern. For V&V scoring, vintage comparison, and bulk forecast generation, DuckDB-in-Python is the right tool.

The OPENGEM canonical storage stays Postgres + TimescaleDB (transactional, multi-user, the system of record). DuckDB lives at the *analytical* tier — daily-job aggregations, V&V scoring, snapshot generation, Parquet export. They coexist, not compete.

## Motherduck: the managed-DuckDB cloud

Motherduck is the commercial cloud built on DuckDB by the DuckDB Labs team (and others). The pitch: "DuckDB-as-a-service" — a hosted endpoint your DuckDB clients connect to, with shared databases, RBAC, hybrid execution (some compute in-cloud, some on-laptop).

The 2026 pricing changes (the $25/mo Lite plan went away, the Business plan moved from $100 to $250/mo, a free tier was introduced with 3 users / 10GB / 10 compute-hours/mo) make the value proposition more confusing than it was. For OPENGEM specifically:

- The free tier is too capped for production use.
- The Business tier at $250/mo buys "hosted DuckDB" which OPENGEM mostly doesn't need — OPENGEM's Postgres is the system of record, OPENGEM's Parquet on S3 is the analytical archive, OPENGEM's DuckDB-in-Python is the runtime.
- The hybrid execution feature ("query that joins your laptop and the cloud") is genuinely cool but solves a problem OPENGEM doesn't have.

**Motherduck verdict: EVALUATE-LATER.** It might earn a slot if OPENGEM hits a "we need a shared compute layer for collaborators" moment in Y2-Y3. Until then, S3 + DuckDB-in-Python covers the needs.

## Performance / cost comparison

| Task | Postgres | DuckDB | DuckDB-WASM | Motherduck |
|---|---|---|---|---|
| Read 100M rows aggregated by key | minutes | 3-5s | 5-10s | 3-5s |
| Cost per query | $0 (already running) | $0 | $0 | ~$0.001-0.01 |
| Setup cost | $0 (existing) | $0 | $0 | $250/mo minimum |
| Browser-side | impossible | n/a | yes | n/a |

For the public-facing OPENGEM data publishing layer, the math is overwhelming: **emit Parquet to S3, let users query with DuckDB-WASM in the browser**. No backend cost. No connection pool. No rate limit.

## The Parquet + DuckDB-WASM substrate as a *moat*

This is genuinely strategic for OPENGEM:

1. Bloomberg's data is locked in their proprietary API.
2. TradingEconomics' data is locked behind a paywall.
3. Macrobond's data lives only in their client.
4. **OPENGEM's data is a Parquet file you can `wget`.**

The Parquet+DuckDB substrate is "data so portable the incumbents *can't* offer it without breaking their pricing model." That asymmetry is exactly what L001 promised to exploit. The pricing model of every macro-data incumbent forbids them from publishing the raw data in a downloadable, queryable form. OPENGEM has no such constraint.

## DuckDB extensions worth wiring up

- `httpfs` — query Parquet directly from S3/HTTPS URLs.
- `spatial` — H3-indexed geographic queries (for the geopolitical pulse page).
- `iceberg` — read Iceberg tables (L078).
- `delta` — read Delta Lake tables (L078).
- `arrow` — zero-copy Arrow interop with Polars / pandas.
- `excel` — read XLSX (for ingestion from sources that publish Excel).

## Cost summary

| Tool | License | Cost | Use | Ramp |
|---|---|---|---|---|
| DuckDB Python | MIT | $0 | Analytical pipeline (V&V, aggregations) | 1 day |
| DuckDB CLI | MIT | $0 | Ad-hoc queries against snapshots | 1 day |
| DuckDB-WASM | MIT | $0 | Browser-side query, fork-this-query UX | 1 week |
| Motherduck free | proprietary | $0 (capped) | (skipped) | n/a |
| Motherduck Business | proprietary | $250/mo | (skipped) | (skipped) |
| Parquet on S3 (storage) | open format | ~$5-10/mo at typical Y1 size | Public download surface | 1 day |

## Verdict

- **DuckDB Python** in the OPENGEM analytical pipeline: **ADOPT-V1**. $0. 1-day ramp.
- **DuckDB-WASM** in the browser for fork-this-query and DIY filtering: **ADOPT-V1**. $0. 1-week ramp.
- **Parquet on S3** as the public download substrate: **ADOPT-V1**. $5-10/mo storage.
- **Motherduck**: **EVALUATE-LATER**. Revisit if collaborator compute becomes a need.

## What comes next

- **L078** evaluates Iceberg / Delta Lake / Parquet for vintage storage at scale.
- **L094** is the Phase 2 deep dive on DuckDB local-first analytics.

## Related

- [[L076-datasette]] — sister read-only data tier (different shape — row-level browsing vs analytical)
- [[L078-iceberg-delta-parquet]] — Parquet-at-scale storage format
- [[L094-duckdb-local-analytics]] — Phase 2 deep dive
