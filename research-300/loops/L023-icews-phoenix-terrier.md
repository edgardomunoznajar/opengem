# L023 — ICEWS / Phoenix / TERRIER: status, succession, open-event-tooling ecosystem

**Loop**: 023 / 300
**Phase**: 1 — Open-source landscape survey (geopolitical risk + event data)
**Date**: 2026-06-06
**License tag**: **mixed — ICEWS legacy GREEN (CC0, frozen Apr 2023); POLECAT GREEN (CC0); Phoenix GREEN (Illinois Data Bank default open); TERRIER/PETRARCH code Apache-2.0/MIT**

---

## One-paragraph summary

The CAMEO-event-coder world has been in succession crisis since 2020 and the dust has now (mostly) settled. **ICEWS shipped its last public coded event on April 11, 2023** and was succeeded by POLECAT, hosted on Harvard Dataverse, weekly cadence, machine-coded against the new PLOVER ontology, sponsored by the US government's Program on Geostrategic Risk. The Cline Center continues to ship Phoenix-coded historical event data (1945-2019) as a sibling academic dataset. The open tooling — PETRARCH-2, OEDA, TERRIER, PLOVER — is fragmented but viable; the Halterman/Bagozzi/Beger group is the de facto maintainer. For OPENGEM the play is to lean on **POLECAT** (live, GREEN, weekly) and **Phoenix** (deep history, GREEN, frozen) as the open event-data backbone, with GDELT for volume and ACLED for human-validated edge cases.

## Status of each component (June 2026)

**ICEWS** — discontinued April 11, 2023 as a live public stream. Legacy coded event data 1995-2022 remains on Harvard Dataverse (`doi:10.7910/DVN/28075`) under the Dataverse default CC0 dedication. The Lockheed Martin / IARPA-funded crisis-forecasting model is still maintained internally but the public-facing coded event drops stopped. **Use as: historical backfill 1995-2022 only.**

**POLECAT** (POLitical Event Classification, Attributes, and Types) — the explicit ICEWS successor. Lives on Harvard Dataverse at `doi:10.7910/DVN/AJGVIT` (weekly data) and `doi:10.7910/DVN/LMFPIP` (documentation). Hosted by the Program on Geostrategic Risk (formerly Political Instability Task Force, CIA-adjacent). Coverage 2018-01-01 → present. Updated **hourly internally, posted weekly** on Wednesdays. Coded against PLOVER ontology in seven languages from 1,000+ global news sources by a transformer-based machine coder. Harvard Dataverse default license is CC0 unless the depositor overrode it — POLECAT releases have not flagged a custom license, so it inherits CC0. **Use as: live event stream, primary post-2018 backbone.**

**Phoenix (Cline Center Historical Phoenix Event Data)** — academic CAMEO-coded historical event dataset, 1945-2019, ~8.2M events from 21.2M news stories (NYT, BBC SWB, WSJ, FBIS), coded via PETRARCH-2. Lives on Illinois Data Bank (`databank.illinois.edu/datasets/IDB-2796521`). The Illinois Data Bank default sharing terms are CC0 / open-access unless the depositor specified otherwise; Cline Center datasets have historically been treated as openly redistributable for academic and non-commercial purposes. **Use as: deep historical backfill 1945-2018.**

**TERRIER** (Temporally Extended, Regular, Reproducible International Event Records) — an earlier academic project (Halterman et al, U-Penn) that pre-figured POLECAT. Frozen as a research artifact. Code on GitHub (MIT). **Use as: methodological reference, not live data.**

**PETRARCH / PETRARCH-2** — the open-source CAMEO event coder that powered Phoenix and (earlier versions of) ICEWS. Repos at `openeventdata/petrarch2` (Apache-2.0). Now mostly superseded by transformer-based coders (POLECAT's Mordecai / NGEC pipeline). **Use as: forkable reference coder if we want to run our own pipeline; not necessary if we ingest POLECAT directly.**

**PLOVER** (Political Language Ontology for Verifiable Event Records) — the new event ontology that replaced CAMEO for POLECAT. ~12 event types (assault, coerce, consult, cooperate, mobilize, protest, reject, request, sanction, threaten, etc.) with rich attribute slots. Designed for machine-learning coders. Lives in the Halterman/Bagozzi/Beger/Schrodt/Scarborough working paper.

**OEDA** (Open Event Data Alliance) — the loose academic consortium maintaining the open-event tooling. Active GitHub presence at `openeventdata/`. Not a vendor; not a service; a code substrate.

## Why ICEWS dying matters

ICEWS was the longest-running, most-cited, government-funded political event stream. Its disappearance from the public surface in April 2023 was a near-disaster for academic conflict and crisis-forecasting research. POLECAT was rolled out specifically to fill that hole — same sponsor lineage, different ontology, modern ML coder. The continuity is "mostly there" but the schema break (CAMEO → PLOVER) means you cannot directly concatenate ICEWS 1995-2022 with POLECAT 2018-present without ontology-translation tables. There is a published crosswalk in the PLOVER paper but it is lossy in both directions.

For OPENGEM this resolves cleanly:

- 1945-1994: Phoenix only (Cline Center)
- 1995-2017: Phoenix + ICEWS legacy (overlap years allow validation)
- 2018-2022: ICEWS legacy + POLECAT (overlap years for crosswalk fitting)
- 2023+: POLECAT only (ICEWS no longer ships)

We standardize internally on the PLOVER ontology, translate Phoenix/ICEWS-CAMEO → PLOVER via the published crosswalk, store provenance per row (which coder produced it), and surface PLOVER labels in the public UI with a footnote linking back to the original CAMEO label for pre-2018 events.

## License audit (the thing that matters)

| Component | Default license | OPENGEM tag | Republish derived metrics? |
|---|---|---|---|
| POLECAT weekly data (Harvard Dataverse) | CC0 (Dataverse default) | GREEN | Yes |
| ICEWS legacy 1995-2022 (Harvard Dataverse) | CC0 (Dataverse default) | GREEN | Yes |
| Cline Center Phoenix (Illinois Data Bank) | Open (default) | GREEN | Yes (with citation) |
| PETRARCH-2 source code | Apache-2.0 | GREEN | Yes (Apache compatible with our Apache-2.0 codebase) |
| PLOVER ontology | (academic, citation expected) | GREEN | Yes |
| TERRIER source code | MIT | GREEN | Yes |

The Harvard Dataverse default-CC0 policy is the single most important fact in this loop. It means OPENGEM can mirror POLECAT weekly drops to R2, derive country × month aggregates, publish those aggregates as CC-BY-4.0, and expose them via OPENGEM's public API without negotiating any commercial agreement. POLECAT does what ACLED does (curated political event stream) but under a license that lets OPENGEM honor its CC-BY-4.0 substrate promise.

## Schema (POLECAT, the live one OPENGEM cares about)

POLECAT weekly drops are CSV (often Parquet alongside since v2024) with the following key columns:

- `event_id`, `date`, `hour` (hour-precise timestamp)
- `event_type` (PLOVER root, e.g. ASSAULT, COERCE, COOPERATE, MOBILIZE)
- `event_mode` (subtype slot for the root)
- `event_attributes` (semi-structured slot list: military, civilian, energy, etc.)
- `actor_a`, `actor_b` (entity strings, country codes, roles)
- `location` (geocoded — Mordecai/NGEC pipeline produces ADM1/ADM2 + lat/lon)
- `country` (ISO-3 country of action)
- `intensity` (PLOVER intensity score, -10..+10, replaces Goldstein)
- `confidence` (machine-coder confidence, 0..1)
- `source_url`, `source_name`, `source_lang`
- `multi_source_count` (number of independent sources reporting same event after dedup)

This is conceptually cleaner than CAMEO — fewer event types, richer attribute slots, ML-friendly. The PLOVER intensity scale is z-score-comparable to Goldstein but not identical; methodologically we treat them as separate features rather than concatenating.

## Ingestion pattern for OPENGEM

```
Weekly Wednesday Dagster job:
  1. Poll Harvard Dataverse API for new POLECAT release
  2. Download CSV bundle (~50-200 MB per week)
  3. Validate schema against pinned PLOVER spec
  4. Upsert into local Iceberg `polecat_events` table partitioned by date
  5. Derive: country × week × event_type aggregates
  6. Derive: country × month × intensity aggregates
  7. Publish to R2 + Datasette mirror
  8. Diff against last vintage, log changes
```

For historical backfill we run a one-time job:
```
  1. Download ICEWS legacy bundle (1995-2022) from Harvard Dataverse
  2. Download Cline Center Phoenix bundle (1945-2019) from Illinois Data Bank
  3. Apply CAMEO→PLOVER crosswalk
  4. Backfill `polecat_events` with provenance tag `legacy_icews` / `legacy_phoenix`
  5. Store both raw CAMEO label and translated PLOVER label per row
```

Total historical ingest is ~15-25 GB depending on compression. Comfortable for R2 backing storage.

## Open tooling state

The open-event-tooling ecosystem is small, fragmented, and academic-maintained. As of June 2026:

- `openeventdata/petrarch2` — Apache-2.0 — Python CAMEO coder. Last meaningful commit 2022. Still works but unmaintained.
- `openeventdata/PLOVER` — the ontology repo, mostly docs.
- `andybeger/polecat-data` — community wrappers for the weekly POLECAT releases. MIT.
- `andyhalterman/plover` — Halterman's research code, MIT.
- `ahalterman/mordecai` — Apache-2.0 — the geocoder used in POLECAT (geoparse plus elasticsearch resolution).
- `openeventdata/CAMEO_codes` — the CAMEO codebook in JSON.

OPENGEM does **not** want to maintain its own event coder. The PLOVER → POLECAT pipeline is sophisticated, requires a labeled news corpus we don't have, and would be a years-long sub-project. We consume POLECAT downstream. If we ever want to label OPENGEM-specific events (e.g., financial-sanction announcements that don't make POLECAT's threshold), we can call out to a transformer with a constrained PLOVER prompt — much cheaper than a coder pipeline.

## What goes in the OPENGEM dashboard

- The **L228 Conflict Tracker page** uses POLECAT as primary event source (instead of ACLED) for any view that needs to be free / openly republished.
- The **L229 Sentiment / News Tone page** uses GDELT GKG tone + POLECAT intensity as paired tiles.
- The **forecast feature pipeline** ingests POLECAT country-week event counts by type + intensity as inputs to the L3 ensemble.
- The **historical scenario backtest** (e.g., "rewind to Sept 2008, what did POLECAT/ICEWS show?") uses the legacy ICEWS data to demonstrate the open-vintage time machine in L173.

## Risks

- **Harvard Dataverse policy change**: if Dataverse changes its default-CC0 rule, POLECAT could become more restrictive. **Mitigation**: mirror weekly drops to R2 immediately on release. Each vintage is then versioned and self-archived.
- **Sponsor change**: POLECAT is funded through Program on Geostrategic Risk, which is in the lineage of the CIA-adjacent Political Instability Task Force. Funding cuts could pause publication. **Mitigation**: GDELT as the always-on fallback for live event signal.
- **PLOVER schema drift**: PLOVER is still a research-active ontology. **Mitigation**: pin schema version in the adapter, gate upgrades, run cross-version validation.

## Action items

1. Build `opengem-data-polecat` package — Harvard Dataverse polling adapter, schema validation, weekly Dagster job, R2 mirror.
2. Backfill ICEWS legacy and Cline Center Phoenix as one-time jobs.
3. Implement CAMEO → PLOVER crosswalk module, store both labels per row.
4. Wire POLECAT-derived metrics into L228 Conflict Tracker and L229 News Tone pages.
5. Update L282 License Audit table — POLECAT/Phoenix/ICEWS all GREEN.

## Related

- [[L001-vision-statement]] — the CC-BY-4.0 promise; GREEN sources are the backbone
- [[L021-gdelt-gkg]] — volume signal sibling
- [[L022-acled]] — YELLOW human-validated sibling; POLECAT is the GREEN substitute
- [[L024-gpr]] — derived index sibling; GPR is partly downstream of similar event signal
- [[L025-cline-center]] — sibling loop, Phoenix is treated jointly there
- [[L026-ucdp]] — annual conflict dataset, GREEN
- [[L173-vintage-time-machine]] — uses ICEWS legacy for rewinds
- [[L228-conflict-tracker-page]] — primary visualizer
- [[L282-license-audit]] — POLECAT/Phoenix/ICEWS all GREEN row

## Sources

- [POLECAT Weekly Data on Harvard Dataverse](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/AJGVIT)
- [POLECAT Documentation](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/LMFPIP)
- [ICEWS Dataverse (legacy)](https://dataverse.harvard.edu/dataverse.xhtml?alias=icews)
- [Harvard Dataverse Terms of Use — default CC0](https://support.dataverse.harvard.edu/harvard-dataverse-general-terms-use)
- [Cline Center Historical Phoenix Event Data](https://www.clinecenter.illinois.edu/project/machine-generated-event-data-projects/phoenix-data)
- [Cline Center Phoenix v1.3.0 on Illinois Data Bank](https://databank.illinois.edu/datasets/IDB-2796521)
- [Plover and Polecat paper (Halterman, Bagozzi, Beger, Schrodt, Scarborough)](https://andrewhalterman.com/files/PLOVER_POLECAT_Halterman_Bagozzi_Beger_Schrodt_Scarborough.pdf)
- [Andy Beger — POLECAT event data writeup](https://www.andybeger.com/blog/2024-05-21-polecat-event-data/)
- [openeventdata/petrarch2 on GitHub](https://github.com/openeventdata/petrarch2)
- [Integrated Crisis Early Warning System (Wikipedia)](https://en.wikipedia.org/wiki/Integrated_Crisis_Early_Warning_System)
