---
loop: 133
phase: 3
title: Forecast Leaderboard Page
date: 2026-06-06
status: decided
---

# L133 — Forecast Leaderboard Page

**Loop**: 133 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design `/ledger/scoreboard`. Per-indicator × per-horizon × per-model leaderboard. Sort order. Columns. Drilldown.

This is the page that makes OPENGEM dangerous to the cartel. It is the page that lets a journalist write "OPENGEM beat WEO on US CPI 4Q forecasts in 14 of the last 16 vintages." It is the page that makes the calibration argument concrete.

## The structure

The page is a configurable scoreboard. The user picks an indicator, a horizon, a country (or "world aggregate"), a metric, and a baseline; the table shows forecaster ranks by that metric over a rolling window.

```
+--------------------------------------------------------------------------+
| OPENGEM > Ledger > Scoreboard  ·  /ledger/scoreboard                      |
+--------------------------------------------------------------------------+
| FILTERS                                                                   |
| [Indicator: CPI YoY ▼] [Horizon: 4Q ▼] [Country: USA ▼]                  |
| [Metric: CRPS ▼ (lower is better)]                                        |
| [Window: trailing 24 vintages ▼]                                          |
| [Forecasters: ✓ OPENGEM ✓ WEO ✓ OECD EO ✓ FRB SEP ✓ Cleveland ✓ Atl.GDPNow|
|              ✓ ECB SPF ✓ random walk ✓ AR(1) baseline]                    |
+--------------------------------------------------------------------------+
| LEADERBOARD                                                               |
|                                                                          |
| Rank Forecaster           CRPS    Δ vs OPENGEM   PIT   Bias   MAE   Win% |
|                                                                          |
|  1   OPENGEM L3-BMA       0.842   (anchor)       0.78  -0.04  0.31   —    |
|  2   FRB SEP              0.871   +0.029         0.74  -0.07  0.33   0.42|
|  3   Cleveland Nowcast    0.880   +0.038         —     -0.02  0.32   0.50|
|  4   WEO Apr/Oct          0.912   +0.070         0.68  +0.11  0.36   0.38|
|  5   OECD EO May/Nov      0.918   +0.076         0.71  +0.09  0.35   0.42|
|  6   ECB SPF              0.951   +0.109         0.70  +0.06  0.38   0.46|
|  7   AR(1) baseline       1.421   +0.579         0.65  +0.04  0.51   0.21|
|  8   Random walk          1.512   +0.670         0.51  +0.18  0.62   0.17|
|                                                                          |
| Win% column: fraction of trailing vintages where this forecaster's       |
| P50 was closer to actual than OPENGEM's P50.                             |
+--------------------------------------------------------------------------+
| VIZ STRIP                                                                |
|                                                                          |
| ┌────────────────────────────────────────────────────────────────────┐  |
| │  CRPS over time (trailing 24 vintages, line per forecaster)         │  |
| │                                                                     │  |
| │  ─── OPENGEM L3-BMA                                                 │  |
| │  ─── FRB SEP                                                         │  |
| │  ─── WEO                                                             │  |
| │  ─── OECD EO                                                          │  |
| │  ┄ random walk                                                       │  |
| │                                                                     │  |
| │  with annotations at each vintage (release date markers)            │  |
| └────────────────────────────────────────────────────────────────────┘  |
+--------------------------------------------------------------------------+
| DRILLDOWN PER FORECASTER (click a row)                                  |
|                                                                          |
| Selected: FRB SEP                                                        |
|   Source: federalreserve.gov/monetarypolicy/fomccalendars.htm           |
|   Cadence: 4 vintages/year (March, June, September, December)           |
|   Coverage: US-only (PCE inflation; we map to CPI for comparison)        |
|   Calibration to date:                                                   |
|     CRPS  0.871  (vs OPENGEM 0.842)                                      |
|     PIT   0.74                                                            |
|     Bias  -0.07                                                          |
|   Forecast values, last 4 vintages:                                     |
|     2026-06 SEP   2.6%  vs actual ___  (pending)                         |
|     2026-03 SEP   2.9%  vs actual 2.7%  miss -0.2                        |
|     2025-12 SEP   2.5%  vs actual 2.4%  miss +0.1                        |
|     2025-09 SEP   2.6%  vs actual 2.9%  miss -0.3                        |
|                                                                          |
| [Open FRB SEP page →] [Compare per-vintage view →]                        |
+--------------------------------------------------------------------------+
| METHODOLOGY                                                              |
| · CRPS computed on density forecast (where available) or P50 + std       |
|   approximation when only point forecast is published.                   |
| · Coverage: USA CPI YoY 4Q-ahead, trailing 24 vintages (2020-06 onwards).|
| · Baseline normalization: each metric is reported in original units; the |
|   Δ vs OPENGEM column subtracts OPENGEM's value.                         |
| · Forecaster comparison is on the same dates only (intersection of       |
|   vintage availability). Misses are computed against final published     |
|   actual (not vintage-truncated).                                        |
| · Full methodology: [/ledger/methodology]                                |
+--------------------------------------------------------------------------+
| [Embed this scoreboard] [Cite] [API] [Subscribe to scoreboard digest]   |
+--------------------------------------------------------------------------+
```

## Why this structure (and not the alternatives)

The natural alternative is a top-level "all-cells leaderboard" — show every (indicator, horizon, country) cell ranked across all forecasters. That structure is wrong for two reasons:
1. It is overwhelming on first arrival (too many cells, no editorial).
2. It conflates apples and oranges (CPI 4Q is not GDP 4Q; the metric magnitudes differ).

The configurable-with-defaults structure lets the user land with sensible defaults (CPI YoY × 4Q × USA × CRPS × OPENGEM beats baselines) and explore from there.

## Column choices

- **Rank**: integer rank by selected metric.
- **Forecaster**: name + tiny logo + link to forecaster info page.
- **Metric value**: in original units (CRPS, MAE, etc.).
- **Δ vs OPENGEM**: signed difference vs OPENGEM's value, color-coded green (better than OPENGEM) / red (worse than OPENGEM).
- **PIT** (probability integral transform): the calibration metric. Higher is better, with 0.70 as the "pass" threshold (per L008-vv-matrix bar). Only shown where density forecasts exist.
- **Bias**: signed mean forecast error. Closer to 0 is better.
- **MAE**: mean absolute error. Lower is better.
- **Win%**: fraction of trailing vintages where this forecaster beat OPENGEM by P50. The "head-to-head" column. Sortable.

The columns are configurable in a `[Columns ▼]` menu but the default set is the above six.

## Sort order

Default sort: by selected metric, ascending if "lower is better" (CRPS, MAE, |Bias|), descending if "higher is better" (PIT, Win%, AUC for binary).

OPENGEM is highlighted (background tint) in the row regardless of its rank, so the user can see "where do we sit?" at a glance. If OPENGEM is rank 1, the highlight is a positive shade. If OPENGEM is rank 7, the highlight is unchanged — we do not hide our position.

## Metric choices

- **CRPS** (Continuous Ranked Probability Score): primary metric for density forecasts. Lower is better.
- **Log-score**: alternative for density forecasts. Higher is better.
- **MAE**: point-forecast metric. Universal applicability.
- **RMSE**: point-forecast metric. More sensitive to large misses.
- **PIT**: calibration. Higher is better (within 0-1 range with 0.70 threshold).
- **Bias**: |mean error|. Lower is better.
- **Win%**: head-to-head fraction. Higher is better.
- **AUC** (for binary forecasts like recession probability): higher is better.

## Forecaster inclusion rules

- OPENGEM L3-BMA — always included.
- Public institutional forecasters (WEO, OECD EO, FRB SEP, ECB SPF, Cleveland Fed Nowcast, Atlanta GDPNow) — included where coverage applies. If a forecaster does not publish at the relevant indicator × country × horizon, it is excluded from that scoreboard.
- Naive baselines (Random Walk, AR(1)) — always included.
- BloombergEcon, Goldman GIR, JPM Macro — *not* included by default because we cannot legally redistribute their forecasts. We mention them in the methodology footer ("not included because proprietary") so the absence is not a hidden bias.
- Forecast LP customers' own forecasts — included on their private scoreboard view, never on the public page (per pricing model).

## Drilldown per forecaster

Clicking a row expands a panel below the leaderboard with:
- Source URL + cadence + coverage scope.
- Calibration scorecard.
- Last 4 forecast values + actuals + misses.
- Links to: forecaster's own page (e.g., WEO landing), per-vintage compare view (Compare-2 with OPENGEM vs this forecaster on this cell).

## The viz strip

Below the table, a line chart shows CRPS (or selected metric) over time for each visible forecaster. Line per forecaster, color-coded. The chart includes a release-date marker for each vintage, so the user can see "OPENGEM dropped to 0.7 CRPS after the Sept 2024 vintage."

The viz is the storytelling layer. Without it, the leaderboard is just a table. With it, the user sees the *trajectory* of OPENGEM's outperformance (or underperformance).

## Window choices

- Trailing 24 vintages (default, ~2 years for monthly forecasters)
- Trailing 12 vintages
- Trailing 8 vintages
- Trailing 4 vintages
- All-time (since inception)
- Custom date range

The window affects which vintages contribute to each forecaster's metric.

## Coverage table

A separate `/ledger/coverage` page (linked from the bottom of this page) shows which forecasters publish which indicator × country × horizon cells. This is the "where are the gaps" surface.

## Honest caveats

The methodology box at the bottom is mandatory. It must spell out:

- CRPS computation when only point forecast is available (we approximate with P50 + a "typical historical band" std; this is acknowledged as approximation).
- Vintage availability intersection rules (a forecaster with sparse vintages competes on the dates it published, not on dates it skipped — which can flatter or punish unfairly).
- Final-actual normalization (we use the latest published actual, not the vintage-truncated actual at the time of forecast; this can disadvantage forecasters who forecast against early estimates).
- Coverage normalization (Cleveland Nowcast publishes monthly, WEO publishes semiannually; the comparison is on dates where both publish).

This is the "publishing our mistakes" stance applied to the leaderboard itself: even our scoreboard is open about its limitations.

## Anti-gaming

The forecaster set is *not* user-configurable to "remove poor performers" — it always includes naive baselines (RW, AR(1)) so the user can see "is OPENGEM beating naive?" If a forecaster is missing from the displayed set, it is shown in a "Not displayed (no coverage on this cell)" line at the bottom.

The user can deselect forecasters in the viz strip to declutter, but the leaderboard table always shows the full ranked set.

## What this loop produced

- Page is configurable scoreboard: indicator × horizon × country × metric × window × forecaster set.
- Default state: CPI YoY × 4Q × USA × CRPS × 24 vintages × all forecasters.
- Six columns: Rank, Forecaster, Metric, Δ-vs-OPENGEM, PIT, Bias, MAE, Win%.
- OPENGEM row highlighted regardless of rank.
- Viz strip: line per forecaster over rolling vintages, with release annotations.
- Drilldown panel on row click with source, cadence, last 4 forecasts.
- Methodology footer mandatory with honest caveats (CRPS approximation, vintage intersection, final-actual normalization).
- Anti-gaming: baselines always included; missing forecasters listed explicitly.
- Embed + cite + API + subscription.

## What comes next

- **L134** designs the track-record page (single-cell deep dive vs this multi-cell view).
- **L194** designs the coverage page (which forecaster covers which cell).
- **L190** designs the consensus comparison detail.
- **L200** designs the failure log per-forecaster.

## Related

- [[L121-information-architecture]] — /ledger/scoreboard URL space
- [[L126-forecast-page]] — leaderboard drilldown links here
- [[L132-provenance-drawer]] — per-cell drawer with same data
- [[L134-track-record-page]] — single-cell calibration drill
- [[L184-ranking-algorithm]] — algorithm behind the ranking
- [[L190-consensus-comparison]] — consensus source list
