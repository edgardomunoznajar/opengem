# L043 — ECB SPF + consensus-forecast surfaces: open vs paywalled

**Loop**: 043 / 300
**Phase**: 1 — Open-source landscape survey (consensus forecasts)
**Date**: 2026-06-06
**OPENGEM adoption grade**: **A for ECB SPF + Philly Fed SPF + OECD EO + IMF WEO + WB GEP; D for Consensus Economics / Reuters polls / Blue Chip / FocusEconomics**

---

## TL;DR

The consensus-forecast landscape splits cleanly into "free, dated, open, machine-readable" vs "paid, often proprietary, rarely vintaged":

**Open and adoptable** (we adopt all of these):

- **ECB SPF** (`data.ecb.europa.eu/data/datasets/SPF`) — quarterly, ~50 forecaster panel, anonymized microdata + aggregates, SDMX 2.1 + CSV downloads, no API key. Coverage: euro area GDP growth, HICP inflation, core HICP, unemployment.
- **Philly Fed SPF** (`philadelphiafed.org/surveys-and-data/real-time-data-research/spf`) — the US-side, quarterly since 1968, the oldest macroeconomic survey of forecasts in the world. ~30+ forecasters per round. Aggregates + anonymized individuals + density forecasts. Excel + CSV downloads.
- **IMF WEO** — twice-yearly (April + October), 150+ countries, downloadable. Free; copyright-noted but practically free use with attribution (L040).
- **OECD Economic Outlook** — twice-yearly + interim updates, ~50 country forecasts, downloadable via OECD Data Explorer (SDMX 2.1/3.0 API). Free; subject to OECD Terms and Conditions.
- **World Bank GEP / MPO** — see L042. CC-BY 4.0. Best license terms.

**Paywalled / closed** (we do not depend on these):

- **Consensus Economics** — subscription. Their data is the operational consensus benchmark in private banks, but **the *annual* means are sometimes free**, while monthly granular forecasts are paywalled. Available via Datastream pass-through. Not for us at IOC. Maybe at FOC if a paid tier emerges that needs it.
- **Reuters Polls** — subscription via LSEG. Free press summaries; paid microdata.
- **Blue Chip Economic Indicators / Blue Chip Financial Forecasts** — Wolters Kluwer subscription. ~50+ US economists. Historical archive at UCI Library is for academic use only.
- **FocusEconomics** — subscription. Covers 198 countries + 30 commodities. They built an API explicitly for "machine-driven use cases." Closed.
- **CEIC** — subscription. The data aggregator side of consensus.

**The killer adoption is the SPF doubleheader**: ECB SPF for euro area + Philly Fed SPF for US, both free, both well-documented, both with anonymized microdata that lets us do *forecaster-level* analysis (e.g. dispersion, surprise indices, calibration tracking). Plus IMF WEO + OECD EO + WB GEP as the official-institution overlays. **This is the entire consensus-comparison layer (L190) without paying a cent.**

## ECB SPF in detail

| Field | Value |
|---|---|
| Frequency | Quarterly (Feb, May, Aug, Nov releases) |
| Coverage | Euro area (HICP, core HICP, GDP, unemployment) |
| Horizons | Current year + 1 + 2 + 5-year-ahead + long-run |
| Density | Yes — full probability distributions, anonymized per forecaster |
| Aggregate access | SDMX 2.1, CSV, ECB Data Portal |
| Microdata access | Anonymized individuals published quarterly |
| API key required? | No |
| License | Not explicitly CC-BY but freely downloadable; ECB Data Portal terms apply |

Started 1999 (alongside euro launch). ~50 forecasters from financial and non-financial institutions across the euro area. ECB's 2019 economic bulletin "Twenty years of the ECB Survey of Professional Forecasters" is the reference paper.

The SPF microdata is **the gold-standard** for studying forecaster behavior — academic literature uses it for overconfidence, herding, persistence, calibration studies. For OPENGEM, the value is:

1. **Consensus median + bands as overlay** on euro-area country pages.
2. **Forecaster-level dispersion as a "uncertainty" indicator** — when SPF dispersion widens, that's a signal.
3. **Calibration of our own forecasts vs SPF panel** — a defensible benchmark for our euro-area V&V matrix.

## Philly Fed SPF in detail

| Field | Value |
|---|---|
| Frequency | Quarterly |
| Coverage | US (CPI, real GDP, unemployment, payrolls, T-bill, T-bond, Stock-Watson recession prob, others) |
| Horizons | Current quarter, 1Q ahead, 2-4Q ahead, current year, next year, 5Y, 10Y |
| Density | Yes — full probability distributions per variable, per forecaster |
| Aggregate access | Excel + CSV at philadelphiafed.org |
| Microdata access | Anonymized individuals published quarterly |
| API key required? | No |
| License | Public-domain (US federal-charter institution) — free use |

Started 1968 by ASA + NBER; Philly Fed took over in 1990. ~30+ forecasters. Variables include: CPI, real GDP, nominal GDP, GDP price index, payroll employment, civilian unemployment, T-bill rate, 10Y T-bond, AAA corporate, Stock-Watson recession probabilities, real consumption, real residential investment, real corporate profits.

There's an open-source `spf` R package (`markushhh/spf` on GitHub) that wraps the Excel downloads with R functions. No Python equivalent, but a 2-week build to ship `opengem-data-philly-spf`.

**Adopt as the canonical US consensus overlay** alongside IMF WEO / OECD EO on the US country pages.

## OECD Economic Outlook

| Field | Value |
|---|---|
| Frequency | Twice-yearly (May + Nov) + interim updates (March + September) |
| Coverage | OECD members + selected partners (~50 countries) |
| Horizons | Current year + next 2 |
| Density | No — point forecasts only |
| API access | SDMX 2.1 + 3.0 via OECD Data Explorer |
| License | OECD Terms and Conditions (similar to IMF: free use with attribution; no large-scale redistribution) |

The OECD EO is the OECD analog to IMF WEO. Coverage skews toward developed economies (the OECD-26 + a few partners). The Data Explorer has a "Developer API" button on every dataset that shows the exact SDMX query needed.

**Adopt as the second multilateral overlay** alongside IMF WEO on all our country pages.

## What about Consensus Economics?

Consensus Economics is the operational gold-standard in private banks. Their offering: monthly survey of 1000+ economists across 100+ countries, with detailed per-economist forecasts for GDP, inflation, interest rates, exchange rates, fiscal/monetary indicators.

**Cost**: low-five-figures USD/year per institutional seat. Some annual mean data is free; monthly granular is paywalled.

For OPENGEM:

- **Not at IOC** (free public dashboard).
- **Maybe at FOC** for the paid tier — "if you pay us, we add Consensus Economics overlays to your dashboard view." This is a paid-tier feature, not a runtime dependency.
- The asymmetry: we publish our own track record vs Consensus Economics where available; they cannot do the reverse.

## Open vs paywalled — a market view

The fact that the open multilateral surveys (SPF, EO, WEO, GEP) **collectively cover ~99% of OPENGEM's consensus-comparison need** is the substantive finding. Consensus Economics monetizes the gap between "twice-a-year institution forecast" and "monthly market-grade forecast" — a one-month resolution improvement and a single-economist breakdown.

OPENGEM's positioning: **our own monthly+ forecasts are at the market-grade resolution, fully open and tracked.** The free SPF surveys provide overlay. Consensus Economics is the optional premium signal we may or may not add later.

The key gap: there is no free European multi-economist monthly survey. ECB SPF is quarterly. Reuters polls (paid via LSEG) are monthly. Until our own euro-area nowcast is competitive with Reuters poll medians, there's a real "what does the median forecaster say *this month*" gap. We accept this gap at IOC.

## OPENGEM build plan

### Block I (immediate)

- `opengem-data-ecb-spf` adapter (3 days). SDMX 2.1 pull from ECB Data Portal. Aggregate + anonymized microdata. Vintage stamp = release quarter.
- `opengem-data-philly-spf` adapter (1 week). Excel + CSV pull from Philly Fed. Aggregate + anonymized microdata. Vintage stamp = release quarter.
- `opengem-data-oecd-eo` adapter (3 days). SDMX 3.0 pull from OECD Data Explorer.
- `opengem-data-imf-weo` adapter (already in L040 scope, 1 week).
- `opengem-data-wb-gep` adapter (already in L042 scope, 1 week).

Total Block I: ~3 weeks across 5 adapters. Result: complete consensus-overlay coverage for our V&V matrix.

### Block II

- Consensus comparison page (L190) uses these adapters as the overlay layer.
- Surprise-index tile (L169, L191) computes "our nowcast - consensus median" as a daily indicator.
- Calibration page (L193) tracks our calibration vs SPF and WEO over time.

### Block III (optional)

- Paid-tier integration of Consensus Economics for the "premium calibration" view.
- Forecaster-level analysis using SPF microdata (academic research direction).

## License compatibility

- **ECB Data Portal**: not explicitly CC-BY, but freely downloadable for non-commercial and commercial use with attribution. Practically open.
- **Philly Fed SPF**: public-domain. The most permissive.
- **OECD Data Explorer**: OECD Terms and Conditions allow free use with attribution, no large-scale redistribution.
- **IMF WEO / WB GEP / MPO**: see L040 / L042.

We attribute every consensus point. We don't redistribute the surveys as-is. We compute derived series (e.g. our own surprise index from "OPENGEM nowcast - SPF median"). All practically compliant.

## Risks

1. **SDMX API drift.** ECB and OECD both migrate periodically. Mitigation: `sdmx1` Python lib insulates us from most version churn.

2. **Vintage preservation.** SPF doesn't preserve old vintages in a clean API. Mitigation: we snapshot every quarter's release; maintain our own SPF vintage archive.

3. **License creep.** ECB or OECD could tighten terms (FRED did in 2024). Mitigation: keep our own archive; have a fallback in case live API access becomes restricted.

4. **Microdata anonymization.** SPF microdata is anonymized by ID. We must not re-identify forecasters. Mitigation: trivial; we don't have other channels to cross-reference.

5. **Consensus Economics competitive pressure.** If we surface free SPF aggregates better than Consensus Economics does for their paid customers, we may face copyright pressure on derived works. Mitigation: clear citation; legal review of our derived-series policy before public launch.

## Verdict

**Grade A** for the open-consensus stack: **ECB SPF + Philly Fed SPF + OECD EO + IMF WEO + WB GEP**. Adopt all five as data adapters in Block I. This is the entire consensus-comparison layer.

**Grade D** for Consensus Economics / Reuters Polls / Blue Chip / FocusEconomics. Don't depend on them; consider paid-tier integration in Block III at the earliest.

## Citations

- ECB SPF: https://data.ecb.europa.eu/data/datasets/SPF
- ECB SPF methodology: https://data.ecb.europa.eu/methodology/survey-professional-forecasters-spf
- ECB 2019 bulletin "Twenty years of the ECB SPF": https://www.ecb.europa.eu/press/economic-bulletin/articles/2019/html/ecb.ebart201901_01~8300a24082.en.html
- Philly Fed SPF: https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/survey-of-professional-forecasters
- OECD Data Explorer: https://data-explorer.oecd.org/
- OECD EO publications: https://www.oecd.org/en/publications/serials/oecd-economic-outlook
- Consensus Economics: https://www.consensuseconomics.com/
- Blue Chip Economic Indicators: Wolters Kluwer paywalled
- FocusEconomics: https://www.focus-economics.com/
- `markushhh/spf` R package (Philly Fed SPF): https://github.com/markushhh/spf

## Related

- [[L040]] — IMF (WEO is the multi-country consensus)
- [[L042]] — World Bank (GEP is the developing-country consensus)
- [[L050]] — ECB SDW (broader ECB data)
- [[L169]] — Surprise index tile
- [[L190]] — Consensus comparison (this is the home of all five adapters)
- [[L191]] — Surprise index per indicator
- [[L193]] — Calibration plot per indicator × horizon
