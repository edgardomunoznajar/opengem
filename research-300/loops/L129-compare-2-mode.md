---
loop: 129
phase: 3
title: Compare-2 Mode — Side-by-Side Layout
date: 2026-06-06
status: decided
---

# L129 — Compare-2 Mode: Side-by-Side Layout

**Loop**: 129 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design Compare-2: a side-by-side mode for two records of the same type (two countries, two indicators, two scenarios). Invoked via command bar (`> compare USA EZ`), via the `c` keystroke from a record page, or via URL (`/compare?a=...&b=...`). Pick a layout pattern.

## Why no Compare-3 / Compare-N

Compare-2 is the standard. Compare-3 looks tempting but breaks down quickly:
- Charts overlay poorly past two lines (the bands collide).
- Map regions stop being legible past two countries highlighted.
- The cognitive load of "which one is which" jumps with N.
- For >2 comparison, the Indicator page small-multiples (L124) is the right surface — 19 panels at once, browse, no overlay.

So Compare-2 is a focused side-by-side. If users want N-way comparison they use the Indicator page or the Scoreboard view (L133). This keeps Compare-2 simple and good rather than configurable and mediocre.

## Layout pattern — "Mirror with shared chrome"

```
+--------------------------------------------------------------------------+
| OPENGEM > Compare > USA vs EUR  ·  /compare?a=USA&b=EUR                  |
+--------------------------------------------------------------------------+
| SHARED CONTROLS (apply to both sides)                                    |
| [Indicator: CPI YoY ▼] [Horizon: 4Q ▼] [Vintage: 2026-06-02 ▼]          |
| [Consensus overlay: WEO ▼] [Sync axes: ON ▼] [Side ratio: 50:50 ▼]      |
+--------------------------------------------------------------------------+
| LEFT (50%)                              | RIGHT (50%)                    |
|                                          |                                |
| 🇺🇸 UNITED STATES                          | 🇪🇺 EURO AREA                  |
| CPI YoY 2.9% ▼0.2pp m/m                  | CPI YoY 2.4% ▼0.1pp m/m         |
| P50 4Q ahead 2.4% band 1.4-3.5%         | P50 4Q ahead 2.2% band 1.2-3.4%|
| consensus 2.8% (OPENGEM -0.4pp)         | consensus 2.5% (OPENGEM -0.3pp)|
|                                          |                                |
| ┌──────────────────────────┐             | ┌──────────────────────┐     |
| │ chart with bands         │             | │ chart with bands     │     |
| │ x-axis synced            │             | │ x-axis synced        │     |
| │ y-axis synced (toggle)   │             | │ y-axis synced        │     |
| └──────────────────────────┘             | └──────────────────────┘     |
|                                          |                                |
| Scenarios triggered: 2                   | Scenarios triggered: 4         |
|  Trade-LATAM P=0.62 (partial)            |  Red-Sea-#4 P=0.78             |
|  EU-rate-hold P=0.55                     |  Trade-LATAM P=0.62 (partial)  |
|                                          |  EU-rate-hold P=0.55           |
|                                          |  Oil-shock P=0.34              |
|                                          |                                |
| Recent events: 12                        | Recent events: 18              |
| (last 14 days)                           | (last 14 days)                 |
+------------------------------------------+--------------------------------+
| DIFF STRIP (synthesis, full-width)                                       |
|                                                                          |
| CPI gap:        USA 2.9% vs EUR 2.4%      diff +0.5pp                   |
| P50 4Q gap:     USA 2.4% vs EUR 2.2%      diff +0.2pp                   |
| consensus gap:  WEO USA 2.8% vs EUR 2.5%  WEO diff +0.3pp               |
| Scenarios diff: USA has 0 not in EUR; EUR has 2 not in USA              |
| Direction:      USA disinflation faster (slope -0.3pp/Q vs -0.1pp/Q)    |
+--------------------------------------------------------------------------+
| [Swap sides ⇄] [Export both as PDF] [Cite this comparison] [Embed]      |
+--------------------------------------------------------------------------+
```

## Why mirror-with-shared-chrome

The pattern is opinionated: both sides are visually identical templates rendered with different data. Shared controls at top (indicator, horizon, vintage, overlay) apply to both sides simultaneously. The diff strip at the bottom synthesizes the comparison so the user does not have to do mental arithmetic.

Three reasons this beats the alternatives:

1. **Shared axes are tractable.** A common pitfall in side-by-side is each side scaling its own y-axis, so 2.4% in EUR visually equals 2.9% in USA. The "Sync axes" toggle forces a common y-range across both sides; on by default for CPI/GDP/Unemp (where absolute level matters), off for indices (where shape matters). The user can override.

2. **The diff strip is the editorial.** Without a diff, the user has to read two screens and remember both. The diff strip does the arithmetic: gaps, directions, scenario set differences. It is the answer to "what does this comparison show?"

3. **Swap sides is a single keystroke.** Pressing `s` swaps left and right. Useful because the visual order matters for "vs." readings — readers tend to give the left side editorial precedence.

## Cross-type comparison

Compare-2 supports same-type comparison out of the box:
- Country vs Country (per the above example).
- Indicator vs Indicator (e.g., CPI vs Core CPI, both global).
- Scenario vs Scenario (e.g., Trade-LATAM vs Trade-CN-US).

Cross-type comparison (country vs scenario, indicator vs country) is *not* supported. Those are not meaningful side-by-sides; they are cross-references and live as linkbacks on each record page.

## Country vs Country specifics

When comparing two countries, the default indicator is the most-shared indicator from the user's watchlist. If the user has no watchlist, the default is CPI YoY (the most-asked indicator across personas).

The lower half of each side shows scenario set + event count + 3-4 indicator minibars (a tiny strip showing GDP, CPI, Unemp, PR). This gives a multi-indicator readout without forcing the user to switch indicators.

## Indicator vs Indicator specifics

When comparing two indicators, the user picks a country (or "world aggregate") rather than an indicator. Default: USA. Default: latest vintage.

The diff strip switches to indicator-specific synthesis: correlation, lead/lag relationship (cross-correlation peak), volatility ratio.

## Scenario vs Scenario specifics

When comparing two scenarios, each side shows the affected-countries rollup, the trigger conditions, the narrative paragraph, and a count of historical co-fires. The diff strip shows:
- Overlap of affected countries (intersection / union).
- Overlap of trigger sources.
- Historical co-fire rate ("these two have co-fired N times in M past windows").
- Forecast effect difference per shared affected country.

## Sync controls

The shared controls at top:
- **Indicator** (when comparing countries): the active indicator. Both sides show the same one.
- **Horizon**: forecast horizon for both sides.
- **Vintage**: vintage applies to both. Sliding the vintage rewinds both sides synchronously.
- **Consensus overlay**: source of consensus dots on both sides.
- **Sync axes**: y-axis sync toggle (default on for level indicators, off for indices).
- **Side ratio**: 50:50 default; can be 30:70 or 70:30 if the user wants asymmetric attention.

## Mobile

On portrait phones, side-by-side becomes tab-stack: the left side shows by default with a chip control to swap to the right. The diff strip stays at the bottom (it is the synthesis and always relevant). The user can also toggle to "stacked" mode (one side above the other), but only on tablets and larger.

## Compare-2 from a record page

Pressing `c` on any record page opens an inline picker for the second side:

```
+--------------------------------------------------------------------------+
| You are on /c/USA                                                        |
| Compare against:                                                         |
|                                                                          |
| ┌──────────────────────────────────────────┐                            |
| │ search countries...                       │                            |
| └──────────────────────────────────────────┘                            |
|                                                                          |
| Suggested:                                                               |
|   🇪🇺 EUR    🇨🇳 CHN    🇬🇧 GBR    🇯🇵 JPN    🇲🇽 MEX                       |
|   (based on macro similarity + your watchlist + recent visits)          |
|                                                                          |
| [Cancel · Esc]                                                          |
+--------------------------------------------------------------------------+
```

Picking a suggestion or typing a country name navigates to `/compare?a=USA&b=EUR`.

## URL convention

The URL convention is `/compare?a={ID}&b={ID}` with optional `indicator`, `horizon`, `vintage` params. Examples:
- `/compare?a=USA&b=EUR` (defaults)
- `/compare?a=USA&b=EUR&indicator=cpi-yoy&horizon=4Q`
- `/compare?a=USA&b=EUR&vintage=2024-09-15` (compare-at-vintage)
- `/compare?a=trade-latam&b=oil-shock` (scenario comparison)
- `/compare?a=cpi-yoy&b=cpi-core&country=USA` (indicator comparison)

URLs are stable. Compare-2 views are citable.

## What is intentionally out of scope

- **Compare-3 / Compare-N**: use Indicator small-multiples or Scoreboard view.
- **Cross-type compare** (country vs scenario): not meaningful; use linkbacks.
- **Custom y-axis transforms per side** (log vs linear differently): forces incomparability; if needed, both sides switch together.
- **Annotation overlay across sides**: too noisy. Annotations stay per-side.
- **Compare-2 of forecasts at different vintages from the same record**: that is the vintage diff view inside the Forecast page (L126), not a side-by-side.

## What this loop produced

- Compare-2 = side-by-side, two records of the same type. Same-type only.
- Layout pattern: mirror with shared chrome + diff strip below.
- Shared controls (indicator, horizon, vintage, overlay, sync axes) apply to both sides.
- Diff strip at the bottom does the synthesis arithmetic.
- Sync-axes default: ON for level indicators, OFF for indices.
- Swap sides via `s` keystroke.
- Inline picker for second-side selection from a record page.
- Mobile collapses to tab-stack with diff strip always visible.
- URL: `/compare?a=...&b=...&[indicator,horizon,vintage,country]`.
- Compare-3 / cross-type compare explicitly out of scope.

## What comes next

- **L130** designs Watchlist (suggestions in the picker draw from watchlist).
- **L133** designs Scoreboard view (the N-way alternative).
- **L143** designs the print export; Compare-2 prints as two-up landscape.
- **L159** designs the forecast-diff view (today vs last-week vs WEO).
- **L244** prototypes Compare-2 in code.

## Related

- [[L121-information-architecture]] — /compare URL space
- [[L124-indicator-page]] — N-way alternative
- [[L128-search-command-bar]] — `> compare` invocation
- [[L130-watchlist-ux]] — suggestion source for compare picker
- [[L143-print-tearsheet]] — print version of compare
- [[L159-forecast-diff-view]] — within-record vintage diff
