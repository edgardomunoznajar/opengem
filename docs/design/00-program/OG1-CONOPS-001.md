# OG1-CONOPS-001 — Concept of Operations
## Open Global Economic Macroeconometric (OPENGEM) Forecasting System

| Field | Value |
|---|---|
| Document ID | OG1-CONOPS-001 |
| Revision | B (draft) |
| Date | 2026-05-19 |
| Lifecycle Phase | Concept |
| Supersedes | §1 of `00-master-design-document-v1.0.md` |
| Format Reference | IEEE Std 1362-1998 (System Definition — CONOPS) |

---

## 1. Scope

### 1.1 Identification
This document defines the Concept of Operations for **Program OPENGEM-1**, Block I, the open-source Open Global Economic Macroeconometric Forecasting System (henceforth **OPENGEM** or "the system").

### 1.2 System Overview
OPENGEM is a multi-country, mixed-frequency, density-producing macroeconomic forecasting and scenario system. It composes three estimation layers (semi-structural country cores, Bayesian Global VAR, and Dynamic Factor Model with ML residual correction) into a single Bayesian-Model-Averaged forecast distribution per country-variable-horizon cell. Outputs are published via REST and MCP interfaces, archived for accountability audit, and continuously benchmarked against named external forecasts on a public leaderboard.

### 1.3 Document Overview
This CONOPS establishes the *why*, *for whom*, *under what conditions*, and *to what end* of OPENGEM Block I. It precedes and constrains all downstream artifacts (StRS, SRS, SAD, SSDDs, ICDs). Approval of this document at SRR baselines the **Functional Configuration** of the program.

---

## 2. Referenced Documents

| Ref | Title |
|---|---|
| R-01 | Pesaran, Schuermann, Weiner (2004). *Modeling Regional Interdependencies Using a Global Error-Correcting Macroeconometric Model.* |
| R-02 | Banbura, Giannone, Reichlin (2010). *Nowcasting.* ECB WP. |
| R-03 | IMF (2018). *FPAS Mark II — Quarterly Projection Model documentation.* |
| R-04 | NIESR. *NiGEM model reference manual.* (paywall — used only conceptually) |
| R-05 | Diebold & Mariano (1995). *Comparing predictive accuracy.* |
| R-06 | Hansen, Lunde, Nason (2011). *Model Confidence Set.* |
| R-07 | Philadelphia Fed. *Real-Time Data Set for Macroeconomists.* |
| R-08 | Makridakis et al. *M5/M6 competition reports.* |
| R-09 | IEEE Std 1362-1998. *Guide for Information Technology — System Definition — Concept of Operations Document.* |
| R-10 | MIL-STD-498 (1994). *Software Development and Documentation.* |

---

## 3. Current Situation

### 3.1 Incumbent Systems
The world economy is currently forecast operationally by a small cartel of proprietary models:

| System | Operator | Coverage | License Cost | Open Source |
|---|---|---|---|---|
| Global Economic Model (GEM) | Oxford Economics | ~80 countries, ~200 light | USD 50–250k/yr | No |
| NiGEM | NIESR | ~80 countries | USD ~80–150k/yr | No (licensable) |
| Moody's Analytics Global | Moody's | ~80 countries | USD 100k+/yr | No |
| FRB/US | Federal Reserve | US only | Free | Code public, US-only |
| IMF GIMF | IMF | ~6 regions | Free | DSGE, narrow scope |
| EAGLE | ECB | 4 regions | Free (Dynare) | Narrow scope |
| GVAR Toolbox | Pesaran et al. | ~33 countries | Free (Matlab) | Yes, reduced-form |
| BGVAR (R) | M. Böck | configurable | Free (CRAN) | Yes |

### 3.2 Diagnosed Gap
- No system combines (a) **open license**, (b) **multi-country breadth**, (c) **structural + reduced-form + ML hybrid**, (d) **vintage-correct continuous backtests**, and (e) **public leaderboard against named benchmarks**.
- Even where open models exist (GVAR, BGVAR, EAGLE, FRB/US), they ship as research artifacts. They are not *operated* — there is no daily pipeline, no leaderboard, no MCP/REST surface, no model cards, and rarely real-time vintage discipline.
- The verifiability gap is the central pathology: forecasts are routinely published without subsequent public scoring, so consumers cannot tell which models earn their cost.

### 3.3 Stakeholder Pain (current)
| Pain Point | Affected Stakeholder | Cost |
|---|---|---|
| Cannot afford GEM/NiGEM for small shops | Independent analysts, journalists, small funds | Forced to use point estimates from headlines |
| Cannot independently audit consensus accuracy | Academics, regulators | Reliance on self-reporting |
| Cannot run custom scenarios outside subscription | Same | Either pay or improvise |
| Cannot integrate into agentic tooling | Internal oblique suite | No MCP surface from any incumbent |

---

## 4. Justification for the System

### 4.1 Necessity
The intersection of cheap cloud compute, public macro datasets, mature Bayesian inference libraries, and the MCP standard makes a guerrilla-developer-scale clone of GEM technically feasible for the first time. Without OPENGEM, the open-source community lacks a credible answer to "what does the world economy look like in 2027 under shock X, and how do I know your answer is right?"

### 4.2 Strategic Fit (within the oblique suite)
- **oblique-oracle** already provides Monte Carlo simulation primitives; OPENGEM consumes those for parameter-uncertainty propagation.
- **oblique-anvil** generates stress scenarios; OPENGEM consumes shock specifications.
- **oblique-plan** turns OPENGEM scenario outputs into decision trees.
- **oblique-lawyer**'s MCP monetization template at v0.5 is the playbook for OPENGEM's commercial surface.

### 4.3 Commercial Rationale
While the core is Apache-2.0, the **MCP server** is the monetization vector: pay tiers gate scenario authoring, custom benchmarks, and bulk historical forecast exports. Open-core / commercial-API split is the dominant viable model for this class of artifact.

---

## 5. Concepts for the Proposed System

### 5.1 Background, Objectives, and Scope

#### 5.1.1 Objectives (ranked)
1. **Verifiability.** Every forecast carries a provenance hash; every forecast is publicly scored on a leaderboard within 4Q of issue.
2. **Coverage.** ≥40 economies at IOC, ≥80 at FOC, all with density forecasts.
3. **Interpretability + Accuracy.** Both, not either — that's the rationale for the 3-layer hybrid.
4. **Cost discipline.** Sustaining operation ≤ USD 200/mo.
5. **Integration.** First-class MCP citizen of the oblique suite.

#### 5.1.2 Scope (Block I)
*In scope:* macro variables (GDP, CPI, policy rate, unemployment, FX), quarterly modeling, monthly nowcasting, scenario impulse responses, public leaderboard.
*Out of scope:* sectoral/industry detail (Block II), climate/energy coupling (Block III), HF financial markets, causal counterfactuals beyond shock IRFs.

### 5.2 Operational Policies and Constraints

| Policy-ID | Statement |
|---|---|
| POL-01 | All data sources used in OPENGEM shall be either public-domain or licensed for free redistribution. Sources requiring per-user authentication shall be wrapped to expose only derivative aggregates. |
| POL-02 | Every published forecast shall be reproducible from `(code_sha, vintage_hash, prior_hash, posterior_hash)`. |
| POL-03 | Backtests shall use real-time (vintage) data. Backtests using revised data are categorically prohibited from the leaderboard. |
| POL-04 | Forecasts shall never be silently retracted. Corrections produce a *new* run; the prior run remains archived with a `superseded_by` pointer. |
| POL-05 | Model cards shall accompany every release; every model card lists known biases, training period, and last-validated date. |
| POL-06 | GPU usage shall be ephemeral and bursty; no GPU shall remain provisioned outside re-estimation windows. |
| POL-07 | No PII shall enter the system at any layer. |
| POL-08 | All schemas and ICDs are open; private extensions are forbidden. |
| POL-09 | The leaderboard ranking algorithm shall itself be open and version-pinned per leaderboard epoch. |
| POL-10 | "Beat consensus" claims require Diebold-Mariano p<0.05 evidence over ≥8 quarters of vintage-correct out-of-sample data. Lesser claims must be hedged. |

### 5.3 Description of the Proposed System

#### 5.3.1 System-Level Block Diagram (textual)

```
   ┌────────────────────── External Data Sources ──────────────────────┐
   │ IMF IFS · WB WDI · OECD MEI · FRED · ECB SDW · BIS · UN Comtrade │
   │ + GDELT · VIIRS · AIS · Google Trends · electricity grids       │
   └───────────────────────────────┬───────────────────────────────────┘
                                   │ HTTPS pulls (POL-01)
                                   ▼
   ┌─────────────────── Ingestion + Vintage Store ─────────────────────┐
   │  Source adapters → Validators → Vintage Hasher → PostgreSQL/TS   │
   └───────────────────────────────┬───────────────────────────────────┘
                                   ▼
   ┌──────────────────── Curation + Feature Layer ─────────────────────┐
   │  Frequency harmonization · Seasonal adj · Trade-weight builder   │
   └─────────┬────────────────┬────────────────────────┬───────────────┘
             ▼                ▼                        ▼
   ┌──────── L1 ────────┐  ┌── L2 ──┐         ┌─────── L3 ─────────┐
   │ Country cores     │  │ GVAR  │         │ DFM + ML residual  │
   │ (semi-structural) │  │ (BGVAR)│         │ (Kalman + LightGBM)│
   └─────────┬─────────┘  └───┬────┘         └─────────┬──────────┘
             └────────┬───────┴────────────┬───────────┘
                      ▼                    ▼
              ┌────── Combiner (BMA) ──────┐
              └────────────┬───────────────┘
                           ▼
   ┌──────── Forecast · Scenario · Backtest Services ──────────────────┐
   └────────────────────────┬─────────────────────────────────────────┘
                            ▼
   ┌──── REST API (Spring Boot) · MCP Server · Public Dashboard ──────┐
   └──────────────────────────────────────────────────────────────────┘
```

#### 5.3.2 Capabilities Delivered

| Cap-ID | Capability | Block I Status |
|---|---|---|
| CAP-01 | Density GDP forecast, 1Q/4Q/8Q/20Q horizons | IOC |
| CAP-02 | Density CPI forecast, same horizons | IOC |
| CAP-03 | Policy-rate path | IOC |
| CAP-04 | Unemployment forecast | v0.4 |
| CAP-05 | FX nominal/real | v0.4 |
| CAP-06 | Daily current-quarter nowcast | v0.4 |
| CAP-07 | Ad-hoc scenario IRFs | v0.4 |
| CAP-08 | Public leaderboard | v0.4 |
| CAP-09 | Model cards | v1.0 |
| CAP-10 | Bulk historical forecast export | v1.0 |
| CAP-11 | MCP-driven scenario authoring | v0.4 |

### 5.4 Modes of Operation

| Mode-ID | Mode | Description | Trigger |
|---|---|---|---|
| M-01 | Quiescent Read | Serve cached forecasts; no model run | Default |
| M-02 | Daily Nowcast | Refresh L3 state on yesterday's data | 06:00 UTC cron |
| M-03 | Monthly Recalibration | Re-estimate L3 weights + Combiner weights | First Mon 02:00 UTC |
| M-04 | Quarterly Full Run | Re-estimate L1 + L2; emit new forecast cohort | National accounts release detected |
| M-05 | Scenario Run | Apply shock; compute counterfactual; cache | API POST `/scenario` |
| M-06 | Vintage Replay | Backtest over historical vintages | CI on PR or cron weekly |
| M-07 | Maintenance | Read-only frozen; reindex DB; rebuild caches | Operator-initiated |
| M-08 | Degraded | One subsystem failed; serve last-good with warnings | Auto |

Mode transitions:
- M-01 → M-02/03/04: scheduler.
- Any → M-08: subsystem health check fail.
- M-08 → M-01: operator clears alert.
- Any → M-07: operator scheduled window.

### 5.5 User Classes and Other Involved Personnel

| User-ID | Class | Persona Sketch | Primary Mode | Auth |
|---|---|---|---|---|
| U-01 | Anonymous reader | Journalist checking next-quarter GDP for an article | M-01 read-only | None |
| U-02 | Registered analyst | Macro consultant authoring scenarios | M-05 | API key (free tier) |
| U-03 | Paying subscriber | Asset manager pulling bulk densities | M-05 + M-01 | API key (paid) |
| U-04 | Internal agent | oblique-anvil pushing stress shocks | M-05 | mTLS |
| U-05 | Academic auditor | Verifying leaderboard claim | M-06 (replay) | None |
| U-06 | Program operator | Triggers M-07, responds to M-08 | Admin | SSH + 2FA |
| U-07 | Contributor | Adds new country adapter | Dev environment only | GitHub |
| U-08 | Model card reviewer | External SME validating release | M-01 + repo access | GitHub |

### 5.6 Support Environment
- **Hosting:** Hetzner CCX23 (×2 VMs); GitHub for code; Vercel for dashboard; Modal/RunPod for ephemeral GPU.
- **Monitoring:** Grafana + Loki + Prometheus on `og-app-01`; budget alarms via cloud provider.
- **Documentation:** Markdown in-repo; auto-rendered to GitHub Pages; OpenAPI/MCP descriptors auto-published.
- **Community:** GitHub Discussions + Discord; SLA-free, public-only.

---

## 6. Operational Scenarios (expanded)

### 6.1 OS-01 — Routine Daily Nowcast (happy path)
- **Pre-conditions:** all data adapters healthy as of yesterday 18:00 UTC.
- **Steps:**
  1. 06:00 UTC cron fires `daily_nowcast` Dagster job.
  2. Adapters fetch any new daily-frequency observations (electricity, AIS, GDELT, Trends).
  3. L3 DFM Kalman filter advances; ML residual is recomputed.
  4. Combiner reads L1 and L2 last-known posterior, mixes with new L3, emits new nowcast.
  5. Forecast records appended to `forecast_point` with new `run_id`.
  6. Dashboard refresh; MCP cache invalidation.
- **Post-conditions:** new run visible in `/v1/runs/{run_id}` within 30 min of cron start.
- **Success criteria:** end-to-end wall clock ≤ 30 min; zero NaN forecasts emitted.

### 6.2 OS-02 — Monthly Re-estimation
- **Pre-conditions:** prior month's daily runs complete; vintage cutoff frozen.
- **Steps:**
  1. First Monday 02:00 UTC, `monthly_recalibration` job fires.
  2. GPU provisioned via Modal API.
  3. L3 weights re-estimated (LightGBM retraining on factor scores + alt features).
  4. Combiner BMA weights recomputed from rolling 24-month log-score window.
  5. Leaderboard materialized view rebuilt.
  6. GPU released.
- **Failure response:** if GPU provisioning fails 3× → fall back to CPU (slower, still ≤ 4h); if still fails → mode M-08, weights pinned to last-good.

### 6.3 OS-03 — Quarterly Full Run
- **Pre-conditions:** national accounts release detected (BEA, Eurostat, ABS, etc.) → triggers per country.
- **Steps:**
  1. Vintage snapshot frozen at release time; hash computed.
  2. L1 country cores re-estimated via NUTS (NumPyro) on GPU.
  3. L2 GVAR re-estimated using L1 posteriors as informative priors.
  4. L3 retrained on new factor structure.
  5. Combiner emits forecast cohort for all horizons.
  6. Backtest subsystem appends out-of-sample point against now-revealed actual.
- **Success criteria:** new run available within 4h of release.

### 6.4 OS-04 — Ad-hoc Scenario (subscriber)
- **Pre-conditions:** valid API key with scenario quota remaining.
- **Steps:**
  1. POST `/v1/scenario` with shock JSON.
  2. Scenario Parser validates; identifies originating country and shock channel.
  3. Identification selector defaults to Cholesky unless overridden.
  4. Propagator pulls cached L1+L2+L3 posteriors, applies shock at L1 of originating country, propagates through L2, recomputes conditional L3.
  5. Fan chart rendered server-side (matplotlib → PNG and JSON quantiles).
  6. Response with `run_id`, JSON quantile paths, and PNG URL.
- **Performance gate:** p95 ≤ 60 s (canonical workload WLD-SCEN-01).

### 6.5 OS-05 — Vintage Replay (CI)
- **Trigger:** PR opened touching `model/` or `combiner/`.
- **Steps:**
  1. CI checks out PR branch.
  2. Spins up replay environment (containerized).
  3. Iterates over monthly vintages from 2014-01 to most recent − 2y.
  4. At each vintage, re-runs forecast as system would have at the time.
  5. Computes RMSE / CRPS vs. ultimate-revised actuals.
  6. Posts comparison vs. main branch to PR.
- **Pass criterion:** no metric degraded by >5% across any country-horizon cell.

### 6.6 OS-06 — Stress Event Auto-trigger
- **Trigger:** monitored signal exceeds threshold (e.g., VIX > 35, BAA-10y spread > 400bp, equity sell-off > 5% in 1 day).
- **Steps:**
  1. Stress detector emits event.
  2. Scenario service queues canonical stress shocks (Anvil-generated library).
  3. Results published to dashboard; subscribers alerted via webhook.

### 6.7 OS-07 — Source Outage (failure path)
- **Trigger:** primary source 5xx for ≥ 6 consecutive pulls (≈ 30 min).
- **Steps:**
  1. Adapter switches to mirror source if defined (e.g., FRED → ALFRED ALFRED → ECB SDW fallback for some series).
  2. If no mirror, freeze series at last-good; forecast issued with `data_completeness` flag.
  3. If completeness < 90%, refuse to emit (M-08).

### 6.8 OS-08 — Bad Forecast Discovered Post-Publication
- **Trigger:** internal QA or external auditor identifies error.
- **Steps:**
  1. Open incident issue (`inc/` label).
  2. New corrected run issued with same input vintage but new `posterior_hash`.
  3. Old run's `superseded_by` pointer set.
  4. Public retraction notice posted on dashboard incident log.
  5. Post-mortem within 5 business days, published.

---

## 7. Summary of Impacts

### 7.1 Operational
- Adds a daily 06:00 UTC compute window (≤ 30 min on baseline).
- Adds a monthly Sunday→Monday GPU burst window (≤ 4h).
- Adds quarterly full-run windows triggered by external releases.

### 7.2 Organizational
- Requires a single program owner + at most one part-time data lead initially; bus factor risk mitigated by doc-as-code (NFR-MNT-001).

### 7.3 Financial
- Sustaining cloud: ≤ USD 200/mo (NFR-COS-001), broken down approximately as:
  - VMs: USD 80
  - GPU bursts: USD 40
  - Storage: USD 30
  - Egress/CDN/dashboard: USD 30
  - Contingency: USD 20

### 7.4 Reputational
- Public leaderboard exposes the system to embarrassment when wrong — by design. This is a feature, not a bug. The program owner must accept that early-life accuracy below consensus is publicly visible.

---

## 8. Analysis of Proposed System

### 8.1 Summary of Improvements over Status Quo
- Open license closes the access gap.
- Vintage discipline closes the verifiability gap.
- MCP surface closes the agentic-integration gap.
- Hybrid architecture closes the "structural OR accurate" false dilemma.

### 8.2 Disadvantages and Limitations
- **D-01:** Three-layer system is harder to debug than monoliths.
- **D-02:** Bayesian estimation at 80 countries is non-trivial; performance risk RSK-002.
- **D-03:** Vintage discipline for many emerging-market series is fundamentally unavailable pre-2026; backtests will have coverage gaps.
- **D-04:** Public leaderboard means early embarrassment is guaranteed.
- **D-05:** Open dataset constraint forecloses some alt-data sources (e.g., licensed credit card panels) that incumbents use.

### 8.3 Alternatives Considered

| Alt-ID | Alternative | Rejected because |
|---|---|---|
| ALT-01 | Pure ML (Nixtla-only, no structural layer) | Loses interpretability; no scenario semantics |
| ALT-02 | Pure DSGE (EAGLE-style only) | Forecast accuracy historically poor; scaling to 80 countries impractical |
| ALT-03 | Pure GVAR (Pesaran-only) | No structural interpretation; no nowcasting |
| ALT-04 | Wrap an LLM as forecaster | No verifiable inference; would fail POL-02, POL-10 |
| ALT-05 | Use only NiGEM via license | Defeats open-source mission; cost model fails |
| ALT-06 | Defer to academia (don't build) | Gap has persisted >20 years; will not close passively |

### 8.4 Critical Success Factors
- **CSF-01:** Bilateral trade matrix construction must be automatable from Comtrade. If manual curation creeps in, IOC schedule slips.
- **CSF-02:** Vintage archival must start day-1; missed days are permanently lost.
- **CSF-03:** Leaderboard must be live by v0.4 or the verifiability proposition is rhetoric.
- **CSF-04:** Hardware ceiling at 4 vCPU / 16 GB must hold for L2; if not, cost model breaks.

### 8.5 Critical Failure Conditions
- **CFC-01:** OPENGEM at FOC fails primary V&V (≥75% beating AR(1)) → re-baseline as "GVAR-only forecasting toolkit," abandon parity claim.
- **CFC-02:** Cloud bill > USD 400/mo for 2 consecutive months → architectural rebase; possible move to colocated hardware.
- **CFC-03:** Source license violation discovered → take down affected derivatives within 24h.

---

## 9. Notes

### 9.1 Naming
"OPENGEM" intentionally puns on Oxford Economics' GEM as a banner of intent. No trademark conflict has been identified at the time of writing (TBR-005: confirm before public launch).

### 9.2 Open Issues (carried to StRS / SRS)
- TBR-001: country list at IOC (master doc Appendix B).
- TBR-002: Australia inclusion priority (personal-use signal from program owner).
- TBR-003: Whether MCP server's "scenario" tool requires paid auth from day 1 or after pilot.

---

## 10. Appendices

### Appendix A — Acronyms used herein
ADR, BMA, BOE, BMA, CRPS, DM, DSGE, FOC, FPAS, GDP, GEM, GVAR, ICD, IFS, IOC, MCP, MCS, NIESR, OCR, OEx, PDR, PIT, RMSE, SRR, SDR, StRS, SSDD, TBD, TBR, V&V, WB, WDI, WEO. (Full glossary deferred to Iteration 25.)

### Appendix B — Cross-Reference to Master Document Sections
- This document realizes master §1 in full.
- Forward references: §5.3.2 anticipates SSDDs 001–007; §5.4 anticipates the State Machine specified in SAD §4.

### Appendix C — Approval
- Drafted: 2026-05-19 by Chief Systems Engineer (acting).
- Awaiting SRR signoff by Program Owner.

---
*End of OG1-CONOPS-001 — Revision B (draft).*
