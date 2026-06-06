---
loop: 127
phase: 3
title: Event / News Stream Page — Layout Decision
date: 2026-06-06
status: decided
---

# L127 — Event / News Stream Page

**Loop**: 127 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design `/events`. Must support:
1. GDELT-driven items (the primary feed).
2. Deduplication (one logical event, many headlines).
3. Geo-tagging (every item has a country / region).
4. Link-out to source (we are not the news brand).
5. "What this affects" tags (which scenarios, which indicators, which countries this event touches).

Pick a layout. Candidates below.

## Why this page exists

OPENGEM is not a news site. We do not produce reporting and we do not paraphrase headlines. But events drive forecast revisions and scenario triggers. The event stream is the page that connects "something happened in the world" to "the forecast moved" — the causality rail. The user comes here to ask: "what happened that caused today's recession-probability bump?"

The page is also a natural landing point for SEO and RSS. We publish the stream as a feed; we publish dedup'd events as canonical IDs; we let the LLM and the user paste the link into their own analysis.

## Candidates

### A — "Twitter-style infinite scroll"

```
+--------------------------------------------------------------------------+
| Header + filters (region, indicator-affected, severity)                 |
+--------------------------------------------------------------------------+
| ● 06:14 UTC  OPEC+ surprise cut announced                                |
|              affects: oil, energy, EZ-CPI, US-CPI · scenarios: Oil-shock|
|              sources: Reuters, Bloomberg, FT  →                          |
+--------------------------------------------------------------------------+
| ● 06:09 UTC  US CPI release scheduled tomorrow 14:30 ET                  |
|              affects: CPI · scenarios: (none)                            |
|              sources: BLS                                                |
+--------------------------------------------------------------------------+
| ...                                                                      |
+--------------------------------------------------------------------------+
```

### B — "Compact table"

```
+--------------------------------------------------------------------------+
| Time | Country | Event                  | Affects        | Sources       |
+--------------------------------------------------------------------------+
| 06:14 | GLOBAL  | OPEC+ surprise cut    | oil, EZ/US CPI | Reut, Bbg, FT |
| 06:09 | USA     | US CPI release tmrw   | CPI            | BLS           |
| ...                                                                      |
+--------------------------------------------------------------------------+
```

### C — "Card grid"

```
+--------------------------------------------------------------------------+
| 2-column card grid                                                       |
| each card: severity badge, headline, dek, country tag, scenario tags,   |
|            sources, timestamp, link                                     |
+--------------------------------------------------------------------------+
```

### D — "Timeline ribbon + detail"

```
+--------------------------------------------------------------------------+
| Top: horizontal time ribbon (last 7 days, severity-coded dots)         |
+--------------------------------------------------------------------------+
| Below: selected event detail card                                       |
+--------------------------------------------------------------------------+
| Below: ranked list of events with same affects                          |
+--------------------------------------------------------------------------+
```

### E — "Stream + Map"

```
+--------------------------------------------------------------------------+
| LEFT (60%)                              | RIGHT (40%)                    |
| Twitter-style stream                    | World map: dots at event       |
| filters above                           | locations, sized by severity   |
|                                          |                                |
|                                          | Click dot → highlight stream  |
|                                          | item                          |
+--------------------------------------------------------------------------+
```

### F — "Grouped by causal cluster"

```
+--------------------------------------------------------------------------+
| Group 1: Oil supply (3 events today)                                    |
|   ● OPEC+ surprise cut                                                   |
|   ● Saudi production statement                                           |
|   ● Brent spot +3.2% intraday                                            |
+--------------------------------------------------------------------------+
| Group 2: US data releases (2 events today)                              |
|   ● US CPI tomorrow                                                      |
|   ● BEA Q1 revision                                                      |
+--------------------------------------------------------------------------+
```

## The decision — Candidate E (Stream + Map)

Pick **E (Stream + Map)** with the stream as the primary surface and the map as a navigation aid, not the focal point.

Final spec:

```
+--------------------------------------------------------------------------+
| OPENGEM > Events  ·  /events                                             |
| Last 24h: 47 events  ·  4 scenarios fired  ·  RSS / Atom available       |
+--------------------------------------------------------------------------+
| FILTERS                                                                  |
| [Region: all ▼] [Country: all ▼] [Severity: all ▼] [Indicator: all ▼]   |
| [Scenario tag: all ▼] [Source: GDELT + ENRICHED ▼] [Sort: time ▼]       |
| [Search query ___________]                                                |
+--------------------------------------------------------------------------+
| LEFT (60%)                              | RIGHT (40%)                    |
|                                          |                                |
| EVENT STREAM                             | EVENT MAP                       |
|                                          |                                |
| ┌─ 06:14 UTC ──── 🔥 high ──────────┐  |  ┌────────────────────────┐    |
| │ OPEC+ surprise cut announced     │  |  │   [world map]           │    |
| │ Group: 4 headlines (dedup'd)     │  |  │   dots at event coords  │    |
| │ ─ Reuters, Bloomberg, FT, AP     │  |  │   sized by severity      │    |
| │ affects: Oil, EZ-CPI, US-CPI     │  |  │   colored by scenario   │    |
| │ scenario: Oil-shock fired P=0.34 │  |  │                          │    |
| │ countries: SAU, RUS, USA, EZ     │  |  │                          │    |
| │ [view scenario] [open sources →] │  |  │                          │    |
| └──────────────────────────────────┘  |  │                          │    |
|                                          |  └────────────────────────┘    |
| ┌─ 06:09 UTC ──── ⚪ info ─────────┐  |                                  |
| │ US CPI release tomorrow 14:30 ET │  | UPCOMING (next 7d)              |
| │ affects: CPI · scenarios: (none) │  |                                  |
| │ source: BLS · CALENDAR EVENT    │  | 06-07  US CPI release            |
| └──────────────────────────────────┘  | 06-09  ECB rate decision         |
|                                          | 06-11  PBoC LPR fixing            |
| ┌─ 05:58 UTC ──── 🟡 medium ───────┐  | 06-12  WTO Forum opens            |
| │ PBoC LPR cut by 5bp              │  | 06-13  BLS payrolls               |
| │ Group: 2 headlines                │  |                                  |
| │ affects: CN-CPI, CN-PR, EM-FX    │  | INDICATOR-IMPACT INDEX           |
| │ scenarios: (none)                  │  |                                  |
| │ source: PBoC + WSJ + Reuters      │  | Top affected today:               |
| └──────────────────────────────────┘  |   1. Oil       12 events         |
|                                          |   2. EZ-CPI    8 events           |
| [load more...]                           |   3. US-CPI    7 events           |
|                                          |   4. EM-FX     5 events           |
|                                          |   5. CN-PR     4 events           |
+--------------------------------------------------------------------------+
| RSS / Atom / JSON feeds:                                                |
|  /events.rss  ·  /events.atom  ·  /events.json (last 24h)               |
|  Filtered: /events.rss?country=USA&severity=high                        |
+--------------------------------------------------------------------------+
```

## Why E (and not the others)

**A (Twitter scroll) is the close runner-up.** A clean reverse-chronological stream with rich item cards is what the reader wants. The reason E beats A is the map: when 47 events fire in a day, the map gives the reader spatial structure ("most of these are in LATAM today") that the stream alone hides.

**B (compact table)** is the right view for the analyst who is doing forensic work ("show me all CPI-affecting events in the last 7 days"). It stays as a *view-mode toggle* (the user can switch to table mode), not the default.

**C (card grid)** wastes vertical space (two columns of cards = half the items per fold). Stream-as-list is denser.

**D (timeline ribbon)** is interesting but it linearizes what should be browse-able. The ribbon's main benefit is "see all events of the last 7 days at once," but a 7-day timeline with 300 dots becomes a smear. Better to use the small "Upcoming" panel on the right (showing the next 7 days, calendar-style) than a full timeline ribbon.

**F (grouped by causal cluster)** is what the deduplication output should look like *within* each item card (one item = many headlines, grouped under one logical event). It is not the right top-level structure — the reader wants reverse-chronological by default and can re-sort to causal cluster if they want it.

## Deduplication

Deduplication is GDELT-native plus an OPENGEM-specific logical event ID. The GDELT GKG provides cluster IDs for related coverage; OPENGEM adds an extra layer of logical event resolution using:

1. **Temporal proximity**: events within a 4-hour window with overlapping entity tags are candidates for merge.
2. **Entity overlap**: 60%+ overlap on extracted entities (orgs, persons, countries, commodities) → merge.
3. **Semantic similarity**: cosine similarity on event embedding ≥ 0.85 → merge.
4. **Manual override**: editor can promote two events that overlap entity but represent distinct phenomena.

The dedup'd event has a canonical OPENGEM event ID (`evt_2026-06-06_opec-cut`) and a list of source headlines. The card displays the count ("Group: 4 headlines") and lists source publications.

## Geo-tagging

Every event has one or more country tags. GDELT provides geographic location codes; OPENGEM normalizes to ISO 3166-1 alpha-3. For events that affect multiple countries (e.g., "OPEC+ cut affects USA, EZ, China"), the tag list is union of GDELT-detected + scenario-pack-derived.

Geo-tags are clickable: clicking a country chip filters the stream to only events tagged that country.

## "What this affects" tags

Each event card shows three things below the headline:
- **Affects** (indicators): `oil, EZ-CPI, US-CPI` — clickable; opens the indicator page filtered to this event in the annotations.
- **Scenarios** (packs touched): `Oil-shock fired P=0.34` — clickable; opens the scenario page.
- **Countries**: `SAU, RUS, USA, EZ` — clickable; opens country page.

This is the causality rail. The user can trace from event → indicator → forecast → scenario without leaving the dashboard semantics.

## Severity rating

Each event has a severity badge:
- **🔥 high** — triggered a scenario pack and/or caused a measurable forecast revision (>0.1pp on any 4Q forecast).
- **🟡 medium** — relevant to scheduled data release or central-bank action but not yet a forecast mover.
- **⚪ info** — calendar event, scheduled release, advisory.

Severity is computed automatically from the impact analysis (which packs fired, which forecasts shifted) and editor-overridable.

## Source linking

The card never paraphrases. Each source is a hyperlink to the original publisher. OPENGEM is the index, not the content. This is the legal-safety play (no copyright drama) and the editorial play ("we are not the news").

When a source link is dead (publisher takedown, paywall, geo-block), OPENGEM shows the archived snapshot URL via the Wayback Machine API. Always.

## RSS / Atom / JSON

The stream is published as RSS, Atom, and JSON. Filtered feeds via query string (e.g., `/events.rss?country=USA`). This is the distribution play: the YouTuber subscribes by country, the journalist subscribes by indicator, the LP subscribes by scenario.

JSON-LD on every event card so search engines and LLMs ingest the causal links.

## The right rail

The right rail has three sections below the map:
1. **Upcoming (next 7d)**: calendar of scheduled releases and known events. Five items max.
2. **Indicator-impact index**: which indicators received the most event-impact today. Five rows max.
3. (Scrolling further) **Recent forecast revisions**: list of forecasts that moved today, linked.

## What this loop produced

- Six candidate event-stream layouts as ASCII wireframes.
- Decision: Candidate E (Stream + Map) with stream as primary, map as nav aid.
- Deduplication rules: GDELT cluster + 4h window + 60% entity overlap + ≥0.85 embedding sim + manual override.
- Geo-tagging normalized to ISO 3166-1 alpha-3.
- "What this affects" tags: indicators / scenarios / countries (all clickable).
- Severity scoring: high (scenario fired) / medium (data release) / info (calendar).
- No paraphrase; source linking only; Wayback fallback for dead links.
- RSS / Atom / JSON feeds with query-string filters.

## What comes next

- **L170** designs the top-of-mind feed ranking (the algorithm behind "top events today").
- **L179** designs the RSS / Atom feed catalog in detail.
- **L227** designs the election calendar + political risk page.
- **L229** designs the sentiment / news tone page (GDELT GKG features).
- **L241** prototypes the live news feed in code.

## Related

- [[L121-information-architecture]] — /events URL space
- [[L122-home-screen]] — World page right column is a preview of this feed
- [[L123-country-page]] — country page right rail is a country-filtered version of this
- [[L125-scenario-page]] — events trigger scenarios; this page is the causality rail
- [[L170-top-of-mind-feed]] — ranking algorithm
- [[L179-rss-atom-catalog]] — feed catalog
