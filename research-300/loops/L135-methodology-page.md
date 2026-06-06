---
loop: 135
phase: 3
title: Methodology Page (per scenario pack)
date: 2026-06-06
status: decided
---

# L135 — Methodology Page (per scenario pack)

**Loop**: 135 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design `/s/{pack-id}/methodology` — the per-scenario-pack methodology page. Trigger spec. Model link. V&V evidence.

This is the page a reviewer reads when evaluating whether an OPENGEM scenario pack is a serious instrument or a marketing claim. Methodology pages for forecasts and indicators have parallel structure; this loop focuses on scenario packs because they are the most editorial-prone artifacts (and most likely to be challenged).

## The structure

```
+--------------------------------------------------------------------------+
| OPENGEM > Scenarios > Trade-LATAM > Methodology                          |
| /s/trade-latam/methodology                                               |
+--------------------------------------------------------------------------+
| HEADER                                                                   |
|                                                                          |
| Pack: Trade-LATAM                                                        |
| Version: v3 (2026-04-15 — current)                                       |
| Author: OPENGEM Core (Edgardo Muñoz Najar) + opengem-scenarios v0.4.1   |
| License: CC-BY-4.0                                                       |
| Reproducibility envelope: commit abc1234, container opengem:0.4.1        |
|                                                                          |
| [Pack JSON →] [Version history →] [Submit a critique →]                  |
+--------------------------------------------------------------------------+
| 1. WHAT THIS PACK CLAIMS                                                 |
|                                                                          |
| Trade-LATAM is a binary trigger pack for trade-shock events in           |
| Latin America. It claims to identify states-of-the-world where a         |
| major LATAM trading partner imposes tariffs or makes a step-change       |
| monetary policy move, with measurable downstream effects on forecast    |
| paths for affected countries.                                            |
|                                                                          |
| Specifically:                                                           |
|   - Probability of firing at any given snapshot.                         |
|   - List of affected countries with per-country P.                       |
|   - Forecast effects (P50 / band shifts) at 1Q, 4Q, 2Y horizons.        |
|   - Historical fire log with realized impact.                            |
|                                                                          |
| Not claimed:                                                            |
|   - Causal attribution beyond statistical correlation.                  |
|   - Precise timing of impact transmission.                              |
|   - Exhaustive coverage of all trade shocks (this pack is one of many). |
+--------------------------------------------------------------------------+
| 2. TRIGGER SPECIFICATION                                                 |
|                                                                          |
| Logical structure: Condition (1) OR Condition (2)                       |
|                                                                          |
| Condition (1) — Tariff event                                            |
|   - A LATAM-region country imposes import tariffs > 15%                 |
|     on US exports.                                                       |
|   - Tariff effective date within the next 90 days.                      |
|   - Source: WTO Trade Policy Reviews + national government gazettes.    |
|   - Trigger threshold: 15% nominal tariff rate (configurable in pack).  |
|   - Why 15%: historical analysis of LATAM tariff events 2010-2024 shows |
|     bimodal distribution at <10% (mild) and >18% (severe); 15% is the   |
|     pragmatic midpoint where forecast effects become detectable in our  |
|     L3 model backtests. See section 5.                                  |
|                                                                          |
| Condition (2) — Monetary surprise                                       |
|   - A LATAM central bank moves policy rate by >100bp in a single        |
|     meeting outside its forward-guidance band.                          |
|   - Source: BIS CBPOL + central bank press releases.                    |
|   - Trigger threshold: 100bp single-meeting move.                       |
|   - Why 100bp: in BIS CBPOL data 2010-2024, single-meeting moves >100bp |
|     are <5% of all moves and consistently associated with regime-shift  |
|     news; smaller moves are within forward-guidance noise.              |
+--------------------------------------------------------------------------+
| 3. AFFECTED COUNTRIES MAP                                               |
|                                                                          |
| Base list: 12 countries (MEX, BRA, CHL, COL, PER, ARG, URY, VEN, ECU,   |
|            BOL, PRY, CRI).                                              |
|                                                                          |
| Per-country weighting: each country has a relevance score derived       |
| from its trade-share with the US (BACI 2010-2024 mean).                 |
|                                                                          |
| Per-country P: conditional on the pack firing, each country has         |
| its own P-of-impact based on:                                           |
|   - Trade-share with the triggering source.                             |
|   - Currency regime (floating vs pegged).                               |
|   - FX reserve adequacy (IMF ARA).                                      |
|   - Historical sensitivity to tariff / rate shocks (L3 IRF).            |
|                                                                          |
| Coefficient table: [show full table]                                    |
+--------------------------------------------------------------------------+
| 4. PROBABILITY ROLLUP                                                    |
|                                                                          |
| Global P = BMA-weighted average of per-country Ps, weighted by GDP-PPP. |
| Source: IMF WEO PPP weights, vintage 2026-04.                            |
|                                                                          |
| Per-country P computation:                                               |
|   P(country | pack fires) = α × trade_share +                            |
|                              β × currency_regime_score +                 |
|                              γ × historical_IRF_response                 |
|   where α=0.42, β=0.21, γ=0.37, fitted on 2010-2024 fire history.        |
+--------------------------------------------------------------------------+
| 5. V&V EVIDENCE                                                          |
|                                                                          |
| Backtest scope: 2010-01 to 2024-12 monthly.                             |
| Fire events in backtest: 12 (4 tariff, 8 monetary).                      |
| Hits / Misses / False Positives: HC TBD on next refresh.                |
|                                                                          |
| Binary classification metrics (does pack predict trouble?):              |
|   AUC: 0.78 (90% CI: 0.71-0.84)                                          |
|   Precision @ 0.5 threshold: 0.67                                        |
|   Recall @ 0.5 threshold: 0.75                                           |
|   Brier score: 0.18                                                      |
|                                                                          |
| Forecast-impact accuracy (does P50 shift match realized direction?):   |
|   Hit direction rate: 73% (significant at p<0.01)                       |
|   Magnitude MAE: 0.34 pp                                                  |
|                                                                          |
| Comparison to alternates:                                                |
|   AR(1) baseline: AUC 0.51 (no signal)                                  |
|   Simple-threshold (tariff >5%): AUC 0.61                                |
|   Trade-LATAM L3: AUC 0.78 (significant improvement)                    |
|                                                                          |
| Sensitivity tests:                                                      |
|   Threshold sweep (tariff): AUC peaks at 13-17% (we chose 15%).          |
|   Threshold sweep (rate move): AUC peaks at 80-130bp (we chose 100bp).  |
|   Out-of-sample 2024 only: AUC 0.74 (close to in-sample).               |
+--------------------------------------------------------------------------+
| 6. MODEL CARD (for the underlying L3 model)                              |
|                                                                          |
| The trigger evaluation uses opengem-event-detector + opengem-scenarios. |
| The forecast-impact estimation uses opengem-L3 (BMA over BVAR, DFM,    |
| RF, NHITS sub-models).                                                  |
|                                                                          |
| [Full L3 model card →]                                                  |
| [Full event-detector spec →]                                             |
| [opengem-scenarios codebase →]                                           |
+--------------------------------------------------------------------------+
| 7. ASSUMPTIONS                                                           |
|                                                                          |
|   (1) Tariff announcements are observed via WTO + gazettes within         |
|       7 days of effective date. Coverage holes exist for non-WTO         |
|       members.                                                          |
|   (2) BIS CBPOL series is timely. Some central banks publish rates       |
|       on a lag; we use latest available.                                 |
|   (3) Per-country relevance weights fitted on 2010-2024 may not          |
|       generalize to regime shifts (e.g., USMCA 2.0).                    |
|   (4) The BMA combiner weights are point estimates, not posterior        |
|       distributions; we report central tendency.                        |
|   (5) Trade-share-with-US is computed from BACI; for very small         |
|       countries the share is noisy.                                    |
+--------------------------------------------------------------------------+
| 8. KNOWN LIMITATIONS                                                     |
|                                                                          |
|   - Tariff data has 2-3 day lag for non-G20 LATAM countries.            |
|   - Backtest fire count is small (n=12) → wide confidence intervals.    |
|   - Spillover to non-LATAM countries (e.g., to East Asia via global     |
|     trade) is not currently modeled.                                    |
|   - The pack does not capture cumulative effects of multiple             |
|     simultaneous events; each fire is treated independently.            |
+--------------------------------------------------------------------------+
| 9. VERSION HISTORY                                                       |
|                                                                          |
|   v3 (2026-04-15) — re-fit on 2010-2024 data; threshold tightened       |
|                     to 100bp (was 75bp); added Costa Rica to roster.   |
|   v2 (2025-06-01) — added monetary condition (was tariff-only).         |
|   v1 (2024-09-15) — initial release.                                    |
|                                                                          |
| [Diff v3 vs v2] [Diff v2 vs v1]                                          |
+--------------------------------------------------------------------------+
| 10. EXTERNAL CRITIQUE                                                    |
|                                                                          |
| Reviewers' notes (public):                                              |
|   - [Reviewer 001, 2025-12-04, anon LATAM economist]: "Need to test     |
|     pre-2010 fires (1994 peso crisis, 1999 Brazil)." → Acknowledged;    |
|     pre-2010 not in our vintage horizon, on roadmap.                    |
|   - [Reviewer 002, 2026-02-08, sovereign-fund analyst]: "Should weight |
|     against PMI signal." → Under evaluation for v4.                    |
|                                                                          |
| [Submit a critique →]                                                    |
+--------------------------------------------------------------------------+
| 11. CITATION                                                             |
|                                                                          |
| OPENGEM World Dashboard. (2026). Trade-LATAM scenario pack methodology  |
| v3. Retrieved {date} from https://opengem.world/s/trade-latam/         |
| methodology.                                                            |
|                                                                          |
| BibTeX: [show]                                                          |
| DOI-like URN: urn:opengem:pack:trade-latam:v3                            |
+--------------------------------------------------------------------------+
| FOOTER                                                                   |
| Submitted to V&V review: 2026-04-20                                      |
| Last reviewed: 2026-05-30 by OPENGEM Core                                |
| Next scheduled review: 2026-10-15                                        |
+--------------------------------------------------------------------------+
```

## Why a single long page (not a tabbed structure)

The methodology page is read end-to-end by reviewers, not browsed. A tabbed structure would hide critical content (e.g., assumptions, limitations) behind clicks. A reviewer evaluating the pack needs to see the *whole argument* in one scroll. The page can be long; that is correct.

For browsing readers who only want a section, a sticky table-of-contents on the right anchors to each section (1-11).

## What every methodology page must contain

The eleven sections are the minimum spec. Every methodology page (scenario, forecast model, or indicator pipeline) follows this template:

1. **What this artifact claims** (and explicitly does not claim).
2. **Trigger / model specification** (the operational definition).
3. **Coverage / affected scope**.
4. **Probability or output computation rule**.
5. **V&V evidence** (with comparison to baselines).
6. **Model card link** (link to underlying model details).
7. **Assumptions**.
8. **Known limitations**.
9. **Version history** (with diffs).
10. **External critique** (public review log).
11. **Citation**.

This template is enforced by a CI lint (`methodology-template-lint`): every methodology page is checked for the presence of all 11 sections. Missing sections fail the build.

## V&V evidence framing

V&V evidence is the load-bearing section. It must include:
- Backtest scope (date range, cadence).
- Sample size (number of fires / forecasts in backtest).
- Performance metrics with confidence intervals.
- Comparison to at least one naive baseline (random walk, AR(1), or coin flip).
- Sensitivity analysis (threshold sweep, out-of-sample test).

If a pack cannot pass V&V (AUC > naive baseline, p < 0.05), it is *not published* with claims of skill. The methodology page is still public, but the headline says "NOT PUBLISHED FOR FORECAST USE — V&V evidence insufficient." This is the rigor floor.

## Known limitations

Every methodology page lists known limitations. This is the brand commitment: we say what we cannot do. The Trade-LATAM example lists 4 specific limitations; other packs will have their own.

If the page does not list at least 3 known limitations, the CI lint flags it ("too confident to be honest").

## External critique

The reviewers' notes section is public. Anyone can submit a critique via the "Submit a critique →" link. Critiques are moderated for relevance (no spam) but are otherwise published.

Critiques can lead to version bumps. The reviewer is credited (with their permission) in the version history.

This is the "we publish our reviewers" commitment — a counter to closed peer review.

## Version history with diff

Every pack version is preserved. Clicking "Diff v3 vs v2" shows the changes (threshold values, country roster, code commits, V&V metric changes). The full version history is permanent: v1 is still cite-able even if it has been superseded by v3.

## Reproducibility

The header lists the reproducibility envelope (commit, container, lockfile). Clicking the "Pack JSON" link downloads the canonical pack definition. Clicking "Submit a critique →" opens a GitHub issue with the pack ID pre-filled (sign-in required to avoid spam).

The pack can be re-run by anyone with the envelope. The Replay button (on the country/scenario page) takes care of running it; the methodology page documents how.

## What this loop produced

- Per-pack methodology page with 11 mandatory sections enforced by CI lint.
- Long-page (not tabbed) format with sticky table-of-contents.
- V&V evidence requires baseline comparison + sensitivity sweep.
- Known limitations section (≥3 limitations required).
- External critique section is public and moderated; can lead to version bumps.
- Version history is permanent; v1 remains cite-able even when superseded.
- Pack JSON downloadable; pack reproducible from envelope.
- "NOT PUBLISHED FOR FORECAST USE" stamp for packs that fail V&V.

## What comes next

- **L136** designs the about / governance / changelog page (which links methodology versions).
- **L137** designs the API docs page (per-pack API endpoint documentation).
- **L185** designs the open backtest harness (the engine behind V&V evidence).
- **L196** designs scenario trigger evaluation in code.
- **L199** designs trust signals page (which forecasts have which V&V evidence).

## Related

- [[L121-information-architecture]] — /s/{pack}/methodology URL space
- [[L125-scenario-page]] — methodology link on scenario page
- [[L132-provenance-drawer]] — methodology link from drawer
- [[L134-track-record-page]] — V&V cell status surfaced here
- [[L185-backtest-harness]] — engine behind V&V evidence
- [[L199-trust-signals]] — which forecasts have V&V evidence
