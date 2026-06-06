# L296 — SEO content engine plan

**Loop**: 296 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis

OPENGEM's SEO content engine is **programmatic, not editorial**. We generate ~10,000 high-quality, statically renderable pages from a single page template × country × indicator × horizon — and serve each one as a fast, semantically marked-up, JSON-LD-injected, canonically URL'd page. Google + Bing + LLM indexers (Perplexity, ChatGPT-search, Claude-search) consume all of them at near-zero marginal cost.

This is exactly the playbook OurWorldInData runs, and it works because the underlying data substance is genuinely high-value and the maintenance cost amortizes across pages.

## The page matrix

Programmatic pages emitted by OPENGEM:

| Page family | Count at v1 | URL pattern |
|---|---|---|
| Country pages | 22 (Tier-V) + 110 (Tier-T) = 132 | `/countries/[iso3]` |
| Indicator pages | 7 canonical × all countries = ~924 | `/indicators/[id]` (canonical) + `/c/[iso3]/i/[id]` (cross-paginated) |
| Forecast detail pages | 132 countries × 7 indicators × 5 horizons = ~4,620 | `/forecasts/[vintage_id]/[iso3]/[indicator]/[horizon]` |
| Scenario pages | 10 active + 50 historical (Y1) = 60 | `/scenarios/[slug]` |
| Methodology pages | ~30 | `/methodology/[topic]` |
| Track record pages | 7 indicators × 5 horizons = 35 | `/track-record/[indicator]` |
| Vintage rewinder pages | Q1+ 2024–onward × monthly = 30 | `/vintage/[YYYY-MM-DD]` |
| Long-tail "country × scenario" intersections | ~600 | `/c/[iso3]/s/[slug]` |
| Methodology pop-ups (per chart) | ~50 | `/methodology/[topic]/[detail]` |

Total: ~6,500 pages at v1 launch; ~10,000-15,000 by Y1.

## Page-level SEO discipline (per L107)

Every programmatic page emits:

1. **Canonical URL** with `<link rel="canonical">` — the canonical form is the lowest-friction URL (e.g., `/countries/USA`, not `/c/USA`).
2. **Open Graph + Twitter Card** with auto-generated preview image (server-rendered SVG snapshot).
3. **JSON-LD per page type** (per L107 + L248):
   - Country page → `Dataset` + `Place`
   - Indicator page → `Dataset` + `StatisticalReport`
   - Forecast detail → `Observation`
   - Scenario page → `AnalysisNewsArticle`
   - Methodology page → `TechArticle`
   - Track record page → `Report`
4. **`<meta description>`** auto-generated from the latest figure: "OPENGEM forecasts US GDP at 1.9% for 2027-Q2 (band 0.8–3.0%); see how this compares to WEO 2.2%, OECD EO 2.1%."
5. **Crumb path** with schema.org `BreadcrumbList` for Google rich results.
6. **`<time datetime>`** on every numeric value for freshness signals.
7. **Vintage-aware `<link rel="archive">`** pointing to the prior vintage at `/v/[date]/...`.

## Long-tail keyword strategy

Programmatic SEO works when each page wins a long-tail query that conventional macro publishers don't bother indexing. The OPENGEM target queries:

| Query template | Example | Page that wins |
|---|---|---|
| "[country] gdp forecast 2027" | "germany gdp forecast 2027" | `/countries/DEU` (or its forecast detail page) |
| "[country] recession probability 2026" | "japan recession probability 2026" | `/track-record/recession-probability` filtered to JPN |
| "[indicator] nowcast vs WEO" | "cpi nowcast vs WEO" | `/indicators/cpi_yoy` |
| "[country] yield curve [date]" | "us yield curve march 2026" | `/vintage/2026-03-01/countries/USA` |
| "[scenario] probability" | "EU energy shock probability winter 2026" | `/scenarios/eu-energy-shock-winter-2026` |
| "opengem vs bloomberg" | direct brand searches | `/about` + `/about/methodology` |

Each of these queries has 100–10,000 monthly search volume but is poorly served by closed-source incumbents (who require login).

## Content freshness

The "vintage-stamped + revised-when-truth-prints" pattern is uniquely good for SEO freshness signals. Google rewards pages that update with new information; OPENGEM's accountability discipline causes every miss to update its own page with a post-mortem. That update signal is recognized by search algorithms as content freshness.

## Schema.org + LLM indexing

LLMs increasingly read JSON-LD to ground their answers. By emitting clean `Dataset` + `Observation` schema on every page, OPENGEM becomes a citable source for ChatGPT Search, Perplexity, Claude's web tool, Gemini's grounding, etc. — without explicit MCP integration. The JSON-LD discipline is the SEO equivalent of the MCP server.

## Performance budget per page

- LCP ≤ 1.5s on Slow 4G (the hard target for programmatic SEO ranking)
- TBT ≤ 200ms
- Total JS ≤ 50 KB gzipped per page (server-component-only baseline; interactive islands lazy-loaded)
- Total CSS ≤ 20 KB gzipped (Tailwind + critical inline)

The Cloudflare Pages edge + RSC server-side rendering reaches all of these easily. We do not need a separate static-export step.

## Operational discipline

- **No auto-generated content with weasel-word fillers.** Every programmatic page has at least one fully numeric paragraph derived from real data, not "in 2027, USA's GDP growth is expected to reach..." style.
- **No orphan pages.** Every page is linked from at least one parent listing.
- **No keyword-stuffed page titles.** "USA GDP forecast — OPENGEM" is the format, not "USA GDP forecast 2027 2028 2029 forecast prediction outlook — OPENGEM."
- **Sitemap.xml is dynamic.** Updated on each vintage cycle.
- **robots.txt explicitly allows AI/LLM crawlers** including GPTBot, ClaudeBot, PerplexityBot, Google-Extended, etc. The whole point is to be indexed by them.

## What this loop produced

- The ~6,500-page programmatic SEO matrix at v1
- The per-page SEO discipline (canonical, OG, JSON-LD, meta description, breadcrumbs, time tags)
- The long-tail keyword strategy with example queries per page family
- The performance budget per programmatic page
- The robots.txt + LLM-crawler-friendly stance

## Related

- [[L107-json-ld-schema-org-seo]] — the SEO mechanics deep-dive
- [[L248-json-ld-seo]] (in L239-256 batch) — implementation pointer
- [[L091-observable-framework-explainer-reports]] — the long-tail explainer subdomain
- [[L274-kpi-dashboard-meta]] — programmatic SEO is the leading indicator of long-arc traffic
