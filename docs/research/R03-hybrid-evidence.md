# R03 — Hybrid Architecture Evidence

| Field | Value |
|---|---|
| Document ID | OG1-RES-003 |
| Revision | B (populated 2026-05-24) |
| Date | 2026-05-24 |
| Status | **Investigated — verdict: H-3 WEAK as stated. Architectural rescope proposed.** |
| Tests hypothesis | H-3 |

---

## 1. Hypothesis under test (H-3)

> The 3-layer hybrid (L1 country cores + L2 BGVAR + L3 DFM/ML), combined via BMA, **strictly dominates** each constituent layer alone in published out-of-sample evaluations, by a margin large enough to justify the engineering cost of building all three.

## 2. Evidence

### 2.1 Combinations

- Stock-Watson and the broader combination literature: **simple equal-weighted forecast combinations are remarkably competitive with sophisticated weighting schemes.** "In cases where the marginal predictive content of variables is small or modest, a simple average forecast might be more accurate than estimated combinations." Time-varying weights can add gains but inconsistently. ([Hansen, JoE 2008](https://www.sciencedirect.com/science/article/abs/pii/S0304407608001097); follow-ups.)
- For *density* forecasts in macro: equal-weighted combination for output growth, **BMA for inflation**, are the best-calibrated single methods ([Rossi-Sekhposyan, IJF 2014](https://www.sciencedirect.com/science/article/abs/pii/S0169207013000460)).
- **Combination > any single model** is well-established. **Combination of three vs. combination of two** is *not*.

### 2.2 L2 (GVAR / BGVAR) — what's it actually good for?

- The reference forecasting evaluation: Chudik-Pesaran review and follow-up Fed IFDP 1056 ("Evaluating a Global Vector Autoregression for Forecasting"). Conclusion: "substantial room for an improved, more robust specification of the GVAR" — i.e., GVAR is a credible but not dominant forecaster. ([Fed IFDP 1056](https://www.federalreserve.gov/pubs/ifdp/2012/1056/ifdp1056.pdf); [Chudik-Pesaran handbook chapter](https://files.econ.cam.ac.uk/people-files/mhp1/pp16/Chudik-and-Pesaran-(2016)-Theory-and-practice-of-GVAR-modelling.pdf).)
- Where GVAR shines: **cross-country spillover IRFs**, **joint multi-country shock propagation**, **global imbalance analysis**. These are the *story* applications, not the *baseline forecast* applications.
- For point forecasts of country-level GDP / CPI, large BVAR + factor models routinely match or beat GVAR.

### 2.3 L1 (DSGE / semi-structural country cores)

- ECB NAWM (Christoffel-Coenen-Warne, ECB WP 1185): NAWM "compares quite well with the reduced-form models" — but **a large BVAR can outperform NAWM** for area-wide forecasts. ([ECB WP 1185](https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp1185.pdf).)
- Follow-up density-forecast comparison: BVAR generally provided superior density forecasts; **performance deteriorated substantially with the onset of the Great Recession** — structural-break vulnerability common to both. ([ECB WP 1536](https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp1536.pdf).)
- DSGE / structural cores: **strong for narrative and identification** (shocks have economic interpretation, IRFs tell a story, fiscal-monetary feedback is explicit); **mixed for raw forecast accuracy** post-1985.

### 2.4 L3 (DFM + ML)

- Goulet Coulombe's **Macroeconomic Random Forest** ([JoAE 2024](https://onlinelibrary.wiley.com/doi/abs/10.1002/jae.3030)): "delivers clear forecasting gains over numerous alternatives, performs well for inflation." Sources of ML gains decomposed as: nonlinearities, regularization, cross-validation, alternative loss functions. ([Coulombe et al. JoAE 2022, "How is ML useful for macro forecasting?"](https://onlinelibrary.wiley.com/doi/full/10.1002/jae.2910).)
- Mixed-frequency DFMs (Banbura-Giannone-Reichlin, Stock-Watson) are the workhorse for **short-horizon nowcasting** and remain hard to beat at 1Q.
- DFM + ML residual is the **dominant forecast-accuracy combination** in the recent literature.

## 3. What this means for the 3-layer hybrid claim

The hypothesis "L1 + L2 + L3 strictly dominates any 2-layer subset, by a margin worth the engineering cost" **does not survive contact with the literature**:

| Pair / triple | Forecast-accuracy evidence | Cost evidence |
|---|---|---|
| L3 alone | Strong; ML+DFM is the workhorse | Cheap |
| L2 + L3 | Plausibly adds spillover-aware scenarios, but L2's *forecast* contribution is marginal | L2 expensive (see R04) |
| L1 + L3 | L1 adds narrative; little forecast gain | L1 most expensive (per-country priors, identification, equations) |
| L1 + L2 + L3 | No published evidence of a strictly-dominant 3-layer macro forecaster at the OPENGEM scale | Most expensive of all |

**The 3-layer hybrid is not justified by *forecast accuracy* literature.** It is justified — if at all — by *what each layer does that the others can't*:

| Layer | Unique job | Forecast-accuracy contribution |
|---|---|---|
| L1 country core | Structural shock identification, fiscal-monetary feedback story, narrative on *why* | Low to moderate, often dominated by BVAR |
| L2 GVAR | Cross-country spillover scenarios, joint shock propagation | Marginal vs. country-by-country BVAR + DFM |
| L3 DFM + ML | Short-horizon point and density forecasts | High — the workhorse |
| Combiner | Calibration of density via combination | High — both equal-weight and BMA work |

## 4. Verdict on H-3

**H-3 as stated: WEAK.** The 3-layer hybrid is *not* the architecture the forecasting literature would prescribe if the goal is forecast accuracy. It's the architecture you build if you want **all three things** — accurate forecasts + structural narrative + spillover scenarios — under one roof.

That may still be the right answer for OPENGEM. But the CONOPS rationale needs to change: stop claiming the 3-layer hybrid is forecast-accuracy-superior (it isn't published as such), and start claiming it covers *three distinct jobs-to-be-done*: forecast, explain, project.

## 5. Proposed architectural rescope (subject to R99 / program-owner sign-off)

This is the major proposed change. **Block I architecture is rescoped:**

### 5.1 Forecast critical path → L3 only

The **baseline forecast service runs on L3 alone** (DFM + ML residual + a small set of large-BVAR or BMA peers if useful). This is where forecast-accuracy V&V (R01 matrix) is evaluated.

This matches the literature: L3 is the forecast workhorse. Stop pretending we'd get better accuracy from L1+L2.

### 5.2 L2 (GVAR) → Scenario Subsystem only

**L2 is invoked only by the Scenario Subsystem (SSDD-006) for spillover IRFs.** It does not feed the baseline forecast. Estimation cadence relaxes from "every quarterly run" to "annually or on-demand" — the spillover structure changes slowly and re-estimation pressure drops.

This is also where R04's compute concerns become much smaller — quarterly cost was driven by quarterly re-estimation, which is no longer required.

### 5.3 L1 (country cores) → Optional per country, Block I = US only

**L1 is reframed as "Narrative Subsystem" — optional per country, US-only at IOC.** Its job is structural identification and shock-story generation for the Scenario Subsystem and for model-card explanations. Forecast contributions are downstream of L3 not L1.

Per-country L1 cores for ≥40 countries was the single biggest engineering cost in the original CONOPS. Dropping to US-only at IOC removes that.

### 5.4 New combiner role

If L3 carries the baseline forecast, the BMA combiner is **combining L3 variants** (e.g., DFM-only, DFM+RF, DFM+gradient-boosted), not three different layers. This is closer to what the density-forecast literature shows works.

### 5.5 Architecture diagram, revised

```
   Data + Vintage (Tier-V: 25 countries)
                  │
                  ▼
          ┌───────────────┐
          │   L3 layer    │  Baseline forecast (DFM + ML variants + BVAR)
          │  (workhorse)  │
          └──────┬────────┘
                 │ density via BMA over L3 variants
                 ▼
         ┌───────────────────────────────────────┐
         │  Forecast Service + Backtest Service  │
         │  (R01 V&V bars apply here)            │
         └───────────────────────────────────────┘

   Scenario request:
   ── Scenario Subsystem ──► L2 GVAR (spillover IRFs, est. annually)
                          ╰► L1 US Core (structural identification, story)

   Wider information surface (R06):
   ── D-MKT, D-SCN, D-GEO, D-MED ──► L3 covariates (T-A)
   ── Term-spread recession-prob endpoint, GPR nowcast (T-B) ──► Situation Subsystem
```

Net layer count for IOC: **L3 (forecast) + L2 (spillover, on-demand) + L1 (US-only narrative) + Situation (R06).** Same SSDD count, very different criticality and cadence.

## 6. Decision implications for CONOPS

| Source | Current | Proposed change |
|---|---|---|
| **CONOPS §1.2** | "Three estimation layers … combined via BMA" | "L3 baseline forecast (BMA over DFM + ML variants). L2 invoked for spillover scenarios. L1 (US-only at IOC) for structural narrative." |
| **CONOPS §5.3.2 CAP-01..05** | Density forecasts at standard horizons | Unchanged but explicitly attributed to L3. |
| **Master-doc §4.1 Logical View** | L3 Model band with L1+L2+L3 | Redrawn with L3 in the critical path; L1/L2 in a sidebar "scenario/narrative" track. |
| **Master-doc §4.4 ADR-005** | "Three-layer hybrid" rationale | Rewrite: "Three layers each serve a distinct job (forecast / spillover / narrative). The forecast critical path is L3 only." |
| **ADR-007 BMA combiner** | BMA over L1+L2+L3 | BMA over L3 variants. |
| **SSDD-003 (L1 country cores)** | "Per-country" | Reframe as "Narrative Subsystem; US only at IOC." Block II+ for additional countries. |
| **SSDD-004 (L2 GVAR)** | Quarterly re-estimation | Annual re-estimation; invoked on-demand for scenarios. |
| **SSDD-005a (Combiner)** | BMA over 3 layers | BMA over L3 variants. |
| **NFR-PRF-003** | 4h quarterly full system run | Relaxed: L3-only quarterly is fast; L1/L2 re-est. is on a different cadence. |
| **LOOP_PLAN Iter 14** | "Per-country equation system" for L1 | Reduced to "US-only country core; spec for adding more in Block II." |

## 7. Counter-argument and when to revisit

The 3-layer hybrid claim could be **strengthened**, not abandoned, if:

- A specific use case appears where L1 narrative is the *product* (e.g., subscriber wants "explain this forecast with a Taylor-rule story"). The Block-II monetization path may justify the L1 cost; private project does not.
- A specific scenario-driven workflow requires *joint* L1+L2 propagation (a structural shock identified in L1 propagating via L2). Defer this to Block II/III when the Scenario Subsystem matures.

For Block I private use: **L3-as-workhorse is the right answer.**

## 8. Bottom line

OPENGEM Block I should be built as an **L3-centered forecasting system** with L1 (US-only) and L2 (annual) as scenario/narrative satellites. The 3-layer story stays in the CONOPS as a *staged ambition*, not as the Block-I architecture.

This change is the largest of any in R01–R06 and is flagged for explicit program-owner sign-off in R99.

---

*End of R03 Rev B.*
