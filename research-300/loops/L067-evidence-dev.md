# L067 — Evidence.dev: SQL-First Analytics Website Builder

**Loop**: 067 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Thesis of this loop

Evidence.dev is the "SvelteKit + Markdown + SQL" answer to the same prompt Observable Framework (L066) answers with "Vite + Markdown + JS." It is the *closest competitor* to Observable Framework in spirit: static site builder, code-first, BI-as-code, deployable to any static host, free and MIT-licensed.

The differentiator is the *interaction model*: Evidence is SQL-first (every chart is a SQL query against a warehouse, baked at build time), while Observable is JS-first (every chart is JS, the SQL is one of many possible data loaders). For a team whose mental model is "everything starts as a SQL query against the warehouse," Evidence is the most ergonomic tool in this entire survey.

For OPENGEM, which is *not* warehouse-shaped — OPENGEM's data is curated, methodology-stamped, vintage-tracked indicator series, not a Snowflake table you BI over — Evidence is the *wrong* primitive at the top of the stack. But it's a fascinating reference for the SQL-first reporting layer and worth a real evaluation.

This loop: **EVALUATE-LATER** for OPENGEM. The Observable Framework path is strategically simpler. But the Evidence model is a serious specimen worth understanding.

## What Evidence is

- Open source under the **MIT license**. No "open core" trick. There's a managed cloud (Evidence Cloud, paid) but the OSS is genuinely complete.
- Tech stack: SvelteKit (compiles to static HTML/JS/CSS for build-time), Markdown-with-embedded-SQL authoring, DuckDB or warehouse-of-your-choice at build time.
- Authoring: write a `.md` file, embed a SQL query in a fenced code block, reference the query result by name in another fenced block as a chart. The chart is rendered at build time as static SVG/Canvas.
- Datasources: BigQuery, Snowflake, Databricks, Postgres, MySQL, MSSQL, Redshift, MotherDuck, DuckDB, CSV, parquet, faker. Comprehensive.
- Components: ~30 chart and data components (line chart, bar chart, big-value, scatter, area, table). Slimmer than Observable Plot but enough for 90% of analytics dashboards. Custom Svelte components are possible but require Svelte familiarity.
- Theming: Tailwind-based, configurable but opinionated. The default looks like Stripe's docs — clean, professional, not Bloomberg-dense.
- Deployment: Vercel, Netlify, Cloudflare Pages, GitHub Pages, or any static host. Build runs in CI.

## Specimen inspection

The cloned repo (`research-300/clones/evidence-dev/`) is a monorepo of ~30 packages: the core builder, the component library, and a fleet of datasource adapters. The architecture is clean — each datasource is a thin shim, the core treats query results as normalized JSON.

Notable from `evidence-dev/package.json`:
- Heavy reliance on DuckDB-WASM (`@duckdb/duckdb-wasm`) for in-browser query execution.
- Universal SQL approach: every query goes through DuckDB at build time, regardless of source. This is *clever*: pull data once with the source adapter, then let DuckDB do the SQL. The user can write Postgres-flavored SQL even if their source is BigQuery.
- The `core-components` package contains the chart library; it's SvelteKit-native.

## Where Evidence wins vs Observable Framework

1. **SQL is the lingua franca.** Macro analysts know SQL. A SQL query is more debuggable than a JS data loader. If OPENGEM ever had a team of analysts writing reports, Evidence is the obvious tool.
2. **DuckDB-WASM in the browser** for the truly enormous joins. Observable Framework can do this too but it's not the default; Evidence's universal SQL model makes it natural.
3. **Filters and inputs are first-class** via the `<Dropdown />` and `<Slider />` components, with cross-filter behavior. Observable's inputs are JS, more flexible but less ergonomic.
4. **Cleaner default aesthetic.** Tailwind-based, looks professional out of the box.
5. **Templated pages** with URL params (`/[country].md`) generate per-country pages from a single template. Same pattern as Observable's `index.md.js`.

## Where Evidence loses vs Observable Framework

1. **Chart vocabulary is narrower.** Observable Plot is a grammar of graphics — composable, infinite. Evidence has 30 components, fixed. Forecast bands with multiple confidence levels, vintage overlays, methodology-call-outs — possible in Evidence with custom Svelte, but the seams show.
2. **JS escape hatch is harder.** When you outgrow the components, dropping into custom Svelte mid-page is more friction than dropping into custom JS in an Observable Framework page.
3. **SvelteKit bias.** Most macro analysts don't know Svelte. The OPENGEM team doesn't either. The escape hatch from Evidence's defaults requires learning Svelte.
4. **Storytelling primitives are weaker.** Methodology pop-ups, annotation tables, vintage drawers — all easier in plain JS + HTML (Observable) than in SvelteKit components.

## License and cost

- **Evidence OSS**: MIT, free forever.
- **Evidence Cloud** (managed hosting + auth + scheduled builds + a "homepage builder"): $499/mo for up to 25 users, custom pricing above. Not relevant for OPENGEM.
- **Hosting**: same as Observable — free on GitHub Pages / Cloudflare Pages, ~$5-15/mo on S3+CloudFront.
- **DuckDB-WASM bundle**: ~5MB. Loads once, caches.

## Why Evidence is *not quite* the right top-of-stack for OPENGEM

OPENGEM's data does not live in a warehouse. It lives in:
- Postgres + TimescaleDB (canonical indicator series, vintage history).
- Parquet on S3 (large bulk forecast outputs).
- Python notebooks (one-shot computations from the modeling layer).
- A Python core library (the OPENGEM adapter ecosystem).

A SQL-first builder forces the data into "SQL-shaped." That's *fine* — Postgres serves SQL natively — but it discourages the rich-Python integration that makes OPENGEM's forecast layer composable. Observable Framework's "any language at build time" loader is closer to OPENGEM's reality.

The other consideration: Evidence's chart vocabulary, while clean, is not where forecast bands with vintage overlays live naturally. Observable Plot has been chosen explicitly by Mike Bostock as the modern grammar for statistical graphics, and OPENGEM's chart vocabulary maps to it almost 1:1.

If OPENGEM had a SQL-shaped data stack (Snowflake or BigQuery + dbt), Evidence would be the default. We don't. So Observable Framework wins by 60-40.

## Where Evidence *might* belong in OPENGEM

A "data-tearsheet" template that an analyst writes against the OPENGEM API (which speaks SQL via DuckDB-WASM querying the JSON+Parquet exports) could be Evidence. This is a Y2-Y3 nice-to-have: "any analyst can fork a tearsheet, point it at their custom SQL view, redeploy in 5 minutes." Evidence is genuinely good at this. But it's not the V1 dashboard.

## Verdict

- **OPENGEM public dashboard**: **SKIP** in favor of Observable Framework (L066) + Next.js (L073).
- **OPENGEM analyst-tearsheet template (Y2-Y3)**: **EVALUATE-LATER**. A "fork-this-tearsheet" public template might serve a real demand.
- **Evidence Cloud**: **SKIP**.

## Cost summary

| Use | Cost | Ramp |
|---|---|---|
| Self-host Evidence on Cloudflare Pages | $0/mo | 1-2 weeks |
| Evidence Cloud | $499/mo | 1 day |
| Tearsheet template (Y2-Y3) | $0/mo | 2 weeks |

## What comes next

- **L068** examines the closed-source notebook BI tools (Hex, Mode) for design pattern theft.
- **L069** picks the visualization library family across all OPENGEM chart types.

## Related

- [[L066-observable-framework]] — the primary public-dashboard winner; Evidence loses to it on chart vocabulary
- [[L076-datasette]] — the read-only public-data complement
- [[L069-d3-vega-plotly]] — which chart grammar OPENGEM picks
