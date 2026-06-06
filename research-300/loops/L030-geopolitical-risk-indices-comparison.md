# L030 — Geopolitical risk indices comparison matrix

**Loop**: 030 / 300
**Phase**: 1 — Open-source landscape survey (geopolitical risk + event data)
**Date**: 2026-06-06
**License tags**: see matrix below — **only three are GREEN at the country-month level (GPR, WGI, V-Dem). PRS / EIU / Maplecroft / Fitch / FSI are YELLOW or RED.**

---

## One-paragraph summary

There are roughly nine canonical geopolitical-and-country-risk indices in serious use globally. Three are GREEN (open-license, redistributable derived metrics): **GPR** (Caldara-Iacoviello, Fed-publication, free CSV, citation), **WGI** (World Bank Worldwide Governance Indicators, CC-BY-4.0), and **V-Dem** (Gothenburg academic, free academic license with citation). Three are paid commercial subscriptions that OPENGEM cannot republish but *can score as competitor benchmarks*: **PRS Group ICRG, EIU Viewpoint, Verisk Maplecroft, Fitch Solutions Country Risk**. Two sit in an ambiguous middle: **Fragile States Index** (Fund for Peace, "all rights reserved" but freely downloadable for non-commercial use), and **Freedom House** scores (free download, citation required, not formally CC). For OPENGEM the play is to re-render the GREEN three as primary, score the YELLOW/RED competitors on a comparison matrix as benchmarks, and never republish their proprietary numbers.

## The matrix

| Index | Vendor / source | License | OPENGEM tag | Coverage | Methodology core | Cadence | Country count | OPENGEM use |
|---|---|---|---|---|---|---|---|---|
| **GPR** (Caldara-Iacoviello) | Fed/personal site | Free CSV + cite | **GREEN** | 1985-present (global), 1900-present (historical), 44 country-specific | Newspaper text-search count, 10 papers, 8 categories | Monthly + daily GPRD | 44 country-specific + global | Primary geopolitical risk feature |
| **WGI** (Worldwide Governance Indicators) | World Bank | CC-BY-4.0 | **GREEN** | 1996-present, annual | Unobserved Components Model over 35 sources | Annual | 200+ economies | Primary governance feature |
| **V-Dem** | U. Gothenburg | Free + cite (academic) | **GREEN** | 1789-present, annual | Bayesian IRT over ~4,000 expert coders, 531 indicators | Annual | 202 polities | Primary democracy/institutions feature |
| **Fragile States Index** | Fund for Peace | "All rights reserved", free download non-commercial | YELLOW | 2005-present, annual | 12 indicators × CAST framework, triangulation | Annual | 178 countries | Cite as benchmark only |
| **Freedom House — Freedom in the World** | Freedom House | Free + cite, no CC | YELLOW | 1972-present, annual | Expert assessment, structured questions | Annual | 195 countries | Cite as benchmark only |
| **PRS ICRG** | PRS Group | Paid subscription | RED | 1980s-present, monthly | 22 variables × 3 categories (political/financial/economic) | Monthly | 140-141 countries | Benchmark on leaderboard only |
| **EIU Viewpoint Country Risk** | Economist Group | Paid subscription | RED | continuous, quarterly | Hybrid quant + qualitative analyst | Quarterly | 200+ countries | Benchmark only |
| **Verisk Maplecroft Country Risk** | Verisk Analytics | Paid subscription | RED | continuous, varies by index | 900+ indicators, ML + expert | Daily/monthly/quarterly | 200 countries, subnational available | Benchmark only |
| **Fitch Solutions Country Risk** | Fitch Group | Paid subscription, partial Investortools redistribution | RED | continuous | Quantitative + qualitative | Quarterly | 205 markets | Benchmark only |

## The three GREEN indices, in detail

### GPR (Caldara-Iacoviello)

Covered in depth in L024. License: GREEN. Methodology: simple newspaper-text-search, fully replicable, fully open. Time depth: 125 years for the GPR-H variant. Country coverage: 44 country-specific indices + global. The only published geopolitical-risk index with daily cadence (GPRD). OPENGEM ingests live via `opengem-data-gpr`; extensions documented in L024.

### WGI (World Bank Worldwide Governance Indicators)

Six aggregate dimensions: Voice and Accountability, Political Stability and Absence of Violence/Terrorism, Government Effectiveness, Regulatory Quality, Rule of Law, Control of Corruption. Built from 30+ underlying perception sources via an Unobserved Components Model that estimates a latent governance dimension and reports point estimate + standard error per country-year-dimension. CC-BY-4.0 license confirmed on the World Bank Data Catalog. **For OPENGEM this is the cleanest publicly-licensed governance index with annual updates and 200+ country coverage.** The annual cadence is the limitation — for monthly governance signal we layer V-Dem episodes and POLECAT/UCDP events on top.

### V-Dem

Covered in detail in L027. License: GREEN academic, free academic redistribution with citation; explicit CC-BY clarification pending. Methodology: Bayesian IRT over ~4,000 expert coders, 531 indicators, 251 indices. Time depth: 1789-present. Country coverage: 202 polities.

## The two YELLOW indices

### Fragile States Index (Fund for Peace)

12 indicators across cohesion, economic, political, social dimensions. Annual rankings since 2005, published every May. Data is freely downloadable from `fragilestatesindex.org/global-data/`. The published copyright is "all rights reserved by The Fund for Peace" but the site explicitly enables free download for non-commercial research and journalism. Republishing FSI numbers in OPENGEM's free-tier dashboard with attribution is established practice (Our World in Data does this); republishing them in OPENGEM's paid API surface is risky.

**OPENGEM treatment**: cite as benchmark in narrative context (L222, L227). Show single-country FSI score with attribution in the country page. Do not bulk-republish the panel or expose via paid API. Treat as YELLOW until a written clarification from FFP is obtained.

### Freedom House — Freedom in the World

Per-country annual ratings on Political Rights (1-7) and Civil Liberties (1-7), aggregated to a Freedom Status (Free / Partly Free / Not Free). Published since 1972. Data is freely downloadable. License: copyright Freedom House, citation expected. Not formally Creative Commons. Functionally similar to FSI — embed-with-attribution is fine in journalism and research; bulk republishing in commercial products is gray.

**OPENGEM treatment**: same as FSI. Cite as benchmark, show single-country values with attribution, do not bulk-republish.

## The four RED commercial indices

### PRS Group ICRG (International Country Risk Guide)

Founded 1980. 22 variables across political (12), financial (5), economic (5) sub-categories, weighted to a composite. Methodology paper is publicly available; raw data is paid subscription. Monthly release. 140-141 country coverage. Pricing: undisclosed, negotiated, "consultation with Dr. McKee" required.

**OPENGEM cannot ingest ICRG data.** What we can do: track *aggregate* ICRG country rankings that PRS publishes for marketing (annual press releases), score them on the L133 leaderboard. We never reproduce ICRG numbers in OPENGEM's substrate.

### EIU Viewpoint Country Risk

The Economist Group's country-risk product. ~200+ countries, quarterly outlooks, scenario forecasts, quant+qual hybrid. Premium subscription product. Pricing in the $5K-$50K range depending on seat / API tier.

**OPENGEM treatment**: same as PRS — track publicly-released forecasts (EIU does press releases on year-ahead views), score them. Cannot ingest.

### Verisk Maplecroft

900+ proprietary indicators across political, regulatory, ESG, climate, human-rights, security risks. Daily-cadence for some indicators, monthly for others, subnational drilldown to province/state. Built on Verisk's enterprise risk platform; pricing enterprise-grade.

**OPENGEM treatment**: same as PRS/EIU. Maplecroft is the most methodologically sophisticated commercial competitor — they use ML over unstructured data which is precisely what OPENGEM's GREEN-substrate strategy aims to replicate openly. The Cline Center Global News Index + LLM-recoded GPR variant is OPENGEM's path to a Maplecroft-equivalent feature without the proprietary substrate.

### Fitch Solutions Country Risk

205 markets, 28M+ data points, 13.3K indicators across 22 sectors and 35 commodities. Mix of country risk + industry research. Subscription product. Some Fitch ratings are redistributable through licensed Investortools partners under explicit Fitch redistribution terms; the core country-risk methodology is not.

**OPENGEM treatment**: same. Cite as benchmark, don't reproduce.

## What OPENGEM rebuilds vs cites

The strategic question: which of these is OPENGEM trying to *replace* with open substrate, versus which is it just *citing as a benchmark*?

Tier 1 — **Replace with open substrate**:
- GPR is *already* open; we extend.
- WGI is open; we wrap.
- V-Dem is open; we wrap.
- **OPENGEM-GPR** (planned, see L024 Extension and L025 Global News Index) replaces Maplecroft's news-monitoring component with an open, CC-BY-4.0 substrate.
- **OPENGEM-Conflict-Intensity** (planned, from UCDP + GED + POLECAT) replaces ICRG's political-risk component.
- **OPENGEM-Sovereign-Risk** (planned, L216) replaces ICRG's financial-risk component with WB + IMF + BIS data.

Tier 2 — **Cite as benchmark on the leaderboard, don't reproduce**:
- PRS ICRG aggregate rankings (annual press release).
- EIU Viewpoint annual country outlooks.
- Maplecroft top-10/bottom-10 lists (annual press release).
- Fitch country-risk ratings transitions.
- Fragile States Index annual rankings.
- Freedom House Freedom in the World annual rankings.
- Stratfor / Geopolitical Futures annual forecasts (L029).

The leaderboard (L133, L184) becomes the OPENGEM moat against the commercial competitors: we have an open substrate that nobody else has, and we publicly score everyone's published predictions against ground truth. The L008 differentiation thesis — "publishes its mistakes" — applies here in the strongest form. Incumbents who never publish track records have nothing to hide because they never expose anything. OPENGEM exposes its own *and* exposes the incumbents' few public commitments.

## Methodology comparison (the part that matters for trust)

| Index | Underlying method | Coder model | Uncertainty quantification |
|---|---|---|---|
| GPR | Newspaper text-search | Rule-based regex | Per-month standard error from cross-newspaper variance |
| WGI | Unobserved Components Model | Bayesian latent variable | Per-country-year SE from UCM posterior |
| V-Dem | Bayesian IRT | ~4,000 expert coders | Per-indicator credible interval |
| FSI | CAST framework | Triangulation (quant + qual + expert) | None published |
| Freedom House | Expert assessment | Internal analysts | None published |
| PRS ICRG | Variable-by-variable scoring | Internal editors | None published |
| EIU | Hybrid quant + analyst | Internal analysts | None published |
| Maplecroft | 900+ indicator composite | ML + expert | Implicit only |
| Fitch | Quant + qual | Internal | None published |

Two observations:

1. **The three GREEN indices are also the three with explicit uncertainty quantification.** This is not a coincidence. Open-academic methodology pushes toward published priors and posteriors. Closed-commercial methodology hides uncertainty because the customer wants a single number to act on.
2. **OPENGEM's own forecasts will publish credible intervals everywhere.** This is the V&V matrix promise. The credible interval becomes part of the marketing of the V&V system. When the competitor publishes "Country X risk: 6.4/10," OPENGEM publishes "Country X risk: 6.4 ± 1.1 (95% credible) — here are the input series and methodology — here is our backtest CRPS over the last 5 years against the realized event labels." That side-by-side comparison is the demonstration.

## Update cadence comparison

| Index | Cadence | Real-time lag |
|---|---|---|
| GPR Daily (GPRD) | Daily | ~1-3 business days |
| GPR Monthly | Monthly | ~10 days after month end |
| WGI | Annual | ~6-12 months after year end |
| V-Dem | Annual | ~3-4 months after year end |
| FSI | Annual | ~5 months after year end |
| Freedom House | Annual | ~3 months after year end |
| PRS ICRG | Monthly | ~few weeks |
| EIU | Quarterly | ~weeks |
| Maplecroft | Daily/monthly/quarterly | Variable |
| Fitch | Quarterly | ~weeks |

For OPENGEM the cadence story: GPR-D is the only daily geopolitical risk signal in the GREEN tier. For everything else, the daily geopolitical "now-cast" needs to be built from GDELT (L021) + POLECAT (L023/L025) + ACLED Candidate (L022) + UCDP GED Candidate (L026). The slower annual indices (WGI, V-Dem, FSI, Freedom House) serve as structural baselines that the high-frequency event data sits on top of.

## Where OPENGEM has unique signal nobody else publishes

Three places:

1. **Open uncertainty quantification on every risk score** — credible bands shown directly. Match the V-Dem aesthetic, extend it to every chart.
2. **Open forecast leaderboard scoring all the indices above** — the L133 page is the moat.
3. **OPENGEM-derived composite risk score** built from the GREEN substrate (GPR + WGI + V-Dem + UCDP + POLECAT + GDELT + OpenSanctions exposure), fully reproducible, CC-BY-4.0 — published as an alternative to the commercial composite scores.

That last is the 5-year vision target. The L300 final synthesis will pick it up.

## Action items

1. Build `opengem-data-wgi` package — World Bank API adapter, annual job.
2. Build `opengem-data-vdem` package (already noted in L027).
3. Build `opengem-data-freedom-house` package — limited mirror, attribution-driven.
4. Build leaderboard schema (L184) to accept all 9 indices above as benchmark entries.
5. Plan the OPENGEM-Composite-Risk index — Phase 4 (L209-ish placement).
6. Update L282 License Audit with all 9 entries.

## Related

- [[L001-vision-statement]] — substrate-publishing thesis
- [[L008-differentiation]] — publishes its mistakes; explicit uncertainty
- [[L021-gdelt-gkg]] — primary geo-event substrate
- [[L022-acled]] — YELLOW human-validated sibling
- [[L023-icews-phoenix-terrier]] — POLECAT GREEN substrate
- [[L024-gpr]] — primary GREEN risk index
- [[L025-cline-center]] — Global News Index, OPENGEM-GPR substrate
- [[L026-ucdp]] — primary GREEN conflict substrate
- [[L027-vdem]] — primary GREEN democracy substrate
- [[L028-opensanctions]] — YELLOW sanctions-risk substrate
- [[L029-stratfor-osint-mirrors]] — RED commercial competitors, citation-only
- [[L133-forecast-leaderboard]] — all 9 indices benchmarked here
- [[L184-leaderboard-ranking-algorithm]] — scoring rules
- [[L209-causal-vs-forecast-claims]] — uncertainty quantification standard
- [[L282-license-audit]] — comprehensive matrix landing here
- [[L300-final-synthesis]] — OPENGEM-Composite-Risk endgame

## Sources

- [Caldara & Iacoviello GPR](https://www.matteoiacoviello.com/gpr.htm)
- [World Bank WGI](https://www.worldbank.org/en/publication/worldwide-governance-indicators)
- [WGI in World Bank Data Catalog (CC-BY-4.0)](https://datacatalog.worldbank.org/search/dataset/0038026/worldwide-governance-indicators)
- [V-Dem homepage](https://www.v-dem.net/)
- [V-Dem Dataset](https://www.v-dem.net/data/the-v-dem-dataset/)
- [Fragile States Index](https://fragilestatesindex.org/)
- [FSI Methodology](https://fragilestatesindex.org/methodology/)
- [PRS Group ICRG](https://www.prsgroup.com/explore-our-products/icrg/)
- [PRS ICRG Methodology PDF](https://www.prsgroup.com/wp-content/uploads/2012/11/icrgmethodology.pdf)
- [EIU on Grokipedia (Methodology summary)](https://grokipedia.com/page/Economist_Intelligence_Unit)
- [Verisk Maplecroft Country Risk Data](https://www.maplecroft.com/data/country-risk-data/)
- [Verisk Maplecroft factsheet (PDF)](https://www.maplecroft.com/48e66f/siteassets/images/pdfs/verisk-maplecroft_country_risk_insight_factsheet.pdf)
- [Fitch Solutions CRIR brochure (PDF)](https://your.fitch.group/rs/732-CKH-767/images/FS_CRIR_Data_brochure.pdf)
- [Fitch Solutions Investortools licensing](https://www.investortools.com/licenses/fitch/)
- [Earthian AI — Best geopolitical risk models 2026](https://www.earthianai.com/learn/best-geopolitics-risk-models-2026)
- [Fed FEDS Note — Measuring Geopolitical Risk Exposure (2025)](https://www.federalreserve.gov/econres/notes/feds-notes/measuring-geopolitical-risk-exposure-across-industries-a-firm-centered-approach-20250829.html)
