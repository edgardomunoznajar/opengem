# L091 — Observable Framework for Explainer Reports: How OPENGEM Produces Them

**Loop**: 091 / 300
**Phase**: 2 — Integration deep dive
**Date**: 2026-06-06
**Verdict**: **ADOPT-V1 (long-tail SEO pages + methodology cards + per-vintage explainers + tearsheet exports)**

---

## What this loop produces

L066 named Observable Framework as the most strategically aligned dashboard tool surveyed in Phase 1. This Phase 2 loop converts that framing into a concrete production pattern: *how does OPENGEM use Observable Framework, what does the build pipeline look like, what's the page taxonomy, what does the developer ergonomics actually feel like in practice?*

The answer: **a parallel static-site build that runs every OPENGEM data refresh, mounted at `https://opengem.org/explainer/...`, templated against country/indicator/methodology slugs, deployed to Cloudflare Pages for $0/mo, with data loaders that read directly from the OPENGEM vintage store via DuckDB-WASM.** The build is the long-tail SEO play (L066's identified TradingEconomics-moat-attack), the per-vintage explainer ("here's what we said on 2024-09-15 and why"), and the citable methodology card surface (cited in every Next.js chart's pop-up).

## Inspecting the cloned repo

`research-300/clones/observable-framework/`:

```
observable-framework/
  src/                   # the Framework source itself (TypeScript)
    bin/                 # CLI entry points (`observable build`, `observable preview`)
    duckdb.ts            # DuckDB-WASM browser integration
    deploy.ts            # Cloudflare/Observable Cloud deploy targets
    create.ts            # template scaffolding
    config.ts            # observablehq.config.{js,ts} loader
    ...
  examples/              # 40+ example projects
    api/                 # API-backed dashboard
    eia/                 # EIA electricity grid — directly analogous to OPENGEM
    loader-duckdb/       # DuckDB-WASM data loaders
    loader-parquet/      # Parquet loaders
    loader-postgres/     # Postgres loaders (TimescaleDB compatible)
    geotiff/             # geo + map layers
    ...
  templates/             # `observable create` scaffolds
  observablehq.config.ts # the Framework's own config (themes, sidebar, head)
```

License: **ISC** (MIT-equivalent). Last commit recent (June 2026). Maintained by Observable Inc., the company behind D3 and Observable Notebooks.

## The EIA example — direct OPENGEM analog

The `examples/eia/` project is the closest direct analog to what OPENGEM ships. Looking at its `src/`:

```
eia/src/
  components/
    charts.js              # Observable Plot chart compositions
    map.js                 # D3-geo map of US states
  data/
    us-demand.csv.js       # data loader hits EIA REST API at build time
    us-demand.csv          # output of the loader (cached)
    country-interchange.csv
    us-states.json.js
    us-counties-10m.json
    eia-ba-hourly.csv.js
  index.md                 # the actual page — Markdown + embedded JS
```

The pattern is clean:
- **Data loaders** (`*.csv.js`, `*.json.js`, `*.json.sh`, etc.) are scripts in *any* language that run at build time and emit static files. The example `us-demand.csv.js` is 28 lines: fetch from the EIA REST API, transform via d3, `process.stdout.write` CSV.
- **The Markdown page** imports the chart components and renders them with the data loaders as static sources.
- **The components** are plain JS modules with `export function countryInterchangeChart(data)` returning Observable Plot output.

There is no runtime server. The whole site is `vite build`-equivalent: a directory of HTML + JS + JSON that Cloudflare Pages serves for free.

## OPENGEM's Observable Framework site — the page taxonomy

The site lives at `https://opengem.org/explainer/` and ships four page categories:

### Category 1 — Long-tail country × indicator pages

URL: `/explainer/{country-slug}/{indicator-slug}/`

Example: `/explainer/usa/gdp-real-growth/`

Content:
- Hero chart: 25-year history + latest OPENGEM forecast band + WEO/OECD overlay.
- Methodology pop-up summary inline.
- Vintage timeline: a small chart showing how our forecast for the next quarter has evolved across the last 12 vintages.
- "Compare to other countries" cross-link.
- JSON-LD schema markup for SEO.
- Citation widget (DOI-style — L158).

Generated count: ~200 countries × ~30 indicators = **6,000 pages**.

These pages are the *TradingEconomics SEO moat attack*. Every country × indicator combination is a real URL with real server-side-rendered HTML and a useful OG card. They get indexed; they show up in long-tail Google searches; they pull traffic that the interactive Next.js dashboard would never reach because Google doesn't crawl JavaScript-rendered SPAs effectively.

### Category 2 — Methodology cards

URL: `/explainer/methodology/{model-id}/`

Example: `/explainer/methodology/dfm-us-tier-v-v3/`

Content:
- Model description (DFM specification, panel composition, EM convergence diagnostics).
- The Bok et al. (2017) reference and our news-decomposition adaptation (L086).
- Backtest CRPS over the last 5 years.
- Code link to the `opengem-l3-dfm` package + version.
- "Cite this methodology" copy-button.

Generated count: one per published L3 ensemble member + one per L1 baseline + one per L2 variant = ~25 pages at v1, growing.

### Category 3 — Per-vintage explainers

URL: `/explainer/forecast/{country}/{indicator}/{vintage-date}/`

Example: `/explainer/forecast/usa/gdp/2026-06-01/`

Content:
- The forecast as published on that vintage date (immutable).
- The L3 ensemble decomposition (which models said what, with which BMA weights).
- The news decomposition for the trailing 4 weeks (what releases moved the forecast).
- The realized value (if available since publication) and the miss size.
- A back-link to the methodology card and the input panel definition.

This is the load-bearing "publishes its mistakes" UI. Every vintage gets a permanent URL. Every miss has a post-mortem in the same place as the original forecast. Generated count: scales linearly with vintages × indicators — ~6,000 country-indicator-vintages per quarter, capped by retention policy.

### Category 4 — Track-record sheets

URL: `/explainer/track-record/{country}/{indicator}/{horizon}/`

Example: `/explainer/track-record/usa/gdp/4Q/`

Content:
- The full backtest of every OPENGEM forecast vintage at this horizon.
- CRPS / log-score / MAE / RMSE over time.
- Calibration plot (PIT histogram).
- Comparison against WEO / OECD / SPF consensus.
- Underwater-miss chart (the canonical accountability artifact, L013).

Generated count: ~200 × 30 × 5 horizons = ~30,000 pages, but most are sparse early on (no real track record for emerging-market quarterly horizons). Practical at v1: ~5,000 pages with meaningful content.

## Build pipeline

```
                ┌──────────────────────────────────┐
                │  OPENGEM Vintage Store (TimescaleDB) │
                └──────────────────────────────────┘
                                │
                                ▼
                ┌──────────────────────────────────┐
                │  Nightly export job (Dagster)    │
                │  → emit Parquet per country/ind  │
                │     to R2 at canonical paths     │
                └──────────────────────────────────┘
                                │
                                ▼
                ┌──────────────────────────────────┐
                │  Observable Framework build job  │
                │  - reads R2 Parquet via DuckDB   │
                │  - generates ~10K+ pages         │
                │  - emits static HTML+JS+JSON     │
                └──────────────────────────────────┘
                                │
                                ▼
                ┌──────────────────────────────────┐
                │  Cloudflare Pages deploy         │
                │  - HTTPS, free, CDN-cached       │
                │  - served at /explainer/*        │
                └──────────────────────────────────┘
```

Build cadence: daily. The build runs against a snapshot of yesterday's vintage store, generates ~10,000 pages, and deploys to Cloudflare Pages.

Build duration: at ~10K pages with template caching and incremental builds, target ~30-60 minutes. This is the *one real engineering challenge* with Observable Framework at scale — Framework's incremental builds work, but on a fresh CI runner the full build can take 30+ minutes. We accept this and run the build during the early-morning data quiet period.

Build cost: ~5 min × ~30 days × ~$0.01/min for Cloudflare Pages Workers Build (or GitHub Actions free tier) = $0/mo.

## The data loader pattern

Each page reads from the `opengem-explainer-data` Parquet snapshot via DuckDB-WASM at build time. A representative loader:

```javascript
// src/data/country-indicator-history.parquet.js
// Emits parquet directly, no need to decode to CSV.
import { DuckDBInstance } from "@duckdb/node-api";

const { country, indicator } = process.env;

const db = await DuckDBInstance.create();
const conn = await db.connect();

await conn.run(`
  COPY (
    SELECT observed_at, value, vintage_at
    FROM read_parquet('https://r2.opengem.org/vintage/${country}_${indicator}.parquet')
    ORDER BY observed_at, vintage_at
  ) TO STDOUT (FORMAT PARQUET);
`);
```

Then `index.md` for the country page:

```markdown
---
theme: dashboard
title: "${country} ${indicator} — OPENGEM Explainer"
---

# ${country.toUpperCase()} ${indicator.toUpperCase()} — OPENGEM forecast & track record

```js
const history = FileAttachment("./data/country-indicator-history.parquet").parquet();
const forecast = FileAttachment("./data/country-indicator-forecast.parquet").parquet();
const consensus = FileAttachment("./data/consensus-overlay.parquet").parquet();
```

```js
import {forecastBandChart} from "./components/forecast-band-chart.js";
display(forecastBandChart({history, forecast, consensus, width: 980}));
```

Source: OPENGEM vintage store. Last updated: ${new Date().toISOString()}.
Citation: [Cite this view](/cite/${country}-${indicator}/${vintage_date})
```

The pattern is dense in info, light on code. Each page is ~30-50 lines.

## Page generation strategy

Two options:

### Option A — Static per-page Markdown (canonical Framework pattern)

Generate one `.md` file per page. The Phase 5 build script walks the country × indicator product and writes `src/explainer/{country}/{indicator}/index.md` with templated content. Observable Framework `build` then renders each file.

Pro: each page is a real Markdown file in source control; easy to inspect; easy to customize per page.
Con: 10K Markdown files in the repo. Diff noise. Heavy git history.

### Option B — Dynamic page generation via `dynamicPaths`

Framework's `dynamicPaths` config (added 2024) lets one Markdown template render many URLs. We write `src/explainer/[country]/[indicator]/index.md` and config emits all 6,000 country × indicator combinations.

Pro: 1 source file, 6,000 generated pages. Clean repo.
Con: Slightly newer Framework feature; ergonomic edge cases on per-page meta tags.

**Pick: Option B.** Single template, generated pages, easier maintenance. Worth tolerating the few edge cases.

## Tearsheet PDF export

The L143 print/PDF design says every page should be exportable as a PDF tearsheet. Observable Framework's static HTML pages are *natural* PDF exports — `chrome --headless --print-to-pdf` produces a clean A4 PDF with all charts rendered. The print stylesheet (L143) tunes typography for print.

We ship a small `tearsheet/` route per page: `https://opengem.org/explainer/usa/gdp/tearsheet.pdf` rendered nightly via headless Chrome and cached. Approximately ~$0.01 per PDF generation at scale; cost ~$10/mo for the full 10K-page nightly run.

## Theming + brand consistency

Observable Framework's theme system (CSS custom properties) is configurable in `observablehq.config.ts`. We define the OPENGEM theme tokens once:

```javascript
// observablehq.config.ts
export default {
  title: "OPENGEM Explainer",
  theme: ["dark", "midnight"],
  style: "style.css",
  head: `
    <link rel="canonical" href="https://opengem.org/explainer/">
    <meta property="og:site_name" content="OPENGEM World Dashboard">
    <link rel="alternate" type="application/rss+xml" href="/feed.rss">
  `,
};
```

```css
/* src/style.css */
:root {
  --theme-foreground: #ffaa66;        /* terminal-orange */
  --theme-background: #0c0c0c;
  --theme-foreground-faint: #888;
  --theme-foreground-faintest: #555;
  /* … shared with the Next.js Tailwind tokens via a generated JSON */
}
```

The single point of style coordination across Next.js and Observable Framework is a `design-tokens.json` file that both stacks consume. Updates flow through CI.

## SEO surface

Each generated page ships:

- `<title>` with the country and indicator.
- `<meta description>` with the latest forecast + a short narrative.
- OG image: a pre-rendered PNG of the forecast band chart (per L107).
- JSON-LD schema markup (`Article` + `Dataset` types).
- Canonical URL.
- Cross-links to related country/indicator pages.

This is the L107 SEO loop's downstream landing. Done correctly, the long-tail country/indicator/explainer pages should outrank TradingEconomics on niche queries within 6-12 months of consistent indexing.

## Cost summary

| Item | Y1 cost |
|---|---|
| Initial Framework site build | 4 dev-weeks |
| Nightly build job (CI) | $0/mo (Cloudflare Workers Build) |
| Cloudflare Pages hosting | $0/mo (free tier, unlimited bandwidth) |
| Per-page PDF tearsheet generation | ~$10/mo |
| **Total operating** | **~$10/mo** |
| **Total v1 ramp** | **4 dev-weeks** |

Cheap. Strategic. Correct.

## Risks

1. **Build duration grows with page count.** At 30K pages the build could approach 2 hours. Mitigation: split the build by region, parallelize CI jobs, prune stale per-vintage pages older than 1 year.

2. **DuckDB-WASM in the loader fails on cold-start CI.** Mitigation: pin the DuckDB version, cache the WASM binary, fallback to a Python loader if DuckDB-WASM regresses.

3. **The Framework's API surface changes.** Observable is still pre-1.0 (as of mid-2026, in the 1.x preview range). Mitigation: pin minor versions; monitor the changelog; budget half a day per quarter for upgrades.

4. **Cross-link consistency with Next.js drifts.** Mitigation: shared URL convention (L154); CI link-checker that walks both sites looking for 404s.

5. **The "static site doesn't update intra-day" problem.** The L066 thesis tolerates this — OPENGEM is daily/weekly/monthly cadence. For users wanting "latest as of right now," the Next.js interactive surface serves them.

## What this loop produced

- Four-category page taxonomy (long-tail + methodology + per-vintage + track-record).
- Build-pipeline diagram tying TimescaleDB → R2 Parquet → DuckDB-WASM → Framework → Cloudflare Pages.
- Concrete `index.md` + data-loader code skeleton.
- Theme/design-token coordination plan with Next.js.
- Dynamic pages via `dynamicPaths` as the canonical pattern.
- ~$10/mo operating cost, 4-week initial ramp.

## What comes next

- **L095** — Datasette public ledger (sibling static surface for raw data).
- **L107** — JSON-LD + schema.org for SEO (downstream consumer).
- **L143** — Print/PDF export design (tearsheet pattern).
- **L158** — Cite-this-view (DOI-like) (consumer of methodology card URLs).

## Related

- [[L066-observable-framework]] — Phase 1 verdict.
- [[L089-streamlit-vs-nextjs-dashboard-frontend]] — sibling frontend strategy.
- [[L090-grafana-vs-custom-operational-dashboards]] — sibling ops surface.
- [[L107-jsonld-schema-seo]] — SEO consumer.
- [[L154-url-convention]] — shared link contract.
- inspected source: `/mnt/bigdata/home/edgardo/projectsd/opengem/research-300/clones/observable-framework/examples/eia/src/*`
- inspected source: `/mnt/bigdata/home/edgardo/projectsd/opengem/research-300/clones/observable-framework/src/duckdb.ts`
