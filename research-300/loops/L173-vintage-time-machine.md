# L173 — Vintage Time Machine

**Loop**: 173 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

"Rewind to September 2024 and show me what we were forecasting then." This single UX makes OPENGEM's accountability arc tangible. The user can replay history, see what we got right, what we got wrong, what the world looked like.

It's both a demo feature and a research tool.

## The UX

A vintage selector in the top-right of every page:

```
   ┌────────────────────────────────┐
   │  Vintage: [ 2026-06-04 ▼]   ⏪ │
   └────────────────────────────────┘
```

Clicking the dropdown opens a date picker. Clicking the rewind icon opens the full time-machine drawer.

## The time-machine drawer

```
   ┌──────────────────────────────────────────────┐
   │  ✕  Time Machine                              │
   │  ──────────────────────────────────────────  │
   │                                                │
   │  Current vintage: 2026-06-04 (latest)          │
   │  Rewind to:                                    │
   │                                                │
   │  ┌────────────────────────────────────────┐  │
   │  │ [Calendar with available vintages       │  │
   │  │  highlighted as bullet points]          │  │
   │  └────────────────────────────────────────┘  │
   │                                                │
   │  Quick rewind:                                 │
   │   [-1 day] [-1 week] [-1 month] [-3mo] [-1y]  │
   │                                                │
   │  Significant moments:                          │
   │   • 2024-09-18  Fed cut 50bps                 │
   │   • 2024-08-05  Japan FX shock                │
   │   • 2024-03-22  SVB anniversary               │
   │   • 2024-02-24  Russia-Ukraine 2yr            │
   │   ...                                          │
   │                                                │
   │  ──────────────────────────────────────────   │
   │  [ Rewind ]                                    │
   └──────────────────────────────────────────────┘
```

## URL contract

```
   ?vintage=2024-09-18
   ?asof=2024-09-18T15:30:00Z   (second-resolution)
```

`vintage` = data snapshot. The chart shows what data existed on that date.

`asof` = same idea but second-resolution. Used for replaying a release moment.

Per L154 — these are URL params on any page.

## What changes when rewound

Every data display, every forecast, every score, every methodology is pinned to the vintage. Specifically:

| Surface | Behavior at vintage |
|---|---|
| Chart data | Shows only data points published ≤ vintage |
| Forecast | Shows the forecast issued at the vintage (not the latest) |
| Methodology version | Shows the methodology that was in use |
| Pulse score | Shows the pulse computed at that date |
| Surprise index | Shows the index value at that date |
| Glossary | Same (definitions don't have vintages) |
| Navigation / shell | Same (UI doesn't time-travel; only data does) |

## The rewind banner

When in rewind mode, a persistent banner across the top:

```
   ┌──────────────────────────────────────────────┐
   │ ⏪ Viewing 2024-09-18 vintage.                  │
   │ (~21 months ago)             [Return to live] │
   └──────────────────────────────────────────────┘
```

Yellow / warn-colored to make the time-shift unmissable. Clicking "Return to live" removes the param.

The banner persists across navigation. Routing to another page preserves the vintage.

## The "what we forecast then vs what actually happened" overlay

In rewind mode, every chart with a forecast layer optionally renders an extra layer: "actuals since vintage."

```
   USA CPI YoY forecast at 2024-09-18 vintage
   ──────────────────────────────────────────────
                                              actual ●●
            P90 ╲   ╲   ╲
   3.5%       ╲   ╲   ╲                       ●
                                              
                                                ●
   3.0%   ──────────●──────●                    
                              forecast P50         
                                                
   2.5%       ╱   ╱   ╱
                  P10 ╱
                                              
       2024-09  2024-12   2025-03   2025-06   
       forecast horizon
```

The actuals since vintage trace beyond the forecast band. The user can see how well OPENGEM did.

## The animated rewind

A "play" button on the time-machine drawer:

```
   ┌──────────────────────────────────────────────┐
   │  ▶ Animate from 2024-09 to today (21 months) │
   │                                                │
   │  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
   │                                                │
   │  Frame: 2024-12  ←─── slider ───→             │
   │                                                │
   │  Speed: [ 1mo/sec ▼]                          │
   └──────────────────────────────────────────────┘
```

Plays through the vintages. Each frame stamp updates. Useful for telling stories ("watch our recession-prob rise through Q1 2025").

Exportable as GIF (L155). Killer.

## Significant moments catalog

Editorially curated. A list of dates worth rewinding to:

- 2024-09-18 — Fed 50bps cut
- 2024-08-05 — Japan FX / yen carry unwind
- 2024-03-22 — SVB anniversary (regional bank stress)
- 2024-02-24 — 2yr anniversary of Russia-Ukraine
- 2023-10-07 — Israel-Hamas
- 2023-03-10 — SVB failure
- 2022-09-23 — UK Truss mini-budget
- 2022-02-24 — Russia invasion
- 2020-03-23 — Global market low
- 2020-03-11 — WHO pandemic declaration
- 2008-09-15 — Lehman
- ...

User-curated lists (paid feature) come later.

## Coverage by vintage

OPENGEM has data from:
- Forecasts: from 2024-Q1 onward (when we started publishing)
- Indicator data: from 1990 (earlier where available)
- Methodology versions: from v1.0 (Q4 2023)

Earlier vintages have less coverage. The calendar dims unavailable dates.

For pre-2024 dates: we can replay raw data but not OPENGEM forecasts (we didn't exist). Useful for backtesting demos.

## Implementation

- URL params parsed at page-render time
- Data fetch includes `vintage` parameter
- Server cache keyed on (entity, vintage)
- Storage: vintaged data stored in an Iceberg/Delta table per L078; lookup by date is O(1)
- Methodology resolved via methodology catalog lookup

## Performance

- Switching vintages: typical fetch <500ms (cached vintages are <100ms)
- Animation playback: pre-rendered frames cached, playback at 30fps
- Storage cost: bounded by Iceberg compression; entire vintage store fits in single-digit TB

## "Compare two vintages" mode

Drawer offers a "compare two vintages" toggle:

```
   Compare:
     A: 2024-09-18
     B: 2026-06-04 (latest)
```

The chart then renders both layers — forecast at A as a dashed line, forecast at B as a solid line. Diff annotations between them.

## The accountability tie-in

Rewinding makes the accountability page (L175) immediately useful. A user can:
1. Rewind to 2024-09
2. See the forecast we published
3. Fast-forward to today
4. See how well it played out

This is the "OPENGEM publishes its mistakes" thesis in motion.

## Mobile

At <640px:
- Vintage selector compresses to icon + date
- Drawer slides up as a bottom sheet
- Animation playback simplified (no real-time chart rendering; pre-rendered frames as a slideshow)

## Sharing a vintage view

The URL with `?vintage=...` is shareable per L154/155. A user can tweet "Here's what OPENGEM forecast for inflation in Sep 2024 — they were 0.3pp high: <url>."

This is the unhinged transparency move. No incumbent does this.

## Editorial use

OPENGEM editorial uses the vintage time-machine to write retrospective pieces ("How OPENGEM saw the Fed cut six weeks before it happened"). The piece embeds vintage-pinned charts.

The editorial team has a "rewind to write" button that opens an editor with the vintage pinned, ready to compose.

## What we won't ship

- Hourly vintage resolution. Daily is the discipline. Intraday revisions are an L181/L182 concern; vintage is end-of-day.
- Editing past forecasts. We never rewrite history.
- Comparing more than 2 vintages on one chart. After 2, the chart becomes spaghetti. Use animation instead.

## The asymmetric move

Bloomberg doesn't time-travel. Their data is current-state; old vintages live only in archives accessible to subscribers via separate commands. The terminal UX is "now" by default.

OPENGEM's time-machine is one click from anywhere. It's the user experience embodiment of "we publish our history."
