---
loop: 122
phase: 3
title: Home Screen — World Page Layout
date: 2026-06-06
status: decided
---

# L122 — Home Screen: Seven Layout Candidates, One Decision

**Loop**: 122 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design the World page (`/`). It must give a "world economy at a glance" in ten seconds. A visitor who arrives cold, with no context, should leave the fold knowing: which countries are in trouble, which scenarios fired today, what the consensus recession probability is, and where to click next. Seven candidate layouts. Pick one. Argue.

## Candidate A — "Bloomberg Tile Wall"

```
+--------------------------------------------------------------------------+
| OPENGEM    World  Countries  Indicators  Scenarios  Forecasts  Ledger    |
+--------------------------------------------------------------------------+
| Today 2026-06-06 · 4 packs fired · GPR 132 · WGCPI +0.18 · CrCs 5.40    |
+----------------+----------------+----------------+----------------+------+
| US Recession  | EZ Recession   | UK Recession   | JP Recession   | CN.. |
|   34%  +2pp   |   41%  +1pp    |   28%  -1pp    |   12%  flat    |  19% |
| ┄┄┄┄┄┄ band   | ┄┄┄┄┄┄ band    | ┄┄┄┄┄┄ band    | ┄┄┄┄┄┄ band   | band |
+----------------+----------------+----------------+----------------+------+
| US CPI 4Q     | EZ CPI 4Q      | UK CPI 4Q      | JP CPI 4Q      | etc. |
+----------------+----------------+----------------+----------------+------+
| 30 tiles total · 6 rows × 5 cols · scroll for "next 30"                  |
+--------------------------------------------------------------------------+
```

A wall of micro-tiles. High density, no editorial.

## Candidate B — "Editorial Front Page (FT-style)"

```
+--------------------------------------------------------------------------+
|  THE WORLD TODAY · 2026-06-06                                            |
+--------------------------------------------------------------------------+
|                                                                          |
|   [HERO 700x300]  GPR globe pulse — 4 countries pulsing red              |
|                                                                          |
|   LEAD STORY: "Trade-shock pack fires across LATAM"                      |
|   Three sentence dek. P=0.62. Affected: BRA MEX CHL COL.                |
|                                                                          |
+--------------------------------------------------------------------------+
|  Recession watch (5 countries)  |  CPI overshoot (3 countries)            |
|  ┄┄┄┄ sparklines                |  ┄┄┄┄ sparklines                       |
+--------------------------------------------------------------------------+
|  Today's event stream (8 items, GDELT-driven, dedup'd)                  |
+--------------------------------------------------------------------------+
```

Looks like a newspaper. Slow, narrative-led.

## Candidate C — "Three-Column Briefing"

```
+--------------------------------------------------------------------------+
| Left column            | Center column         | Right column            |
| SITUATION              | FORECASTS              | EVENTS                  |
|                        |                       |                         |
| World GPR 132 ▲        | Recession-Watch       | • OPEC+ surprise cut    |
| Recession idx 32% ▲    |   USA 34% EZ 41%      | • US CPI release tmrw   |
| Inflation idx 4.1% ▼   |   UK 28% JP 12%       | • PBoC LPR -5bp         |
| GSCPI 0.32 ▲           | CPI 4Q                | • Red Sea attack #4     |
| Pulse → globe          |   USA 2.9 EZ 2.4      | • Argentina IMF talks   |
|                        | GDP 1Q nowcast        |                         |
| Scenarios fired today  |   USA +0.6 EZ +0.1    | Scenarios fired (4)     |
|  • Trade-LATAM (.62)   |                       | View all events →       |
|  • Oil-shock (.34)     |                       |                         |
|  • Red-Sea (.78)       |                       |                         |
|  • EU-rate-hold (.55)  |                       |                         |
+--------------------------------------------------------------------------+
```

Three columns; each is a story. Density is medium.

## Candidate D — "Globe-first"

```
+--------------------------------------------------------------------------+
|                                                                          |
|                                                                          |
|                  [ 3D GPR globe takes full width × 60% height ]          |
|                  countries pulse by current GPR level                    |
|                  click country → goes to /c/{iso3}                       |
|                                                                          |
|                                                                          |
+--------------------------------------------------------------------------+
| Below the fold: country tiles, event stream, scenario list               |
+--------------------------------------------------------------------------+
```

Beautiful. Slow to load. Mobile-hostile.

## Candidate E — "Quad Quadrant"

```
+--------------------------------+-----------------------------------------+
| RECESSION WATCH                | INFLATION WATCH                         |
| ┄ small multiples: 12 countries| ┄ small multiples: 12 countries        |
|   stacked sparklines           |   stacked sparklines                   |
+--------------------------------+-----------------------------------------+
| SCENARIO BOARD                 | EVENT STREAM                            |
| 4 packs fired today            | 12 events, GDELT-ranked                |
| top 10 in priority order       | dedup'd, geo-tagged                     |
+--------------------------------+-----------------------------------------+
```

Symmetric, scannable. Boring.

## Candidate F — "Headline + Strip + Stream"

```
+--------------------------------------------------------------------------+
|  HEADLINE TILE (1 across, 25% height)                                   |
|  "Three packs fired overnight; recession risk rising in EZ + UK"       |
|  [click to expand → dek + chart]                                         |
+--------------------------------------------------------------------------+
|  STRIP: 6 numbers across (50% height)                                  |
|  GPR | RecProb | CPI | GSCPI | EquityVol | OilPx | each with sparkline |
+--------------------------------------------------------------------------+
|  TWO COLUMNS (50% height)                                              |
|  Left: country tiles (G7 + ~5 more) compact                            |
|  Right: event stream (GDELT, ranked, dedup'd)                          |
+--------------------------------------------------------------------------+
```

Layered hierarchy. Reads top-to-bottom in five seconds.

## Candidate G — "Terminal Console"

```
> opengem world today
Loaded 2026-06-06 06:00 UTC · 4 packs fired

Situation
  GPR........... 132  (+8 d/d, +24 w/w)
  RecessionIdx.. 32%  (+1pp d/d)
  GSCPI......... 0.32 (+0.04 d/d)

Today's packs
  [1] Trade-LATAM   P=0.62  affects BRA MEX CHL COL
  [2] Oil-shock     P=0.34  affects USA EZ IND
  [3] Red-Sea-#4    P=0.78  affects EZ EGY ISR
  [4] EU-rate-hold  P=0.55  affects EUR-area

Events (top 12)
  06:14  OPEC+ surprise cut announced
  06:09  US CPI release scheduled tomorrow 14:30 ET
  05:58  PBoC LPR cut by 5bp
  ...
> _
```

REPL aesthetic. Pure terminal. Hostile to newcomers.

## The decision — Candidate F, modified

Pick **F (Headline + Strip + Stream)** as the World page. Rationale below.

```
+--------------------------------------------------------------------------+
| OPENGEM    World  Countries  Indicators  Scenarios  Forecasts  Ledger    |
+--------------------------------------------------------------------------+
| 2026-06-06 06:00 UTC · next refresh 08:00 · 4 packs fired · changelog → |
+--------------------------------------------------------------------------+
| HEADLINE                                                                |
| "Trade-LATAM and Red-Sea packs fired; EZ recession risk +3pp"          |
| 2-sentence dek (auto-generated from top-priority scenario rollup)      |
| [thumbnail chart] [view scenario] [view methodology]                   |
+--------------------------------------------------------------------------+
| STRIP — six headline numbers, each tappable, each with 30d sparkline    |
| GPR 132▲ | RecProb 32%▲ | CPI 4.1%▼ | GSCPI 0.32▲ | VIX 17▼ | Oil 84▲ |
| ┄ each: number, dod%, color-coded ▲/▼, sparkline, link to /i/{slug}    |
+--------------------------------------------------------------------------+
| LEFT (60%)                              | RIGHT (40%)                    |
| COUNTRY BOARD                           | TODAY'S STREAM                 |
| G7 row (7 micro-tiles)                  | All packs fired today          |
| BRICS+ row (5 micro-tiles)              | + event stream (15 items)       |
| Watchlist row (custom, if logged in)    | dedup'd, geo-tagged             |
| each tile: flag, name, RecProb, CPI 4Q  | "what this affects" tags        |
|            policy rate, +/- vs y/y      | infinite scroll                 |
+--------------------------------------------------------------------------+
| FOOTER STRIP                                                            |
| "Open ledger: today's calibration score for OPENGEM is 0.72."           |
| [link → /ledger/today]                                                  |
+--------------------------------------------------------------------------+
```

## Why F (and not A, B, C, D, E, G)

**A loses** because a tile wall with no editorial says "go figure it out yourself." Bloomberg's terminal works because the user has a thesis and types into a command line. OPENGEM's audience is broader — the YouTuber, the journalist, the LP — and they want a 10-second readout before they decide whether to dive in. A tile wall makes the 10-second job take 90 seconds.

**B loses** because pure newspaper-front-page hands away the density advantage. The FT and the Economist do this beautifully on top of a paid audience that wants to read. OPENGEM is data-grounded; the editorial is *output*, not input. A hero photo would feel like cosplay.

**C is the close second.** Three columns reads well, fits desktop perfectly, and gives equal weight to Situation, Forecasts, Events — the three nouns that define the dashboard. The problem is that all three columns scroll independently, and the user does not know which one matters most today. There is no editorial decision encoded in the layout itself. F encodes "today's headline matters most" by giving it the top slot.

**D loses** on three counts. The globe is gorgeous in a demo and useless in daily use. Globe.gl needs a half-second to a full second to spin up. Mobile portrait gets nothing. And the headline information — which scenarios fired? which countries are in trouble? — is buried below the fold.

**E loses** because four equal quadrants is what dashboards look like when no one has decided what matters. Symmetry is a tell that the designer didn't pick. OPENGEM has a brand voice and it should pick: today's headline matters more than the inflation quadrant.

**G loses** because the terminal aesthetic is intoxicating and wrong-audience. The forecast LP wants a terminal feel; the YouTuber and the journalist will close the tab. Keep terminal as a keyboard-driven *mode* (the command-bar in L128, the keyboard shortcuts in L152) layered over the visual UI, not the default rendering.

**F wins** because it encodes three editorial decisions into the layout:

1. **The headline is the lede.** Today's most important fact gets the top 25% of vertical real estate. The auto-generated lede draws from the highest-priority scenario rollup and the largest forecast revision. It changes daily. It reads in three seconds.
2. **The strip is the dashboard.** Six numbers, each a "world-economy heartbeat" reading. Pickable in any order. Tappable. Sparkline-anchored. This is the "10-second readout."
3. **Country board + event stream is the drill-down layer.** It encodes "depth lives below the strip." If you want to go deeper, scroll. If you don't, you've already read the world in 10 seconds.

## Density math

Headline: 25% of fold height (roughly 240px on a 1080p monitor at 100% zoom). Strip: 15% (~150px, two rows of three on mobile). Left/right pair: 50% (the meat). Footer: 10% (always visible, always pointing at the Ledger).

This means a 13-inch laptop screen at 100% zoom (effective fold ~700px) shows headline + strip + first row of country tiles + first three stream items. That is exactly the "10-second world readout" target.

## What dies if F is wrong

If F is wrong, the headline tile feels like wasted vertical real estate. The fix is to compress the headline to a one-liner ticker and reclaim the row. The strip stays. The pair stays. So the downside risk of F is bounded — at worst it degrades to a slightly fancier version of C.

If C had been picked instead and was wrong, there is no graceful degradation. Three independent scrolling columns either work or do not; they do not become a four-column or two-column without a rewrite.

## What this loop produced

- Seven candidate home-screen layouts as ASCII wireframes.
- Decision: Candidate F (Headline + Strip + Stream).
- Density math (25/15/50/10) and 10-second-readout justification.
- Failure mode for F: collapses gracefully to a richer version of C.
- Explicit exclusion of globe (D) and terminal (G) as defaults; both live elsewhere.

## What comes next

- **L123** designs the Country page (one-level-deeper from any tile on the board).
- **L125** designs the Scenario page (drill into the headline pack).
- **L127** designs the event stream UX (the right column extends to a full page).
- **L161** designs the country card grid in detail (the left half of the pair).
- **L170** designs the top-of-mind feed ranking (what goes into the right half).

## Related

- [[L121-information-architecture]] — World tab populates this page
- [[L123-country-page]] — every country tile drills here
- [[L127-event-stream]] — right column is a preview of the full /events feed
- [[L142-mobile-information-density]] — F collapses gracefully to portrait
- [[L145-dashboard-themes]] — terminal-orange theme applies to this page
