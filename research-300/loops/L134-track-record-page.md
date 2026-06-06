---
loop: 134
phase: 3
title: Track-Record Page (per indicator × per horizon)
date: 2026-06-06
status: decided
---

# L134 — Track-Record Page

**Loop**: 134 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design `/ledger/{indicator}/{horizon}` — the per-cell track record page. Calibration plot. Hit-rate table. Per-vintage detail. This is the page you cite when defending OPENGEM as a serious forecaster.

## The structure

The track-record page is the single-cell deep dive that the leaderboard (L133) drills into. Where the leaderboard compares many forecasters across one metric, the track-record page shows everything about *one* cell — OPENGEM's full performance history at the (indicator, horizon) granularity, with country roll-up below.

Per-country breakouts live as a tab strip; default tab is "All Tier-V."

```
+--------------------------------------------------------------------------+
| OPENGEM > Ledger > CPI YoY · 4Q ahead                                    |
| /ledger/cpi-yoy/4Q                                                       |
+--------------------------------------------------------------------------+
| HEADLINE                                                                 |
|                                                                          |
| CPI YoY · 4 quarters ahead                                              |
| Coverage: 26 Tier-V countries · 32 vintages (2024-06 → 2026-06)         |
|                                                                          |
| Aggregate calibration to date:                                          |
|   CRPS    0.84   PASS (vs WEO 0.91, vs OECD EO 0.92, vs RW 1.42)        |
|   PIT     0.78   PASS (threshold 0.70)                                   |
|   Bias   -0.04   PASS                                                    |
|   MAE     0.31   PASS                                                    |
|   Coverage rate at P10-P90: 81% (target 80%)                            |
|                                                                          |
| V&V cell status: GREEN (all 5 cells PASS)                                |
+--------------------------------------------------------------------------+
| CALIBRATION PLOT (full-width)                                            |
|                                                                          |
|   1.0 ┤                                                                  |
|       │                                       ╱                          |
|   0.8 ┤                                  ●  ╱                            |
|       │                              ●   ╱                               |
|   0.6 ┤                          ●    ╱                                  |
|       │                      ●      ╱                                    |
|   0.4 ┤                   ●       ╱                                      |
|       │                ●        ╱                                        |
|   0.2 ┤             ●         ╱                                          |
|       │          ●          ╱                                            |
|       └─────────●─────────╱─────────────────                              |
|        0.0   0.2   0.4   0.6   0.8   1.0                                 |
|        nominal quantile                                                  |
|                                                                          |
|  ● OPENGEM L3-BMA  (PIT 0.78)                                           |
|  ○ WEO  (PIT 0.68 — over-confident at upper tail)                       |
|  ─ Perfect calibration (diagonal)                                       |
|                                                                          |
|  KS statistic vs diagonal:   OPENGEM 0.04 (PASS), WEO 0.12 (BORDERLINE)|
+--------------------------------------------------------------------------+
| HIT-RATE TABLE (per country)                                            |
|                                                                          |
| Country  Vintages  CRPS  PIT  Bias   MAE  Hit%@P10-P90  Notes            |
|                                                                          |
| 🇺🇸 USA       32   0.84  0.78  -0.04  0.31      81%                       |
| 🇪🇺 EUR       32   0.79  0.81  -0.02  0.29      84%                       |
| 🇬🇧 GBR       32   0.91  0.74  +0.07  0.35      77%   ⚠ slight over-pred |
| 🇯🇵 JPN       32   0.62  0.85  -0.01  0.21      88%   excellent          |
| 🇨🇦 CAN       32   0.82  0.79  -0.03  0.30      82%                       |
| 🇦🇺 AUS       32   0.89  0.76  +0.04  0.33      79%                       |
| 🇩🇪 DEU       32   0.81  0.80  -0.02  0.30      83%                       |
| 🇫🇷 FRA       32   0.83  0.79  -0.03  0.31      82%                       |
| 🇮🇹 ITA       28   0.94  0.72  +0.08  0.36      74%   ⚠ over-pred         |
| 🇪🇸 ESP       28   0.85  0.78  +0.04  0.32      80%                       |
| 🇲🇽 MEX       24   1.02  0.69  +0.11  0.41      71%   ⚠ PIT under thresh |
| 🇧🇷 BRA       24   1.18  0.65  +0.18  0.49      66%   ⚠ FAIL PIT          |
| 🇰🇷 KOR       24   0.77  0.81  -0.02  0.28      84%                       |
| 🇮🇩 IDN       24   1.04  0.68  +0.12  0.42      70%   ⚠ borderline       |
| ...                                                                       |
| (sortable by any column)                                                 |
+--------------------------------------------------------------------------+
| PER-VINTAGE TIMELINE                                                     |
|                                                                          |
| Scatter plot: x = vintage date, y = miss (signed)                       |
| color by country, size by absolute miss                                  |
| zero line bolded                                                        |
| trailing 12-vintage mean as a smoothed line                             |
|                                                                          |
| Annotations at major release dates (WEO Apr/Oct, OECD May/Nov, etc.)    |
+--------------------------------------------------------------------------+
| MISS LOG (sortable, filterable)                                          |
|                                                                          |
| Vintage     Country  P50    Actual  Miss   Note                          |
|                                                                          |
| 2026-03-02  USA      3.1    3.4     +0.3   missed Apr-May energy rebound|
| 2026-03-02  EUR      2.6    2.5     -0.1                                  |
| 2025-12-02  USA      2.7    2.9     +0.2                                  |
| 2025-12-02  EUR      2.5    2.4     -0.1                                  |
| 2025-09-02  USA      3.4    3.1     -0.3   over-pred — China dis-inf.   |
| 2025-09-02  BRA      4.2    5.8     +1.6   large miss — see post-mortem |
| ...                                                                       |
|                                                                          |
| [Full miss log →]                                                        |
+--------------------------------------------------------------------------+
| FAILURE ANALYSIS                                                         |
|                                                                          |
| Pre-mortem analyses for the 3 largest misses:                           |
|                                                                          |
|   1. BRA 2025-09 vintage (+1.6pp)  → [post-mortem PM-014]              |
|   2. ITA 2025-06 vintage (+1.2pp)  → [post-mortem PM-011]              |
|   3. MEX 2024-12 vintage (+0.9pp)  → [post-mortem PM-008]              |
|                                                                          |
| Each post-mortem follows the same template (R200 / L298):                |
|   - What we forecast                                                    |
|   - What happened                                                        |
|   - Why the model missed                                                 |
|   - What changed in the next vintage                                     |
|   - Open question for V&V                                                |
+--------------------------------------------------------------------------+
| FOOTER ACTIONS                                                          |
| [Compare to WEO →] [Open per-country drilldown] [API] [Cite] [Embed]    |
| [Subscribe: alert on CRPS deterioration] [Subscribe: monthly digest]    |
+--------------------------------------------------------------------------+
```

## Why this structure

The page answers three questions in three layers:

1. **"Is OPENGEM calibrated?"** → headline + calibration plot. The headline says PASS/FAIL on the V&V cells, the plot shows how close OPENGEM's predicted quantiles match actual realized quantiles.

2. **"Where does OPENGEM win / lose?"** → hit-rate table. Per-country breakout shows which countries OPENGEM forecasts well and which ones drag down the aggregate. The honest table includes ⚠ marks for cells that fail PIT or have abnormal bias.

3. **"What happened on the bad days?"** → miss log + failure analysis. Every miss is in the log. The biggest misses link to public post-mortems. There is no hiding.

## The calibration plot

The P-P plot is the most powerful single visualization on the dashboard. It shows, for every probability quantile p ∈ [0,1], how often the actual fell at or below the predicted p-quantile. A perfectly calibrated forecaster lies on the diagonal.

OPENGEM is overlaid against WEO (and optionally other forecasters via toggle) so the reader sees calibration *comparatively*, not just absolutely. WEO's documented over-confidence at the upper tail appears visually.

Below the plot, the KS statistic (Kolmogorov-Smirnov) gives a single-number summary of calibration deviation. Threshold: KS ≤ 0.05 = PASS, 0.05–0.10 = BORDERLINE, > 0.10 = FAIL.

## The hit-rate table

The hit-rate table is per-country. Each row: vintages-evaluated, CRPS, PIT, Bias, MAE, Hit% (the fraction of actuals that fell inside the P10-P90 band — should be ~80% by construction, with deviation flagged), and a notes column for editorial flags.

The notes column uses ⚠ for cells below threshold and a short reason. This is the table the LP screenshots into their internal memo. It must be clean, sortable, exportable.

## Per-vintage timeline

The scatter plot shows the time-trajectory of misses. The user can see, e.g., that OPENGEM's CPI 4Q forecasts had high variance in 2024 and tightened in 2025 (as the model learned).

Vertical annotation lines mark major institutional release dates (WEO Apr/Oct, OECD May/Nov) so the user can correlate OPENGEM's vintage shifts with consensus shifts.

## Miss log

Reverse-chronological, paginated, sortable by vintage / country / miss size. Each row links to the underlying forecast page (so the reader can verify the forecast and the actual).

Notes column has free-text editor comments where relevant. These are *not* defenses — they are diagnostic ("over-pred — China disinflation propagation faster than model assumed").

## Failure analysis (post-mortems)

The 3 largest misses get full public post-mortems. The post-mortem template (L298) is:
1. What we forecast.
2. What actually happened.
3. Why the model missed (diagnostic, model-grounded).
4. What changed in the next vintage (calibration response).
5. An open question for V&V (what we still don't fully understand).

Post-mortems live as `/ledger/post-mortems/PM-{NNN}`. They are permanent. They are dated. They are stamped with the same provenance drawer (L132) as forecasts.

This is the "publish our mistakes in the same place we published the original" promise.

## Sortability and filtering

All tables and the plot are filterable:
- By country.
- By vintage range.
- By miss size threshold.
- By PASS/FAIL status.

Filter state encodes into the URL so views are shareable.

## Aggregation rules

Aggregate calibration metrics (top of page) are computed across the union of (country, vintage) cells in the displayed scope. The aggregation is:
- **CRPS**: GDP-PPP-weighted mean across countries.
- **PIT**: pooled across all (country, vintage) realizations.
- **Bias / MAE**: simple mean across cells.
- **Coverage rate**: total actuals within P10-P90 / total actuals.

The aggregation methodology is documented in `/ledger/methodology` (L135 designs the methodology page).

## What this page is NOT

- **Not a per-vintage forecast page**. That is `/f/{indicator}/{iso3}/{horizon}/v/{vintage}` (L126).
- **Not a forecaster comparison**. That is the leaderboard (L133).
- **Not a methodology defense**. That is the methodology page (L135).
- **Not editorial commentary**. The notes column is diagnostic; the post-mortems are templated. There is no "OPENGEM is great" voice anywhere on this page.

## What this loop produced

- Page structure: headline → calibration plot → hit-rate table → per-vintage timeline → miss log → failure analysis.
- V&V cell status (GREEN / YELLOW / RED) at the headline based on CRPS / PIT / Bias / Coverage thresholds.
- P-P calibration plot with OPENGEM vs WEO overlay; KS statistic threshold.
- Hit-rate table per-country with ⚠ flags for failing cells.
- Per-vintage scatter timeline with institutional-release annotations.
- Miss log with diagnostic notes; the 3 largest misses get full post-mortems.
- Post-mortem template (5-section).
- Aggregation rules (GDP-PPP for CRPS, pooled for PIT, simple mean for Bias/MAE).
- Filterable + URL-encoded view state.
- Honest framing: ⚠ flags are surfaced, not hidden.

## What comes next

- **L135** designs the methodology page (V&V methodology in detail).
- **L185** designs the open backtest harness API.
- **L193** designs the calibration plot in detail (per-indicator).
- **L200** designs the dashboard-wide failure log page.
- **L298** designs the post-mortem template.

## Related

- [[L121-information-architecture]] — /ledger URL space
- [[L126-forecast-page]] — per-record miss log drilldown
- [[L132-provenance-drawer]] — full track record link from drawer
- [[L133-forecast-leaderboard]] — multi-forecaster comparison
- [[L135-methodology-page]] — V&V methodology
- [[L298-post-mortem-template]] — post-mortem format
