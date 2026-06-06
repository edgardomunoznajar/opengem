# R01 — Accuracy Ceiling

| Field | Value |
|---|---|
| Document ID | OG1-RES-001 |
| Revision | B (populated 2026-05-24) |
| Date | 2026-05-24 |
| Status | **Investigated — verdict: H-1 PARTIALLY HOLDS but is the wrong bar; the V&V framework should be redesigned by variable and horizon.** |
| Tests hypothesis | H-1 |

---

## 1. Hypothesis under test (H-1)

> Best-in-class operational forecasts beat AR(1) on ≥75% of country-horizon cells for 4Q-ahead GDP density forecasts. I.e., the OPENGEM v1.0 V&V bar (CONOPS §8.3) is genuinely ambitious — not a layup.

## 2. What the literature actually shows

### 2.1 AR(1) / RW as benchmarks — strength varies sharply by variable

| Variable | Is AR(1) / RW hard to beat? | Reference |
|---|---|---|
| **GDP growth** | **No — AR(1) is generally easy to beat** for point forecasts. Studies routinely show "every model fared better than the AR(1) benchmark, with Random Forest exhibiting the best performance." | [Forecasting US GDP growth in rich data environment, J. Forecasting 2024](https://www.sciencedirect.com/science/article/abs/pii/S1059056024004684) |
| **Inflation (CPI)** | **Yes — naive forecasts are remarkably hard to beat post-1985.** "Judgmental forecasts are remarkably hard to beat." Even atheoretical large-dataset methods are dominated by Greenbook; univariate models lose to both. | [Faust & Wright (2013) Handbook chapter / 2009 paper](https://www.sciencedirect.com/science/article/abs/pii/S016920701300037X) |
| **Inflation post-Great Moderation** | The ability to predict inflation and real activity relative to naive forecasts has **declined remarkably since the mid-1980s**. "Great Moderation predictability paradox." | [D'Agostino, Giannone, Surico (2008)](https://www.ssrn.com/abstract=890990); [D'Agostino, Gambetti, Giannone, J. Applied Econometrics 2013](https://onlinelibrary.wiley.com/doi/abs/10.1002/jae.1257) |
| **Unemployment** | Mixed — AR(1) beatable at short horizons by Phillips-curve-style models; at long horizons, persistence kills most models. | Same Faust-Wright handbook |
| **Policy rate** | Forward rate curve / OIS-implied path is the right benchmark, not AR(1). OPENGEM should not try to beat the curve. | Industry standard |

**Implication for CONOPS §8.3 primary metric.** A 75% win rate vs. AR(1) for *4Q GDP* is **actually a generous bar** — most published models clear it. The bar becomes meaningful only when restated as: vs. AR(1) and RW, AND vs. consensus, AND with density calibration tests, AND broken out by variable.

### 2.2 Specific RMSE benchmarks for GDP growth

From the IMF WEO 2004–17 evaluation ([WP/21/216](https://www.imf.org/-/media/Files/Publications/WP/2021/English/wpiea2021216-print-pdf.ashx)):

| Horizon | Median RMSE, advanced economies (pp of GDP growth) |
|---|---|
| Current-year forecasts | ~0.7 pp |
| Next-year forecasts | ~1.8 pp |

For China (2016 NBER WP 22402): RMSEs at 2y / 3y / 4y ahead = 0.754% / 0.744% / 0.540%.

These are **operational, judgmental, multi-country** benchmarks. OPENGEM's job-to-be-done is to come within these envelopes and ideally narrow them on density.

### 2.3 Density-forecast literature — the harder, more important question

- **Best-calibrated density forecasts** in macro come from **combination methods** — simple equal weighting for output growth, **Bayesian Model Averaging for inflation** ([Rossi & Sekhposyan, IJF 2014](https://www.sciencedirect.com/science/article/abs/pii/S0169207013000460)). This validates OPENGEM's BMA-combiner choice **specifically for inflation density calibration**.
- **PIT uniformity is harder to achieve for inflation than for GDP**: more evidence against PIT uniformity, more serial correlation in second-moment PITs. Inflation density is the hard problem.
- **M6 competition** (2022–2023, financial assets but density-forecasting evidence applies generally): **<25% of teams beat a uniform-probability benchmark.** Top teams clustered within 0.155–0.165 RPS, "almost no differentiation between competitors besides luck" ([Makridakis et al., IJF 2024](https://www.sciencedirect.com/science/article/pii/S0169207024001079)). Density forecasting is unforgiving.

**Implication:** the CONOPS secondary metric ("PIT uniformity at 5% on ≥60% of country-horizon pairs") is **easy for GDP, ambitious for inflation, and very ambitious for inflation with multi-country density combination.** This bar should split by variable.

### 2.4 What judgmental beats — and what we can't replicate

- **Greenbook and SPF** consistently beat univariate, atheoretical, and most theoretical models for inflation. Faust-Wright: "judgmental forecasts are remarkably hard to beat."
- OPENGEM cannot replicate judgmental forecasts (no in-house FOMC). But **Consensus Economics** collects forecasts from >1000 economists across 50+ countries — a per-country vintage of consensus is the natural benchmark and is *paid* but small for personal-use scale ([Consensus Economics Awards](https://www.consensuseconomics.com/cf-2025-forecast-accuracy-award-winners/)).
- Alternative free benchmarks: **IMF WEO** (April / October release, semi-annual vintage), **OECD Economic Outlook** (May / November), **central-bank own forecasts** (Bank of England, ECB, RBA quarterly). All have natural vintages.

## 3. Verdict on H-1

**H-1 as stated partially holds — but is the wrong bar.**

- For **GDP density at 4Q**: beating AR(1) on 75% is *not* ambitious. Most multivariate models do this. As a sole bar, it's weak.
- For **inflation density at 4Q**: beating AR(1) on 75% **is** ambitious (D'Agostino result), and beating consensus is genuinely hard.
- For **unemployment and policy rate**: AR(1) is a strawman; the right benchmark is curve-implied (rates) or labor-flow models (unemployment), not AR(1).

The CONOPS gate as currently written would let OPENGEM pass with a GDP-easy result and dodge the harder bars. **Reframe.**

## 4. Proposed redesigned V&V framework

Replace CONOPS §8.3 single-metric gate with the following matrix. **Each cell is its own bar.** All bars must clear for FOC.

| Variable | Horizon | Primary benchmark | Density bar |
|---|---|---|---|
| **GDP growth** | 1Q | Vs. **RW + AR(1)**: beat both on ≥80% of Tier-V countries by CRPS | PIT KS-test pass at 5% on ≥80% |
| GDP growth | 4Q | Vs. **WEO / OECD EO same-vintage**: not statistically worse (DM p>0.05) on ≥50% of Tier-V countries | PIT pass on ≥70% |
| GDP growth | 8Q | Vs. **WEO same-vintage**: not stat. worse on ≥40% | PIT pass on ≥60% |
| **CPI** | 1Q | Vs. AR(1) **and** vs. naive last-12m-average: beat both by CRPS on ≥65% | PIT pass on ≥60% |
| CPI | 4Q | Vs. **WEO / OECD EO**: not stat. worse on ≥40% | PIT pass on ≥50% |
| **Unemployment** | 1Q | Vs. AR(1): beat on ≥75% | PIT pass on ≥70% |
| Unemployment | 4Q | Vs. WEO: not stat. worse on ≥50% | PIT pass on ≥60% |
| **Policy rate** | 1Q–4Q | Vs. **forward curve / OIS-implied path**: **not stat. worse**. (We don't try to beat the curve.) | N/A at IOC |
| **Term-spread recession probability** (per R06) | 12m | Vs. **SF Fed term-spread model** (Bauer-Mertens replication): AUC ≥ 0.85, not worse than 0.05 below the published model | N/A — calibration via reliability diagram |

This framework forces OPENGEM to defend itself against **the actual hard benchmark for each cell**, not a single weak AR(1) bar.

**Notes on the new framework:**

- It requires WEO and OECD EO same-vintage forecasts. These are *available* (April/October WEO releases; OECD May/November) and can be ingested. Consensus is *paid* and deferred (or skipped for personal-use scope).
- It requires forward-curve / OIS implied paths for the policy-rate gate — already in R06 source list.
- It introduces a Tier-V scope (per R02) so the bars are only evaluated where vintage data exists.

## 5. Decision implications for the CONOPS

| Source | Current text | Proposed change |
|---|---|---|
| **CONOPS §8.3 Primary V&V metric** | "Beat AR(1) on 4Q-ahead GDP RMSE in ≥75% of covered countries AND not statistically worse than consensus (DM p>0.05) in ≥50%" | **Replace** with the matrix in §4 above. Add: gate clears only if ALL non-deferred cells clear. |
| **CONOPS §8.3 Secondary** | "Density forecasts pass PIT uniformity tests at the 5% level for ≥60% of country-horizon pairs" | Replace with cell-specific PIT bars per §4. |
| **POL-10** | "Beat consensus" claims require Diebold-Mariano p<0.05 evidence over ≥8 quarters | Keep, but rename — replace "consensus" (paid, deferred) with "WEO or OECD EO" as primary judgmental benchmarks. Consensus benchmark added later if access becomes feasible. |
| **CONOPS §5.3.2 CAP** | CAP-12 (recession probability, added in R06) | Add explicit V&V bar: "AUC ≥ 0.85 vs. Bauer-Mertens benchmark, ≥10 years of out-of-sample." |
| **Master-doc §8.3** | "Beat AR(1) on 75%" | Same replacement as above. |
| **StRS-005** | "≥3 named benchmarks (consensus, WEO, AR(1))" | Update to "≥4 named benchmarks: AR(1), RW, WEO, OECD EO. Consensus added when access path resolves." |

## 6. Open probes deferred

1. **Consensus Economics access path** — pricing and feasibility for personal-use research scale. Currently in R05's "deferred to public-launch round" bucket, but a one-off historical-data purchase might be tractable. Cost of one country-set archive ≈ $X (TBD).
2. **Bauer-Mertens replication code** — confirm a public reference implementation for the term-spread recession-probability benchmark, so the AUC comparison is uncontestable. Likely already in SF Fed's published code; verify in R05 work.
3. **WEO vintage ingestion** — confirm full WEO release archive is downloadable (April/October PDFs + databases). This is a key benchmark dependency.
4. **PIT-uniformity test family** — choice between KS, Anderson-Darling, Hong-Li tests. Defer to V&V plan (Iter 20 of LOOP_PLAN when it restarts).

## 7. Synthesis with R02 and R06

- **R02 (vintage cliff)**: V&V bars apply only over Tier-V countries (~25 economies). Tier-T countries get a "tracking" view, no leaderboard inclusion at IOC.
- **R06 (wider surface)**: adds two non-macro V&V bars — term-spread recession probability and GPR nowcast (if T-B build proceeds). Each gets its own benchmark and metric.
- **R03 (hybrid evidence — next)**: the V&V framework here assumes the 3-layer hybrid produces a single combined density forecast. If R03 weakens the hybrid case, the bars don't change, but the producing model does.

## 8. Bottom line

The CONOPS bar "beat AR(1) on 75%" is **not the bar that demonstrates OPENGEM is worth running.** It's the bar that demonstrates OPENGEM is not broken. The bar that demonstrates value is **PIT-uniform density forecasts at multiple horizons for inflation (the hardest cell) on a non-trivial country set**, evaluated against operational judgmental benchmarks (WEO/OECD EO). The proposed §4 matrix re-anchors V&V around that meaningful claim.

---

*End of R01 Rev B.*
