# L298 — Post-mortem template for forecast misses

**Loop**: 298 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The template

Every miss post-mortem is a markdown file at `/postmortem/<iso3>-<indicator>-<vintage-date>` with this *exact* structure. No exceptions. Editorial discipline depends on the format being mechanical.

```markdown
# {Country} {Indicator} {vintage_period} forecast — missed

**Vintage**: {vintage_id}
**Forecast**: {point}% (80% band {p10}–{p90})
**Actual**: {actual}%
**Miss**: {actual - point}pp ({outside / inside} 80% band)
**Days from vintage to truth**: {N}
**Model**: [{model_id}]({model_card_url})

## The miss

What happened, in one paragraph. The reader's first question is "by how much" — answer it.

## What our model did NOT see

The honest version. What signal was in the data that our model didn't weight enough, or what signal wasn't in the data at the vintage we forecast.

## What changed in next vintage

The concrete model / data / methodology change in subsequent vintages. Link to the diff in the model card history. If no change was made (intentionally — we don't want to retro-fit), say so explicitly:

> No methodology change. This miss is within the calibration envelope (80% band miss rate target ≤20%; current cumulative miss rate {X}%). Adjusting after a single observation would be over-fitting.

## What we will NOT change

The discipline statement. We do not adjust priors after one miss. We do not silently re-weight components. We do not retract.

## Consensus comparison (was anyone right?)

How WEO / OECD EO / SEP / SPF / individual-bank forecasts performed on the same period.

| Source | Forecast | Miss |
|---|---|---|
| OPENGEM (v{vintage}) | {p50}% | {miss}pp |
| WEO ({date}) | {weo}% | {weo_miss}pp |
| OECD EO ({date}) | {oecd}% | {oecd_miss}pp |
| ... | ... | ... |

Whether others missed too matters editorially. If consensus also missed, the discipline message is "no one had the signal." If consensus had it and we didn't, that's the modeling failure to write up.

## What this means for current forecast

If our current vintage's forecast for {country} {indicator} is informed by what we learned here, link to that current vintage. Otherwise be silent — no retroactive narrative.

## Reproducibility envelope

- `vintage_id`: {vintage_id}
- `git_sha`: {git_sha} ([browse]({github_commit_url}))
- `data_lockfile_hash`: {hash}
- `container_digest`: {digest}
- `generated_at`: {timestamp}

## Signed

{Edgardo / contributor name}, {date of post-mortem}.

Comments are open at [GitHub discussion link]({url}).
```

## The "what we will NOT change" section is load-bearing

Most institutional post-mortems include a "remediation plan" section. OPENGEM's editorial discipline says: usually, we will NOT remediate after a single miss. The 80% band is calibrated to miss 20% of the time. A single miss is *expected behavior*, not a bug.

The "what we will NOT change" section forces us to defend that discipline explicitly to a reader who might otherwise expect dramatic methodology changes. It also is the editorial signature that distinguishes OPENGEM's post-mortems from typical corporate "lessons learned" PR.

When we DO change methodology, it's after:
- A pattern of misses (3+ consecutive misses in the same cell, OR cumulative miss rate >25% on the cell)
- OR a structural break we can name (regime shift, data revision, methodology paper that supersedes ours)

The change is documented in the model card history, linked from the post-mortem, with a clean diff.

## What goes on the consensus comparison

Critical editorial choice: we **always** include consensus comparison. Even when we beat consensus (less interesting for "publishes its mistakes" narrative). Even when consensus also missed badly. The discipline is: we publish *our* miss in the context of *what others were forecasting*.

This protects against the "we look bad" framing — readers see the miss as part of a forecasting-industry pattern, not a unique OPENGEM failure.

## Approval flow

Post-mortems are NOT reviewed by an editor before publication. Single-author, single-sign. The author commits via git, the CI pipeline auto-deploys, the post-mortem lives at its URL within ~10 minutes of the miss being scored.

Why no review: review introduces delay, and delay erodes the credibility of "miss-in-place" (every day the post-mortem is delayed, the reader's impression is "they're spinning"). One-author, fast, with reader comments open as the QA mechanism.

## When the post-mortem itself contains an error

We append a `## Update {date}: correction` section at the bottom. We do NOT silently edit the body. The original wording stays. This is consistent with the rest of OPENGEM's editorial discipline.

## What this loop produced

- The literal markdown template
- The "what we will NOT change" load-bearing section
- The single-author no-review approval flow
- The append-only correction discipline

## Related

- [[L200-failure-log]] (in forecast mechanics) — the upstream concept
- [[L286-failure-log-page]] (in Phase 6) — the page that lists post-mortems
- [[L259-track-record-page]] (in Phase 5 batch) — where post-mortems are linked
- [[L008-differentiation]] — the editorial discipline this enforces
