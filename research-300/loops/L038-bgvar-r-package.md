# L038 — BGVAR R package + Octave / Python alternatives for cross-country forecasting

**Loop**: 038 / 300
**Phase**: 1 — Open-source landscape survey (Global VAR)
**Date**: 2026-06-06
**OPENGEM adoption grade**: **B** (adopt via rpy2 in Block II — there is no Python equivalent at this maturity)

---

## TL;DR

BGVAR (Boeck, Feldkircher, Huber, *JSS* 2022) is **the best open-source Global VAR / cross-country macro forecasting package**. R-only, GPL-licensed (effectively), `m`BVAR with hierarchical shrinkage priors + stochastic volatility + structural identification, on CRAN, actively maintained as v2.5.8, well-documented.

For OPENGEM's L2 layer (the BGVAR scenario satellite, per R03/R14 architecture), this is the canonical pick. **There is no Python equivalent at the same maturity level.** The Python BVAR ports (`covbayesvar`, `Allisterh/Large-BVAR-Python-codes-`) are single-country, research-grade, not GVAR. The Vienna group around Crespo Cuaresma, Feldkircher, Huber has continuously published GVAR research since the 2010s, and BGVAR is the operational product.

Three integration paths for OPENGEM:

1. **`rpy2` shell-out** — install BGVAR in R, call from `opengem-l2-gvar` Python package via rpy2. Pros: zero re-implementation cost. Cons: R dependency in our toolchain, JSON serialization between languages.
2. **Re-implement in Python** — would take ~2 months, ~3000–5000 LoC, with risk of subtle deviation from the JSS paper. Not worth it.
3. **Bridge model output only** — run BGVAR offline (batch), serialize forecast tensors to JSON / Parquet, consume from Python without runtime dependency. Pros: clean separation. Cons: loses some flexibility.

**Recommendation: option 3 for Block II, option 1 for Block III**. The annual BGVAR run cadence (per the R04 / R14 rebaseline — L2 is annual-cadence by design) makes the offline serialization perfectly acceptable.

## What BGVAR does

BGVAR implements the **Global Vector Autoregression (GVAR)** framework from Pesaran-Schuermann-Weiner (2004), with Bayesian estimation à la Crespo Cuaresma, Feldkircher, Huber (2016).

Architecture:

- One country model per country, each a small BVAR with the country's own variables.
- Each country model also includes **foreign variables** constructed as weighted averages of other countries' variables (trade-weighted, financial-weighted, GDP-weighted, etc).
- The full system is estimated **one country at a time** (single-country BVARs), then stitched together using the international weighting matrices. This is what makes GVAR computationally tractable across 30+ countries.
- Bayesian shrinkage priors (Minnesota, SSVS, Normal-Gamma) regularize the country-level estimation.
- Optional stochastic volatility per country.
- Structural identification via Cholesky, sign restrictions, magnitude restrictions, or external instruments.
- Built-in IRFs, FEVDs, historical decompositions, conditional forecasts.

What this lets you do:

- **Cross-country spillover analysis**: "if US GDP drops 2%, how does Germany's IP move next quarter?"
- **Global shock propagation**: oil shocks, sanctions, monetary-policy synchronization.
- **Long-horizon scenarios**: GVAR is designed for medium-to-long-horizon counterfactuals; forecast horizons of 8–16 quarters are typical.

For OPENGEM, this is **exactly the L2 layer** in the rev-C CONOPS:

- L1 is US narrative satellite (annual). Cite FRB/US or do without.
- L2 is BGVAR (annual cadence, 30+ countries). Adopt BGVAR.
- L3 is the daily-cadence workhorse (DFM + BVAR + ML), per L032 / L035.

## BGVAR code state

| Field | Value |
|---|---|
| CRAN version | 2.5.8 |
| License | GPL-3 (R package default; effectively GPL-3.0-or-later) |
| GitHub | https://github.com/mboeck11/BGVAR |
| Stars | 34 |
| Forks | 23 |
| Activity | Active (CRAN updates as recent as 2024) |
| Language mix | TeX 45% (documentation) / R 44% / C++ 11% |
| Documentation | JSS paper (Boeck, Feldkircher, Huber 2022, 28 pages) + CRAN vignettes + examples |

The C++ component handles the inner loops (SSVS draws, conjugate posterior updates). R wraps everything and exposes the user API.

The R package quality is **high**. Boeck et al. published in *Journal of Statistical Software* (rigorous editorial process). CRAN package compliance means it runs on R 4.0+ on Mac / Linux / Windows.

## Why Python doesn't have an equivalent

The GVAR framework has been operationally important since Pesaran's 2004 paper, but:

- It's MATLAB-first by tradition (the original Pesaran code, the Smith-Galesi GVAR Toolbox were both MATLAB).
- The Bayesian extensions (Crespo Cuaresma et al. 2016, Feldkircher-Huber 2016) were also MATLAB.
- The R port by Boeck et al. is the *first* free-and-open implementation, and was good enough that no one stepped up to do the Python port.
- The Python BVAR community has focused on single-country large BVARs (Crump-Eusepi-Giannone-Qian-Sbordone 2021 → covbayesvar / Allisterh) rather than cross-country GVAR.

If someone shipped a maintained Python BGVAR port (e.g. a wrapper around `BGVAR` via rpy2 with a clean Python API), it would be cited and used. Open opportunity — but not one OPENGEM needs to fill itself.

## Octave / MATLAB heritage

- **GVAR Toolbox** by Smith and Galesi (Cambridge / Pesaran group). MATLAB. Still cited in academic work. Last meaningful update ~2014. Closed (request access).
- **MFE Toolbox** (Sheppard, Oxford). Includes some VAR / GARCH tools that complement GVAR work. Active.
- **BEAR Toolbox** (ECB, L041). Includes Bayesian Panel VAR which is GVAR-adjacent. MATLAB.
- **MEMS** (Mauro, Pesaran). Largely historical.

The Octave/MATLAB world *had* the lead on GVAR for a decade. The BGVAR R package is the modern center of gravity.

## OPENGEM integration plan

### Block I (now)
- Cite BGVAR in R12 (reference systems) and R14 (L3 architecture, where L2 sits adjacent). Done.

### Block II (the actual build)
- Build `opengem-l2-gvar` package. Public API:
  - `BGVAR.fit(panel, weights, lags, prior)` — kicks off an R subprocess via rpy2.
  - `BGVAR.predict(horizon, conditional={...})` — returns a forecast tensor (countries × variables × horizons × posterior draws).
  - `BGVAR.spillover(shock)` — IRF + FEVD for a given structural shock.
- Operational pattern: run **annually** (per R04 compute-budget memo: GVAR is too expensive for daily, makes sense at the WEO / OECD-EO cadence).
- Output goes into our scenario subsystem (L1 satellites use L2 spillover tensors as inputs for the narrative — e.g. "if US tariffs hit Asia, our GVAR says India IP -1.2% over 4Q").

### Block III (out of scope for now)
- If `rpy2` becomes a maintenance burden, evaluate (i) building a clean Python wrapper as a community OSS contribution, or (ii) translating just the parts we need into Python.
- Either way, this is a 1+ FTE-quarter project. Don't do it unless we have to.

## License compatibility

GPL-3 is a copyleft license. If we *link* to BGVAR (call it as a runtime dependency in a binary distribution), our distribution would need to be GPL-3 compatible. But:

- We are **not distributing binaries**. We are distributing source (Apache-2.0).
- We are **not statically linking** — we are calling R via subprocess (rpy2 spawns R).
- The standard interpretation is: subprocess / IPC calls to GPL software do not virally license the caller. (This is the rsync / SSH precedent. The FSF supports this interpretation.)
- Our `opengem-l2-gvar` Python wrapper code is Apache-2.0 and ships separately from the BGVAR R installation.

We should:
- Document in our model card that BGVAR (GPL-3) is a runtime dependency.
- Make BGVAR installation a documented user step, not a bundled binary.
- Cite Boeck et al. (2022) in every BGVAR-derived output.
- Not redistribute BGVAR source.

This is essentially the same posture as a Python project that depends on R via rpy2 today — accepted practice.

## Risks

1. **rpy2 maintenance pain.** rpy2 has historically been finicky on Mac (especially M-series). Mitigation: ship a Docker reference image for our developers; document an `R + rpy2` install script.

2. **R version drift.** BGVAR works on R 4.x. If R 5 introduces breaking changes, BGVAR may lag the release. Mitigation: pin R version in our reproducibility envelope (R16 memo).

3. **Computational cost.** A full BGVAR estimation across 30+ countries with stochastic volatility and SSVS can take hours on a laptop. Per R04, this is acceptable at annual cadence.

4. **GPL-3 audit risk.** If a downstream commercial user wants to embed OPENGEM in a closed-source product, the GPL-3 dependency could be a problem. Mitigation: make BGVAR an *optional* layer behind a feature flag. The dashboard works without L2; L2 just adds the cross-country spillover stories.

5. **Posterior draws JSON serialization.** Each BGVAR run produces gigabytes of posterior tensors. We need a smart serialization: posterior summaries (median + intervals) in JSON, full draws in Parquet, optional, behind a "deep mode" flag.

## Alternatives we evaluated and rejected

- **Translate BGVAR to Python**: 2+ FTE-months. Not worth it for an annual-cadence module. Defer to Block III at the earliest.
- **PyMC hierarchical BVAR across countries**: technically possible (PyMC Labs has a blog post on hierarchical BVAR). But it's not GVAR — it's hierarchical single-country BVAR with cross-country shrinkage, which is different. Useful as a complementary L3 component, not a replacement for L2.
- **Smith-Galesi GVAR Toolbox (MATLAB)**: still cited, but requires MATLAB license. Not aligned with our Apache-2.0 + free-stack ethos.
- **BEAR (ECB MATLAB)**: covers panel BVAR which is adjacent. MATLAB-only. Same problem.

## Verdict

**Grade B**: BGVAR is the right pick for our L2 layer; the rpy2 path keeps it manageable. The grade is not A only because of the GPL-3 and R-runtime cost; in pure-Python terms, the equivalent functionality is not yet available.

## Citations

- Boeck, M., Feldkircher, M., Huber, F. "BGVAR: Bayesian Global Vector Autoregressions with Shrinkage Priors in R." *Journal of Statistical Software* 104(9), 2022, pp. 1–28.
- Crespo Cuaresma, J., Feldkircher, M., Huber, F. "Forecasting with Global Vector Autoregressive Models: A Bayesian Approach." *Journal of Applied Econometrics* 31(7), 2016, pp. 1371–1391.
- Pesaran, Schuermann, Weiner. "Modeling Regional Interdependencies Using a Global Error-Correcting Macroeconometric Model." *Journal of Business & Economic Statistics* 22(2), 2004.
- CRAN BGVAR: https://cran.r-project.org/web/packages/BGVAR/
- GitHub BGVAR: https://github.com/mboeck11/BGVAR
- Dallas Fed WP version: https://www.dallasfed.org/~/media/documents/research/international/wpapers/2020/0395.pdf

## Related

- [[L032]] — NY Fed Nowcasting (L3 workhorse; L2 sits adjacent)
- [[L035]] — statsmodels + BVAR ecosystem (the Python side)
- [[L036]] — PyMC for hierarchical Bayesian extensions
- [[L039]] — Federal Reserve open code (the parallel GPL story for FRB/US)
- [[L041]] — Bank of England + BEAR ECB toolboxes
- R04 — BGVAR compute budget
- R12 — reference systems memo
- R14 — L3 architecture (where L2 BGVAR sits)
