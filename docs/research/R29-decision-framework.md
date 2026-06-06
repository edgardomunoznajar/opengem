# R29 — Decision Framework: What Would Change the Recommendation?

| Field | Value |
|---|---|
| Document ID | OG1-RES-029 |
| Revision | A (2026-05-24) |
| Date | 2026-05-24 |
| Status | **Decision-aid memo for the program owner. Read alongside R99.** |

---

## 1. Why this exists

R99 recommends Option A (accept rebaseline). R13 stress-tests it adversarially. R29 explicitly asks: **what new information would flip the recommendation?** This gives the program owner a clean mental model for "should I sign off, or wait for more information."

## 2. Information that strengthens A

If any of these become true, A becomes more obviously right:

| Trigger | Why it matters |
|---|---|
| ORDRA verification confirms 35+ countries with full quartet | Tier-V is wider than the R02 conservative estimate; OPENGEM is more impressive at IOC. |
| PyFRB/US package suitable for direct embedding as L1 US core | Removes ~2 months of L1 work; lower IOC effort. |
| GPR-nowcast skill probe passes | Block I gets an unambiguously novel endpoint (not just a wrapper). |
| Initial 6-week L3-on-US MVP passes the V&V gate cleanly | The premise of the rescope (L3-as-workhorse) is empirically validated; rest of Block I is execution. |
| oblique-lawyer v0.5 monetization revenue arrives | Funds the optional Consensus Economics archive; opens public-launch decision earlier. |
| Co-maintainer expresses interest | Bus factor of 1 → 2; the year-2 reckoning is lower-stakes. |

## 3. Information that weakens A

If any of these become true, A is *still* probably right but with caveats:

| Trigger | What changes |
|---|---|
| OECD ORDRA coverage matrix is sparser than R07 estimates | Tier-V Core shrinks to ~15–18 countries. Public framing softens; still A but less impressive. |
| Philly RTDSM ToS turns out to restrict caching | A still right but US vintage path requires self-archive from upstream BEA / BLS (already done in R09); minor execution cost. |
| BGVAR R package has un-noted scaling issue at N>25 | VB fallback per R04 covers it; still A. |
| First 90 days takes 12+ weeks instead of 13 | Scope-staging adjusts; still A. |

## 4. Information that flips A → B (renarrow)

These would force a hard re-scope downward:

| Trigger | New scope |
|---|---|
| 6-week L3 MVP fails C-01 or C-02 cells on US | Drop forecast-accuracy ambition; pivot to scenario + situation-only system. |
| Single-maintainer time budget proves <4 hr/week | Block I L3 scope is too large; pivot to "Tier-V data foundation + Situation Subsystem only, no forecasting." |
| 2+ adapter cohort schema changes require >1 day each within first 90 days | Maintenance velocity not sustainable; reduce to BEA + BLS only and accept narrower variable coverage. |

## 5. Information that flips A → C (sunset)

These would justify sunsetting the program before significant code is written:

| Trigger | Why sunset |
|---|---|
| L3 MVP fails 0/3 V&V cells after 4+ weeks of iteration | The premise that L3 can carry forecast accuracy is wrong; nothing else in the architecture makes sense. |
| Owner determines OPENGEM use cases (R15) don't pull them into using the system in v0.4 pilot | The system doesn't have a user — even the program owner doesn't use it. No reason to build more. |
| Two of: bus factor of 1; >6 active projects; sustained 0 hr/week attention | Project is structurally unsustainable. Sunset cleanly. |
| FRED ToS reads worse than R05 §3 captured (e.g., even *query* use is restricted) | Re-doing the upstream-substitution work is acceptable; but if other agency ToS proves similarly restrictive, sunset is honest. |

## 6. Information that means "wait, don't decide yet"

These suggest deferring sign-off rather than choosing A/B/C:

| Trigger | What to do |
|---|---|
| Several P0 open issues (R27 §2.1) un-investigated | Investigate them; revisit after. |
| Owner is in the middle of a heavy oblique-lawyer or novel-adaptation sprint | Defer for 2–4 weeks; decision quality improves with attention. |
| External signal that the macro forecasting space is fundamentally changing (new entrant, regulatory shift) | Defer; reassess the value proposition. |

## 7. Decision quality discipline

A pre-mortem question to ask before signing off:

> "If, 12 months from now, OPENGEM Block I is unfinished and I've abandoned it, what was the most likely reason?"

Common answers and their preventative actions:

| Likely failure cause | Prevention |
|---|---|
| L3 architecture didn't work | The 6-week MVP probe (R18 Phase 3) catches this before scope investment |
| Time budget was wrong | Honest weekly time-budget commitment at SRR-2; revisit at Phase 3 |
| Lost interest | R15 use cases concretely named; owner uses the system before publishing |
| Adapter cohort decay | Mechanized correctness (R16, R17) catches drift before it propagates |
| One of the 5 other projects became all-consuming | Block I designed for pickup-and-put-down work; phases are checkpoints |

If you can't credibly answer "no" to any of these, defer.

## 8. The default

In the absence of a triggering event, the default is **A** — sign off, restart LOOP_PLAN v2, begin Phase 0 of the first-90-days plan.

The recommendation is **explicit but not coerced**. R99 + R13 + R29 collectively give the program owner enough material to disagree with the recommendation if their judgment differs.

## 9. The sign-off ritual (if Option A)

When you decide:

1. Commit a `SIGNOFF.md` to the repo with the decision date and a one-sentence rationale.
2. Tag the repo `pre-pdr-r99-accepted-YYYY-MM-DD`.
3. Move rev C CONOPS draft to `OG1-CONOPS-001.md` (replacing rev B).
4. Move master-doc v2.0 draft to `00-master-design-document.md` (replacing v1.0).
5. Move LOOP_PLAN v2 to `LOOP_PLAN.md` (replacing v1).
6. Update README banner from "awaiting sign-off" to "Pre-PDR; LOOP_PLAN active."

That's the SRR-2 walkthrough complete. Implementation can begin.

## 10. Bottom line

R29 makes the decision explicit: A is the default; specific triggers move you to B, C, or "wait." The program owner should make this decision **based on their own honest answer to the use-case and time-budget questions**, not on the rhetorical force of the synthesis memos. The discipline of naming what would change your mind is itself a hedge against overcommitment.

---

*End of R29 Rev A.*
