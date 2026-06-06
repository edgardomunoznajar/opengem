# OPENGEM-1 — Pre-PDR Research Round

**Status: COMPLETE. Awaiting program-owner sign-off on R99 recommendation.**

**Read order**: `/MORNING-BRIEFING.md` → `R99-synthesis.md` → `R29-decision-framework.md` → `R100-vision.md` → deep-dives.

**Posture**: rev B CONOPS and master-doc commitments treated as falsifiable hypotheses.
**Scope**: private project; market/monetization/branding questions deferred.

## Final status board (28 memos)

### Core hypothesis-test memos (R00–R06)

| ID  | Title | Verdict |
|-----|-------|---------|
| R00 | [Charter](R00-charter.md) | Framework drafted |
| R01 | [Accuracy ceiling](R01-accuracy-ceiling.md) | Partially holds; V&V matrix proposed |
| R02 | [Vintage data coverage cliff](R02-vintage-coverage.md) | BROKEN; Tier-V/Tier-T split |
| R03 | [Hybrid architecture evidence](R03-hybrid-evidence.md) | WEAK; L3-as-workhorse rescope |
| R04 | [BGVAR compute requirements](R04-bgvar-compute.md) | Green-light |
| R05 | [Source access terms](R05-source-access.md) | Holds for 10/12; FRED-substitution mandated |
| R06 | [Wider information surface](R06-wider-information-surface.md) | HOLDS; per-domain treatment; new SSDD-008 |

### Synthesis + Vision (R99, R100)

| ID | Title | Status |
|---|---|---|
| **R99** | **[Synthesis & CONOPS rebaseline](R99-synthesis.md)** | **Decision-ready (Option A recommended)** |
| **R100** | **[Vision: 5-year arc](R100-vision.md)** | Aspirational; informs Block I |

### Deep-dive closure memos (R07–R29)

| ID  | Title | Purpose |
|-----|-------|---------|
| R07 | [Tier-V country roster](R07-tier-v-roster.md) | Definitive ~26 Core, +9 Extended, +5 BRICS+ |
| R08 | [V&V matrix detail](R08-vv-matrix-detail.md) | 17-cell IOC matrix |
| R09 | [FRED-substitution map](R09-fred-substitution.md) | Per-series upstream-agency mapping |
| R10 | [SSDD-008 Situation Subsystem](R10-ssdd-008-situation.md) | Preliminary design |
| R11 | [Scenario invocation patterns](R11-scenario-invocation.md) | Three-path orchestration |
| R12 | [Reference systems comparison](R12-reference-systems.md) | vs FRB/US, FPAS-II, NiGEM, GEM, EAGLE, BGVAR |
| R13 | [Anvil stress-test](R13-anvil-stress-test.md) | Adversarial red-team — proposal survives |
| R14 | [L3 architecture](R14-l3-architecture.md) | Variants + combiner + feature stack |
| R15 | [Personal use cases](R15-personal-use-cases.md) | Concrete jobs-to-be-done for the owner |
| R16 | [Reproducibility architecture](R16-reproducibility.md) | Hash quintuple + replay-and-diff CI |
| R17 | [Bus-factor & sustainability](R17-bus-factor.md) | Single-maintainer risk mitigations |
| R18 | [First 90 days execution plan](R18-first-90-days.md) | Phased week-by-week plan |
| R19 | [Adapter code skeletons](R19-adapter-skeletons.md) | Python reference for 5 US agencies |
| R20 | [Contingency trees](R20-contingency-trees.md) | Pre-mortem with named Plan B branches |
| R21 | [Block II/III scoping](R21-block-2-3-scope.md) | Preview of Year 2–5 |
| R22 | [5-year cost projection](R22-cost-projection.md) | Operational cost ~$1k → $6k/yr |
| R23 | [Oblique-lawyer parallels](R23-oblique-lawyer-parallels.md) | Cross-suite lessons + integration |
| R24 | [Backtest engine design](R24-backtest-engine.md) | SSDD-007 v2 architecture |
| R25 | [Leaderboard algorithm](R25-leaderboard-algorithm.md) | OPENGEM Index v1.0 |
| R26 | [Security & privacy boundary](R26-security-privacy.md) | Threat model + secret management |
| R27 | [Open issues catalog](R27-open-issues.md) | 25 issues, P0/P1/P2/P3 ranked |
| R28 | [Glossary](R28-glossary.md) | Acronyms + concept definitions |
| R29 | [Decision framework](R29-decision-framework.md) | What would flip the A/B/C recommendation |

### Concrete rebaseline drafts

- `../design/00-program/OG1-CONOPS-001-revC-draft.md` — full CONOPS rewrite.
- `../design/00-master-design-document-v2.0-draft.md` — master doc rewrite.
- `../design/LOOP_PLAN-v2.md` — restarted loop sequence.

## Decision in front of the program owner

R99 §6: **A (accept rebaseline)** / B (renarrow) / C (sunset). Recommendation: **A**.

R29 specifies what new information would flip the recommendation, so the decision is *informed* not *coerced*.

## Sign-off mechanism

Per R29 §9, when ready:

1. Commit `SIGNOFF.md` with decision date and one-sentence rationale.
2. Tag `pre-pdr-r99-accepted-YYYY-MM-DD`.
3. Promote drafts to baseline filenames (rev C → `OG1-CONOPS-001.md`; v2.0 → `00-master-design-document.md`; LOOP v2 → `LOOP_PLAN.md`).
4. Update README banner.
5. Begin R18 Phase 0 (~4 hours, repo setup).

## Round metrics

- **Memos**: 28 (R00–R29 with gaps filled).
- **Words**: ~75k of design analysis.
- **Web searches**: ~40 across forecasting literature, data archives, ToS pages, and reference systems.
- **Code written**: 0 (per program-owner direction).
- **Decisions made**: 0 (recommendation only).
- **Days**: 1 (2026-05-24, autonomous overnight session).

## Changelog

- **2026-05-24** — Initial research round complete. 28 memos + CONOPS rev C draft + master-doc v2.0 draft + LOOP_PLAN v2 draft + Morning Briefing. Pre-PDR round closes pending program-owner decision.
