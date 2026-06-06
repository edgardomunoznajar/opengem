# L175 — Accountability Page

**Loop**: 175 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

The accountability page is the *single most important page* OPENGEM publishes. It's the open ledger of every forecast ever made, with current scoring against actuals.

It's the artifact that justifies the brand. Without it, OPENGEM is just another dashboard. With it, OPENGEM is the public macro-accountability ledger.

## URL

`/accountability`

Linked from:
- Top nav (always visible)
- Every forecast methodology page
- Every forecast diff visualization
- The footer

## The page structure

```
   ┌────────────────────────────────────────────────┐
   │  Accountability Ledger                           │
   │  Every forecast OPENGEM has ever published.      │
   │  ──────────────────────────────────────────    │
   │                                                  │
   │  HEADLINE STATS                                  │
   │  ──────────────                                  │
   │  Forecasts published       12,438                │
   │  Scored                    8,221                 │
   │  Mean CRPS (24mo trailing) 0.41                  │
   │  Median rank vs consensus  3rd of 6              │
   │                                                  │
   │  ──────────────────────────────────────────    │
   │                                                  │
   │  RECENT MISSES                                   │
   │  Worst-scoring forecasts in last 30 days:        │
   │                                                  │
   │  • 2026-Q1 USA CPI: pred 3.1%, actual 3.5%       │
   │    Error +0.4pp · z = -1.4 (below band)         │
   │    [post-mortem]                                 │
   │                                                  │
   │  • 2025-Q4 JPN GDP: pred 0.8%, actual 0.2%       │
   │    Error -0.6pp · z = -1.8                       │
   │    [post-mortem]                                 │
   │                                                  │
   │  ──────────────────────────────────────────    │
   │                                                  │
   │  RECENT BEATS                                    │
   │                                                  │
   │  • 2025-Q4 USA recession-prob: pred 28%, actual no recession │
   │    Brier 0.078 · ranked 2nd of 6                 │
   │                                                  │
   │  • 2026-Q1 GBR CPI: pred 2.9%, actual 2.85%      │
   │    Error -0.05pp · z = -0.2                      │
   │                                                  │
   │  ──────────────────────────────────────────    │
   │                                                  │
   │  FULL LEDGER                                     │
   │  [Filter by: indicator, country, horizon, year] │
   │  [Sort by: date, error, rank]                   │
   │  ┌───────────────────────────────────────────┐  │
   │  │ ... 12,438-row table ...                  │  │
   │  └───────────────────────────────────────────┘  │
   │                                                  │
   │  ──────────────────────────────────────────    │
   │                                                  │
   │  HOW WE SCORE                                    │
   │  [methodology cards]                             │
   │                                                  │
   │  ──────────────────────────────────────────    │
   │                                                  │
   │  COMPARE OPENGEM TO OTHER FORECASTERS            │
   │  [calibration plot]                              │
   │                                                  │
   └────────────────────────────────────────────────┘
```

## Headline stats

Auto-computed, refreshed daily. Hero-sized numbers:

```
   12,438     Forecasts published since 2024-Q1
   8,221      Scored (rest pending horizon)
   0.41       Mean CRPS (24-month trailing)
   3rd        Median rank vs WEO/OECD/Bloomberg/Goldman/JPM (6-forecaster pool)
```

Each stat hoverable for tooltip explaining the metric.

## Recent misses (the unhinged transparency)

A list of the worst-scoring forecasts in the last 30 days. NOT cherry-picked. Sorted by worst CRPS or worst |z-score|.

```
   2026-Q1 USA CPI nowcast for May 2026 release
   ────────────────────────────────────────────
   Predicted: 3.1% (P10 2.4, P90 3.6)
   Actual:    3.5%
   Error:     +0.4pp · z = -1.4 (below P90 band)
   
   Post-mortem: Underweighted shelter component;
   subsequent retrospective showed CleveFed-DFM
   alternative would have been closer.
   
   [Full post-mortem] [Methodology] [Vintage view]
```

Each miss has:
- The forecast (with vintage)
- The actual
- The error
- The post-mortem (linked or inline)
- The methodology in use
- A "vintage view" link to see the original forecast in context

## Post-mortem template

Every miss with |z-score| > 1.5 gets a post-mortem within 7 days. Template (L298):

```
   ## What we forecast
   [the chart, vintage-pinned]

   ## What happened
   [the actual]

   ## What we got wrong
   [diagnosis in 100-200 words]

   ## What we changed
   [methodology adjustment, or "no change — within model variance"]

   ## How we'll detect this earlier next time
   [process change]

   ## What we won't change
   [explicit non-changes — sometimes the model was right and the world surprised]
```

Public. Cited. Linked.

## Recent beats

Same structure as misses but with low-CRPS forecasts. Not as a victory lap — as a fair contrast. We show beats and misses with equal prominence.

The ratio of beats vs misses is itself a metric (and we publish that too).

## Full ledger

A paginated, filterable table. Every row is one forecast:

```
   Indicator   Country  Vintage    Pred  Actual  Error  Z    Rank
   ──────────────────────────────────────────────────────────────
   CPI YoY    USA       2026-06-04  3.32  3.50    +0.18 -0.7  2/6
   GDP nowcast USA      2026-06-04  2.10  TBD                  —
   GDP nowcast DEU      2026-06-01  0.40  0.45    +0.05 -0.2  1/6
   ...
```

Columns:
- Indicator
- Country
- Forecast vintage
- Horizon
- Predicted (P50)
- Actual
- Error (signed)
- Z-score (signed)
- Rank (vs comparator pool)
- Methodology link
- Vintage view link

Pagination: 50 rows/page, virtualized.

Filters: indicator, country, horizon, year, methodology version, has-post-mortem.

Sort: date (default desc), error (worst first), z-score, rank.

Export: CSV download of the entire ledger. Open via Datasette mount (`/data/ledger`).

## How we score (methodology)

A section explaining the scoring:

- **CRPS** — what it is, why we use it
- **PIT** — uniform-distribution check
- **Brier** — for binary forecasts
- **Rank** — vs the comparator pool
- **Z-score** — error relative to forecast spread

Plus the rules:
- We score against the *first* actual release, not subsequent revisions (to avoid "we got the revision right")
- We log the actual at the moment of release, vintaged
- We don't re-score historical forecasts when methodology changes (the old methodology's forecasts retain their score)

## Compare OPENGEM to other forecasters

A calibration plot per indicator showing OPENGEM, WEO, OECD, Bloomberg consensus (where licensable), and others.

```
   USA CPI calibration (4Q horizon, last 24 vintages)
   ────────────────────────────────────────────────
              actual
       1.0 │            ● OPENGEM
           │
       0.5 │      ● OPENGEM
           │   ●
       0.0 │──────────────●─────
                  predicted

   Brier scores:
    OPENGEM    0.058
    NY Fed     0.061
    WEO        0.092
    OECD       0.087
    Bloomberg  0.075   (where available)
```

Honest: we publish where we beat and where we lose. Discipline.

## The "calibration grid" — every indicator × every horizon

A matrix view:

```
                  CRPS (lower = better)
           Nowcast  3M    6M    12M   24M
   ─────────────────────────────────────────
   USA CPI    0.12  0.18  0.25  0.32  0.45
   USA GDP    0.21  0.28  0.33  0.42  0.61
   DEU CPI    0.18  0.22  0.28  0.36  0.51
   ...
   ─────────────────────────────────────────
   Comparator (best of pool):
   USA CPI    0.14  0.17  0.23  0.31  0.42
   USA GDP    0.19  0.27  0.31  0.40  0.58
   ...
```

Color cells by relative rank: green when OPENGEM is best, red when worst.

This is the at-a-glance answer to "how is OPENGEM doing across the board?"

## Quarterly retrospective

Each calendar quarter, OPENGEM publishes an editorial retrospective:
- Stats summary
- 3 worst misses with post-mortems
- 3 best beats
- Methodology changes shipped
- Roadmap for next quarter

Permalink: `/accountability/retrospective/<year>-Q<n>`.

## The "open ledger" RSS feed

Every forecast scoring event emits an Atom entry. Subscribers see:
- New miss → new entry
- New post-mortem → new entry
- Quarterly retrospective → new entry

See L179 for feed catalog.

## URL contract

```
/accountability
/accountability?indicator=cpi-yoy&country=usa
/accountability?horizon=4q&year=2026
/accountability/postmortem/<id>
/accountability/retrospective/<year>-Q<n>
```

## The "no asterisks" rule

Three explicit non-tricks:

1. **No survivorship bias.** Every forecast we ever published is in the ledger, including the ones from beta methodology versions we later changed.

2. **No selective scoring.** Every scored forecast counts. We don't drop bad ones because of "data quality issues" — we either rerun with a documented exception or accept the bad score.

3. **No fixed reference.** When the indicator was revised after release, we score against the first release (the value the forecast was actually trying to predict). We disclose the revision separately.

## The "compare to me" view

For paid users, an "add my forecasts" feature: upload your own forecasts (CSV format), OPENGEM scores them alongside, you see your performance.

V2 — V1 ships with OPENGEM-only ledger.

## Implementation

- Backend: scored forecasts stored in `accountability_ledger` table
- Daily job: pulls newly-released actuals, scores all forecasts with that release as target
- Page: server-rendered, virtualized table, sortable
- Cache: 1h on aggregates, 5min on recent additions

## Performance

- 12K+ row table: virtualized via TanStack Table
- Filters apply server-side for large filters, client-side for small
- Full CSV export: 5-second job, cached

## The asymmetric move

No other macro forecaster publishes this page. Goldman doesn't. JPM doesn't. IMF doesn't (they publish WEO calibration in research papers, with multi-year lag). Bloomberg has internal scoring nobody outside ever sees.

OPENGEM's accountability page is the artifact that, five years from now, people cite as proof that public-accountability macro is viable.

It's also the page we'd be terrified to launch with — because once it's public, every miss is a story. That's the point. It forces us to be good.
