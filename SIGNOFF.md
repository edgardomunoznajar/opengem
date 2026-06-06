# Pre-PDR Sign-off

**Date**: 2026-06-06
**Program Owner**: edgardo
**Decision**: **A — Accept rebaseline**

**One-sentence rationale**:
> The unique value proposition (open + vintage-correct + dense + leaderboard +
> MCP + situation) exists nowhere else and remains buildable at personal scale;
> the rebaseline keeps that combination viable, and a working-and-verified
> Block I foundation (245 tests green) now exists in git to build on.

**References reviewed**:
- [x] R99 Synthesis (docs/research/R99-synthesis.md)
- [x] R29 Decision framework (docs/research/R29-decision-framework.md)
- [x] R13 Anvil stress-test (docs/research/R13-anvil-stress-test.md)
- [x] R15 Personal use cases (docs/research/R15-personal-use-cases.md)
- [x] CONOPS rev C (promoted from draft — see below)
- [x] Master design doc v2.0 (promoted from draft — see below)
- [x] LOOP_PLAN v2 (promoted from draft — see below)
- [x] **STATE-OF-REALITY.md** — evidence-based audit of what is real vs stub
      (added this round; the honest counterpart to the design dossier)

## Verification basis for accepting (Goal A, 2026-06-06)

This sign-off is backed by a reproducible verification pass, not just document
review:

- `uv sync --all-packages` installs all 21 Python workspace members editable.
- `ruff check .` passes (shipped code).
- `pytest` → **245 passed** (was 33 collection errors — nothing had ever been
  installed; no source logic was broken).
- 20 / 21 packages import cleanly; `opengem-mcp` is a broken stub (documented).
- Dashboard (`npm run build`) succeeds after 3 fixes; FastAPI `opengem-api` is a
  prototype stub.
- CI authored (`.github/workflows/ci.yml`) and validated locally.

Full evidence and the real-vs-stub map: **STATE-OF-REALITY.md**.

## Honest answers to the pre-mortem questions (R29 §7)

> "If, 12 months from now, OPENGEM Block I is unfinished and I've abandoned it,
> what was the most likely reason?"

Most likely: single-maintainer attrition (competing projects in the oblique
suite + novel + others), OR the V&V matrix proves harder than expected once a
real-data backtest runs (the matrix is currently design-only; no backtest
harness exists yet — see SSDD-007 "stub" in STATE-OF-REALITY.md).

> What I've committed in time per week:

`[owner to confirm]` — R18 estimates ~56 hours total across 13 weeks (~4–5
hrs/week) to a Tier-V Core US IOC.

> Risks I'm consciously accepting (from R13 / R20):

- **Data-path risk**: every adapter is mocked; no live BEA/BLS/FRB pull has run.
  Upstream schema/auth/rate-limit reality is undiscovered.
- **Scope risk**: L1, L2, the L3 BMA combiner, and the backtest/V&V harness are
  unbuilt; "Block I IOC" currently means L3-DFM only.
- **Country-code debt**: forecasts use ISO-2, event data uses ISO-3; must be
  normalized before SSDD-002.
- **Surface debt**: the MCP monetization lever does not currently run.

**Promotion of drafts to baseline** (Decision = A):

- [x] `OG1-CONOPS-001-revC-draft.md` → `OG1-CONOPS-001.md` (rev C is baseline; rev B in git history)
- [x] `00-master-design-document-v2.0-draft.md` → `00-master-design-document.md`
- [x] `LOOP_PLAN-v2.md` → `LOOP_PLAN.md` (v2 is baseline; v1 in git history)
- [x] README banner updated (counts reconciled: 245 tests, not 183)
- [x] Tags committed: `v2.0-baseline` and `pre-pdr-r99-accepted-2026-06-06`

**Next action** (per R18 Phase 0): the foundation is green and baselined. Next
checkpoint is the first **real-data** US pull (BEA/BLS/FRB) → vintage store →
L3-DFM forecast — the step that converts mocked confidence into real confidence.

---

*Signed off under Goal A — "Green, Honest, Baselined", 2026-06-06.*
