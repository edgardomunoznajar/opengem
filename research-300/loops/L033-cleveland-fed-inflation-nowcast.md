# L033 — Cleveland Fed inflation nowcast / Now-Casting.com style: methodology and replications

**Loop**: 033 / 300
**Phase**: 1 — Open-source landscape survey (macro forecasting / nowcasting)
**Date**: 2026-06-06
**OPENGEM adoption grade**: **B** (adopt the methodology, replicate as `opengem-l3-inflation-nowcast`; cite the Cleveland Fed print)

---

## TL;DR

There are **two distinct things** the queue lumps together:

1. **Cleveland Fed Inflation Nowcasting** — a public, daily, free-to-view CPI / PCE inflation nowcast. Methodology paper (Knotek & Zaman 2017) has a JMCB replication archive in MATLAB. Code not on GitHub but available via OSU's JMCB repository. The model is small, mechanical, and re-implementable in one weekend.

2. **Now-Casting.com** — a UK-incorporated commercial service founded by Lucrezia Reichlin and Domenico Giannone in 2011. **Paid subscription only.** Covers 34 economies. They are the *commercial* version of the Bok et al. (2017) NY Fed framework (L032). No code is published; the framework they use is the same one that powers `statsmodels.DynamicFactorMQ`.

For OPENGEM, the Cleveland Fed model is **a B-grade adopt** — methodology is small enough to replicate in Python in a focused sprint, the inputs (oil price, gasoline price, monthly CPI/PCE) are all on free-to-access feeds we already partially adapt (FRB, EIA), and the dashboard would be much more credible with a US inflation nowcast tile than without one.

Now-Casting.com is **a C-grade** "cite, don't depend." It's a competitor to OPENGEM's hosted offering. Their model is closed-source. Reichlin and Giannone are the academic foundation we already build on via the NY Fed / DFM track. We do not need a separate dependency on them.

## Cleveland Fed inflation nowcast — what the model does

Knotek and Zaman (2017) in *JMCB* describe a "deterministic model switching" (DMS) system that picks among a small set of candidate models depending on which data has been released so far in the current month. The components:

1. **Core inflation** — nowcast based on the average reading over the prior 12 months (a deliberately simple core-trend anchor).
2. **Food inflation** — same approach as core; trend-anchored.
3. **Gasoline price inflation** — combination of current weekly gasoline prices (EIA) and daily oil prices (NYMEX WTI / Brent), in essence translating the oil-to-gas pass-through into a gasoline CPI nowcast.
4. **All-items** = weighted aggregation of core + food + energy components, using BLS CPI relative-importance weights.
5. **Special-case logic** — there are several heuristics for handling things like the seasonal-adjustment of gasoline prices, the within-month sequence of CPI vs PCE releases, and the "stale-data" backup when a release is delayed.

The model has been live since circa 2010 and updates **daily**, including weekends. The Knotek-Zaman (2024) refresh paper (FRB Cleveland WP 24-06, "Nowcasting Inflation") generalizes the framework with more variables, more frequencies, and a deterministic-model-averaging twist.

The **2023 economic commentary** by Higgins et al. ("A Real-Time Assessment of Inflation Nowcasting at the Cleveland Fed") provides the public scorecard: median absolute error of ~0.08–0.12 percentage points on the headline CPI on the day-of-release, beating Bloomberg consensus by a meaningful margin and matching survey medians for PCE.

## Open replications and replication packages

- **JMCB replication archive**: Knotek & Zaman (2017) MATLAB + data archive lives at the Journal of Money, Credit and Banking data repository (hosted on OSU's economics website). Public download; CC-BY-equivalent academic norm. This is the canonical reference for replicating the original 2017 model. (The 2024 refresh paper has its own replication package via FRB Cleveland's working-paper portal.)
- **No mainstream Python port** on GitHub as of search date. A few educational notebooks (e.g. the InflaBERT 2024 ML extension at `paultltc/InflaBERT`) cite the model and use it as a benchmark, but do not replicate it.
- **Cleveland Fed public Excel** — the daily nowcasts for CPI, PCE, core, and headline are all published as an Excel-downloadable history on the Cleveland Fed inflation-nowcasting page. The history goes back to circa 2010.
- **RATS replication thread** — the Estima RATS forum has a multi-year thread of practitioner replications and gotchas, useful as a knowledge base if we hit numerical drift during our own replication.

## Now-Casting.com — the commercial offering

Now-Casting Economics Ltd is a UK-registered company founded in 2011 by Reichlin (LBS) and Giannone (then NY Fed, now ECB). They sell their proprietary, continuously-updated nowcast feed to "asset managers, hedge funds, and banks" and also to central banks. Coverage: 34 economies, ~85% of world GDP. Underlying methodology is the Bańbura-Giannone-Modugno-Reichlin "now-casting and the real-time data flow" DFM framework — the same family that the NY Fed code (L032) reimplements.

Subscription is annual and (from publicly-available pricing references) appears to be in the low-five-figures USD/year range per institutional seat. **No public code, no public data feed.**

For OPENGEM:
- They are a direct competitor at the dashboard layer (premium inflation/GDP nowcasts for institutional buyers).
- Their existence is a useful market validation: there are buyers for "high-quality multi-country nowcasts" who pay real money.
- Our positioning: open + free + vintaged + accountable. We are not trying to be a paid feed; we are trying to be the public-benchmark substrate.

## OPENGEM adoption plan

### Block I (immediate, in-scope)
- **Cite Cleveland Fed prints** on the US inflation page (parallel to the GDPNow citation on the GDP page).
- Read Knotek & Zaman (2017) + (2024). The math is short.

### Block II (the actual build)
- Implement `opengem-l3-inflation-nowcast` per Knotek & Zaman (2017), pure Python, no MATLAB dependency.
- Inputs: BLS CPI (we have `opengem-data-bls`), BEA PCE (we have `opengem-data-bea`), EIA gasoline + oil (need a new `opengem-data-eia` adapter), maybe FRB H.15 (we have `opengem-data-frb`).
- Output: daily nowcast of headline + core CPI + headline + core PCE, with vintage stamps and PIT calibration scoring per the V&V matrix.
- Dashboard surface: `opengem-l3-inflation-nowcast/{country}` and tile per L167.

### Block III (Tier-V extension)
- Generalize the framework country-by-country for inflation nowcasting in Tier-V economies. Each country needs its own input mix (e.g. UK: weekly fuel price + monthly retail price index; Germany: HICP early release + ifo Geschäftsklima).
- This is where the Bańbura-Giannone-Modugno DFM framework (and thus `DynamicFactorMQ` from L032) starts replacing the Cleveland Fed's simpler DMS — the Cleveland model is US-tuned and doesn't generalize.

### Now-Casting.com angle (not a build item)
- Document the commercial competitor in the L002 / L010 competitive landscape work.
- Use their existence as evidence in the pricing thesis (L006): there is willingness-to-pay for multi-country nowcasts.

## Why the Cleveland model is the right starter (vs the NY Fed DFM)

The Cleveland Fed model uses ~5 inputs. The NY Fed DFM (L032) uses ~30–127. The Cleveland model converges in seconds. The NY Fed DFM takes a minute and can land in local optima. For our inflation tile, the Cleveland approach is:

- **Faster to ship.** Three days end-to-end including tests.
- **Easier to explain.** Three components, three regressions, one aggregator.
- **More transparent.** Every line of code corresponds to an equation in the paper.
- **More robust at the tail.** When oil shocks happen, the Cleveland model handles them gracefully because oil is a *named input*; the NY Fed DFM has to learn it through factor structure.

The NY Fed DFM is the right tool for **GDP**, where you want to integrate dozens of soft indicators. The Cleveland model is the right tool for **inflation**, where you want to track a handful of high-frequency hard inputs and respect well-known economic structure.

## Risks

1. **MATLAB replication friction.** JMCB archives are not always plug-and-play; expect a day or two of trial-and-error to match the published series exactly.
2. **2024 refresh not yet replicated.** The Knotek-Zaman 2024 paper introduced model-averaging tweaks; the replication package exists but is newer and less battle-tested.
3. **EIA data adapter not yet built.** Adding `opengem-data-eia` is a 1-week task. Already on the data adapter roadmap.
4. **Gasoline-pass-through nonlinearity.** During large oil shocks, the linear pass-through breaks; the Cleveland Fed has heuristics for this. We need to replicate those heuristics, not just the headline equation.
5. **License of JMCB archive.** Academic-norm but not formally licensed. We re-implement, do not redistribute the original MATLAB. Our code is Apache-2.0 in our repo.

## Verdict

**Grade B**, with the caveat that the inflation nowcast is **the second-highest-priority L3 build** for OPENGEM (after the GDP DFM from L032). We replicate, we ship, we cite. Now-Casting.com is **Grade C**, cite-only, treat as competitive intelligence.

## Citations

- Knotek, Edward S., II, and Saeed Zaman. "Nowcasting US Headline and Core Inflation." *Journal of Money, Credit and Banking* 49(5): 931–968, 2017.
- Knotek, Edward S., II, and Saeed Zaman. "Nowcasting Inflation." FRB Cleveland Working Paper 24-06, 2024. https://www.clevelandfed.org/people/profiles/z/zaman-saeed/wp-2406-nowcasting-inflation
- "Inflation Nowcasting" page: https://www.clevelandfed.org/indicators-and-data/inflation-nowcasting
- "A Real-Time Assessment of Inflation Nowcasting at the Cleveland Fed." Economic Commentary EC 2023-06.
- Bańbura, Giannone, Modugno, Reichlin. "Now-casting and the Real-Time Data Flow." ECB Working Paper 1564, 2013.
- Now-Casting.com: https://www.now-casting.com/

## Related

- [[L031]] — Atlanta Fed GDPNow (parallel closed-source US nowcast)
- [[L032]] — NY Fed Nowcasting (the bigger framework; same intellectual lineage as Now-Casting.com)
- [[L167]] — Inflation nowcast tile in the dashboard
- [[L168]] — GDP nowcast tile
- [[L190]] — Consensus comparison
- [[L033]] — this file
