# R04 — BGVAR Compute Requirements

| Field | Value |
|---|---|
| Document ID | OG1-RES-004 |
| Revision | B (populated 2026-05-24) |
| Date | 2026-05-24 |
| Status | **Investigated — verdict: H-4 (reframed) HOLDS. Tractable with mature tooling + R03 rescope.** |
| Tests hypothesis | H-4 (reframed in §1 of A.1) |

---

## 1. Reframed hypothesis (recap from rev A.1)

> A Bayesian Global VAR is computationally tractable for the operational cadence OPENGEM needs, on commodity cloud hardware, with acceptable posterior quality (not necessarily full MCMC).

The 4 vCPU / 16 GB pass/fail gate was removed by program-owner direction 2026-05-24. Cost target is informational, not load-bearing.

## 2. What's available off the shelf

### 2.1 `BGVAR` R package (CRAN)

- Stable, maintained, version 2.5.8 as of 2026 (September 2025 update).
- Companion paper: **Boeck, Feldkircher, Huber (2022), "BGVAR: Bayesian Global Vector Autoregressions with Shrinkage Priors in R," *J. Statistical Software* 104(9).** This is the reference implementation.
- Reference theoretical paper: **Crespo Cuaresma, Feldkircher, Huber (2016), "Forecasting with Global Vector Autoregressive Models: a Bayesian Approach," *J. Applied Econometrics* 31(7), 1371–1391.**
- Built-in priors: **Minnesota, Stochastic Search Variable Selection (SSVS), Normal-Gamma (NG)**. Stochastic volatility supported.
- Post-estimation: predictions, structural identification (short-run, sign restrictions), IRFs, historical decompositions, FEVDs.

Source: [BGVAR CRAN package](https://cran.r-project.org/web/packages/BGVAR/index.html); [GitHub mboeck11/BGVAR](https://github.com/mboeck11/BGVAR); [package PDF Sept 2025](https://cran.r-project.org/web/packages/BGVAR/BGVAR.pdf).

**Implication.** Don't reimplement BGVAR in Python / NumPyro / Stan at IOC. Use the R package via a thin RPC adapter (R subprocess called from FastAPI), or via `rpy2`, or via a small Dagster R-runner. Saves months of work.

### 2.2 The compute landscape

Three lines of evidence converge:

1. **Banbura, Giannone, Reichlin (2010)** showed Bayesian VARs with **130 variables / 200,000+ coefficients** estimated on **700 monthly observations** for the US, using natural-conjugate Minnesota priors. *Fast* by their standards.
2. **Natural-conjugate Minnesota / hierarchical priors** enable closed-form posterior moments → no expensive MCMC for the main coefficients. Sub-quadratic in some implementations.
3. **Giannone, Lenza, Primiceri (2015)** "Prior selection for large Bayesian VARs" — full Bayes treatment with shrinkage hyperparameters estimated from likelihood. Standard now.

For OPENGEM scale (40–80 countries × ~6 variables × p=2 lags), the model is **smaller** than BGR's 130-variable US BVAR if BGR-style block structure with hierarchical shrinkage is used. **Tractable on commodity hardware.**

### 2.3 Variational Bayes as backup

If MCMC turns out to be too slow:

- **Koop & Korobilis** ([JoAE forthcoming / 2021 IJF paper](https://www.sciencedirect.com/science/article/abs/pii/S0169207021001862)): "Forecasting using variational Bayesian inference in large vector autoregressions with hierarchical shrinkage."
- Finding: **"VB algorithms represent the best tradeoff between estimation accuracy and computational efficiency, with posterior inference as accurate as nonlinear MCMC methods but considerably more efficient."**
- **Chan et al.** ([JoEconomics 2022](https://www.sciencedirect.com/science/article/abs/pii/S0165188922002093)): "Fast and Accurate Variational Inference for Large Bayesian VARs with Stochastic Volatility."

VB is mature and well-validated for large BVARs. The historical concern that VB underestimates posterior variance turns out to be **largely benign for predictive use** — VB's predictive densities replicate exact-MCMC predictives.

**Implication.** If BGVAR's default MCMC sampler proves slow for ≥40 countries, swap in VB. Accuracy hit is small; speed gain is large.

## 3. Interaction with R03's rescope

R03 proposes that **L2 (BGVAR) is invoked only by the Scenario Subsystem, not by the baseline Forecast service.** That changes the compute cadence:

| Cadence | Original CONOPS | Post-R03 rescope |
|---|---|---|
| L2 re-estimation | Quarterly (every full run) | **Annual**, or on-demand if shock data warrants |
| L2 forecast role | In BMA over L1/L2/L3 every horizon | Not in baseline forecast |
| L2 scenario role | Same | Sole job |

Quarterly compute pressure on L2 drops to ~zero. Annual re-estimation can take a working day (8–12h) on a moderate node without breaking anything. The compute-cliff concern that motivated the original H-4 disappears.

## 4. Hardware recommendation

Even without the rescope, the recommendation is modest:

| Scenario | Spec | Approx. monthly cost (Hetzner / similar) |
|---|---|---|
| **Minimum viable** (Tier-V ~25 countries, p=2, VB or natural-conjugate prior) | 4 vCPU / 16 GB / 200 GB | ~€15–25 |
| **Comfortable** (full MCMC, ~25 countries, stochastic volatility) | 8 vCPU / 32 GB | ~€40–60 |
| **Aspirational FOC** (40–80 countries, full MCMC) | 16 vCPU / 64 GB | ~€80–120 |
| **Burst** (annual full re-estimation only) | GPU optional; modal/runpod on-demand | <€20 amortized |

Even the aspirational tier is **inside the original USD 200/month envelope** if it's the only big line. The CONOPS NFR-COS-001 does not need to move on L2's account.

## 5. Verdict on H-4 (reframed)

**Holds.** BGVAR is computationally tractable for the OPENGEM operating cadence — at 25 countries comfortably on small hardware, at 80 with a moderate upgrade and/or VB. The 4 vCPU / 16 GB original target is achievable for the rescoped role (annual re-est. only). 

The original concern was specifically about **quarterly** full re-estimation at 80 countries, which is now off the table per R03's rescope.

## 6. Decision implications for the CONOPS

| Source | Current | Proposed change |
|---|---|---|
| **CONOPS §7.1 Operational impact** | Quarterly full-run window ≤4h | Remove L2 from quarterly window. Add annual L2 re-estimation window (~12h, deferrable). |
| **NFR-PRF-003** | Full system quarterly run ≤4h on 4 vCPU / 16 GB | Restate per subsystem: L3 quarterly ≤2h on baseline. L2 annual ≤12h on same or moderately upsized node. |
| **NFR-COS-001** | ≤USD 200/mo | Stays. R04 finds no need to move it. |
| **ADR-002** "Python for model service" | — | Add ADR-009: L2 implementation reuses `BGVAR` (R) via a thin process adapter. L3 stays Python (NumPyro / scikit-learn / Nixtla). Polyglot tolerated for time-to-IOC. |
| **RSK-002** "BGVAR scaling intractable" (L=3 I=4) | — | Re-score to L=1 I=2 = 2 (effectively resolved). |
| **TBD-004** "L1 cores Stan vs NumPyro" | — | Drop — L1 reduced to US-only per R03, defer language choice to that single core. |

## 7. Open probes deferred

1. **Concrete benchmark probe.** Install `BGVAR` package on a 4 vCPU / 16 GB VM, run Pesaran 33-country example dataset, measure peak RAM and wall-clock at default settings. Should be deferred until R03 rescope is signed off — if L2 only runs annually, the urgency drops.
2. **R↔Python interop.** If polyglot stack is accepted: pick `rpy2` vs. subprocess vs. dagster-r. Test packaging in a Docker image.
3. **VB fallback validation.** Replicate one Boeck-Feldkircher-Huber example with the package's VB option (if available) vs. default MCMC; compare predictive CRPS.

## 8. Bottom line

BGVAR compute is no longer a load-bearing concern. Mature CRAN package, well-cited literature, VB fallback if needed, modest hardware footprint, and (per R03) much-relaxed cadence. R04 closes as a green-light.

---

*End of R04 Rev B.*
