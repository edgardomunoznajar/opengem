---
loop: 125
phase: 3
title: Scenario Page — Structure and Eight Layout Candidates
date: 2026-06-06
status: decided
---

# L125 — Scenario Page: Structure + Eight Candidates

**Loop**: 125 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design `/s/{pack-id}`. Must support:
1. Trigger conditions (what fires this pack).
2. Affected countries map.
3. Narrative block (3-paragraph contextual prose, model-grounded).
4. Probability rollup (per-country + global synthesis).
5. Related scenarios (this-and-that, this-vs-that).

Eight candidate layouts. Pick one.

The Scenario page is where OPENGEM's "scenario pack" concept becomes visible to the public. The existing `opengem-scenarios` package already encodes scenario packs as data; this page is the human-readable surface. It is the page a journalist will link to in a story. It is the page an LP will paste into an investment memo.

## Candidate A — "Vertical narrative scroll"

```
+--------------------------------------------------------------------------+
| Header: pack name, status (fired today / armed / dormant)               |
+--------------------------------------------------------------------------+
| Trigger conditions block                                                |
| Narrative block (3 paragraphs)                                          |
| Affected countries list                                                |
| Probability rollup                                                     |
| Related scenarios                                                     |
+--------------------------------------------------------------------------+
```

Pure linear reading.

## Candidate B — "Map-first"

```
+--------------------------------------------------------------------------+
| Header                                                                   |
+--------------------------------------------------------------------------+
| Big world map: countries colored by affected/not, opacity = probability |
+--------------------------------------------------------------------------+
| Below: narrative, triggers, probability, related, methodology          |
+--------------------------------------------------------------------------+
```

## Candidate C — "Three-column briefing"

```
+--------------------------------------------------------------------------+
| Header                                                                   |
+--------------------------------------------------------------------------+
| Trigger          | Narrative              | Affected countries          |
| spec              | 3-para markdown       | list with per-country P     |
|                   |                        |                              |
| Probability       | Related scenarios      | Methodology link            |
| rollup            | (this-and-that)        |                              |
+--------------------------------------------------------------------------+
```

## Candidate D — "Tabbed pack"

```
+--------------------------------------------------------------------------+
| Header                                                                   |
| Tabs: Overview | Trigger | Affected | Methodology | History              |
+--------------------------------------------------------------------------+
| Tab content fills below                                                |
+--------------------------------------------------------------------------+
```

## Candidate E — "Hero + map + drilldown"

```
+--------------------------------------------------------------------------+
| Hero block: pack name, status, global P, last fire timestamp           |
| Narrative block (3 paragraphs auto-generated from pack JSON)           |
+--------------------------------------------------------------------------+
| LEFT (60%)                              | RIGHT (40%)                    |
| Affected countries map                  | Probability rollup            |
| (regional view, click to drilldown)     | per-country bar chart          |
|                                         |                               |
| Below map: trigger conditions detail    | Related scenarios cards      |
|                                         |                               |
|                                         | Methodology link              |
+--------------------------------------------------------------------------+
```

## Candidate F — "Timeline + state"

```
+--------------------------------------------------------------------------+
| Header                                                                   |
+--------------------------------------------------------------------------+
| Timeline: this pack's fire history across all countries × time          |
| each cell = (country, date) → fired/armed/dormant + probability         |
+--------------------------------------------------------------------------+
| Below: trigger, narrative, affected, related, methodology              |
+--------------------------------------------------------------------------+
```

## Candidate G — "Card stack"

```
+--------------------------------------------------------------------------+
| Header                                                                   |
+--------------------------------------------------------------------------+
| Card 1: What this pack is (narrative)                                  |
| Card 2: When it fires (trigger)                                         |
| Card 3: Where it bites (countries + map)                               |
| Card 4: How likely (probability + methodology)                         |
| Card 5: What else to watch (related scenarios)                         |
+--------------------------------------------------------------------------+
```

## Candidate H — "Two-row hero"

```
+--------------------------------------------------------------------------+
| Hero row 1: name + status + global P + last fire                       |
+--------------------------------------------------------------------------+
| Hero row 2: 3-paragraph narrative                                       |
+--------------------------------------------------------------------------+
| Wider canvas below: split panes (map, rollup, triggers, related)       |
+--------------------------------------------------------------------------+
```

## The decision — Candidate E

Pick **E (Hero + Map + Drilldown)** with one refinement: the narrative block goes *above* the hero status line (LLM-generated 3 paragraphs are the lede), not below.

Final spec:

```
+--------------------------------------------------------------------------+
| OPENGEM > Scenarios > Trade-LATAM · /s/trade-latam                       |
+--------------------------------------------------------------------------+
|                                                                          |
| TRADE-LATAM                                                              |
| Status: FIRED today  ·  Global P: 0.62  ·  Affects: 12 countries        |
| Last fire: 2026-06-06 05:30 UTC  ·  Fire count YTD: 3                    |
|                                                                          |
+--------------------------------------------------------------------------+
| NARRATIVE  (auto-generated from pack JSON via opengem-narrative)        |
|                                                                          |
| Trade-LATAM fires when (1) a major LATAM trading partner imposes        |
| tariffs above 15% on US exports, OR (2) a LATAM central bank moves      |
| rates by more than 100bp in a single meeting outside its forward        |
| guidance band. As of 2026-06-06, Brazil announced a 22% retaliatory     |
| tariff on US soy, triggering condition (1). The probability rollup      |
| reflects elevated risk to Mexico, Brazil, Chile, and Colombia.          |
|                                                                          |
| Forecast effects: 4Q-ahead GDP forecasts for BRA -0.4pp, MEX -0.2pp,    |
| CHL -0.1pp, COL -0.1pp vs the pre-fire vintage. CPI forecasts for       |
| BRA +0.3pp, MEX +0.1pp at 4Q horizon. Affected indicators include      |
| FX, equity, sovereign CDS, and trade-balance composition.               |
|                                                                          |
| Track record: this pack has fired 12 times historically (2019–2026).   |
| Median 4Q-ahead realized GDP impact on BRA was -0.5pp (IQR -0.2 to     |
| -0.8). For the full track record see [methodology →].                  |
+--------------------------------------------------------------------------+
| LEFT (60%)                              | RIGHT (40%)                    |
|                                          |                                |
| AFFECTED COUNTRIES MAP                   | PROBABILITY ROLLUP             |
|                                          |                                |
|  [LATAM regional map]                    | Country    P    affected horiz |
|  countries shaded by P (heatmap)         | BRA       0.72  1Q, 4Q, 2Y     |
|  click country → /c/{iso3}               | MEX       0.65  1Q, 4Q         |
|                                          | CHL       0.41  4Q              |
|                                          | COL       0.38  4Q              |
|                                          | PER       0.24  4Q              |
|                                          | URY       0.18  4Q              |
|                                          | ARG       0.16  1Q              |
|                                          |                                |
| TRIGGER CONDITIONS                       | RELATED SCENARIOS               |
|                                          |                                |
| Condition (1) OR (2):                    | Trade-CN-US     P=0.45         |
| (1) LATAM tariff > 15% on US exports     | Oil-shock-LATAM P=0.28         |
|     SOURCE: WTO + national gazettes      | EM-FX-crisis    P=0.32         |
| (2) LATAM CB rate move >100bp out-of-band| Dollar-rally    P=0.31          |
|     SOURCE: BIS CBPOL + central bank     |                                |
|     press releases                       | "If this fires, also watch:"   |
|                                          | Sovereign-CDS-LATAM, Equity-    |
| Last 5 fires:                            | LATAM, Commodity-soy           |
|  2026-06-06  cond (1)  BRA 22% tariff   |                                |
|  2025-11-12  cond (2)  ARG 200bp hike   |                                |
|  2025-03-04  cond (1)  MEX 17% tariff   |                                |
|  2024-09-22  cond (2)  BRA 150bp cut    |                                |
|  2024-02-11  cond (1)  COL 18% tariff   |                                |
+--------------------------------------------------------------------------+
| [Full methodology →] [Pack JSON] [API] [Subscribe to alerts] [Cite]    |
+--------------------------------------------------------------------------+
```

## Why E (and not the others)

**A (linear scroll)** is the right shape for the methodology page (L135), not the scenario page. The scenario page is a multi-attribute object: location (map), severity (probability), causality (trigger), narrative, related. A single column linearizes what should be co-visible.

**B (map-first)** is a quarter-right idea. A big map is honest about "where this bites" but expensive on first impression. The map should be a key panel, not the whole page. E gives the map 60% of the second-row width — large enough to read, small enough to leave room for the probability rollup beside it.

**C (three-column briefing)** is a tighter version of E but suffers from C's general problem (see L122): three equal columns encode no editorial. E's two-column split (map 60%, rollup + triggers + related 40%) makes the editorial weighting explicit.

**D (tabs)** hides the most important reading — the narrative — behind a tab. The user has to click to find the lede. Wrong.

**F (timeline)** is interesting and reserved for the historical view inside the methodology drawer (a tab named "History"). It is the wrong default surface because most visitors don't want historical fire patterns; they want to know "what is this pack and is it firing now."

**G (card stack)** is the Notion/Linear pattern and is the wrong fit. Equal-sized cards encode equality of importance; the narrative is more important than "related scenarios." E breaks the cards down by importance and assigns them screen real estate accordingly.

**H (two-row hero) is a close cousin** of E, but having the narrative as Row 2 inside the hero competes for hero real estate with the status line. E hoists the narrative *above* the status line so the hero block reads: name → narrative → status. That order matches how a reader reads.

## The narrative block

The narrative is auto-generated from pack JSON via the existing `opengem-narrative` package's ChatGPT system prompt — but rendered server-side and cached, not via live API calls. Each pack vintage gets one canonical narrative, stored alongside the pack data. The narrative is grounded entirely in numbers from the pack (probability rollup, trigger source, track record); the LLM does prose-style generation, not analysis.

The narrative is editorial. The first paragraph names the trigger and the firing condition. The second paragraph quantifies the forecast effects. The third paragraph cites the track record. Three paragraphs is the format because that is what fits in a Substack quote, a tweet thread, or a YouTube b-roll.

## The probability rollup

The rollup is a per-country list, sorted by P descending. Each row: country code, P, affected horizons (1Q, 4Q, 2Y, 5Y), and a small affected-indicator chip set on click. The rollup is the "where to look" surface.

The global P (in the hero) is the BMA-weighted aggregation of per-country Ps, weighted by GDP-PPP. The methodology link explains the weighting choice.

## The affected countries map

Default is the smallest regional view that contains all affected countries. For Trade-LATAM the regional view is South + Central America. For Oil-shock it might be the whole world. The map uses a sequential color scale (white → orange for the terminal theme) keyed to P. Click a country to drill into /c/{iso3} for that country.

## Trigger conditions

Trigger conditions are presented as a logical expression (e.g., "Condition (1) OR (2)") plus the source attribution for each condition. The last 5 historical fires are listed below — date, which condition fired, the precipitating event. This is the trust-builder: anyone can verify the pack does what it claims to do.

## Related scenarios

Related scenarios are computed from co-occurrence in the historical fire log. Two packs that fire within 14 days of each other ≥30% of the time are "related." This is data-driven, not editorial.

The "If this fires, also watch:" line is a short list of indicators that historically move with this pack (e.g., sovereign CDS, equity, commodity). It links to those indicator pages with the relevant country filter already applied.

## The methodology link

The methodology link opens the methodology page (`/s/{pack-id}/methodology`, designed in L135) — separate from the scenario page itself. Methodology includes the full V&V evidence, the model link, the historical AUC/calibration scores, and the assumption list.

## What this loop produced

- Eight candidate scenario-page layouts as ASCII wireframes.
- Decision: Candidate E (Hero + Map + Drilldown) with narrative-above-status hoist.
- The narrative block is auto-generated via opengem-narrative and cached per vintage.
- Probability rollup is per-country, GDP-PPP-weighted global aggregate.
- Map defaults to the smallest regional view containing all affected countries.
- Related scenarios computed from historical co-occurrence.
- Methodology link opens the full methodology page (L135 design).

## What comes next

- **L126** designs the Forecast page (drilldown from a probability row).
- **L132** designs the methodology drawer.
- **L135** designs the methodology page per pack.
- **L160** designs the scenario probability rollup visual.
- **L196** designs scenario trigger evaluation in code.

## Related

- [[L121-information-architecture]] — /s/{pack-id} URL space
- [[L122-home-screen]] — scenario cards on home page drill here
- [[L123-country-page]] — country page shows scenarios triggered for that country
- [[L132-provenance-drawer]] — methodology drawer
- [[L135-methodology-page]] — full pack methodology + V&V
