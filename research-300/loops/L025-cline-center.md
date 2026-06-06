# L025 — Cline Center: POLECAT, SPEED, Phoenix, Global News Index, Coup, CREG

**Loop**: 025 / 300
**Phase**: 1 — Open-source landscape survey (geopolitical risk + event data)
**Date**: 2026-06-06
**License tag**: **GREEN — academic-default open access; Illinois Data Bank / Harvard Dataverse hosting (CC0 unless overridden); per-dataset citation required**

---

## One-paragraph summary

The Cline Center for Advanced Social Research at the University of Illinois Urbana-Champaign is the most prolific academic publisher of political-event and historical-political-data assets in the world. The portfolio includes Phoenix (CAMEO event coding, 1945-2019), SPEED (human-validated civil-unrest events, 1945-present), the Global News Index (200M+ news stories, 2006-present), POLECAT (the live PLOVER-coded event stream, shared lineage with the Cline Center via the OEDA consortium), the Coup d'état Project (1945-present), CREG (Composition of Religious and Ethnic Groups), and the Rule-of-Law dataset. Hosting is via Illinois Data Bank and Harvard Dataverse; both default to CC0 / open-access. For OPENGEM this is the deepest reservoir of GREEN-license geopolitical training and forecast-feature data we have. The cost of ingestion is engineering effort, not licensing fees.

## What the Cline Center actually is

The Cline Center is a soft-money research center at UIUC, founded ~2014, that runs three programmatic axes: machine-coded event data (Phoenix-family, in OEDA partnership), human-validated event data (SPEED), and historical political-structure data (Rule of Law, Constitutions, Coup, CREG). It is the *academic* arm of the open-event-data world; POLECAT is the *government-adjacent* arm (Program on Geostrategic Risk); ACLED is the *non-profit* arm; GDELT is the *volunteer-founder* arm. Cline Center is most useful to OPENGEM because it has the longest historical depth and the cleanest academic-archival licensing.

## The seven datasets, ranked by OPENGEM utility

### 1. Cline Center Historical Phoenix Event Data (1945-2019)

The flagship asset. ~8.2M CAMEO-coded events extracted from 21.2M news stories using PETRARCH-2, drawn from NYT (1945-2018), BBC SWB (1979-2019), WSJ (1945-2005), and FBIS (1995-2004). Hosted on Illinois Data Bank as `IDB-2796521`, version 1.3.0. License inheritance: Illinois Data Bank default is open-access with citation; no custom restriction observed.

**Use in OPENGEM**: deep historical backfill for the event tracker. Concatenate with ICEWS legacy (1995-2022) and POLECAT (2018-present) after CAMEO→PLOVER translation. This becomes the 1945→present backbone of the L173 vintage time machine and L228 conflict tracker.

**Schema**: per-event row with CAMEO root + leaf codes, geocoded location, Goldstein scale, actor codes. ~50 columns. Approximate size: 5 GB CSV uncompressed.

### 2. SPEED — Social, Political, Economic Event Dataset

Human-curated event database, 1945-present. Focus: civil unrest, political violence, property destruction, contentious politics. ~3.5M events coded by trained human analysts using a structured protocol — *much* slower than Phoenix but much more accurate per-event. Hosted on Illinois Data Bank with multiple country-specific releases (e.g., Liberia, IDB-7407320).

**Use in OPENGEM**: the human-validated gold standard for the historical conflict layer. SPEED records have richer narrative detail than CAMEO/PLOVER coders produce, including event triggers, organizing actors, and outcomes. We surface SPEED in the L228 Conflict Tracker as a "deep-validated" toggle next to the live (POLECAT) layer.

**Schema**: events with structured human-coded fields for trigger, actors, demands, outcomes, fatalities, locations. Per-region variations.

### 3. Global News Index and Extracted Features Repository

200M+ historical news reports from 2006-present (plus historical archives 1945+), with extracted feature sets (named entities, topics, sentiment). Hosted on Illinois Data Bank `IDB-5649852`.

**Use in OPENGEM**: this is the open news corpus we'd run our own GPR-style index over (see L024 Extension — building OPENGEM-GPR). The Global News Index is significantly broader than Iacoviello's 10-newspaper corpus and importantly is freely redistributable in its extracted-features form. This is the *substrate* for an open-source competitor to all the commercial geopolitical-risk indices.

**Schema**: extracted features per news story — TF-IDF top-K, named entities, geocoded mentions, sentiment scores, topic tags. Not the raw article text (which would have copyright issues), but the structured features.

**This is OPENGEM's path to an in-house geopolitical-risk index that doesn't depend on Iacoviello's monthly drop.**

### 4. POLECAT (shared lineage)

Covered in detail in L023. Cline Center is one of the academic homes for POLECAT (though primary hosting is Harvard Dataverse via the Program on Geostrategic Risk). The Cline Center surfaces POLECAT alongside Phoenix as part of the OEDA-aligned event-data portfolio.

### 5. Coup d'état Project

1,000+ coup events globally, 1945-2005, for countries with population >500K. Hosted on Illinois Data Bank.

**Use in OPENGEM**: feature for the country-level political-stability dimension. Coup events are rare but very predictive of subsequent fiscal/exchange-rate stress; the dataset fits naturally into the L213 recession-prob model and the L216 sovereign-risk page.

### 6. CREG — Composition of Religious and Ethnic Groups

Population trend data for religious and ethnic groups, 1945-2013. Hosted on Illinois Data Bank.

**Use in OPENGEM**: deep-context for the L227 election-and-political-risk page and L228 conflict tracker. CREG is a slow-moving dataset (annual or coarser); not a forecast feature, but a contextual layer that drives the per-country narrative on the L222 demography page.

### 7. Rule-of-Law dataset (Comparative Constitutions Project + historical legal periodicals 1773-present + education programs 1100-present)

Niche but unique. The constitutional-history coverage from 1773 is genuinely one-of-a-kind.

**Use in OPENGEM**: feeds the L222 institutional/long-run page and the V-Dem-comparison view on the L227 governance pages. Not a forecast feature; a credibility layer.

## License audit (the critical table)

| Dataset | Host | Default license | OPENGEM tag | Republish derived? |
|---|---|---|---|---|
| Phoenix Event Data | Illinois Data Bank | Open access, cite | GREEN | Yes |
| SPEED | Illinois Data Bank | Open access, cite | GREEN | Yes |
| Global News Index — extracted features | Illinois Data Bank | Open access, cite | GREEN | Yes (features only; not raw text) |
| Global News Index — raw text | (not redistributed) | Copyright-restricted (per-source) | RED | No — only features |
| POLECAT | Harvard Dataverse | CC0 (Dataverse default) | GREEN | Yes |
| Coup d'état Project | Illinois Data Bank | Open access, cite | GREEN | Yes |
| CREG | Illinois Data Bank | Open access, cite | GREEN | Yes |
| Rule of Law / CCP | Illinois Data Bank | Open access, cite | GREEN | Yes |

**Important nuance**: the Global News Index distinguishes between extracted features (redistributable) and raw article text (copyright held by the original publishers, not redistributable). OPENGEM uses features only.

For all GREEN entries the OPENGEM citation pattern is the same: dataset name + Cline Center + version + DOI on every chart's methodology pop-up. The Cline Center provides recommended citations on each Illinois Data Bank page.

## Ingestion pattern

The Cline Center datasets are large but tractable. Illinois Data Bank supports HTTP file downloads with predictable URLs; no API authentication required.

```
One-time backfill jobs:
  - cline_phoenix_backfill — pull v1.3.0 Phoenix bundle, 1945-2019, ~5 GB
  - cline_speed_backfill — pull SPEED regional bundles, ~3 GB total
  - cline_news_features_backfill — pull Global News Index features, ~150 GB (selective: post-2006 most useful)
  - cline_coup_backfill — pull Coup d'état Project, ~5 MB
  - cline_creg_backfill — pull CREG, ~10 MB
  - cline_rule_of_law_backfill — pull CCP + historical legal periodicals, ~500 MB

Periodic jobs:
  - cline_news_features_incremental — daily check for Global News Index updates (new stories added daily)
  - cline_speed_check — monthly check for SPEED additions
```

The 150 GB Global News Index features download is the only cost-sensitive piece. Pre-aggregating to country × month × topic before storing in R2 cuts that to ~20 GB. The full features set lives in cold storage for the future OPENGEM-GPR build.

## What the Cline Center gives OPENGEM that no other source does

Three unique capabilities:

1. **1945→present coverage**, longer than any commercial competitor. Phoenix + SPEED + Coup + CREG span the entire postwar period. This is the substrate for "rewind to 1948 / 1973 / 1989" historical scenario backtests.
2. **Human-validated events** (SPEED) at a granular per-event level. ACLED is the comparable human-validated commercial-grade dataset but is YELLOW; SPEED is GREEN.
3. **Open news corpus features** (Global News Index) suitable for in-house geopolitical-risk index construction without the Factiva dependency that Caldara-Iacoviello have.

The third is the strategic one. OPENGEM building its own GPR-style index on top of Cline Center features is the play that breaks dependence on the Iacoviello monthly drop and makes OPENGEM the *source-of-record* for a new, fully-open geopolitical-risk index. That's a multi-loop project but the Cline Center makes it possible.

## Risks and mitigations

- **Funding instability** — academic centers depend on grants. **Mitigation**: archive each Cline Center release to R2 on download; we own offline copies.
- **Citation drift** — recommended citations occasionally update. **Mitigation**: store the citation string per-vintage in the methodology pop-up; the vintage-rewind page surfaces the citation that was current when the data was used.
- **Schema versioning** — Phoenix has gone through v1.0 → v1.3.0; not all versions are backward-compatible. **Mitigation**: pin the version in the adapter; treat version upgrades as scheduled migration loops.

## Action items

1. Build `opengem-data-cline` package — one adapter module per dataset, shared HTTP-fetch utility, R2 mirror.
2. Run the Phoenix + SPEED + Coup + CREG one-time backfills. Ingest into Iceberg with provenance tags.
3. Plan the Global News Index features ingestion (separate loop — likely Phase 2 since it's large and forward-strategic).
4. Wire SPEED into the L228 Conflict Tracker as the "validated history" toggle.
5. Wire Coup events into the L213 recession-prob feature pipeline (rare-event indicator).
6. Wire CREG into the L222 demography page as background context.
7. Update L282 License Audit table — all Cline Center entries GREEN.

## Comparison summary

| Need | Cline source | Sibling sources |
|---|---|---|
| Live event stream | (POLECAT via Harvard) | GDELT (L021), ACLED (L022, YELLOW) |
| Deep history events | Phoenix 1945- | ICEWS legacy 1995-2022 |
| Human-validated events | SPEED | ACLED (YELLOW) |
| News corpus features | Global News Index | (no GREEN sibling) |
| Coup events | Coup d'état Project | UCDP (L026) one-sided violence |
| Ethnic/religious composition | CREG | (Pew, no GREEN sibling at depth) |
| Constitutional/rule-of-law | CCP, Rule of Law | V-Dem (L027) |

## Related

- [[L001-vision-statement]] — substrate-publishing thesis fits perfectly
- [[L021-gdelt-gkg]] — sibling open-event stream
- [[L023-icews-phoenix-terrier]] — POLECAT/PLOVER lineage
- [[L024-gpr]] — Global News Index is the substrate for OPENGEM-GPR
- [[L026-ucdp]] — sibling GREEN conflict source
- [[L027-vdem]] — sibling GREEN governance source
- [[L173-vintage-time-machine]] — Phoenix backfill enables 1945+ rewinds
- [[L213-recession-prob-page]] — Coup events as features
- [[L222-demography-long-run]] — CREG context
- [[L228-conflict-tracker-page]] — SPEED as validated layer
- [[L282-license-audit]] — Cline Center entries all GREEN

## Sources

- [Cline Center — Resources & Assets](https://clinecenter.illinois.edu/what-we-do/resources-and-assets)
- [Global News Index project page](https://clinecenter.illinois.edu/project/data-science/global-news-index)
- [Global News Index on Illinois Data Bank](https://databank.illinois.edu/datasets/IDB-5649852)
- [Cline Center Historical Phoenix Event Data on Illinois Data Bank](https://databank.illinois.edu/datasets/IDB-2796521)
- [SPEED project](https://clinecenter.illinois.edu/project/human-loop-event-data-projects/SPEED)
- [Machine-generated Event Data Projects](https://clinecenter.illinois.edu/project/machine-generated-event-data-projects)
- [Human-in-the-loop Event Data Projects](https://clinecenter.illinois.edu/project/human-loop-event-data-projects)
- [Archer and the Global News Index — UIUC LibGuide](https://guides.library.illinois.edu/archer)
- [PLOVER and POLECAT paper (joint with OEDA)](https://andrewhalterman.com/files/PLOVER_POLECAT_Halterman_Bagozzi_Beger_Schrodt_Scarborough.pdf)
