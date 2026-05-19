# Program OPENGEM-1
## System Design Document Set — Block I
### Open Global Economic Macroeconometric (OPENGEM) Forecasting System

**Document Set Version:** 1.0 (Preliminary Design Review draft)
**Classification:** Open / Unclassified
**Lifecycle Model:** Waterfall (DoD-5000 / MIL-STD-498 derived)
**Prepared by:** Chief Systems Engineer (acting), Economics & Systems Branch
**Date:** 2026-05-19
**Status:** Pre-PDR

> This is the integrated master design document at v1.0. It will be progressively decomposed
> into the per-document artifacts listed in §0 as the loop expands each section. When a
> section here has been fully realized in its own file, the section body in this master
> document becomes a **stub with a forward link**.

---

## 0. Document Set Index

| # | Doc ID | Title | Section | File (when realized) |
|---|---|---|---|---|
| 1 | OG1-CONOPS-001 | Concept of Operations | §1 | `00-program/OG1-CONOPS-001.md` |
| 2 | OG1-STRS-001 | Stakeholder Requirements Spec | §2 | `00-program/OG1-STRS-001.md` |
| 3 | OG1-SRS-001 | System Requirements Spec | §3 | `00-program/OG1-SRS-001.md` |
| 4 | OG1-SAD-001 | System Architecture Document | §4 | `00-program/OG1-SAD-001.md` |
| 5 | OG1-SSDD-001…007 | Subsystem Design Documents | §5 | `10-subsystems/OG1-SSDD-00N.md` |
| 6 | OG1-ICD-001…006 | Interface Control Documents | §6 | `20-interfaces/OG1-ICD-00N.md` |
| 7 | OG1-DBDD-001 | Database Design Document | §7 | `30-data/OG1-DBDD-001.md` |
| 8 | OG1-VVP-001 | Verification & Validation Plan | §8 | `40-vv/OG1-VVP-001.md` |
| 9 | OG1-RISK-001 | Risk Management Plan & Register | §9 | `50-risk/OG1-RISK-001.md` |
| 10 | OG1-WBS-001 | Work Breakdown Structure & Schedule | §10 | `60-schedule/OG1-WBS-001.md` |
| 11 | OG1-AGP-001 | Acceptance, Gates, and Phasing | §11 | `00-program/OG1-AGP-001.md` |
| 12 | OG1-CMP-001 | Configuration Management Plan | §12 | `70-cm/OG1-CMP-001.md` |

---

## 1. CONOPS — Concept of Operations (OG1-CONOPS-001)

### 1.1 Mission Statement
Deliver an open-source, continuously verifiable, multi-country macroeconomic forecasting and scenario system at operational parity (≥70% use-case coverage) with proprietary incumbent systems (Oxford Economics GEM, NIESR NiGEM, Moody's Analytics), at a sustaining cost of <USD 200/month and with statistical performance auditable in public.

### 1.2 Operational View (OV-1, textual)

```
                        +-----------------------+
   Data Sources  ---->  |  OPENGEM Core System  |  ----> Forecast products
   (IMF, WB, FRED,      |                       |        Scenario products
   OECD, ECB, BIS,      |  - Ingestion          |        Backtest leaderboard
   Comtrade, GDELT,     |  - Estimation         |        MCP endpoints
   VIIRS, AIS, Trends)  |  - Forecast           |
                        |  - Scenario           |  ----> Users:
   Operators       --> |  - Backtest            |        - Researchers
   (recalibration,      |  - Publication        |        - Asset managers
    scenario authoring) +-----------------------+        - Policy shops
                                                         - Journalists
                                                         - Internal (oblique suite)
```

### 1.3 Operational Scenarios

| OS-ID | Scenario | Trigger | Outcome |
|---|---|---|---|
| OS-01 | Routine daily nowcast | Cron 06:00 UTC | Updated GDP/CPI nowcasts for IOC countries |
| OS-02 | Monthly re-estimation | First Mon of month | Posterior weights updated, leaderboard refreshed |
| OS-03 | Quarterly full run | National-accounts release | Full L1+L2+L3 forecast publication |
| OS-04 | Ad-hoc scenario | Analyst POST /scenario | Fan chart + impulse responses returned <60s |
| OS-05 | Vintage replay | CI on PR | Backtest reruns over last 10y of vintages |
| OS-06 | Stress event | Market vol > threshold | Auto-trigger sensitivity sweep, alert subscribers |

### 1.4 Stakeholders

| ID | Stakeholder | Concerns |
|---|---|---|
| SH-01 | Forecast consumers (subscribers) | Accuracy, freshness, density forecasts |
| SH-02 | Open-source community | Reproducibility, license clarity, code quality |
| SH-03 | Academic auditors | Vintage discipline, methodological transparency |
| SH-04 | Program owner | Cloud-bill viability, MCP monetization fit |
| SH-05 | Adjacent oblique systems | API stability for oracle/anvil/plan integration |
| SH-06 | Regulators (future) | Auditable provenance, model cards |

### 1.5 Out-of-Scope (Block I)
- Sectoral / industry forecasts (deferred to Block II).
- Climate-economy coupling à la GCAM (deferred to Block III).
- Real-time financial market models (FX/equity high-freq) — only quarterly/monthly macro covered.
- Causal counterfactual analysis beyond shock impulse responses.

---

## 2. Stakeholder Requirements Specification (OG1-STRS-001)

| StRS-ID | Requirement | Source |
|---|---|---|
| StRS-001 | The system shall produce GDP, CPI, policy rate, and unemployment forecasts for ≥40 economies at IOC and ≥80 at FOC. | SH-01 |
| StRS-002 | Forecasts shall be published with density (P10/P50/P90), not only point estimates. | SH-01, SH-03 |
| StRS-003 | All forecasts shall be reproducible from a `(code_sha, data_vintage, prior_hash)` triplet. | SH-02, SH-03 |
| StRS-004 | Backtests shall use vintage (real-time) data only. | SH-03 |
| StRS-005 | The public leaderboard shall compare to ≥3 named benchmarks (consensus, WEO, AR(1)). | SH-03, SH-01 |
| StRS-006 | The operating cost of the production environment shall not exceed USD 200/month. | SH-04 |
| StRS-007 | The system shall expose an MCP-compatible interface for monetization. | SH-04, SH-05 |
| StRS-008 | All code, data schemas, model priors, and trained posteriors shall be open-licensed (Apache-2.0 / CC-BY-4.0). | SH-02 |
| StRS-009 | Ad-hoc scenario response shall return within 60 seconds for ≤3-country, ≤8-quarter shocks. | SH-01 |
| StRS-010 | The system shall preserve every published forecast indefinitely for accountability audit. | SH-03, SH-06 |

---

## 3. System Requirements Specification (OG1-SRS-001)

### 3.1 Functional Requirements (FR)

| Req-ID | Statement | Traces |
|---|---|---|
| FR-DAT-001 | The Data Subsystem shall ingest macro time series from ≥7 named sources (IMF IFS, WB WDI, OECD MEI, FRED, ECB SDW, BIS, UN Comtrade). | StRS-001, 003 |
| FR-DAT-002 | Every ingestion shall write a new vintage row; revisions shall not overwrite prior values. | StRS-003, 004 |
| FR-DAT-003 | The Data Subsystem shall ingest ≥5 alternative data streams (GDELT, VIIRS night lights, AIS shipping, Google Trends, electricity load). | StRS-001 |
| FR-MOD-001 | The Model Subsystem shall implement three estimation layers: L1 (semi-structural country core), L2 (Bayesian Global VAR), L3 (Dynamic Factor Model + ML residual). | StRS-002 |
| FR-MOD-002 | L2 shall accept bilateral trade weights derived from Comtrade with annual refresh. | StRS-001 |
| FR-MOD-003 | The Combiner shall produce a single density forecast via Bayesian Model Averaging weighted by rolling-window predictive log score. | StRS-002 |
| FR-FOR-001 | The Forecast Service shall publish forecasts at horizons {1Q, 4Q, 8Q, 20Q}. | StRS-001 |
| FR-FOR-002 | Each published forecast record shall carry `(code_sha, vintage_hash, prior_hash, posterior_hash, run_id)`. | StRS-003, 010 |
| FR-SCN-001 | The Scenario Subsystem shall accept shocks as structured JSON specifying variable, country, magnitude, horizon, start period. | StRS-009 |
| FR-SCN-002 | The Scenario Subsystem shall return impulse-response paths and counterfactual density forecasts within 60s for the canonical shock workload. | StRS-009 |
| FR-BCT-001 | The Backtest Subsystem shall run rolling-origin out-of-sample evaluation on stored vintages with windows {1Q, 4Q, 8Q, 20Q}. | StRS-004 |
| FR-BCT-002 | The Backtest Subsystem shall compute RMSE, MAE, CRPS, log score, Diebold-Mariano p-values, and Model Confidence Set membership against benchmarks {consensus, WEO, AR(1), RW, SPF where available}. | StRS-005 |
| FR-PUB-001 | The Publication Subsystem shall serve a public leaderboard table refreshed at least weekly. | StRS-005 |
| FR-PUB-002 | The Publication Subsystem shall expose REST and MCP endpoints. | StRS-007 |
| FR-CFG-001 | Every artifact (data, code, prior, posterior) shall be addressable by content hash. | StRS-003 |

### 3.2 Non-Functional Requirements (NFR)

| Req-ID | Statement | Method |
|---|---|---|
| NFR-PRF-001 | p95 latency of `/forecast` GET ≤ 500 ms. | Test |
| NFR-PRF-002 | p95 latency of `/scenario` POST ≤ 60 s (canonical workload). | Test |
| NFR-PRF-003 | Full system quarterly run ≤ 4 h on baseline hardware (4 vCPU, 16 GB RAM, 1× A10G ephemeral). | Test |
| NFR-AVL-001 | Read API availability ≥ 99.0% monthly (no SLA on model retraining). | Inspect |
| NFR-COS-001 | Production cloud cost ≤ USD 200/month sustaining. | Analysis |
| NFR-SEC-001 | No PII; all data sources are public; secrets managed via vault. | Inspect |
| NFR-MNT-001 | Bus factor ≥ 2; every CI must be documented in `OG1-CMP-001`. | Inspect |
| NFR-RPR-001 | Bit-identical reproduction of any published forecast from its hash triplet on baseline image. | Test |

### 3.3 Interface Requirements (IFR)

| Req-ID | Interface | Spec |
|---|---|---|
| IFR-EXT-001 | Inbound data | HTTPS pull per source; documented in ICD-001. |
| IFR-EXT-002 | Outbound REST API | OpenAPI 3.1; documented in ICD-002. |
| IFR-EXT-003 | Outbound MCP server | MCP 1.0 spec; documented in ICD-003. |
| IFR-INT-001 | Java API ↔ Python model service | gRPC over Unix domain socket (same host); ICD-004. |
| IFR-INT-002 | Model service ↔ PostgreSQL | JDBC / psycopg3; ICD-005. |
| IFR-INT-003 | Orchestrator ↔ Subsystems | Dagster job graph; ICD-006. |

---

## 4. System Architecture Document (OG1-SAD-001)

### 4.1 Logical View

```
+---------------------------------------------------------------+
| L7  Publication      | Leaderboard, Dashboard, MCP Server     |
+---------------------------------------------------------------+
| L6  API              | Spring Boot Read API (Java 21)         |
+---------------------------------------------------------------+
| L5  Orchestration    | Dagster jobs (Python)                  |
+---------------------------------------------------------------+
| L4  Application      | Forecast Svc | Scenario Svc | Backtest |
|                      | (FastAPI)    | (FastAPI)    | Svc      |
+---------------------------------------------------------------+
| L3  Model            | L1 Core (Stan/NumPyro) | L2 GVAR       |
|                      | L3 DFM/ML (Nixtla)     | Combiner BMA  |
+---------------------------------------------------------------+
| L2  Data             | PostgreSQL + TimescaleDB | Object Store |
+---------------------------------------------------------------+
| L1  Ingestion        | Source adapters, validators, archivers |
+---------------------------------------------------------------+
```

### 4.2 Physical View (Block I, IOC)

| Node | Spec | Role |
|---|---|---|
| `og-app-01` | 4 vCPU / 16 GB / 200 GB SSD, Hetzner CCX23 | Spring API, FastAPI, Dagster |
| `og-db-01`  | 4 vCPU / 16 GB / 500 GB SSD, Hetzner CCX23 | Postgres + TimescaleDB + MinIO |
| `og-gpu-01` | Ephemeral Modal/RunPod A10G | Bayesian re-estimation only |
| Vercel       | Free tier | Public dashboard |
| GitHub       | Free public | Code, releases, Pages mirror |

### 4.3 Deployment View
- Containers: Docker, orchestrated by Docker Compose at IOC; migration to k3s deferred to Block II.
- CI/CD: GitHub Actions; image registry GHCR; immutable tags per release.
- Secrets: SOPS + age, committed encrypted.

### 4.4 Architectural Decision Records (ADRs) — initial set

| ADR | Decision | Rationale |
|---|---|---|
| ADR-001 | Java Spring Boot for read API | Org standard; Lombok/DI culture; stability |
| ADR-002 | Python for model service | Stan, NumPyro, Nixtla, BGVAR ecosystem |
| ADR-003 | PostgreSQL + TimescaleDB over InfluxDB | Org standard; hypertables sufficient |
| ADR-004 | Reject Neo4j for Block I | Trade graph too small to justify; revisit Block II for sector graph |
| ADR-005 | Three-layer hybrid model | No single school of macro dominates accuracy AND interpretation |
| ADR-006 | Vintage-first data layer | Without it, backtests are unfalsifiable |
| ADR-007 | Bayesian Model Averaging combiner | Transparent, monotone in evidence, no black-box gating |
| ADR-008 | Single MCP server, dual-mode REST + MCP | Single source of truth; MCP is the monetization path |

---

## 5. Subsystem Design Documents (OG1-SSDD-001…007)

### 5.1 SSDD-001 — Data Ingestion Subsystem
- **Purpose:** acquire and archive raw time series and bilateral matrices.
- **Inputs:** scheduled HTTP/HTTPS pulls; manual triggers.
- **Outputs:** rows in `raw_observations`, `vintage_snapshots`, `trade_matrices`.
- **Components:** Source Adapter (one per source), Schema Validator, Vintage Hasher, Archiver, Alerter.
- **State:** last successful pull timestamp per source; revision diff log.
- **Failure modes:** source schema drift (detected by validator), partial fetch (auto-retry with exponential backoff), upstream outage (raise to operator after N=3 failures).

### 5.2 SSDD-002 — Data Curation & Feature Subsystem
- **Purpose:** derive analysis-ready panels from raw observations.
- **Components:** Frequency Harmonizer, Seasonal Adjuster (X-13), Outlier Detector (TRAMO), Trade-Weight Builder, Alt-Data Aligner.
- **Outputs:** `analytic_panels` (mixed frequency), `weight_matrices`.

### 5.3 SSDD-003 — Model Subsystem L1 (Country Cores)
- **Purpose:** per-country semi-structural Bayesian core (10–15 equations: IS, Phillips, Taylor, UIP, fiscal closure).
- **Estimator:** NUTS in NumPyro; priors derived from FPAS-Mark-II tradition.
- **Outputs:** posterior samples, conditional forecasts.

### 5.4 SSDD-004 — Model Subsystem L2 (Bayesian GVAR)
- **Purpose:** cross-country spillover engine over country aggregates.
- **Inputs:** country posteriors from L1 (as informative priors), trade-weight matrices.
- **Estimator:** Bayesian GVAR (hierarchical priors on cross-country coefficients); reference implementation `BGVAR`.
- **Outputs:** global posterior, joint impulse-response functions.

### 5.5 SSDD-005 — Model Subsystem L3 (Nowcast + ML Residual)
- **Purpose:** high-frequency state estimation and ML residual correction.
- **Components:** Mixed-Frequency Dynamic Factor Model (state-space, Kalman filter); LightGBM residual model on factor scores + alt-data features.
- **Outputs:** daily-updated current-quarter point and density estimates.

### 5.6 SSDD-006 — Scenario Subsystem
- **Purpose:** apply structured shocks; produce counterfactual densities.
- **Components:** Shock Parser, Identification Selector (Cholesky / sign / narrative), Propagator (calls L1 then L2 then L3), Fan-Chart Builder, Cache.
- **State:** scenario cache keyed by (shock, posterior_hash).

### 5.7 SSDD-007 — Backtest & Publication Subsystem
- **Purpose:** continuous evaluation; leaderboard generation; public artifact publication.
- **Components:** Vintage Replayer, Benchmark Fetcher (WEO, consensus), Metric Engine (RMSE/MAE/CRPS/LS/DM/MCS), Leaderboard Materializer, Forecast Archiver.

---

## 6. Interface Control Documents (OG1-ICD-001…006)

### 6.1 ICD-001 — External Data Source Interfaces
For each source: protocol, auth, schema, refresh frequency, rate-limit policy, fallback. Tabulated; populated at CDR. **TBD** for VIIRS access tier choice.

### 6.2 ICD-002 — Public REST API
- `GET /v1/forecast?country=&horizon=&run_id=`
- `GET /v1/density?country=&horizon=&run_id=`
- `POST /v1/scenario` (body: shock spec; returns run_id + fan chart URL)
- `GET /v1/backtest/leaderboard?as_of=&metric=&horizon=`
- `GET /v1/runs/{run_id}` (provenance)
- OpenAPI 3.1 contract authoritative.

### 6.3 ICD-003 — MCP Server Contract
Tools: `forecast`, `scenario`, `compare_to_consensus`, `backtest_query`. Resources: `country_card`, `model_card`, `leaderboard_snapshot`.

### 6.4 ICD-004 — Java ↔ Python (gRPC)
Proto `opengem.v1.ModelService` with `Forecast`, `RunScenario`, `Backtest` RPCs. Streaming for long-running scenario draws.

### 6.5 ICD-005 — Model Service ↔ PostgreSQL
Schema-scoped roles: `ingest_rw`, `model_ro`, `model_rw_posteriors`, `api_ro`. Strict per-service privilege boundary.

### 6.6 ICD-006 — Orchestrator ↔ Subsystems
Dagster asset graph; assets are typed; partitions: country × vintage × frequency.

---

## 7. Database Design Document (OG1-DBDD-001)

### 7.1 Conceptual Entities

```
Source ─< Series ─< Observation (vintage-keyed)
Country ─< CountryPanel ─< Forecast (run_id-keyed)
Run ── posterior_hash ── prior_hash ── code_sha ── vintage_hash
Scenario ─< Shock; Scenario ─< Run
Benchmark ─< BenchmarkForecast
LeaderboardEntry (run_id, country, horizon, metric, benchmark, value)
```

### 7.2 Physical Tables (selected)

| Table | Type | Key columns | Notes |
|---|---|---|---|
| `raw_observation` | Timescale hypertable | (series_id, observed_at, vintage_at) | Append-only |
| `series_meta` | Relational | series_id | Unit, frequency, source |
| `trade_matrix` | Relational | (year, country_i, country_j) | Symmetric or directional |
| `prior_set` | Relational | prior_hash | JSON blob of priors |
| `posterior` | Object store ref | posterior_hash | Parquet on MinIO |
| `forecast_run` | Relational | run_id | Provenance triplet + run metadata |
| `forecast_point` | Hypertable | (run_id, country, horizon_q, variable) | Quantiles in cols |
| `scenario` | Relational | scenario_id | JSON shock spec |
| `leaderboard` | Materialized view | weekly refresh | Public-readable role |

### 7.3 Retention Policy
- Raw observations: forever.
- Posteriors: forever for tagged releases; 90 days for ephemeral CI runs.
- Forecast points: forever (StRS-010).

---

## 8. Verification & Validation Plan (OG1-VVP-001)

### 8.1 Verification Methods (per requirement)
Each Req-ID assigned one of: **T** (Test), **D** (Demonstration), **I** (Inspection), **A** (Analysis).

| Req-ID | Method | Activity |
|---|---|---|
| FR-DAT-001 | I+T | Adapter unit tests; integration with golden fixtures |
| FR-DAT-002 | T | Property test: revision never overwrites |
| FR-MOD-001..003 | T+A | Posterior recovery on synthetic data; cross-method ablation |
| FR-FOR-002 | T | Hash-triplet roundtrip test |
| FR-SCN-001..002 | T | Latency tests on canonical workload |
| FR-BCT-001..002 | T+A | Vintage replay over 2014–2025; statistical tests |
| NFR-PRF-* | T | Load test (k6) |
| NFR-COS-001 | A | Monthly cost report from cloud bill |
| NFR-RPR-001 | T | Replay-and-diff CI job |

### 8.2 Test Levels
- L0 unit (per module)
- L1 integration (subsystem boundaries)
- L2 system (end-to-end vintage replay)
- L3 acceptance (gates in §11)

### 8.3 Validation (does it forecast?)
- **Primary V&V metric for v1.0:** OPENGEM beats AR(1) on 4Q-ahead GDP RMSE in ≥75% of covered countries AND is not statistically worse than consensus (Diebold-Mariano p>0.05) in ≥50%.
- **Secondary V&V:** density forecasts pass PIT uniformity tests at the 5% level for ≥60% of country-horizon pairs.

---

## 9. Risk Management Plan & Register (OG1-RISK-001)

| Risk-ID | Description | L | I | LxI | Mitigation | Owner |
|---|---|---|---|---|---|---|
| RSK-001 | Vintage data unavailable for many emerging markets | 4 | 4 | 16 | Self-archive from day 1; mark countries as "post-2026 vintage only" | Data Lead |
| RSK-002 | Bayesian GVAR scaling intractable at 80 countries | 3 | 4 | 12 | Hierarchical priors + VB for global; MCMC only for L1 | Model Lead |
| RSK-003 | Underperformance vs. consensus at v1.0 gate | 3 | 5 | 15 | Iterate IOC→v1.0 via use-case loops; multiple combiner candidates | Program Owner |
| RSK-004 | Source-license violation in alt-data | 2 | 5 | 10 | Legal review per source; default to public-domain only at IOC | Data Lead |
| RSK-005 | MCP monetization fails | 3 | 3 | 9 | Decouple from open-source core; product is the leaderboard credibility | Program Owner |
| RSK-006 | Cloud cost overrun | 2 | 3 | 6 | Cost alarms; ephemeral GPU only; static dashboard | DevOps |
| RSK-007 | Single maintainer dependency | 4 | 4 | 16 | Doc-as-code; subsystem ADRs; recorded design rationale | Program Owner |
| RSK-008 | Identification critique from academia | 3 | 2 | 6 | Publish multiple identifications; model card per release | Model Lead |
| RSK-009 | Comtrade trade-weight lag (1–2y) | 4 | 2 | 8 | AIS-nowcast trade weights | Data Lead |
| RSK-010 | Schema drift in IMF/WB APIs | 3 | 3 | 9 | Schema-validation gate; pinned snapshot fallback | Data Lead |

---

## 10. Work Breakdown Structure & Schedule (OG1-WBS-001)

### 10.1 WBS (level 3)

```
1.0  Program Management
     1.1 Planning  1.2 Reviews  1.3 Risk  1.4 Comms
2.0  Systems Engineering
     2.1 Requirements  2.2 Architecture  2.3 ICDs  2.4 V&V Plan
3.0  Data Subsystem
     3.1 Ingestion  3.2 Vintage Store  3.3 Curation  3.4 Alt-Data
4.0  Model Subsystem
     4.1 L1 Country Cores  4.2 L2 GVAR  4.3 L3 DFM/ML  4.4 Combiner
5.0  Application Services
     5.1 Forecast  5.2 Scenario  5.3 Backtest  5.4 Publication
6.0  Platform
     6.1 Java API  6.2 MCP Server  6.3 Orchestration  6.4 Infra/CI
7.0  V&V
     7.1 Unit  7.2 Integration  7.3 Vintage Replay  7.4 Acceptance
8.0  Release & Ops
     8.1 Documentation  8.2 Model Cards  8.3 Dashboard  8.4 Run-Ops
```

### 10.2 Master Schedule

| Phase | Weeks | Deliverable | Gate |
|---|---|---|---|
| Concept | W01–W02 | CONOPS, StRS approved | SRR |
| Requirements | W03–W04 | SRS, ICDs draft | SDR |
| Preliminary Design | W05–W07 | SAD, SSDDs draft | **PDR** |
| Critical Design | W08–W10 | All ICDs, DBDD, V&V plan, test harness scaffolds | **CDR** |
| Implementation Block IOC | W11–W22 | Data + L2 + Forecast + Backtest for G7+China | TRR |
| IOC Test | W23–W24 | Vintage replay, gate evaluation | **IOC** |
| Implementation v0.4 | W25–W34 | Scenario + MCP + leaderboard | TRR-2 |
| v0.4 Test | W35–W36 | External user pilots | **OCR** |
| Implementation v1.0 | W37–W52 | L1 cores + scale to 80 countries | TRR-3 |
| v1.0 V&V | W53–W56 | Full V&V, model cards | **FOC** |

---

## 11. Acceptance, Gates, and Phasing (OG1-AGP-001)

### 11.1 Phase Gate Criteria (exit criteria)

| Gate | Exit Criteria |
|---|---|
| SRR | StRS signed; CONOPS signed; risk register baseline |
| SDR | SRS signed; SAD agreed; ICDs at draft B |
| PDR | All SSDDs at draft B; risk LxI re-scored; no unresolved show-stopper design conflicts |
| CDR | ICDs frozen; DBDD frozen; V&V plan signed; test scaffolds compile |
| TRR (IOC) | All FR-DAT-* and FR-BCT-* unit and integration tests pass on G7+China |
| IOC | Vintage replay beats AR(1) RMSE on 4Q-ahead GDP for ≥5/8 countries |
| OCR | Scenario service meets NFR-PRF-002; 3 external pilot users sign off |
| FOC | v1.0 V&V criteria of §8.3 met; leaderboard live; model cards published |

### 11.2 Canonical Workloads
- **WLD-FCST-01:** GDP density forecast, single country, horizon 4Q.
- **WLD-SCEN-01:** +100bp Fed funds shock, 3 countries (US, EU, JP), horizon 8Q.
- **WLD-BACK-01:** Full vintage replay 2014–2025, G7+China, all horizons.

### 11.3 Decision Authority
- ADR changes after CDR require Program Owner + Model Lead concurrence.
- Schedule slips >2 weeks at any gate trigger formal re-plan.

---

## 12. Configuration Management Plan (OG1-CMP-001)

- **Configuration Items (CIs):** code (Git SHA), data (vintage hash), priors (hash), posteriors (hash), trained ML models (hash), Docker images (digest), schemas (migration version).
- **Baselines:** Functional (post-SRR), Allocated (post-PDR), Product (post-CDR), Operational (per release).
- **Change control:** Engineering Change Proposals (ECPs) tracked as GitHub issues with `ecp/` prefix; required for any post-CDR ICD or SRS change.
- **Releases:** semver; release notes include all four hash classes for every published forecast cohort.

---

## Appendix A — Glossary
*(deferred; will populate at PDR)*

## Appendix B — Open TBD/TBR Items

| ID | Item | Resolution by |
|---|---|---|
| TBD-001 | VIIRS access tier (NASA EarthData free vs. paid) | CDR |
| TBD-002 | Choice between LightGBM vs. XGBoost vs. CatBoost for L3 residual | PDR |
| TBR-001 | Country list at IOC (currently G7+China; add Australia for personal use?) | SRR |
| TBD-003 | License for downstream commercial wrappers around MCP server | OCR |
| TBD-004 | Whether L1 cores use Stan or NumPyro (perf + maintainability trade) | CDR |

## Appendix C — Traceability Matrix (excerpt)

| StRS | SRS | SSDD | V&V |
|---|---|---|---|
| StRS-001 | FR-DAT-001, FR-FOR-001 | SSDD-001, 002, 007 | T (8.1) |
| StRS-003 | FR-FOR-002, FR-CFG-001, NFR-RPR-001 | SSDD-001, 007 | T (8.1) |
| StRS-004 | FR-BCT-001 | SSDD-007 | T+A (8.1, 8.3) |
| StRS-005 | FR-BCT-002, FR-PUB-001 | SSDD-007 | T+A (8.3) |
| StRS-006 | NFR-COS-001 | All | A (8.1) |
| StRS-007 | FR-PUB-002, IFR-EXT-003 | SSDD-007, ICD-003 | D (8.1) |
| StRS-009 | FR-SCN-002, NFR-PRF-002 | SSDD-006 | T (8.1) |
| StRS-010 | FR-FOR-002 | SSDD-007 | I (8.1) |

---

**End of Master Design Document — Block I, v1.0 (PDR draft).**

Next action: SRR walkthrough; loop to decompose each section into its own document with full detail.
