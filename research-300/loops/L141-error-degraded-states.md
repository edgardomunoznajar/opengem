---
loop: 141
phase: 3
title: Error and Degraded-Data States
date: 2026-06-06
status: decided
---

# L141 — Error / Degraded-Data States

**Loop**: 141 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design the error and degraded-data states. When does an adapter failure surface? When does stale data surface? When does a forecast past-due surface?

Empty states (L140) handle "there is nothing here yet." Error states handle "there should be something here but something went wrong." Degraded states handle "there is something here but it is not ideal."

OPENGEM's brand commitment is "publish our mistakes" — this includes operational failures. Errors and degradations are surfaced, not hidden behind a fallback.

## Three categories

### Category 1 — Hard errors (system fault)

The page cannot render because of a code or infrastructure failure. Examples:
- 5xx from upstream service.
- Database connection failure.
- Crashed render in SSR.

### Category 2 — Degraded data (input fault)

The page can render but the underlying data is older than the SLA, partially missing, or otherwise sub-spec. Examples:
- Adapter fetched data 11 hours ago but the source updates every 6 hours.
- One sub-model in the BMA ensemble failed; the ensemble runs with 4 of 5 sub-models.
- A consensus source (e.g., WEO) released after the forecast vintage; the overlay shows but with a "behind" badge.

### Category 3 — Past-due (timing fault)

A forecast that was scheduled to publish has not published yet. The vintage is overdue.

## Hard error states

### 500 / system error

```
+----------------------------------------------------+
| Something is broken.                               |
+----------------------------------------------------+
|                                                    |
| OPENGEM hit an unexpected error rendering this    |
| page. The error has been logged.                  |
|                                                    |
| Error ID: err_2026_06_06_abc123                   |
|                                                    |
| What you can do:                                   |
|   - Reload the page                                |
|   - Try the underlying API endpoint directly      |
|     [/v1/{the-record-id}]                          |
|   - View the same record at a different vintage   |
|                                                    |
| If this keeps happening, file at:                  |
|   github.com/opengem/opengem/issues with err_id   |
|                                                    |
| [Reload] [Status page →] [File issue →]            |
+----------------------------------------------------+
```

Voice: no apology, no anthropomorphizing, error ID for grep, paths forward.

### 404 / record not found

```
+----------------------------------------------------+
| /c/XYZ does not exist.                              |
+----------------------------------------------------+
|                                                    |
| OPENGEM does not have a record at this URL.       |
|                                                    |
| If you typed a country code: country codes are     |
| ISO 3166-1 alpha-3 (e.g., USA, EUR, GBR).        |
|                                                    |
| If you came from a link: the URL may have changed |
| or the record may not be in our roster.           |
|                                                    |
| Try:                                                |
|   - [Search countries →]                            |
|   - [Browse the country grid →]                     |
|   - [/about/coverage]                               |
|                                                    |
| [⌘K to search]                                      |
+----------------------------------------------------+
```

### 503 / service degraded

```
+----------------------------------------------------+
| One or more services are degraded.                 |
+----------------------------------------------------+
|                                                    |
| Affected: forecast computation service              |
| Detected: 2026-06-06 14:32 UTC (12 minutes ago)   |
| Current state: returning cached results            |
|                                                    |
| What this means for you:                            |
|   - Live forecast pages render the last good      |
|     forecast vintage.                              |
|   - Replay-and-diff is currently disabled.        |
|   - Watchlist and alerts continue to work.        |
|                                                    |
| [Status page →] [last good vintage →]              |
+----------------------------------------------------+
```

## Degraded-data states

### Adapter degraded — staleness banner

A page-level banner sits at the top of any record whose underlying adapter is in degraded state:

```
+----------------------------------------------------+
| ⚠️ Data is stale. Adapter BLS (US CPI) last         |
|   refreshed 11 hours ago. SLA: 6 hours.            |
|   The displayed values are from the last           |
|   successful vintage. [status page]                |
+----------------------------------------------------+
```

The banner is yellow-tinted, dismissible per-session but reappears next page load. The page renders normally below the banner.

### Per-value badge — vintage delta

On individual values where the source is stale:

```
| US CPI YoY  2.9%  ⚠ source 11h stale (SLA 6h)      |
| ▼ 0.2pp m/m                                         |
```

The badge has a hover tooltip with the per-source details.

### Sub-model failure (BMA ensemble degraded)

When an L3 BMA sub-model fails to converge or run, the ensemble runs with the remaining sub-models. The provenance drawer reports the degradation:

```
| FORECAST MODEL                                      |
|                                                    |
| Architecture: L3-BMA over 4 sub-models             |
| (1 of 5 sub-models failed for this vintage)        |
|                                                    |
|   AR(p)     w=0.13   ran                            |
|   BVAR      w=0.34   ran                            |
|   DFM       w=0.31   ran                            |
|   RF        w=0.22   ran                            |
|   NHITS     —        FAILED (timeout)              |
|                                                    |
| Note: BMA weights renormalized over running        |
| sub-models. Compare to last full-run vintage:      |
| [2026-03-02 vintage with all 5 sub-models →]       |
```

This is the load-bearing transparency move. The user sees that the forecast is *not* the same shape as last time.

### Consensus overlay — release timing mismatch

When a consensus source has not released for the current forecast vintage:

```
| CONSENSUS OVERLAY                                    |
|                                                    |
| WEO Apr 2026         2.8%  (last release; behind   |
|                            OPENGEM 2026-06-02 by   |
|                            ~2 months)              |
| OECD EO May 2026     2.7%  (last release; behind)  |
| FRB SEP Jun 2026     2.6%  (current)               |
| Cleveland Nowcast    2.9%  (current)               |
```

The "behind" badge is visible in the consensus dot tooltip and in the leaderboard comparison.

### Coverage gap — country not in Tier-V

When viewing a country in Tier-T (tracked but not vintage-correct):

```
| 🇳🇬 NIGERIA                                          |
|                                                    |
| Coverage: Tier-T (tracked, not vintage-correct).   |
|                                                    |
| What this means:                                    |
|   - Indicator values are published as available.   |
|   - Forecast vintages cannot be reproduced because |
|     source vintage history is not maintained.     |
|   - Calibration metrics are not computed for      |
|     Tier-T countries.                              |
|                                                    |
| [Tier-V vs Tier-T explained →]                     |
| [Coverage roster →]                                |
```

Per-page banner on every Tier-T country page.

### License-restricted data

When data exists but cannot be displayed in raw form due to source license (e.g., BIS aggregate):

```
| Series: BIS Effective Exchange Rates (broad,        |
| narrow indices)                                    |
|                                                    |
| Display: 5-year chart visible.                      |
| Download: not available due to BIS distribution    |
| terms.                                             |
|                                                    |
| To access raw data:                                 |
|   - Visit BIS Statistics warehouse [link]         |
|   - Free, registration not required               |
|                                                    |
| OPENGEM uses this series under BIS-approved terms |
| and does not redistribute.                          |
```

The chart still renders. The download is gated.

## Past-due states

### Forecast past-due

When the scheduled publication time for a vintage has passed without publication:

```
| Forecast: US CPI YoY 4Q ahead                       |
|                                                    |
| Scheduled vintage 2026-06-25 06:00 UTC.            |
| Status: PAST DUE (4 hours overdue).                 |
|                                                    |
| Why might this happen:                              |
|   - Upstream data adapter is degraded.             |
|   - L3 compute job is queued behind other vintages.|
|   - Vintage was skipped for V&V (rare; logged).    |
|                                                    |
| What we serve in the meantime: the previous good   |
| vintage (2026-06-02).                              |
|                                                    |
| ETA: best-effort 2 hours.                          |
|                                                    |
| [status page] [subscribe to publish notification]  |
```

The past-due state is honest. The page renders the prior vintage with a clear banner. If a forecast is skipped for V&V reasons, that gets a dedicated banner with a link to the V&V incident report.

### Scenario pack past-due (rare)

```
| Pack: Trade-LATAM                                   |
|                                                    |
| Daily reevaluation overdue (scheduled 06:00 UTC,   |
| ran last at 2026-06-05 18:00 UTC).                 |
|                                                    |
| Last evaluation: 2026-06-05 18:00 UTC.             |
| Probability shown is from last evaluation.        |
|                                                    |
| [status page]                                       |
```

## How to surface staleness

Three visibility levels:

1. **Page-level banner** (yellow tint, top of page) — when adapter degradation affects the displayed record's primary data.
2. **Per-value badge** (⚠ next to the number) — for granular staleness.
3. **Provenance drawer entry** — always (the drawer is the always-on truth source).

The most aggressive surface is the page-level banner; it appears only when the primary data is stale enough that the displayed values may mislead.

The provenance drawer is the universal surface — it always tells the full truth of staleness even when banners and badges are not warranted.

## Status page

`/status` is the operational dashboard. It lists every adapter, every model job, every cache, with their current state:

```
+----------------------------------------------------+
| OPENGEM Status · live                              |
+----------------------------------------------------+
| ADAPTERS                                            |
|                                                    |
| BLS (US CPI)             ⚠ degraded — 11h stale    |
| BEA (US GDP)             ✓ healthy                  |
| FRB (US Treasury yields) ✓ healthy                  |
| Treasury (FiscalData)    ✓ healthy                  |
| Census (M3, MRTS)        ✓ healthy                  |
| ORDRA (OECD multi-cty)   ✓ healthy                  |
| BIS (CBPOL)              ✓ healthy                  |
| GSCPI (NY Fed)           ✓ healthy                  |
| GPR (Caldara-Iacoviello) ✓ healthy                  |
| GDELT GKG                ✓ healthy                  |
|                                                    |
| MODEL JOBS                                          |
|                                                    |
| L3-BMA daily forecast    ✓ ran 2026-06-06 06:00    |
| Recession probability    ✓ ran 2026-06-06 06:15    |
| GPR nowcast              ✓ ran 2026-06-06 06:20    |
| Event detector           ✓ ran 2026-06-06 06:30    |
| Scenario rule engine      ✓ ran 2026-06-06 06:40    |
|                                                    |
| PUBLIC SURFACE                                      |
|                                                    |
| Dashboard (Next.js + CDN)  ✓ p95 187ms              |
| REST API (Spring Boot)     ✓ p95 124ms              |
| MCP server                 ✓ p95 224ms              |
|                                                    |
| RECENT INCIDENTS                                    |
|                                                    |
| 2026-06-06 14:32  BLS adapter SLA breach            |
|                   ETA: 2026-06-06 18:00            |
| 2026-06-03 03:14  GDELT 12h outage (recovered)    |
| 2026-05-28 09:00  L3 sub-model NHITS timeout      |
|                                                    |
| [Subscribe to status updates] [RSS]                 |
+----------------------------------------------------+
```

The status page is public. It is auto-generated from health checks. There is no fictional uptime — outages are listed honestly.

## Per-record incident log

Each forecast / scenario / indicator record has a small "incidents" section in the provenance drawer that lists the recent incidents affecting that record:

```
| INCIDENTS AFFECTING THIS RECORD                     |
|                                                    |
| 2026-06-06  BLS adapter stale (11h, ongoing)       |
|             → forecast bands include staleness     |
|             → see status page                      |
|                                                    |
| 2026-03-15  L3 sub-model NHITS retired             |
|             → recombiner weights adjusted          |
|             → see changelog                         |
```

## What this loop produced

- Three categories: hard errors, degraded data, past-due timing.
- Hard error states for 500 (with error ID), 404 (with search CTA), 503 (with cached fallback).
- Degraded-data state pattern: page-level banner + per-value badge + provenance drawer note.
- Sub-model failure transparency: BMA ensemble running with fewer sub-models is disclosed.
- Consensus overlay shows "behind" badge when source release lags forecast vintage.
- Tier-T (tracked-only) coverage explicitly framed on country pages.
- License-restricted data renders chart but gates download with link to source.
- Past-due forecast renders previous vintage with banner and ETA.
- Public /status page with adapter health, model jobs, public surface metrics, incident log.
- Per-record incidents list in provenance drawer.

## What comes next

- **L264** prototypes empty / loading / error / degraded states in code.
- **L132** integrates incident list into the provenance drawer.
- **L141 backlinks to**: L140 (sibling concern), L186 (reproducibility envelope).

## Related

- [[L121-information-architecture]] — /status URL space
- [[L132-provenance-drawer]] — incidents surface in drawer
- [[L136-about-governance-changelog]] — Trust commitment (A) no retroactive editing
- [[L140-empty-states]] — sibling concern
- [[L186-reproducibility-envelope]] — sub-model failure surfaces here
