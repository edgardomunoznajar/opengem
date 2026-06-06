# L027 — V-Dem: variables, time-series depth, country coverage, visualizer ecosystem

**Loop**: 027 / 300
**Phase**: 1 — Open-source landscape survey (geopolitical risk + event data)
**Date**: 2026-06-06
**License tag**: **GREEN — University of Gothenburg / V-Dem Institute, free download with citation; treated as open-academic redistribution**

---

## One-paragraph summary

V-Dem (Varieties of Democracy) is the most ambitious cross-national democracy-measurement project ever attempted: 531 indicators, 251 high-level indices, 202 polities, 1789-2025, built from ~4,000 expert coders' assessments aggregated through a Bayesian item-response model that produces both point estimates *and* credible intervals. Version 16 ships in 2026 with the "Unraveling The Democratic Era?" report. All data is freely downloadable, multiple formats (Stata/CSV/R/SPSS), each release ships a codebook + suggested-citation block. The Bayesian credible intervals are the methodological gift: they are exactly the kind of explicit-uncertainty signal that OPENGEM's V&V matrix wants to surface. For the L227 election-risk page, L222 institutional / long-run page, and L216 sovereign-risk page, V-Dem is the canonical structural data layer.

## What V-Dem actually is

V-Dem is a research project headquartered at the V-Dem Institute, Department of Political Science, University of Gothenburg, with project leads spread across roughly 30 research centers worldwide. Founded ~2014 by Michael Coppedge, John Gerring, Staffan Lindberg and collaborators. Funded primarily by Swedish Research Council, with European Research Council and US foundation grants.

The methodological core is unusual: V-Dem hires ~4,000 country experts (typically academics or in-country specialists) who code the same set of structured questions about their country-year. Each indicator is coded by ~5 experts; the aggregation runs a Bayesian item-response model (IRT) to:

1. Convert ordinal-scale expert coding into continuous latent estimates.
2. Calibrate inter-coder reliability (some experts are tougher graders than others).
3. Produce both a point estimate AND a posterior credible interval per country-year-indicator.

This last property is what no commercial democracy index gives you. Freedom House gives you a single score; EIU gives you a single score; V-Dem gives you a posterior with credible band. The credible band lets OPENGEM surface "this rating is high-uncertainty" in countries where coder disagreement is high — the kind of epistemic honesty that no incumbent has the institutional incentive to publish.

## What's in v16 (current as of 2026)

- **531 indicators** — granular per-question coder outputs
- **251 indices** — aggregated composite measures
- **202 polities** — every country-state-territory with sufficient historical record
- **Time depth**: 1789-2025 for indicators with long-history coverage; most variables 1900+; many post-WWII
- **Five high-level democracy indices**: Electoral, Liberal, Participatory, Deliberative, Egalitarian
- **62 additional indicators** sourced from external datasets (cross-walked)

## The five democracy indices (the headline measures)

V-Dem refuses to commit to a single definition of democracy. Instead it ships five:

1. **Electoral Democracy Index (EDI)** — focuses on free, fair, multiparty elections + suffrage + freedom of expression. Closest to a "minimal" democracy measure.
2. **Liberal Democracy Index (LDI)** — EDI + constraints on government, civil liberties, rule of law.
3. **Participatory Democracy Index (PDI)** — EDI + active citizen participation (referenda, civil society).
4. **Deliberative Democracy Index (DDI)** — EDI + quality of public deliberation, evidence-based politics.
5. **Egalitarian Democracy Index** — EDI + equality of political opportunity across groups.

For OPENGEM's purposes the LDI is the workhorse — it correlates with sovereign-credit spreads, FDI flows, and recession-recovery speed in the literature. We surface all five with toggle in the L227 page.

## Sub-indicators that matter for forecasting

A non-exhaustive list of V-Dem variables OPENGEM will use as forecast features:

- `v2x_polyarchy` — Electoral Democracy
- `v2x_libdem` — Liberal Democracy
- `v2x_jucon` — Judicial constraint on the executive
- `v2x_corr` — Political corruption index
- `v2x_rule` — Rule of law index
- `v2x_freexp_altinf` — Freedom of expression
- `v2regelec*` — Election quality sub-indicators (turnout, fraud, intimidation)
- `v2cltrnslw_osp` — Transparent law-making
- `v2dlconslt` — Quality of pre-decision consultation
- `v2xnp_pres` — Presidentialism

The credible intervals are stored as `_codelow` and `_codehigh` (and the median is the main column) per indicator. OPENGEM's V&V matrix exposes these intervals on the country page — which is the difference between "Country X is a 0.42 on liberal democracy" and "Country X is somewhere in [0.31, 0.53] with 95% credibility."

## File formats and access

V-Dem distributes via direct download from `v-dem.net/data/`. ZIP packages per dataset variant include the data plus codebook plus what's-new plus cautionary-notes plus suggested-citation. Variants:

- **Country-Year Core** — five high-level indices + 93 sub-indices + 179 indicators (the workhorse file, ~50 MB CSV).
- **Country-Year Full** — all 531 indicators + 251 indices + 62 external (the kitchen sink, ~200 MB CSV).
- **Country-Date** — same indicators in a denser time axis where election/event timing matters (~150 MB).
- **V-Party Dataset** — separate dataset on political parties.
- **ERT (Episodes of Regime Transformation)** — coded episodes of democratic backsliding or transition.

All four file formats — Stata `.dta`, R `.rds`, CSV, SPSS — are bundled. The R package `vdemdata` (on `vdeminstitute/vdemdata` GitHub) provides idiomatic loaders.

The Demscore e-infrastructure provides an alternative authenticated API to V-Dem, useful for cross-dataset queries against UCDP / Quality of Government / other Swedish datasets.

## License and citation

V-Dem makes "all data freely available." The codebook carries a "© University of Gothenburg, V-Dem Institute" notice and bundles a suggested-citation block. There is no explicit Creative Commons banner on the headline page, but:

- The data is freely redistributable for academic and non-commercial purposes.
- The codebook is copyrighted (so we attribute and link rather than mirror).
- Suggested citations are provided per-release.
- The vdemdata R package on GitHub is MIT-licensed.
- Mirrors on Notre Dame's curate.nd.edu and on Quality of Government data-finder confirm open redistribution norms.

For OPENGEM we treat V-Dem as **GREEN — academic free redistribution with mandatory citation per release**. We mirror dataset CSVs to R2 for the vintage-rewind / cite-this-view feature, and surface the V-Dem suggested-citation in every methodology pop-up that touches a V-Dem-derived chart.

If V-Dem were to clarify with an explicit CC-BY-NC, OPENGEM's commercial-API tier would be affected. The pragmatic path: pre-launch, write to V-Dem requesting a licensing clarification for our use case (open-source dashboard + paid API throughput tier). Their historical position has been permissive but explicit clarification removes risk.

## Country coverage and the long-history caveat

Coverage detail:

| Period | Country count | Note |
|---|---|---|
| 1789-1899 | ~30 | Mainly Atlantic states; pre-modern coding |
| 1900-1945 | ~80 | Most of Europe + Latin America + key Asia |
| 1946-1989 | ~150 | Post-decolonization coverage |
| 1990-2025 | 202 | Full coverage |

For OPENGEM's L222 long-run page, the pre-1900 panel is unique and irreplaceable — no other dataset gives you Switzerland's electoral-democracy score in 1820. For real-time forecast features, we use 1946+ where the panel is dense.

## Visualizer ecosystem (the part that helps OPENGEM build faster)

V-Dem's own viz tools (`v-dem.net/graphing/`) include:

- **Country Graph** — pick country, pick indicator(s), get a time-series plot. Vanilla but functional.
- **Variable Graph** — pick indicator, see cross-country comparison.
- **Map** — choropleth by year.

Quality is academic-functional, not terminal-grade. OPENGEM does not embed V-Dem's viz; we re-render with our own Lightweight Charts + globe.gl stack using V-Dem data ingested into our Iceberg store.

The most useful third-party visualizer is **Our World in Data** (OWID, `ourworldindata.org/grapher/electoral-democracy-index`), which embeds V-Dem-based grappers with consistent design. OWID itself is CC-BY-4.0; their treatment of V-Dem provides a reference design for OPENGEM's L227 page. We do not republish OWID charts directly (CC-BY attribution is fine but we want our own design system), but the visual grammar (line chart with country selector + map + table) is a useful baseline.

The `vdemdata` R package and the Python `pyvdem` community wrapper handle the ingest mechanics.

## How OPENGEM uses V-Dem

Four primary surfaces:

1. **L227 Election Calendar + Political-Risk page** — V-Dem LDI + EDI + corruption indices as the structural baseline; overlay UCDP electoral-violence events; overlay POLECAT election-related event volume; overlay upcoming elections from external calendar.
2. **L222 Institutional / Long-Run page** — V-Dem democracy indices, rule-of-law, judicial-constraint as the long-run institutional measures. The pre-1900 coverage makes this page genuinely deep.
3. **L216 Sovereign-Risk page** — V-Dem rule-of-law + corruption indices + judicial-independence as institutional inputs to sovereign-credit forecasts. The credible-band display lets us flag countries where structural assessment is uncertain.
4. **L213 Recession-Prob page** — V-Dem democracy regime score as a slow-moving prior on recession-recovery speed. Democracies recover faster from recessions on average; non-democracies are higher-variance.

## Risks

- **License ambiguity** — no explicit CC-BY banner. **Mitigation**: write to V-Dem, request clarification; meanwhile treat as GREEN academic with conservative attribution.
- **Codebook lookup burden** — 531 indicators means OPENGEM needs an internal indicator dictionary. **Mitigation**: build `opengem-vdem-index` JSON mapping indicator code → name + description + cite + range + interpretation. One-time effort, reusable across every chart.
- **Expert-coder pool stability** — V-Dem depends on ~4,000 volunteer-paid experts. Some country panels have only 2-3 coders. **Mitigation**: surface `n_coders` per country-indicator-year in the methodology pop-up; the credible band already encodes this uncertainty.
- **Annual release cadence** — V-Dem updates yearly (typically March). Real-time political-event movement is not reflected. **Mitigation**: pair with POLECAT/ACLED/GDELT event signal for live; V-Dem provides the slow-moving institutional baseline.

## Action items

1. Build `opengem-data-vdem` package — adapter, version pinning, mirror to R2.
2. Ingest v16 Country-Year Full (~200 MB) on release.
3. Build `opengem-vdem-index` indicator dictionary (one-time, 531 entries).
4. Wire V-Dem LDI + EDI + LDI credible bands into L227 page.
5. Wire V-Dem rule-of-law + corruption into L216 sovereign-risk forecast features.
6. Request licensing clarification from V-Dem Institute (pre-launch task).
7. Update L282 License Audit — V-Dem GREEN with note about explicit clarification pending.

## Related

- [[L001-vision-statement]] — credible bands fit the V&V matrix promise
- [[L022-acled]] — sibling YELLOW; V-Dem is the GREEN governance equivalent
- [[L026-ucdp]] — sibling GREEN; pairs with V-Dem for structural + violence layer
- [[L030-geopolitical-risk-indices-comparison]] — V-Dem is the open democracy index in the table
- [[L173-vintage-time-machine]] — V-Dem historical depth enables 1789+ rewinds for some indicators
- [[L216-sovereign-risk-page]] — V-Dem institutional inputs
- [[L222-demography-long-run]] — V-Dem long-run institutional context
- [[L227-election-calendar-political-risk]] — V-Dem primary visualizer
- [[L282-license-audit]] — V-Dem GREEN with clarification flag

## Sources

- [V-Dem — homepage](https://www.v-dem.net/)
- [V-Dem Dataset page](https://www.v-dem.net/data/the-v-dem-dataset/)
- [V-Dem Datasets list](https://www.v-dem.net/data/)
- [V-Dem Methodology](https://www.v-dem.net/about/v-dem-project/methodology/)
- [V-Dem Codebook v14 (PDF)](https://v-dem.net/documents/38/V-Dem_Codebook_v14.pdf)
- [V-Dem Methodology v13 (PDF)](https://v-dem.net/documents/26/methodology_v13.pdf)
- [V-Dem Democracy Indices (Wikipedia)](https://en.wikipedia.org/wiki/V-Dem_Democracy_Indices)
- [V-Dem vdemdata R package on GitHub](https://github.com/vdeminstitute/vdemdata)
- [Notre Dame V-Dem mirror](https://curate.nd.edu/articles/dataset/Varieties_of_Democracy_V-Dem_Data_v_14/25810768)
- [Our World in Data — Varieties of Democracy](https://ourworldindata.org/grapher/varieties-democracy-vdem)
- [OWID — Electoral Democracy Index](https://ourworldindata.org/grapher/electoral-democracy-index)
- [Quality of Government V-Dem mirror](https://datafinder.qog.gu.se/dataset/vdem)
