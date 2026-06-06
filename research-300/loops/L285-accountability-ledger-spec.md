# L285 — Accountability Ledger Page (The Spec)

**Loop**: 285 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis of this loop

`/accountability` is the most important page on the dashboard. Every other page exists to surface data; this one exists to make the data trustworthy. The prototype at `/app/accountability/page.tsx` shows the surface. This loop specifies the full content model — the data structures, the edit discipline, the post-mortem template that companion-loop [[L286]] expands on, and the governance that ensures the page does what the brand promises.

A bad accountability ledger is worse than no accountability ledger. If we publish a half-finished page with stale numbers and missing post-mortems, the brand inverts — we become "the people who pretend to publish their misses." This loop specifies the discipline that prevents that failure mode.

---

## The content model

The page has four blocks that map to a JSON content schema:

```json
{
  "schema": "opengem.accountability_page.v1",
  "snapshot_at": "2026-06-06T00:00:00Z",
  "scoreboard": {
    "published": 14283,
    "scored": 11902,
    "out_of_band": 2117,
    "pending_scoring": 264,
    "since": "2024-01-01"
  },
  "recent_misses": [
    {
      "rank_by_magnitude": 1,
      "entry_id": "fail_2025-Q2_USA_GDP_4Q_direction",
      "vintage": "2025-Q2",
      "country": "USA",
      "indicator": "gdp_yoy",
      "horizon": "4Q",
      "forecast_point": 1.4,
      "actual": 2.6,
      "miss_pp": 1.2,
      "rmse_rank_at_vintage": 47,
      "summary": "Persistent Q1-2025 revisions pushed GDP surprise outside our 80% band; component DFM under-weighted services consumption.",
      "post_mortem_url": "/postmortem/usa-gdp-2025q2",
      "post_mortem_status": "published",
      "remedial_action_count": 2
    }
  ],
  "publication_discipline": [
    {
      "principle": "Vintage permanence",
      "body": "Every published forecast is permanent. No silent retract, no edit-in-place. If we change method, we publish a new vintage with a forward link."
    }
  ],
  "scoring_methodology_url": "/methodology/scoring",
  "calibration_target": {
    "band": "80%",
    "max_out_of_band_rate": 0.20
  },
  "calibration_current": {
    "band": "80%",
    "current_out_of_band_rate": 0.178
  }
}
```

The JSON is what the dashboard renders from, what the API serves at `/v1/accountability/snapshot`, and what the auto-archive bot snapshots to GitHub nightly. Any change to the page reflects a change to the JSON; any change to the JSON is git-traceable.

---

## The four blocks (visual + content spec)

### Block 1 — Header

```
ACCOUNTABILITY LEDGER

Every forecast OPENGEM has ever published. Scored against truth at horizon.
Misses are not retracted — they are post-mortemed in place. This is the page
that doesn't exist anywhere else.
```

Three lines, no more. The third line is the brand-defining sentence. It does *not* change between releases without a governance review.

### Block 2 — Scoreboard (four tiles)

Four metrics laid out as identical tiles:

| Tile | Value | Sub-label |
|---|---|---|
| Forecasts published | 14,283 | since 2024-Q1 |
| Scored | 11,902 (83.3% of publishable) | (green badge) |
| Outside band (miss) | 2,117 (17.8% of scored) | target ≤ 20% (green if under) |
| Pending scoring | 264 | awaiting truth print |

The four tiles match the design density of all other dashboard tiles. The "(% of scored)" calculation is exposed because the buyer (Marcus, Nadia) cares about the *rate* not the count.

Below the four tiles, a small line: "Updated: [as-of timestamp]. Snapshot archive: [link to GitHub archive of this snapshot]." The snapshot archive line is critical — it proves the numbers were not retroactively edited.

### Block 3 — Recent misses (top 3 by magnitude)

A table with the columns: vintage, country, indicator, horizon, forecast, actual, miss, "why" (one-line), post-mortem link.

Three rows visible. "All 2,117 misses →" link to the full filterable table at `/accountability/misses`.

Critical UX detail: "Every miss above has its own URL. The URL was assigned *before* we knew we'd miss. That's the promise." This is the in-page proof that the misses are not curated after the fact.

### Block 4 — Publication discipline

Five bullets, each a 1-sentence principle + 1-sentence body. Drawn from [[L008]] and [[L200]]:

1. **Vintage permanence.** Every published forecast is permanent. No silent retract, no edit-in-place. If we change method, we publish a new vintage with a forward link.
2. **Miss-in-place.** A missed forecast doesn't leave the page it was on. A post-mortem appears below it.
3. **Consensus side-by-side.** Every forecast shows WEO, OECD EO, FRB SEP, ECB SPF where available — so a miss is visible in context.
4. **Reproducibility envelope.** Git SHA, data lockfile hash, container digest, generated-at timestamp. Anyone can replay any vintage.
5. **Calibration is a target.** The ledger commits to ≤20% out-of-band rate at the 80% band. When it drifts above, we say so on this page.

These bullets *do not change between releases without a governance review*. They are brand commitments.

---

## The edit discipline

A change to the accountability ledger page (header text, scoreboard formula, publication-discipline bullets, post-mortem template) requires:

1. **PR opened against `opengem/accountability-ledger` repo** (per [[L272]] ADR-025).
2. **Founder approval + 2-of-3 advisory board signoff** (the L271 governance model).
3. **24-hour cooling period** before merge — gives the team a chance to second-guess in cold blood.
4. **Changelog entry on `/governance/changelog`** with rationale.
5. **Prior version preserved at `/accountability/v[N]`** with full historical access.

This is more friction than any other page on the dashboard. Intentionally. The whole brand depends on this page being the same page Marcus saw last quarter.

The *data* on the page (scoreboard numbers, recent misses) updates automatically. The *content structure* (the 4-block layout, the bullets, the brand sentence) does not change without a deliberate amendment.

---

## The post-mortem template (link to L286 for the full spec)

Per [[L200]] and [[L286]], each entry in the misses table links to a post-mortem at `/postmortem/[slug]`. The template enforces:

```
Title: Post-Mortem: {country} {indicator} {horizon} {vintage}

Sections (required, in order):
1. What we forecast
2. What actually happened
3. What we got wrong
4. Why we got it wrong
5. What we changed
6. Did the change work? (filled in N≥4 quarters later)
7. Lessons learned
```

The post-mortem itself lives in the `opengem/accountability-ledger` repo as a Markdown file with YAML frontmatter. The dashboard renders from the repo at build time. Editorial discipline: every post-mortem PR requires founder + at least one external reviewer (advisory board member or community-confirmed-miss reporter) approval.

A post-mortem that has not landed within 30 days of a confirmed miss triggers a "post-mortem overdue" badge on the misses table, *publicly visible*. We do not get to procrastinate.

---

## Scoring methodology (linked, not on-page)

The scoring methodology page at `/methodology/scoring` is dense (~3,000 words) and exists separately. It specifies:

- How CRPS, log-score, PIT, MAE, RMSE are computed per indicator and horizon.
- The "outside band" definition (realized value not within the P10-P90 interval).
- How nowcasts are scored vs forecasts (different realized-data alignment).
- The reproducibility envelope (envelope ID, data lockfile, container digest).
- The "miss class" taxonomy from [[L200]] (direction / magnitude / calibration / scenario / replay).

The accountability page does *not* re-explain the methodology; it links to it. A reader who wants to question the calibration math goes to `/methodology/scoring` and finds the answer there.

---

## Calibration current vs target — the inline honesty signal

The block 4 bullet "Calibration is a target. The ledger commits to ≤20% out-of-band rate at the 80% band. When it drifts above, we say so on this page" requires a *visible* indicator that shows current calibration vs target.

Implementation: a small green / red badge near the scoreboard.

```
Current: 17.8% out of band (target ≤20%) ✓ on track
```

or

```
Current: 22.3% out of band (target ≤20%) ✗ drifted; corrective post on /governance
```

If we drift above 20%, the dashboard does not hide it. We add a `<Banner>` to the accountability page with a link to a governance post explaining the drift. This is the L008 promise operationalized at the data-display level.

---

## API endpoints

```
GET  /v1/accountability/snapshot          → current JSON snapshot
GET  /v1/accountability/snapshots/{date}  → historical snapshot
GET  /v1/accountability/misses            → filterable misses list
GET  /v1/accountability/calibration       → current vs target time series
GET  /v1/postmortems                      → list all post-mortems
GET  /v1/postmortems/{slug}               → single post-mortem
GET  /v1/accountability/feed.rss          → RSS of all new entries
```

Every endpoint is public (no auth required). The data is published; we want it cited.

---

## Versioning and archival

- **Nightly snapshot to GitHub**: a bot commits the day's `snapshot.json` to `opengem/accountability-ledger/snapshots/YYYY-MM-DD.json`. This is the canonical archive. Git history is the proof that numbers are not retroactively edited.
- **Quarterly snapshot to Internet Archive**: founder manually submits the accountability page to the Wayback Machine quarterly. Belt-and-suspenders archival.
- **Annual published retrospective**: the [[L299]] template's annual variant includes the full year of accountability snapshots compressed into a single ZIP, mirrored to multiple hosts.

---

## What this page is *for*

The page is for three audiences, in order of importance:

1. **The journalist who's about to write about OPENGEM and needs to verify the "publishes its own mistakes" claim.** The accountability page is the answer they get to. The four-tile scoreboard is the screenshot they include.

2. **The institutional buyer (Nadia) who's evaluating whether to white-label OPENGEM at $5k/mo.** They check the calibration target vs current to see if our forecasts are within stated bands. If yes, the buying decision becomes easier.

3. **The reader who wants to be inspired by a working model of accountability infrastructure.** This is the long-arc audience — the L008 brand seeker who will become a community advocate.

The page is *not* for:
- Day traders looking for forecast alpha.
- Crypto buyers looking for inside info.
- Academic referees doing a methodology review (they go to `/methodology/scoring` for that).

---

## What this loop produced

- A JSON content model (`opengem.accountability_page.v1`).
- Four block specs (header / scoreboard / recent misses / publication discipline).
- An edit discipline that gates changes through founder + advisory board + 24h cooling.
- A calibration indicator that surfaces drift visibly.
- Public API endpoints for the accountability data.
- A versioning + archival strategy (nightly GitHub, quarterly Internet Archive, annual ZIP).
- A statement of what the page is for and what it isn't.

## What comes next

- **L286** — the failure-log page, the companion spec for individual miss post-mortems.
- **L298** — the literal post-mortem template specified by this loop.
- **L299** — quarterly retrospective uses the snapshot history.

## Related

- [[L008-differentiation]] — promise 2 (name every miss) → this page
- [[L200-failure-log]] — Phase 4 failure-log spec → this page surfaces the data
- [[L286-failure-log-page]] — the format for individual miss post-mortems
- [[L298-postmortem-template]] — the literal template
- [[L299-quarterly-retrospective]] — uses snapshots from this page
