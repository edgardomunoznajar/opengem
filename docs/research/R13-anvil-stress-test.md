# R13 — Adversarial Stress-Test of the Rebaseline

| Field | Value |
|---|---|
| Document ID | OG1-RES-013 |
| Revision | A (2026-05-24) |
| Date | 2026-05-24 |
| Status | **Anvil-style red-team of R99 + rev C CONOPS. Read after R99.** |
| Audience | Program Owner |

---

## 1. Why this exists

R99 is a synthesis written by the same agent who wrote R01–R06. Confirmation bias risk is high. R13 deliberately attacks the proposal from hostile angles to surface failure modes the synthesis may have glossed.

Rule: **every attack here is treated as serious until specifically dispatched.**

## 2. Attack #1 — "The architecture rescope is over-fitting to literature, not to product"

**Charge**: R03 reads forecasting-literature meta-results and concludes L3 dominates. But OPENGEM's actual product job isn't "win the M-competition." It's "be a structured, interpretable, accountable economic forecast system that the owner can defend." L1's narrative value is *the product*, not an optional extra. Stripping L1 from the critical path strips the thing that makes OPENGEM defensible.

**Defense**: The rev C rescope **keeps L1** — it just relocates it out of the forecast critical path and into the Scenario Subsystem. The narrative job is preserved; the engineering cost of 25-country L1 cores at IOC is removed. If the program owner wants L1 in the forecast path, the trade is: add ~25× the per-country structural-model maintenance burden for marginal forecast-accuracy improvement that the literature doesn't actually show. That trade fails for a single-maintainer project.

**Residual risk**: if v0.4 demonstrates that the narrative value of L1 is what makes the system *valuable* (not the accuracy of L3), the rescope is wrong. Mitigation: at v0.4 review, explicitly assess "does L1 US narrative produce usable scenario stories?" — if yes, accelerate L1 for UK/EA at v1.0; if no, defer indefinitely.

**Verdict**: defense holds with explicit v0.4 checkpoint.

## 3. Attack #2 — "Tier-V is honest but unimpressive"

**Charge**: ~26 countries (or 35 if BRICS+ ORDRA coverage validates) is a modest scope. NiGEM has 60+. OPENGEM at IOC is publishing forecasts for less than half of NiGEM's coverage. The "global" branding becomes empty. Pivot — call it OPENGEM-OECD or similar.

**Defense**: Tier-V is what's *vintage-correct and leaderboard-eligible*. Tier-T tracks the remaining ~50 economies; they appear in dashboards just not on the public leaderboard. From an end-user perspective, the dashboard shows ~80 economies; from an accountability perspective, the rigorous leaderboard claim is on 26 of them. This is honest framing, not narrow framing. NiGEM publishes 60+ countries with no public scoring — claiming all 60 is *less* defensible than claiming 26 with full scoring.

**Residual risk**: the rebranding question is real. "OPENGEM" still sounds global. Mitigation: defer the naming question; if Block II/III matures and width grows, the name fits better; if not, rename.

**Verdict**: defense holds.

## 4. Attack #3 — "The V&V matrix is a moving goalpost"

**Charge**: Replacing a single bar with 17 cells lets OPENGEM declare partial success on any combination of cells that happen to clear. Game-able. The original single bar was at least falsifiable.

**Defense**: The matrix is more falsifiable, not less. Each cell has its own pass/fail bar; FOC requires ALL non-deferred cells pass; IOC has a smaller subset. Reporting cell-by-cell makes failure interpretable rather than dismissible. The single bar would have been gameable by inflating GDP confidence intervals to "beat AR(1)" trivially without being useful.

**Residual risk**: governance — who decides which cells are "non-deferred" at FOC? Mitigation: list the FOC cells explicitly in master-doc v2.0 §8.3 (done); changes require an ECP per CMP rules.

**Verdict**: defense holds.

## 5. Attack #4 — "The FRED substitution is a one-time win that becomes ongoing maintenance pain"

**Charge**: Five upstream-agency adapters (BEA / BLS / FRB / Treasury / Census) each have their own quirks, release calendars, schema changes, and API rotations. FRED-as-aggregator absorbed all that pain. OPENGEM trades a single dependency for five, and the maintenance burden is permanent.

**Defense**: FRED's 2024 ToS is binary — it's incompatible with OPENGEM's archive+train design. Mitigation is not optional. The five-agency cohort is the *minimum*; downside is real. Mitigation: schema-validation gates per agency; per-agency outage handling; golden-fixture tests that catch schema drift on every CI run.

**Residual risk**: a future agency adapter could fail silently in a way that pollutes the vintage archive. Mitigation: cross-source-of-truth validation — FRED can still be *queried* (not cached) for verification of recent series values; if BEA's adapter disagrees with FRED's mirror of BEA by >epsilon, alert.

**Verdict**: real ongoing cost. Accepted. The alternative (FRED-only) is ToS-violating and therefore non-existent.

## 6. Attack #5 — "Annual L2 cadence is too slow for crisis scenarios"

**Charge**: Spillover IRFs from L2 are presented as "annual re-estimation; on-demand for scenarios." But during an actual crisis (e.g., COVID-2020, energy 2022), trade-weight structures change rapidly. An L2 posterior estimated in January 2020 is unfit for purpose in October 2020.

**Defense**: True — and that's a real limitation. Mitigations:
1. **Manual trigger override**: Scenario Subsystem allows requesting L2 re-estimation on demand if posterior age exceeds N months OR if a crisis flag is raised in Situation Subsystem (term-spread inverted, GPR spike, etc.).
2. **Stale-posterior warnings**: every scenario response includes `L2_posterior_age_months`; users see it.
3. **Annual re-estimation date is configurable** per major release; doesn't have to be calendar-anchored.

But ultimately: an L2 estimated mid-crisis on crisis data has its own validity issues (parameter shifts during a regime change are notoriously hard). Annual is a reasonable default; on-demand-override is the safety valve.

**Residual risk**: discovering during the first real crisis that on-demand re-estimation doesn't actually work because the operator (single maintainer) is busy. Mitigation: pre-build the on-demand workflow at v0.4 so it's a button-press not a workflow-design exercise.

**Verdict**: defense holds with explicit pre-built crisis workflow.

## 7. Attack #6 — "Situation Subsystem adds product surface without adding product"

**Charge**: Recession-probability is a *wrapper* over Bauer-Mertens. GPR nowcast is a *wrapper* over Caldara-Iacoviello. Neither is novel. Both increase the API surface and the model-card maintenance burden. The "differentiation" is illusory.

**Defense**: Both endpoints integrate well-validated published methods *with OPENGEM's vintage + provenance + MCP discipline*. The novelty isn't in the model — it's in the operational delivery (daily refresh, programmatic access, MCP-integrated, scored against published replications). Recession-probability *as a service* doesn't exist anywhere in 2026 with these properties.

The deferred-build of GPR nowcast specifically gates on skill probe — if it doesn't beat persistence, it doesn't get built. So the "wrapper without value" risk is bounded.

**Residual risk**: term-spread recession probability for Tier-V countries other than US is on shakier ground (literature evidence is US-strong, ROW-weaker). Mitigation: per-country model card lists AUC; if a country's AUC < 0.7, the endpoint marks it `low_confidence: true` rather than removing it (transparency over precision).

**Verdict**: defense holds with per-country confidence flags.

## 8. Attack #7 — "Single maintainer cannot deliver this in any reasonable horizon"

**Charge**: Block I is large. Five-agency adapter cohort + L3 + L2 wrapper + L1 US core + Situation Subsystem + Scenario Subsystem + Backtest with V&V matrix + leaderboard + MCP server + dashboard. Plus operational concerns (deployments, monitoring, alerts). One person cannot do all of this in 12–18 months without quality collapsing.

**Defense**: This is the genuine risk. R99 §5 already lists single-maintainer as residual high-severity risk. Mitigations:
1. **Scope-staging**: IOC delivers only US Tier-V Core (one country, one architecture). v0.4 adds Tier-V Core breadth. v1.0 adds Situation Subsystem and Tier-V Extended.
2. **Reuse over rebuild**: PyFRB/US for L1 (rather than reimplementing), `BGVAR` for L2, established Python forecasting libraries for L3, NY Fed code for recession-probability.
3. **Doc-as-code**: every design decision recorded; recovery from interruption easier.
4. **Bus factor escalation at v0.4**: if v0.4 is reached and the project shows traction, recruit a co-maintainer or transfer to a foundation/university. Don't try to be both maintainer and operator past v0.4.

**Residual risk**: significant. Even staged, this is a 12+-month commitment with no monetary reward (private project). Sustainability depends on the program owner finding the work intrinsically motivating.

**Verdict**: defense partial. Accept this is the dominant risk. Plan accordingly.

## 9. Attack #8 — "The vision document is aspirational hand-waving"

**Charge**: R100's "sovereign-grade open forecast infrastructure" framing is the kind of mission-creep grandeur that kills startups. Stay focused on Block I; don't pre-commit to year-3+ architecture that may never need to exist.

**Defense**: R100 is explicitly labeled aspirational; the rev C CONOPS, master-doc, and LOOP_PLAN are *not* committed to any year-2+ work. R100 exists to validate that Block I's discipline doesn't foreclose later options, not to commit to those options. If year-2 reality contradicts the vision, the vision is rewritten or sunset; the foundation remains useful regardless.

**Residual risk**: scope creep into Block II via "but we said this in the vision." Mitigation: any Block II work requires its own pre-PDR research round with its own R99-style synthesis. Vision is not a planning document.

**Verdict**: defense holds with explicit governance.

## 10. Attack #9 — "Edgardo specifically has 5+ active projects; this is the 6th"

**Charge**: Per the program-owner profile, active projects include oblique-lawyer (in v0.4 → v0.5), slod, novel adaptation (chapters 7–9 of 20), vestara-super, kalshi. Adding OPENGEM as the 6th major project with a 12+ month horizon is divided-attention failure waiting to happen.

**Defense**: This is the realest of the realities. Mitigations:
1. **OPENGEM is currently pre-implementation**, so no active code commitment yet. The research round closed cleanly.
2. **First-90-days plan** (R18) front-loads the small, contained, technically-uncomplicated work (adapters, ingestion, infrastructure). These are episodic, can be picked up and put down without thrash.
3. **L3 forecast modeling work** is the harder, more thought-intensive piece — schedule it after adapter foundation is solid so it can absorb undistracted blocks.
4. **The Block I outcome is small** by the time it's done: ~5 endpoints, ~30 country panels, one architecture rescope. This is not a 6th major project — it's a focused sub-quarter of work with high reusability for the oblique suite.

**Residual risk**: program owner's attention is the real bottleneck. R100's year-2+ ambitions are explicitly aspirational; year-1 demands the minimum.

**Verdict**: real concern. Block I is *sized* for sustainability; whether the program owner can sustain six projects is outside this proposal's scope.

## 11. Attack #10 — "What about hidden costs we haven't budgeted?"

**Charge**: The cost analysis (~USD 65–120/mo) covers compute and storage. But it doesn't include: (a) developer time at any opportunity cost; (b) potential paid-data dependencies if free sources prove insufficient (Consensus Economics access ~thousands of USD; commercial AIS feed ~hundreds/mo); (c) eventual professional services (security audit, compliance review) if the public dashboard launches; (d) eventual legal review of redistribution terms when something gets shared externally.

**Defense**: (a) is real but opportunity-cost is not a cash-flow item. (b) is genuinely deferred — Consensus Economics is in R05's "future public-launch round" bucket. AIS uses PortWatch (free) not commercial. (c) and (d) are also deferred to public-launch round. Block I's USD 65–120/mo estimate is for the operational system at the personal-use scope. Future audit/legal costs are independent of that envelope and are public-launch decisions.

**Residual risk**: scope creep adds paid dependencies invisibly. Mitigation: ADR-014 already commits the wider information surface to free sources only; any paid-data addition requires explicit ECP per CMP rules.

**Verdict**: defense holds with explicit ADR-style cost-discipline gate.

## 12. Verdicts in summary

| Attack | Verdict | Action |
|---|---|---|
| #1 Architecture rescope over-fits to literature | Hold w/ v0.4 narrative checkpoint | Explicit gate at v0.4 |
| #2 Tier-V unimpressive | Hold; honest framing | Defer naming question |
| #3 V&V matrix gameable | Hold; matrix is *more* falsifiable | Lock cells in master-doc |
| #4 Adapter cohort permanent maintenance | Real cost; accepted | Cross-source-of-truth validation |
| #5 Annual L2 too slow for crisis | Hold w/ pre-built on-demand workflow | Pre-build at v0.4 |
| #6 Situation Subsystem illusory novelty | Hold w/ per-country confidence flags | Confidence flags in API |
| #7 Single maintainer cannot deliver | Partial defense; dominant risk | Scope-staging + bus-factor escalation at v0.4 |
| #8 Vision is hand-waving | Hold w/ explicit governance | Block II requires own research round |
| #9 6th major project attention divide | Real; out of scope to fix | Block I sized for sustainability |
| #10 Hidden costs | Hold w/ cost-discipline ADR | ADR-014 already commits |

**Net assessment**: the proposal survives adversarial review with **two genuinely-difficult residual risks** — single-maintainer attention and adapter-cohort maintenance burden. Neither invalidates the recommendation; both should be explicitly named in the R99 acceptance.

## 13. What attacks would change R99's recommendation?

These attacks, if validated, would flip R99's recommendation from A → B or C:

- **Vintage data turns out to be more available** than R02 found (e.g., a paid provider becomes free, or a major EM stat agency publishes vintage archive): then Tier-V is bigger; Block I scope can grow; A still wins but the case strengthens.
- **L3-only proves underwhelming** in a probe (e.g., 6-week MVP of DFM+ML shows it can't even pass C-01 in the V&V matrix): then the L3-as-workhorse premise is wrong; rev C is invalid; revisit fundamentals.
- **FRED 2024 ToS gets clarified** to permit research-archive use: then ADR-010 is moot; substitution work is wasted (but adapter cohort is still defensible).
- **Program owner determines time budget is <10h/month**: then Block I is too large; pivot to B or C.

**Stress-test gates for the next round**: (a) a 6-week L3-MVP-on-US probe to validate the L3-as-workhorse premise before full SAD investment; (b) an explicit weekly time-budget commitment in the SRR-2 walkthrough.

---

*End of R13 Rev A.*
