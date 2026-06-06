# OPENGEM Design Loop Plan — v2 (post-rebaseline)

| Field | Value |
|---|---|
| Version | v2 (DRAFT, supersedes `LOOP_PLAN.md` v1 upon sign-off) |
| Date | 2026-05-24 |
| Authority | R99 synthesis |
| Predecessor | `LOOP_PLAN.md` (v1) |

**Purpose**: sequence the decomposition of the **v2.0 master design document** into per-document artifacts.

**Discipline**: one iteration = one document at "draft B" (≥3× the depth of the master-doc section it replaces). When done, master-doc section becomes a stub link-forward and a checkbox below ticks.

**Pre-condition**: program-owner sign-off on
- `R99-synthesis.md` (recommendation)
- `OG1-CONOPS-001-revC-draft.md` (rev C CONOPS)
- `00-master-design-document-v2.0-draft.md` (v2.0 master doc)

Until that sign-off, **the loop is paused**.

## Decomposition order (post-rebaseline)

- [x] **Iter 00 — Pre-PDR Research Round** (R01–R06 + R99 synthesis + draft rev C / v2.0) — *realized 2026-05-24*
- [ ] **Iter 02 — OG1-STRS-001 v2** Stakeholder Requirements (Tier-V/Tier-T split, wider info surface, FRED-substitution)
- [ ] **Iter 03 — OG1-SRS-001 v2** System Requirements (FR/NFR/IFR with V&V matrix per cell)
- [ ] **Iter 04 — OG1-SAD-001 v2** System Architecture (revised logical view; ADR-005..014)
- [ ] **Iter 05 — OG1-ICD-001 v2** External Data Source Interfaces (upstream-agency cohort)
- [ ] **Iter 06 — OG1-ICD-002 v2** Public REST API (incl. `/recession-probability`, `/gpr-nowcast`, `/tracked`)
- [ ] **Iter 07 — OG1-ICD-003 v2** MCP Server Contract (new tools)
- [ ] **Iter 08 — OG1-ICD-004** Java ↔ Python gRPC (incl. R adapter for L2)
- [ ] **Iter 09 — OG1-ICD-005** Model Service ↔ PostgreSQL
- [ ] **Iter 10 — OG1-ICD-006** Orchestrator ↔ Subsystems (Tier-V partitions; annual L2 partition)
- [ ] **Iter 11 — OG1-DBDD-001 v2** Database Design (incl. Tier-V/Tier-T tables, Situation tables)
- [ ] **Iter 12 — OG1-SSDD-001 v2** Data Ingestion (upstream-agency adapter cohort)
- [ ] **Iter 13 — OG1-SSDD-002 v2** Data Curation & Feature
- [ ] **Iter 14 — OG1-SSDD-003 v2** L1 — US-only core
- [ ] **Iter 15 — OG1-SSDD-004 v2** L2 — Annual BGVAR (R adapter)
- [ ] **Iter 16 — OG1-SSDD-005 v2** L3 — Workhorse Forecast Layer (DFM + ML + large BVAR variants)
- [ ] **Iter 17 — OG1-SSDD-005a v2** Combiner — BMA over L3 variants
- [ ] **Iter 18 — OG1-SSDD-006 v2** Scenario Subsystem (L1+L2 invocation)
- [ ] **Iter 19 — OG1-SSDD-007 v2** Backtest & Publication (V&V matrix, Tier-V/Tier-T split)
- [ ] **Iter 19a (NEW) — OG1-SSDD-008** Situation Subsystem (term-spread + GPR nowcast)
- [ ] **Iter 20 — OG1-VVP-001 v2** Verification & Validation Plan (matrix gates)
- [ ] **Iter 21 — OG1-RISK-001 v2** Risk Register (per master-doc §9 v2.0)
- [ ] **Iter 22 — OG1-WBS-001 v2** WBS & Schedule (re-sequenced)
- [ ] **Iter 23 — OG1-AGP-001 v2** Acceptance/Gates/Phasing (matrix-based gates)
- [ ] **Iter 24 — OG1-CMP-001** Configuration Management
- [ ] **Iter 25 — Glossary + Acronyms** (incl. Tier-V/Tier-T, GSCPI, GPR, etc.)
- [ ] **Iter 26 — Traceability Matrix Complete** (every Req → SSDD → V&V cell)
- [ ] **Iter 27 — Pre-PDR review pass** (consistency audit; finalize ADRs)

## Iteration protocol (unchanged from v1)

1. Read master section + prior realized docs.
2. Draft target file in destined folder.
3. Replace master-doc section with stub forward-link.
4. Update this LOOP_PLAN: tick box, note new TBDs.
5. Commit with `design(OG1-XXX-NNN): realize <title>`.
6. Schedule next wakeup or yield.

## Exit criterion

All boxes ticked AND zero unresolved TBDs except those legitimately deferred. At that point the design set is **PDR-ready** and implementation can begin under the new Block I scope.

---

*Authority: R99 synthesis, 2026-05-24.*
