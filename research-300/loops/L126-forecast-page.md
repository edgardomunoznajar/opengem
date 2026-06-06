---
loop: 126
phase: 3
title: Forecast Page — Structure and Eight Layout Candidates
date: 2026-06-06
status: decided
---

# L126 — Forecast Page: Structure + Eight Candidates

**Loop**: 126 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design `/f/{indicator}/{iso3}/{horizon}`. Must support:
1. P10/P50/P90 bands (the headline chart).
2. Consensus overlay (WEO, OECD, FRB SEP, ECB SPF, Cleveland, GDPNow as appropriate).
3. Vintage rewind (slider across vintages).
4. Model card link.
5. Miss log (per-vintage miss with diagnostic notes).

Eight candidate layouts. Pick one.

The Forecast page is the most-frequently-cited page on the dashboard. It is what an analyst opens to defend a number in a meeting. It is the page the API returns as the canonical record for a forecast. It is what the MCP server serves. The page must be print-grade.

## Candidate A — "Big chart, small footnotes"

```
+--------------------------------------------------------------------------+
| Header                                                                   |
+--------------------------------------------------------------------------+
| Big chart (80% of fold)                                                  |
| P10/P50/P90 bands, consensus overlay, history + horizon                 |
+--------------------------------------------------------------------------+
| Vintage slider · Model card link · Miss log link below                |
+--------------------------------------------------------------------------+
```

## Candidate B — "Chart + miss log + model card"

```
+--------------------------------------------------------------------------+
| Header                                                                   |
+--------------------------------------------------------------------------+
| LEFT (66%)                              | RIGHT (33%)                    |
| Chart with bands + overlay              | Miss log (per-vintage)        |
| Vintage slider below                    | Model card summary              |
|                                          | Compare button                  |
+--------------------------------------------------------------------------+
```

## Candidate C — "Tabbed chart + history"

```
+--------------------------------------------------------------------------+
| Tabs: Chart | History | Calibration | Methodology | Miss log              |
+--------------------------------------------------------------------------+
| selected tab content fills below                                        |
+--------------------------------------------------------------------------+
```

## Candidate D — "Print tearsheet"

```
+--------------------------------------------------------------------------+
| Header (large, brand-prominent)                                          |
+--------------------------------------------------------------------------+
| Chart                                                                    |
+--------------------------------------------------------------------------+
| 4-quadrant footnote: methodology + miss log + consensus + sources       |
+--------------------------------------------------------------------------+
```

## Candidate E — "Headline + chart + drilldown"

```
+--------------------------------------------------------------------------+
| HEADLINE STRIP                                                           |
| P50: 2.6%  band: 1.9%-3.4%  consensus: 2.8%  miss: -0.4pp avg            |
| vintage: 2026-06-02  horizon: 1Q (Aug 2026)                              |
+--------------------------------------------------------------------------+
| MAIN CHART                                                               |
| historical line + P10/P50/P90 forecast bands                           |
| consensus dots at horizon (WEO / OECD / FRB SEP / Cleveland)            |
| vertical line at vintage date                                            |
| event annotations on x-axis                                              |
+--------------------------------------------------------------------------+
| VINTAGE REWIND BAR                                                       |
| [<──── slider ────>] [step back][step forward][play]                     |
+--------------------------------------------------------------------------+
| LEFT (50%)                              | RIGHT (50%)                    |
| MISS LOG                                | MODEL CARD SUMMARY              |
| last 8 vintages with realized values   | model: L3-BMA (5 sub-models)   |
| diagnostic notes                        | weights table                   |
| calibration plot mini                   | track record: CRPS, PIT, bias   |
|                                          | last revision date              |
+--------------------------------------------------------------------------+
| [Full model card] [Replay-and-diff] [API] [Cite] [Subscribe] [Embed]   |
+--------------------------------------------------------------------------+
```

## Candidate F — "Two charts side-by-side"

```
+--------------------------------------------------------------------------+
| Header                                                                   |
+--------------------------------------------------------------------------+
| LEFT (50%): chart at current vintage     | RIGHT (50%): chart at prior   |
| with bands + overlay                     | vintage with bands + overlay  |
+--------------------------------------------------------------------------+
| Vintage slider controls both             |                                |
+--------------------------------------------------------------------------+
| Miss log + model card link below                                       |
+--------------------------------------------------------------------------+
```

## Candidate G — "Calibration-first"

```
+--------------------------------------------------------------------------+
| Header                                                                   |
+--------------------------------------------------------------------------+
| Calibration plot (P-P plot at top, very prominent)                     |
+--------------------------------------------------------------------------+
| Chart with bands below                                                  |
+--------------------------------------------------------------------------+
| Miss log + model card link                                              |
+--------------------------------------------------------------------------+
```

## Candidate H — "Stacked panels"

```
+--------------------------------------------------------------------------+
| Header                                                                   |
+--------------------------------------------------------------------------+
| Panel 1: chart with bands                                                |
| Panel 2: consensus overlay (this vintage vs latest WEO, OECD, etc.)    |
| Panel 3: vintage history (small-multiples: each vintage's bands)        |
| Panel 4: miss log table                                                  |
| Panel 5: model card summary                                              |
+--------------------------------------------------------------------------+
```

## The decision — Candidate E

Pick **E (Headline + Chart + Drilldown)**. It is the cleanest expression of "the forecast is the page" with all required elements present and visible.

Final spec:

```
+--------------------------------------------------------------------------+
| OPENGEM > Forecasts > US · CPI YoY · 1Q ahead                            |
| /f/cpi-yoy/USA/1Q  ·  vintage 2026-06-02                                 |
+--------------------------------------------------------------------------+
| HEADLINE                                                                 |
|                                                                          |
| US CPI YoY · 1Q ahead (Aug 2026 release)                                |
|                                                                          |
| P50    2.6%        P10-P90 band   1.9% — 3.4%                            |
| Last vintage P50  2.7%   (revision -0.1pp)                              |
| Consensus average  2.8%   (OPENGEM -0.2pp)                              |
|   WEO Apr 2026     2.8%                                                  |
|   OECD May 2026    2.7%                                                  |
|   FRB SEP Jun 2026 2.6%   (OPENGEM = SEP)                                |
|   Cleveland Now    2.9%   (OPENGEM -0.3pp)                               |
|                                                                          |
| Calibration to date (last 24 vintages)                                  |
|   CRPS 0.84   PIT 0.78   Bias -0.04   MAE 0.31                          |
|                                                                          |
+--------------------------------------------------------------------------+
| MAIN CHART                                                               |
|                                                                          |
|  4.5┤                                                                     |
|  4.0┤      ╲                                                              |
|  3.5┤       ╲___                                                          |
|  3.0┤           ╲___        ┌─~~~~~ P90                                   |
|  2.5┤               ╲ ─ ─ ─ │                                            |
|  2.0┤                       │  ─~~~ P50                                   |
|  1.5┤                       └ ─~~~ P10                                    |
|     └────────────────────────┼────────────────────────                    |
|     2023        2024        2025        2026        2027                  |
|                              ↑ vintage 2026-06-02                         |
|                                                                          |
| event annotations (small text under x-axis):                            |
|   2024-03  Fed first cut · 2025-01  Trump tariffs · 2026-04  WEO Spring   |
|                                                                          |
| consensus dots at forecast horizon (Aug 2026):                          |
|   ● WEO 2.8   ● OECD 2.7   ● FRB SEP 2.6   ● Cleveland 2.9               |
+--------------------------------------------------------------------------+
| VINTAGE REWIND                                                           |
| [<──────────────  slider  ──────────────>]   [play ▶] [step ⏮ ⏭]         |
| 2024-06 ░ 2024-12 ░ 2025-06 ░ 2025-12 ░ 2026-06                          |
+--------------------------------------------------------------------------+
| MISS LOG (last 8 vintages)         | MODEL CARD SUMMARY                  |
|                                     |                                     |
| 2026-03  P50 3.1  actual 3.4  +0.3  | Model: L3-BMA (5 sub-models)        |
| 2025-12  P50 2.7  actual 2.9  +0.2  |                                     |
| 2025-09  P50 3.4  actual 3.1  -0.3  |  AR(p)     w=0.12                   |
| 2025-06  P50 3.0  actual 3.2  +0.2  |  BVAR      w=0.31                   |
| 2025-03  P50 2.8  actual 2.6  -0.2  |  DFM       w=0.28                   |
| 2024-12  P50 2.5  actual 2.4  -0.1  |  RF        w=0.19                   |
| 2024-09  P50 2.3  actual 2.6  +0.3  |  NHITS     w=0.10                   |
| 2024-06  P50 2.0  actual 2.4  +0.4  |                                     |
|                                     | Reproducibility:                    |
| Mini calibration plot               |  commit  abc1234 · 2026-06-02      |
| (P-P plot 80x80)                    |  container  opengem:0.4.1           |
|                                     |  data lockfile  L1f2a8b              |
|                                     | [replay-and-diff →]                 |
+--------------------------------------------------------------------------+
| [Full model card] [Backtest data] [API] [Cite] [Subscribe alerts]      |
| [Embed]                                                                |
+--------------------------------------------------------------------------+
```

## Why E (and not the others)

**A (big chart, small footnotes) loses** because the forecast page is the trust page. The reader has to see calibration numbers, miss log, consensus comparison — *immediately*. Footnotes-below-the-chart pushes them out of frame.

**B (chart + miss log right rail) is close** to E. The difference is that B does not surface the vintage rewind prominently. E gives vintage rewind its own dedicated horizontal strip between chart and miss-log because rewind is the defining feature of an OPENGEM forecast page; it is the operationalization of "every forecast is dated."

**C (tabs) hides the miss log and model card.** Both must be immediately visible to anchor trust.

**D (print tearsheet) is the right pattern for the print export (L143), not the screen.** Online, four equally-weighted quadrants below the chart are too symmetric — the user does not know where to look first.

**E (headline + chart + drilldown) wins** because it encodes the editorial: headline numbers (the lede) → chart with bands and overlay (the evidence) → vintage rewind (the receipts) → miss log + model card (the audit trail). The page reads top to bottom as a single argument.

**F (two charts side-by-side)** is too clever. The user wants to see the forecast first, and rewind to compare *only on demand*. F shows the current vintage and the previous vintage simultaneously, which fragments attention. Vintage rewind (the E pattern) is more honest: one chart, the user controls when to rewind.

**G (calibration-first)** is wrong-priority. Calibration is the trust anchor, but the user wants to see "what does OPENGEM say" before they see "how good has OPENGEM been." E puts the headline number first (with calibration as a sub-line in the headline) and the chart second; G inverts this and feels like a methodology page rather than a forecast page.

**H (stacked panels) leaks the same problem as B (long scroll, no editorial weighting).** Each panel is equal-weighted; the user does not know which one matters most. E gives the chart 50% of vertical space and the miss log + model card 25% combined, which encodes the weighting.

## The headline strip

The headline is dense by design. P50, the band, the previous vintage's P50 (to show revision direction), the consensus average + per-source breakdown, and the calibration scorecard. This is the analyst's printable record of "what OPENGEM says today."

The consensus average is bolded; per-source breakdown is shown below in monospace for tabular comparison. Each consensus source links to its own vintage record (so the user can verify OPENGEM's read of WEO is accurate).

The calibration scorecard shows CRPS, PIT, Bias, MAE over the last 24 vintages. These four metrics give the analyst what they need to defend the forecast. The full track record is one click away (per L134).

## The main chart

The chart shows the historical series (solid line) for ~3-5 years, then the forecast (P10/P50/P90 shaded bands) extending to the horizon. A vertical dashed line marks the vintage date. Event annotations sit just below the x-axis (small font) — major shocks, releases, policy moves — so the chart reads as "here's what happened and here's what OPENGEM thinks will happen next."

Consensus dots at the horizon are small filled circles with source labels on hover. They cluster around OPENGEM's P50 if OPENGEM is consensus-aligned, or scatter visibly if OPENGEM is contrarian.

The chart is interactive — hover any point on the historical line for value + date; hover any forecast point for P10/P50/P90 at that quantile. Hovering the consensus dot shows source + vintage + value.

## Vintage rewind

The vintage rewind slider scrolls through every vintage of this forecast — back to inception. Sliding back updates the chart: the forecast bands shift to what was thought at that vintage, the consensus dots shift to what consensus was at that vintage, the historical line truncates at the vintage date.

The "play" button animates the slider at 500ms/vintage, showing the evolution of OPENGEM's view over time. This is the most powerful demo move on the dashboard. It is what the YouTuber will record in their video.

Vintage tick marks on the slider align to major release dates (WEO Apr/Oct, OECD May/Nov, monthly OPENGEM vintages).

## The miss log

The miss log is a table: vintage date, P50 forecast, actual realized value, miss (signed), and an optional diagnostic note. The 8 most recent vintages are shown. The full miss log is one click away.

The miss log is what makes the dashboard a Ledger. Every published forecast has a row. There is no rewriting, no retroactive deletion. If a forecast was wrong, the row stays.

The mini calibration plot (P-P plot, 80x80 pixels) sits below the miss log table — a small but always-visible reminder of calibration health.

## The model card summary

Right column. Lists the model architecture, sub-model weights (current), and reproducibility envelope (commit hash, container digest, data lockfile). One click to the full model card.

The reproducibility line is OPENGEM's hardest commitment: every forecast can be re-run from the listed envelope. Click [replay-and-diff] to launch a CI job that re-runs the forecast and shows any diff. This is the operationalization of "the dashboard publishes its mistakes."

## What this loop produced

- Eight candidate forecast-page layouts as ASCII wireframes.
- Decision: Candidate E (Headline + Chart + Drilldown).
- Headline shows P50, band, previous vintage, full consensus breakdown, calibration scorecard.
- Vintage rewind has dedicated horizontal strip with play/step controls.
- Miss log + mini P-P calibration plot in the left drilldown column.
- Model card + reproducibility envelope in the right drilldown column.
- "Replay-and-diff" button operationalizes the reproducibility claim.

## What comes next

- **L132** designs the methodology drawer (open from the model card link).
- **L133** designs the forecast leaderboard (compare OPENGEM's model to alternates).
- **L134** designs the track-record page (full calibration plot).
- **L143** designs the print tearsheet (this page → PDF).
- **L144** designs the embed widget (this page → iframe).
- **L182** designs forecast vintage lineage in code.

## Related

- [[L121-information-architecture]] — /f/{indicator}/{iso3}/{horizon} URL space
- [[L123-country-page]] — country page's forecast chart drills here
- [[L132-provenance-drawer]] — model card slide-out
- [[L134-track-record-page]] — full calibration drill
- [[L143-print-tearsheet]] — print version of this page
- [[L186-reproducibility-envelope]] — replay-and-diff implementation
