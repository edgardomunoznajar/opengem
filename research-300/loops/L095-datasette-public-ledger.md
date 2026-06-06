# L095 — Datasette Public Ledger: Mount at /data for Raw CSV/Parquet Access

**Loop**: 095 / 300
**Phase**: 2 — Integration deep dive
**Date**: 2026-06-06
**Verdict**: **ADOPT-V1 (Datasette at `data.opengem.org`, immutable read-only, mounted as a sibling subdomain to the main app)**

---

## What this loop converts

L076 named Datasette as "the right read-only public-data publisher for OPENGEM's accountability ledger." This Phase 2 loop converts that into the concrete deployment pattern, the data-publishing contract, and the boundary with DuckDB-WASM (L094) and Observable Framework (L091).

The headline: **a Datasette instance at `data.opengem.org`, deployed from a Cloudflare Worker / Cloud Run container, serving immutable SQLite databases generated nightly from the vintage store, with `datasette-cors`, `datasette-publish-cloudrun`, and a curated set of canned queries pinned at the top of every database page.** Total cost: ~$5/mo. Total dev cost: ~1 dev-week initial + 2 hours/month maintenance.

Datasette is the *third* prong of the OPENGEM public data publishing triad alongside the static-build Observable Framework (L091) and the in-browser DuckDB-WASM (L094). Each serves a distinct audience.

## Inspecting the cloned repo

`research-300/clones/datasette/`:

- License: **Apache 2.0** (verified in `pyproject.toml`).
- Maintainer: Simon Willison. Mature, well-funded, stable cadence.
- `datasette/app.py`: ~3,034 lines. ASGI app on top of SQLite.
- Plugin ecosystem: ~300+ published plugins on `datasette.io/plugins`.
- Production deploys: NICAR/IRE, Library of Congress, the World Bank historical dataset, many newsrooms.

The architecture: SQLite (or attached DuckDB) databases as the substrate, an ASGI app that exposes browsable HTML + JSON + CSV per row + per query, with a plugin model for permissions, output formats, custom HTML, charts, exports.

For OPENGEM, the immutable read-only mode is the right shape: we publish snapshots nightly and never let users write.

## Why Datasette in addition to DuckDB-WASM and Observable Framework

The three public-data surfaces look superficially similar but serve different audiences:

| Surface | Audience | What they do | Tech |
|---|---|---|---|
| **DuckDB-WASM** | Developers, data-savvy YouTubers, LLM-tool-builders | Run SQL in the browser, iterate fast, no auth, no signup | Lazy 5MB WASM bundle in Next.js |
| **Observable Framework** | Researchers, journalists, students | Read a curated explainer page with charts + tables | Static HTML/JS at `opengem.org/explainer/` |
| **Datasette** | Power users, dataset crawlers, "give me the raw rows" requests | Browse the database directly, click cell-by-cell, get a CSV per query | ASGI app at `data.opengem.org` |

The Datasette user wants something the other two don't quite deliver: **the row-level browse experience**. They want to click into a row, see related rows, follow foreign-key links, faceted-filter across the schema, and download whatever they're viewing as a one-click CSV. Datasette is the canonical tool for this experience.

It's also the *machine-readable surface* for our data-publishing thesis. Every row has a stable URL (`data.opengem.org/forecasts/forecasts/{row_id}.json`), every facet is bookmarkable, and the entire database is exportable. This is the surface that the L007 distribution thesis aims at — "any LLM, any RSS subscriber, any crawler can reach the data without a SDK." Datasette is the embodiment of that thesis.

## What lives in Datasette

Two SQLite databases, immutable per build, regenerated nightly:

### Database 1 — `forecasts.db`

Tables:
- `forecasts(model_id, country, indicator, horizon, vintage_at, target_date, p10, p25, p50, p75, p90)`
- `realized(country, indicator, observed_at, value, is_final, vintage_published_at)`
- `models(model_id, family, methodology_card_url, license, n_params, last_calibration)`
- `pairs_for_scoring(model_id, country, indicator, horizon, vintage_at, target_date, p10, p50, p90, realized, crps_score)`

This is the V&V scorable substrate. Every paired forecast/realized observation is here, with the CRPS already computed. Anyone can run "show me OPENGEM's worst-CRPS country-indicator pairs in 2025" with one click.

### Database 2 — `indicators.db`

Tables:
- `indicators(country, indicator, observed_at, value, source_id, vintage_at, units)`
- `series_meta(country, indicator, source_id, frequency, license_tag, methodology_url)`
- `vintages(vintage_at, source_id, n_rows, snapshot_hash)`
- `provenance(observation_id, source_id, fetched_at, source_url, fetcher_version)`

This is the raw observation substrate: every datum, every vintage, every provenance link. Anyone can run "show me US CPI history as of 2024-09-15 vs as of 2026-06-01" and see exactly how the revisions evolved.

### Optional Database 3 — `geopolitics.db`

Tables:
- `gpr_country_month(country, year, month, gpr_value, source)`
- `conflict_intensity(country, year, month, intensity_z, source_substrate)` — derived from L085's substrate abstraction
- `events_summary(country, day, event_count_by_type)` — aggregated GDELT + POLECAT + UCDP
- `methodology_versions(date, change_summary)` — the methodology changelog

This is the geopolitical derivative substrate (the GREEN aggregates; nothing under ACLED YELLOW EULA, per L085).

## Deployment pattern

Datasette ships as a single Python ASGI app. We deploy it via `datasette-publish-cloudrun` (or a hand-rolled Dockerfile to Cloud Run):

```bash
# nightly Dagster step — after the vintage-store Parquet export runs
opengem-vintage-export-sqlite --out forecasts.db --table forecasts --table realized --table models --table pairs_for_scoring
opengem-vintage-export-sqlite --out indicators.db --table indicators --table series_meta --table vintages --table provenance
opengem-geopolitics-export-sqlite --out geopolitics.db --substrate green --tables gpr,conflict,events,methodology

# Push to Cloud Run with a fresh container
datasette publish cloudrun \
  forecasts.db indicators.db geopolitics.db \
  --service opengem-data \
  --metadata datasette-metadata.yml \
  --install datasette-cors \
  --install datasette-vega \
  --install datasette-cluster-map \
  --install datasette-leaflet-geojson
```

The `datasette-metadata.yml` defines:
- The site title, description, footer, OPENGEM branding.
- Canned queries (e.g. "Top-10 worst-CRPS forecasts of 2025" → SQL embedded as a saved query).
- Per-table description (semantic glossary lookup).
- License tag per table (GREEN substrate publishable as CC-BY-4.0; YELLOW substrate inferred from L085 substrate flag).

The deployed Cloud Run service is read-only, behind Cloudflare (TLS + CDN cache), at `data.opengem.org`.

## Bandwidth and cost envelope

Datasette serves HTML pages (cheap) and JSON responses (cheap) and CSV downloads (cheap). Cloudflare caches everything for 1 hour by default; we set longer TTLs on canned queries.

Cost components:
- **Cloud Run idle**: $0/mo (Cloud Run scales to zero).
- **Cloud Run active**: ~$5-10/mo for typical Y1 traffic (a few thousand visitor-minutes per day).
- **Cloudflare bandwidth**: $0/mo (free tier covers Y1; Y2+ may need Pro at $20/mo).
- **SQLite file size**: ~300MB total (forecasts + indicators + geopolitics combined). Stored in the container image, regenerated nightly.

**Total**: $5-10/mo at v1, $25-40/mo at Y2 scale.

## Canned queries — the editorial layer

Datasette's "canned queries" feature is the editorial layer. Each database ships with ~10-20 pre-pinned queries that show the data at its best:

```yaml
# datasette-metadata.yml (excerpt)
databases:
  forecasts:
    queries:
      worst_crps_2025:
        title: "Worst-CRPS OPENGEM forecasts of 2025"
        description: "The forecasts we got most wrong. Click through to the post-mortem."
        sql: |
          SELECT model_id, country, indicator, horizon, vintage_at, p50, realized,
            (p50 - realized) AS error, crps_score
          FROM pairs_for_scoring
          WHERE vintage_at >= '2025-01-01' AND vintage_at < '2026-01-01'
            AND crps_score IS NOT NULL
          ORDER BY crps_score DESC
          LIMIT 50
      best_crps_2025:
        title: "Best-CRPS OPENGEM forecasts of 2025"
        sql: |
          SELECT model_id, country, indicator, horizon, vintage_at, p50, realized, crps_score
          FROM pairs_for_scoring
          WHERE vintage_at >= '2025-01-01' AND vintage_at < '2026-01-01'
            AND crps_score IS NOT NULL
          ORDER BY crps_score ASC
          LIMIT 50
      vintage_evolution_usa_gdp_2026q1:
        title: "How our US GDP Q1 2026 nowcast evolved"
        description: "Vintage-by-vintage path; matches the narrative on /explainer/forecast/usa/gdp/2026-Q1/"
        sql: |
          SELECT vintage_at, p10, p50, p90
          FROM forecasts
          WHERE country = 'USA' AND indicator = 'gdp_real_growth'
            AND horizon = 'nowcast' AND target_date = '2026-03-31'
          ORDER BY vintage_at
```

These queries become URLs the user can share and embed. Every "publish your mistakes" promise lives in the worst_crps_2025 page.

## URLs are first-class citizens

Datasette URLs are sharable, citable, machine-readable. Every query produces a stable URL:

- `data.opengem.org/forecasts/forecasts.json?country=USA&indicator=gdp_real_growth&_size=50`
- `data.opengem.org/forecasts/worst_crps_2025.csv`
- `data.opengem.org/forecasts/forecasts/12345.json`  (single row)

These URLs go in the OPENGEM RSS feeds (L179), in citation widgets (L158), in the OpenAPI spec as references (L249), and in the Substack/Medium copy-paste workflow (L112). They are the *machine-readable trust signal* of the substrate.

## Plugins we install

- **`datasette-cors`** — cross-origin headers so JS clients can fetch JSON.
- **`datasette-vega`** — inline Vega-Lite charts for query result visualization.
- **`datasette-cluster-map`** — automatic map view for queries with lat/lng columns.
- **`datasette-leaflet-geojson`** — render GeoJSON cells as map embeds.
- **`datasette-rich-extras`** — Markdown rendering for description fields.
- **`datasette-block`** — IP blocklist for abuse.

Avoid:
- **`datasette-auth-*`** — not needed for read-only public.
- **`datasette-edit-*`** — write capabilities are explicitly out of scope.

## The "fork the database" affordance

Every Datasette page has a "Download .db" link. Users can download the entire `forecasts.db` SQLite file (~150MB), open it locally, run any query they want, write their own analysis. This is the strongest "you own the substrate" signal we can ship — it's not even an API, it's a literal file the user runs locally.

For research-grade users this is the *winning* affordance. The journalist who builds a story on OPENGEM data can vendor the SQLite alongside her notebook and the analysis is reproducible regardless of what OPENGEM does in the future.

## How Datasette plays with DuckDB-WASM and Observable Framework

- **Datasette serves row-level browse + canned queries + CSV downloads + full-database download.** It's the **lookup + curated** surface.
- **Observable Framework serves chart-grade explainer pages with narrative.** It's the **story + interpretation** surface.
- **DuckDB-WASM serves in-browser ad-hoc queries against Parquet.** It's the **explore + power-user** surface.

A typical user flow: a researcher reads the Observable Framework explainer page for US GDP, clicks "see the vintage history" → lands on Datasette's canned query, clicks "download CSV," or clicks "open in DuckDB-WASM" which loads the equivalent Parquet into the Compare-2 page. All three surfaces are deeply linked.

## Risks

1. **Cloud Run cold-start latency** can hit 2-5 seconds for the first request. Mitigation: minimum 1 instance during business hours, scale-to-zero overnight.
2. **Schema migrations** require regenerating the SQLite file. Mitigation: nightly rebuild from source is the canonical path; no in-place migration.
3. **CSV download abuse** — single user downloading 10K queries to scrape. Mitigation: Cloudflare rate limiting at the subdomain level; aggressive cache-control on canned queries.
4. **Datasette plugin breakage on upgrade**. Mitigation: pin plugin versions; quarterly compatibility check.
5. **License-tag confusion**. Mitigation: every table's metadata declares its license tag from L282; YELLOW substrate (if any made it through) gets a red badge in the UI.

## Cost summary

| Item | Y1 cost |
|---|---|
| Cloud Run hosting | $5-10/mo |
| Cloudflare bandwidth | $0/mo |
| SQLite generation (nightly Dagster) | ~5 min compute, $0/mo marginal |
| Initial setup + metadata + canned queries | 1 dev-week |
| Quarterly plugin maintenance | 2 hours/quarter |
| **Total** | **~$5-10/mo, ~1 dev-week + 8 hr/year ongoing** |

## What this loop produced

- Three-database design (forecasts, indicators, geopolitics) with explicit table contracts.
- Deployment pattern via `datasette publish cloudrun`.
- Editorial canned queries as the "publishes its mistakes" surface.
- Plugin selection rationale.
- Triad with Observable Framework + DuckDB-WASM articulated.
- ~$5-10/mo, ~1 dev-week ramp.

## What comes next

- **L107** — JSON-LD + schema.org for SEO (Datasette pages benefit).
- **L179** — RSS / Atom feed catalog (Datasette URLs go in).
- **L253** — Datasette mounted at `/data` for raw access (Phase 5 code).
- **L285** — Accountability ledger (uses worst-CRPS canned queries as evidence).

## Related

- [[L076-datasette]] — Phase 1 deep dive.
- [[L077-duckdb-motherduck]] — sibling pattern.
- [[L091-observable-framework-explainer-reports]] — sibling pattern.
- [[L094-duckdb-local-first-analytics]] — sibling pattern.
- [[L007-distribution-thesis]] — the distribution wedge this serves.
- [[L179-rss-atom-feed-catalog]] — downstream consumer.
- [[L253-datasette-prototype]] — Phase 5 code.
- [[L282-license-audit]] — license-tag source.
- inspected source: `/mnt/bigdata/home/edgardo/projectsd/opengem/research-300/clones/datasette/pyproject.toml`
- inspected source: `/mnt/bigdata/home/edgardo/projectsd/opengem/research-300/clones/datasette/datasette/{app.py,cli.py,database.py}` (3,034 + 25.6K + 32.6K lines, Apache 2.0)
