# L024 — Caldara-Iacoviello GPR: replication, country indices, extensions

**Loop**: 024 / 300
**Phase**: 1 — Open-source landscape survey (geopolitical risk + event data)
**Date**: 2026-06-06
**License tag**: **GREEN — Fed research, public-domain published, openICPSR replication CC-BY-style; OPENGEM already ingests via `opengem-data-gpr`**

---

## One-paragraph summary

The Caldara-Iacoviello Geopolitical Risk Index (GPR) is the only academic geopolitical-risk measure with a published methodology, published replication code, monthly updates from a Fed economist's personal site, and 125-year historical depth (GPRH back to 1900). OPENGEM already vendors it as `opengem-data-gpr`. The interesting question for L024 is **what extensions are valuable** — and there are five: (1) daily GPR (GPRD) since 2017, (2) country-specific GPR-C for 44 countries, (3) the AI-GPR LLM-based recoder published in 2024, (4) the GPR-SR subset by topic (war, terror, sanctions, etc.), and (5) running the replication code ourselves to extend coverage to additional newspapers, additional countries, or alternative event taxonomies. The license is the rare clean case: Caldara-Iacoviello are Fed staff publishing in the public domain under a personal-academic site with explicit citation requirement and replication-code distribution on openICPSR. **OPENGEM is free to republish derived GPR series with citation, and free to re-run the replication pipeline to extend the index.**

## What GPR actually is

GPR is a **newspaper-text-search-based** measure of adverse geopolitical events. The construction is deliberately simple — that's the methodological point of the paper:

1. Take the electronic archives of 10 major English-language newspapers: Chicago Tribune, Daily Telegraph, Financial Times, Globe and Mail, The Guardian, LA Times, NYT, USA Today, WSJ, Washington Post.
2. Define a list of search-term groups across 8 categories: (1) war threats, (2) peace threats, (3) military buildups, (4) nuclear threats, (5) terror threats, (6) beginning of war, (7) escalation of war, (8) terror acts.
3. For each newspaper-month, count the share of articles matching at least one search-term group, normalize against the 1985-2019 mean = 100.
4. Average across newspapers — that's the index.

Subindices:

- **GPRT** (Geopolitical Threats) — categories 1-5 (threats not yet realized).
- **GPRA** (Geopolitical Acts) — categories 6-8 (realized events).

This split matters: GPRA spikes coincide with realized military events (gulf wars, 9/11, Russia-Ukraine); GPRT runs ahead and is more predictive of forward-looking macro effects (investment, employment, equity prices).

The headline academic finding (Caldara & Iacoviello, AER 2022): GPR shocks are associated with lower investment, lower stock prices, lower employment, and higher recession probability — even after controlling for macro/political-uncertainty proxies. That's the basis for treating it as a forecast feature, not just a descriptive index.

## What variants exist

The GPR family on `matteoiacoviello.com` is now substantial:

| Variant | Time depth | Cadence | Description |
|---|---|---|---|
| GPR (Benchmark) | 1985-01 → present | Monthly | 10 newspapers, 8 categories |
| GPRH (Historical) | 1900-01 → present | Monthly | 3 newspapers (NYT, WaPo, Chicago Tribune), longer history |
| GPRD (Daily) | 2000 → present (2017 onwards stable) | Daily | Daily version of GPR for high-frequency macro |
| GPR-C (Country) | varies, 1985+ | Monthly | Country-specific GPR for 44 countries |
| GPR-SR (Subcategory) | 1985+ | Monthly | Per-category breakdown (war, terror, etc.) |
| AI-GPR | 1900+ | Monthly | LLM-recoder version, methodological alternative |

OPENGEM already has the monthly Benchmark GPR + country GPR-C ingested (see `packages/opengem-data-gpr`). The five extensions below are the open work.

## Replication and license

The replication archive is at `openicpsr.org/openicpsr/project/154781` (DOI 10.3886/E154781V1), distributed by ICPSR under a license selected by the depositor — for AER articles this is typically CC-BY-NC or Public Domain Mark. The code is Stata + Python + Matlab depending on the panel; data inputs are the newspaper article counts (which Caldara and Iacoviello obtained via institutional access to ProQuest / Factiva).

Two important points:

1. **The construction code is openly published.** OPENGEM can re-run it.
2. **The newspaper-article-count input data is *not* re-published** — it's a downstream of Factiva/ProQuest which are subscription products. Replicators need their own access.

For OPENGEM the practical path is **not** to re-run the construction (no Factiva license) but to **mirror Iacoviello's monthly published CSVs** and add derived series. This is what the existing `opengem-data-gpr` package already does. The monthly CSVs are at `https://www.matteoiacoviello.com/gpr_files/` and are updated around the 10th of each month.

The license tag is GREEN because:
- Caldara and Iacoviello are Fed staff; the underlying analytic work is implicitly public-domain US-government output.
- The published CSVs carry no restrictive license; the cited paper requires citation per AER's standard CC-BY-NC-derivative norm.
- The replication code on openICPSR is openly redistributable.

OPENGEM's citation in the methodology pop-up names Caldara & Iacoviello AER 2022 and links to `matteoiacoviello.com/gpr.htm`.

## Five extensions OPENGEM should build

### Extension 1 — Daily GPR (GPRD) ingestion

The current `opengem-data-gpr` package ingests monthly only. Daily GPRD is published as a separate CSV with `Date,GPRD` columns since 2000 (and clean since 2017). Adding it gives OPENGEM a daily-cadence geopolitical-risk signal that pairs with GDELT for cross-validation. **Effort: half a day. Value: high.**

### Extension 2 — Full GPR-C country-month grid as a tile

Country-specific GPR-C exists for 44 countries; OPENGEM already pulls them. The unbuilt piece is the **comparison tile** — a heatmap of country × month × GPR-C-z-score for the last 24 months, sortable, with country drilldown. Combined with the L161 country-card grid, this becomes the geopolitical risk landing page. **Effort: 2 days. Value: high.**

### Extension 3 — GPR-SR category breakdown as a per-country sidebar

GPR-SR breaks the index into 8 categories. Surfacing the per-country category contribution lets users see *why* a country's GPR is elevated this month (terror? sanctions? war threats?). This is the kind of structured narrative that beats the Stratfor editorial newsletter on transparency. **Effort: 2-3 days. Value: high — this is the kind of explainability moat OPENGEM cannot afford to skip.**

### Extension 4 — AI-GPR cross-validation

In 2024 Caldara/Iacoviello published an LLM-recoded version (AI-GPR) that re-classifies historical articles using a large language model rather than rule-based search. Methodologically it's a different measurement; substantively it correlates ~0.95 with the original. OPENGEM should ingest AI-GPR alongside GPR and surface both in the methodology pop-up — this is exactly the "publish your alternatives" play that builds credibility against opaque incumbents. **Effort: 1 day to ingest, 1 day to wire into pop-up. Value: medium-high.**

### Extension 5 — GPR-derived forecast feature

GPRT (Threats) at horizon h is a known leading indicator for recession probability at h+12 months. Wire GPRT-Δ + GPRA-Δ as features into the L3 ensemble for the recession-probability tile (L213) and the country-level FX-misalignment forecast (L217). The Caldara-Iacoviello paper provides estimated coefficients we can use as Bayesian priors. **Effort: 2 days. Value: high — closes the loop from descriptive index → forecast input.**

## What the AI-GPR shift means

Caldara/Iacoviello publishing an LLM-recoded variant in 2024 is the single most important methodological development in geopolitical-index literature in the last decade. It signals that the rule-based search-term approach (which OPENGEM has been treating as canonical) is now considered *one* approach among several, with LLM-recoded variants offering similar signal at lower curation cost.

The strategic implication for OPENGEM: we should be willing to build an **OPENGEM-GPR** variant in-house once we have a story for the Factiva-equivalent corpus (GDELT-DOC + Common Crawl news subset is a candidate). This would let OPENGEM publish its own country-month GPR-style index under CC-BY-4.0 with full provenance, without depending on Iacoviello's monthly CSV drop. That's a 5-loop project (later phase), but the path is now clear.

## Country coverage (the 44)

The GPR-C panel covers Argentina, Australia, Brazil, Belgium, Canada, Chile, China, Colombia, Czech Rep, Denmark, Egypt, Finland, France, Germany, Hungary, India, Indonesia, Ireland, Israel, Italy, Japan, Malaysia, Mexico, Netherlands, Norway, Pakistan, Peru, Philippines, Poland, Portugal, Russia, Saudi Arabia, Singapore, South Africa, South Korea, Spain, Sweden, Switzerland, Taiwan, Thailand, Turkey, UK, US, Venezuela, Ukraine, Vietnam.

That's effectively the G20 + most large emerging markets + a handful of conflict-relevant smaller economies (Israel, Saudi, Egypt, Ukraine). The notable gaps: most of sub-Saharan Africa, Iran (politically charged), North Korea, Central Asia.

OPENGEM's country page surfaces GPR-C where it exists and falls back to GPR-Global + L228 ACLED/POLECAT conflict density for countries outside the 44.

## Update cadence

- Monthly CSV refresh around the 10th of each month, with preliminary current-month reading based on search through day 10.
- Daily GPRD updated daily-ish, sometimes lagging by a few business days.
- AI-GPR updated monthly with the same cadence as GPR.

For OPENGEM the Dagster schedule: poll `https://www.matteoiacoviello.com/gpr_files/` daily, fetch new month when it appears, validate schema, upsert. This is already what the existing adapter does.

## Risks

- **Iacoviello's personal site is the single point of distribution.** No CDN, no DOI versioning, no JSON API — just a static HTML page with CSV links. If the site went away, OPENGEM's GPR ingest breaks. **Mitigation**: weekly archival snapshot of the CSVs into R2 + a fork to the Iacoviello repo to track changes.
- **Methodology drift.** Caldara/Iacoviello have updated the GPR search terms a few times. Each update technically breaks back-comparability. **Mitigation**: vintage every CSV download with retrieval-date, publish methodology version per chart.

## Action items

1. Extend `opengem-data-gpr` with daily GPRD series (Extension 1).
2. Extend the package with GPR-SR category breakdown (Extension 3).
3. Add AI-GPR ingestion (Extension 4).
4. Build the country-month GPR-C heatmap tile (Extension 2) — this lands on the L161 country-card grid.
5. Wire GPRT-Δ + GPRA-Δ into the L3 forecast feature pipeline (Extension 5).
6. Plan the "OPENGEM-GPR" derivative — Phase 2 loop, after we have a corpus story.

## Related

- [[L001-vision-statement]] — publish-the-substrate; GPR fits cleanly
- [[L021-gdelt-gkg]] — GDELT is one of the natural news-corpus substitutes for an OPENGEM-GPR variant
- [[L022-acled]] — ACLED is the curated-event sibling; GPR is text-search
- [[L023-icews-phoenix-terrier]] — event-based geopolitical signal sibling
- [[L030-geopolitical-risk-indices-comparison]] — GPR ranks #1 there on license and methodology
- [[L161-country-card-grid]] — GPR-C heatmap target
- [[L213-recession-prob-page]] — forecast feature consumer
- [[L237-gpr-pulse-globe-prototype]] — visualizer
- existing package: `/mnt/bigdata/home/edgardo/projectsd/opengem/packages/opengem-data-gpr/`

## Sources

- [Matteo Iacoviello — Geopolitical Risk Index page](https://www.matteoiacoviello.com/gpr.htm)
- [Country-Specific GPR](https://www.matteoiacoviello.com/gpr_country.htm)
- [Old GPR (2019 vintage)](https://www.matteoiacoviello.com/gpr2019.htm)
- [AI-GPR Index](https://www.matteoiacoviello.com/ai_gpr.html)
- [Caldara & Iacoviello (2022) "Measuring Geopolitical Risk" AER (PDF)](https://www.matteoiacoviello.com/gpr_files/GPR_PAPER.pdf)
- [Replication Material page](https://www.matteoiacoviello.com/gpr_replication.htm)
- [openICPSR — Data and Code for "Measuring Geopolitical Risk"](https://www.openicpsr.org/openicpsr/project/154781/version/V1/view)
- [Dario Caldara — Geopolitical Risk](https://sites.google.com/view/dariocaldara/geopolitical-risk?authuser=0)
- [Fed IFDP 1222 — Measuring Geopolitical Risk (PDF)](https://www.federalreserve.gov/econres/ifdp/files/ifdp1222.pdf)
- [Policy Uncertainty — GPR](https://www.policyuncertainty.com/gpr.html)
