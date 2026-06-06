# L045 — Replication packages catalog: Mercator / SSRN / openICPSR / JASA / OpenReview — what OPENGEM can adopt

**Loop**: 045 / 300
**Phase**: 1 — Open-source landscape survey (replication ecosystem)
**Date**: 2026-06-06
**OPENGEM adoption grade**: **B for the openICPSR + AEA + JASA-ACS catalogs as a pipeline of named-paper replications, C for ad-hoc SSRN/OpenReview**

---

## TL;DR

There are four orthogonal universes of macro-forecasting replication packages:

1. **AEA Data and Code Repository at openICPSR** (`openICPSR/AEA`). The *operational* archive for replication packages tied to AEA journals (AER, AEJ:Macro, AEJ:Applied, etc.). **Since 2019 mandatory pre-publication verification.** Search by paper, download MATLAB / Stata / R / Python / Dynare. Public; free. **Hundreds of macro-forecasting papers** with replication packages.

2. **JASA-ACS** (`github.com/jasa-acs` plus paper-Dataverse). The JASA reproducibility initiative, GitHub-hosted. Awards for reproducibility (Niu et al. 2023, Guerrier et al. 2024). High signal-to-noise but **not macro-forecasting focused** — covers all of statistics.

3. **OpenReview** (ICML / ICLR / NeurIPS). ML conferences. Strong on **time-series foundation models** (TimeGPT, Time-MoE, Timer-XL, Chronos, PatchTST, NHITS). Weak on macro-specific work — most papers benchmark on M4 / M5 / ETTh / weather, not on macro vintages.

4. **SSRN** + **arXiv** + individual-economist sites. The wild west. Mumtaz code page, Cascaldi-Garcia pandemic priors, Allisterh large-BVAR repos. Quality varies wildly. Not a curated catalog.

The "Mercator" in the queue was a misremembered reference. **There is no "Mercator replication package catalog" for macroeconomics.** (MERICS = Mercator Institute for China Studies, a German think tank; Mercator Center at GMU is a policy research center. Neither runs a macro-replication archive.)

**The actionable conclusion**: build OPENGEM's "research adoption pipeline" around **openICPSR + AEA** as the primary source, with **JASA-ACS** as the secondary high-quality filter, and **OpenReview + individual sites** as the bleeding-edge frontier feed. Concretely, we should:

- **Maintain a curated `opengem-research/` directory** with cloned snapshots of ~15–25 high-relevance papers' replication packages.
- For each, write a **methodology card** (what's the model, what's the evidence base, what's the OPENGEM applicability score).
- **Adopt the top 3–5** by writing Python re-implementations in `opengem-l3-variants/` and benchmarking against our `DynamicFactorMQ` baseline.

## openICPSR / AEA pipeline

The AEA Data and Code Repository at openICPSR is the **canonical** archive for macro-forecasting replication packages from AEA journals. Since the 2019 policy revision, replication packages undergo **pre-publication verification** by a dedicated data editor team. This means:

- The code in the archive **runs** (not always; mostly).
- The data **matches** (not always; mostly — proprietary data is the main exception).
- The **README is structured** with a standard template.

This is meaningfully higher signal-to-noise than the open web. For our pipeline:

1. **Query openICPSR for keywords**: nowcast, DFM, BVAR, mixed-frequency, real-time data, forecast combination, scenario analysis.
2. **Filter by year**: 2020+ for most relevance.
3. **Download replication packages** to `opengem/research-300/clones/openicpsr-<id>/`.
4. **Triage**: does the paper's model fit our L3 ensemble? Is the data accessible to us? Does the language match (Python > R > MATLAB > Stata)?
5. **For the top N, write a methodology card + benchmark vs our DFM baseline.**

Recent high-relevance examples:

- **Lenza & Primiceri "How to estimate a VAR after March 2020" (2022)** — pandemic-prior BVAR. Replication code at openICPSR + Cascaldi-Garcia GitHub. Multiple language ports.
- **Crump, Eusepi, Giannone, Qian, Sbordone "A Large Bayesian VAR of the United States Economy" (2021)** — MATLAB, ported to Python in `covbayesvar`.
- **Rossi & Sekhposyan "Macroeconomic Uncertainty Indices Based on Nowcast and Forecast Error Distributions" (2015)** — replication available on openICPSR.
- **Bańbura, Modugno, Giannone, Reichlin "Nowcasting"** family of papers — most have JSS replication packages.

## JASA-ACS pipeline

JASA-ACS is GitHub-hosted. The reproducibility initiative is led by an Associate Editor for Reproducibility. **Code and data required as minimum standard since 2017.** Awards (2023, 2024) recognize exceptional reproducibility.

For OPENGEM:
- **Less macro-specific** than openICPSR. Mostly applied statistics, spatial models, biomedical, ML methodology.
- **Higher reproducibility standard** than openICPSR for the papers that are in scope.
- **Useful for methodology** (state-space innovations, hierarchical Bayesian techniques) rather than direct macro adoption.

Specific repos to watch:

- `jasa-acs/Priors-for-the-Long-Run` (Giannone, Lenza, Primiceri JASA 2019). MATLAB BVAR with long-run priors. 5 stars; small but rigorous.
- Reproducibility-award winners (Niu et al. 2023 on covariate-assisted Bayesian graph learning, Guerrier et al. 2024 on COVID prevalence) — methodology adjacent.

## OpenReview (NeurIPS / ICML / ICLR)

The ML conferences have become the **center of gravity for time-series foundation models** in 2023–2026. Recent landmark papers with code:

- **TimesNet** (Wu et al. ICLR 2023).
- **PatchTST** (Nie et al. ICLR 2023).
- **NHITS** (Challu et al. AAAI 2023).
- **iTransformer** (Liu et al. ICLR 2024).
- **Time-MoE** (ICLR 2025) — 2.4B parameter mixture-of-experts TS model.
- **Timer-XL** (ICLR 2025).
- **Chronos / Chronos-2** (AWS) — pretrained on M4 + various.

For OPENGEM:
- **Most papers benchmark on synthetic / non-macro datasets** (M4, M5, ETTh1/2, electricity, weather). Their wins on these datasets do not always transfer to macro vintages.
- **Code is generally well-organized** (paper-with-code culture is strong in ML).
- **Foundation model approach** is interesting but conflicts with our "every forecast is a named model" principle (L008).
- **Use as inspiration**, not direct adoption. The Nixtla `neuralforecast` library (L044) already wraps several of these models.

The recurring theme: ICLR / NeurIPS papers add 2-5% on M4 with 100x compute. On our macro horizons, this may be a 0-1% gain at the same compute. We pick narrowly.

## SSRN + arXiv + individual sites

The bleeding-edge. Variable quality.

High-quality examples we should track:

- **Cascaldi-Garcia "Pandemic Priors BVAR"** site (`sites.google.com/site/cascaldigarcia/pandemic-priors-bvar`) — multiple language ports of the Lenza-Primiceri pandemic prior. Active.
- **Mumtaz code page** (`sites.google.com/site/hmumtaz77/code`) — Bayesian VAR / TVP-VAR / DFM examples from the BoE CCBS handbook era.
- **Hartwig** BoE / EU Commission research repos.
- **Boehl** (Bonn) — `econpizza` for HANK; `pynare` (archived); `pydsge` family.
- **Chad Fulton** blog (`chadfulton.com`) — state-space examples in statsmodels.

Lower-quality / proceed-with-care:

- Many GitHub "replication" repos at 3–10 stars are unmaintained student work. Read the README; check the test suite; usually not for adoption.

## The OPENGEM "research adoption pipeline"

A repeatable process:

1. **Identify**. Quarterly scan of:
   - openICPSR new replication packages tagged with our keywords.
   - JASA-ACS award winners + new ACS papers in our area.
   - ICLR/ICML/NeurIPS new time-series papers (filter by "macro" / "economic" / "GDP" / "inflation" in title).
   - Track 3-4 active economists (Mumtaz, Cascaldi-Garcia, Boehl, Giannone) for new code releases.

2. **Triage**. For each, score:
   - **Relevance** (0–5): does it address something in our L3 layer?
   - **Quality** (0–5): does the code run? Tests pass? Documentation OK?
   - **Cost** (0–5): how much effort to port to our stack?
   - **License** (binary): compatible with Apache-2.0 distribution?

3. **Clone**. For score-15+, clone to `opengem/research-300/clones/<slug>/`.

4. **Reproduce**. Run it on our infra. Confirm we can match the published numbers within rounding.

5. **Port**. If we adopt, write Python that lives in `opengem-l3-variants/` with model card + V&V benchmark.

6. **Cite**. Every adoption gets full citation in the model card.

This pipeline lives in `opengem/research-300/synthesis/` (synthesis directory already exists in our queue structure).

## OPENGEM's mandatory replication priorities

If we want to maximize Block II forecasting quality, here's the priority queue:

1. **Bok et al. 2017 NY Fed DFM** — already adopted via statsmodels (L032).
2. **Knotek-Zaman 2017 + 2024 Cleveland Fed inflation** — Block II (L033).
3. **Crump-Eusepi-Giannone-Qian-Sbordone 2021 Large BVAR US** — Block II via PyMC or covbayesvar.
4. **Lenza-Primiceri 2022 pandemic priors** — Block II via PyMC, layered on top of #3.
5. **Giannone-Lenza-Primiceri 2015 hierarchical priors** — Block II via R `bvar` or PyMC.
6. **Boehl 2025 HANK on Speed** — Block III if we ever want HANK (via econpizza, L034).
7. **Pesaran-Schuermann-Weiner 2004 GVAR + Crespo Cuaresma et al. 2016 Bayesian extensions** — Block II via BGVAR R + rpy2 (L038).

These 7 papers + their replication packages cover ~80% of the L3 layer's intellectual content. Worth maintaining canonical, vintaged, Python-readable copies in `clones/`.

## License compatibility

Replication packages have heterogeneous licenses:

- **openICPSR**: per-paper license, usually "Custom" with academic citation. We don't redistribute the package; we re-implement in our own code with attribution.
- **JASA-ACS GitHub**: usually MIT or "academic use only." Same posture.
- **OpenReview code**: usually MIT or Apache-2.0 (ML conferences are permissive).
- **Individual researcher sites**: per-page license, often vague. "Use of code for research purposes is permitted with proper reference" is common.

Our posture for **all** of these: **re-implement, cite, do not redistribute.** Our `opengem-l3-variants/` is Apache-2.0. Their papers + replication packages are credited in our model cards.

## Risks

1. **Adoption velocity**. Hundreds of new macro-forecasting papers per year. We can't track them all. Mitigation: focus on the 3–4 economists we already follow + quarterly batch search; accept missing 10–20% of frontier.

2. **Verification effort**. Just confirming a replication package matches published results takes 1–3 days. For 20+ packages a year, that's a sizable chunk of effort. Mitigation: only fully reproduce the ones we want to adopt; partial-verification (read README, run smoke test) for the rest.

3. **Reproducibility crisis is real**. ~40% of empirical economics papers don't replicate cleanly even with the AEA verification. Pick papers from authors with track records.

4. **MATLAB / Stata barrier**. Most macro replications are MATLAB / Stata. Translation effort. Mitigation: keep MATLAB / Octave / Stata in our reference Docker image; use MATLAB only for "verify this reproduces" and re-implement in Python for our codebase.

5. **License creep on openICPSR**. The AEA could tighten replication terms in the future. Mitigation: snapshot what we use; keep our re-implementations clean of the original code.

## Verdict

**Grade B** for the openICPSR + AEA + JASA-ACS *pipeline*. The pipeline itself is high-value; specific adoptions are project-by-project.

**Grade C** for ad-hoc SSRN / OpenReview frontier. Useful for ideation; rarely direct adoption.

**Grade D** for the imaginary "Mercator catalog" — doesn't exist.

## Citations

- openICPSR / AEA Data and Code Repository: https://www.openicpsr.org/openicpsr/searchstudies?searchableId=true&keyWord=&institution=AEA
- AEA Data and Code Availability Policy: https://www.aeaweb.org/journals/data/data-code-policy
- JASA-ACS GitHub: https://github.com/jasa-acs
- JASA Reproducibility Guide: https://jasa-acs.github.io/repro-guide/
- JASA Reproducibility Award: https://jasa-acs.github.io/repro-award/
- Cascaldi-Garcia Pandemic Priors: https://sites.google.com/site/cascaldigarcia/pandemic-priors-bvar
- Mumtaz code page: https://sites.google.com/site/hmumtaz77/code
- Boehl GitHub: https://github.com/gboehl
- OpenReview ICLR: https://openreview.net/group?id=ICLR.cc
- OpenReview ICML: https://openreview.net/group?id=ICML.cc
- `jasa-acs/Priors-for-the-Long-Run`: https://github.com/jasa-acs/Priors-for-the-Long-Run

## Related

- [[L032]] — NY Fed Nowcasting (top priority replication)
- [[L033]] — Cleveland Fed inflation (priority #2)
- [[L035]] — statsmodels + BVAR ecosystem (where these get implemented)
- [[L036]] — PyMC (the porting substrate)
- [[L038]] — BGVAR (the cross-country reference)
- R16 — Reproducibility architecture (this loop is the *input* side; R16 is the *output* side)
