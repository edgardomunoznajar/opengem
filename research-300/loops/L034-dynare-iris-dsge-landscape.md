# L034 — Dynare + IRIS Toolbox: DSGE open-source landscape and OPENGEM fit

**Loop**: 034 / 300
**Phase**: 1 — Open-source landscape survey (DSGE)
**Date**: 2026-06-06
**OPENGEM adoption grade**: **D for Block I, C for Block II** (DSGE is a satellite, not a workhorse)

---

## TL;DR

DSGE — Dynamic Stochastic General Equilibrium — is the workhorse of central-bank policy modeling and the elite sport of modern macro. The open-source landscape is split:

- **Dynare** (MATLAB/Octave/Julia) — the canonical platform since 2001. GPL licensed. **Not Python.** Has a Julia rewrite (Dynare.jl, v0.10.4 as of Oct 2025) that is in active beta, and an older "DynarePython" attempt that the wiki marks abandoned.
- **IRIS Toolbox** (MATLAB-only) — a competing macro toolbox from 2001+, ~98 stars on GitHub, last release June 2023 — semi-dormant.
- **PyMacLab** — Python DSGE library, Apache-2.0, last meaningful update circa 2013–14. Effectively abandoned.
- **Pynare** — Python wrapper around Dynare, last activity 2023, abandoned per maintainer's own README ("no longer under active development").
- **Snowdrop** — newer (2025) Python DSGE package from Goumilevski; JOSS paper; YAML model spec a la Dynare; benchmarks comparable to Dynare/IRIS for "small to medium" models. The most promising pure-Python DSGE option.
- **econpizza** (Boehl, v0.6.9 Nov 2025) — pure-Python heterogeneous-agent (HANK) DSGE solver with JAX backend. Modern, fast, actively maintained. Best-in-class for *nonlinear HANK*.
- **Dolo / Jolo** — Python and Julia compilers for dynamic economic models; smaller scope than Dynare.
- **FRBNY-DSGE.jl** — see L039 (separate loop).

For OPENGEM, this whole class is **D-grade for Block I** (we are not building a DSGE-centric system) and **C-grade for Block II** (a single-country DSGE *might* be a useful satellite for the US scenario layer, but only if we have a concrete need). The R12 reference-systems memo concluded the same thing under "vs. FRB/US, FPAS-II, NiGEM, GEM, EAGLE": these are *all* legitimate macro models; *none* are good fits for a personal-scale, multi-country, open-vintage forecast leaderboard.

If we ever do touch DSGE, the recommendation is **econpizza for HANK** or **Dynare.jl for traditional medium-scale DSGE**. Never re-implement Dynare's solver — too much spec surface, too much Smets-Wouters historical baggage.

## The four DSGE flavors

| Flavor | What it is | OPENGEM fit |
|---|---|---|
| Linearized RBC / Smets-Wouters | The 30-equation workhorses of the 2000s. Solved with first-order perturbation. | Block II satellite, *maybe*. Not better than BVAR for forecast accuracy at our horizons. |
| Medium-scale FRB/US-style | Hundreds of equations, behavioral, calibrated to US data. | No fit. Too US-specific, too maintenance-heavy. |
| Two-asset HANK | Heterogeneous-agent New Keynesian. The post-2018 frontier. | Interesting for inequality / monetary-policy transmission stories. Block III at the earliest. |
| Nonlinear projection-methods | Full nonlinear DSGE without linearization. | Not relevant. Computational cost prohibitive. |

## Dynare (the standard)

- **Lineage**: developed since the late 1990s at CEPREMAP (Paris) by Michel Juillard et al., now an enormous community project across Banque de France, ECB, IMF, US Fed, etc.
- **License**: GPL-3.0 (note: this affects redistribution — see "License compatibility" below).
- **Platforms**: MATLAB, GNU Octave, Julia (Dynare.jl).
- **Strengths**: comprehensive — solving (perturbation 1st/2nd order, projection, perfect-foresight), estimation (MLE + Bayesian + SMC), occasionally-binding constraints, optimal policy, sensitivity analysis. Has thousands of replication packages on `DSGE_mod` (Pfeifer's repo) and similar.
- **Weaknesses**: MATLAB-first means you need a commercial license if you don't want to use Octave (which is slower and has subtle differences). Steep learning curve. .mod file DSL is its own little language.

### Dynare.jl

- **Status**: v0.10.4 as of October 2025. Active. Backed by Banque de France + DSGE-net. Still pre-1.0 — implementing API changes.
- **Coverage**: 18+ Dynare instructions (steady-state, stochastic simulation, estimation, forecast, optimal policy). PARDISO and PATH solvers for hard problems.
- **Maturity**: Beta. Numerical results match Dynare reference for the tests in the suite, but the maintainers explicitly warn about "WORK IN PROGRESS" and known limitations (e.g., purely backward models not yet supported).
- **For OPENGEM**: If we ever do DSGE in Block II, **this is the path**, not the MATLAB original. Julia interop with Python is good (PyJulia, JuliaCall).

## IRIS Toolbox

- **Lineage**: started 2001 (overlapping origin with Dynare), Czech National Bank seed.
- **License**: Apache-2.0.
- **Platform**: MATLAB only. ~98 stars on GitHub, 164 releases, last release June 2023 — momentum has slowed.
- **Coverage**: structural modeling, time-series modeling, data management, reporting. Less DSGE-centric than Dynare; more of a general macro toolbox.
- **For OPENGEM**: The "data management + reporting" pieces are interesting because we have similar concerns, but they're in MATLAB and we are not adopting MATLAB. Snowdrop (below) is essentially "IRIS in Python" with a similar YAML model spec.

## The Python DSGE ecosystem

### Snowdrop (the most promising Python-native)

- Goumilevski (IMF). Published 2025 in JOSS. **Apache-2.0**.
- YAML model spec compatible with Dynare/IRIS users.
- Benchmarks against Dynare and IRIS for small-to-medium models (a few hundred equations) show comparable CPU performance.
- **Status**: Recently launched, low GitHub footprint yet. Worth watching for Block II.

### econpizza (the most promising for HANK)

- Boehl (Bonn). v0.6.9, Nov 2025. Apache-2.0.
- **JAX backend** — automatic differentiation, GPU support, fast Newton iteration for HANK steady states.
- Implements Boehl's 2025 "HANK on Speed" *JET* paper method (sequence-space Jacobian, automatic differentiation).
- Solves nonlinear models with heterogeneous agents (HANK, one and two assets).
- Can find steady state + IRFs in seconds for typical specifications.
- **Status**: Actively maintained, modern dependencies, real users.

### Others (mostly background)

- **PyMacLab**: Apache-2.0, but stuck at 2014-era development. Not the path.
- **Pynare**: Python wrapper around Dynare. Abandoned per maintainer (recommended migration: econpizza for HANK, Dynare.jl for everything else).
- **DynarePython**: archive only. DEAD.
- **Dolo / Jolo**: small-prototype DSGE compilers. Niche.
- **BeforeIT.jl**: agent-based macro, not DSGE per se. Interesting for Block III.

## The OPENGEM decision

We are deliberately a **forecast-leaderboard / nowcast-first** system. DSGE has well-known weaknesses for short-horizon forecast accuracy (it tends to underperform Bayesian VARs in real time). It has well-known strengths for **counterfactual analysis** ("what if the Fed had held at 5.25%?") and **policy scenario modeling**.

Per the rev-C CONOPS, our scenario layer (L1 narrative, L2 BGVAR) does the counterfactual work for us via simpler tools (term-structure shocks, oil shocks, etc.). We do not currently need DSGE.

But two scenarios where DSGE might enter:

1. **Block II: US monetary-policy transmission story.** If a friend / user wants "what does a 50bp cut do to inflation in 8 quarters", BGVAR gives a passable answer; a calibrated DSGE gives a *structural* answer that names channels (intertemporal substitution, real rates, etc.). Worth ~3 weeks of effort to wire up Dynare.jl or econpizza for one US model. The model would be either Smets-Wouters 2007 or one of the public FRB/US-lite specs.

2. **Block III: Inequality / monetary transmission.** If we want to publish "how does CPI vs core CPI shock the bottom-quartile household" stories, HANK is essential. econpizza is the only reasonable Python path.

For both, our adoption is: **call out to a battle-tested external tool, do not build our own solver.** Dynare.jl from Python via JuliaCall, or econpizza directly.

## License compatibility

- Dynare GPL-3.0: Compatible with our use as a callable tool (we shell out to it; we do not link our codebase to its source). If we ever wanted to redistribute a Dynare model file as part of an Apache-2.0-licensed OPENGEM package, we'd need to be careful. **Recommendation**: keep DSGE model files in a separate `models/` directory with explicit GPL-3.0 attribution per-file. Do not commingle.
- Dynare.jl: BSD-style (TBD per repo LICENSE.md). Should be Apache-2.0-compatible.
- econpizza: Apache-2.0. Drop-in compatible.
- Snowdrop: Apache-2.0. Drop-in compatible.
- IRIS: Apache-2.0. Drop-in compatible.
- PyMacLab: Apache-2.0. Drop-in compatible.

## Verdict

**Block I**: D-grade adoption. Do not touch DSGE. Cite it as the "structural" alternative in our methodology pop-ups, but it is not in the build.

**Block II**: C-grade adoption *if* a concrete need arises. Path: Dynare.jl for medium-scale Smets-Wouters-style models; econpizza for HANK. Don't write our own solver.

**Block III**: B-grade for HANK / heterogeneous-agent stories if we want to publish inequality + monetary-policy transmission. econpizza is the path.

**Snowdrop is the watchlist** — if it gains real traction by 2027, it might become the right pure-Python adoption for medium-scale DSGE.

## Citations

- Dynare project: https://www.dynare.org/
- Dynare.jl: https://github.com/DynareJulia/Dynare.jl
- IRIS Toolbox: https://github.com/IRIS-Solutions-Team/IRIS-Toolbox
- Snowdrop (Goumilevski, JOSS 2025): https://joss.theoj.org/papers/10.21105/joss.08197
- econpizza (Boehl): https://github.com/gboehl/econpizza
- "HANK on Speed: Robust Nonlinear Solutions using Automatic Differentiation" (Boehl 2025, *JET*).
- PyMacLab (archived reference): https://pythonhosted.org/pymaclab/
- BasileGrassi/dynare-python (archived reference): https://github.com/BasileGrassi/dynare-python

## Related

- [[L032]] — NY Fed Nowcasting (the forecast workhorse we *are* adopting)
- [[L039]] — Federal Reserve open code (FRBNY-DSGE.jl is the FRBNY half of the DSGE story)
- [[L210]] — Counterfactual scenarios (sanctions hit, oil shock, geopolitical event)
- [[L211]] — Generic shock library (impulse responses)
- R12 — Reference systems (vs. FRB/US, FPAS-II, NiGEM, GEM, EAGLE, BGVAR)
- R14 — L3 architecture (where DSGE deliberately is not)
