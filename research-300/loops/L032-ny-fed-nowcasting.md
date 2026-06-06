# L032 — NY Fed Nowcasting: code release status, statsmodels DFM connection, replication packages

**Loop**: 032 / 300
**Phase**: 1 — Open-source landscape survey (macro forecasting / nowcasting)
**Date**: 2026-06-06
**OPENGEM adoption grade**: **A** (adopt into Block II L3 layer)

---

## TL;DR

The NY Fed Nowcasting code is the **best-documented, most-cited, and most-extensible open-source macroeconomic nowcasting codebase in the world**. It is BSD-3-Clause, lives at `FRBNY-TimeSeriesAnalysis/Nowcasting` (232 stars, 88 forks), implements the Bok–Caratelli–Giannone–Sbordone–Tambalotti (2017) framework as described in NY Fed Staff Report 830, and — critically — has a **first-class native equivalent inside `statsmodels.tsa.statespace.DynamicFactorMQ`** maintained by Chad Fulton, who also wrote the seminal blog post connecting the two.

For OPENGEM, this is a "use the statsmodels port directly" decision. The MATLAB original is the spec; the statsmodels class is the *production* implementation. We don't need to re-implement, we don't need to clone the Python port (which is stale: last commit 2021-02), we don't need to fork. We need to:

1. Read Bok et al. 2017 to understand the spec.
2. Use `DynamicFactorMQ` with our own Tier-V data panel.
3. Add a `news_decomposition` wrapper (data-release impact analysis), which is what makes the NY Fed model special.

This becomes the spine of the L3 workhorse layer (per the rebaselined R03 + R14 memos). It gives us GDP nowcasts for any country with a monthly hard/soft data panel, mixed frequency, missing-data-tolerant, with a built-in attribution to "which data release moved the nowcast." This is a literal A-grade adoption — the only Tier-A pick in this whole batch.

## What the framework does

The NY Fed Nowcasting model is a **Dynamic Factor Model (DFM) for mixed-frequency macroeconomic data**. The math:

- Quarterly target (real GDP growth) + a panel of ~30–40 monthly indicators (PMI, industrial production, payroll employment, retail sales, housing starts, building permits, capacity utilization, hours worked, ISM new orders, consumer confidence, etc.).
- The monthly indicators are modeled as the sum of a small number of latent factors (usually 1 global + maybe 1–2 "blocks" for real/financial/labor) plus idiosyncratic AR(1) noise.
- Quarterly GDP is modeled as a function of monthly aggregates of those factors via a Mariano-Murasawa state-space identity.
- Parameters are estimated by **EM algorithm** (no MCMC — fast, deterministic, scales to large panels).
- The Kalman filter handles missing observations and mixed-frequency seamlessly.

The "news" decomposition (Bańbura & Modugno 2014) is what makes the framework genuinely useful: when a new data release lands, you can decompose the nowcast revision into "how much each released variable contributed to the revision," which is what gets surfaced in the famous weekly NY Fed Nowcast report.

## Code state

The repo at https://github.com/FRBNY-TimeSeriesAnalysis/Nowcasting:

| Field | Value |
|---|---|
| License | BSD-3-Clause |
| Language | MATLAB only (R2015b+) |
| Stars | 232 |
| Forks | 88 |
| Last meaningful commit | 2019-09-26 |
| Issues | Mostly historical |
| Maintenance status | Frozen — but spec-canonical |

The MATLAB code is **frozen** because the NY Fed paused the Nowcast publication in 2021 ("Pausing the Publication of the Nowcast" Liberty Street blog) due to COVID-driven structural breaks invalidating the priors. They restarted in 2024 with a refreshed model (paper forthcoming as of the search date). The 2019 code is still useful as a reference because:

1. The math is unchanged.
2. The structural breaks are a data issue, not a code issue.
3. The statsmodels port (below) is actively maintained and reflects current best practice.

There is a Python translation by MajesticKhan (133 stars, BSD-3) — but the maintainer states up front that they "moved away from time series and started focusing on deep learning" and the repo is stale at 2021-02. **Do not use as a primary dependency.** Useful as a reading aid.

## The statsmodels connection — the actual recommendation

Chad Fulton (NY Fed staff economist, lead author of `statsmodels.tsa.statespace`) wrote a blog post + accompanying notebook titled "Large dynamic factor models, forecasting, and nowcasting" that does three things:

1. Documents `DynamicFactorMQ` — a `statsmodels` class designed *specifically* to be the same framework as the NY Fed Staff Nowcast, "Although they use a different dataset, and update their results weekly, their underlying framework is the same as that used in this notebook."

2. Walks through nowcasting US GDP with a 127-monthly + 1-quarterly panel, including:
   - Specification with factor blocks and ordering
   - Parameter estimation via EM
   - Factor extraction with confidence intervals
   - Forecasting and nowcasting with the news decomposition

3. Provides production-grade code that runs on `statsmodels >= 0.12`, BSD-3-licensed, Python 3, actively maintained.

This is the killer combination: **MATLAB code as the spec, statsmodels as the implementation, the same author bridging the two.**

## What OPENGEM should do

### Block I (now)
- Read Bok et al. (2017) NY Fed Staff Report 830.
- Read Fulton's notebook end-to-end.
- Stand up a 5-line proof-of-concept that runs `DynamicFactorMQ` on our `opengem-vintage` US Tier-V panel for real GDP growth.
- Don't ship it yet — it's the spike that proves the L3 backbone works.

### Block II (next 6 months)
- Build `opengem-l3-dfm` package. Public API: `Nowcast.fit(panel, target)`, `Nowcast.predict(as_of)`, `Nowcast.news_decomposition(release_event)`.
- Run it for each Tier-V country with a reasonable monthly panel. The big-six (US, EU aggregate, UK, Japan, Korea, Canada) get full panels; the rest get smaller panels.
- Surface in dashboard as `/v1/nowcast/{country}/{indicator}` with full provenance: which `statsmodels` version, which panel hash, which model spec hash.

### Block III (out of scope for now)
- Replace EM with VB or full Bayes via PyMC (L036) if EM proves unstable on emerging-market data.
- Extend to inflation nowcast (parallel to Cleveland Fed model — L033).

## What about the data restrictions?

The FRBNY MATLAB code README says "These example files do not exactly reproduce the New York Fed Staff Nowcasting Report released every Friday because data redistribution restrictions prevent us from providing the complete data set used in our model." Translation: **they use Haver and proprietary survey data**. Their *spec* (the model + the news decomposition) is open. Their *inputs* are not.

OPENGEM's advantage: we use upstream-agency public data (BEA, BLS, FRB, Census) per R09's FRED-substitution. We will not match the NY Fed print exactly. We will have a print that is **fully reproducible from public sources**, which is what we promised.

## License compatibility

BSD-3-Clause is compatible with Apache-2.0 (OPENGEM's chosen license) under the OSI matrix. We can:
- Vendor reference code if needed (with attribution).
- Depend on statsmodels (BSD-3) as a regular dependency.
- Cite Bok et al. (2017) and Fulton in our model card.

No license blocker.

## Risks

1. **Statsmodels API drift.** `DynamicFactorMQ` is under `statespace`, which is mature but still gets API-breaking changes between major versions (e.g. parameter ordering for the EM initialization). Pin the version in `pyproject.toml`. Use the same version across all V&V backtests.

2. **EM convergence on small panels.** With Tier-V smaller economies (15–20 monthly indicators), EM can land in local optima. Mitigation: multiple random restarts; warm-start with prior-period parameters.

3. **The NY Fed paused their own model in 2021** because of structural breaks. We need to plan for the same: post-COVID regime indicator, recession-period parameter freeze, etc. (See R10 SSDD-008 — Situation Subsystem already addresses regime classification.)

4. **MATLAB-vs-Python numerical drift.** The statsmodels implementation and the MATLAB reference can produce slightly different numerical results due to differences in optimizer initialization and convergence criteria. For the spec we follow Bok et al., not the reference code byte-for-byte.

## Verdict

**Grade A.** This is the single highest-grade pick from L031–L045. Adopt directly into the L3 layer as `opengem-l3-dfm`, built on `statsmodels.tsa.statespace.DynamicFactorMQ`. Cite Bok et al. (2017) and Fulton. Do not depend on the MATLAB reference repo at runtime; use it only as the canonical spec.

## Citations

- Bok, Brandyn, Daniele Caratelli, Domenico Giannone, Argia M. Sbordone, and Andrea Tambalotti. "Macroeconomic Nowcasting and Forecasting with Big Data." FRBNY Staff Report 830, 2017. https://www.newyorkfed.org/research/staff_reports/sr830.html
- Fulton, Chad. "Large dynamic factor models, forecasting, and nowcasting." http://www.chadfulton.com/topics/statespace_large_dynamic_factor_models.html
- "Opening the Toolbox: The Nowcasting Code on GitHub." Liberty Street Economics, 2018-08. https://libertystreeteconomics.newyorkfed.org/2018/08/opening-the-toolbox-the-nowcasting-code-on-github/
- statsmodels `DynamicFactorMQ`: https://www.statsmodels.org/dev/generated/statsmodels.tsa.statespace.dynamic_factor_mq.DynamicFactorMQ.html
- FRBNY-TimeSeriesAnalysis/Nowcasting (MATLAB, BSD-3, frozen): https://github.com/FRBNY-TimeSeriesAnalysis/Nowcasting
- MajesticKhan/Nowcasting-Python (stale; reading aid only): https://github.com/MajesticKhan/Nowcasting-Python

## Related

- [[L031]] — Atlanta Fed GDPNow (closed-source cousin)
- [[L033]] — Cleveland Fed inflation nowcast (parallel methodology)
- [[L035]] — statsmodels DFM + statsmodels.tsa Bayesian VAR ecosystem (the substrate)
- [[L037]] — Kalman/state-space libs (statsmodels.tsa.statespace is the recommendation)
- [[L039]] — Federal Reserve open code (this is the centerpiece)
- R03 — Hybrid evidence (L3-as-workhorse decision)
- R14 — L3 architecture detail
