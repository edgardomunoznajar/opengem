# OG1-CONOPS-001 — Concept of Operations (Rev C — DRAFT)

## Open Global Economic Macroeconometric (OPENGEM) Forecasting System

| Field | Value |
|---|---|
| Document ID | OG1-CONOPS-001 |
| Revision | **C (draft, post-pre-PDR research round)** |
| Date | 2026-05-24 |
| Lifecycle Phase | Concept |
| Supersedes | rev B (`OG1-CONOPS-001.md`) following R99 synthesis |
| Format Reference | IEEE Std 1362-1998 |
| Authority for changes | R99-synthesis.md §3, R01–R06 |

---

## 1. Scope

### 1.1 Identification

This document defines the Concept of Operations for **Program OPENGEM-1**, Block I, the open-source Open Global Economic Macroeconometric Forecasting System. Rev C supersedes rev B following a pre-PDR research round (R01–R06) that pressure-tested the load-bearing assumptions of the prior architecture.

### 1.2 System Overview

OPENGEM is a personal-use, open-source, **OECD-26-vintage-correct** macroeconomic forecasting and situation-awareness system for ~25 economies, with a tracked-only panel for the rest. It produces density forecasts via an L3-centered architecture (Dynamic Factor Model + machine-learning residual + large Bayesian VAR variants, combined via Bayesian Model Averaging). Spillover scenarios are produced on demand by a Bayesian Global VAR (L2). A US-only semi-structural core (L1) provides structural shock identification and narrative for scenarios. A separate Situation Subsystem publishes term-spread recession probabilities and (deferred) geopolitical-risk nowcasts. The system is continuously benchmarked on a public leaderboard against AR(1), random walk, IMF WEO, OECD EO, and forward-curve benchmarks per a variable×horizon evaluation matrix.

### 1.3 Document Overview

This CONOPS establishes the *why*, *for whom*, *under what conditions*, and *to what end* of OPENGEM Block I after the rev B rebaseline. Approval of rev C baselines the **Functional Configuration** of the program for the restarted LOOP_PLAN.

---

## 2. Referenced Documents

Carried forward from rev B plus additions from R01–R06.

| Ref | Title |
|---|---|
| R-01 | Pesaran, Schuermann, Weiner (2004). *Modeling Regional Interdependencies Using a Global Error-Correcting Macroeconometric Model.* |
| R-02 | Banbura, Giannone, Reichlin (2010). *Large Bayesian VARs.* |
| R-03 | IMF FPAS Mark II QPM documentation. |
| R-04 | Faust & Wright (2013). *Forecasting Inflation.* Handbook of Economic Forecasting. |
| R-05 | Diebold & Mariano (1995). *Comparing predictive accuracy.* |
| R-06 | Hansen, Lunde, Nason (2011). *Model Confidence Set.* |
| R-07 | Croushore & Stark (2001). *A real-time data set for macroeconomists.* JoE. |
| R-08 | Rossi & Sekhposyan (2014). *Evaluating predictive densities.* IJF. |
| R-09 | D'Agostino, Gambetti, Giannone (2013). *Macroeconomic forecasting and structural change.* JoAE. |
| R-10 | Goulet Coulombe (2024). *The Macroeconomy as a Random Forest.* JoAE. |
| R-11 | Boeck, Feldkircher, Huber (2022). *BGVAR: Bayesian Global VARs with Shrinkage Priors in R.* JSS 104(9). |
| R-12 | Koop & Korobilis. *Variational Bayesian inference in large VARs with hierarchical shrinkage.* IJF 2021. |
| R-13 | Bauer & Mertens (2018). *Economic Forecasts with the Yield Curve.* FRBSF Economic Letter / Annual Review of Financial Economics. |
| R-14 | Benigno, Di Giovanni, Groen, Noble (NY Fed SR1017). *The GSCPI: A New Barometer of Global Supply Chain Pressures.* |
| R-15 | Caldara & Iacoviello (2022). *Measuring Geopolitical Risk.* FRB IFDP 1222. |
| R-16 | Bybee, Kelly, Manela, Xiu (2024). *Business News and Business Cycles.* Journal of Finance. |
| R-17 | Fernandez, Koenig, Nikolsko-Rzhevskyy (2011). *A Real-Time Historical Database for the OECD.* Dallas Fed WP 96. |
| R-18 | IEEE Std 1362-1998. *CONOPS Guide.* |
| R-19 | MIL-STD-498 (1994). *Software Development and Documentation.* |

---

## 3. Current Situation

### 3.1 Incumbent Systems (unchanged from rev B)

Proprietary multi-country macroeconometric systems remain dominated by Oxford Economics GEM, NIESR NiGEM, Moody's Analytics Global. Open alternatives (FRB/US, EAGLE, GVAR Toolbox, BGVAR R package) are research artifacts without operational pipelines, leaderboards, or MCP surfaces.

### 3.2 Diagnosed Gap (updated)

The gap as stated in rev B remains real, but its *resolution* is bounded by **data availability** (R02): there is no public real-time vintage archive for most non-OECD economies. Therefore the "open global" framing of rev B is aspirational past the OECD-26 perimeter.

The gap OPENGEM Block I actually closes is:

- An **operational, continuously-verified, vintage-correct forecasting + scenario + situation-awareness system** for the OECD-26, with density forecasts, multiple horizons, MCP integration, and a public leaderboard — none of which the open alternatives offer in combination.

The "global" ambition is preserved as a Block II/III goal contingent on emerging-market self-archive maturation.

### 3.3 Stakeholder Pain (private-use scope)

Single stakeholder: the program owner (personal use). Pain points:

| Pain | Cost today |
|---|---|
| No personally-owned multi-country density forecast | Reliance on headline-level consensus / news |
| Cannot run custom scenarios with structural identification | Subscription cost or improvise |
| Cannot integrate forecasts into oblique-suite agentic tooling | No MCP surface from any incumbent |
| No vintage-corrected backtest of any forecast I'd want to trust | Forecasts are unfalsifiable |

---

## 4. Justification

### 4.1 Necessity

Same as rev B but reframed for private-use scope: cheap cloud + mature Bayesian libraries + free public data + MCP standard now make a personal-scale OECD-26 forecasting system feasible. OPENGEM is the missing piece in the oblique suite's economic-reasoning chain.

### 4.2 Strategic Fit within the oblique suite

| oblique-* | Role with OPENGEM |
|---|---|
| oblique-oracle | Consumes OPENGEM forecasts as priors for Monte Carlo simulation |
| oblique-anvil | Generates stress shocks; OPENGEM consumes shock specs via Scenario subsystem |
| oblique-plan | Turns OPENGEM scenarios into decision trees |
| oblique-lawyer | Independent — no direct dependency |
| oblique-thinker | Independent |
| oblique-seer | OPENGEM dashboard styled via seer-derived patterns (later) |
| oblique-weaver | Used to consistency-check forecast cards vs. data layer |

### 4.3 Commercial Rationale

**Deferred.** Rev B contained a monetization narrative; rev C marks it deferred per program-owner direction 2026-05-24. The MCP-compatible interface is built for *personal-agentic* use first; monetization re-evaluation in a future public-launch review.

---

## 5. Concepts for the Proposed System

### 5.1 Background, Objectives, and Scope

#### 5.1.1 Objectives (re-ranked per R99)

1. **Verifiability** for Tier-V countries: every forecast has provenance, is scored on the leaderboard within 4Q.
2. **Coverage tiered**: Tier-V (vintage-correct, ~25 countries) + Tier-T (tracked-only, ~50+ countries).
3. **Interpretability + Accuracy**: L3 carries accuracy; L1 (US) and L2 carry interpretability.
4. **Cost discipline** (informational; no longer a hard gate).
5. **Integration**: first-class MCP citizen of the oblique suite.

#### 5.1.2 Scope (Block I, post-rebaseline)

**In scope:**
- Density forecasts for **Tier-V countries** at horizons {1Q, 4Q, 8Q, 20Q} for: GDP (real, nominal), CPI (headline, core), policy rate (decision-record + curve-implied path), unemployment rate.
- Monthly L3 nowcast refresh for Tier-V; daily nowcast where high-frequency covariates exist.
- Ad-hoc scenario IRFs (L2 propagation, L1 identification when origin = US).
- Public leaderboard for Tier-V vs. AR(1), RW, WEO, OECD EO benchmarks.
- **Wider information surface (R06): D-MKT, D-SCN, D-GEO, D-MED** as L3 covariates.
- **Situation Subsystem**: term-spread recession probability (Tier-V); GPR nowcast endpoint (deferred build).
- Tracked-only dashboard for Tier-T countries (no leaderboard inclusion).
- MCP server with tools for forecast/scenario/recession-probability/situation.

**Out of scope (Block II/III):**
- Sectoral / industry detail.
- Climate / energy coupling beyond GSCPI-style aggregates.
- Tier-T leaderboard inclusion before self-archive matures (~2028+).
- High-frequency financial markets forecasting (beyond term-spread).
- Custom topic model for media (use GDELT GKG tone at IOC; defer Bybee-style topic model to v0.4+).

#### 5.1.3 Tier-V country roster (initial; finalize at SRR)

Derived from R02 §3 best-case tier:
**Tier-V (≥4 variables, ≥10 years vintage, BIS policy rates):**
US, CA, UK, DE, FR, IT, ES, NL, BE, AT, LU, IE, GR, PT, FI, SE, DK, NO, CH, JP, KR, AU, NZ, MX, IS (~25 countries).
**Conditionally Tier-V** (subject to ORDRA roster confirmation): TR, CL, CZ, HU, PL, SK, SI, EE.
**Tier-T (tracked-only, no leaderboard):** RU, CN, IN, BR, ID, ZA, SA, AE, EG, NG, VN, TH, PH, MY, AR, CO, PE, others as bandwidth allows.

### 5.2 Operational Policies and Constraints

| Policy-ID | Statement | Change vs. rev B |
|---|---|---|
| POL-01 | All ingestion is from public or programmatic-access-permitted sources. **OPENGEM does not redistribute or cache FRED Content; FRED is used for series discovery only. Upstream agencies (BEA/BLS/FRB/Treasury/Census/Eurostat/...) are the persistent source of truth.** | Reworded for FRED 2024 ToS |
| POL-02 | Every published forecast reproducible from `(code_sha, vintage_hash, prior_hash, posterior_hash)`. | Unchanged |
| POL-03 | **Tier-V leaderboard uses real-time (vintage) data only.** Tier-T tracked panel uses latest-revised, clearly labelled. | New tier semantics |
| POL-04 | Forecasts are never silently retracted. | Unchanged |
| POL-05 | Model cards accompany every release. | Unchanged |
| POL-06 | GPU usage is ephemeral. | Unchanged |
| POL-07 | No PII. | Unchanged |
| POL-08 | All schemas and ICDs are open. | Unchanged |
| POL-09 | Leaderboard ranking algorithm is open and version-pinned. | Unchanged |
| POL-10 | "Beat WEO/OECD EO" claims require Diebold-Mariano p<0.05 over ≥8 quarters of vintage-correct out-of-sample data. **Consensus Economics benchmark deferred** until access path resolves. | Substituted WEO/OECD EO for consensus |
| **POL-11 (new)** | **Tier-T countries are tracked-only and explicitly excluded from leaderboard claims**, regardless of how well OPENGEM appears to do on revised-data backtests for them. |  |

### 5.3 Description of the Proposed System

#### 5.3.1 System-Level Block Diagram (revised)

```
                 ┌────────────── External Data Sources ──────────────┐
                 │  Upstream US agencies (BEA, BLS, FRB, Treasury,   │
                 │  Census) · OECD ORDRA · ECB SDW · BIS · IMF SDMX  │
                 │  · WB WDI · UN Comtrade  │  GSCPI · PortWatch ·   │
                 │  GPR · GDELT GKG · OFAC/EU/UN sanctions           │
                 └───────────────────┬───────────────────────────────┘
                                     ▼
                  Ingestion + Vintage Store (Tier-V: vintage; Tier-T: latest-only)
                                     ▼
                   Curation & Feature Layer (frequency harmoniz., SA, weights)
                                     ▼
                   ┌─────────────────────────────────────────────┐
                   │     L3  —  Workhorse Forecast Layer        │
                   │   (DFM + ML residual + large BVAR variants;│
                   │    BMA over variants → density forecast)   │
                   └────────────┬────────────────────────────────┘
                                │
   ┌────────────────────────────┼──────────────────────────────┐
   ▼                            ▼                              ▼
 Forecast Service        Backtest Service             Scenario Subsystem
 (Tier-V leaderboard,   (vintage replay,                ──► L2 BGVAR (spillover IRFs, annual re-est.)
  V&V matrix gates)      DM tests, MCS)                 ──► L1 US Core (structural identification, narrative)
                                                       
   ┌──────────────── Situation Subsystem (new) ───────────────┐
   │  Term-spread recession probability (Tier-V)               │
   │  GPR nowcast (44 countries, deferred build)              │
   └───────────────────────────────────────────────────────────┘

   Public surface: REST API (Spring Boot) · MCP Server · Dashboard (Vercel)
```

#### 5.3.2 Capabilities

| Cap-ID | Capability | Block I Status |
|---|---|---|
| CAP-01 | Density GDP forecast, Tier-V, 1Q/4Q/8Q/20Q | IOC |
| CAP-02 | Density CPI forecast, Tier-V | IOC |
| CAP-03 | Policy-rate path (curve-anchored), Tier-V | IOC |
| CAP-04 | Unemployment forecast, Tier-V | v0.4 |
| CAP-05 | Daily L3 nowcast where high-freq covariates exist | v0.4 |
| CAP-06 | Ad-hoc scenario IRFs (L2 propagation; L1 identification when US-origin) | v0.4 |
| CAP-07 | Tier-V public leaderboard with V&V matrix | v0.4 |
| CAP-08 | Tracked-only dashboard for Tier-T | v0.4 |
| CAP-09 | Model cards per release | v1.0 |
| CAP-10 | Bulk historical forecast export | v1.0 |
| CAP-11 | MCP-driven scenario authoring | v0.4 |
| **CAP-12 (new)** | **Term-spread recession-probability endpoint (Tier-V)** | v0.4 |
| **CAP-13 (new)** | **GPR nowcast endpoint (44 countries)** | Block II candidate; build deferred pending probe |

### 5.4 Modes of Operation

| Mode-ID | Mode | Description | Trigger | Change |
|---|---|---|---|---|
| M-01 | Quiescent Read | Serve cached forecasts | Default | — |
| M-02 | Daily Nowcast | Refresh L3 state | 06:00 UTC cron | L3 only |
| M-03 | Monthly Recalibration | Re-estimate L3 weights + BMA over variants | 1st Mon 02:00 UTC | L3 only (was L3+L2+L1) |
| M-04 | Quarterly Full Run | Re-estimate L3 + L1 (US) | National accounts release | L2 dropped from quarterly |
| **M-04a (new)** | **Annual GVAR Re-estimation** | Re-estimate L2 BGVAR | Once per calendar year on a fixed date | New mode |
| M-05 | Scenario Run | Apply shock; compute counterfactual; cache | API POST `/scenario` | L1+L2 invoked |
| M-06 | Vintage Replay | Backtest over historical vintages | CI on PR or cron weekly | Tier-V only |
| M-07 | Maintenance | Read-only frozen | Operator-initiated | — |
| M-08 | Degraded | One subsystem failed | Auto | — |
| **M-09 (new)** | **Situation Refresh** | Recompute recession probability + (when built) GPR nowcast | Daily | New mode |

### 5.5 User Classes (private-use scope)

Rev B listed 8 personas; rev C narrows to realistic private-use shape:

| User-ID | Class | Persona | Auth |
|---|---|---|---|
| U-01 | Program owner (self) | Both consumer and operator | SSH + 2FA + API key |
| U-02 | Internal agent (oblique-anvil, -oracle, -plan) | Programmatic shock submission and forecast consumption | API key (rotating) |
| U-03 | Public anonymous reader | Dashboard browsing only | None |
| U-04 | Future academic auditor | Vintage replay verification (read-only) | None |

### 5.6 Support Environment

- **Hosting:** Hetzner CCX23 baseline (1 VM at IOC; second only if L2 annual re-estimation needs it).
- **Monitoring:** Grafana + Loki + Prometheus on-node.
- **Documentation:** Markdown in-repo; GitHub Pages.
- **Community:** GitHub repository, public; no Discord at private-project scope.

---

## 6. Operational Scenarios

Carried forward from rev B with edits per architecture changes.

### 6.1 OS-01 — Routine Daily Nowcast

Unchanged from rev B except: **L3 only** (no L2 in critical path). End-to-end ≤30 min.

### 6.2 OS-02 — Monthly Re-estimation

**L3 weights only.** GPU provisioned via Modal API for the boost-tree retraining if needed; otherwise CPU. Combiner BMA over L3 variants is recomputed from rolling 24-month log-score window.

### 6.3 OS-03 — Quarterly Full Run

L3 + L1 (US). National-accounts triggered. L2 *not* in this loop.

### 6.4 OS-03a (new) — Annual GVAR Re-estimation

Once per year, fixed date. L2 BGVAR re-estimated via the `BGVAR` R package on a moderately sized node (8–16 vCPU / 32–64 GB). Annual posterior cached; used by Scenario Subsystem until next year. If MCMC slow, VB fallback per R04.

### 6.5 OS-04 — Ad-hoc Scenario

POST `/v1/scenario`. Scenario Subsystem retrieves cached L2 posterior; uses L1 (US) for identification if shock origin = US, otherwise default Cholesky / sign restrictions in L2. Propagation through L2; L3-conditional updates for non-Tier-V countries. Fan chart rendered. p95 ≤ 60s.

### 6.6 OS-05 — Vintage Replay (CI)

Tier-V only. PR opened touching `model/` or `combiner/`. Replays 2014–most-recent over monthly vintages; computes RMSE / CRPS / DM / MCS vs. main branch. Pass: no metric degraded >5%.

### 6.7 OS-06 — Stress Event Auto-trigger

Unchanged from rev B. Triggers stress shocks library through Scenario Subsystem.

### 6.8 OS-07 — Source Outage

Adapter switches to mirror. **Notable additional fallback for FRED-substituted sources**: each upstream US agency has its own outage profile; the adapter cohort handles per-agency 5xx independently.

### 6.9 OS-08 — Bad Forecast Discovered

Unchanged.

### 6.10 OS-09 (new) — Situation Endpoint Update

Daily. Term-spread recession-probability recomputed per Tier-V country using Bauer-Mertens replication code adapted per country. When GPR nowcast build is approved, runs alongside.

---

## 7. Summary of Impacts

### 7.1 Operational

- Daily L3 nowcast window (≤30 min on baseline).
- Monthly L3 recalibration window (≤4h CPU; GPU optional).
- Quarterly L3+L1 window (≤4h per Tier-V country).
- **Annual L2 re-estimation window** (~12h, fixed date).
- Daily Situation refresh (≤5 min).

### 7.2 Organizational

Single program owner; bus factor of 1 mitigated by doc-as-code.

### 7.3 Financial

| Line | Estimate (USD/mo) | Note |
|---|---|---|
| Primary VM (Hetzner CCX23 or equivalent) | 30–50 | Baseline |
| Annual L2 re-estimation node (amortized) | 5–10 | Burst node × 12h × 1/year |
| GPU bursts (Modal/RunPod) | 10–30 | Monthly L3 retraining |
| Storage (incl. vintage archive ~50 GB) | 5–10 | Negligible |
| Egress + dashboard CDN | 5–10 | Vercel free or minimal |
| Contingency | 10 | — |
| **Total realistic** | **65–120** | Inside USD 200 informational target |

### 7.4 Reputational

Tier-V leaderboard is publicly visible from day 1. Early-life performance below WEO/OECD EO is acceptable as long as the *failure mode is interpretable* via the V&V matrix.

---

## 8. Analysis

### 8.1 Improvements over status quo

- **Open license + vintage discipline + density forecasts + MCP surface** — none of the open alternatives offer this combination.
- **OECD-26 personal-scale operational forecasting** — a market of one, served well.

### 8.2 Disadvantages and Limitations

- D-01: Tier-V scope is honestly OECD-only. Naming "OPENGEM" is aspirational.
- D-02: Single-maintainer.
- D-03: Public leaderboard means visible failure.
- D-04: Upstream-agency adapter cohort is more complex than a single FRED dependency would have been.
- D-05: Block I cannot deliver true "≥40 / ≥80" coverage; Tier-T is a tracking, not forecasting, claim.

### 8.3 Alternatives Considered (carried + added)

| Alt-ID | Alternative | Rejected because |
|---|---|---|
| ALT-01 | Pure ML | Loses interpretability/scenarios; |
| ALT-02 | Pure DSGE | Accuracy historically poor at scale; |
| ALT-03 | Pure GVAR | No nowcasting/density at scale; |
| ALT-04 | LLM-as-forecaster | Unverifiable; |
| ALT-05 | Wrap NiGEM | Open-source mission failure; |
| ALT-06 | Defer to academia | Gap persists 20+ years; |
| **ALT-07 (new)** | **Stay with rev B 3-layer-equal architecture** | R03 evidence: 3 ≯ 2 ≯ 1 for accuracy; cost not justified |
| **ALT-08 (new)** | **Use FRED as primary US data source** | R05: 2024 ToS prohibits caching + ML training |

### 8.4 Critical Success Factors (revised)

- CSF-01 Tier-V data foundation present at IOC (vintage adapters complete; upstream-agency adapters complete).
- CSF-02 L3 BMA-combiner produces well-calibrated density on Tier-V at 1Q–4Q.
- CSF-03 Leaderboard live by v0.4 with V&V matrix.
- CSF-04 Hardware envelope holds informationally (≤USD 200/mo target, no hard ceiling).
- **CSF-05 (new)** Upstream-agency adapter cohort complete for US BEFORE FRED-substitution-dependent code is written.

### 8.5 Critical Failure Conditions (revised)

- CFC-01 Tier-V V&V matrix fails at FOC across the board → re-baseline as "verifiable forecast infrastructure," drop "operational parity" framing.
- CFC-02 *removed* — cost is informational, no auto-rebase.
- CFC-03 Source ToS violation discovered → take down within 24h. (Unchanged.)
- **CFC-04 (new)** Vintage archive corruption discovered → re-derive from raw source; mark affected leaderboard window void.

---

## 9. Notes

### 9.1 Naming

"OPENGEM" remains aspirational on the global axis. Consider re-naming if Block II/III doesn't materialize. Defer the naming question.

### 9.2 Open Issues carried to STRS / SRS

- TBR-006: ACLED ToS for private-non-commercial use.
- TBR-007: Final Tier-V country roster (currently ~25; finalize at SRR).
- TBR-008: Consensus Economics access (deferred to future public-launch round).
- TBR-009: Whether the SSDD-008 Situation Subsystem owns L3-internal recession-probability or wraps an external Bauer-Mertens replication.

---

## 10. Appendices

### Appendix A — Acronyms

Carried forward; add: **BMA**, **BVAR**, **CRPS**, **DFM**, **GPR**, **GSCPI**, **MCS**, **NUTS**, **ORDRA**, **PIT**, **RTDSM**, **SDMX**, **Tier-V / Tier-T**, **WEO**.

### Appendix B — Approval

- Drafted (rev C): 2026-05-24 by Chief Systems Engineer (acting).
- **Awaiting program-owner sign-off** to baseline.
- Predecessor rev B remains the prior baseline until sign-off.

---

*End of OG1-CONOPS-001 — Revision C (DRAFT).*
