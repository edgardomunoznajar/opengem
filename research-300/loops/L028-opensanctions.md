# L028 — OpenSanctions: dataset, API, license, sanctions-risk tile

**Loop**: 028 / 300
**Phase**: 1 — Open-source landscape survey (geopolitical risk + event data)
**Date**: 2026-06-06
**License tag**: **YELLOW — code MIT (GREEN), data CC-BY-NC (non-commercial only — commercial use requires paid license)**

---

## One-paragraph summary

OpenSanctions is the world's best open-data aggregation of sanctions lists, politically-exposed persons (PEPs), criminal entities, and adverse-media-flagged actors — 2.77M entities consolidated from 337 source lists, updated daily, hosted on a clean public infrastructure with a documented yente entity-matching API. Source code is MIT (GREEN), but **the data is licensed CC-BY-NC** — non-commercial use only; any commercial use (including OPENGEM's paid API tier and any white-label embed for a paying customer) requires a paid license. For OPENGEM v1 this means: free public sanctions-risk tile uses OpenSanctions under CC-BY-NC with explicit attribution; the paid API does not expose OpenSanctions-derived rows until we have a commercial agreement; the self-host option (yente + bulk download) is the architectural fallback that decouples cost from per-request metering.

## What OpenSanctions is

OpenSanctions, founded ~2019 by Friedrich Lindenberg (formerly of OCCRP and Aleph), is a German-Czech non-profit-adjacent commercial venture that runs scrapers against 337+ official sources — OFAC SDN lists, EU consolidated sanctions, UK HMT, UN Security Council, Russian Ministry of Internal Affairs wanted lists, regional regulator watchlists, debarment registries, public company filings, PEP databases — and normalizes them into a single FollowTheMoney ontology. The result is consolidated, deduplicated, and machine-queryable.

The org structure is the most interesting part: open-source code (the `opensanctions/opensanctions` scrapers and the `yente` matching API are MIT-licensed), open data (CC-BY-NC), and a paid commercial license for businesses. This is the now-common dual-license commercial-open-source pattern, applied to a domain (sanctions compliance) where the customer is willing to pay because the alternative is regulatory fines.

## What's actually in it (as of June 2026)

| Collection | Entity count | Cadence |
|---|---|---|
| Consolidated Sanctions | 99.5K | Daily |
| OpenSanctions Default (quality screen) | 2.77M | Multiple times daily |
| Politically Exposed Persons (PEPs) | 936K | Daily |
| Sanctioned Securities | 1.01M | Daily |
| Debarment lists | 220K | Daily |
| Criminal/Warrants | 261K | Daily |
| Regulatory Watchlists | 166K | Daily |
| Maritime Sanctions (vessels) | 135K | Daily |
| Know-Your-Business (KYB) | 102.9M | Monthly |

The KYB dataset is the largest by far — bulk-corporate-registry data, monthly cadence. Most of OpenSanctions' commercial revenue comes from KYB customers (financial-crime compliance, beneficial-ownership investigations). For OPENGEM's geopolitics dashboard, the most relevant slices are **Consolidated Sanctions, PEPs, Sanctioned Securities, and Maritime Sanctions** — these power the daily Sanctions-Risk tile, the country-level sanctions exposure breakdown, and the optional supply-chain overlay.

## Schema (FollowTheMoney ontology, OpenSanctions flavor)

Every entity is represented as a FollowTheMoney (FtM) object — a graph-shaped data model with named entity classes (Person, Company, Vessel, Address, etc.) and typed properties.

Per-entity row example:
- `id` — stable OpenSanctions ID
- `caption` — human-readable name
- `schema` — FtM class (`Person`, `Company`, `Organization`, `Vessel`, etc.)
- `properties` — typed property dict (`name`, `birthDate`, `nationality`, `country`, `address`, `sanctionTarget`, `sourceUrl`)
- `target` — boolean: is this entity sanctioned itself
- `referents` — alternative IDs from source registries
- `datasets` — which OpenSanctions collections this entity appears in
- `last_seen`, `first_seen` — temporal provenance
- `topics` — tagged risk categories: `sanction`, `sanction.linked`, `crime`, `crime.fin`, `role.pep`, etc.

The schema is FtM-standard; the same model powers Aleph (`alephdata.org`), OCCRP's investigative platform. This means tooling is interoperable and the OPENGEM ingestion can reuse libraries from Aleph's ecosystem.

## API surface (yente)

Two production-ready APIs:

1. **Hosted API at `api.opensanctions.org`** — REST/JSON, three endpoint families:
   - `/search/<scope>` — fuzzy name search, paginated
   - `/match/<scope>` — bulk entity matching with the Reconciliation API spec
   - `/entities/<id>` — entity lookup
   - Pay-as-you-go metering; free trial keys for journalists, activists, academic research; business email = free tier with quota; commercial use = paid license
2. **Self-hosted via `opensanctions/yente`** (MIT) — Docker image, runs against the bulk data download (CC-BY-NC for non-commercial; paid license for commercial). **The self-hosted path bypasses per-request metering** — bulk-data license + own infrastructure cost only.

For OPENGEM the architecturally honest path is **self-hosted yente against weekly bulk data**, because:
- Avoids per-request metering surprises if traffic spikes (Substack post goes viral; LLM agent hammers the MCP server).
- Keeps the entity matching service inside OPENGEM's R2/Cloudflare boundary.
- Decouples OPENGEM availability from OpenSanctions hosted-API uptime.
- Forces us to make the commercial-license decision once, not per-request.

## License — the YELLOW heart

> "OpenSanctions is free for non-commercial users. Businesses must acquire a data license to use the dataset."
> "The code within this repository is licensed under the MIT License. For content and data, we adhere to CC 4.0 Attribution-NonCommercial."

The line between "non-commercial" and "commercial" is intentionally fuzzy in CC-BY-NC; OpenSanctions resolves this by drawing the line at *business use*. The relevant question for OPENGEM is whether our paid tier (API throughput, MCP throughput, white-label embeds) constitutes commercial use that requires a license. The answer is almost certainly **yes** — once a paying customer hits an OpenSanctions-backed endpoint, we have crossed the threshold.

Three OPENGEM commitments that follow:

1. **Free public dashboard** uses OpenSanctions under CC-BY-NC with prominent attribution. The Sanctions-Risk tile, country-page sanctions exposure card, and supply-chain overlay all qualify as non-commercial use as long as the public-facing surface is free.
2. **Paid API and MCP server** do not expose OpenSanctions-derived rows until OPENGEM has a commercial agreement in hand. Pre-launch task.
3. **MCP server's tool catalog** flags OpenSanctions-derived tools as "commercial-license-required" so LLM clients understand the licensing context.

This is OPENGEM's second YELLOW source after ACLED. Same pattern: the data is good enough that we pay rather than build a substitute; the EULA shapes the surface where it can appear.

## The Sanctions-Risk tile (the OPENGEM build)

A single composite tile on the country page:

- **Headline number** — current count of sanctioned entities (Consolidated Sanctions, scope = country) with 30-day delta.
- **Sub-metric** — count of PEPs in the country (from PEPs collection).
- **Sparkline** — 365-day daily count of newly-added sanctioned entities (proxies sanctions intensity).
- **Top entities strip** — three most-recently-added sanctioned entities (name, sanctioning body, date, source link).
- **Drilldown** — opens a country-scoped table with filters (entity type, sanctioning body, status, date range).

A second "Sanctioned Securities Exposure" tile uses the Sanctioned Securities collection — count of ISINs / tickers under sanction, sortable by country of issuer. This is uniquely interesting for OPENGEM because it ties geopolitical risk directly to portfolio exposure, which is exactly the kind of structured composability the LP-tier customer wants.

A third "Maritime Sanctions" overlay on the L055 Shipping page renders sanctioned vessel IDs against PortWatch / AIS data — a supply-chain risk layer no incumbent dashboard surfaces openly.

## Ingestion pattern

Recommended pattern (self-host):

```
Weekly Dagster job:
  1. Download OpenSanctions bulk data (Default collection ~500 MB FtM-JSON; KYB ~10 GB)
  2. Restore into ElasticSearch index (yente expects ES; OpenSearch 2.x also works)
  3. Restart yente container against new index
  4. Diff against previous vintage, log changes
  5. Compute per-country aggregates → R2

Daily incremental pull:
  6. Fetch Consolidated Sanctions delta (~20-50 new entities/day typically)
  7. Index delta into ES; run aggregate refresh
  8. Update tile JSON
```

Infrastructure cost on Cloudflare Workers + R2 + a small managed ElasticSearch (Bonsai or self-hosted): ~$50/mo at v1 scale.

## Risks and mitigations

- **OpenSanctions changes pricing or licensing.** **Mitigation**: every weekly bulk pull is archived in R2 with vintage tag, so OPENGEM has a continually-fresh offline copy. We are not dependent on the hosted API.
- **CC-BY-NC interpretation is contested for "open-source projects with paid tier."** **Mitigation**: get a written license interpretation from OpenSanctions before launch; document the answer in L282 and the public methodology page. Better to know than to guess.
- **False positives in entity matching.** Yente's matcher is good but not perfect — common-name collisions are an unsolved problem in sanctions screening. **Mitigation**: OPENGEM never shows individual-entity matches without source URL + last-seen date + confidence score; we are not a compliance tool, we are a geopolitics dashboard. We surface counts and trends, not "Person X is sanctioned" assertions.
- **Source-list incompleteness.** OpenSanctions can only show what its 337 scrapers can scrape. Some sanctions regimes (e.g., Iranian internal lists, Chinese unilateral sanctions) are under-covered. **Mitigation**: methodology pop-up names the source-list coverage; we don't claim global completeness.

## Action items

1. Build `opengem-data-opensanctions` package — yente self-host adapter, weekly bulk pull, daily incremental.
2. Stand up self-hosted yente on Cloudflare or small VM with managed ElasticSearch.
3. Pre-launch: request written CC-BY-NC interpretation from OpenSanctions for OPENGEM's open-source-with-paid-tier model. If commercial license required, budget for it.
4. Build Sanctions-Risk tile on country page (L161 / L163 / L225).
5. Build Sanctioned Securities tile (uniquely valuable for LP tier).
6. Build Maritime Sanctions overlay on L055 Shipping page.
7. Wire MCP server tool catalog to flag OpenSanctions tools as commercial-license-restricted in the tool description (transparent to LLM clients).
8. Update L282 License Audit — OpenSanctions YELLOW with explicit note about commercial-tier gate.

## Comparison to siblings

| Source | License | Best for |
|---|---|---|
| OFAC SDN List (raw, US Treasury) | GREEN (public domain US gov) | Single-jurisdiction sanctions; raw |
| EU Consolidated Sanctions (raw) | GREEN | Single-jurisdiction sanctions; raw |
| **OpenSanctions** (this) | **YELLOW (CC-BY-NC + commercial license)** | **Consolidated, deduplicated, FtM-modeled cross-jurisdiction** |
| Refinitiv World-Check | RED (commercial only) | Compliance gold standard, expensive |
| Dow Jones Risk & Compliance | RED | Compliance gold standard |
| ICIJ Offshore Leaks | GREEN (CC-BY-NC for some, public for others) | Beneficial ownership leaks |

OpenSanctions sits in the middle of the curve: cleaner than raw OFAC scrapes, dramatically cheaper than Refinitiv/Dow Jones, but YELLOW for OPENGEM's paid tier. The free OFAC + EU raw data is a fallback if OpenSanctions licensing becomes untenable — much worse UX but GREEN.

## Related

- [[L001-vision-statement]] — the CC-BY-NC sits awkwardly against CC-BY-4.0 substrate promise; we annotate this in the License Audit
- [[L022-acled]] — sibling YELLOW source with EULA restriction
- [[L055-shipping-portwatch]] — Maritime Sanctions overlay target
- [[L161-country-card-grid]] — Sanctions-Risk tile target
- [[L216-sovereign-risk-page]] — sanctions exposure feature
- [[L225-geopolitical-alliances-sanctions]] — primary visualizer
- [[L282-license-audit]] — OpenSanctions YELLOW row with commercial-license-required note

## Sources

- [OpenSanctions homepage](https://www.opensanctions.org/)
- [opensanctions/opensanctions on GitHub (MIT)](https://github.com/opensanctions/opensanctions)
- [opensanctions/yente entity matching API on GitHub (MIT)](https://github.com/opensanctions/yente)
- [OpenSanctions licensing page](https://www.opensanctions.org/licensing/)
- [Commercial use FAQ](https://www.opensanctions.org/docs/commercial/faq/)
- [Paying for use FAQ](https://www.opensanctions.org/faq/156/paying-for-use/)
- [Pricing tier guide](https://www.opensanctions.org/faq/29/pricing-tier/)
- [API documentation](https://www.opensanctions.org/docs/api/)
- [API usage limits and optimization](https://www.opensanctions.org/faq/154/api-usage-limits-optimization/)
- [Bulk distributions page](https://www.opensanctions.org/datasets/)
- [Open source components page](https://www.opensanctions.org/docs/opensource/)
- [Aleph data commons — sanctions](https://github.com/alephdata/docs/blob/master/data-commons/sanctions.md)
