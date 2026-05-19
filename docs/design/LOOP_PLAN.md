# OPENGEM Design Loop Plan

**Purpose:** sequence the decomposition of the master design document (`00-program/00-master-design-document-v1.0.md`) into per-document artifacts at full waterfall detail.

**Loop discipline:** one iteration = one document realized at "draft B" quality (≥3× the depth of the master-doc section it replaces). When done, the master-doc section becomes a stub linking forward to the realized file, and a checkbox below is ticked.

## Decomposition order (dependency-respecting)

Order chosen so that downstream documents can reference upstream ones without forward-declared TBDs.

- [x] **Iter 01 — OG1-CONOPS-001** Concept of Operations (full OV-1/OV-2/OV-5 textual, expanded scenarios, exclusions, success/failure narratives) — *realized 2026-05-19*
- [ ] **Iter 02 — OG1-STRS-001** Stakeholder Requirements (expanded, with stakeholder interviews framed as personas, full needs decomposition)
- [ ] **Iter 03 — OG1-SRS-001** System Requirements (full FR/NFR/IFR catalog with verification methods, completed traceability)
- [ ] **Iter 04 — OG1-SAD-001** System Architecture (logical, physical, deployment, runtime; ADR-001…ADR-020+; views per 4+1)
- [ ] **Iter 05 — OG1-ICD-001** External Data Source Interfaces (one row per source, full schemas, rate limits, fallbacks)
- [ ] **Iter 06 — OG1-ICD-002** Public REST API (OpenAPI 3.1 stubs as YAML inside doc; auth model; error model)
- [ ] **Iter 07 — OG1-ICD-003** MCP Server Contract (tool list, resource list, prompt list, auth, monetization gates)
- [ ] **Iter 08 — OG1-ICD-004** Java ↔ Python gRPC (full proto, streaming semantics, deadline propagation)
- [ ] **Iter 09 — OG1-ICD-005** Model Service ↔ PostgreSQL (role model, connection pooling, migration policy)
- [ ] **Iter 10 — OG1-ICD-006** Orchestrator ↔ Subsystems (Dagster asset graph DSL, partition spec)
- [ ] **Iter 11 — OG1-DBDD-001** Database Design (full ER, all tables with column-level spec, indexes, retention)
- [ ] **Iter 12 — OG1-SSDD-001** Data Ingestion Subsystem
- [ ] **Iter 13 — OG1-SSDD-002** Data Curation & Feature Subsystem
- [ ] **Iter 14 — OG1-SSDD-003** Model L1 — Country Cores (per-country equation system, priors, identification)
- [ ] **Iter 15 — OG1-SSDD-004** Model L2 — Bayesian GVAR (full spec, weight matrix design, identification choices)
- [ ] **Iter 16 — OG1-SSDD-005** Model L3 — DFM + ML Residual (state-space spec, feature inventory)
- [ ] **Iter 17 — OG1-SSDD-005a** Combiner — BMA over L1/L2/L3 (weight evolution, freezing rules)
- [ ] **Iter 18 — OG1-SSDD-006** Scenario Subsystem (shock grammar, identification selector, caching)
- [ ] **Iter 19 — OG1-SSDD-007** Backtest & Publication Subsystem (vintage replayer, metric engine, leaderboard schema)
- [ ] **Iter 20 — OG1-VVP-001** Verification & Validation Plan (test pyramid, vintage CI, gate-by-gate exit tests)
- [ ] **Iter 21 — OG1-RISK-001** Risk Register (expanded to 25+ risks, response plans, owners, tripwires)
- [ ] **Iter 22 — OG1-WBS-001** WBS & Schedule (level-4 WBS, Gantt-style table, critical path)
- [ ] **Iter 23 — OG1-AGP-001** Acceptance, Gates, Phasing (canonical workload specs, evidence per gate)
- [ ] **Iter 24 — OG1-CMP-001** Configuration Management (CI inventory, baselines, ECP workflow, release engineering)
- [ ] **Iter 25 — Glossary + Acronyms** (Appendix A fleshed out)
- [ ] **Iter 26 — Traceability Matrix Complete** (every Req → SSDD → V&V cell filled)
- [ ] **Iter 27 — Pre-PDR review pass** (consistency audit across all docs, kill TBDs, finalize ADRs)

## Iteration protocol

1. Read the master document section + any prior realized docs the new doc must reference.
2. Draft the target file in its destined folder.
3. Replace the master document section with a stub: `*Realized in [`OG1-XXX-NNN.md`](path).*`
4. Update this LOOP_PLAN: tick the box, add notes if new TBDs surfaced.
5. Commit with message `design(OG1-XXX-NNN): realize <title>`.
6. Schedule next wakeup (if running autonomously) or yield.

## Exit criterion for the loop

All boxes ticked AND zero unresolved TBDs except those legitimately deferred to CDR/OCR per Appendix B. At that point the design set is **PDR-ready**.
