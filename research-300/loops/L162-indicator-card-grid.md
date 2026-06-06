# L162 — Indicator Card Grid Pattern

**Loop**: 162 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

The "indicator card grid" is the inverse of the country card grid (L161). Where L161 picks countries and shows N indicators per country, this picks **indicators** and shows N countries per indicator. The page is a small-multiples chart wall.

Used on:
- Indicator pages (e.g., `/indicator/cpi-yoy` shows CPI across 30 countries)
- "Compare indicators" view (top 4 indicators, all G7)
- Watchlist views (user's indicators, user's countries)

## The indicator card (atom)

```
   ┌─────────────────────────────────────────────────────┐
   │  CPI YoY · USA                                        │
   │  ──────────────────────────────────────              │
   │  3.4%   ▲ +0.2pp                                      │
   │                                                       │
   │       ╱╲       ╱──                                    │
   │     ╱    ╲   ╱                                        │
   │   ╱        ╲╱                                         │
   │                                                       │
   │  Mar-26    May-26                                     │
   │  Range: 0.1 – 9.1   (since 2020)                     │
   │  Source: FRED CPIAUCSL                               │
   └─────────────────────────────────────────────────────┘
   width: ~320px, height: ~200px
```

Card components:
- Indicator + country header
- Latest value + delta
- Mini-chart (Level 3 per L149)
- 2-tick x-axis
- Range disclosure (min/max over reference period)
- Source attribution

## Use case 1: indicator page

`/indicator/cpi-yoy?countries=usa,deu,fra,gbr,jpn,ita,can` produces a 7-card grid of CPI sparklines.

Layout: responsive grid. At 1440px: 4 columns. At 1024px: 3 columns. At 768px: 2 columns. At <640px: 1 column stacked.

```
   CPI YoY across G7
   ──────────────────────────────────────────────────
   ┌──────────┬──────────┬──────────┬──────────┐
   │ USA      │ DEU      │ FRA      │ GBR      │
   │ 3.4 ▲    │ 2.6 ⌃    │ 2.4 ▼    │ 2.9 ⌃    │
   │ ─╱╲╱─    │ ─╲─╱─    │ ─╲╱╱─    │ ─╱╲╱─    │
   ├──────────┼──────────┼──────────┼──────────┤
   │ JPN      │ ITA      │ CAN      │ (empty)  │
   │ 1.2 ▲    │ 1.8 ⌃    │ 2.5 ▼    │          │
   │ ─╱╱╱─    │ ─╲╲─╱    │ ─╲─╱─    │          │
   └──────────┴──────────┴──────────┴──────────┘
```

## Use case 2: 4-up indicator view

The "indicator card" is also the building block for a 4-up dashboard:

```
   USA macro
   ──────────────────────────────────────────────────
   ┌─────────────────────────┬─────────────────────────┐
   │ CPI YoY                  │ GDP nowcast             │
   │ 3.4%   ▲ +0.2pp           │ 2.1%   ⌃ flat            │
   │ [mini chart]             │ [mini chart]            │
   ├─────────────────────────┼─────────────────────────┤
   │ Unemployment             │ Policy rate              │
   │ 4.0%   ⌃ flat             │ 5.25%  ⌃ held            │
   │ [mini chart]             │ [mini chart]            │
   └─────────────────────────┴─────────────────────────┘
```

This is the structure that goes inside a country page (each indicator a card), each card pull from a different indicator's data.

## The shared x-axis option

By default each card has its own x-axis. The "synchronize axes" toggle aligns all cards to a shared range — useful for comparing series of different cadences. When toggled:

- All cards show the same date range
- All cards use the same scale (this is automatic if same indicator across countries)
- All cards highlight the same hover-x (cross-chart cursor)

This is the small-multiples discipline. Tufte-coded.

## Cross-chart cursor

When hovering on any card with synchronized axes, all other cards show a vertical line at the same x position with a numeric label for their value. The dashboard becomes a single coordinated chart.

This is the "Bloomberg-grade" affordance — the asymmetric advantage over Excel-screenshots-pasted-into-Substack.

## Indicator picker

The page header includes:
```
   Indicator:  [ CPI YoY ▼ ]   Y/Y  ☑   Bands ☐   Log scale ☐
   Countries:  [ + G7 ] [ + G20 ] [ + Custom ]    Selected: 7
```

The "Y/Y" toggle re-aggregates the underlying data. Bands toggles confidence layers (if forecast). Log scale for the y-axis.

## Sort order

- Default: by alphabetical country code
- "Sort by..." dropdown: by latest value desc, by latest delta desc, by surprise score, by similarity to a target country (e.g., "show countries most like Germany")

## Indicator scrubber (URL-bound)

The bottom of the page has a horizontal indicator picker — a strip of all indicators in the same group (e.g., the "inflation family": CPI YoY, CPI MoM, Core CPI, PPI, etc.). Clicking jumps to that indicator with the same country selection.

```
   ▼ Inflation family
   CPI Y/Y  ・  CPI M/M  ・  Core CPI  ・  PPI Y/Y  ・  Wage Y/Y
```

## Empty cards

If a country lacks data for the selected indicator:

```
   ┌──────────────┐
   │ MMR          │
   │ — no data —  │
   │              │
   │ Coverage gap │
   │ [request]   │
   └──────────────┘
```

A grayed-out card with a "request indicator coverage" link — feeds into the data engineering backlog.

## "Sparkbar" mode

For very dense grids (e.g., 38 OECD countries), the user can downgrade to "sparkbar" mode: each card collapses to a single row with a sparkline + value:

```
   USA  CPI YoY  3.4% ▲   ─╱╲╱──
   DEU  CPI YoY  2.6% ⌃   ─╲─╱──
   FRA  CPI YoY  2.4% ▼   ─╲╱╱──
   ...
```

This is the table form of the same data. Sortable columns.

## "Heatcard" mode

Another downgrade: each card collapses to a colored tile showing only the latest value (using sequential or diverging palette from L148):

```
   ┌─────┬─────┬─────┬─────┐
   │ USA │ DEU │ FRA │ GBR │
   │ 3.4 │ 2.6 │ 2.4 │ 2.9 │
   ├─────┼─────┼─────┼─────┤
   │ JPN │ ITA │ CAN │     │
   │ 1.2 │ 1.8 │ 2.5 │     │
   └─────┴─────┴─────┴─────┘
```

Cell color encodes value vs target / threshold. Useful for at-a-glance "where's it hot."

## Density ladder

| Mode | Cards per row | Detail per card |
|---|---|---|
| Full | 3–4 | Mini-chart + axis + range + source |
| Compact | 4–6 | Mini-chart + value + delta |
| Sparkbar | 1 (row form) | Sparkline + value |
| Heatcard | 6–8 | Color cell + value only |

Toggle via top-right segmented control. Defaults to Full at >1024px, Compact below.

## URL pattern

```
/indicator/cpi-yoy?countries=usa,deu,fra,gbr,jpn,ita,can&density=full&sort=value-desc
/indicator/cpi-yoy?cohort=g7
/indicator/cpi-yoy?cohort=oecd&density=heatcard
```

`cohort=` is a shortcut: expands to the list. `density=` controls mode.

## Comparison overlay (toggle)

The "Show all on one chart" toggle collapses the grid into a single multi-line chart. Same data, different view. Useful for trend comparison; loses per-country resolution.

## Forecast layers

If the indicator has a forecast, each card can optionally show the forecast band overlaid:

```
   USA CPI
   3.4% ▲    fcast 4Q: 2.8% (P10 2.1, P90 3.5)
   ─╱╲╱── ⌈ ⌉   ← forecast fan extension
```

Toggleable. Off by default to keep the cards readable.

## Forecast leaderboard tie-in

If forecasts exist for this indicator, a "Show leaderboard for CPI" link appears, routing to the per-indicator leaderboard (L133).

## Performance

For a 38-card OECD view: 38 mini-charts. Server-rendered SVG for first paint. Hover/interaction hydrated lazy. Bundle: <80KB JS additional for full interactivity.

## Implementation

- Cards are server components by default
- Sparklines: hand-rolled SVG generator (same as L161)
- Mini-charts: shared D3 component, controlled by `mode` prop
- Cross-chart cursor: a shared Zustand store updated on hover, subscribed by every card
- Virtualization: only for "All countries" (200+ cards)

## Mobile

At <640px, cards stack vertically. Each card retains the mini-chart at full width. Density mode forced to Compact. Heatcard mode unavailable below tablet width.

## Indicator-specific defaults

Some indicators have natural defaults:
- CPI Y/Y → range = last 5 years, Y/Y toggle on
- GDP Q/Q SAAR → range = last 10 years
- Policy rate → range = last 10 years, step-chart style
- Unemployment → range = last 10 years, recession bands on

These defaults live in the indicator catalog and apply when the user first lands without explicit URL params.
