# R15 — Personal Use Cases for OPENGEM

| Field | Value |
|---|---|
| Document ID | OG1-RES-015 |
| Revision | A (2026-05-24) |
| Date | 2026-05-24 |
| Status | **Concrete personal-use scenarios — anchors the "why am I building this" question for the program owner.** |

---

## 1. Why this exists

Private project. Single owner. The question "what will I actually *use* this for?" is more load-bearing than any technical-architecture choice. This memo enumerates concrete, situation-specific use cases drawn from the program owner's active project list and stated interests.

## 2. The owner's situation, as inputs

From the Honcho-memory profile and prior context:

- **Active projects**: oblique-lawyer (legal knowledge graph, Australian law), slod, novel adaptation (The Practitioner), vestara-super, kalshi. Plus OPENGEM as #6.
- **Oblique suite**: anvil, weaver, oracle, thinker, seer, plan — economic forecasting is a missing primitive.
- **Geographic interest**: Australia (oblique-lawyer focus); broader for novel work.
- **Skills/inclination**: systematic/procedural; data-driven; iterative loop-based workflows; Java/Spring + Python/FastAPI stack.
- **Revenue interest**: generates revenue from projects; biggest-wins-first; but explicit "no marketing thoughts yet" on OPENGEM (private scope).

## 3. Use Case A — Sanity-check macro intuitions

**Situation**: program owner reads an article saying "the next recession is coming." Wants to test the claim against a model rather than rely on the article's narrative.

**Workflow**:
1. Open dashboard or MCP query.
2. `recession_probability(country="US")` → 0.18 with reliability diagram.
3. `forecast(country="US", variable="gdp_real", horizon="4Q")` → density.
4. Compare to article's claim → form independent opinion.

**Value**: trust-but-verify against media narrative. **Time saved per use**: ~15 minutes of independent reasoning, ~weekly frequency. Cumulative over a year: 13 hours of clearer-headed reading.

**Cell from V&V matrix that backs this**: C-17 (recession AUC ≥ 0.85), C-03 (GDP-4Q not worse than WEO).

## 4. Use Case B — Inform Australian-context legal-graph work

**Situation**: oblique-lawyer indexes Australian legislation. Macro context (RBA policy, AU CPI, AU unemployment) is one of the natural overlays for risk-surface scoring — legislation about, e.g., responsible-lending obligations is more salient when the credit cycle is at a particular stage.

**Workflow**:
1. oblique-lawyer's risk-surface scoring calls OPENGEM MCP for current AU macro state.
2. `forecast(country="AU", variable=["gdp_real", "cpi_headline", "policy_rate"], horizon=["1Q","4Q"])` returns the current density.
3. oblique-lawyer's domain-classifier uses macro state as a feature in its risk score.

**Value**: cross-project synergy. Makes oblique-lawyer's risk surface *time-aware* rather than static. **Reuse pattern**: standard MCP integration; ~1 day of integration work in oblique-lawyer once OPENGEM Block I exposes AU as Tier-V.

## 5. Use Case C — Scenario testing for vestara-super

**Situation**: vestara-super is a superannuation-related project. Long-horizon outcomes for super accounts depend on macro paths (equity returns, inflation, wage growth). Scenario testing is a natural primitive.

**Workflow**:
1. `scenario(shock={"type":"path_shock", "variable":"cpi_headline", "country":"AU", "magnitude":"+2pp_over_4Q"})` → counterfactual densities.
2. vestara-super pipes the counterfactual into its long-horizon balance simulation.
3. User of vestara-super sees how their projected super balance changes under high-inflation scenarios.

**Value**: scenario-driven retirement-balance projections become *credible* rather than hand-wavy. Direct revenue connection for vestara-super if/when it monetizes.

## 6. Use Case D — Kalshi prediction-market positioning

**Situation**: Kalshi (project on the active list) is a regulated prediction-market platform. Has markets on macro outcomes (e.g., "will inflation be above 3% by Q4 2026?"). OPENGEM's density forecasts are a natural prior for positioning.

**Workflow**:
1. Identify a Kalshi market on a Tier-V macro outcome.
2. Query OPENGEM density at the relevant horizon.
3. Compare implied probability from Kalshi market to OPENGEM's density-implied probability for the same event.
4. If meaningful divergence and OPENGEM's track record on the cell is strong (per V&V matrix), take a position.

**Value**: edge-finding. **Caveat**: implies high confidence in OPENGEM's calibration, which only matures over time. **Risk**: market-based feedback loops — if any other actor uses similar methodology, edge erodes. Track OPENGEM's own positioning track record as a meta-V&V signal.

## 7. Use Case E — Novel adaptation (The Practitioner) — economic-context realism

**Situation**: the novel is set partly in a dating-app investigation context. Modern fiction sometimes uses macro backdrop for verisimilitude (recession setting, inflation impact on character lifestyle, etc.). OPENGEM gives the author a quantitative reference for the macro state of any given quarter in the timeline.

**Workflow**:
1. Looking up "what was US GDP doing in Q3 2024" → query OPENGEM's vintage archive.
2. Used as a fact-check for time-keyed details in the manuscript.

**Value**: small per-use; cumulative consistency for a novel that touches reality.

## 8. Use Case F — Oblique suite economic primitive

**Situation**: the oblique suite (anvil, oracle, weaver, plan, thinker, seer) currently lacks an economic primitive. Oracle does Monte Carlo simulation on arbitrary inputs but those inputs have to come from somewhere. OPENGEM provides priors.

**Workflow**:
1. Owner asks oblique-oracle to simulate a 10-year outcome (business plan, retirement plan, market entry scenario).
2. Oracle's macro-prior inputs come from OPENGEM's long-horizon density forecasts (20Q for GDP, CPI).
3. Oracle's distribution outputs reflect macro uncertainty correctly.

**Value**: oblique suite becomes more rigorous. **Cross-link**: OPENGEM's MCP server exposes `forecast(country, variable, horizon, density="full")` and `scenario(...)`; oracle consumes via its own MCP client.

## 9. Use Case G — Independent benchmark of news / consensus / Twitter

**Situation**: the program owner reads economic Twitter and financial news. There's always someone saying "this is the inflection point." Most are wrong.

**Workflow**:
1. Daily-ish — see a claim about macro turning point.
2. Pull OPENGEM's term-spread recession probability + 4Q GDP density.
3. Use as a baseline against which the claim is calibrated.

**Value**: epistemic-discipline tooling for personal reading. Same value as a daily newspaper, but ones you built and can audit.

## 10. Use Case H — Long-horizon retrospective

**Situation**: 5 years from now (year-5 in R100's vision arc), the program owner can look back at OPENGEM's archived forecasts and see how often the system was right vs. wrong on what cells.

**Workflow**:
- Annual ritual: read the public-facing year-in-review post.
- Update the model card based on what was wrong; document what was learned.

**Value**: epistemic humility + public accountability. Probably the most valuable single output of the project over a long horizon.

## 11. Use Case priorities

Ranking by frequency of use × value per use:

| Use Case | Frequency | Value per use | Priority for IOC |
|---|---|---|---|
| A — Sanity-check macro intuitions | Weekly | Medium | **High** — daily-usable |
| F — Oblique suite economic primitive | Monthly | High | **High** — strategic cross-suite |
| C — vestara-super scenario testing | Per-project-iteration | High | Medium-High — depends on vestara-super needing this at IOC |
| G — Independent benchmark of news | Daily | Low-Medium | Medium |
| B — oblique-lawyer macro context | Per-iteration | Medium | Medium — needs AU Tier-V (post-IOC) |
| H — Long-horizon retrospective | Annual | High | Low priority but designed in |
| D — Kalshi positioning | Per-market | Variable | Low — needs mature V&V track record first |
| E — Novel context | Rare | Low | Low — bonus |

## 12. What this means for Block I scope

The use cases that matter most at IOC:

- **US Tier-V Core**: covers Use Cases A, G, and most of F (oblique suite consumption).
- **MCP server**: enables F (oblique suite), B (future), C (future).
- **AU Tier-V Core (post-IOC, v0.4)**: enables B (oblique-lawyer integration).

Therefore IOC should focus on **US Tier-V Core + MCP server**. Other Tier-V countries (AU, UK, DE, etc.) follow at v0.4. The first-90-days plan (R18) reflects this.

## 13. The honest pivot question

If after Phase 3 MVP, US Tier-V Core works but Use Cases A and F don't pull the system into daily use, **the project's premise is wrong**. The whole point is that the owner *will use* the system. R200 (Day-90 retrospective) explicitly asks: "in the last 30 days, did I open OPENGEM at all? Did I send any MCP queries to it from oblique-anvil/oracle?" If no — pivot the use-case set or sunset.

## 14. Bottom line

OPENGEM has at least 4–5 realistic personal use cases at IOC + v0.4 scope, ranging from daily epistemic-discipline tooling to monthly strategic cross-project queries. The system is not a hobby in search of users — it has a user (the program owner) with multiple concrete jobs-to-be-done. Block I is sized to deliver those jobs.

---

*End of R15 Rev A.*
