---
loop: 123
phase: 3
title: Country Page — Structure and Eight Layout Candidates
date: 2026-06-06
status: decided
---

# L123 — Country Page: Structure + Eight Candidates

**Loop**: 123 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design `/c/{iso3}`. Must include:
1. Header tile (flag, key indicators).
2. Forecast strip.
3. Situation tile (recession probability, GPR).
4. Event feed.
5. Scenarios triggered.
6. Methodology drawer.

Eight candidate layouts. Pick one.

## Candidate A — "Tabbed Drill"

```
+--------------------------------------------------------------------------+
| Header: flag + name + key indicators (1 row)                            |
+--------------------------------------------------------------------------+
| Tabs: Overview | Forecasts | Scenarios | Events | Methodology            |
+--------------------------------------------------------------------------+
| (selected tab content fills below)                                      |
+--------------------------------------------------------------------------+
```

## Candidate B — "Long Scroll, No Tabs"

```
+--------------------------------------------------------------------------+
| Header tile                                                              |
+--------------------------------------------------------------------------+
| Forecast strip (4 charts: GDP, CPI, Unemp, PolicyRate, all P10/P50/P90)|
+--------------------------------------------------------------------------+
| Situation tile (RecProb, GPR, GSCPI exposure)                          |
+--------------------------------------------------------------------------+
| Scenarios triggered (cards)                                            |
+--------------------------------------------------------------------------+
| Event feed (last 30 days)                                              |
+--------------------------------------------------------------------------+
| Methodology drawer (collapsed by default)                              |
+--------------------------------------------------------------------------+
```

## Candidate C — "Two-Column with Sticky Header"

```
+--------------------------------------------------------------------------+
| Sticky header tile                                                       |
+--------------------------------------------------------------------------+
| LEFT (66%)                              | RIGHT (33%)                    |
| Forecast strip                          | Situation tile                 |
| Scenario cards                          | Event feed                     |
| Indicator small-multiples               | Watchlist actions              |
|                                         | Methodology drawer (collapsed) |
+--------------------------------------------------------------------------+
```

## Candidate D — "Tile Wall (Bloomberg-style)"

```
+--------------------------------------------------------------------------+
| Header row                                                               |
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+--+
| GDP| CPI| UE | PR | TB | CA | FX | RT | EQ | OI | GPR| RP | GSCPI |  |
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+--+
| each tile: number, sparkline, delta, click → indicator page             |
+--------------------------------------------------------------------------+
| Scenarios + Events bar at bottom                                        |
+--------------------------------------------------------------------------+
```

## Candidate E — "Vertical Sidebar Nav"

```
+--+-----------------------------------------------------------------------+
|  | Header tile                                                           |
|  +-----------------------------------------------------------------------+
|N | Indicator panel (one chart at a time, big)                           |
|a |                                                                       |
|v | each nav item: Overview / Forecasts / Scenarios / Events / Methodology|
|  +-----------------------------------------------------------------------+
+--+-----------------------------------------------------------------------+
```

## Candidate F — "Hero + Strip + Drilldown"

```
+--------------------------------------------------------------------------+
| Hero tile: flag, name, big stats (GDP, CPI, Unemp, PolicyRate)         |
| 4 forecast minibars (P10/P50/P90 inline)                               |
+--------------------------------------------------------------------------+
| Strip: RecProb · GPR · GSCPI exposure · Surprise · Last revision        |
+--------------------------------------------------------------------------+
| LEFT (60%)                              | RIGHT (40%)                    |
| Forecast detail (chart per indicator,   | Scenarios triggered (top 5)   |
|   tabbed: GDP, CPI, Unemp, PolRate,     | each card: name, P, last fire |
|   ER, equity)                           | ─────────────────────────────  |
|                                         | Event feed (last 14 days)      |
|                                         | dedup'd, geo-tagged            |
+--------------------------------------------------------------------------+
| Methodology drawer (sticky bottom, click to expand)                    |
+--------------------------------------------------------------------------+
```

## Candidate G — "Map-Centered"

```
+--------------------------------------------------------------------------+
| Header tile                                                              |
+--------------------------------------------------------------------------+
| Large country map (with key regions highlighted)                       |
| with GPR pulse, GSCPI port heatmap, etc.                               |
+--------------------------------------------------------------------------+
| Forecast strip below                                                    |
| Scenario cards + event feed below                                       |
+--------------------------------------------------------------------------+
```

## Candidate H — "Card Grid (Notion-style)"

```
+--------------------------------------------------------------------------+
| Header tile                                                              |
+--------------------------------------------------------------------------+
| 3-col card grid, each card is a different section                        |
| [Forecast: GDP] [Forecast: CPI] [Forecast: Unemp]                       |
| [Forecast: PR]  [Situation]      [Scenarios]                            |
| [Event feed (spans 2 cols)]       [Methodology (collapsed)]            |
+--------------------------------------------------------------------------+
```

## The decision — Candidate F

Pick **F (Hero + Strip + Drilldown)** with one modification: the Methodology drawer is a right-edge slide-out, not a bottom drawer. The bottom-sticky-drawer convention competes for vertical space with the forecast detail; an edge slide-out is invisible until invoked.

Final spec:

```
+--------------------------------------------------------------------------+
| OPENGEM  > Countries > United States  ·  /c/USA                          |
+--------------------------------------------------------------------------+
| 🇺🇸 UNITED STATES        Population: 335M  ·  GDP $27.8T  ·  Vintage 2026-06-06
|                                                                          |
| GDP YoY  CPI YoY  Unemp%  PolicyRate                                    |
|  2.4%     2.9%    3.7%    5.25%                                          |
|  ▲0.1     ▼0.2    ▲0.1    flat                                           |
|  P50: 1.9 P50: 2.7 P50: 3.9 P50: 4.75    (1Q ahead, P10/P50/P90 minibar)|
+--------------------------------------------------------------------------+
| STRIP — RecProb 34%▲ · GPR 89▲ · GSCPI exposure 0.18 · Surprise +0.4   |
|         Last forecast revision: 2026-06-02 (4 days ago)                 |
+--------------------------------------------------------------------------+
| FORECAST DETAIL (60%)              |  SITUATION + STREAM (40%)          |
| [Tabs: GDP | CPI | Unemp | PolRate]|                                    |
|                                    |  RECESSION PROBABILITY              |
| ┌─────────────────────────────┐    |  ┌──────────────────────┐         |
| │                            │     |  │ 34% (P50)            │         |
| │   GDP forecast chart        │    |  │ band 18%-52%         │         |
| │   P10/P50/P90 bands         │    |  │ Bauer-Mertens probit │         |
| │   consensus overlay (WEO)   │    |  └──────────────────────┘         |
| │   vintage rewind slider     │    |                                    |
| │                            │     |  SCENARIOS TRIGGERED (4)            |
| └─────────────────────────────┘    |  ┌──────────────────────┐         |
|                                    |  │ Trade-LATAM  P=0.62  │         |
| ANNOTATIONS                        |  │ Red-Sea-#4   P=0.78  │         |
| · 2026-05-28: WEO release         |  │ Oil-shock    P=0.34  │         |
| · 2026-06-02: BEA Q1 advance      |  │ EU-rate-hold P=0.55  │         |
|                                    |  └──────────────────────┘         |
|                                    |                                    |
|                                    |  EVENT FEED (last 14 days)         |
|                                    |  · 06-05: OPEC+ cut                 |
|                                    |  · 06-04: NFP +185k                 |
|                                    |  · 06-03: Yellen Beijing visit     |
|                                    |  · 06-02: BEA Q1 +1.3% (rev)       |
|                                    |  · 06-01: 10y 4.42% (-3bp)          |
|                                    |  [view all 87 events →]            |
+--------------------------------------------------------------------------+
| [Methodology] [Compare] [Watchlist+] [Cite this view] [API] [Embed]    |
+--------------------------------------------------------------------------+
                                                       [Methodology ⓘ] →
```

The right-edge slide-out (invoked via the ⓘ at bottom-right or the M keystroke) reveals:

```
| METHODOLOGY                                          [×]   |
|------------------------------------------------------------|
| Country: United States (USA)                               |
| Last forecast vintage: 2026-06-02                          |
| Last source vintage: 2026-06-05 (BEA Q1 advance)           |
|                                                            |
| Forecast model: L3-BMA over 5 sub-models                   |
|  ─ AR(p) baseline                                          |
|  ─ Bayesian VAR                                            |
|  ─ Dynamic Factor Model                                    |
|  ─ Random Forest                                           |
|  ─ Neural Forecast (Nixtla NHITS)                          |
|                                                            |
| Combiner weights (latest):                                 |
|  AR(p)        0.12                                         |
|  BVAR         0.31                                         |
|  DFM          0.28                                         |
|  RF           0.19                                         |
|  NHITS        0.10                                         |
|                                                            |
| Track record (4-quarter horizon):                          |
|  CRPS:    0.84  (vs WEO 0.91, vs RW 1.42)                  |
|  PIT:     0.78  (pass: yes, ≥0.70 threshold)               |
|  Bias:    -0.04                                            |
|                                                            |
| [Full model card →]  [Backtest data →]  [Replay-and-diff →]|
```

## Why F (and not the others)

**A (Tabs) hides things.** The whole point of a country page is to show forecasts, situation, scenarios, events on the same surface so the user can see causality (e.g., GPR spike → scenarios fired → forecast revised). Tabs separate what should be co-visible.

**B (Long scroll) buries scenarios.** Scenarios triggered is high-value at the top of the visit and is two screens down in B. The user has to scroll past forecasts and situation before seeing what packs fired. That defeats the editorial: "what should I worry about?"

**C (Two-column sticky header) is the close second.** It is essentially the structure of F with a different header treatment. F adds the hero tile with inline minibars (so the user sees forecasts in the header before scrolling) and tabs the forecast detail (so it doesn't sprawl). C scrolls the whole forecast section as a list of charts, which is heavier.

**D (Tile wall) is too dense for a country page.** Tile walls work for the World page (L122) where the user is grazing across many countries. A country page is the destination — depth matters more than density.

**E (Sidebar nav) is a power-user pattern that punishes the casual.** The sidebar makes the page feel like an application; the user needs to learn the navigation. Country pages get linked from Twitter, from emails, from RSS — they need to communicate everything in one viewport without nav-learning cost.

**G (Map-centered) is overweight on one signal.** Most country pages don't need a big map — the GPR pulse and GSCPI tile are spot-readings, not geographic explorations. A map for the United States adds little; a map for a small country with regional conflict (e.g., Yemen) might add value, but the page template should not pay that cost universally.

**H (Card grid) is Notion's pattern and it leaks the same problem as E (Quad) in L122 — symmetric equally-sized cards encode "no editorial decision." On a country page, forecasts matter more than events. F gives forecasts 60% and events 40% to encode that.

**F wins** because it encodes the editorial hierarchy: hero tile → strip → forecast detail (primary) + situation/scenarios/events rail (secondary) → methodology (on demand). It reads top-down in 5 seconds for the casual visitor and supports 20 minutes of drilldown for the analyst.

## The header tile

The header is more than a label. It is a 6-second readout of "where this country is." Four big stats (GDP YoY, CPI YoY, Unemployment, Policy Rate) with current values, daily delta, and a P10/P50/P90 minibar for the 1Q-ahead forecast. The minibar is the move that distinguishes OPENGEM from every other country page on the internet — the forecast is *in the header*, not buried.

The flag emoji is intentional. ISO 3166 country emoji render correctly in 99% of browsers and convey identity faster than a flag image (which is a separate HTTP request). The downside is that some locale-edge cases (Kosovo, Taiwan) need text fallbacks; the template handles that.

## The situation tile

Recession probability gets pride of place (top of the right rail) because it is the single most-asked question of macro forecasters by lay audiences. Below it: GPR with sparkline, GSCPI exposure (how much this country's economy is exposed to global supply chain pressure), and Surprise index (current month).

## The forecast strip

The forecast strip is the same instrument across every country page. It always shows the same six indicators (RecProb, GPR, GSCPI exposure, Surprise, Last revision date, Vintage). This consistency is the brand promise: every country page reads the same way.

## The methodology drawer

The drawer is mandatory (L132 is the design loop for the drawer in detail). On a country page, the drawer is keyed to the forecast model currently in view (whichever indicator tab is active). Click the indicator tab and the drawer's "Forecast model" section updates accordingly. The drawer is reachable via M keystroke (per L152 keyboard shortcuts).

## What this loop produced

- Eight candidate country-page layouts as ASCII wireframes.
- Decision: Candidate F (Hero + Strip + Drilldown) with a right-edge slide-out methodology drawer instead of bottom-sticky.
- The header is forecast-aware (P10/P50/P90 minibars inline).
- The 60/40 forecast/situation split is intentional editorial weighting.
- Methodology drawer keyed to active indicator tab.

## What comes next

- **L124** designs the Indicator page (the cross-country view of the same indicator).
- **L125** designs the Scenario page (drill into a scenario card from the right rail).
- **L126** designs the Forecast page (drill into the forecast chart in the center).
- **L132** designs the methodology drawer in detail.
- **L161** designs the country card grid (the World-page tile that drills here).

## Related

- [[L121-information-architecture]] — /c/{iso3} URL space
- [[L122-home-screen]] — country tiles on the World page drill here
- [[L126-forecast-page]] — clicking the forecast chart opens the deep forecast view
- [[L132-provenance-drawer]] — methodology slide-out details
- [[L143-print-tearsheet]] — one-page PDF derives from this layout
