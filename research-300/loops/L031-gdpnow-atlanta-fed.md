# L031 — Atlanta Fed GDPNow: methodology, code status, replication viability

**Loop**: 031 / 300
**Phase**: 1 — Open-source landscape survey (macro forecasting / nowcasting)
**Date**: 2026-06-06
**OPENGEM adoption grade**: **C** (cite, partially adapt; do not adopt wholesale)

---

## TL;DR

GDPNow is the most-watched US GDP nowcast — published since 2014, updated daily-ish, FRED series `GDPNOW` — and it is the **closest thing in macroeconomics to an open-source forecasting model that is not actually open source**. The Atlanta Fed publishes the working paper (Higgins 2014), a modifications log, and a live Excel workbook with every input and every intermediate factor. They do **not** publish the source code, and the FAQ says so plainly.

For OPENGEM, this means: cite the methodology, replicate the architecture in Python from the paper + Excel cells, but do **not** depend on GDPNow as a runtime. The Atlanta Fed reserves the right to modify the model without notice (and frequently does — see "Modifications.pdf"). A re-implementation that ships in our repo and runs on our data is the only defensible path. The Excel workbook is enough to bootstrap the re-implementation in 2–3 weeks of focused effort. Expect to get within ~0.2pp of the live print after one quarter of vintage tuning.

## Methodology in one paragraph

GDPNow is a **bridge-equation system** with a small dynamic factor model (DFM) feeding the bridge equations to fill in not-yet-released monthly source data for the GDP subcomponents (PCE goods, PCE services, equipment, structures, IP, exports, imports, government, change in private inventories). The DFM extracts a single latent factor from a ~13-variable monthly panel. The subcomponent forecasts are then aggregated bottom-up to a real GDP growth nowcast using BEA's chained-dollar formula. Higgins (2014) writes every equation; subsequent modifications (~30 since 2014, all logged) tweak the variable panel, deal with seasonal-adjustment shocks, and add the "alternative model average" that GDPNow now publishes alongside the headline.

The model is **deliberately mechanical**. There is no judgmental override, no Greenbook-style smoothing, no Bayesian shrinkage on the bridge coefficients. This is its strength as an open benchmark — the only inputs are public data, the only knobs are public, the model card is essentially Higgins (2014) + the Modifications.pdf — and its weakness as a forecast (it whips around with every ISM and retail-sales print).

## What is open vs. closed

| Artifact | Available? | Format | License |
|---|---|---|---|
| Working paper (Higgins 2014, WP 2014-7) | ✅ | PDF | Public domain (US federal work) |
| Modifications log | ✅ | PDF | Public domain |
| Excel workbook with every input + intermediate factor | ✅ | XLSX (refreshed each release) | "Provided as a service"; no explicit ToS |
| Source code | ❌ | — | — |
| Vintage history of forecasts | ✅ | ALFRED has `GDPNOW` vintage series | FRED ToS (no caching, no derivative datasets) |
| Latent factor time series | ✅ | In the Excel workbook | Same |

The FAQ ("Will the source code be made available?") answers in the negative: "The Atlanta Fed is not planning to release the source code for GDPNow at this time. However, sufficient detail is provided in the working paper and supporting documents for interested users to construct their own version of the model." Translation: replicate or pay nothing.

## Open re-implementations on GitHub

A search of GitHub for "GDPNow" surfaces:

- **No canonical Python port** with significant stars or active maintenance.
- A handful of educational notebooks (e.g. Brian Curry's "Inside GDPNow" Medium series, 2026, includes code) that get ~80% of the way but skip the alternative-model-average and the seasonal-adjustment fix-ups.
- The MajesticKhan/Nowcasting-Python repo (133 stars, BSD-3, last touched 2021-02) is the NY Fed model, **not** GDPNow — different architecture (single DFM, EM-estimated) vs. GDPNow's bridge-equation aggregation.
- GDPNow has been *informally* reverse-engineered inside hedge funds and bank research desks since 2015; none have published. That tells you the moat is small but the work is real.

So the answer to "is there a Python GDPNow we can just import?" is **no**. The answer to "could we ship one in three weeks?" is **yes**, and the case for doing so is below.

## OPENGEM angle: should we replicate?

There are three options:

1. **Cite-only** (D grade). Show GDPNow's print on the US country page, link to the Atlanta Fed page, do not depend on it. Cheapest. Useful for the dashboard's "consensus overlay" feature (L190).

2. **Excel scrape + republish** (C grade). Pull the Atlanta Fed's Excel workbook nightly, parse the latent factor + subcomponent forecasts, surface them on the dashboard as a tracked third-party forecast. Cheap to build, but the Excel format changes when the Atlanta Fed modifies the model — we'd have a parser break every 6–12 months. Also, ALFRED has it as a series anyway, so the only added value is the subcomponent decomposition.

3. **Full Python re-implementation** (B grade if done well, C grade as a side project). Code up Higgins (2014) + Modifications.pdf on top of `statsmodels.tsa.statespace.DynamicFactorMQ` (the same factor backbone the NY Fed code uses), with bridge equations as simple OLS regressions, and aggregation via BEA chained-dollar formula. Ship as `opengem-gdpnow`. The asymmetry is real: our re-implementation can be tagged, vintaged, and backtested in the same V&V matrix as everything else; their model cannot. This is exactly the "publishes its mistakes" play.

**Recommendation**: Option 1 at IOC. Option 3 at FOC (Block II), tagged as `opengem-us-gdp-nowcast`, with explicit "tracks the Higgins (2014) methodology, modifications log followed through release X" provenance. Do not promise GDPNow-equivalent print; promise vintage-correct, reproducible, opinionated.

## What it teaches us, even if we don't replicate

1. **Bridge equations are powerful and simple.** Each subcomponent of GDP is a regression on a small set of monthly source series with deliberately ugly variable selection (it's all "what does BEA actually use to compute this"). This is the right pattern for a *country-specific* US nowcast that explains itself.

2. **DFM-as-filler.** The DFM's job is *not* to forecast GDP. It's to fill in the missing-data cells of the monthly panel so the bridge equations can run. This is a usefully narrow application of factor models — DFM as imputation, not as model — and it's much easier to defend than DFM-as-direct-forecaster.

3. **Publish the inputs.** The Excel workbook is the model card. We should match that and *exceed* it by publishing JSON every cycle.

4. **Daily cadence is feasible for nowcast publication.** The Atlanta Fed publishes ~6–7 times a month. We can match that easily.

## Risks of replication

- **Drift from official print.** Even a perfect re-implementation of the 2014 paper will diverge from the live GDPNow once a few modifications are made. We'd need a "tracking confidence" signal that says how recent our last sync was.
- **Haver dependency.** GDPNow uses some Haver-licensed series (e.g. ATL Fed business-survey series). For our open re-implementation, we either substitute with BLS / Census public series (small accuracy loss) or accept the gap. The R09 FRED-substitution memo already takes the substitution path.
- **Seasonal-adjustment shocks.** The Modifications log shows the model gets repeatedly patched after big SA revisions. A maintained replication carries ongoing maintenance.

## Verdict

**Grade C** for direct adoption — the code is closed, the model drifts, the Haver dependency is a minor headache. **Grade B** for the *methodology pattern* (bridge equations + DFM-as-imputer) which OPENGEM should adopt as its US GDP nowcast architecture. Replicate in Block II, not Block I.

## Citations

- Higgins, Patrick. "GDPNow: A Model for GDP 'Nowcasting'." Federal Reserve Bank of Atlanta Working Paper 2014-7, July 2014. [FRASER link](https://fraser.stlouisfed.org/title/working-papers-federal-reserve-bank-atlanta-8586/gdpnow-657082).
- "Atlanta Fed GDPNow" page: https://www.atlantafed.org/cqer/research/gdpnow
- "What Is GDPNow?" explainer: https://www.atlantafed.org/research-and-data/data/gdpnow/explainer
- FRED series `GDPNOW`: https://fred.stlouisfed.org/series/GDPNOW

## Related

- [[L032]] — NY Fed Nowcasting (the open-source DFM cousin, BSD-licensed)
- [[L033]] — Cleveland Fed inflation nowcast (open, daily, also closed-source but Excel-published)
- [[L168]] — GDP nowcast tile in the dashboard
- [[L190]] — Consensus comparison (where GDPNow lives as overlay)
