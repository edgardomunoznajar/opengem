# L154 — URL Convention

**Loop**: 154 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

**Every view in OPENGEM has a URL. Every URL is human-readable, machine-parseable, and stable.**

A URL is the smallest possible "shared object" we can produce. It's how forecasts get pasted into Substacks, how journalists cite, how LLMs ground their answers. If a view can't be expressed as a URL, it can't be shared, can't be cited, can't be archived.

## URL grammar — formal

```
https://opengem.app/<entity>/<id>[/<sub-entity>/<id>]...
   ?<param>=<value>
   &<param>=<value>
   #<fragment>
```

- Path: hierarchical entity addressing (lowercase, dash-separated).
- Query: filters, dimensions, vintages, share tokens.
- Fragment: drawer state and intra-page anchors.

## Top-level entities

| Path prefix | Resource |
|---|---|
| `/` | Home |
| `/country/<iso3>` | Country page (e.g., `/country/usa`) |
| `/indicator/<id>` | Indicator page (e.g., `/indicator/cpi-yoy`) |
| `/scenario/<id>` | Scenario page |
| `/forecast/<id>` | Forecast page (versioned via vintage param) |
| `/news/<id>` | News item |
| `/event/<id>` | Event detail |
| `/leaderboard` | Forecast leaderboard |
| `/accountability` | Open ledger |
| `/methodology` | Methodology index |
| `/methodology/<id>` | Specific methodology |
| `/compare` | Compare-2 view |
| `/watchlist` | Watchlist |
| `/alerts` | Alerts |
| `/about` | About / governance |
| `/api` | API docs |
| `/mcp` | MCP install page |
| `/pricing` | Pricing |
| `/data` | Datasette mount (raw data) |

All in lowercase. No trailing slashes.

## Identifier conventions

| Resource | ID format | Example |
|---|---|---|
| Country | ISO-3166 alpha-3 lowercase | `usa`, `deu`, `chn` |
| Indicator | slug-of-name | `cpi-yoy`, `gdp-real`, `unemp-u3` |
| Scenario | scenario-pack slug | `2026q3-globe-pack` |
| Forecast | UUID v7 (time-ordered) | `f-01j7k...` |
| News/event | UUID v7 prefixed `n-` / `e-` | `n-01j7k...` |
| Methodology | numbered slug | `dfm-ny-fed-v2`, `combiner-v4` |
| Vintage | ISO date | `2026-06-04` |
| Share token | base32 nanoid (10 chars) | `b7k2m9pq3x` |

UUID v7 is time-ordered: agents can sort URLs chronologically without parsing.

## Query parameters

### Universal

- `?vintage=<YYYY-MM-DD>` — pin to a specific vintage. Default: latest.
- `?asof=<YYYY-MM-DDTHH:MM:SSZ>` — same idea, second resolution. For real-time replay.
- `?lang=<BCP47>` — locale override.
- `?theme=<dark|light>` — theme override.
- `?share=<token>` — share-token (see L155).
- `?embed=1` — render embed-friendly shell (no nav, no footer).

### Page-specific

#### Country page

- `?indicator=<id>` — focus on a specific indicator
- `?horizon=<nowcast|1q|4q|2y|5y>`
- `?bands=<p10p90|p5p95|p25p75|p50only>`
- `?consensus=<weo|oecd|spf|gir|none>`

#### Indicator page

- `?countries=<iso,iso,iso>` — show specific countries
- `?range=<YYYY-MM-DD,YYYY-MM-DD>` — date range
- `?yoy=<1|0>` — toggle Y/Y vs level
- `?log=<1|0>` — toggle log scale

#### Forecast page

- `?model=<id>` — show only one model variant
- `?compare=<vintage1,vintage2>` — diff two vintages
- `?show=<bands,consensus,revisions,actuals>` — toggle layers

#### Compare page

- `?a=<entity-id>&b=<entity-id>` — two objects
- `?dim=<level|yoy|delta>` — comparison dimension

#### Scenario page

- `?probability=<weighted|equal>`
- `?branch=<id>` — drill to one branch of the scenario tree

#### Leaderboard

- `?metric=<crps|mae|logscore|pit>`
- `?horizon=<nowcast|1q|4q>`
- `?indicator=<id>`

### Fragment (hash) — drawer + anchor

- `#drawer=<provenance|methodology|annotation|share|cite|vintage>` — open a drawer
- `#section=<id>` — scroll-anchor to a section
- `#annotation=<id>` — focus an annotation in the layer

## Example URLs

A handful of fully-resolved URLs that should be canonical:

```
https://opengem.app/
https://opengem.app/country/usa
https://opengem.app/country/usa?indicator=cpi-yoy&horizon=4q&vintage=2026-06-04
https://opengem.app/indicator/cpi-yoy?countries=usa,deu,chn,jpn&range=2020-01-01,2026-06-01
https://opengem.app/forecast/f-01j7kabcd?compare=2026-05-21,2026-06-04
https://opengem.app/compare?a=country:deu:cpi-yoy&b=country:fra:cpi-yoy
https://opengem.app/scenario/2026q3-globe-pack?branch=baseline
https://opengem.app/leaderboard?metric=crps&horizon=4q&indicator=cpi-yoy
https://opengem.app/country/usa#drawer=provenance
https://opengem.app/country/usa?vintage=2024-09-15  ← time machine
https://opengem.app/news/n-01j7kxyz?share=b7k2m9pq3x
```

## Parsing rules

1. Path order matters. `/country/usa/indicator/cpi-yoy` is INVALID — we route flat, not nested. Use a query param.
2. Query parameter order does NOT matter. We canonicalize on read for cache keys.
3. Unknown query params are preserved (forward-compat for tracking codes like `utm_*`, `ref=`) and ignored by the renderer.
4. Boolean params: `1` is truthy, `0` is falsy. No `true/false/yes/no`. Discipline.
5. Multi-value params use comma separation, not repeated keys: `countries=usa,deu,chn` (NOT `countries=usa&countries=deu`).
6. Dates always ISO 8601: `YYYY-MM-DD` for vintages, full ISO for asof.

## Canonicalization

On every URL render we run a canonicalize step:
- Sort query params alphabetically.
- Drop default values (`?bands=p10p90` is the default → omit).
- Drop unknown params before generating a canonical share-link.
- Set `<link rel="canonical">` to the canonical form.

This means:

```
input:  /country/USA?theme=dark&vintage=2026-06-04&bands=p10p90&utm=foo
canonical: /country/usa?vintage=2026-06-04
```

The user's tab keeps the original URL (no jarring rewrite), but `<link rel="canonical">` and the "copy permalink" button emit the canonical form.

## Share-token deep links

`?share=<token>` is opaque (random base32). Resolves server-side to a saved view object containing: full path + params + optionally annotation layer + vintage. Used for:

- Compressing very long URLs into something tweet-friendly.
- Bookmarking an annotated view (annotations stored server-side, looked up by token).
- "Cite-this-view" stable IDs (L158).

Tokens are stable; the resolved view object is immutable. Editing creates a new token.

## Versioned URLs vs vintaged URLs

Two concepts that look similar but aren't:

- **Vintage**: data snapshot. `?vintage=2026-06-04` means "show me the data that existed on June 4."
- **Version**: schema or methodology version. Encoded in the methodology ID itself (`methodology/dfm-ny-fed-v2`), not as a query param.

This separation lets us evolve methodology while keeping vintage URLs stable.

## URL stability promise

Once published, a URL is a **promise**:
1. The same URL returns semantically equivalent content forever.
2. If we deprecate an indicator, the URL 301-redirects to its successor.
3. If we rename a country (e.g., Türkiye), the old slug 301-redirects (`/country/tur` aliased).
4. If we kill a feature, the URL serves a tombstone page explaining the removal + a link to the closest substitute.

No 404s for previously-published URLs. Ever. This is the open-archive contract.

## SEO and machine readability

Every page emits:
- `<link rel="canonical">`
- `<link rel="alternate" type="application/json">` pointing to the JSON representation of the view
- `<link rel="alternate" type="text/csv">` for data views
- `<link rel="alternate" type="application/atom+xml">` for feed-bearing pages (see L179)
- `<link rel="alternate" hreflang="...">` for translated versions when L118 lands

The JSON alternate is critical for the MCP server and for LLM ingestion: an agent can hit any URL with `Accept: application/json` and get the structured payload.

## Robots and crawl

- Public: all listed URLs.
- Disallowed: `/_design/*`, `/api/*` (rate-limit-protected), `/data/raw/*` (huge).
- Sitemap: auto-generated daily, indexed by entity type. Submitted to Search Console + Bing.
- `/sitemap.xml` is a sitemap-index pointing to per-entity sitemaps (`sitemap-countries.xml`, etc.).

## Embed URL pattern

`?embed=1` strips the shell, removes the footer, sets a 16:9 aspect chart, and adds a small "via OPENGEM" attribution. For oEmbed (L155), the endpoint is:

```
GET /oembed?url=<encoded-page-url>&maxwidth=600
```

Returns oEmbed JSON pointing to the same page with `?embed=1`.

## Implementation

- Next.js App Router with dynamic segments matching the grammar.
- A `routes.ts` registry exports the canonical patterns; tested by a snapshot test.
- A URL builder utility (`buildUrl({entity, id, ...params})`) is used everywhere — never construct URLs by string concatenation.
- A URL parser utility tested against the example list above.
