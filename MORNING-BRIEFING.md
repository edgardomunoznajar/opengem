# Morning Briefing — OPENGEM Pre-PDR Research Round

**Date completed**: 2026-05-24
**Recommended read order**: this file → R99 → CONOPS rev C → vision → deep-dives as needed.

---

## TL;DR

The pre-PDR research round (R01–R12 + R99 synthesis) is complete. **Three of the five load-bearing CONOPS rev B claims are broken or wrong; two are fine. A clean rebaseline is recommended and drafted.** No code has been written.

**What you wake up to:**

- A **complete research dossier** of 13 memos (R00–R12 + R99 + R100 vision).
- A **rev C CONOPS draft** ready for sign-off.
- A **master design document v2.0 draft** ready for sign-off.
- A **revised LOOP_PLAN v2** sequencing the restart.
- One decision in front of you (§7 below).

---

## What's broken in the rev B CONOPS

| Claim | Reality | Impact |
|---|---|---|
| "Coverage for ≥40 / ≥80 economies with full vintage backtest" | Vintage data exists for **OECD-26 + 5 ORDRA-covered BRICS+** countries, at most ~35. Emerging-market vintage archives don't exist publicly. | Adopt **Tier-V (vintage-correct ~26–35) + Tier-T (tracked-only)** split. |
| "3-layer hybrid (L1+L2+L3) dominates" | Literature doesn't show this for forecast accuracy. L3 is the workhorse; L1 narrative; L2 spillovers. Each does a different job. | **Re-architect**: L3 is the forecast critical path. L1 (US only at IOC) is narrative satellite. L2 is annual-cadence scenario satellite. |
| "FRED + ALFRED are core data sources" | FRED's 2024 ToS prohibits caching, archiving, and ML training. | **Substitute** to upstream agencies (BEA / BLS / FRB Board / Treasury / Census). FRED for discovery only. |

## What's fine in the rev B CONOPS

| Claim | Status |
|---|---|
| "BGVAR fits modest hardware" | Confirmed. R `BGVAR` package + VB fallback + annual cadence per the rescope. |
| "AR(1) is a meaningful baseline" | Reframed. A single AR(1) bar is too easy for GDP and too hard for inflation. **Replaced by a 17-cell V&V matrix** (R01 §4, R08 detail). |

## What's added by R06

The CONOPS gets a **new subsystem (SSDD-008 "Situation")** that publishes:
- **Term-spread recession probability** per Tier-V country (Bauer-Mertens replication).
- **GPR nowcast** per 44 countries (Caldara-Iacoviello extension) — *deferred build* until a skill probe validates.

Plus the wider information surface (markets, supply chain, geopolitics, media) is formally in scope as L3 covariates from free sources (GSCPI, PortWatch, GPR, GDELT).

---

## The new architecture in one diagram

```
   Upstream agencies (BEA/BLS/FRB/Treasury/Census) ──┐
   OECD ORDRA · ECB SDW · BIS · IMF SDMX · WB · UN ──┼── Ingestion + Vintage Store
   GSCPI · PortWatch · GPR · GDELT GKG · sanctions ──┘     (Tier-V vs Tier-T)
                                                              │
                                                              ▼
                                                       L3 — Workhorse Layer
                                                       (DFM + ML + BVAR variants
                                                        + BMA combiner over them)
                                                              │
                  ┌───────────────────────────────────────────┼──────────────────┐
                  ▼                                           ▼                  ▼
          Forecast Service                            Backtest Service     Scenario Subsystem
          (Tier-V leaderboard)                        (V&V matrix)         (calls L1 + L2 on demand)
                                                                                │
                                                                                ├─ L2 BGVAR (annual)
                                                                                └─ L1 US core (narrative)
   ┌──────────── Situation Subsystem (new) ─────────────┐
   │  /v1/recession-probability  ·  /v1/gpr-nowcast    │
   └────────────────────────────────────────────────────┘

   Public surface: Spring Boot REST · MCP Server · Dashboard
```

---

## The new V&V bar (the actually-meaningful one)

17 cells at IOC, ~25 at FOC. Highlights:

- **GDP-1Q**: beat AR(1) and RW by CRPS on ≥80% Tier-V. PIT pass ≥80%.
- **GDP-4Q**: not statistically worse (DM p>0.05) than WEO/OECD EO on ≥50% Tier-V. PIT ≥70%.
- **CPI-4Q**: not worse than WEO/OECD EO on ≥40% Tier-V.
- **Policy rate**: not worse than forward curve / OIS-implied.
- **Recession**: AUC ≥ 0.85 vs. Bauer-Mertens replication.

Full matrix in `docs/research/R08-vv-matrix-detail.md`.

---

## What's in the repo now

```
opengem/
├── MORNING-BRIEFING.md                  ← this file
├── README.md
├── docs/
│   ├── design/
│   │   ├── 00-master-design-document-v1.0.md           (rev B baseline; unchanged)
│   │   ├── 00-master-design-document-v2.0-draft.md     ★ DRAFT — awaiting sign-off
│   │   ├── LOOP_PLAN.md                                 (v1; paused)
│   │   ├── LOOP_PLAN-v2.md                              ★ v2 (paused pending sign-off)
│   │   └── 00-program/
│   │       ├── OG1-CONOPS-001.md                        (rev B baseline; unchanged)
│   │       └── OG1-CONOPS-001-revC-draft.md             ★ DRAFT — awaiting sign-off
│   └── research/
│       ├── README.md                                    (status board)
│       ├── R00-charter.md                               (falsifiable-hypotheses framework)
│       ├── R01-accuracy-ceiling.md                      (V&V matrix rationale)
│       ├── R02-vintage-coverage.md                      (Tier-V/Tier-T)
│       ├── R03-hybrid-evidence.md                       (L3-as-workhorse)
│       ├── R04-bgvar-compute.md                         (green-light)
│       ├── R05-source-access.md                         (FRED-substitution mandate)
│       ├── R06-wider-information-surface.md             (SSDD-008 + L3 covariates)
│       ├── R07-tier-v-roster.md                         (definitive country list)
│       ├── R08-vv-matrix-detail.md                      (full 17-cell matrix)
│       ├── R09-fred-substitution.md                     (upstream-agency map)
│       ├── R10-ssdd-008-situation.md                    (Situation Subsystem design)
│       ├── R11-scenario-invocation.md                   (L1+L2 invocation paths)
│       ├── R12-reference-systems.md                     (vs. FRB/US, FPAS-II, NiGEM, GEM, EAGLE, BGVAR)
│       ├── R99-synthesis.md                             ★ READ FIRST after this briefing
│       └── R100-vision.md                               (5-year arc, dream-big)
```

★ = artifacts produced this round; rest are inputs or prior baseline.

---

## The decision in front of you

**One decision, three options.** R99 §6 spells these out. Restated here:

**A. Accept rebaseline.** Sign rev C CONOPS + master-doc v2.0; restart LOOP_PLAN v2; begin upstream-agency adapter work in parallel with SAD/SSDD decomposition. **This is the recommendation.**

**B. Renarrow scope further.** Block I = "L3 only on Tier-V; no L1/L2; no Situation Subsystem." Minimal product. Re-evaluate later.

**C. Sunset.** The data foundation is too narrow, FRED issues too annoying, narrative value not worth its cost. Mothball cleanly.

R99 argues for **A** because the unique value proposition (open + vintage + density + leaderboard + MCP + situation) **does not exist anywhere else**, and the rebaseline keeps that unique combination buildable at personal scale.

---

## Open probes still deferred (low priority, won't change the decision)

- BIS Policy Rates programmatic-access verification (will land in R05's source map at SAD-2 time).
- ORDRA full variable matrix per country, especially BRICS+ (verify at SRR-2).
- ABS Australia revision-triangles batch request (one email; load once).
- WEO + OECD EO historical-vintage download paths (verify at SRR-2).
- GPR-nowcast skill probe (gates the SSDD-008 second endpoint).
- Custom topic model on news (deferred to v0.4+ at earliest).
- Consensus Economics access (deferred to future public-launch round).

---

## Vision (in case you want the long view)

`docs/research/R100-vision.md` is a deliberately aspirational 5-year arc — Block I as foundation; Block II width (40+ Tier-V); Block III depth + sovereign-grade hosting for small economies; Block IV public goods (dataset as standard); Block V five-year retrospective.

The single sentence:

> OPENGEM is a personal-scale, public-accountability macroeconometric forecasting system whose Block I builds the foundation for a five-year arc toward becoming a sovereign-grade open forecast infrastructure, accountable to its own public track record, owned by no institution, and irreducibly more honest than the systems it eventually displaces.

The vision document acknowledges where the dream could break (V&V failure, single-maintainer attrition, no demand for hosted-sovereignty, incumbent counterattack).

---

## What I'd do next (if you say Option A)

Sequence per LOOP_PLAN v2:

1. **SRR-2**: walk through rev C CONOPS and v2.0 master doc; sign off; baseline.
2. **Iter 02–03**: refresh StRS and SRS at v2 with Tier-V/Tier-T language, V&V matrix, wider information surface.
3. **Iter 04**: SAD v2 with the new ADRs (ADR-005..014).
4. **Iter 05**: ICD-001 with the upstream-agency adapter cohort spec.
5. **Iter 12**: SSDD-001 v2 with the adapter cohort detailed.
6. In parallel — once Iter 05 is signed — **start coding the BEA + BLS + FRB Board adapters**. These are independent, deterministic, well-scoped. ~1–2 weeks to functional ingestion of US series.

That gets a working data layer for Tier-V Core US within 3–4 weeks of sign-off. L3 first-pass forecasts on US data follow ~2 weeks after that. First Tier-V Core IOC milestone at ~3 months.

---

## Addendum — full dossier scope (updated overnight)

The research round expanded beyond R01–R06 + R99 + R100 into a full decision-ready dossier of **28 memos** plus the three concrete drafts (CONOPS rev C, master-doc v2.0, LOOP_PLAN v2).

Deep-dive memos worth reading if you have time:

- **R29 [Decision framework](docs/research/R29-decision-framework.md)** — what would flip A → B / C / wait. Read alongside R99 for honest decision-making.
- **R18 [First 90 days execution plan](docs/research/R18-first-90-days.md)** — phased weekly plan, ~56 hours total across 13 weeks. Most actionable artifact.
- **R13 [Anvil stress-test](docs/research/R13-anvil-stress-test.md)** — 10 hostile attacks on the proposal; survives with 2 acknowledged residual risks.
- **R15 [Personal use cases](docs/research/R15-personal-use-cases.md)** — concrete jobs-to-be-done; sanity check for "do I actually want this?"
- **R20 [Contingency trees](docs/research/R20-contingency-trees.md)** — pre-mortem; every failure has a named Plan B.
- **R23 [Oblique-lawyer parallels](docs/research/R23-oblique-lawyer-parallels.md)** — cross-suite lessons + attention-conflict naming.

For implementation specifics:

- **R09 [FRED-substitution map](docs/research/R09-fred-substitution.md)** — every FRED series → upstream agency.
- **R19 [Adapter code skeletons](docs/research/R19-adapter-skeletons.md)** — reference Python implementations.
- **R10 [SSDD-008 Situation Subsystem](docs/research/R10-ssdd-008-situation.md)** — the new subsystem in detail.
- **R14 [L3 architecture](docs/research/R14-l3-architecture.md)** — variants + combiner detail.
- **R16 [Reproducibility architecture](docs/research/R16-reproducibility.md)** — hash quintuple + replay-and-diff CI.

For long-arc context:

- **R100 [Vision: 5-year arc](docs/research/R100-vision.md)** — aspirational ceiling.
- **R21 [Block II/III scoping](docs/research/R21-block-2-3-scope.md)** — what comes after Block I.
- **R22 [Cost projection](docs/research/R22-cost-projection.md)** — ~$1k/yr Block I, ~$6k/yr Block IV+.

## Sign-off mechanism

If Option A:

1. Commit `SIGNOFF.md` to repo root with decision date + one-sentence rationale.
2. Tag `pre-pdr-r99-accepted-2026-MM-DD`.
3. Promote drafts: `OG1-CONOPS-001-revC-draft.md` → `OG1-CONOPS-001.md`; `00-master-design-document-v2.0-draft.md` → replaces `v1.0`; `LOOP_PLAN-v2.md` → `LOOP_PLAN.md`.
4. Update README banner.
5. Begin R18 Phase 0.

---

*End of Morning Briefing. Full dossier in `docs/research/`. Pre-PDR round closed pending your decision. No code written. Sleep well.*
