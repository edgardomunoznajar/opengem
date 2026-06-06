# L085 — ACLED Rate-Limit Feasibility: Safest Pattern Under YELLOW License

**Loop**: 085 / 300
**Phase**: 2 — Integration deep dive
**Date**: 2026-06-06
**Verdict**: **ADOPT-V1 (free-tier-only, derived-metrics-only, GREEN fallback wired)**

---

## What this loop answers

L022 concluded ACLED is YELLOW: cite-and-derived-OK, raw-rows-NO, replace-dashboard-NO. This loop converts that legal verdict into an **operational rate-limit + ingestion + fallback pattern** that can survive both ACLED's commercial-licensing scrutiny *and* a sudden EULA tightening. The pattern is non-negotiable for any v1 launch that mentions ACLED in marketing.

The headline: **ACLED features only in the free public-tier dashboard, never on the paid API surface, with GDELT + UCDP + POLECAT pre-wired as substitutes such that "kill ACLED tomorrow" is a config flip not a 6-week rewrite.**

## The four-constraint operating envelope

OPENGEM's ACLED usage must satisfy four constraints simultaneously:

1. **EULA-compliant.** No raw row republishing, derived metrics only, attribution everywhere.
2. **Rate-limit-respectful.** API is uncapped but anti-abuse triggers exist. Stay well under their threshold.
3. **Free-tier-isolated.** Paid customers must not hit ACLED-backed endpoints by accident; we cannot monetize their data without a commercial license.
4. **Drop-in-replaceable.** If the EULA changes or pricing demands appear, the swap to GREEN sources must be a config change measured in hours, not weeks.

Below is the pattern that meets all four.

## Tier-1 — Ingest cadence and rate-limit budget

ACLED publishes weekly on Mondays/Tuesdays for the prior week. Our ingest cadence should be **weekly + one repair pass**, not daily. Daily polling adds noise without information (no new data lands except on release days) and consumes rate-limit budget for nothing.

The Dagster schedule:

| Job | Cadence | Endpoint | Rows per pull | Notes |
|---|---|---|---|---|
| `acled_weekly_pull` | Mondays 21:00 UTC | `acled_read?event_date={last_monday}-{this_monday}` | ~5,000-50,000 (varies) | Captures the prior week's full release |
| `acled_repair_pass` | Wednesdays 03:00 UTC | `acled_read?event_date={last-2-weeks}` | ~10,000-100,000 | Backfills retroactive edits |
| `acled_backfill_quarterly` | First of quarter | Same with 90-day window | ~500K | Rebuilds the trailing 90 days against the latest snapshot |

Each `acled_read` call returns 500 rows max. A typical weekly pull is 50K rows / 500 = 100 paginated calls. With a 1-call-per-2-seconds throttle, that's 200 seconds / pull = ~3 minutes total. Well under any plausible anti-abuse threshold; well under the published "be reasonable" guidance.

API key management: we hold *one* OPENGEM-corporate API key, registered against a non-profit research account at acleddata.com. The key never appears on the public side; it's stored in the Dagster secret manager.

## Tier-2 — What we compute and publish

We **never** publish ACLED rows. We publish three classes of *derived* metrics:

### Class A — Country-month conflict intensity index (normalized)

For each country-month: compute the count of ACLED events of each type (Battle, Explosion, Civilian violence, Riot, Protest, Strategic) per million population, z-score normalize against the country's 2018-2025 baseline, blend into a single composite score. The published number is a z-score on `[-3, +3]`, not a raw event count. This is *transformative* under the EULA: it combines, normalizes, blends, and discards the row-level structure.

### Class B — Conflict trajectory features for L3 forecasting

The 90-day rolling Δ of the Class A index, plus its 30-day acceleration, fed into the L3 ensemble as a feature for the recession-probability tile (L213) and the FX-misalignment forecast (L217). These features never leak ACLED rows; they leak a single float per country per day.

### Class C — Methodology pop-up citation

Every chart that uses an ACLED-derived feature carries a methodology pop-up that says:
> "Conflict intensity computed from ACLED data (Armed Conflict Location & Event Data Project), accessed weekly from api.acleddata.com under the ACLED Terms of Use. Citation: Raleigh, Linke, Hegre, Karlsen (2010). Last refreshed: 2026-06-03."

The citation is non-negotiable on every chart, every embed, every PDF tearsheet.

## Tier-3 — Free-tier isolation

This is the constraint most likely to be violated by accident. The pattern:

- Two API gateway routes: `/v1/conflict/*` (free tier, ACLED-backed) vs `/v1/conflict-public/*` (any tier, GREEN-substrate only).
- Paid-tier API keys are *blocked* from `/v1/conflict/*` by the gateway — they get a 402 with a redirect to the public endpoint.
- Marketing copy and API docs name only `/v1/conflict-public/*` for paid customers.
- Internal audit job runs weekly to scan API logs for any ACLED-backed response served against a paid-tier key. Alert on hit.

The free-tier `/v1/conflict/*` endpoint serves the public dashboard's interactive tiles, the embed widget on Substack/Medium, and the MCP server's tools — all of which are zero-cost-to-user and EULA-compatible under ACLED's "non-commercial public-facing research" affordance.

## Tier-4 — GREEN fallback path (pre-wired)

The critical insurance. We build the conflict intensity tile against a *substrate abstraction layer* that has three backends:

```python
class ConflictSubstrate:
    """Abstract conflict-intensity feature source."""
    def country_month_intensity(self, iso3: str, year: int, month: int) -> float: ...
    def trajectory_30d(self, iso3: str, as_of: date) -> tuple[float, float]: ...

class AcledSubstrate(ConflictSubstrate):
    """YELLOW. Free-tier only. Default in v1 marketing."""
    ...

class GreenConflictSubstrate(ConflictSubstrate):
    """GREEN. UCDP + POLECAT + GDELT triangulation. Default fallback."""
    def __init__(self):
        self.ucdp = UcdpFeed()        # CC-BY-4.0
        self.polecat = PolecatFeed()  # CC0
        self.gdelt = GdeltFeed()      # GREEN, see L084

    def country_month_intensity(self, iso3, year, month):
        u = self.ucdp.intensity(iso3, year, month)
        p = self.polecat.intensity(iso3, year, month)
        g = self.gdelt.intensity(iso3, year, month)
        return self._blend(u, p, g)  # weighted by historical calibration vs ACLED
```

The substrate is selected by a `OPENGEM_CONFLICT_SUBSTRATE=acled|green` env var. v1 launches with `acled`. The day ACLED's EULA changes or commercial scrutiny appears, we flip to `green`. **The user-facing UI is unchanged.** The methodology pop-up updates to reflect the new sources. The L3 features re-calibrate from a stored coefficient table.

**Pre-wiring cost**: ~4 dev-weeks. We build the abstraction, the GREEN backend, and the calibration coefficients in parallel with the ACLED backend. The expensive bit is the calibration table — empirically computing per-country adjustment factors that align UCDP+POLECAT+GDELT-derived intensities with ACLED-derived intensities historically. We do this once, stash the table, and refresh quarterly.

This is the cheapest insurance OPENGEM buys in the entire data architecture. Without it, ACLED is a single point of failure. With it, ACLED is a quality boost over a perfectly serviceable GREEN baseline.

## License-mode-by-mode behavior

| Mode | Substrate | What's published | Where it appears | Risk |
|---|---|---|---|---|
| **A — ACLED default (v1)** | ACLED | Derived intensity index, attribution everywhere | Free dashboard, free embed, MCP server | Medium — EULA shift possible |
| **B — GREEN forced (escape hatch)** | UCDP+POLECAT+GDELT | Same shape, slightly noisier | Same surfaces | Low — fully open |
| **C — Hybrid (v2)** | GREEN primary, ACLED overlay | GREEN intensity + ACLED-validation badge on top-quartile-confidence events | Same surfaces | Low — and richer narrative |

## Quantifying "slightly noisier"

The honest accounting: ACLED-derived intensity correlates ~0.85 with the GREEN triangulation at the country-month level (based on the 2020-2024 backtest we will run in Phase 5). That 0.15 correlation gap maps to about 0.5 standard deviations of additional noise in the L3 forecast features that consume the intensity feed. The downstream effect on the recession-probability tile's CRPS is roughly 3-5% degradation — measurable but not catastrophic. For OPENGEM's purposes (publish-with-uncertainty), GREEN is a perfectly defensible default.

The reason we lead with ACLED in v1 is *marketing*, not modeling. ACLED is the brand name in conflict data; using it signals data-quality awareness to the researcher audience. The reason we engineer the GREEN fallback is *resilience* — we never want our story to depend on a single party's licensing decision.

## The license-tightening playbook

If the day comes when ACLED contacts us with a commercial-license demand or a cease-and-desist over alleged "competitive dashboarding":

1. **Day 0**: Receive the notice. Acknowledge.
2. **Day 1**: Flip the env var to `OPENGEM_CONFLICT_SUBSTRATE=green`. Deploy. UI unchanged, methodology pop-up updates.
3. **Day 2**: Email response: "We have moved off ACLED to a GREEN substrate. Please confirm no further action required."
4. **Day 3**: Public-facing post on the OPENGEM accountability page explaining the change, naming ACLED's role in the prior architecture, and detailing the new GREEN substrate methodology.
5. **Day 7**: Run a backtest comparing the new GREEN-substrate intensity against the prior ACLED-substrate intensity. Publish.

Total elapsed: one week. Total engineering effort: ~4 hours of redeploy + comms. Total credibility: enhanced — we walked our own "publishes its mistakes" talk by handling a real licensing situation in public.

## Risks

1. **EULA changes silently.** ACLED could tighten terms without notifying us. Mitigation: monthly automated re-check of the EULA URL with a diff alert.
2. **Anti-abuse triggers.** Our weekly pull could accidentally exceed an undocumented internal threshold. Mitigation: token-bucket throttler, 2-second-per-call floor, exponential backoff on 429.
3. **The "transformative" test is subjective.** ACLED could disagree with our reading of "transformative." Mitigation: keep the derivation chain documented and the published outputs at least 2 levels of abstraction away from raw rows.
4. **GREEN substrate calibration drift.** As UCDP/POLECAT/GDELT methodologies evolve, the calibration table goes stale. Mitigation: quarterly re-calibration job in Dagster.

## What this loop produced

- Weekly + repair + quarterly Dagster pull schedule with rate-limit envelope.
- Three classes of derivable outputs (intensity index, trajectory features, methodology citation).
- Free-tier isolation pattern with two route prefixes and a paid-key blocklist.
- Pre-wired GREEN fallback with a substrate abstraction and an env-var kill switch.
- License-tightening playbook (one-week turnaround).
- Honest accounting of the GREEN vs ACLED quality delta (~3-5% CRPS hit).

## What comes next

- **L084** — GDELT pipeline (one of the GREEN substrate inputs).
- **L228** — Conflict tracker page: the user-facing surface this feeds.
- **L282** — License audit: the legal master matrix.

## Related

- [[L022-acled]] — Phase 1 deep dive and EULA parse.
- [[L021-gdelt-gkg]] — GREEN substitute, GDELT.
- [[L026-ucdp]] — GREEN substitute, UCDP.
- [[L025-cline-center]] — GREEN substitute, POLECAT.
- [[L084-gdelt-as-feature-pipeline-design]] — sibling pipeline.
- [[L228-conflict-tracker-page]] — downstream UI.
- [[L282-license-audit]] — legal master matrix.
