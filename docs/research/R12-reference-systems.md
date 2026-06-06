# R12 — Reference Systems Comparison

| Field | Value |
|---|---|
| Document ID | OG1-RES-012 |
| Revision | A (2026-05-24) |
| Date | 2026-05-24 |
| Status | **Reference-only memo: how OPENGEM rev C compares to the systems it's measured against.** |

---

## 1. Why this exists

Six published systems form the reference set for OPENGEM:

- **FRB/US** (Federal Reserve Board) — closed structural US model
- **FPAS Mark II** (IMF / national central banks) — open QPM template
- **NiGEM** (NIESR) — proprietary global model
- **Oxford GEM** (Oxford Economics) — proprietary global model
- **EAGLE / EAGLE-FLI** (ECB) — open DSGE euro-area model
- **GVAR Toolbox / BGVAR** (Pesaran et al. / Boeck et al.) — open spillover-VAR

This memo summarizes each and locates OPENGEM rev C in that space.

## 2. FRB/US

**What it is**: Large-scale estimated general equilibrium model of the US economy, in use at the Fed since 1996.
**Coverage**: US-only.
**Code**: Open Python (`PyFRB/US`) since April 2022; latest update February 2026. EViews version also distributed.
**Source**: [federalreserve.gov/econres/us-models-python.htm](https://www.federalreserve.gov/econres/us-models-python.htm).
**What OPENGEM borrows**: L1 US semi-structural core is in the FRB/US tradition (Taylor rule, NK Phillips curve, fiscal closure). PyFRB/US is a candidate **reference implementation** for OPENGEM's L1 if NumPyro reimplementation proves slow.
**What OPENGEM does differently**: OPENGEM L1 is *one of three layers*, not the whole system. OPENGEM's forecast critical path is L3, not L1.
**Verdict**: PyFRB/US is a useful starting point for OPENGEM L1. Consider extending or wrapping rather than rebuilding.

## 3. FPAS Mark II (IMF / national QPM template)

**What it is**: Second-generation Policy Analysis and Forecasting System framework developed by the IMF and adopted by national central banks. Emphasizes uncertainty quantification and risk-management framing for monetary policy.
**Coverage**: Country-specific QPMs in Ghana, Rwanda, Jordan, Philippines, India, Armenia (most recent — launched 2024), and ~20+ others through IMF capacity-development engagements.
**Approach**: Semi-structural Bayesian quarterly projection model per country — exactly OPENGEM's L1 archetype.
**Code**: Country-specific; documentation in IMF Working Papers. No single unified open codebase.
**What OPENGEM borrows**: L1 country-core design pattern is FPAS-II inspired. Prior structure, equation system count, identification strategy.
**What OPENGEM does differently**: FPAS-II is *per central bank*, owned by that institution. OPENGEM is *one operator, many countries* — for Block I, only US is built; others deferred.
**Verdict**: FPAS-II is the design pattern; OPENGEM is not in scope to compete with FPAS-II as a deployment.

## 4. NiGEM (NIESR)

**What it is**: Global econometric model in use since 1987. Proprietary; licensed.
**Coverage**: **60+ countries and regions**, 5,000+ macro-variables, 80–200 variables per country.
**Approach**: New Keynesian DSGE-influenced general equilibrium; **econometrically estimated** key behavioral equations; rational/model-consistent expectations; Taylor-rule monetary policy; long-run fiscal solvency.
**Closure**: Global — outflows from one country match inflows to others.
**Coverage of policy regimes**: Modifiable; 5,000+ variables tunable for scenarios.
**Pricing**: ~USD 80–150k/year for institutional subscribers.
**What OPENGEM at FOC reaches toward**: NiGEM-level country breadth (60+) and variable depth (80–200 per country). Block I doesn't try.
**What OPENGEM does differently**: Open license; vintage discipline; public leaderboard; smaller variable set per country; L3-centered architecture vs. NiGEM's monolithic structural-econometric core.
**Verdict**: NiGEM is the **commercial moat OPENGEM is asymptotically trying to displace**, not Block I's competitor. Block I aims for OECD-26 with comparable rigor at zero cost; FOC is wider; Block II/III imagines comparable breadth.

## 5. Oxford GEM (Oxford Economics)

**What it is**: Proprietary global econometric model; ~80 countries deep + ~200 lighter.
**Approach**: Similar New-Keynesian-influenced framework to NiGEM, with proprietary calibration and extensive sectoral detail.
**Pricing**: USD 50–250k/year.
**Coverage**: 200+ countries (varying depth).
**What OPENGEM does differently**: Same as vs. NiGEM — open, smaller scope, vintage-correct, accountable.
**Verdict**: GEM is the *namesake* OPENGEM puns on, and the commercial benchmark. Block I doesn't approach GEM's breadth; the bet is that **transparency + accountability is more valuable than breadth** for the use case OPENGEM serves.

## 6. EAGLE / EAGLE-FLI (ECB)

**What it is**: New Keynesian multi-country DSGE model of the euro area + global. EAGLE-FLI extends with banking sector and financial frictions.
**Coverage**: 4 regions in baseline EAGLE (US, EA, Rest of EU, Rest of World); extended to LU-EAGLE for Luxembourg-specific analysis; per-country extensions by various central banks.
**Approach**: Microfounded DSGE with full New Keynesian structure; designed for policy analysis, not raw forecasting.
**Code**: Implemented in Dynare; open via ECB working papers and Dynare archives.
**What OPENGEM borrows**: Identification design patterns for L1 US core; scenario propagation logic for the Scenario Subsystem.
**What OPENGEM does differently**: Forecasting-first orientation (L3 workhorse); not DSGE; multi-country breadth via L2 GVAR, not coupled DSGE blocks.
**Verdict**: Useful reference for scenario identification; not a forecasting competitor.

## 7. GVAR Toolbox / BGVAR

**What it is**: GVAR Toolbox = Pesaran et al.'s Matlab/Excel implementation, ~33 countries. BGVAR = Boeck-Feldkircher-Huber 2022 R package on CRAN with Bayesian shrinkage priors.
**Approach**: Spillover-VAR with country-specific blocks weighted by bilateral trade.
**What OPENGEM uses directly**: **BGVAR R package as the L2 implementation**, called via process adapter (ADR-009).
**Verdict**: This is OPENGEM's actual dependency, not a reference comparison. The whole L2 layer is essentially "BGVAR with annual cadence, integrated."

## 8. Where OPENGEM rev C sits

| Axis | FRB/US | FPAS-II | NiGEM | Oxford GEM | EAGLE-FLI | BGVAR | **OPENGEM rev C** |
|---|---|---|---|---|---|---|---|
| Open license | ✓ (US) | Partial | ✗ | ✗ | ✓ (EA) | ✓ (R) | **✓ end-to-end** |
| Multi-country | ✗ | ✗ (per CB) | ✓ (60+) | ✓ (80+) | ✓ (4 region) | ✓ (33) | **✓ Tier-V ~26–35** |
| Density forecasts | Partial | ✓ | Partial | Partial | Limited | ✓ | **✓ (BMA over L3 variants)** |
| Vintage-correct backtests | Internal | Internal | Internal | Internal | Limited | Limited | **✓ public** |
| Public leaderboard | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | **✓** |
| Operational pipeline | ✓ (Fed) | ✓ (national CBs) | ✓ | ✓ | Partial | ✗ (research) | **✓** |
| MCP / agentic surface | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | **✓** |
| Cost (institutional) | $0 | Capacity-dev | $80–150k | $50–250k | $0 | $0 | **$0** |
| Structural narrative | ✓✓ | ✓✓ | ✓ | ✓ | ✓✓ | ✗ | **✓ (US only)** |
| Spillover IRFs | ✗ | ✗ | ✓ | ✓ | ✓ (EA) | ✓ | **✓ (annual L2)** |
| Situation/recession indicators | ✗ | ✗ | Partial | Partial | ✗ | ✗ | **✓ (new SSDD)** |

**Reading this table**: no single reference system combines all the columns. OPENGEM rev C is the first attempt to combine **open license + multi-country + density + vintage + public leaderboard + MCP** in one place.

## 9. Where OPENGEM should *not* try to win

- **Country breadth**: NiGEM and Oxford GEM have 60–80+ deep country cores from 30+ years of investment. OPENGEM never catches them on raw breadth. Don't try.
- **Sectoral depth**: Both commercial systems carry industry-level GVA, demographic detail, household composition. OPENGEM Block I is macro-aggregate only.
- **High-frequency financial markets**: Oxford GEM has investment-grade FX and rates forecasts. OPENGEM treats markets as inputs and one situational endpoint (recession probability). Don't compete on FX forecast accuracy.
- **Structural narrative breadth**: FPAS-II/NiGEM produce per-country narratives. OPENGEM produces US narrative only at IOC.

## 10. Where OPENGEM should win

- **Transparency**: vintage-correct backtests public from day 1; no incumbent does this.
- **Reproducibility**: every forecast carries `(code_sha, vintage_hash, prior_hash, posterior_hash)`; impossible to replicate any incumbent's historical forecast.
- **Cost**: zero subscription vs. $50–250k/year.
- **Density**: explicit P10/P50/P90 with PIT-tested calibration; most incumbents publish point forecasts with narrative uncertainty bands.
- **Agentic integration**: MCP-native from IOC; no incumbent has this.
- **Situation awareness**: dedicated recession-probability and (deferred) GPR-nowcast endpoints; commercial systems bury these in commentary.
- **Accountability culture**: leaderboard ranking algorithm itself is open and version-pinned; no incumbent invites that scrutiny.

## 11. Bottom line

OPENGEM rev C is not "NiGEM but cheaper." It's **a different product**: an open, vintage-correct, density-aware, accountability-first, agent-integrated economic forecasting system for OECD-26 + small set of EM economies, with structural narrative and spillover scenarios as add-ons rather than as the primary deliverable. The reference systems above are useful design vocabulary; none of them is OPENGEM's competitor in 1:1 sense.

---

*End of R12 Rev A.*
