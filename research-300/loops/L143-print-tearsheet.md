---
loop: 143
phase: 3
title: Print / PDF Tearsheet Design
date: 2026-06-06
status: decided
---

# L143 — Print / PDF Tearsheet Design

**Loop**: 143 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design a one-page tearsheet for: a country, an indicator, a scenario.

Print is the offline distribution channel. The tearsheet lives in:
- Email attachments (briefing summaries).
- Substack posts (embedded as a static image).
- PDF appendix in a board memo.
- Hand-out at a conference panel.
- Print pinned to an analyst's office wall.

The constraint: one page, machine-printable on US Letter / A4, brand-recognizable as OPENGEM, readable from 18 inches away in 11pt body.

## Design rules

### Format

- US Letter (8.5" × 11") landscape orientation by default. A4 secondary.
- Margins: 0.5" all sides.
- Header band: 0.8" tall, brand-tinted (terminal-orange theme; per L145 default).
- Footer band: 0.4" tall, with citation + URL + vintage stamp.

### Why landscape

Landscape gives the chart room. The country page tearsheet is dominated by a forecast chart; landscape lets that chart stretch to ~9 inches wide. Portrait would make the chart cramped and the right rail wide.

### Typography

- Headline: 24pt Inter or Söhne, bold.
- Section heads: 14pt Inter, bold, uppercase, letter-spaced.
- Body: 11pt Inter, regular.
- Captions: 9pt Inter, regular, secondary-color.
- Tabular numbers throughout (lining figures).
- Monospace for data values: JetBrains Mono or IBM Plex Mono at the same point size.

### Color

- Brand: terminal-orange (#FF6F00) for the brand band + accent lines.
- Body: near-black (#1A1A1A) on near-white (#FAFAFA).
- Bands: P10/P50/P90 use three opacity tiers of the brand color (10%, 30%, solid for P50 line).
- Consensus dots: gray-tone variants by source (no extra colors).

### Watermark / brand

Top-right of the header band: small OPENGEM wordmark + globe icon. Bottom-left of footer: "OPENGEM World Dashboard · CC-BY-4.0".

## The Country Tearsheet

```
+--------------------------------------------------------------------------+
| OPENGEM · UNITED STATES                                  vintage 2026-06-02
+--------------------------------------------------------------------------+
| HEADLINE INDICATORS                                                       |
| GDP YoY   2.4%  ▲0.1            CPI YoY    2.9%  ▼0.2                    |
| Unemp     3.7%  ▲0.1            Policy Rate 5.25% flat                   |
| Population 335M  GDP $27.8T  P50 1Q-ahead growth 1.9%                   |
+--------------------------------------------------------------------------+
|                                                                          |
|  FORECAST: US REAL GDP YoY                                                |
|                                                                          |
|  3.5┤                                                                     |
|  3.0┤                                                                     |
|  2.5┤                       ╱─────                                       |
|  2.0┤              ╱──────╱        ─~~~~ P90                              |
|  1.5┤      ╱──────╱                ─~~~ P50                              |
|  1.0┤                              ─~~~ P10                              |
|     └────────────────────────────                                        |
|     2022    2023    2024    2025    2026    2027                          |
|     ╳ vintage 2026-06-02                                                  |
|                                                                          |
|     consensus dots:                                                       |
|       ● WEO 2.0  ● OECD 2.1  ● FRB SEP 2.2                                |
|                                                                          |
+--------------------------------------------------------------------------+
| SITUATION                       SCENARIOS TRIGGERED FOR USA               |
|                                                                          |
| Recession (Bauer-Mertens)        Trade-LATAM      P=0.62                  |
|   P50    34%                     Red-Sea-#4      P=0.78                  |
|   band   18%-52%                 Oil-shock       P=0.34                  |
|                                  EU-rate-hold    P=0.55                  |
| GPR (Caldara-Iacoviello)                                                  |
|   Current     89                                                          |
|   30d Δ       +12                EVENT FEED (last 14d, 12 events)        |
|                                                                          |
| GSCPI exposure                   2026-06-05  OPEC+ cut                   |
|   Level       0.18                2026-06-04  US NFP +185k                |
|   30d Δ       +0.04               2026-06-03  Yellen visits Beijing       |
|                                  2026-06-02  BEA Q1 +1.3% (rev)          |
| Surprise idx                     2026-06-01  10y -3bp                     |
|   Current     +0.4                                                         |
|   30d Δ       +0.2                                                         |
+--------------------------------------------------------------------------+
| METHODOLOGY      Forecast: L3-BMA over 5 sub-models; replay envelope:    |
|                  commit abc1234 · container opengem:0.4.1 · seed 42       |
|                                                                          |
| TRACK RECORD     CPI 4Q: CRPS 0.84 (vs WEO 0.91)                          |
| (trailing 24Q)   GDP 4Q: CRPS 0.84 (vs WEO 0.91)                          |
|                  Recession: AUC 0.79 (vs Bauer-Mertens 0.69)              |
|                                                                          |
+--------------------------------------------------------------------------+
| OPENGEM World Dashboard · CC-BY-4.0 · opengem.world/c/USA · 2026-06-02   |
| Cite: urn:opengem:country:USA:2026-06-02                                  |
+--------------------------------------------------------------------------+
```

The country tearsheet is the densest layout. It has:
1. Headline indicators band (top).
2. One big chart (GDP P10/P50/P90 with consensus dots).
3. Situation + scenarios + events three-column band (middle).
4. Methodology + track record band (bottom).
5. Citation footer.

The user gets the country in one page. Print this and pin it.

## The Indicator Tearsheet

```
+--------------------------------------------------------------------------+
| OPENGEM · CPI YoY · WORLD                              vintage 2026-06-02
+--------------------------------------------------------------------------+
| WORLD AGGREGATE (PPP-weighted)                                            |
| 4.1% ▼0.2pp m/m  · P50 4Q-ahead 3.6%  band 2.4-5.1                       |
| Consensus 3.9% (WEO + OECD avg)  · OPENGEM -0.3pp                         |
+--------------------------------------------------------------------------+
| SMALL-MULTIPLES — 12 countries (G7 + BRICS+, sorted by latest reading)   |
|                                                                          |
|  🇹🇷 TUR 37%  ━━━━╲━━ ░░░░~      🇺🇸 USA 2.9% ━━ ━━╲━ ░░░░~              |
|  🇦🇷 ARG 142% ━━━━╲━━ ░░░░~      🇨🇦 CAN 2.7% ━━ ━━╲━ ░░░░~              |
|  🇷🇺 RUS 9.2%━━━ ━━╱━ ░░░░~      🇪🇺 EUR 2.4% ━━ ━━╲━ ░░░░~              |
|  🇿🇦 ZAF 5.6%━━━ ━━╱━ ░░░░~      🇰🇷 KOR 2.3% ━━ ━━╱━ ░░░░~              |
|  🇮🇳 IND 5.1%━━━ ━━╲━ ░░░░~      🇯🇵 JPN 2.7% ━━ ━━╱━ ░░░░~              |
|  🇲🇽 MEX 4.6%━━━ ━━╱━ ░░░░~      🇨🇳 CHN 0.4% ━━ ━━╱━ ░░░░~              |
|                                                                          |
|  each: 5y line + 4Q forecast band (P10-P90 shaded) + consensus dot       |
+--------------------------------------------------------------------------+
| TRACK RECORD                    LEADERBOARD (CPI 4Q ahead, trailing 24Q)|
|                                                                          |
| Aggregate calibration            1. OPENGEM L3-BMA  CRPS 0.84            |
|   CRPS    0.84  PASS              2. FRB SEP        CRPS 0.87            |
|   PIT     0.78  PASS              3. Cleveland Now  CRPS 0.88            |
|   Bias   -0.04                    4. WEO            CRPS 0.91            |
|   Coverage P10-P90: 81%            5. OECD EO       CRPS 0.92            |
|                                  6. ECB SPF        CRPS 0.95            |
| V&V cell status: GREEN            7. AR(1) baseline CRPS 1.42            |
|                                  8. Random walk    CRPS 1.51            |
+--------------------------------------------------------------------------+
| METHODOLOGY  L3-BMA over 5 sub-models (AR, BVAR, DFM, RF, NHITS).        |
|              CRPS computed on density forecast; PIT on uniform IT.       |
|              Calibration plot: see /ledger/cpi-yoy/4Q                    |
|                                                                          |
| OPENGEM World Dashboard · CC-BY-4.0 · opengem.world/i/cpi-yoy · 2026-06-02|
+--------------------------------------------------------------------------+
```

The indicator tearsheet emphasizes cross-country structure (small-multiples grid) plus the track-record / leaderboard combination (the rigor argument).

## The Scenario Tearsheet

```
+--------------------------------------------------------------------------+
| OPENGEM · SCENARIO: TRADE-LATAM                       vintage 2026-06-02
+--------------------------------------------------------------------------+
| STATUS: FIRED today  · Global P 0.62  · Last fire 2026-06-06             |
| Affects 12 LATAM countries (relevance-weighted)                          |
+--------------------------------------------------------------------------+
| NARRATIVE                                                                 |
|                                                                          |
| Trade-LATAM fires when (1) a major LATAM trading partner imposes         |
| tariffs > 15% on US exports, OR (2) a LATAM central bank moves rates     |
| by more than 100bp in a single meeting outside its forward guidance.     |
| As of 2026-06-06, Brazil announced a 22% retaliatory tariff on US soy,   |
| triggering condition (1). The probability rollup reflects elevated       |
| risk to Mexico, Brazil, Chile, and Colombia.                             |
|                                                                          |
| Median 4Q-ahead realized GDP impact on BRA in past fires: -0.5pp (IQR    |
| -0.2 to -0.8). For the full historical track record see methodology.    |
+--------------------------------------------------------------------------+
| AFFECTED COUNTRIES MAP        |  PROBABILITY ROLLUP                       |
|                              |                                          |
| [LATAM regional map,          |   Country  P     Affected horizons        |
|  countries shaded by P]       |   BRA      0.72  1Q, 4Q, 2Y               |
|                              |   MEX      0.65  1Q, 4Q                  |
|                              |   CHL      0.41  4Q                       |
|                              |   COL      0.38  4Q                       |
|                              |   PER      0.24  4Q                       |
|                              |   URY      0.18  4Q                       |
|                              |   ARG      0.16  1Q                       |
|                              |                                          |
+--------------------------------------------------------------------------+
| TRIGGER CONDITIONS             V&V EVIDENCE (n=12 backtest fires)         |
|                                                                          |
| Condition (1) — Tariff event   AUC 0.78 (90% CI 0.71-0.84)                |
|   LATAM tariff > 15% on US     Precision @ 0.5: 0.67                     |
|   Source: WTO + gazettes       Recall @ 0.5: 0.75                        |
|                                Brier score 0.18                          |
| Condition (2) — Monetary       Direction hit rate 73% (p<0.01)            |
|   LATAM CB rate move > 100bp   vs AR(1) baseline AUC 0.51                 |
|   in single meeting outside    vs threshold-only AUC 0.61                |
|   forward guidance band                                                  |
|   Source: BIS CBPOL + press    Out-of-sample 2024: AUC 0.74              |
|                                                                          |
+--------------------------------------------------------------------------+
| METHODOLOGY  v3 (2026-04-15) · pack JSON urn:opengem:pack:trade-latam:v3 |
|              See /s/trade-latam/methodology for full V&V evidence.       |
|                                                                          |
| OPENGEM World Dashboard · CC-BY-4.0 · opengem.world/s/trade-latam        |
+--------------------------------------------------------------------------+
```

The scenario tearsheet emphasizes narrative + map + rollup + V&V evidence — the four things that make a scenario credible.

## Generation pipeline

The tearsheets are server-rendered SVG → PDF:

1. Server-side React renders the tearsheet to an SVG-first layout.
2. The SVG is wrapped in a PDF container (via PDFKit, ReportLab, or similar).
3. Charts are rendered as actual SVG (not raster) so the print is sharp at any DPI.
4. The PDF is cached at the vintage level (one PDF per record per vintage).

The PDF can be downloaded from any record page via the `[PDF tearsheet]` button (or `> export pdf` command).

## Branded tearsheets (Team tier)

Team tier customers can:
- Replace the header band with their own logo + branding (white-label).
- Customize footer text (e.g., "Prepared for [Firm] · confidential").
- Optionally hide the OPENGEM URL.

The OPENGEM watermark (small, footer) is preserved unless the customer has an explicit white-label agreement.

## What does NOT print

- Vintage rewind controls.
- Interactive consensus toggles.
- Drilldown drawers.
- Search bar.
- Watchlist / alert chrome.

The tearsheet is a static snapshot. Interactive elements are stripped.

## Print typography rules

Numbers always use lining tabular figures (so values align in columns). Country names use the same font but with letter-spacing tightened. Headers use brand color sparingly (the header band only).

Page numbers and total page count appear in the footer only if the export is multi-page (which the tearsheet is not — single page is the spec).

## What this loop produced

- Three tearsheets specified: country, indicator, scenario.
- Format: US Letter landscape, 0.5" margins, header + body + footer bands.
- Typography: Inter for type, JetBrains Mono for values, 11pt body, tabular figures.
- Color: terminal-orange header band, three-opacity P10/P50/P90 bands.
- Country tearsheet: 5 horizontal bands (headline / chart / situation+scenarios+events / methodology+track-record / citation).
- Indicator tearsheet: 4 bands (headline / small-multiples / track-record+leaderboard / methodology+citation).
- Scenario tearsheet: 4 bands (status / narrative / map+rollup / triggers+V&V / methodology+citation).
- Generation: server-side SVG → PDF, cached at vintage level.
- Team-tier white-label option.
- Interactive elements stripped from print.

## What comes next

- **L116** integrates: print-grade SVG export for tearsheets.
- **L246** prototypes the print tearsheet generation pipeline.
- **L155** designs the sharing UX (PDF is one of the share formats).

## Related

- [[L121-information-architecture]] — every record page has a [PDF tearsheet] button
- [[L123-country-page]] — country tearsheet derives from this layout
- [[L132-provenance-drawer]] — methodology footer references drawer
- [[L138-pricing-page]] — Team tier white-label
- [[L145-dashboard-themes]] — terminal-orange brand applies
- [[L246-print-tearsheet-prototype]] — code prototype
