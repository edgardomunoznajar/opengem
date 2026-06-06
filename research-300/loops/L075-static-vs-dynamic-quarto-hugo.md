# L075 — Static-Site Dashboards: Hugo + Datasette Pattern, Quarto, When OPENGEM Goes Static vs Dynamic

**Loop**: 075 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Thesis of this loop

The Bloomberg terminal model is *dynamic to its core*: live tickers, live chat, live order books. OPENGEM rejected real-time intraday in L001. That rejection is the doorway to a *predominantly static* dashboard strategy — a substrate where most pages are pre-built, deployed to a CDN, and served at near-zero cost, with a thin dynamic shell around the parts that genuinely need to be live (alerts, watchlists, MCP server, search).

This loop frames the static/dynamic boundary and surveys the static-site tools that fit OPENGEM's needs *that aren't* Observable Framework (L066), Evidence (L067), or Astro (L074). The two candidates here:

- **Hugo + Datasette pattern**: Hugo for the content site, Datasette serving the data API beneath. The "static facade over a read-only data API."
- **Quarto**: the modern Pandoc-based scientific document publishing system. Successor to RMarkdown / Jupyter Book in many ways.

Verdict: **Both are great in different niches.** Quarto is **ADOPT-V1** for the methodology pages and academic-style replication packages. Hugo is **EVALUATE-LATER** — Observable Framework / Astro likely cover the same use case more idiomatically.

## The static-vs-dynamic OPENGEM boundary

OPENGEM ships *seven* surfaces. The static/dynamic call for each:

| Surface | Cadence | Static or Dynamic | Tool |
|---|---|---|---|
| Country page (CPI, GDP, unemployment, etc.) | Daily/weekly/monthly | **Static** (rebuild on data update) | Observable Framework / Astro |
| Indicator page | Daily/weekly/monthly | **Static** (rebuild on data update) | Observable Framework / Astro |
| Scenario page | Vintage rollover | **Static per vintage** | Observable Framework |
| Forecast page (interactive bands, vintage scrubber, hover) | User-driven | **Dynamic shell, static data** | Next.js + Lightweight Charts |
| Search / command bar | User-driven | **Dynamic** | Next.js + Algolia / Typesense |
| Watchlist / alerts | User-driven, account-state | **Dynamic** | Next.js + Postgres + auth |
| Methodology / about / changelog | Quarterly | **Static** | Quarto or Observable / Astro |
| Public ledger (raw data exposure) | Continuous | **Static facade + dynamic data API** | Datasette or custom |
| Geopolitical pulse 3D globe | Hourly/daily | **Dynamic shell, static data** | Next.js + globe.gl |

So OPENGEM is **~70% static, ~30% dynamic**. That ratio drives the cost model — most of the dashboard runs on Cloudflare Pages free, with a small Next.js app on Cloud Run / Vercel handling the dynamic parts.

## Quarto: the methodology-page workhorse

Quarto is RStudio's (Posit's) Pandoc-based publishing system. It compiles `.qmd` (Quarto Markdown) files into HTML, PDF, ePub, slides, dashboards, and more. It runs Python, R, Julia, Observable JS code cells inline and embeds the output.

For OPENGEM, Quarto is *the right tool* for:

1. **Methodology pages.** "How OPENGEM computes the GPR composite," "OPENGEM forecast scoring methodology," "data lineage for IMF SDMX series." These are written in Markdown with embedded Python/R code that *runs* (or is executed at render time) and embeds the output figures with proper citations.

2. **Replication packages.** When OPENGEM publishes a forecast post-mortem, it should ship a Quarto report that re-runs the analysis from raw data — the "your forecast was wrong, here's the audit trail" artifact. Quarto's executable-document model is exactly this.

3. **PDF tearsheets.** Quarto compiles to PDF via LaTeX. The "branded tearsheet for the IC" deliverable (an OPENGEM customer-tier feature) is a Quarto template parameterized by country/indicator.

4. **Academic citations.** Quarto's citation model (CSL, Zotero integration) is the standard for academic-style citation rendering. The "OPENGEM appears in a press piece next to WEO and OECD" Y5 success criterion (L001) is helped by having academic-citation-grade Quarto outputs in the corpus.

Hosting: Quarto compiles to static HTML, deployed on the same Cloudflare Pages free tier. Zero hosting cost.

License: **MIT** for Quarto itself. Posit Connect (the paid hosted version) is optional and OPENGEM does not need it.

Ramp-up: 1-2 days for someone who knows RMarkdown / Jupyter / Pandoc. 1 week from cold start.

## Quarto vs Observable Framework

These two overlap *significantly*. Both produce static HTML with embedded data and code. Both support build-time data loaders. Both deploy to any static host. The clean division for OPENGEM:

- **Observable Framework**: the *dashboard pages* — country page, indicator page, scenario page. JS-first, Plot-first, interactive even when static, dashboard-grid layouts.
- **Quarto**: the *prose pages* — methodology, replication, academic-style write-ups, PDF tearsheets. Markdown-first, narrative-first, citation-aware.

The two coexist in the same OPENGEM repo. The Quarto outputs link to the Observable Framework dashboards and vice versa.

## Hugo + Datasette pattern

Hugo is a Go-compiled static-site generator. It's the fastest SSG by build time (10k pages in seconds) and the most flexible by templating language (Go templates). It is *content-first*: written for blogs, documentation sites, marketing sites. Not designed for data-app authoring.

The "Hugo + Datasette" pattern is:
- Hugo builds the static content site (text-heavy, blog-style).
- Datasette runs alongside, serving a queryable read-only API over a SQLite DB.
- Hugo pages link to / embed Datasette query results.

This pattern is a *valid* OPENGEM architecture and Simon Willison has championed it personally. The strengths:

- Hugo's build speed scales to 100k+ pages — perfect for the country×indicator long-tail SEO matrix (L002).
- Datasette gives the *data exposure* layer for free (L076 covers this in depth).
- Both are battle-tested, both deploy cheaply.

The weaknesses for OPENGEM specifically:

- **Hugo's templating is not React.** Custom components (forecast charts, sparkline grids, vintage drawers) require either client-side JS (loaded externally) or template gymnastics.
- **No native data-loader story.** Hugo expects data in `data/` directories at build time. The Python adapter integration is awkward.
- **The aesthetic is "blog."** Theming to terminal-density Bloomberg-feel is real CSS work.
- **No first-class interactive chart story.** Drop in Plotly or Observable Plot as plain `<script>` tags, sure, but you're now hand-rolling what Observable Framework gives you natively.

**Hugo's role in OPENGEM**: maybe none. Observable Framework wins the data-app static pages. Astro wins as backup. Quarto wins the prose pages. There isn't a clear remaining niche where Hugo is the best tool.

The exception: **OPENGEM's marketing site / landing pages / blog**. If OPENGEM ever ships a separate marketing site (which it probably doesn't need until Y2-Y3 paid tier launch), Hugo is the obvious tool. EVALUATE-LATER.

## When OPENGEM is dynamic, period

Three irreducibly dynamic surfaces:

1. **Search / command bar**: user types, results return live. Algolia ($0 starter, $500+/mo at scale) or Typesense (self-host, $0) or Meilisearch (self-host, $0). All three are credible; Typesense likely wins on $0 cost + ergonomics.

2. **Watchlist / alerts**: user-account state. Requires a database (Postgres), an auth layer (Auth.js or Clerk-OSS or Lucia), and a small Next.js API. Cost: ~$15-30/mo for a small Cloud Run + Cloud SQL setup.

3. **MCP server**: an HTTP API speaking the Model Context Protocol. Open-source Apache 2.0 spec. Cost: ~$10-30/mo for a Cloud Run instance.

Everything else can be static, with rebuild-on-data-update CI/CD.

## The rebuild-on-update discipline

The Achilles heel of static dashboards is *staleness*. The mitigation:

- Every data-source push to the OPENGEM Postgres triggers a webhook to GitHub Actions.
- GitHub Actions runs `observable build` (or `astro build`) for the affected pages.
- Output deployed to Cloudflare Pages via the `wrangler` CLI.
- End-to-end latency from data update to deployed page: ~3-8 minutes.

For OPENGEM's daily/weekly/monthly cadence, this is *fine*. The "live ticker" affordance — for those who want sub-minute updates — uses the Next.js dynamic layer reading from the API directly.

## Cost summary

| Tool | License | Cost | Use | Ramp |
|---|---|---|---|---|
| Quarto | MIT | $0 | Methodology, replication, tearsheets | 1 week |
| Hugo | Apache 2.0 | $0 (mostly skipped) | Potential Y2 marketing site | 1 week |
| Datasette | Apache 2.0 | $0 | Read-only data API (see L076) | 1 week |
| Cloudflare Pages | n/a | $0 | Static hosting | 1 day |
| GitHub Actions (CI rebuild) | n/a | $0 (free 2000 min/mo) | Rebuild pipeline | 1 day |
| Typesense self-host | GPL-3 | $5/mo | Dynamic search | 2 days |

## Verdict

- **Quarto** for methodology pages, replication packages, PDF tearsheets: **ADOPT-V1**.
- **Hugo** for OPENGEM Y2 marketing site if/when needed: **EVALUATE-LATER**.
- **Hugo + Datasette** pattern as primary dashboard architecture: **SKIP** in favor of Observable Framework + Datasette.
- **Static-first dashboard discipline overall**: **ADOPT-V1**. ~70% of OPENGEM is static.

## What comes next

- **L076** evaluates Datasette as the read-only data API.
- **L091** is the Phase 2 deep dive on Observable Framework for explainer reports.

## Related

- [[L066-observable-framework]] — primary dashboard static tool
- [[L076-datasette]] — data API beneath
- [[L074-sveltekit-solid-astro-qwik]] — Astro as Observable Framework backup
