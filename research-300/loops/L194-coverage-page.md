# L194 — Coverage Page: Sparse Matrix UX

**Loop**: 194 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

A "coverage page" is the honest answer to *"what forecasts can I get from OPENGEM, for which countries, at which horizons?"* It is the navigable index into the entire forecast surface. The challenge: the surface is sparse — not every country × indicator × horizon cell has a forecast — and the page must communicate sparsity *honestly* without looking broken.

This loop pins the matrix layout, the sparsity legend, and the click-through behaviour.

## The matrix

The coverage matrix has three axes flattened into two visual dimensions:

- **Rows**: countries, grouped by tier (V-Core, V-Extended, Tracked).
- **Columns**: `(indicator × horizon)` tuples, in canonical order.

At IOC the table is approximately 26 rows (Tier-V Core) + ~10 rows (Tier-V Extended placeholder) + ~150 rows (Tier-T placeholder) × ~25 columns (5 indicators × 5 horizons, plus situation-subsystem columns).

The table is large. The UX has to make it scan-friendly.

## Cell states

Each cell shows one of five states:

| State | Visual | Meaning |
|---|---|---|
| **leaderboard** | filled solid teal tile with leaderboard rank number | Forecast published; on the public leaderboard (Tier-V cells only) |
| **published** | filled solid teal tile, no number | Forecast published; not on leaderboard (Tier-T published) |
| **calibrating** | filled hatched teal | Forecast publishes but PIT-KS currently fails; warning attached |
| **planned** | empty grey outline | In scope for Block II or III; not yet published |
| **out-of-scope** | small × marker | Explicitly excluded (e.g. policy rate 5Y) |

The five states cover every cell. No cell is "unknown" — sparsity is *explicit, named, and dated*.

## Layout sketch

```
COUNTRY          GDP            CPI            UR             POLRATE       RECESSION
                 N  1Q 4Q 2Y 5Y N  1Q 4Q 2Y 5Y N  1Q 4Q 2Y  N  1Q 4Q       12m

V-CORE TIER (leaderboard scope)
─────────────────────────────────────────────────────────────────────────────
USA             ■1 ■1 ■1 ■1 ▣  ■2 ■1 ■2 ■2 ▣  ■1 ■1 ■1 ▣   ■1 ■1 ▣        ■1
GBR             ■2 ■2 ■2 ■3 ▣  ■1 ■2 ■1 ■3 ▣  ■2 ■2 ■2 ▣   ■2 ■2 ▣        ■2
DEU             ■1 ■3 ■3 ■2 ▣  ■3 ■3 ■3 ■2 ▣  ■1 ■3 ■3 ▣   ■3 ■3 ▣        ■3
FRA             ■2 ■2 ■2 ■3 ▣  ■2 ■2 ■2 ■3 ▣  ■2 ■2 ■2 ▣   ■2 ■2 ▣        ■3
JPN             ■3 ■2 ■3 ▣  ▣  ■3 ▣  ▣  ▣  ▣  ■2 ■3 ▣  ▣   ■3 ▣  ▣        ▣
                                  (calibration fail on JPN-CPI 4Q)
... (22 more countries) ...

V-EXTENDED TIER (planned IOC + 1 year)
─────────────────────────────────────────────────────────────────────────────
BRA             □  □  □  □  □  □  □  □  □  □  □  □  □  □   □  □  □        □
IND             □  □  □  □  □  □  □  □  □  □  □  □  □  □   □  □  □        □
...

TRACKED-ONLY (Tier-T)
─────────────────────────────────────────────────────────────────────────────
ZAF             ▣  ▣  ▣  □  □  ▣  ▣  ▣  □  □  □  □  □  □   □  □  □        □
EGY             ▣  ▣  ▣  □  □  ▣  ▣  ▣  □  □  □  □  □  □   □  □  □        □
...
```

Legend at top: ■ leaderboard rank #N · ▣ published (no leaderboard) · ▩ calibrating warning · □ planned · × out-of-scope.

The header row groups columns by indicator with a sub-row for horizon labels (N = nowcast, 1Q, 4Q, 2Y, 5Y, plus 12m for recession-only).

## Click-through

- Click a cell → opens the forecast detail page (L195 chart) for that country × indicator × horizon.
- Click a country name → opens the country page (all indicators).
- Click a column header → opens the indicator page (all countries at that horizon).
- Click a tier divider → opens the tier methodology page (what V-Core, V-Extended, Tracked mean).

Every clickable element has a `cmd+click` to open in a new tab (the prosumer cohort lives in tabs).

## Filter and search controls

Above the matrix, the user can:

- Filter by tier (default: show all).
- Filter by country (multi-select with search; type "USA" → autocompletes).
- Filter by indicator family (GDP, CPI, UR, POLRATE, RECESSION).
- Filter by horizon.
- Toggle showing planned/out-of-scope cells (default: hide planned, show out-of-scope as ×).
- Sort countries by tier > leaderboard rank average > alphabetical.

Filters update the URL hash so a filtered view is shareable (`opengem.org/coverage#tier=V-Core&indicator=GDP`).

## Summary stats above the matrix

A one-line stat panel above the matrix:

```
Coverage as of 2026-06-06:
  ▲ 26 countries on leaderboard · 8 published Tier-T · 134 planned
  ▲ 442 cells published · 408 calibrated · 34 calibration warning
  ▲ Last update: 2026-06-06 08:00 UTC · Next refresh: 2026-06-06 14:00 UTC
```

This is what a journalist or researcher scans first before deciding to click in.

## Density across screen sizes

- **≥1280 px** (desktop): full matrix, all columns, ~25 columns × 50 rows visible.
- **≥768 px** (tablet): collapse the multi-horizon group; show one summary cell per `(country, indicator)` with horizons accessible via a hover or click-expand.
- **<768 px** (mobile): drop the matrix; show country cards in a list, each card with a "see all forecasts" link.

## Sparsity is information

Showing "USA 5Y unemployment: ×" (out of scope) is more informative than hiding the cell. The "×" tells the reader: "We do not publish this, by policy, here's why." A link goes to the policy page that explains the methodological reason for excluding 5Y UR.

Showing "JPN 4Q CPI: calibration warning" is more informative than removing JPN from the matrix. The warning is honest; the page links to the PIT plot (L193) where the failure is fully visible.

This is the L001 discipline — every absence is named.

## Refresh cadence

The coverage page refreshes on these triggers:

1. Daily at 00:00 UTC for the summary stats and last-update timestamps.
2. On every cell publication change (new cell added, cell calibration flips state).
3. On every weekly backtest run.

The page itself is statically generated from the V&V results table and CDN-served. Sub-second load even on mobile.

## API contract

A machine-readable version of the coverage matrix is available for LLM grounding:

```
GET /v1/coverage
→ {
    "schema": "opengem.coverage.v1",
    "as_of": "2026-06-06T08:00:00Z",
    "summary": {
      "n_countries_leaderboard": 26,
      "n_countries_published_tier_t": 8,
      "n_countries_planned": 134,
      "n_cells_published": 442,
      "n_cells_calibrated": 408,
      "n_cells_warning": 34
    },
    "matrix": [
      {"country": "USA", "tier": "V-Core",
       "cells": [
         {"indicator": "GDP-real-yoy", "horizon": "nowcast", "state": "leaderboard", "rank": 1, "calibration": "pass"},
         {"indicator": "GDP-real-yoy", "horizon": "1Q", "state": "leaderboard", "rank": 1, "calibration": "pass"},
         ...
       ]},
      ...
    ]
  }
```

## Subtle UX considerations

- **Avoid red.** Calibration-fail cells use a brown/amber hatched fill, not red. Red reads as "broken"; the reality is "fully published with a known limitation". The hatching communicates "with caveat".
- **Tooltip on hover** shows the cell's headline metric ("CRPS = 0.42, CRPS-vs-AR(1) win-rate = 83%") + last refresh date.
- **Aria labels** on every cell for screen-reader accessibility.

## What this loop produced

- Five-state cell legend (leaderboard / published / calibrating / planned / out-of-scope).
- Matrix layout sketch.
- Click-through routing.
- Filter and search controls.
- Summary stats panel.
- Responsive collapse behaviour.
- Machine-readable coverage API.

## What comes next

- **L195** — forecast detail page that opens on click.
- **L199** — trust badges shown next to each cell on hover.

## Related

- [[L181-forecast-object-schema]] — what each cell points at.
- [[L184-leaderboard-ranking]] — leaderboard ranks shown in cells.
- [[L193-calibration-plots]] — PIT plots reached from warning cells.
- [[L195-forecast-ui-spec]] — drill-down chart.
- [[L199-trust-signals]] — badges on hover.
- [[R07-tier-v-roster]] — country tier definitions.
