# L206 — Real-Time vs Final Estimates

**Loop**: 206 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

A "real-time" data point is the value as it was first published; a "final" estimate is the same period's value after years of revisions. These can differ substantially: US 2008-Q4 GDP was reported -3.8% on first vintage; later revised to -8.5%. A forecaster judged on the wrong vintage gets the wrong story about their skill.

This loop pins how OPENGEM displays both, scores against both, and lets the reader switch.

## The two estimates

| Estimate | What it is | Use case |
|---|---|---|
| **Real-time (vintage-as-of-T)** | Value as known at time T. Read from the vintage store at vintage_at ≤ T. | Replicating what was actionable at T; computing forecast errors against the data the forecaster saw |
| **Latest revised** | Most recent vintage of the same period. | Asking "what really happened" |
| **First-vintage** | Value at first publication. | Surprise index baseline (L191); first-vintage error |
| **Final-vintage** | Heuristically, vintage 8+ quarters after the period; treated as ground truth | V&V scoring; "true" outcome for back-testing |

OPENGEM's vintage store (`opengem-vintage`) carries every vintage and can resolve any of these on demand. This loop pins which is shown where.

## Display rules per surface

| Surface | Default estimate shown | Toggleable to |
|---|---|---|
| Country page time-series chart | Latest revised | Real-time, First-vintage |
| Indicator page time-series chart | Latest revised | Real-time, First-vintage |
| Forecast chart "realised history" | Latest revised (left of `now`) | Real-time, First-vintage |
| Forecast chart "scoring point" (post-target) | First-vintage AND latest revised both shown | n/a (both always shown) |
| Backtest scoring "actual" | Final-vintage (= "the eventually-revised value") | Configurable in `vv_results` schema |
| Surprise index input "realised" | First-vintage | Toggleable secondary baseline |
| Coverage page tile | Latest revised | n/a |
| Methodology page reference | All four shown side by side | n/a |

The rationale: the *display* defaults to latest revised because that is what readers usually want to know ("what is GDP currently believed to have been"). The *scoring* defaults to final-vintage to give the model an honest, settled target.

## The vintage selector

On any time-series chart, a small selector lets the user toggle:

```
[ Realised: latest revised ▼ ]
  ├── Latest revised (default)
  ├── First-vintage (real-time as known then)
  ├── Real-time as of: 2026-01-15  [date picker]
  └── Show all vintages overlaid
```

The "show all vintages" mode renders a faded line per vintage, exposing the revision triangle directly. The most-recent vintage is solid; older vintages fade with age.

## The revision triangle

Each `(country, indicator)` has a revision triangle: for every period, how the value evolved across vintages.

```
Period      vintage:    2009-Q1   2009-Q3   2010-Q1   2011-Q1   ...   final
2008-Q4    -3.8%       -5.4%     -6.8%     -8.2%      ...        -8.5%
2009-Q1    -6.1%       -5.7%     -4.9%     -4.4%      ...        -4.4%
2009-Q2    n/a          0.3%      0.9%      1.7%      ...         2.0%
...
```

The revision triangle is published as a downloadable table (CSV + Parquet) per `(country, indicator)`. Power-users (academics, journalists) consume this directly.

## Scoring forecasts: which vintage?

Per R24 / R99, the V&V matrix scores against the **final-vintage** target. Definition:

> The final-vintage value for period P is the value as published in the most recent vintage available at scoring time S, where S ≥ P + 8 quarters.

The 8-quarter rule matches BEA practice: by 8 quarters out, most revisions have happened. We do *not* wait for the 30-year benchmark revisions; the 8-quarter rule is the right operational definition of "eventually revised."

The scoring decision is documented in each cell's methodology page. A reader can request the same forecast re-scored against the first-vintage outcome ("how would this score against real-time data?") via:

```
GET /v1/forecasts/{forecast_id}/score?target_vintage=first
GET /v1/forecasts/{forecast_id}/score?target_vintage=final          (default)
GET /v1/forecasts/{forecast_id}/score?target_vintage=at_T&T=2027-01-31
```

This is the open-source replay surface: anyone can score against whatever vintage they want. We just publish the default that we use.

## Why this matters

Three concrete reasons:

1. **Forecasters' skill looks different against different vintages.** A forecast that was 1 pp off the first-vintage GDP may be exactly right against the eventually-revised value. *Scoring against real-time only* under-credits forecasters who anticipated the revision (and over-credits forecasters who lucked into matching the initial-release noise).

2. **Backtests can leak revision information** if real-time vintages aren't used during training. A model trained on final-vintage data will learn to predict the eventually-revised values, which were not observable at the original vintage time. This is "the revision-trap" — common in academic macro and a known generator of spurious forecast skill.

3. **The friend cares about both.** The YouTuber persona (L001) wants to talk about what was reported (first-vintage) and what we now believe (latest revised). Both have rhetorical roles. The dashboard supports both with clear labels.

## The "vintage-correct" badge

A forecast earns the `vintage-correct` badge (L199) only if its training and inference both used vintage-correct inputs — i.e. for every input series s used at time t, the value used was from a vintage with `vintage_at ≤ t`. The L186 envelope captures this; the lineage record (L182) records every vintage_at. Backtests against final-vintage targets do not invalidate the badge; using final-vintage inputs during forecasting does.

## Storage and resolution speed

The vintage store indexes `(series_id, period, vintage_at)`. Resolution is a single index lookup. A typical query "give me USA GDP for 2026-Q1 as known at 2026-02-15" returns in ~5 ms.

The "all vintages overlay" view requires N queries (one per vintage); for a 30-year history with quarterly vintages, that's ~120 queries. The dashboard batches them into a single round trip via `GET /v1/realised/all-vintages?series=...&period_from=...&period_to=...` returning a 3D table.

## Data adapters and vintage capture

Each upstream-agency adapter writes every snapshot to the vintage store at the moment of release. The `vintage_at` timestamp is the *receipt* time at the adapter, accurate to seconds. This is the timestamp used for backtest replay.

For series that publish without explicit vintage history (some smaller central banks), the adapter creates a synthetic vintage at the time of first scrape; subsequent overwrites are captured as new vintages. We are explicit in the model card about which series have authoritative vintage and which are synthetic.

## Pitfalls

1. **The 8-quarter rule has corner cases.** Some series get revised much later (e.g. national accounts benchmark revisions every 5 years). *Mitigation*: the methodology page flags series where >5% revisions still happen post-8Q. For those, scoring uses the latest available vintage at scoring time.

2. **Confusing the user.** Two simultaneous values for "USA 2008-Q4 GDP" is genuinely confusing. *Mitigation*: clear labels on every chart ("realised, latest revised"); the toggle is sticky; the methodology page has a single explainer.

3. **Cross-country comparability.** Different countries have different revision practices. *Mitigation*: per-country revision-practice notes in the country page; scoring uses each country's own final-vintage rule.

## What this loop produced

- Four vintage classes (real-time, latest, first, final).
- Display defaults per dashboard surface.
- Vintage selector UX.
- Revision triangle as downloadable artefact.
- Scoring rule: final-vintage, 8-quarter lag.
- API for arbitrary-vintage re-scoring.
- Vintage-correct badge tie-in.

## What comes next

- **L207** — density aggregation rules across multiple components.
- **L209** — causal-vs-forecast taxonomy referenced here.

## Related

- [[opengem-vintage]] — vintage store underneath.
- [[R02-vintage-coverage]] — Tier-V/Tier-T coverage.
- [[R24-backtest-engine]] — scoring engine respects final-vintage rule.
- [[L181-forecast-object-schema]] — `base_period`, `scoring_period` semantics.
- [[L182-forecast-vintage-lineage]] — vintage_at captured per series.
- [[L191-surprise-index]] — uses first-vintage baseline.
- [[L199-trust-signals]] — vintage-correct badge.
