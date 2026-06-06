---
loop: 124
phase: 3
title: Indicator Page — Structure and Eight Layout Candidates
date: 2026-06-06
status: decided
---

# L124 — Indicator Page: Structure + Eight Candidates

**Loop**: 124 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design `/i/{indicator-slug}`. Must support:
1. Cross-country small-multiples (the headline view).
2. Vintage rewind.
3. Consensus overlay (WEO, OECD EO, FRB SEP, ECB SPF, Cleveland Fed Inflation Nowcast).
4. Forecast bands (P10/P50/P90).

Eight candidate layouts. Pick one.

The Indicator page is the inverse of the Country page. Country page = "everything about one country." Indicator page = "this one thing across all countries." It is the page a macro analyst lives in. The challenge is density without chaos.

## Candidate A — "Grid of small-multiples"

```
+--------------------------------------------------------------------------+
| Header: indicator name + definition + global aggregate                  |
+--------------------------------------------------------------------------+
| 5x6 grid of country sparklines (30 countries, ranked by latest reading) |
| each: flag, country, current value, sparkline, forecast extension      |
+--------------------------------------------------------------------------+
```

## Candidate B — "Single big chart, country toggles"

```
+--------------------------------------------------------------------------+
| Header                                                                   |
+--------------------------------------------------------------------------+
| Big chart (one country at a time, or multi-line)                       |
| with vintage slider, consensus overlay toggle, forecast band toggle    |
+--------------------------------------------------------------------------+
| Country picker (chips) and methodology drawer below                    |
+--------------------------------------------------------------------------+
```

## Candidate C — "Two pane: list + detail"

```
+--+-----------------------------------------------------------------------+
|  | Header                                                                |
|L +-----------------------------------------------------------------------+
|i | Selected country detail chart                                        |
|s | with bands, consensus, vintage                                       |
|t |                                                                       |
|  | Methodology + miss log + forecast diff below                         |
+--+-----------------------------------------------------------------------+
```

## Candidate D — "Heatmap of all countries × time"

```
+--------------------------------------------------------------------------+
| Header                                                                   |
+--------------------------------------------------------------------------+
| Y axis: countries (sorted)                                               |
| X axis: time (last 5 years + forecast horizon)                         |
| color: indicator value (semantic scale)                                |
| click any cell → time-series chart for that country opens below        |
+--------------------------------------------------------------------------+
```

## Candidate E — "Headline + Small-multiples + Drilldown"

```
+--------------------------------------------------------------------------+
| Header: indicator name + definition                                      |
| Big headline number: World aggregate (PPP-weighted)                    |
+--------------------------------------------------------------------------+
| Strip: P10/P50/P90 forecast for world aggregate, consensus comparison  |
+--------------------------------------------------------------------------+
| Small-multiples grid: 12 countries (G20 default, watchlist override)    |
| each panel: 5y series + 4q forecast band + consensus dot at horizon    |
| click panel → country×indicator drilldown opens to the right            |
+--------------------------------------------------------------------------+
| Drilldown panel (right side, conditional): selected country detail     |
| with vintage rewind slider, miss log, methodology link                  |
+--------------------------------------------------------------------------+
```

## Candidate F — "Time-series with country brushing"

```
+--------------------------------------------------------------------------+
| Header                                                                   |
+--------------------------------------------------------------------------+
| Single time-series chart with one line per country (multi-line)        |
| color by region or by indicator regime                                 |
| brushing on chart highlights country in lower table                    |
+--------------------------------------------------------------------------+
| Country table below                                                    |
+--------------------------------------------------------------------------+
```

## Candidate G — "Scoreboard-first"

```
+--------------------------------------------------------------------------+
| Header                                                                   |
+--------------------------------------------------------------------------+
| Sortable table (countries × columns)                                    |
| Columns: latest value, 1Q chg, YoY chg, P50 4Q, consensus 4Q, surprise|
| rows colored by current vs consensus deviation                         |
+--------------------------------------------------------------------------+
| Detail chart below for selected row                                    |
+--------------------------------------------------------------------------+
```

## Candidate H — "Two-row hero + multiples"

```
+--------------------------------------------------------------------------+
| Header: indicator name                                                   |
+--------------------------------------------------------------------------+
| Row 1 (hero): G7 small-multiples (7 countries inline)                  |
+--------------------------------------------------------------------------+
| Row 2: BRICS+ small-multiples (5-7 countries inline)                   |
+--------------------------------------------------------------------------+
| Row 3 (optional): EU-area, ASEAN, custom watchlist                      |
+--------------------------------------------------------------------------+
| Bottom: vintage rewind, consensus overlay, methodology link            |
+--------------------------------------------------------------------------+
```

## The decision — Candidate E

Pick **E (Headline + Small-multiples + Drilldown)** with the drilldown rendered as a right-side slide-out, not a below-the-fold panel.

Final spec:

```
+--------------------------------------------------------------------------+
| OPENGEM > Indicators > Consumer Price Index (YoY) · /i/cpi-yoy           |
+--------------------------------------------------------------------------+
| CPI year-over-year inflation                                            |
| Definition: percentage change in headline CPI vs 12 months ago         |
| Sources: BLS · BEA · ORDRA · ECB SDW · OECD · ONS · ABS · ...           |
|                                                                          |
| WORLD AGGREGATE (PPP-weighted)        4.1%  ▼0.2pp m/m                  |
| P50 4Q ahead                          3.6%  band 2.4% — 5.1%            |
| Consensus (WEO, OECD EO avg)          3.9%  OPENGEM is 0.3pp lower      |
+--------------------------------------------------------------------------+
| SMALL-MULTIPLES (default G20, editable to watchlist)                    |
|                                                                          |
| 🇺🇸 USA    2.9% ▼  ┄┄┄~~~ band                                            |
| 🇪🇺 EUR    2.4% ▼  ┄┄┄~~~ band                                            |
| 🇬🇧 GBR    3.1% ▼  ┄┄┄~~~ band                                            |
| 🇯🇵 JPN    2.7% ▲  ┄┄┄~~~ band                                            |
| 🇨🇳 CHN    0.4% ▲  ┄┄┄~~~ band                                            |
| 🇨🇦 CAN    2.7% ▼  ┄┄┄~~~ band                                            |
| 🇦🇺 AUS    3.4% ▼  ┄┄┄~~~ band                                            |
| 🇧🇷 BRA    4.2% ▲  ┄┄┄~~~ band                                            |
| 🇲🇽 MEX    4.6% ▲  ┄┄┄~~~ band                                            |
| 🇮🇳 IND    5.1% ▼  ┄┄┄~~~ band                                            |
| 🇰🇷 KOR    2.3% ▲  ┄┄┄~~~ band                                            |
| 🇮🇩 IDN    2.9% ▼  ┄┄┄~~~ band                                            |
| 🇿🇦 ZAF    5.6% ▲  ┄┄┄~~~ band                                            |
| 🇹🇷 TUR    37%  ▼  ┄┄┄~~~ band                                            |
| 🇦🇷 ARG    142% ▼  ┄┄┄~~~ band                                            |
| 🇷🇺 RUS    9.2% ▲  ┄┄┄~~~ band                                            |
| 🇸🇦 SAU    1.6% flat ┄┄┄~~~ band                                          |
| (G20 = 19+EU; up to 19 panels)                                          |
| each: 5y trailing line + 4q forecast band (P10-P90 shaded)              |
| consensus dot (WEO + OECD EO avg) at 4Q horizon                         |
+--------------------------------------------------------------------------+
| CONTROLS                                                                |
| [Vintage: 2026-06-06 ▼] [Horizon: 1Q | 4Q | 2Y]                         |
| [Consensus overlay: ON ▼ which: WEO | OECD | FRB | ECB SPF | Cleveland]|
| [Forecast band: P10/P50/P90 ▼]                                          |
| [View as: Small-mult ▼ | Scoreboard | Heatmap | Trend-line]             |
+--------------------------------------------------------------------------+
| Click panel → /c/{iso3}/cpi-yoy detail                                   |
| Click country row in scoreboard view → same                              |
+--------------------------------------------------------------------------+
```

The right-side drilldown drawer (slides in when a panel is clicked):

```
| 🇺🇸 USA · CPI YoY                                       [×]   |
|--------------------------------------------------------------|
| Latest reading: 2.9%   period: May 2026   source: BLS         |
| Released: 2026-06-12 (4 days ago)                             |
|                                                               |
| [zoom chart, full width, with bands and vintage slider]      |
|                                                               |
| FORECAST AT THIS HORIZON                                     |
| 1Q ahead (Aug 2026)   P50 2.6%   band 1.9% – 3.4%             |
| 4Q ahead (May 2027)   P50 2.4%   band 1.4% – 3.5%             |
|                                                               |
| CONSENSUS COMPARISON                                          |
| WEO (Apr 2026)        2.8%       OPENGEM −0.4pp               |
| OECD EO (Mar 2026)    2.7%       OPENGEM −0.3pp               |
| FRB SEP (Jun 2026)    2.6%       OPENGEM 0pp (match)          |
| Cleveland Nowcast     2.9%       OPENGEM 0pp (match)          |
|                                                               |
| VINTAGE REWIND                                                |
| [<──── timeline slider ────────────>]                         |
| 2024-06   2024-12   2025-06   2025-12   2026-06               |
|                                                               |
| MISS LOG (last 4 vintages)                                    |
| 2026-03 vintage: forecast 3.1, actual 3.4, miss +0.3          |
| 2025-12 vintage: forecast 2.7, actual 2.9, miss +0.2          |
| 2025-09 vintage: forecast 3.4, actual 3.1, miss -0.3          |
| 2025-06 vintage: forecast 3.0, actual 3.2, miss +0.2          |
|                                                               |
| [Model card →] [Full track record →] [Replay →] [Cite →]      |
```

## Why E (and not the others)

**A loses on uniformity.** A 30-panel grid says nothing about importance. The user's eye does not know where to land. Defaulting to G20 (≤19 panels) is the right size — small enough to see structure, large enough to cover macro coverage.

**B loses on the cross-country requirement.** A single big chart with multi-line overlays hides the per-country forecast band, which is the whole point of OPENGEM. Bands collapse if you overlay 20 lines.

**C loses on first-impression density.** Two panes with a list-on-the-left is the pattern of an admin tool (Stripe Dashboard, Notion). It is the right shape for an editor, the wrong shape for a reader. The reader wants to see the world at a glance and drill on demand. C makes you click first.

**D (heatmap) is the second-best option.** A country × time heatmap shows structure powerfully — you can see inflation regimes propagate across countries. The problem is that heatmaps lose forecast bands; you cannot encode P10/P50/P90 in a single colored cell. Heatmap stays as a *view-mode toggle* (the "Heatmap" button in the controls strip), not as the default.

**E wins** because it preserves both density (small-multiples show 19 countries simultaneously) and depth (each panel is rich enough to encode bands + consensus dot). The drilldown is on-demand, so the page never feels heavy. The headline (world aggregate, top of page) anchors the reader before they explore the panels.

**F (multi-line) is the FRED pattern** and is the right tool for *time-evolution-of-one-metric-across-a-few-countries* (e.g., EZ inflation: Germany, France, Italy, Spain). Multi-line stays as a view-mode toggle.

**G (scoreboard) is the right view for the analyst who wants to sort and rank** — show me the 10 countries with the largest forecast revision today. Scoreboard stays as a view-mode toggle.

**H (G7 + BRICS+ rows) is a refinement of E** — a specific arrangement of small-multiples. The problem is that "G7" and "BRICS+" are political groupings, not economic ones (e.g., Australia and Korea are macro-relevant and don't fit either). E's default-G20 (with watchlist override) is more honest.

## Vintage rewind

The vintage rewind slider lives in the controls strip (always visible) and in the drilldown drawer (per-country). Sliding it backward in time updates *every panel simultaneously* — both the value and the forecast band redraw at the previous vintage. This is OPENGEM's killer feature for this page: see what we thought 12 months ago vs what we think now.

The slider has tick marks at major release dates (WEO Apr, OECD Sep, etc.) so the user can step through institutional vintages.

## Consensus overlay

Consensus is computed as the simple average of available institutional forecasts at the same horizon, color-coded per source. Overlay options:
- WEO (IMF World Economic Outlook, Apr + Oct vintages)
- OECD EO (Economic Outlook, May + Nov vintages)
- FRB SEP (Federal Reserve Summary of Economic Projections, US only)
- ECB SPF (Survey of Professional Forecasters, EZ only)
- Cleveland Fed Nowcast (inflation only)
- Atlanta GDPNow (US GDP nowcast only)

When the active overlay is irrelevant to a panel (e.g., FRB SEP shown for Brazil), the dot is suppressed.

## Forecast bands

Default is P10/P50/P90 (per L188). The user can toggle to P25/P50/P75 (a tighter view) or the full P5/P25/P50/P75/P95 fan. The P50 line is always solid; the bands are shaded with progressively lower opacity for wider tails.

When the panel is too narrow (≤120px wide), only P50 + a single shaded P10-P90 envelope is drawn (no inner P25/P75 lines). Density gracefully degrades.

## What this loop produced

- Eight candidate indicator-page layouts as ASCII wireframes.
- Decision: Candidate E (Headline + Small-multiples + Drilldown drawer).
- Default panel set: G20 (≤19 panels) with watchlist override.
- View-mode toggles preserve Heatmap (D), Scoreboard (G), Trend-line (F) as alternatives.
- Vintage rewind as a synchronized slider across all panels.
- Consensus overlay sources enumerated (WEO, OECD EO, FRB SEP, ECB SPF, Cleveland, GDPNow).
- Forecast band gracefully degrades for narrow panels.

## What comes next

- **L126** designs the Forecast page (the per-record deep-dive).
- **L132** designs the methodology drawer in detail.
- **L162** designs the indicator card grid for browsing.
- **L173** designs the vintage time-machine for animating across vintages.
- **L195** designs the forecast UI with bands and consensus overlay in code.

## Related

- [[L121-information-architecture]] — /i/{indicator-slug} URL space
- [[L123-country-page]] — country page is the inverse view
- [[L126-forecast-page]] — record drilldown
- [[L132-provenance-drawer]] — methodology slide-out
- [[L173-vintage-time-machine]] — vintage rewind UX
- [[L188-bands-percentile-choice]] — P10/P50/P90 default rationale
