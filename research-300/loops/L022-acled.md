# L022 — ACLED: API, license tiers, country coverage, derived-metric republishing

**Loop**: 022 / 300
**Phase**: 1 — Open-source landscape survey (geopolitical risk + event data)
**Date**: 2026-06-06
**License tag**: **YELLOW — cite-only with restrictions; derivative metrics permitted only if transformative**

---

## One-paragraph summary

ACLED (Armed Conflict Location & Event Data Project) is the gold-standard human-curated conflict event dataset — 200+ countries, weekly cadence, granular event types, validated by humans, geocoded to settlement level. It is also a **YELLOW license source**: ACLED data is not Creative Commons, it is governed by ACLED's own EULA which permits non-commercial use, requires explicit attribution, and bans dashboards that "compete with" or "create a functional substitute for" ACLED's own platforms. For OPENGEM this means: cite-yes, ingest-yes, republish-derived-aggregates-yes (if transformative), republish-raw-dataset-no, replace-ACLED-Dashboard-no. We can render a recession-relevant conflict tile; we cannot mirror their event-export tool.

## What ACLED is

ACLED is a 501(c)(3) non-profit registered in the US, founded 2014, with a global research staff coding political violence and protest events from local press, NGO reports, and verified social media. It is the de facto reference dataset for conflict research and humanitarian operations — used by UN OCHA, USAID, HRW, AP, Reuters, and most of the academic conflict-econ literature.

The dataset coverage as of 2026:

- **200+ countries and territories** including all of Africa, Middle East, South & Southeast Asia, Europe, Latin America, North America, East Asia, Caucasus, Central Asia. Coverage is now genuinely global since the 2022 European expansion.
- **Six event types**: Battles, Explosions/Remote violence, Violence against civilians, Protests, Riots, Strategic developments. Each with subtypes.
- **Variables per event**: date, country, ADM1/ADM2, settlement, lat/lon, actor1, actor2, fatalities, source URL, free-text notes.
- **Cadence**: real-time coding; **weekly release** to the API and Data Export Tool on Mondays/Tuesdays for the prior week.
- **Time depth**: varies by region. Africa back to 1997; Middle East to 2015; Asia to 2018; Latin America to 2018; US to 2020; Europe to 2020 (full); historical backfills ongoing.

## Access surface

Three legitimate entry points:

1. **ACLED API** (`api.acleddata.com`) — REST/JSON, requires registered account + API key. Endpoints: `acled_read`, `actor_read`, `actor_type_read`, `country_read`, `region_read`. Pagination via `page=` (500 rows/page). Tested rate limit: ~10 requests/sec sustainable, no published hard cap but anti-abuse triggers.
2. **Data Export Tool** (UI, CSV/Excel) — same data, manual download. Useful for ad-hoc, not for OPENGEM ingestion.
3. **Curated Data Files** — region-bundled CSV/Excel snapshots updated weekly.
4. **HDX mirror** (`data.humdata.org/organization/acled`) — 246 datasets, country-by-country, useful for backfills, same license terms.

R-package wrappers exist (`acled.api` on CRAN; `acledR`). Python wrappers (`acled`, `acleddata`) are community-maintained. The OPENGEM adapter should be vendored and not depend on third-party wrappers — the API is simple enough that direct calls are cheaper than a transitive dependency.

## The license — what OPENGEM can and cannot do

This is the most important paragraph in this loop. Quoting the ACLED EULA verbatim and parsing:

> "Licensee may only publish or distribute materials incorporating ACLED's data where such materials are transformative in nature"
> "Licensed Content [must not be] simply ... supplemented, appended, excerpted, reorganized, or made available through Licensee's own dashboard"
> "Licensee is not permitted to reproduce, republish, redistribute, or create derivative works from any of ACLED's Analysis, photographs, or videos"
> "[Licensee cannot] create or develop any dataset, product, or platform that competes with, or creates a functional substitute for, any of ACLED's content, products, or platforms"

What this lets OPENGEM do:

- **Compute and publish derived metrics** (e.g., "conflict-event z-score by country, last 90 days") *if* the metric is transformative and not just a remix of the raw rows.
- **Cite ACLED inline** as a source on a methodology pop-up, including DOI and access date.
- **Show an aggregate map** of country-level monthly conflict intensity, as long as users can't drill down to row-level event detail.
- **Compute forecast features** from ACLED that feed an OPENGEM L3 forecast — features are derivative, not redistributed data.

What this prohibits OPENGEM from doing:

- **Republish raw event rows** via API, JSON download, embeddable widget, or "open data mirror."
- **Build a dashboard that replicates ACLED's own Dashboard or Data Export Tool** — even with attribution.
- **Republish ACLED's photos, narrative analysis, or weekly Situation Reports.**

For a project whose first promise is "everything we publish is CC-BY-4.0," ACLED introduces an **island of YELLOW** in an otherwise GREEN ledger. The correct framing is to treat ACLED-derived tiles as "computed from ACLED data under their EULA — link to license — full attribution — derived metrics only." The methodology pop-up names ACLED explicitly so the user can re-license-check if they paste an OPENGEM number into a paywall product.

## Cost / tiering

There is no published "academic vs commercial" price card on the public site. The structure as of 2026:

- **Open Access Account** (free, registered) — API access, weekly data downloads, "non-commercial use only" per the EULA.
- **myACLED Subscriber tiers** (paid, undisclosed pricing, negotiated) — for commercial use, including news media, financial services, and consulting. Required if you "monetize" derivative products.

For OPENGEM's paid tier (API throughput, MCP throughput, white-label embeds — see L006), the trigger for needing a commercial ACLED contract is the moment we charge customers for derivative ACLED metrics. The conservative read: any ACLED-derived metric that flows through a paid OPENGEM endpoint needs a commercial agreement.

The pragmatic read for v1: launch with ACLED-derived tiles in the free public dashboard only (where "transformative non-commercial" applies), keep them out of the paid API surface until we have a commercial agreement in hand.

## Country coverage detail (the part that affects OPENGEM forecasts)

| Region | Earliest start | Confidence as forecast feature |
|---|---|---|
| Africa | 1997 | High — deepest history, best validated |
| Middle East | 2015 | High — current, dense |
| South Asia | 2010 | High |
| Southeast Asia | 2018 | Medium — short panel |
| East Asia | 2018 | Medium — sparse, journalism-bias |
| Europe | 2020 (full) | Medium — short panel, Ukraine spike dominates |
| LATAM | 2018 | Medium |
| US | 2020 | Low for forecasting — short, protest-dominated |
| Central Asia / Caucasus | 2018-2020 | Medium |

For OPENGEM's "conflict-driven recession-risk" feature, we mostly want Africa, Middle East, South Asia, and the post-2020 European panel. The US ACLED panel is too short and too protest-skewed to drive a US macro feature.

## How OPENGEM uses ACLED

Two primary use cases:

1. **L228 Conflict Tracker page** — a per-country conflict-event sparkline + map + actor table. The page renders aggregated weekly counts with ACLED attribution; raw event rows are *not* exposed as JSON download (that would trip the "functional substitute" clause). Drill-down goes to ACLED's own page via outbound link, not in-app.
2. **Forecast feature pipeline** — conflict-event z-score, civilian-fatalities lag, protest density become input features to the L3 ensemble for country-level recession-prob and FX-misalignment forecasts. Features are not republished; only the resulting forecast distributions are.

Both use cases survive the EULA if attribution is clean and the aggregations are coarser than per-event.

## Risks and mitigations

- **Risk**: ACLED revokes our key for perceived EULA violation. **Mitigation**: pre-launch legal review of every ACLED-touching surface; conservative aggregation thresholds (no per-event download); maintain a "compliance log" page documenting what's published and why it's transformative.
- **Risk**: ACLED changes pricing or commercializes API access. **Mitigation**: maintain a fallback computed entirely from GDELT QuadClass-4 + UCDP GED, with a documented quality gap. The fallback is worse but ungated.
- **Risk**: ACLED selectively de-platforms competitors (it has been accused of this historically). **Mitigation**: the GDELT/UCDP fallback above; aggressive attribution that makes OPENGEM more a complement than a substitute.

## Action items

1. Build `opengem-data-acled` package — adapter, API-key env var, weekly Dagster job, ingestion to Iceberg with full row-level audit (private) and country-monthly aggregates (public, derived).
2. Draft the "ACLED methodology pop-up" template (attribution, transformative-aggregation statement, link to ACLED EULA).
3. Decide before v1 launch: do we want a commercial ACLED agreement, or do we keep ACLED-derived metrics free-tier only and rely on UCDP + GDELT for the paid API surface? My call: free-tier only for v1, revisit at first paid customer milestone.
4. Build the GDELT+UCDP fallback metric for L228 so that if ACLED access breaks, the page still renders.

## Comparison to siblings

| Source | License | Cadence | Coverage | Use in OPENGEM |
|---|---|---|---|---|
| GDELT (L021) | GREEN (cite-only) | 15 min | Global | Primary geopolitical pulse |
| ACLED (this loop) | YELLOW (EULA) | Weekly | Global, human-validated | Conflict tracker page; forecast features |
| UCDP (L026) | GREEN (CC-BY-4.0) | Annual + monthly candidate | 1989+ global | Long-run conflict history; forecast features |
| POLECAT (L025) | GREEN (Harvard Dataverse default CC0) | Weekly | 2018+ global | Event labeling; backfill |

The ACLED YELLOW row sits next to two GREEN siblings that do most of what ACLED does. The reason we still want ACLED: human curation quality, fine-grained event subtypes, and the protest layer that UCDP doesn't carry.

## Related

- [[L001-vision-statement]] — the CC-BY-4.0 promise creates the YELLOW tension
- [[L021-gdelt-gkg]] — the GREEN fallback
- [[L023-icews-phoenix-terrier]] — POLECAT successor, also GREEN
- [[L026-ucdp]] — the cleanest CC-BY-4.0 conflict source
- [[L085-acled-rate-limit-feasibility]] — followup on commercial-tier need
- [[L228-conflict-tracker-page]] — the visualizer this loop feeds
- [[L282-license-audit]] — must list ACLED in the YELLOW column

## Sources

- [ACLED — homepage](https://acleddata.com/)
- [ACLED EULA](https://acleddata.com/eula)
- [ACLED API documentation](https://acleddata.com/acled-api-documentation)
- [ACLED Content Usage Terms](https://acleddata.com/contentusage)
- [ACLED 2023 FAQ — Terms of Use, Attribution Policy, Data Access (PDF)](https://acleddata.com/sites/default/files/wp-content-archive/uploads/2023/07/ACLED_Terms-of-Use-Attribution-Access_FAQs_2023.pdf)
- [ACLED on HDX](https://data.humdata.org/organization/acled)
- [acled.api R package on CRAN](https://cran.r-project.org/web/packages/acled.api/acled.api.pdf)
