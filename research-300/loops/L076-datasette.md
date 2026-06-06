# L076 — Datasette + dclient: Read-Only Data Publishing for the Public Ledger

**Loop**: 076 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Thesis of this loop

Datasette is Simon Willison's read-only data publishing tool — and it is *the* tool that maps most cleanly onto OPENGEM's L001 promise of being a "public accountability ledger." Datasette is built on a worldview-level commitment that data should be queryable, exportable, citable, and re-mountable by anyone. That worldview is OPENGEM's worldview.

This loop says: **ADOPT-V1**. Datasette is the read-only API layer beneath the OPENGEM public ledger. It gives away — for free — half the work of building the "every datapoint has its own URL, every query has its own URL, every export has its own URL" plumbing OPENGEM otherwise has to build by hand.

It is not the *only* OPENGEM data API (the curated MCP server and the OpenAPI JSON API on top of Python are separate), but it is the one that most credibly delivers the "you can audit us" promise.

## What Datasette is

- Open source, **Apache 2.0**.
- Python-based. Single Python package, single CLI command (`datasette publish` or `datasette serve`).
- Backed by SQLite (or read-only SQLite views over Postgres/etc via plugins).
- The CLI `datasette serve some.db` exposes:
  - Every table as a paginated, filterable, exportable HTML view.
  - Every table as a JSON, CSV, Parquet endpoint.
  - A SQL query interface where anyone can write read-only SQL against the database.
  - Per-row permalinks.
  - Custom queries (canned queries) as named, embeddable endpoints.
  - A facet system for slice-and-dice.
- Plugin ecosystem: ~150 plugins for auth, custom rendering, alternative backends, vega-lite integration, custom column displays, GraphQL, etc.
- Active development: as of mid-2026, version 1.0a32, with regular weekly alpha releases. Maintenance is steady; the 1.0 release is "soon" but the alpha line is production-stable for read-only workloads.

## The strategic alignment with OPENGEM

Re-read L001's three musts:

> 1. A live, terminal-grade view of the world economy.
> 2. **A public accountability ledger — every forecast vintaged, every backtest scored, every miss named, every methodology pop-up open.**
> 3. **A composable open-source substrate — Apache-2.0 code, CC-BY-4.0 data, model cards, an MCP server, RSS feeds, embeddable widgets.**

Datasette delivers #2 and half of #3 *for free*. Concretely:

- **"Every forecast vintaged"** → Datasette table `forecast_vintages` with permalinks `https://data.opengem.org/vintages/9?_facet=country`.
- **"Every backtest scored"** → Datasette table `backtest_scores` with the V&V matrix queryable.
- **"Every miss named"** → Datasette table `forecast_misses` with the post-mortem text in a column.
- **"Every methodology pop-up open"** → Datasette table `methodologies` linked from every chart.
- **"JSON-block-per-chart" affordance** → every Datasette view has a `.json` endpoint at the same URL with `.html` swapped out.

The composability is the killer feature: a Substack writer can paste an OPENGEM Datasette URL into their post, and the URL is a live link to the *exact slice of data they're citing*, with provenance, with a permalink, with a re-runnable SQL query in the footer.

## Specimen inspection

The cloned repo (`research-300/clones/datasette/`) confirms:
- The 1.0 alpha line is active and stable.
- The plugin system has SDKs (`datasette-auth-github`, `datasette-cluster-map`, `datasette-vega`, `datasette-graphql`, `datasette-export-notebook`).
- The `demos/` directory shows the canonical use patterns.
- Documentation at `docs/` is thorough.
- The codebase is small (~30k lines Python). Easy to understand, easy to fork.

Recent feature highlights from the 2026 release notes:
- 1.0a31 added write queries and stored queries (templated insert/update). Not relevant for the public ledger (which is read-only) but relevant for the internal admin tool.
- 1.0a30 added a customizable "Jump to..." menu. Useful for navigation between OPENGEM tables.
- 1.0a28 was "implemented using Claude Code and Claude Opus 4.7" — Simon's noting that the project is now substantially LLM-assisted, which means the rate of feature shipping is high.

## How OPENGEM uses Datasette specifically

The OPENGEM data lake has Postgres + TimescaleDB as canonical storage (per the broader repo). Datasette serves *snapshots* of the canonical data as SQLite, not the live Postgres directly:

1. A nightly job runs `pg_dump | sqlite3-import` on the OPENGEM tables and emits `opengem_v$VINTAGE.db`.
2. Datasette runs against the SQLite snapshot.
3. The snapshot is versioned — `opengem_v2026-06-06.db`, `opengem_v2026-06-07.db` — so a Datasette URL with a vintage path serves the historical data exactly as published.
4. The Datasette instance runs on Fly.io or Cloud Run for ~$10-20/mo.

This pattern — read-only SQLite snapshots — has three architectural advantages:

1. **Performance.** SQLite is faster than Postgres for read-only single-user workloads. Datasette serves these snapshots from local disk; no DB round-trip.
2. **Reproducibility.** A snapshot is a single file. Anyone can `wget` it and run their own Datasette instance against the same data.
3. **Vintaging is trivial.** Each snapshot is the vintage.

The `dclient` companion tool (Simon's Datasette CLI client) lets users programmatically pull, query, and export from a Datasette instance. This is the "anyone can fork, mirror, derive" affordance, productized.

## What Datasette does NOT do, and what to add

- **Datasette is not a chart-rich dashboard**. The HTML views are tabular. Charts come from the `datasette-vega` plugin or external embeds. For OPENGEM, the dashboard pages live in Observable Framework (L066) / Next.js (L073); Datasette is the *raw data* tier beneath.

- **Datasette is not a write-API**. By design. The OPENGEM write path (forecast submission, scenario authoring) goes through the FastAPI core service. Datasette serves the read.

- **Datasette is not a curated narrative**. The OPENGEM country pages have narrative, methodology, annotation. Datasette has tables. Both surfaces exist.

- **Datasette's HTTPS hosting** is BYO. Fly.io and Cloud Run both work; Datasette has a `datasette publish fly` command that targets Fly.io directly.

- **Datasette's MCP integration** doesn't natively exist. OPENGEM's MCP server is a separate Python service that may query the Datasette tier under the hood, but the MCP contract is OPENGEM-specific.

## Cost

- **Self-hosted on Fly.io**: 256MB VM with persistent volume = ~$5-10/mo.
- **Self-hosted on Cloud Run + Cloud Storage for SQLite blobs**: ~$5-15/mo at low traffic.
- **Self-hosted on Hetzner CX11**: $4/mo for the box, $0 for Datasette.
- **Datasette Cloud** (Simon's managed offering): paid, optional. Skip until there's a reason.

Bandwidth at typical Y1 OPENGEM traffic (~10k unique visitors/mo, 30% engaging with raw data): ~50GB/mo. All providers above handle this in the free tier.

Practical floor: **$5/mo** for OPENGEM's public ledger Datasette.

## Ramp-up

- Day 1: install Datasette, dump Postgres to SQLite, run locally.
- Day 2-3: configure metadata (titles, descriptions, license attribution per table).
- Week 1: deploy to Fly.io with custom domain, configure CORS, configure rate limits.
- Week 2: write canned queries for the 10 most-cited views (e.g., "G7 CPI forecast bands as of latest vintage").
- Week 3: integrate `datasette-vega` plugin for inline charts, or skip in favor of linking to Observable Framework pages.
- Week 4: polish, OG cards, attribution footer, dclient examples.

A 1-month effort to a polished public-ledger surface. The first useful version (week 1) is usable.

## The bonus affordance: MCP-friendly

Datasette URLs are *exactly* the kind of resource an LLM grounded via MCP wants to reference. When OPENGEM's MCP server returns a forecast value, it can include a Datasette permalink as the citation. The LLM's response then contains "OPENGEM forecasts Brazil CPI YoY at 4.2% for 2026-Q4 ([data](https://data.opengem.org/forecasts/12345.json), [methodology](https://data.opengem.org/methodologies/cpi_brazil))."

This is the citation discipline OPENGEM promised in L001, made trivially deliverable by Datasette.

## Verdict

- **Datasette as the read-only public-ledger data tier**: **ADOPT-V1**. $5/mo. 1-month polished ramp; week-1 usable.
- **dclient** for programmatic access from scripts: **ADOPT-V1**. Free, comes with the package.
- **Datasette Cloud**: **SKIP**.

## Cost summary

| Use | Cost | Ramp |
|---|---|---|
| Self-host on Fly.io | $5-10/mo | 1 week useful, 1 month polished |
| Self-host on Hetzner | $4/mo | 1 week useful, 1 month polished |
| Datasette Cloud | (skipped) | (skipped) |

## What comes next

- **L077** evaluates DuckDB + Motherduck for the analytical workload side.
- **L095** is the Phase 2 deep dive on the Datasette public-ledger pattern.

## Related

- [[L066-observable-framework]] — dashboard surface above the ledger
- [[L077-duckdb-motherduck]] — analytical workload sibling
- [[L095-datasette-public-ledger]] — Phase 2 deep dive
- [[L108-mcp-server-contract]] — Datasette permalinks as citation rails
