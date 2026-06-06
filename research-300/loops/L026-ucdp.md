# L026 — UCDP (Uppsala Conflict Data Program): API, datasets, license, dashboard patterns

**Loop**: 026 / 300
**Phase**: 1 — Open-source landscape survey (geopolitical risk + event data)
**Date**: 2026-06-06
**License tag**: **GREEN — all UCDP datasets CC-BY-4.0; free API with token (Feb 2026+)**

---

## One-paragraph summary

UCDP is the Swedish academic gold standard for armed-conflict measurement and the cleanest GREEN substitute for ACLED's YELLOW human-validated stream. All 18 UCDP datasets are released under **CC-BY-4.0** with per-paper citation requirements. The flagship Georeferenced Event Dataset (GED) provides per-event records back to 1989 globally, geocoded to villages and timestamped to single days. The annual datasets (Armed Conflict, Dyadic, One-Sided Violence, Non-State Conflict, Battle-Related Deaths) extend back to 1946. API access was free-and-anonymous through January 2026 and now requires a free token (introduced February 2026, requested by email with project description). For OPENGEM this is the cleanest, most-cited, most-academically-validated open conflict dataset on Earth — and CC-BY-4.0 means we can republish derived metrics on the public ledger without a EULA tangle.

## What UCDP is

UCDP is a research program at the Department of Peace and Conflict Research, Uppsala University, Sweden, founded ~1971 and continuously publishing armed-conflict data since the mid-1980s. The annual conflict-summary in the *Journal of Peace Research* is the canonical academic citation for "how many wars are happening this year, and how many people died." UCDP is funded through DEMSCORE (Swedish Research Council infrastructure grant 2021-00162).

The methodological commitment is to **strict inclusion criteria with high evidentiary thresholds**: every coded event must have multiple independent sources and at least one fatality. This makes UCDP narrower than ACLED (which codes protest and non-fatal events) but more precise — the events that do appear are real, validated, and per-publication audited.

## The 18 datasets, ranked by OPENGEM utility

UCDP exposes datasets in three groups: disaggregated (event-level), annual (conflict-level), and specialized (peace, support, electoral, etc.).

### Tier 1 — disaggregated, OPENGEM ingests directly

**UCDP GED — Georeferenced Event Dataset**
- 1989-01-01 → present (yearly final + monthly Candidate releases)
- ~500K events total, growing ~30K-50K/year
- Per-event row: location to village level, lat/lon, date to day, dyad ID, fatalities best/low/high, source attribution
- Three violence types: state-based (governments vs. organized opposition), non-state (organized armed actors fighting each other), one-sided (organized actor killing civilians)
- API label: `gedevents`
- Critical column: `type_of_violence` (1=state-based, 2=non-state, 3=one-sided), `dyad_id`, `latitude`, `longitude`, `date_start`, `date_end`, `deaths_*`, `where_coordinates`
- Event ID format: `CCC-YYYY-T-DDDDD-SSSS` (country, year, type, dyad_id, counter)

**UCDP Candidate (monthly)**
- A live updates feed of likely events that haven't yet been fully validated for the next annual GED release. Monthly cadence, ~3-month lag from real-time, validated subset becomes the next GED. Use for live tile signal between annual releases. API version label like `26.0.4`.

### Tier 2 — annual, OPENGEM uses for context and forecast features

**UCDP/PRIO Armed Conflict Dataset (1946-present, annual)**
- One row per active conflict per year
- Conflict type, incompatibility (government, territory, both), intensity, parties
- The dataset every conflict-stats paper of the last 30 years cites
- API label: `ucdpprioconflict`

**Dyadic Dataset (1946-present, annual)** — `dyadic`
**One-Sided Violence (1989-present, annual)** — `onesided`
**Non-State Conflict (1989-present, annual)** — `nonstate`
**Battle-Related Deaths (1989-present, annual)** — `battledeaths`

These five annual datasets are the conflict-stats backbone. Each is small (<10 MB), updates yearly, and provides the long-run "how violent is the world?" panel.

### Tier 3 — specialized

- Peace Agreements Dataset (1975+)
- Conflict Termination Dataset
- External Support Dataset
- Electoral Violence Dataset
- Actor Dataset

OPENGEM ingests these on a per-need basis. The Peace Agreements set drives any "diplomatic momentum" tile; the Electoral Violence set feeds the L227 election-risk page.

## Schema details (GED, the one we ingest live)

The GED CSV/Parquet schema (~50 columns):

- `id` — event UUID
- `relid` — UCDP-internal ID with the format above
- `year`, `active_year` (1 if active)
- `code_status` — clear/coding-in-progress/uncertain
- `type_of_violence` (1/2/3)
- `conflict_dset_id`, `conflict_new_id`, `conflict_name`
- `dyad_dset_id`, `dyad_new_id`, `dyad_name`
- `side_a`, `side_a_new_id` — actor on side A
- `side_b`, `side_b_new_id` — actor on side B
- `number_of_sources`, `source_article`, `source_office`, `source_date`, `source_headline`, `source_original`
- `where_prec` (geographic precision, 1-7)
- `where_coordinates`, `latitude`, `longitude`
- `adm_1`, `adm_2`
- `priogrid_gid` — PRIO grid cell ID (joinable to PRIO-GRID for raster context)
- `country`, `country_id`
- `region`
- `event_clarity` (1-2, how clear the event is)
- `date_prec` (1-5, date precision)
- `date_start`, `date_end`
- `deaths_a`, `deaths_b`, `deaths_civilians`, `deaths_unknown`
- `best`, `low`, `high` — best/low/high fatality estimate
- `gwnoa`, `gwnob` — Gleditsch-Ward country IDs

The `priogrid_gid` is the magic column for spatial joins — it lets OPENGEM combine UCDP events with rainfall, ethnicity, terrain, infrastructure rasters that the PRIO group publishes separately. This is how a serious conflict forecast (think Hegre et al.) ties together violence and structural geography.

## API access

UCDP exposes a REST API at `ucdp.uu.se/api/`. As of February 2026, **token-based authentication is required**. The process:

1. Email the API maintainer with project description.
2. Receive an access token.
3. Include `x-ucdp-access-token: <token>` header in every request.
4. Daily quota: **5,000 requests** (errors count).

Endpoint pattern: `https://ucdp.uu.se/api/<dataset_label>/<version>?<params>`

Example: `/api/gedevents/25.1/?Country=Ukraine&pagesize=500&page=1`

Versioning is explicit and historical versions remain accessible — critical for OPENGEM's vintage-time-machine (L173). Pagination via `page` and `pagesize` (max 1000). Result format: JSON.

**For OPENGEM the practical pattern**: weekly Dagster job pulling Candidate updates for the current year + a yearly job pulling final GED on release (typically June). Full-history bulk downloads available via CSV at `ucdp.uu.se/downloads/`.

## License — CC-BY-4.0 with citation per dataset

This is the cleanest license in the entire L021-L030 portfolio:

> "All UCDP datasets are free of charge and licensed under CC BY 4.0 — you are free to use and redistribute them provided you cite the relevant publications listed with each dataset."

OPENGEM implications:

- We can mirror raw UCDP data to R2 / Datasette.
- We can publish derived per-country aggregates under our own CC-BY-4.0.
- We can expose UCDP-derived rows through our public API and our MCP server.
- We must show the per-dataset citation in the methodology pop-up (e.g., for GED: Sundberg & Melander 2013 + the dataset DOI + the JPR annual update).

Compare to ACLED (YELLOW, EULA-restricted) — UCDP gives us 95% of what ACLED gives us under terms that match our CC-BY-4.0 substrate promise. **For OPENGEM's free-tier, paid-tier, and MCP surfaces, UCDP is the default conflict source. ACLED is the human-curated supplement.**

## Dashboard / render patterns

Looking at how UCDP is rendered in the wild:

1. **UCDP's own conflict-encyclopedia + interactive map** (`ucdp.uu.se`) — the academic benchmark, a Mapbox-driven point map with year filter and conflict drilldown. Nice but slow.
2. **Our World in Data — Wars and Violence section** — clean line charts, country-comparison panels, attribution to UCDP. The aesthetic OPENGEM should match for accessibility.
3. **PRIO Conflict Trends** — annual report with map + bar chart layouts. Print-style.
4. **conflictr (R package)** — opinionated ggplot wrappers for UCDP + ICEWS + PIRO. Useful as a methodological reference.
5. **Python: `basic_api_recipes`** repo from UCDP — official Python scripts for API ingest. Simple, pure-stdlib.

For OPENGEM the **L228 Conflict Tracker** page uses:

- Top tile: live "active conflicts" count from `ucdpprioconflict` plus YTD events from GED Candidate.
- Map: `priogrid` heatmap of GED event density × best-estimate fatalities, last 365 days.
- Country card grid: per-country event count + 5-year trend sparkline.
- Drilldown: country page surfaces dyads, peace-agreement timeline (Peace Agreements dataset), top sources cited.

## Coverage and depth

| Dataset | Start | End | Cadence |
|---|---|---|---|
| Armed Conflict | 1946 | latest +1y | Annual (June release) |
| Dyadic | 1946 | latest +1y | Annual |
| GED | 1989 | latest +1y | Annual + monthly Candidate |
| One-Sided Violence | 1989 | latest +1y | Annual |
| Non-State Conflict | 1989 | latest +1y | Annual |
| Battle-Related Deaths | 1989 | latest +1y | Annual |
| Peace Agreements | 1975 | latest +1y | Annual |

Country coverage: all states with active organized violence since 1946 are coded. Many state-years have zero events (peace). Coverage is genuinely global — Iceland-to-Vanuatu — though deeply weighted toward where conflict actually happens.

## Risks

- **API token requirement is new (Feb 2026).** Adoption is uncertain; some research downstream is breaking. **Mitigation**: register early, mirror CSV downloads to R2 as belt-and-suspenders.
- **Annual release cadence** means GED has a real-time gap covered only by Candidate. **Mitigation**: blend Candidate + GDELT + POLECAT for live tile; mark Candidate rows as "preliminary" in UI.
- **Inclusion-threshold conservatism** — UCDP misses civilian protests, low-intensity violence, and ambiguous events that ACLED would code. **Mitigation**: parallel ACLED-derived tile for context; document the threshold in methodology pop-up.
- **Swedish funding dependency** — DEMSCORE is multi-year but not perpetual. **Mitigation**: this is industry-wide risk; UCDP is too central to vanish, and the data is CC-BY-4.0 so historical archive survives funding shocks.

## Action items

1. Build `opengem-data-ucdp` package — adapter, token env-var, weekly Dagster job for Candidate + yearly for GED.
2. Request the API access token (project description: "OPENGEM World Dashboard — public-accountability ledger; UCDP derived metrics in public dashboard").
3. Backfill all 6 core annual datasets + GED 1989-present from CSV downloads.
4. Wire GED into the L228 Conflict Tracker page as primary source.
5. Wire Battle-Related Deaths + Armed Conflict into the L213 recession-prob feature pipeline (long-run "violence intensity" feature).
6. Add PRIO-GRID join scaffold for spatial enrichment (future).
7. Update L282 License Audit — UCDP all GREEN.

## Comparison to siblings

| Source | License | Cadence | Coverage start | Inclusion threshold |
|---|---|---|---|---|
| GDELT (L021) | GREEN cite | 15 min | 1979 | Permissive |
| ACLED (L022) | YELLOW EULA | Weekly | 1997 (Africa) | Moderate, human-validated |
| POLECAT (L023) | GREEN CC0 | Weekly | 2018 | Machine-coded |
| Phoenix (L025) | GREEN open | Historical | 1945 | Machine-coded |
| **UCDP (this)** | **GREEN CC-BY-4.0** | Annual + monthly | 1946 / 1989 | Strict, fatality-required |

UCDP is the *most academically conservative* of the bunch and the *most license-clean*. For OPENGEM's "publishes its methodology" promise, that combination is gold.

## Related

- [[L001-vision-statement]] — CC-BY-4.0 substrate promise; UCDP fits cleanest of all
- [[L021-gdelt-gkg]] — volume sibling
- [[L022-acled]] — YELLOW human-validated sibling
- [[L023-icews-phoenix-terrier]] — POLECAT live sibling
- [[L025-cline-center]] — SPEED is sibling human-validated GREEN
- [[L027-vdem]] — sibling academic GREEN dataset
- [[L173-vintage-time-machine]] — historical GED enables 1989+ rewinds
- [[L213-recession-prob-page]] — BRD feature
- [[L228-conflict-tracker-page]] — primary visualizer
- [[L282-license-audit]] — UCDP entries all GREEN

## Sources

- [UCDP — Uppsala Conflict Data Program homepage](https://www.uu.se/en/websites/ucdp---uppsala-conflict-data-program)
- [UCDP Dataset Download Center](https://ucdp.uu.se/downloads/)
- [UCDP API documentation](https://ucdp.uu.se/apidocs/)
- [UCDP GitHub — basic_api_recipes](https://github.com/UppsalaConflictDataProgram/basic_api_recipes)
- [UCDP GED Codebook v25.1 (PDF)](https://ucdp.uu.se/downloads/ged/ged251.pdf)
- [Sundberg & Melander 2013 — Introducing the UCDP Georeferenced Event Dataset](https://journals.sagepub.com/doi/10.1177/0022343313484347)
- [conflictr R package](https://dante-sttr.gitlab.io/conflictr/)
- [Mapping global violence — UCDP / One Earth review (2025)](https://www.cell.com/one-earth/fulltext/S2590-3322(25)00220-9)
