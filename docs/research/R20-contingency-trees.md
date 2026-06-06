# R20 — Failure-Mode Contingency Trees

| Field | Value |
|---|---|
| Document ID | OG1-RES-020 |
| Revision | A (2026-05-24) |
| Date | 2026-05-24 |
| Status | **Pre-mortem-style contingency planning. Each failure has a Plan B before the failure happens.** |

---

## 1. Why this exists

Anvil-style projects (R13) ask "what could go wrong?" Plan-style projects ask "and what do we do when it does?" R20 is the latter — for each plausible failure, a contingency branch is pre-named.

## 2. Tree 1 — L3 MVP fails the Phase 3 gate (R18 §6.4)

```
L3 MVP (US, GDP, 1Q+4Q) tested 2014–2026 vintage replay
│
├── PASS all 3 V&V cells (C-01, C-02, C-03)
│   → Proceed to Phase 4 (API skeleton)
│
├── PASS 2 of 3 cells
│   ├── If failing cell is C-02 (PIT calibration)
│   │   → Add V4 (TVP-VAR with stochastic volatility) to combiner
│   │   → Re-run; if still fails, accept and note in model card
│   ├── If failing cell is C-03 (vs. WEO)
│   │   → Acceptable at IOC; WEO is a hard benchmark
│   │   → Document; proceed
│   └── If failing cell is C-01 (vs. AR(1))
│       → SERIOUS. AR(1) shouldn't beat L3 on US GDP 1Q.
│       → Investigate: data leakage? feature normalization bug? model overfit?
│       → 2 weeks of debugging; re-test
│
├── PASS 1 of 3 cells
│   → Halt Phase 4. Architecture probably wrong.
│   → Branch A: try equal-weight combination instead of BMA
│   → Branch B: try just V3 (large BVAR Minnesota) without DFM/ML residual
│   → Branch C: add V4 (TVP-VAR)
│   → If none works in 4 weeks: see Tree 2
│
└── PASS 0 of 3 cells
    → L3-as-workhorse premise is wrong. See Tree 2.
```

## 3. Tree 2 — L3-as-workhorse premise invalidated

```
After 4+ weeks of L3 iteration, still failing ≥2 V&V cells on US
│
├── Branch A: re-introduce L2 into baseline forecast critical path
│   → Reverse R03's rescope. BMA over L1(US) + L2 + L3.
│   → Cost: more compute, more complexity, but possibly more accurate
│   → Re-run Phase 3 with full 3-layer; commit if it works
│
├── Branch B: pivot to "scenario-only" framing
│   → Drop the forecast-accuracy claim entirely
│   → OPENGEM becomes a scenario-impulse-response engine
│   → Tier-V leaderboard becomes term-spread recession-prob only
│   → Smaller product, possibly more defensible
│
├── Branch C: pivot to "open data + interface" framing
│   → Drop forecasting entirely; just expose vintage-correct data + Situation endpoints
│   → Smallest product; lowest moat; lowest maintenance
│   → Acceptable if program owner is exhausted
│
└── Branch D: Sunset (R99 Option C)
    → Honest acknowledgment that the gap to a meaningful product is too large
    → Final V&V report; archive; move on
```

## 4. Tree 3 — Adapter cohort breakage

```
One or more US upstream-agency adapters fails (schema change, deprecated endpoint, etc.)
│
├── If single agency, soft failure (degraded coverage):
│   → Adapter retries with exponential backoff for 24h
│   → Beyond 24h: alert; affected series flagged in dashboard with completeness < 0.9
│   → V&V cells using affected series annotated `data_quality: degraded`
│
├── If single agency, hard failure (endpoint moved or removed):
│   → Re-write adapter against new endpoint (typically 1–2 days)
│   → If new endpoint requires payment / not available: pull from FRED for *queries only*,
│     persist via another agency if same series exists upstream (e.g., BLS CPI also from FRED-mirror confirms BLS value)
│   → If truly unavailable: drop that series from L3 feature set; document gap
│
├── If 3+ agencies fail simultaneously (catastrophic):
│   → Highly unlikely; suggests systemic event (gov shutdown, large-scale API redesign)
│   → Freeze data layer at last-good; serve cached forecasts with stale-data warning
│   → Wait for resolution; reassess scope
│
└── If FRED 2024 ToS is *relaxed* (e.g., research-archive exemption granted)
    → Re-enable ALFRED for vintage queries (not bulk archive)
    → Keep upstream-agency adapters as primary; FRED as enrichment
    → Document policy reversal in ADR-010 update
```

## 5. Tree 4 — V&V matrix fails at FOC

```
At FOC test (W53–W56 of master schedule), ≥5 V&V matrix cells fail
│
├── If failures cluster on inflation cells (C-08, C-10, C-11, C-12)
│   → Expected per R01 — inflation density is hard
│   → Pivot to "GDP+unemployment specialization, inflation tracking only"
│   → Inflation leaderboard becomes a watch-only panel
│
├── If failures cluster on long-horizon (8Q, 20Q)
│   → Drop 8Q/20Q from primary V&V; report as informational only
│   → Long-horizon is hard for everyone; consensus too
│
├── If failures cluster on density (PIT) cells but point-forecast cells pass
│   → L3 variants are mis-calibrated; investigate combiner
│   → Try DeCo or Geweke-Amisano combination instead of BMA
│   → Add conformal-prediction wrappers
│
├── If failures cluster on Tier-V Extended (CZ/HU/PL/etc.)
│   → Reduce FOC roster to Tier-V Core
│   → Document why; transparent re-baseline
│
└── If failures are general (≥10 cells across categories)
    → FOC sunset; declare "the goal of operational parity is not met"
    → Re-baseline as "verifiable forecast infrastructure," drop parity claim
    → R100 Year-1 retrospective writes this up honestly
```

## 6. Tree 5 — Maintainer attention drops

```
Program owner has 0 OPENGEM commits for 60 consecutive days
│
├── Day 60: low-maintenance banner on README
│
├── Day 90: pause public dashboard updates
│   → Archived forecasts remain queryable
│   → New forecasts stop being published
│   → Banner: "OPENGEM is in low-maintenance mode"
│
├── Day 180: explicit decision required
│   → Resume? Pre-condition: re-commit to ≥6 hr/month
│   → Mothball? See Tree 6
│   → Hand off? See Tree 7
│
└── Day 365: automatic mothball (Tree 6) if no decision
```

## 7. Tree 6 — Clean mothball

```
Decision made to mothball OPENGEM
│
├── Update README with banner: "OPENGEM archived. Forecasts continue
│    to be served read-only until {date} via frozen pipeline. Code remains
│    public under Apache-2.0."
├── Final V&V matrix evaluation; published as `RETROSPECTIVE.md`
├── Final model cards published
├── Last public dashboard snapshot archived
├── Domain (if registered) redirects to GitHub
├── Final commit: tag `archive-vYYYY-MM-DD`; release notes summarize lessons
└── No shame; the discipline of clean sunset preserves credibility for any successor.
```

## 8. Tree 7 — Hand off

```
External party (academic, OSS contributor, foundation, etc.) wants to take over
│
├── Verify intent: read `docs/governance/handoff.md`; commitments mutual
├── Transfer in stages:
│   ├── Phase 1: external contributor PRs accepted; mentorship from original maintainer
│   ├── Phase 2: external contributor becomes committer; co-maintainership
│   └── Phase 3: original maintainer steps back; advisory only
├── Public announcement of governance change in README + dashboard
├── Re-baseline the V&V claim if architecture changes meaningfully
```

## 9. Tree 8 — Funding becomes available (positive contingency)

```
Program owner gets unexpected revenue / grant / sponsorship interest
│
├── If <$5k: spend on a paid Consensus Economics archive (resolves TBR-008)
│             OR commercial AIS feed if PortWatch insufficient
│             OR a paid 2nd VM for L2 GPU bursts
│
├── If $5k–$50k: hire a contractor for ~3 months
│             → Build out the deferred adapters (e.g., AU national-specific, EU member-state-specific)
│             → Implement custom topic model on news (Bybee-Kelly-Manela-Xiu)
│             → Build out the dashboard polish
│
├── If $50k+: consider non-profit incorporation
│             → 1 FTE co-maintainer
│             → Marketing / community / outreach for Block II
│
└── In all cases: avoid scope creep into "pretend to be NiGEM" — stay focused on
                  the differentiated value (open + vintage + leaderboard + MCP)
```

## 10. Tree 9 — Forecast embarrassment

```
A widely-watched forecast turns out to be very wrong (e.g., OPENGEM misses
a recession by 12 months; or OPENGEM gives a confident 0.05 recession prob
right before a recession hits)
│
├── Detection: post-event V&V evaluation flags the cell
│
├── Within 5 business days: post-mortem published on dashboard
│   → What variables would have helped?
│   → Which variant of L3 was leading? Did the combiner mis-weight?
│   → What feature was missing or stale?
│
├── Model card updated to reflect the failure
│   → Don't retract the run; record it with `superseded_by` pointer if a correction
│     is issued, otherwise leave standing
│
├── If repeated failures (>1 in 12 months): regime-shift detector triggered
│   → Investigate structural break; may trigger early L2 re-estimation
│   → Add a "regime uncertainty" flag to all current forecasts
│
└── Public reputation: "the system that publishes its mistakes is harder to
                       discredit than the system that hides them" (R100 §1)
```

## 11. Tree 10 — Tier-V country falls out (data outage)

```
A Tier-V country's vintage source stops updating (e.g., ORDRA drops a country)
│
├── If ≤30 days: hold position; warn in dashboard with `data_status: stale`
│
├── If 31–180 days: demote to Tier-V "watch-only" — no new forecast records;
│                    historical forecasts remain queryable
│
├── If >180 days: demote to Tier-T tracked-only
│                  → Remove from leaderboard
│                  → Public note in dashboard explaining
│
└── If the country source resumes: re-add via the same process in reverse,
                                    after 1 quarter of clean vintage data
```

## 12. Bottom line

Every plausible failure has a pre-named branch. The discipline of writing them down means **when one of them fires, the response is mechanical rather than emotional**. The single-maintainer project is more resilient with these trees than with hero responses.

---

*End of R20 Rev A.*
