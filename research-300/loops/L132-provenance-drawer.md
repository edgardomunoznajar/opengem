---
loop: 132
phase: 3
title: Provenance / Vintage Drawer — Universal Spec
date: 2026-06-06
status: decided
---

# L132 — Provenance / Vintage Drawer

**Loop**: 132 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design the provenance drawer. It must appear on every chart in the dashboard. It must contain everything an analyst needs to defend the displayed number in a meeting. It must support replay-and-diff.

This is the load-bearing brand mechanism. The drawer is the operational form of "the dashboard publishes its mistakes."

## Where the drawer appears

Every chart, table, scoreboard, and forecast view has a small `[ⓘ provenance]` button in the lower-right corner (or the `M` keystroke when the element is focused). The button is *always present*. There is no chart on OPENGEM without a provenance drawer.

The drawer is a right-edge slide-out, 480px wide on desktop, full-screen on mobile.

## The universal drawer structure

```
+--------------------------------------------------------------+
| PROVENANCE                                              [×]  |
+--------------------------------------------------------------+
| Record                                                       |
|   /f/cpi-yoy/USA/4Q at vintage 2026-06-02                    |
|                                                              |
| Canonical URL                                                |
|   https://opengem.world/f/cpi-yoy/USA/4Q/v/2026-06-02        |
|   [copy] [permalink] [cite]                                  |
+--------------------------------------------------------------+
| DATA SOURCES                                                 |
|                                                              |
| Series 1: US CPI All Items                                  |
|   Publisher: U.S. Bureau of Labor Statistics                |
|   Source URL: bls.gov/cpi                                   |
|   Series ID: CUUR0000SA0                                    |
|   Acquired: 2026-06-02 06:00 UTC                             |
|   Latest observation: 2026-05 (released 2026-06-12)         |
|   Vintage at use: 2026-06-02                                 |
|   License: U.S. Government work (public domain)             |
|                                                              |
| Series 2: 10-year Treasury yield                            |
|   Publisher: Federal Reserve Board (H.15)                   |
|   Source URL: federalreserve.gov/releases/h15                |
|   ...                                                         |
|                                                              |
| (covariate list continues)                                   |
+--------------------------------------------------------------+
| FORECAST MODEL                                              |
|                                                              |
| Architecture: L3-BMA over 5 sub-models                       |
|   AR(p)        weight=0.12                                   |
|   BVAR         weight=0.31                                   |
|   DFM          weight=0.28                                   |
|   RF           weight=0.19                                   |
|   NHITS        weight=0.10                                   |
|                                                              |
| Hyperparameters: lockfile L1f2a8b                            |
| Combiner: Bayesian Model Averaging                          |
| Reference: opengem-L3 v0.4.1                                 |
|                                                              |
| [Full model card →]                                          |
+--------------------------------------------------------------+
| REPRODUCIBILITY ENVELOPE                                    |
|                                                              |
| Commit:        opengem@abc1234                               |
| Container:     ghcr.io/opengem/forecast:0.4.1                |
| Container SHA: sha256:7d3a8b...                              |
| Data lockfile: L1f2a8b                                       |
| Python:        3.12.4                                        |
| OS:            Debian 12.5 (in container)                    |
| Random seed:   42                                            |
| Hardware:      CPU-only, 32GB RAM                            |
|                                                              |
| [Replay this forecast →]                                     |
| [Replay-and-diff this forecast →]                            |
+--------------------------------------------------------------+
| TRACK RECORD (last 24 vintages)                              |
|                                                              |
|   CRPS    0.84   (vs WEO 0.91, RW 1.42)                     |
|   PIT     0.78   (threshold: 0.70 → PASS)                   |
|   Bias   -0.04                                               |
|   MAE     0.31                                               |
|                                                              |
| Mini calibration plot:                                       |
|   [80x80 P-P plot SVG]                                       |
|                                                              |
| [Full track record →]                                        |
+--------------------------------------------------------------+
| MISS LOG (last 4 vintages)                                   |
|                                                              |
|   2026-03  P50 3.1  actual 3.4  miss +0.3                   |
|   2025-12  P50 2.7  actual 2.9  miss +0.2                   |
|   2025-09  P50 3.4  actual 3.1  miss -0.3                   |
|   2025-06  P50 3.0  actual 3.2  miss +0.2                   |
|                                                              |
| [Full miss log →]                                            |
+--------------------------------------------------------------+
| CONSENSUS COMPARISON                                         |
|                                                              |
| WEO Apr 2026         2.8%  OPENGEM -0.4pp                    |
| OECD EO May 2026     2.7%  OPENGEM -0.3pp                    |
| FRB SEP Jun 2026     2.6%  OPENGEM == match                  |
| Cleveland Nowcast    2.9%  OPENGEM -0.3pp                    |
+--------------------------------------------------------------+
| VINTAGE LINEAGE                                              |
|                                                              |
| This vintage chain (last 6):                                 |
|   2026-06-02 ← current (this drawer)                        |
|   2026-03-02   prior                                         |
|   2025-12-02   prior                                         |
|   2025-09-02   prior                                         |
|   2025-06-02   prior                                         |
|   2025-03-02   inception                                     |
|                                                              |
| [Vintage rewind / play] [Diff against previous vintage]      |
+--------------------------------------------------------------+
| LICENSE                                                      |
|                                                              |
| Forecast output: CC-BY-4.0                                   |
| Citation: OPENGEM World Dashboard. (2026). US CPI YoY 4Q     |
|           ahead forecast, vintage 2026-06-02. Retrieved      |
|           {date} from https://opengem.world/f/...            |
| BibTeX: [show] [copy]                                        |
+--------------------------------------------------------------+
| RELATED RECORDS                                              |
|                                                              |
|  • US CPI YoY at different horizons (1Q, 2Y)                |
|  • CPI YoY across other G7 (cross-country)                  |
|  • Scenarios triggered for this country (4)                  |
|  • Model card for L3-BMA                                    |
+--------------------------------------------------------------+
| FOOTER                                                       |
| Last refreshed: 2026-06-02 06:00 UTC                         |
| Next refresh:   2026-06-03 06:00 UTC (daily cadence)         |
| API: GET /v1/forecasts/cpi-yoy/USA/4Q?vintage=2026-06-02     |
| MCP: opengem.forecast({record, vintage})                     |
+--------------------------------------------------------------+
```

## Why the drawer is mandatory

OPENGEM's brand promise is "every number comes with its own report card attached." The provenance drawer is that report card. If a chart appears without a drawer, the chart cannot ship.

The CI guard for this is `prov-presence-lint`: an automated check during the dashboard build that scans every chart-rendering component for a `<ProvenanceTrigger />` JSX element. Charts without one fail the build.

## Why it is a slide-out and not a modal or pop-up

Three reasons:
1. **Persistence**: The user reads the drawer while the chart remains visible. They can hover the chart, see a value, glance at the drawer to verify the source vintage.
2. **Stackability**: The drawer can be opened with the chart already drilled into — the user moves between drawer sections without losing the chart context.
3. **Mobile**: On portrait, the drawer becomes a bottom sheet that the user can drag up to read more.

## The "replay this forecast" button

This is the load-bearing trust mechanism. Clicking "Replay this forecast" launches a CI job:

1. Spawns a container at the listed digest.
2. Hydrates the data lockfile.
3. Runs the forecast model with the listed seed.
4. Produces a new forecast output.
5. Diffs against the displayed forecast.
6. Reports: match / drift (with diff vector) / fail (with error).

The replay job runs on OPENGEM's CI on the free tier (with rate limits). On the pro tier, the user can replay-and-diff against any custom input modification (counterfactual replay).

The replay output is itself archived and citable. So a journalist writing a piece in 2030 can cite OPENGEM's 2026 CPI forecast AND cite OPENGEM's 2030 replay of that same forecast, and the public can verify both.

## Vintage lineage rendering

The vintage chain (last 6 vintages of the same record) is shown by default. Clicking any chain entry drills into the drawer for that vintage. So the user can hop backward through vintages without leaving the drawer.

## Citation block

The CITE button generates a citation in three formats:
1. **Plain text** (publication style): "OPENGEM World Dashboard. (2026). US CPI YoY 4Q ahead forecast, vintage 2026-06-02."
2. **BibTeX**: full entry with DOI-like URN.
3. **DataCite-style JSON-LD**: machine-readable for inclusion in research datasets.

Every forecast vintage has a stable URN (`urn:opengem:forecast:cpi-yoy:USA:4Q:2026-06-02`). The URN is the citation key. Citations are deterministic, persistent, machine-readable.

## What the drawer renders for non-forecast records

For an indicator value (not a forecast), the drawer omits Forecast Model, Track Record, Miss Log, and Consensus Comparison. It keeps Data Sources, Reproducibility Envelope (the ingest provenance), Vintage Lineage (the data vintage chain), License, Related Records, Footer.

For a scenario, the drawer renders Pack Methodology in place of Forecast Model (linking to the full methodology page L135), the Trigger Sources in place of Data Sources, the historical fire log in place of Miss Log, and Pack Track Record (AUC, hit rate) in place of Track Record.

For an event, the drawer renders the GDELT cluster ID + source list, the dedup heuristic that grouped them, the geo-tag normalization, and the scenario/indicator impact analysis.

For a ledger cell, the drawer renders the V&V matrix cell methodology + per-vintage CRPS contributions + the AR(1)/RW baseline scores.

## Accessibility

The drawer is fully keyboard-navigable. Reading order is logical. Each section has a heading and the user can jump to a section with `g s` (g for go, s for sources / m for model / r for replay / t for track / c for cite — vim-style chord within the drawer).

Screen-reader announces the drawer title, then each section heading. The replay button has aria-label "Re-run this forecast in CI and compare the result to the displayed forecast."

## What the drawer does NOT contain

- Editorial commentary on whether the forecast is "good." (The track record is the editorial.)
- Speculation about why a miss happened. (Diagnostic notes per-miss live on the dedicated miss-log page L200.)
- Comparison to other forecasters' Ledger cells. (That is the leaderboard L133.)
- A chat / Q&A widget. (LLMs can use the MCP server; the drawer is reading, not conversation.)

## What this loop produced

- Universal drawer structure with 12 sections (Record, Data Sources, Forecast Model, Reproducibility Envelope, Track Record, Miss Log, Consensus Comparison, Vintage Lineage, License/Citation, Related Records, Footer, action buttons).
- Drawer is mandatory on every chart; CI lint enforces presence.
- Right-edge slide-out on desktop; bottom sheet on mobile.
- Replay-and-diff is a one-click action that runs the forecast in CI and reports diff.
- Stable URN per vintage for citation.
- Per-record-type rendering rules (forecast, indicator, scenario, event, ledger cell).
- Keyboard-navigable with vim-style chords within the drawer.

## What comes next

- **L133** designs the leaderboard (the comparison-to-other-forecasters surface).
- **L134** designs the track-record page (the "full track record" linked from the drawer).
- **L135** designs the methodology page (the "full model card" linked).
- **L158** designs cite-this-view in detail.
- **L186** designs the reproducibility envelope mechanics.
- **L200** designs the miss-log page.

## Related

- [[L121-information-architecture]] — drawer is present on every chart across all sections
- [[L123-country-page]] — drawer opens from each chart on country page
- [[L126-forecast-page]] — drawer is the universal form of the forecast page right rail
- [[L134-track-record-page]] — full track record drilled from drawer
- [[L135-methodology-page]] — full methodology drilled from drawer
- [[L158-cite-this-view]] — citation block detail
- [[L186-reproducibility-envelope]] — replay-and-diff mechanics
