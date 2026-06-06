# L029 — Stratfor public archive + OSINT mirrors: what's open, what's citable, what's radioactive

**Loop**: 029 / 300
**Phase**: 1 — Open-source landscape survey (geopolitical risk + event data)
**Date**: 2026-06-06
**License tag**: **mixed — Stratfor live: RED (paid subscription); Stratfor WikiLeaks gifiles: RED for republication (copyright fair-use risk, citation OK); Bellingcat articles: YELLOW (copyright, citation/fair-use OK, toolkit CC-BY-ND); OCCRP/Aleph: YELLOW (per-source license); Geopolitical Futures: RED (paid); OSINT tooling code: GREEN (most MIT)**

---

## One-paragraph summary

Of the L029 sources, **none are GREEN data sources OPENGEM can ingest as a substrate**. Stratfor is paywalled and editorialized — the "free access" articles are marketing, not a feed. The 5.5M-email WikiLeaks gifiles archive is publicly accessible and frequently cited but legally radioactive for systematic republication (Stratfor copyright is intact; *citing* the archive is fine; *republishing or mirroring* invites a takedown, and even citing relies on the same fair-use posture as the journalists who first published the archive in 2012). Bellingcat publishes investigation articles under a "all rights reserved" model with an explicit fair-use citation culture; the *toolkit* (a separate artifact) is CC-BY-ND. OCCRP's Aleph platform aggregates leaked corporate registries under per-source licensing that varies wildly. The strategic takeaway: this whole layer is **analyst-grade OSINT for narrative citation, not a substrate OPENGEM can mirror**. The right OPENGEM behavior is to *link out*, not to *ingest*. The MCP server can surface OSINT context; the dashboard's substrate stays grounded in GREEN sources (GDELT, UCDP, POLECAT, Cline Center).

## What's in this layer

### Stratfor / RANE Worldview

Strategic Forecasting Inc., founded 1996 by George Friedman, sold to RANE Network in 2020. Operates `worldview.stratfor.com` as a subscription geopolitical-analysis publisher — annual geopolitical forecasts, country assessments, "Snapshots" (event commentary), columns. Pricing as of 2026 is enterprise-grade ($3K-$10K+ per seat). A small fraction of articles are tagged "Free Access" for marketing.

**License for OPENGEM**: RED. The live product is paywalled and copyrighted. There is no public API, no data feed, no JSON. OPENGEM cannot ingest Stratfor Worldview content. We can *link* to the occasional Free Access article in narrative context, and we can *cite* Stratfor as a benchmark forecaster on the L190 forecast-leaderboard page. We do not *quote at length*, *mirror*, or *aggregate* their text.

The methodologically useful thing about Stratfor: their *public forecasts* (the annual Geopolitical Forecast, published every January) become *public benchmarks* OPENGEM can score against. We don't have to consume their text to track their published forecasts — we just need a "this is what Stratfor's 2026 annual forecast predicted" data point we can compare against actual outcomes a year later. This makes Stratfor a *competitor whose track record OPENGEM exposes*, not a substrate we depend on.

### WikiLeaks Global Intelligence Files (gifiles)

Released Feb 27, 2012 — 5,543,061 Stratfor emails dated July 2004 to December 2011. Hosted at `wikileaks.org/the-gifiles.html` with full-text search. Published in partnership with 25+ media organizations including Rolling Stone, La Repubblica, McClatchy, l'Espresso.

**License/legal status**: complex. Stratfor's copyright in the email text is *intact* — the emails were stolen by Jeremy Hammond (since incarcerated and pardoned). WikiLeaks' publication and the 25 newsroom partners' use rest on fair-use journalism precedent (Pentagon Papers lineage). For a researcher to *cite* the archive — author, date, link — is standard practice and accepted in academic and journalistic contexts. For OPENGEM to *mirror, index, or republish* the archive in any systematic form: legally radioactive. Stratfor (now RANE) could plausibly issue takedowns or pursue claims.

The pragmatic OPENGEM treatment: **we do not ingest gifiles in any form**. If a methodology pop-up needs historical context that the gifiles provided (e.g., "Stratfor was tracking X in 2008"), we link out to the specific WikiLeaks page. We do not copy email text into our own pages.

The strategic value of gifiles for OPENGEM is mostly *cultural*: it remains the public-archive proof that the geopolitical-intelligence industry has historically operated as opaque, closed, error-prone, sometimes-corrupt. That's a backdrop story OPENGEM can reference when articulating the "publish the substrate, open the ledger" thesis. But the archive is not a data source.

### Bellingcat

The open-source investigative collective founded by Eliot Higgins in 2014, now a non-profit Stichting registered in the Netherlands. Publishes investigations on `bellingcat.com` with full sourcing and reproducible methodology. Best known for MH17 investigation, Syria chemical-weapons attribution, Skripal poisoning identification, Wagner operations.

**License status**:
- Published articles: traditional copyright "all rights reserved" on the article text. Fair-use citation is accepted; mirroring or systematic republication is not. The Library of Congress collects them with copyright preserved.
- **Bellingcat Online Investigation Toolkit** (`bellingcat.gitbook.io/toolkit`): explicitly licensed **CC-BY-ND 4.0** (Creative Commons Attribution-NoDerivatives 4.0 International). This is the catalog of OSINT tools they curate — usable, citable, downloadable as CSV. No derivatives.
- **Bellingcat code repos** on GitHub (`github.com/bellingcat/auto-archiver`, etc.): mostly **MIT** licensed. Auto-archiver, dog-tag-extractor, various OSINT helpers — all reusable.
- **Bellingcat editorial standards**: explicitly forbid using generative AI to create copy, images, or video in their publications. This is editorial policy, not a license, but it signals seriously about journalistic provenance.

**For OPENGEM**: Bellingcat is a citation source for narrative pages (Russia/Ukraine context, sanctions evasion stories, etc.). The toolkit is YELLOW — useful to reference and link, but no-derivatives means we can't repackage the curation into our own UI. The MIT code repos are GREEN — Auto-archiver in particular is the canonical open-source URL/social-media archiving tool, useful for OPENGEM's own provenance pipeline.

### OCCRP / Aleph

Organized Crime and Corruption Reporting Project. Aleph is OCCRP's open-source structured-data-search platform (`docs.alephdata.org`) that aggregates over 1 billion records — company registries, sanctions lists, person-of-interest databases, land registries, offshore leaks, etc. The **code is open source** (`alephdata/aleph` is MIT). The **data** is per-source: OCCRP's own leaks (Panama Papers, Paradise Papers, FinCEN Files) carry restrictive embargoes for some uses; OpenCorporates data inside Aleph carries OpenCorporates' own terms; OFAC sanctions data inside Aleph is public-domain US-gov.

**For OPENGEM**: Aleph code is GREEN (MIT) — interesting reference architecture for our own entity-search layer. Aleph data is YELLOW-mixed — we don't ingest. We link out to specific Aleph entities when narrative pages need it. Aleph and OpenSanctions (L028) share the FollowTheMoney ontology, so any OPENGEM tooling that handles FtM works against both.

### OSINT Industries / Maltego / commercial OSINT platforms

`osint.industries` is a paid commercial OSINT enrichment service. Maltego is the long-running graph-based OSINT investigation platform (paid). **Both RED for OPENGEM** — closed platforms, paid licenses, no public substrate.

### Geopolitical Futures (George Friedman post-Stratfor)

`geopoliticalfutures.com` — Friedman's post-Stratfor publication. Same model: paid subscription, editorial geopolitical analysis. **RED for OPENGEM**. Same treatment as Stratfor: link occasional free articles, track publicly-stated forecasts for the leaderboard.

## What's legally radioactive vs what's safe

Decision table:

| Action | Stratfor live | gifiles | Bellingcat articles | Bellingcat toolkit | Bellingcat code | OCCRP Aleph data | Aleph code |
|---|---|---|---|---|---|---|---|
| Cite (author, date, link) | OK | OK | OK | OK | OK | OK | OK |
| Quote brief excerpt fair-use | OK | OK | OK | OK | n/a | OK | n/a |
| Link out | OK | OK | OK | OK | n/a | OK | n/a |
| Mirror text | NO | NO | NO | NO | OK (MIT) | NO | OK (MIT) |
| Index / search in own UI | NO | NO | NO | NO | OK | NO | OK |
| Republish as data feed | NO | NO | NO | NO | OK | NO | OK |
| Use as forecast feature | NO | NO | NO | NO | OK | NO | OK |
| Use as competitor benchmark (track public forecasts) | OK | n/a | OK | n/a | n/a | n/a | n/a |
| Use as MCP tool context (LLM grounded) | OK (link out) | risky | OK (link out) | OK | OK | OK (link out) | OK |

The risk surface OPENGEM cares about most: **the MCP server**. An LLM with OPENGEM's MCP tools could be tempted to ingest Bellingcat or Stratfor text wholesale into its context window if we expose a "fetch this URL" tool. The right design: MCP exposes *structured OPENGEM data* and *outbound links*; it does not exfiltrate copyrighted text from third-party sources into LLM contexts on our behalf. This is both a legal and an epistemic stance — citations should link to the source, not paraphrase it through OPENGEM's reputation.

## What OPENGEM should do with this layer

Five concrete behaviors:

1. **Stratfor and Geopolitical Futures**: track publicly-stated annual forecasts (which are press-released and citable). Score them against actual outcomes on the L133 forecast leaderboard alongside IMF WEO, OECD EO, FRB SEP. This is the *exactly* the L008 differentiation play — incumbents' track records are usually private; OPENGEM makes them public by scoring the few forecasts they have publicly committed to.
2. **gifiles**: zero ingestion. Mention in the L300 "history of opacity" narrative essay only.
3. **Bellingcat articles**: link out from narrative pages (L228 Conflict Tracker, L225 Sanctions page, individual country pages where Bellingcat has done relevant work). Do not embed text.
4. **Bellingcat toolkit**: link out from OPENGEM's own glossary / methodology pages. Reference, don't repackage.
5. **Bellingcat code + Aleph code**: review for reusable substrate. Auto-archiver is the obvious one — OPENGEM's own provenance pipeline benefits from a standardized URL archiver. Aleph's FtM tooling pairs with OpenSanctions (L028).

## What this teaches about OPENGEM's substrate philosophy

The Stratfor lineage is a useful negative example. Their value proposition was "we read 100 sources and write you the analysis"; their margin came from the *opacity* of that process. OPENGEM's value proposition inverts: "we ingest the 100 sources publicly, score them publicly, and our analysis is built on the public substrate." Stratfor cannot publish its sources because then the customer doesn't need Stratfor. OPENGEM has no customer at the editorial layer — the editorial is generative-LLM narrative on top of the substrate — so we have no reason not to publish.

This means the L029 sources are not a *gap* in OPENGEM's coverage. They are a *category we deliberately don't compete in*: closed editorial geopolitical analysis. We compete with them by exposing the substrate underneath their analyses and scoring their public forecasts. We do not become them.

## Risks

- **Reputation: looking too aggressive towards Stratfor/Friedman lineage**. The forecast-leaderboard play needs to be evidence-driven, not adversarial. **Mitigation**: rigorous scoring, neutral language, full attribution. "Stratfor 2024 Annual Forecast predicted X; actual: Y; CRPS: Z." Numbers, not narrative.
- **Accidentally crossing fair-use into infringement**. A page that quotes too much Bellingcat text is a takedown risk. **Mitigation**: editorial review checklist for any page that cites L029 sources; default to link-out over excerpt.
- **MCP exfiltration vector**. As described above. **Mitigation**: MCP tool design refuses to fetch arbitrary URLs and stuff into context; instead returns structured OPENGEM data + outbound link annotation.

## Action items

1. Build the L133 Forecast Leaderboard schema to accept Stratfor / Geopolitical Futures public annual forecasts as benchmark entries.
2. Audit MCP tool surface to ensure no tool fetches third-party copyrighted text into LLM context.
3. Adopt Bellingcat Auto-archiver in OPENGEM's provenance pipeline (MIT, drop-in).
4. Add per-source license-tagging to OPENGEM's narrative-CMS so editors can't accidentally embed copyrighted text from L029 sources.
5. Update L282 License Audit with the full L029 matrix (Stratfor RED, gifiles RED for republication, Bellingcat YELLOW, OCCRP YELLOW-mixed, Aleph code MIT GREEN, Bellingcat code MIT GREEN, etc.).
6. Add L300 narrative-essay placeholder: "Why we don't ingest the gifiles."

## Related

- [[L001-vision-statement]] — the publish-the-substrate thesis is precisely *not* what Stratfor sells
- [[L008-differentiation]] — "publishes its mistakes" is the L029-adjacent moat
- [[L022-acled]] — sibling YELLOW source
- [[L024-gpr]] — academic open-substrate sibling
- [[L028-opensanctions]] — sibling FollowTheMoney-ontology source
- [[L030-geopolitical-risk-indices-comparison]] — Stratfor / EIU / etc. ranked there
- [[L133-forecast-leaderboard]] — Stratfor public forecasts scored here
- [[L282-license-audit]] — L029 sources mapped to RED/YELLOW
- [[L300-final-synthesis]] — narrative essay placeholder

## Sources

- [Stratfor Worldview](https://worldview.stratfor.com/)
- [Stratfor — Wikipedia](https://en.wikipedia.org/wiki/Stratfor)
- [Stratfor email leak — Wikipedia](https://en.wikipedia.org/wiki/2012%E2%80%9313_Stratfor_email_leak)
- [WikiLeaks Global Intelligence Files](https://wikileaks.org/the-gifiles.html)
- [Geopolitical Futures](https://geopoliticalfutures.com/welcome/)
- [Bellingcat](https://www.bellingcat.com/)
- [Bellingcat — Editorial Standards & Practices](https://www.bellingcat.com/about/editorial-standards-practices/)
- [Bellingcat Online Investigation Toolkit (CC-BY-ND 4.0)](https://bellingcat.gitbook.io/toolkit)
- [bellingcat/auto-archiver on GitHub (MIT)](https://github.com/bellingcat/auto-archiver)
- [Bellingcat — Wikipedia](https://en.wikipedia.org/wiki/Bellingcat)
- [OCCRP Aleph documentation (Bellingcat toolkit entry)](https://bellingcat.gitbook.io/toolkit/more/all-tools/occrp-aleph)
- [OCCRP Aleph Transforms for Maltego](https://www.maltego.com/transform-hub/occrp-aleph/)
- [Library of Congress — Bellingcat web archive](https://www.loc.gov/item/lcwaN0035331/)
