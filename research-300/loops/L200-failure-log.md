# L200 — Failure Log: When We Got It Wrong + Post-Mortem Template

**Loop**: 200 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

The failure log is the artefact L001 names directly: *"Every miss, with a post-mortem in the same place the original was published."* This loop pins the entry schema, the post-mortem template, the page design, and the cross-linking that makes failures findable from the forecasts they came from.

A failure log without post-mortems is theatre. A failure log with thoughtful post-mortems is the asymmetry that beats the cartel.

## What counts as a "miss"

Five canonical miss categories:

1. **Direction miss** — realised outcome moved in the *opposite* direction of the central forecast (e.g. forecast predicted +0.5% GDP, realised -1.2%). The sign was wrong.
2. **Magnitude miss** — direction was right but the realised value fell *outside the 80% band* (P10-P90). The bands were too narrow.
3. **Calibration drift** — PIT-KS p-value fell below 0.05 on a cell for two consecutive evaluations. The forecast distribution is empirically miscalibrated.
4. **Scenario miss** — a fired scenario did not materialise within 12 months (or *did* materialise without firing).
5. **Replay failure** — replay-and-diff CI (L186) found a forecast that does not byte-replay. Reproducibility broken.

Each miss type triggers a different post-mortem template, but all live in the same failure log surface.

## The failure log entry schema

```json
{
  "schema": "opengem.failure_entry.v1",
  "entry_id": "fail_2025-Q1_USA_GDP_4Q_direction",
  "miss_class": "direction_miss",
  "country": "USA",
  "indicator": "GDP-real-yoy",
  "horizon": "4Q",
  "scoring_period": "2025-Q1",
  "forecast_vintage": "2024-Q1",
  "forecast_at_vintage": {
    "point": 1.8,
    "p10": 0.6,
    "p90": 3.0
  },
  "realised": {
    "value": 2.85,
    "vintage": "2025-04-25",
    "z_score_from_p50": 1.3,
    "inside_p10_p90": true
  },
  "miss_magnitude": {
    "delta_from_point": 1.05,
    "delta_from_p50": 1.05,
    "delta_outside_band": 0
  },
  "post_mortem_url": "https://opengem.org/failures/fail_2025-Q1_USA_GDP_4Q_direction",
  "linked_forecasts": [
    "fcst_2024-Q1_USA_GDP_4Q_OPENGEM-L3-BMA_v2.8.0"
  ],
  "linked_envelopes": [
    "env_2024-Q1_USA-quartet-L3-BMA-v2.8.0"
  ],
  "created_at": "2025-04-25T12:30:00Z",
  "post_mortem_published_at": "2025-05-02T10:00:00Z",
  "remedial_action_taken": [
    {"action": "increased BVAR prior tightness", "issue_url": "github.com/opengem/opengem-1/issues/447"},
    {"action": "added employment-to-population ratio as DFM factor", "pr_url": "github.com/opengem/opengem-1/pull/452"}
  ],
  "lessons_learned": [
    "Q1 2024 vintage data missed the labour-market acceleration that became visible Q2-Q3.",
    "DFM factor set was static; needed online refit on emerging structural break."
  ],
  "miss_recurred": false
}
```

## The post-mortem template

```markdown
# Post-Mortem: {entry_id}

**Country**: {country}
**Indicator**: {indicator}
**Horizon**: {horizon}
**Scoring period**: {scoring_period}
**Forecast vintage**: {forecast_vintage}
**Realised**: {realised}
**Miss class**: {miss_class}

---

## What we forecast

At {forecast_vintage} we forecast {country} {indicator} at {horizon}-ahead to be
{forecast_point}% (P10-P90 = {p10}% to {p90}%).

[link to the original forecast.v1 JSON and its envelope]

## What actually happened

At {scoring_period} the realised value was {realised}%. This is {delta} pp from
our point estimate, or {z} z-scores from our P50.

The realised value was {inside_or_outside} our 80% band.

## What we got wrong

Walk through, with charts and tables, the gap between our forecast distribution
and the realised value. Specifically:

1. Which inputs were available at vintage time but did not load enough signal
   into the model?
2. Which inputs were *not yet visible* at vintage time but would have changed
   the call?
3. Did the BMA combiner weight a weak variant too heavily?
4. Did consensus (WEO, OECD EO) miss in the same direction? (If yes, the miss
   is at least a "consensus miss". If no, OPENGEM-specific.)

## Why we got it wrong

Diagnose. Plain prose, ≤500 words. State the model failure mode in technical
language but accessible to a numerate reader. No blame on individuals.

## What we changed

List concrete code / weight / data changes:
- {action_1} (PR / issue link)
- {action_2}
- ...

Each action must link to a GitHub PR or issue. No vague "we will be more
careful."

## Did the change work?

Once N≥4 quarters have passed since the fix:
- Has the miss class recurred?
- What does the PIT plot look like now?
- What does the leaderboard rank look like?

This section is updated *retroactively* on the post-mortem. The entry's
`miss_recurred` field is recomputed quarterly.

## Lessons learned

Bullet list, ≤200 words. What we now know that we did not before.

## Inputs to track-record badges

Any badges this forecast lost as a result of this miss:
- {badge_id}: lost on {date}, regained on {date}, or "not yet regained"

---

*Generated by the failure-log engine. Reviewed by {maintainer}. Open for
comments via GitHub Discussions: [discussion_url]*
```

## The failure log page

The page (`opengem.org/track-record` and per-country `/track-record/{country}`) shows:

1. **Headline summary**: "{N} misses logged over the last 12 months across all forecasts. {M} post-mortems published. {K} remedial PRs merged."
2. **Filterable table** of failure entries, sortable by: date, country, indicator, miss class, z-score of miss.
3. **Per-entry card** with the miss summary, post-mortem link, related forecasts, and remedial action checklist.
4. **Auto-refresh** on new entries; RSS feed.
5. **"Big misses"** highlight reel — the largest 5 misses by z-score in each year, shown as a wall of shame the dashboard does not hide.

```
TRACK RECORD — USA
─────────────────────────────────────────────────────────────────────────
Total forecasts (1Q-4Q-2Y) since 2014: 5,832
Bands (P10-P90) covered the realised value: 81.4% (target 80%)
Direction misses (P50 wrong sign): 247 (4.2%)
Calibration drift events: 12

RECENT MISSES (last 12 months)
─────────────────────────────────────────────────────────────────────────
2025-Q1 — GDP-4Q ahead — direction miss (forecast 1.8%, realised 2.85%)
  → post-mortem: "Q4-2023 labour-market acceleration underweighted"
  → remedial: PR #452 (added employment-to-population factor)
  → status: ✓ fixed; miss did not recur in 2025-Q2/Q3 vintages

2024-Q4 — CPI-1Q ahead — magnitude miss (band 2.0-3.4%, realised 3.7%)
  → post-mortem: "Energy-component shock; DFM did not pick up"
  → remedial: PR #438 (added natgas spot to L3 features)
  → status: under review (3 quarters since fix; PIT still drifting)

2024-Q2 — Scenario "Soft Landing" probability mis-calibration
  → post-mortem: "Probability of 70% was too high; realised path was hard landing"
  → remedial: PR #421 (recalibrated landing-partition model)
  → status: ✓ fixed
```

## Cross-linking from forecasts

Every forecast on the dashboard (L195) carries a "miss log" link that filters the track-record page to that `(country, indicator, horizon)`. The link shows the count of historical misses inline:

```
USA GDP-real-yoy 4Q-ahead
[chart]
[3 misses in last 24 months ▶]   ← clickable, opens filtered track record
```

A forecast with zero historical misses still shows "0 misses in last 24 months" (honest absence). A forecast with many misses shows the count prominently — readers should weight the forecast accordingly.

## Auto-detection cadence

The engine evaluates miss conditions on every:

- New realised data point landing in the vintage store (direction + magnitude miss checks).
- Weekly V&V matrix re-run (calibration drift checks).
- Scenario resolution event (NBER recession dating update, etc.).
- Replay-and-diff CI failure.

Detection is automatic; the *post-mortem* is human-authored within 7 days. The entry is published immediately with `post_mortem_published_at = null` and a "post-mortem pending" badge. The post-mortem fills in by the deadline.

If the deadline is missed, an automatic "post-mortem overdue" badge appears, visible to the public. We do not get to procrastinate on our misses.

## API contract

```
GET /v1/track-record/{country}                  → all entries for country
GET /v1/track-record/{country}/{indicator}      → filtered
GET /v1/failures/{entry_id}                     → single entry
GET /v1/failures/{entry_id}/post-mortem         → markdown post-mortem
GET /v1/track-record/feed.rss                   → RSS feed of all entries
```

## What this loop produced

- Five canonical miss categories.
- `failure_entry.v1` schema with linked envelopes and remedial actions.
- Post-mortem markdown template.
- Failure log page design (filterable table + highlight reel).
- Cross-linking from forecasts (L195 miss-log link).
- Auto-detection cadence per miss type.
- 7-day post-mortem deadline with public-visible "overdue" badge.
- API contract.

## What comes next

- **L201** — hyperparameter sweep tracking referenced from remedial actions.
- **L184** — leaderboard reflects miss accumulation.

## Related

- [[L001-vision-statement]] — "publishes its mistakes" — operationalised here.
- [[L181-forecast-object-schema]] — `miss_log_url` points at this page.
- [[L182-forecast-vintage-lineage]] — envelope referenced.
- [[L186-reproducibility-envelope]] — replay-failure source.
- [[L192-forecast-revisions]] — drift-toward-error feeds this.
- [[L193-calibration-plots]] — drift detection.
- [[L199-trust-signals]] — badges lost at miss events.
