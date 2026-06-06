# L039 — Federal Reserve open code: catalog, relevance scores, FRBNY-DSGE.jl, FRBNY-Nowcasting, FRB/US in Python

**Loop**: 039 / 300
**Phase**: 1 — Open-source landscape survey (Fed system)
**Date**: 2026-06-06
**OPENGEM adoption grade**: **A for FRBNY-Nowcasting (via statsmodels), B for FRB/US Python, C for FRBNY-DSGE.jl, D for everything else**

---

## TL;DR

The Federal Reserve System publishes a **lot** of open code, but it's scattered across at least 6 GitHub orgs (`FRBNY-DSGE`, `FRBNY-TimeSeriesAnalysis`, `Research-Division` for Atlanta, `bank-of-england`-but-that's-a-different-country, plus per-economist repos). Plus the Federal Reserve Board (Washington) ships **PyFRB/US** as a downloadable ZIP — not on GitHub — and the **EDO Dynare** model files as a downloadable ZIP. None of the Fed *banks* maintains a clean, top-level "official Fed code" portal.

Here is the **comprehensive catalog with relevance scores for OPENGEM**:

| Repo / Package | Maintainer | License | Stars | Last update | OPENGEM relevance | Grade |
|---|---|---|---|---|---|---|
| `FRBNY-TimeSeriesAnalysis/Nowcasting` (MATLAB) | NY Fed | BSD-3 | 232 | 2019-09 | Spec for L3 DFM; we adopt via `statsmodels.DynamicFactorMQ` | **A** |
| `statsmodels.tsa.statespace.DynamicFactorMQ` | Chad Fulton (NY Fed) + community | BSD-3 | (in statsmodels 10K+) | active | Production L3 backbone | **A** |
| `FRBNY-DSGE/DSGE.jl` | NY Fed + QuantEcon | BSD-3 | 947 | v0.8.0 Dec 2025 | Optional DSGE in Block II; Julia | **C** |
| `FRBNY-DSGE/StateSpaceRoutines.jl` | NY Fed | BSD-3 | 89 | active | Supporting lib for DSGE.jl | **C** |
| `FRBNY-DSGE/SMC.jl` | NY Fed | BSD-3 | 75 | active | Sequential Monte Carlo (DSGE estimation) | **C** |
| `FRBNY-DSGE/SSJ.jl` | NY Fed | BSD-3 | — | active | Sequence-Space Jacobian (HANK) | **C** |
| `FRBNY-DSGE/Estimating_HANK` | NY Fed | BSD-3 | — | 2023 | HANK estimation replication | **C** |
| `FRBNY-DSGE/rstarBrookings2017` | NY Fed | BSD-3 | — | 2017 | r-star paper replication | **D** |
| `FRBNY-DSGE/rstarGlobal-18countries` | NY Fed | BSD-3 | — | — | r-star across 18 countries | **D** |
| `Research-Division` (Atlanta Fed) | Atlanta Fed Research | (varies) | — | — | Only 2 repos, no flagship model | **D** |
| **PyFRB/US** (downloadable ZIP) | FRB Board (Washington) | Public-domain US govt work | (not on GitHub) | Feb 2026 | The actual FRB/US model in Python | **B** |
| **EDO Dynare model package** | FRB Board | Public-domain | (downloadable) | recent | Smets-Wouters-like DSGE for US | **C** |
| `bank-of-england/forecast_evaluation` | BoE | (not Fed, but) | 25 | active | Forecast evaluation package | (L041) |

The two FRBNY orgs are the most interesting because they actively publish working code with permissive licenses. The Atlanta Research-Division has surprisingly little (despite Atlanta running GDPNow and the Wage Growth Tracker — both of which are deliberately not open-sourced per the FAQ). St. Louis is FRED-centric — their open code is API clients and dashboards, not models. Cleveland publishes the inflation nowcast as a daily Excel, no code repo. Boston, Chicago, KC, Dallas, Minneapolis, SF, Philadelphia — varied, ad-hoc, individual-economist repos.

## PyFRB/US — the surprising winner

The Federal Reserve Board's flagship US macro model, FRB/US, was **ported to Python in 2022** and is updated continuously. As of May 2026:

- **Python 3 only** (Py2 incompatible — modern Python stack).
- **Last update**: Python package Feb 2026; data package May 2026.
- **Distribution**: downloadable ZIP from federalreserve.gov/econres/us-models-python.htm.
- **License**: US Federal works are not copyrightable (effectively public domain). No GPL, no Apache, no anything — just public domain. **This is the most permissive license possible.**
- **Coverage**: full FRB/US model — hundreds of equations, behavioral, calibrated to US data, with simulation programs, demo programs, technical HTML documentation.

For OPENGEM:

- **A US scenario engine that can answer "if the Fed had held at 5.25% through 2024Q4, what would CPI have been?" is a *very* compelling Block II feature.**
- The Python distribution makes integration *much* easier than it would be in EViews.
- But: FRB/US is a *big* model (hundreds of equations, behavioral). Maintenance burden is non-trivial. We probably want to wrap it behind a clean API and only expose ~5–10 well-curated scenarios.
- The Board updates the model and data quarterly. We'd want an "FRB/US sync" job to pull updates.

**Recommendation**: Block II, B-grade adoption. Build `opengem-fbus-scenarios` package that wraps PyFRB/US for a handful of well-defined counterfactuals (oil shock, FFR shock, tariff shock). Do not expose the full FRB/US API to users; expose the curated scenarios.

## FRBNY-DSGE.jl — the Julia situation

The FRBNY-DSGE org has matured into a serious **Julia-only ecosystem**:

- 11 active repos.
- The flagship `DSGE.jl` (947 stars, BSD-3, v0.8.0 Dec 2025) is the canonical Julia DSGE engine.
- Supported by registered companion packages: `StateSpaceRoutines.jl`, `SMC.jl`, `ModelConstructors.jl`.
- New focus on HANK: `Estimating_HANK` (2023 paper), `HANK_Tradeoffs_Paper` (2025), `SSJ.jl` for sequence-space Jacobian.

For OPENGEM:

- We are not a Julia shop.
- The Python ↔ Julia bridge (`PyJulia`, `juliacall`) works but adds complexity.
- The Block II value is roughly the same as PyFRB/US for US scenarios, but PyFRB/US is *already Python* and FRBNY-DSGE.jl is not.
- If we ever want HANK (heterogeneous-agent New Keynesian, for inequality stories), the FRBNY-DSGE HANK code is the most authoritative reference. But for a Python-first adoption path, we'd prefer `econpizza` (Boehl, L034).

**Recommendation**: C-grade. Cite the work. Maybe wire up `juliacall` for a one-off scenario in Block III if a user asks. Don't make Julia a runtime dependency.

## FRBNY-Nowcasting — already covered (L032)

This is the AAA-grade pick. See L032. The MATLAB code is the spec; `statsmodels.DynamicFactorMQ` is the implementation; we adopt the implementation.

## The other Fed banks

| Bank | Notable open code | OPENGEM relevance |
|---|---|---|
| Atlanta | GDPNow (closed), Wage Growth Tracker (closed), 2 small Research-Division repos | Cite GDPNow + WGT in dashboard; D-grade direct adoption |
| Boston | Project Hamilton (CBDC, with MIT DCI) | Out of scope for macro forecasting |
| Chicago | scattered individual-economist repos | Cherry-pick if useful |
| Cleveland | Inflation nowcast (closed, daily Excel) | Cite + replicate per L033 |
| Dallas | Dallas Fed Trimmed Mean PCE (open data) | Use the data feed; no code |
| KC | Beige Book Sentiment Index (open data) | Use the data |
| Minneapolis | Manuel Amador's sovereign debt repos | Niche; out of scope |
| NY | FRBNY-DSGE.jl + FRBNY-Nowcasting | See above |
| Philadelphia | Survey of Professional Forecasters (open data) | Use the data feed (parallel to ECB SPF, L043) |
| Richmond | scattered econometrics tools | Cherry-pick |
| SF | DSGE updates, individual researcher repos | Cherry-pick |
| St. Louis | FRED + ALFRED (data, with restrictive ToS per R09) | Use ALFRED for vintage discovery only |

The Philadelphia Fed's SPF data is the US analog to ECB SPF (L043) — open-data, downloadable CSVs, no license blocker. **We should adopt the Philly Fed SPF as a consensus overlay on the US dashboard.**

## Risks

1. **License non-uniformity.** US Federal works are technically not copyrightable, but Fed banks (NY, Atlanta etc.) are *technically* private corporations operating under federal charter. Their explicit licenses (BSD-3 for FRBNY repos) clarify this. PyFRB/US is FRB Board (a federal agency) so it's public domain.

2. **Model drift.** PyFRB/US and FRBNY-DSGE.jl are updated continuously. We need an "upstream sync" cadence per package. Quarterly for FRB/US, occasional for DSGE.jl.

3. **Documentation friction.** PyFRB/US ships HTML docs; FRBNY-DSGE.jl ships Julia-style docs. We need to translate both into our model-card format.

4. **No support contract.** These are research codebases. If something breaks at month-end, we file an issue and hope. Mitigation: vendor a known-good snapshot.

5. **Atlanta's reluctance.** Atlanta Fed is the most public-facing of the regional banks on forecasting (GDPNow, Wage Growth Tracker) but is also the most resistant to open-sourcing their code. We accept this and replicate the methodology ourselves (per L031, L033).

## Verdict

- **Grade A for FRBNY-Nowcasting → statsmodels.DynamicFactorMQ** (already covered L032).
- **Grade B for PyFRB/US** as a Block II curated-scenario wrapper.
- **Grade C for FRBNY-DSGE.jl** as a watch / cite item.
- **Grade D for the bulk of other Fed bank repos** — niche or stale.
- **Grade A for the Philly Fed SPF data feed** (not code, but worth noting here for completeness).

The catalog is wider than people realize. The *truly load-bearing* adoptions are still only two: FRBNY-Nowcasting and PyFRB/US.

## Citations

- FRBNY-DSGE org: https://github.com/FRBNY-DSGE
- FRBNY-TimeSeriesAnalysis org: https://github.com/FRBNY-TimeSeriesAnalysis
- DSGE.jl: https://github.com/FRBNY-DSGE/DSGE.jl
- PyFRB/US: https://www.federalreserve.gov/econres/us-models-python.htm
- EDO Model package: https://www.federalreserve.gov/econres/edo-model-package.htm
- Atlanta Research Division: https://github.com/Research-Division
- Philly Fed SPF: https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/survey-of-professional-forecasters

## Related

- [[L031]] — Atlanta GDPNow (closed-source)
- [[L032]] — NY Fed Nowcasting (the AAA pick)
- [[L033]] — Cleveland Fed Inflation Nowcast
- [[L034]] — Dynare + IRIS landscape (EDO Dynare uses Dynare)
- [[L038]] — BGVAR (the cross-country complement)
- [[L043]] — ECB SPF (parallel to Philly Fed SPF)
- R12 — Reference systems
