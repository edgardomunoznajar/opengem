# L021 — GDELT 2.0 + GKG: schema, ingestion, terms, daily pulse

**Loop**: 021 / 300
**Phase**: 1 — Open-source landscape survey (geopolitical risk + event data)
**Date**: 2026-06-06
**License tag**: **GREEN — republish freely (with citation)**

---

## One-paragraph summary

GDELT 2.0 is the single most important open geopolitical data source on Earth, and its terms of use are unambiguous: "unlimited and unrestricted use for any academic, commercial, or governmental use of any kind without fee," provided every use carries a citation back to gdeltproject.org. For OPENGEM this is the rare combination of GREEN license + global coverage + 15-minute cadence + structured CAMEO codes + tone scores — the building blocks of a daily Geopolitical Pulse tile that no incumbent can put behind a paywall.

## What GDELT actually is (in 2026)

GDELT (Global Database of Events, Language, and Tone) is a Google-hosted ingestion pipeline that scrapes broadcast, print and web news in 100+ languages, runs each article through a CAMEO event-coder (Conflict and Mediation Event Observations), geocodes locations, scores sentiment ("Article Tone"), and emits structured rows every 15 minutes. Three product surfaces matter:

1. **GDELT Event Database (V2.0)** — one row per detected event with actor1, actor2, CAMEO code, geolocation, tone, source URL.
2. **GDELT Global Knowledge Graph (GKG 2.1)** — one row per article with extracted persons, organizations, themes (from the GKG theme taxonomy of ~50,000 categories), emotions (V-Score / GCAM), tone, and a dense network signature.
3. **GDELT DOC 2.0 API** — a search-friendly REST API over the article corpus (since 2017), with full-text search, tone filter, theme filter, and trendline endpoint.

The temporal coverage runs Jan 1, 1979 → present, but GKG-grade extraction begins Feb 19, 2015 (the GDELT 2.0 cutover). Daily ingest is roughly 500K–1M article-rows in GKG and ~3M event-rows on Event 2.0.

## Schema (the parts OPENGEM actually needs)

**Event table (V2.0) key columns**:
- `GLOBALEVENTID` (uint64, primary key, monotonically increasing)
- `Day` (yyyymmdd) and `MonthYear`, `Year`, `FractionDate` (decimal year)
- `Actor1Code`, `Actor2Code` (CAMEO actor codes — country, role, ethnicity)
- `EventCode` (CAMEO 3-digit, ~310 leaf classes)
- `EventRootCode` (CAMEO 2-digit, 20 root classes — VERBAL COOPERATION → MILITARY FORCE)
- `QuadClass` (1=Verbal Coop, 2=Material Coop, 3=Verbal Conflict, 4=Material Conflict)
- `GoldsteinScale` (-10 to +10, conflict intensity)
- `NumMentions`, `NumSources`, `NumArticles` (saliency proxies)
- `AvgTone` (article-tone average, -100 to +100)
- `Actor1Geo_*`, `Actor2Geo_*`, `ActionGeo_*` (lat/lon, ADM1/ADM2 codes, FIPS country)
- `SOURCEURL` (the article that triggered the row)

**GKG (V2.1) key columns**:
- `GKGRECORDID`, `DATE`, `SourceCommonName`, `DocumentIdentifier`
- `V2Themes` (semicolon-separated list of theme codes with char offsets)
- `V2Locations` (geocoded entities)
- `V2Persons`, `V2Organizations` (named entities)
- `V2Tone` (six floats: avg tone, positive score, negative score, polarity, activity ref density, self ref density)
- `GCAM` (the "Global Content Analysis Measures" — ~24K dimensions across 35 affect dictionaries — LIWC, WordNet-Affect, Lexicoder, etc.)
- `AllNames`, `Amounts`, `Quotations`, `SharingImage`, `RelatedImages`

For OPENGEM's Geopolitical Pulse tile we mostly want: GKG `V2Tone` + `V2Themes` + `V2Locations`, plus Event `EventRootCode`, `GoldsteinScale`, `AvgTone`, `NumMentions`, `ActionGeo_CountryCode`.

## Ingestion patterns (three, ranked)

**Tier A — BigQuery public dataset** (`gdelt-bq.gdeltv2.events`, `gdelt-bq.gdeltv2.gkg`, `gdelt-bq.gdeltv2.gkg_partitioned`). Google gives you 1 TB free query/month; GDELT GKG is partitioned by day, so a daily pulse query that scans a single day's partition costs ~3-5 GB. Easily fits in free tier if we cache. **This is the OPENGEM default.** SQL is straightforward, joinable to country tables, supports geographic + thematic aggregation.

**Tier B — Raw 15-min CSV drops** at `http://data.gdeltproject.org/gdeltv2/<yyyymmddhhmmss>.export.CSV.zip` (events), `.gkg.csv.zip`, `.mentions.CSV.zip`. The "lastupdate.txt" pointer file tells you the newest batch. Pull via curl, decompress, parse, ingest into local DuckDB or Iceberg. Self-hosted, no Google dependency, suitable for the offline / "cite this view" reproducibility case.

**Tier C — DOC 2.0 API** (`api.gdeltproject.org/api/v2/doc/doc`). REST, returns JSON. Use for the live "what's the global mood right now?" sidecar widget — rate-limited but free. Not suitable for batch.

For OPENGEM v1 we route the daily Pulse job through **Tier A**, mirror the resulting aggregates to R2 as Parquet for cite-this-view, and use **Tier C** for the live ticker overlay. We never republish raw GDELT — we publish derived aggregates with attribution.

## Terms of use (verbatim, this matters)

> "all datasets released by the GDELT Project are available for unlimited and unrestricted use for any academic, commercial, or governmental use of any kind without fee."
> "any use or redistribution of the data must include a citation to the GDELT Project and a link to this website (https://www.gdeltproject.org/)"

Two implications:

1. **OPENGEM can republish GDELT-derived aggregates under CC-BY-4.0** — the GDELT terms permit it, our citation goes on every chart's methodology pop-up and on the page footer.
2. **The "publishes its mistakes" promise extends to GDELT-driven tiles**: when CAMEO miscodes an event (it does, frequently — Goldstein and CAMEO are noisy), we annotate the miss in the same place as the original signal. This is how we differentiate from incumbents who quietly clean their feeds.

## Country / temporal coverage

- Languages: 100+ (translated to English in real time post-2015)
- Countries: every UN member state, plus most disputed territories (Taiwan, Western Sahara, etc.) — geocoded to ADM1/ADM2.
- Date range: 1979-01-01 → present for Events; 2015-02-19 → present for GKG 2.0+. (Earlier GKG 1.0 records go back to April 2013 but with reduced schema.)
- Update cadence: every **15 minutes** for both Event and GKG streams. Daily aggregate files at the day boundary.

## The daily Geopolitical Pulse tile (the OPENGEM build)

The tile is a single number (the "global pulse score") plus a 90-day sparkline plus a 3-cell top-events strip plus a clickthrough to the world map. Specifically:

- **Score** = z-scored daily count of QuadClass-4 (Material Conflict) events, weighted by `GoldsteinScale` magnitude, divided by the 365-day rolling mean. Output bounded -3..+3.
- **Sparkline** = 90-day daily score series.
- **Top events strip** = the three highest `NumMentions × |GoldsteinScale|` events from the last 24 hours, each with country, CAMEO label, source URL.
- **Map clickthrough** = a globe.gl hot-zone heatmap of `ActionGeo_*` density × Goldstein, last 7 days.

The pulse score gets a sibling "Tone Pulse" tile from GKG `V2Tone`, computed as the cross-article mean of negative tone in geopolitics-tagged articles. Tone is noisier than Event-Goldstein but catches narrative shifts the event coder misses (sentiment ahead of action).

Cost envelope: BigQuery scan ~5 GB/day = within free tier; R2 storage ~50 MB/day = pennies. Daily Dagster job, idempotent re-runs cheap.

## Known issues and OPENGEM mitigations

- **CAMEO drift / miscoding**: actor disambiguation is noisy for nonstate actors, especially Africa/MENA. Mitigation: triangulate against ACLED (L022) and POLECAT (L023/L025) on the event-tracker page.
- **Source bias**: GDELT scrapes English-language wire heavily, so events in English-speaking democracies are overweight. Mitigation: normalize per-country by 365-day baseline (already in the score formula).
- **Article tone is article-level, not event-level**: a heavy-tone article that incidentally mentions an event will inflate that event's tone score. Mitigation: prefer NumMentions × Goldstein for ranking, AvgTone only for narrative tiles.
- **No structured forecast horizon**: GDELT is descriptive, not predictive. The forecast tile feeds off ACLED + UCDP + POLECAT (which have richer event labels), with GDELT supplying volume signal.

## OPENGEM action items

1. Build `opengem-data-gdelt` package mirroring the `opengem-data-gpr` layout — BigQuery adapter, raw-zip fallback, DOC-API adapter, three series IDs (`WORLD.GDELT.PULSE.global.D`, `<country>.GDELT.PULSE.country.D`, `<country>.GDELT.TONE.country.D`).
2. Build the Pulse tile component in `prototypes/dashboard-next` (L237 and L163 will lean on this).
3. Wire methodology pop-up: every Pulse chart shows "Source: GDELT 2.0 (gdeltproject.org), CC-by-attribution" + the SQL behind the aggregate.
4. Backfill 2015 → today into Iceberg/R2 (≈1 TB raw → ≈30 GB aggregated). Single BigQuery job; pre-aggregate to daily country × root-code grid.

## Why this is critical for the moat

GDELT is the open substitute for what Bloomberg sells through its "Geopolitical Risk Monitor" overlay and what Stratfor sells through editorial newsletters. Both incumbents charge for *interpretation*; GDELT lets OPENGEM publish the *substrate* the interpretation rides on, machine-readable, daily, free. The asymmetry from L001 — "publishes its mistakes" — applies directly: GDELT's noise is *visible*, and the methodology pop-up makes that visibility part of the brand instead of a liability.

## Related

- [[L001-vision-statement]] — the publish-the-substrate asymmetry
- [[L022-acled]] — narrow-scope sibling (curated conflict events, YELLOW license)
- [[L023-icews-phoenix-terrier]] — POLECAT now the open successor to ICEWS
- [[L024-gpr]] — Caldara-Iacoviello GPR is partly downstream of GDELT themes
- [[L163-geopolitical-pulse-map]] — the visualizer this loop feeds
- [[L237-gpr-pulse-globe-prototype]] — the prototype code target

## Sources

- [GDELT Project — About / License](https://www.gdeltproject.org/about.html)
- [GDELT Data / Querying](https://www.gdeltproject.org/data.html)
- [GDELT Event Codebook V2.0 (PDF)](http://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf)
- [GDELT GKG Codebook V2.1 (PDF)](http://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_Codebook-V2.1.pdf)
- [GDELT DOC 2.0 API debut](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)
- [BigQuery + GDELT walkthrough](https://www.jamelsaadaoui.com/bigquery-with-gdelt/)
