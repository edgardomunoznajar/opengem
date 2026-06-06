# Program OPENGEM-1 — Master Design Document v2.0 (DRAFT)
## Block I — Post-Pre-PDR Rebaseline

| Field | Value |
|---|---|
| Document Set Version | **2.0 (DRAFT)** — supersedes v1.0 |
| Classification | Open / Unclassified |
| Lifecycle Model | Waterfall (DoD-5000 / MIL-STD-498 derived) |
| Prepared by | Chief Systems Engineer (acting) |
| Date | 2026-05-24 |
| Status | **Pre-PDR, post-rebaseline. Awaiting program-owner sign-off to baseline.** |
| Predecessor | `00-master-design-document-v1.0.md` (rev B baseline) |
| Authority for changes | R99 synthesis + R01–R06 research memos |

> This is the integrated master design document at v2.0. Decomposition into per-document artifacts (SSDDs, ICDs, DBDD, …) resumes under the restarted LOOP_PLAN once this document is baselined.

---

## 0. Document Set Index (revised)

| # | Doc ID | Title | §  | Realized in |
|---|---|---|---|---|
| 1 | OG1-CONOPS-001 | Concept of Operations | §1 | `00-program/OG1-CONOPS-001-revC-draft.md` (rev C draft) |
| 2 | OG1-STRS-001 | Stakeholder Requirements | §2 | TBD (LOOP_PLAN Iter 02) |
| 3 | OG1-SRS-001 | System Requirements | §3 | TBD (Iter 03) |
| 4 | OG1-SAD-001 | System Architecture | §4 | TBD (Iter 04) |
| 5 | OG1-SSDD-001..008 | Subsystem Designs | §5 | TBD (Iter 12–19a) |
| 6 | OG1-ICD-001..006 | Interface Control | §6 | TBD (Iter 05–10) |
| 7 | OG1-DBDD-001 | Database Design | §7 | TBD (Iter 11) |
| 8 | OG1-VVP-001 | V&V Plan | §8 | TBD (Iter 20) |
| 9 | OG1-RISK-001 | Risk Management | §9 | TBD (Iter 21) |
| 10 | OG1-WBS-001 | WBS & Schedule | §10 | TBD (Iter 22) |
| 11 | OG1-AGP-001 | Acceptance, Gates, Phasing | §11 | TBD (Iter 23) |
| 12 | OG1-CMP-001 | Configuration Management | §12 | TBD (Iter 24) |

---

## 1. CONOPS

*Realized in [`OG1-CONOPS-001-revC-draft.md`](00-program/OG1-CONOPS-001-revC-draft.md). Summary: OPENGEM is a personal-use OECD-26 vintage-correct macroeconometric forecasting + situation-awareness system, with L3 as the workhorse forecast layer, L2/L1 as scenario/narrative satellites, and a new Situation Subsystem.*

---

## 2. Stakeholder Requirements (refreshed)

| StRS-ID | Requirement | Source |
|---|---|---|
| StRS-001 | Produce GDP, CPI, policy rate, and unemployment density forecasts for **Tier-V** economies (~25 at IOC, ~30 at FOC). Tracked-only panel for **Tier-T** (~50+). | SH-01 |
| StRS-002 | Forecasts published with density (P10/P50/P90), not only point. | SH-01, SH-03 |
| StRS-003 | All forecasts reproducible from `(code_sha, vintage_hash, prior_hash, posterior_hash)`. | SH-02, SH-03 |
| StRS-004 | Tier-V backtests use vintage (real-time) data only. | SH-03 |
| StRS-005 | Public leaderboard compares to **≥4 benchmarks: AR(1), RW, WEO, OECD EO.** Consensus added when access path resolves. | SH-03 |
| StRS-006 | Production cost ≤ USD 200/month informational (no hard gate). | SH-04 |
| StRS-007 | System exposes MCP-compatible interface for personal-agentic use. | SH-04, SH-05 |
| StRS-008 | All code, schemas, priors, posteriors open-licensed. | SH-02 |
| StRS-009 | Ad-hoc scenario response ≤60s for canonical workload. | SH-01 |
| StRS-010 | Every published forecast preserved indefinitely. | SH-03 |
| **StRS-011 (new)** | **Wider information surface (D-MKT, D-SCN, D-GEO, D-MED) ingested as L3 covariates from free public sources.** | R06 |
| **StRS-012 (new)** | **Term-spread recession-probability endpoint published for Tier-V; GPR nowcast endpoint deferred to v0.4+.** | R06 |
| **StRS-013 (new)** | **No reliance on FRED/ALFRED for persistent data; upstream agencies authoritative.** | R05 |

---

## 3. System Requirements (refreshed)

### 3.1 Functional Requirements

| Req-ID | Statement | Traces |
|---|---|---|
| FR-DAT-001 | Ingest macro time series from ≥8 named sources: **BEA, BLS, FRB Board, Treasury, Census, OECD ORDRA, ECB SDW, BIS, IMF SDMX, World Bank WDI, UN Comtrade.** FRED used only for series discovery, never as persistent source. | StRS-001, 003, 013 |
| FR-DAT-002 | Every ingestion writes a new vintage row; revisions never overwrite. | StRS-003, 004 |
| FR-DAT-003 | Ingest **≥5 information-surface sources: GSCPI, PortWatch, GPR (Caldara-Iacoviello), GDELT GKG, OFAC/EU/UN sanctions lists.** | StRS-011 |
| FR-MOD-001 | Implement **L3 (DFM + ML residual + large BVAR variants) as the baseline forecast layer**; L2 (Bayesian GVAR) on annual cadence for scenarios; L1 (US semi-structural core) for scenario identification. | StRS-002 |
| FR-MOD-002 | L2 uses bilateral trade weights from Comtrade with annual refresh. | StRS-001 |
| FR-MOD-003 | **Combiner produces density forecast via BMA over L3 variants (DFM-only, DFM+RF, DFM+GBM, large BVAR variants).** Weights from rolling-window predictive log score. | StRS-002 |
| FR-FOR-001 | Forecast Service publishes at horizons {1Q, 4Q, 8Q, 20Q}. | StRS-001 |
| FR-FOR-002 | Each forecast record carries provenance triplet + run_id. | StRS-003, 010 |
| FR-SCN-001 | Scenario Subsystem accepts shocks as structured JSON. | StRS-009 |
| FR-SCN-002 | Scenario returns IRFs and counterfactual densities ≤60s for canonical workload. | StRS-009 |
| FR-BCT-001 | Backtest runs rolling-origin OOS evaluation on stored vintages with windows {1Q, 4Q, 8Q, 20Q}, **Tier-V only**. | StRS-004 |
| FR-BCT-002 | Backtest computes RMSE, MAE, CRPS, log score, DM, MCS against **AR(1), RW, WEO, OECD EO**. | StRS-005 |
| FR-PUB-001 | Public leaderboard served, **Tier-V only**, refreshed weekly. | StRS-005 |
| FR-PUB-002 | REST + MCP endpoints exposed. | StRS-007 |
| FR-CFG-001 | Every artifact addressable by content hash. | StRS-003 |
| **FR-SIT-001 (new)** | **Situation Subsystem publishes `/v1/recession-probability?country=&horizon=` using a Bauer-Mertens-style term-spread model, Tier-V countries, daily refresh.** | StRS-012 |
| **FR-SIT-002 (new)** | **Situation Subsystem publishes `/v1/gpr-nowcast?country=&horizon=` for 44 countries (deferred build pending forecast-skill probe).** | StRS-012 |

### 3.2 Non-Functional Requirements

| Req-ID | Statement | Method |
|---|---|---|
| NFR-PRF-001 | p95 latency of `/forecast` GET ≤ 500 ms | Test |
| NFR-PRF-002 | p95 latency of `/scenario` POST ≤ 60 s (canonical workload) | Test |
| NFR-PRF-003 | **L3 quarterly full run ≤ 2h** on baseline (4 vCPU / 16 GB). **L2 annual re-est. ≤ 12h** on moderately sized node. L1 (US) quarterly ≤ 30min. | Test |
| NFR-AVL-001 | Read API availability ≥ 99.0% monthly | Inspect |
| NFR-COS-001 | Production cost ≤ USD 200/month **informational** (no auto-rebase). | Analysis |
| NFR-SEC-001 | No PII; secrets via vault. | Inspect |
| NFR-MNT-001 | Bus factor ≥ 1 with doc-as-code. | Inspect |
| NFR-RPR-001 | Bit-identical reproduction from hash triplet on baseline image. | Test |

### 3.3 Interface Requirements

Carried forward from v1.0 with the new SSDD-008 interface added (Situation REST + MCP entries).

---

## 4. System Architecture

### 4.1 Logical View (revised)

```
+-------------------------------------------------------------------+
| L7  Publication       | Leaderboard (Tier-V) · Dashboard ·        |
|                       | Tracked panel (Tier-T) · MCP Server        |
+-------------------------------------------------------------------+
| L6  API               | Spring Boot Read API (Java 21)             |
+-------------------------------------------------------------------+
| L5  Orchestration     | Dagster job graph (Python)                 |
+-------------------------------------------------------------------+
| L4  Application       | Forecast | Scenario | Backtest | Situation |
|   ─ critical path:    |   (L3)   |  (L1+L2) | (Tier-V) |   (new)   |
+-------------------------------------------------------------------+
| L3  Model             | L3 workhorse: DFM + ML residual + BVAR     |
|                       | variants; BMA combiner over variants       |
|                       | --- L2 scenario satellite: BGVAR (R) ---   |
|                       | --- L1 narrative satellite: US core only - |
+-------------------------------------------------------------------+
| L2  Data              | PostgreSQL + TimescaleDB | MinIO object    |
+-------------------------------------------------------------------+
| L1  Ingestion         | Upstream-agency adapters (BEA/BLS/FRB/...) |
|                       | + OECD ORDRA / ECB SDW / BIS / Comtrade /  |
|                       | IMF SDMX / WB WDI / GSCPI / GPR / GDELT    |
+-------------------------------------------------------------------+
```

### 4.2 Physical View (Block I, IOC)

| Node | Spec | Role |
|---|---|---|
| `og-app-01` | 4 vCPU / 16 GB / 200 GB SSD | Spring API, FastAPI, Dagster, L3 quarterly |
| `og-db-01` | 4 vCPU / 16 GB / 500 GB SSD | Postgres + TimescaleDB + MinIO |
| `og-gpu-01` | Ephemeral Modal/RunPod A10G | Monthly L3 boost-tree retraining; optional |
| `og-gvar-01` | **Annual burst** — moderately sized (8–16 vCPU / 32–64 GB) node | L2 BGVAR re-estimation (once per year) |
| Vercel | Free tier | Public dashboard |
| GitHub | Free public | Code, releases, Pages mirror |

### 4.3 Deployment View

- Containers: Docker, Docker Compose at IOC; k3s deferred to Block II.
- CI/CD: GitHub Actions; GHCR.
- Secrets: SOPS + age.
- **L2 BGVAR R container** built once, used annually; R 4.4+ with `BGVAR` 2.5.8.

### 4.4 Architectural Decision Records (ADRs)

ADRs from v1.0 revised + new ADRs from R03/R04/R05/R06:

| ADR | Decision | Rationale |
|---|---|---|
| ADR-001 | Java Spring Boot for read API | Stack standard (unchanged) |
| ADR-002 | Python for L3 model service | Stan/NumPyro/Nixtla/scikit-learn (unchanged) |
| ADR-003 | PostgreSQL + TimescaleDB | (unchanged) |
| ADR-004 | Reject Neo4j for Block I | (unchanged) |
| **ADR-005 (revised)** | **Three layers, three jobs: L3 forecasts, L2 spillovers, L1 narrative. Not three forecast producers.** | R03 evidence: combination > single, but 3-layer hybrid not strictly dominant; each layer does a distinct job |
| ADR-006 | Vintage-first data layer | (unchanged for Tier-V) |
| **ADR-007 (revised)** | **BMA over L3 variants, not over L1+L2+L3.** | Rossi-Sekhposyan: BMA + equal-weight competitive for density |
| ADR-008 | Single MCP server, dual-mode REST + MCP | (unchanged) |
| **ADR-009 (new)** | **Use R `BGVAR` package for L2 via process adapter, not Python reimplementation** | Mature CRAN package; companion paper JSS 104(9); save months of work |
| **ADR-010 (new)** | **Upstream-agency adapters for US (BEA/BLS/FRB/Treasury/Census), not FRED/ALFRED for persistent data.** | FRED 2024 ToS prohibits caching and ML training |
| **ADR-011 (new)** | **Two-tier coverage: Tier-V (vintage-correct, ~25 countries, leaderboard-eligible) and Tier-T (tracked-only, ~50+, dashboard only).** | R02 evidence: vintage data does not exist for non-OECD-26 |
| **ADR-012 (new)** | **VB fallback approved for L2 if MCMC times out** | Koop-Korobilis: VB ≈ MCMC for predictive use at large scale |
| **ADR-013 (new)** | **V&V is a per-cell matrix (variable × horizon × benchmark), not a single AR(1) win rate** | R01: single bar dodges hard cells; matrix forces honest assessment |
| **ADR-014 (new)** | **Wider information surface (markets, supply chain, geopolitics, media) is in scope at IOC as L3 covariates plus one new endpoint (recession probability).** | R06 evidence: forecast power documented in all four domains |

---

## 5. Subsystem Design Documents

### 5.1 SSDD-001 — Data Ingestion Subsystem

Same purpose as v1.0; **adapter cohort revised** per ADR-010:
- **Upstream US**: BEA (NIPA), BLS (CPI, PPI, employment), FRB Board (rates, monetary, IP), Treasury (yields), Census (M3 inventory).
- **Multi-country**: OECD ORDRA (vintages), OECD MEI (latest), ECB SDW (EA + members), BIS (rates, banking, BoP), IMF SDMX (IFS, WEO, GFS), WB WDI.
- **Trade**: UN Comtrade.
- **Information surface**: NY Fed GSCPI, IMF PortWatch, Caldara-Iacoviello GPR, GDELT GKG, sanctions lists.

### 5.2 SSDD-002 — Data Curation & Feature Subsystem

Unchanged from v1.0 in role: frequency harmonization, seasonal adjustment, outlier detection, trade-weight building, alt-data alignment. **Adds**: covariate panel assembly from information-surface sources.

### 5.3 SSDD-003 — Model L1 (US semi-structural core)

**Reduced from "per-country" to US-only at IOC.** 10–15 equations: IS, Phillips, Taylor, UIP, fiscal closure. Estimator: NUTS in NumPyro. Job: **scenario identification and narrative**, not forecast critical path. Block II+ adds other countries if narrative value demonstrated.

### 5.4 SSDD-004 — Model L2 (Bayesian GVAR)

Uses **`BGVAR` R package (Boeck-Feldkircher-Huber 2022)** via process adapter. Hierarchical Minnesota / SSVS / Normal-Gamma prior options. Annual re-estimation. **Job**: spillover IRFs and joint scenario propagation. Trade-weight matrices from Comtrade (annual refresh).

### 5.5 SSDD-005 — Model L3 (Workhorse forecast layer)

**Promoted to the primary forecast producer.** Components:

- Mixed-Frequency DFM (state-space Kalman filter).
- ML residual: LightGBM (and/or RF, GBM) on factor scores + alt-data features.
- Large BVAR variants (Banbura-Giannone-Reichlin style, Minnesota natural conjugate priors).
- BMA combiner over the above variants (ADR-007 revision).

Output: Tier-V density forecasts at 1Q/4Q/8Q/20Q for GDP, CPI, policy rate, unemployment.

### 5.6 SSDD-006 — Scenario Subsystem

Same purpose as v1.0. **Invocation flow revised**: calls L1 (US identification when origin=US), then L2 (propagate), then L3-conditional re-evaluation. L1 always optional; default is L2 Cholesky / sign restrictions.

### 5.7 SSDD-007 — Backtest & Publication Subsystem

**Tier-V only** for leaderboard inclusion. Components: Vintage Replayer, Benchmark Fetcher (WEO/OECD EO/forward-curve), Metric Engine (RMSE/MAE/CRPS/LS/DM/MCS per variable×horizon matrix from R01 §4), Leaderboard Materializer, Forecast Archiver, **Tracked-Panel Materializer (Tier-T, no leaderboard inclusion).**

### 5.8 SSDD-008 (NEW) — Situation Subsystem

**Purpose**: Publish two information-surface endpoints.

**Components**:
- Term-Spread Engine: Bauer-Mertens-style recession-probability model per Tier-V country (10y–3m spread + extensions). Daily refresh.
- GPR Nowcast Engine (deferred build): predicts country GPR index 1–3 months ahead from GDELT GKG covariates. Daily granularity. Built only after a skill probe demonstrates value above persistence baseline.

**Outputs**: `/v1/recession-probability` and `/v1/gpr-nowcast` REST + MCP endpoints. Own model cards, own V&V.

---

## 6. Interface Control Documents

Carried forward from v1.0 with additions:

- **ICD-001** updated source list (R05 §6).
- **ICD-002** adds `/v1/recession-probability`, `/v1/gpr-nowcast`, `/v1/tracked/{country}/series` (Tier-T browse).
- **ICD-003** adds MCP tools: `recession_probability`, `gpr_nowcast`, `tracked_country_view`.
- **ICD-004** unchanged.
- **ICD-005** adds role `situation_rw` for SSDD-008.
- **ICD-006** adds Dagster asset partitions per Tier-V country and per Situation endpoint.

---

## 7. Database Design (refreshed)

Conceptual entities unchanged. Physical tables add:

| Table | Type | Notes |
|---|---|---|
| `tier_v_roster` | Relational | List of Tier-V countries (current; date-versioned) |
| `tier_t_roster` | Relational | Tier-T countries |
| `recession_prob` | Hypertable | Daily Bauer-Mertens output per Tier-V |
| `gpr_nowcast` | Hypertable | Daily GPR nowcast (when built) |
| `info_surface` | Hypertable | GSCPI, PortWatch, GPR, GDELT GKG aggregated covariates |
| `benchmark_forecast` | Hypertable | WEO, OECD EO, AR(1), RW per country×variable×horizon×vintage |

Retention policy unchanged.

---

## 8. Verification & Validation Plan (refreshed)

### 8.1 Methods (per requirement)

Unchanged in structure; updated to reflect new requirements (FR-DAT-003, FR-SIT-001/002).

### 8.2 Test Levels

Unchanged (L0 unit → L3 acceptance).

### 8.3 V&V Matrix (replaces single AR(1) gate)

The full matrix per R01 §4. Reproduced here for the master doc to make it the formal acceptance criterion:

| Variable | Horizon | Primary benchmark | Density bar |
|---|---|---|---|
| GDP growth | 1Q | Beat RW + AR(1) on ≥80% Tier-V by CRPS | PIT KS ≥80% |
| GDP growth | 4Q | Not stat. worse than WEO/OECD EO on ≥50% Tier-V (DM p>0.05) | PIT ≥70% |
| GDP growth | 8Q | Not stat. worse than WEO on ≥40% Tier-V | PIT ≥60% |
| CPI | 1Q | Beat AR(1) and last-12m avg on ≥65% Tier-V by CRPS | PIT ≥60% |
| CPI | 4Q | Not stat. worse than WEO/OECD EO on ≥40% Tier-V | PIT ≥50% |
| Unemp. | 1Q | Beat AR(1) on ≥75% Tier-V | PIT ≥70% |
| Unemp. | 4Q | Not stat. worse than WEO on ≥50% Tier-V | PIT ≥60% |
| Policy rate | 1Q–4Q | Not stat. worse than forward curve / OIS-implied | N/A |
| Recession prob. (term spread) | 12m | AUC ≥ 0.85 vs. Bauer-Mertens replication, ≥10y OOS | Reliability diagram check |

All non-deferred cells must clear for FOC.

---

## 9. Risk Management Plan & Register (refreshed)

| Risk-ID | Description | L | I | LxI | Mitigation | Owner |
|---|---|---|---|---|---|---|
| RSK-001 | **Vintage unavailable for non-OECD-26** | **5** | **4** | **20** | Tier-V/Tier-T split; ADR-011 | Data Lead |
| RSK-002 | **BGVAR scaling intractable** | **1** | **2** | **2** | R04 resolved; mature package + VB fallback + annual cadence | Model Lead |
| RSK-003 | Tier-V V&V matrix fails at FOC | 3 | 5 | 15 | Iterate v0.4→v1.0; multiple combiner candidates | Program Owner |
| RSK-004 | Source-license violation | 2 | 5 | 10 | Per-source ToS map (R05); upstream-substitution for FRED | Data Lead |
| RSK-005 | MCP monetization fails | — | — | — | **Deferred per program-owner direction; not a Block-I risk** | n/a |
| RSK-006 | Cloud cost overrun | 1 | 2 | 2 | Cost informational; node-by-node alarms | DevOps |
| RSK-007 | Single maintainer dependency | 4 | 4 | 16 | Doc-as-code; ADR-rich design | Program Owner |
| RSK-008 | Identification critique | 3 | 2 | 6 | Multiple identifications; per-release model cards | Model Lead |
| RSK-009 | Comtrade trade-weight lag | 4 | 2 | 8 | AIS-nowcast / PortWatch trade weights | Data Lead |
| RSK-010 | Schema drift in source APIs | 3 | 3 | 9 | Schema-validation gate; pinned snapshot fallback | Data Lead |
| **RSK-011 (new)** | **FRED ToS revocation / further restriction** | 2 | 2 | 4 | Upstream-substitution already in place per ADR-010 | Data Lead |
| **RSK-012 (new)** | **Upstream-agency adapter complexity** | 3 | 3 | 9 | Per-agency adapter, integration tests, golden fixtures | Data Lead |
| **RSK-013 (new)** | **Situation endpoint adds support burden** | 2 | 2 | 4 | Both endpoints built on already-public indices; thin wrappers | Program Owner |

---

## 10. WBS & Schedule (re-sequenced)

### 10.1 WBS (revised level-3)

```
1.0 Program Management
2.0 Systems Engineering
3.0 Data Subsystem
    3.1 Upstream-agency adapters (US)
    3.2 OECD ORDRA + multi-country adapters
    3.3 Vintage store (Tier-V) + tracked store (Tier-T)
    3.4 Information-surface adapters
4.0 Model Subsystem
    4.1 L3 (workhorse) — DFM + ML + large BVAR variants
    4.2 L2 (annual) — BGVAR via R adapter
    4.3 L1 (US only) — semi-structural core
    4.4 BMA combiner over L3 variants
5.0 Application Services
    5.1 Forecast (Tier-V)
    5.2 Scenario (L1+L2 invocation)
    5.3 Backtest (V&V matrix)
    5.4 Publication
    5.5 Situation (new)
6.0 Platform
    6.1 Java API
    6.2 MCP Server
    6.3 Orchestration
    6.4 Infra/CI
7.0 V&V
    7.1 Unit
    7.2 Integration
    7.3 Vintage Replay (Tier-V)
    7.4 Acceptance (V&V matrix)
8.0 Release & Ops
```

### 10.2 Master Schedule (re-paced)

| Phase | Weeks | Deliverable | Gate |
|---|---|---|---|
| Concept rebaseline | W01 | Rev C CONOPS + v2.0 master doc signed | **SRR-2** |
| Requirements refresh | W02–W03 | StRS/SRS at v2 | SDR-2 |
| Preliminary Design | W04–W06 | SAD, SSDDs at draft B (incl. SSDD-008) | **PDR** |
| Critical Design | W07–W09 | Frozen ICDs, DBDD, V&V plan, test scaffolds | **CDR** |
| Implementation IOC | W10–W21 | Data + L3 + Forecast + Backtest for Tier-V | TRR |
| IOC Test | W22–W23 | V&V matrix per cell evaluated | **IOC** |
| Implementation v0.4 | W24–W33 | Scenario + Situation + MCP + leaderboard | TRR-2 |
| v0.4 Test | W34–W35 | Pilot self-use | **OCR** |
| Implementation v1.0 | W36–W50 | L1 US core + L2 annual + full V&V | TRR-3 |
| v1.0 V&V | W51–W54 | Full V&V matrix, model cards | **FOC** |

---

## 11. Acceptance, Gates, and Phasing (refreshed)

### 11.1 Phase Gate Criteria

| Gate | Exit Criteria |
|---|---|
| SRR-2 | Rev C CONOPS + v2.0 master doc signed; R99 amendments incorporated |
| SDR-2 | SRS at v2; ICDs at draft B |
| PDR | All SSDDs (incl. 008) at draft B; risk register re-scored |
| CDR | ICDs frozen; DBDD frozen; V&V matrix signed |
| TRR (IOC) | FR-DAT-001..003 and FR-BCT-001..002 unit + integration passing on Tier-V |
| IOC | V&V matrix: GDP-1Q cell clears on ≥80% Tier-V |
| OCR | Scenario meets NFR-PRF-002; self-use signed off; Situation endpoints live |
| FOC | All non-deferred V&V matrix cells clear; leaderboard live; model cards published |

### 11.2 Canonical Workloads

- WLD-FCST-01: GDP density forecast, single Tier-V country, horizon 4Q.
- WLD-SCEN-01: +100bp Fed funds shock, 3 Tier-V countries (US, EU agg, JP), horizon 8Q. L1+L2+L3 chain.
- WLD-BACK-01: Tier-V vintage replay 2014–2025, all horizons, V&V matrix per cell.
- **WLD-SIT-01 (new)**: term-spread recession probability per Tier-V, 12-month horizon, AUC reported.

---

## 12. Configuration Management (unchanged)

CIs, baselines, change control, releases — per v1.0.

---

## Appendix A — Glossary

(Deferred to LOOP_PLAN Iter 25.)

## Appendix B — Open TBDs

| ID | Item | Resolution by |
|---|---|---|
| TBR-006 | ACLED ToS for private-non-commercial | SRR-2 |
| TBR-007 | Final Tier-V roster | SRR-2 |
| TBR-008 | Consensus Economics access | future public-launch round |
| TBR-009 | Whether SSDD-008 owns recession-probability internally or wraps replication | CDR |

## Appendix C — Traceability Matrix excerpt

| StRS | SRS | SSDD | V&V |
|---|---|---|---|
| StRS-001 | FR-DAT-001, FR-FOR-001 | 001, 002, 005, 007 | matrix |
| StRS-003 | FR-FOR-002, FR-CFG-001, NFR-RPR-001 | 001, 007 | T |
| StRS-004 | FR-BCT-001 | 007 | T+A |
| StRS-005 | FR-BCT-002, FR-PUB-001 | 007 | T+A |
| StRS-011 | FR-DAT-003 | 001, 002, 005 | T |
| StRS-012 | FR-SIT-001, FR-SIT-002 | 008 | T (matrix new row) |
| StRS-013 | FR-DAT-001 | 001 | I |

---

**End of Master Design Document — v2.0 DRAFT.**

Next action: program-owner sign-off → SRR-2 walkthrough → restart LOOP_PLAN at iteration 02.
