# R05 — Source Access Terms (Private Use)

| Field | Value |
|---|---|
| Document ID | OG1-RES-005 |
| Revision | B (populated 2026-05-24) |
| Date | 2026-05-24 |
| Status | **Investigated — verdict: H-5 HOLDS for most sources; ONE MAJOR CONSTRAINT discovered: FRED 2024 ToS prohibits archiving and ML training.** |
| Tests hypothesis | H-5 |

---

## 1. Hypothesis under test (H-5)

> All planned data sources permit automated programmatic access at the rates OPENGEM needs, in their current 2026 ToS.

## 2. Per-source findings

### 2.1 Core macro time series

| Source | API | Auth | Rate limit | Automated-access ToS | Caveats |
|---|---|---|---|---|---|
| **FRED** | REST | Free API key | **120 req/min**; 2 req/sec cap | **🚨 RED FLAG.** 2024 ToS update prohibits: *"storing, caching, or archiving any portion of FRED Services or FRED Content"*; *"wholesale downloading"*; *"use in connection with development or training of any software program or system or machine learning, including AI."* | Critical for OPENGEM. See §3. |
| **ALFRED** (Archival FRED) | REST | Same FRED key | Same | Same ToS as FRED (St. Louis Fed). Vintage retrieval is *allowed*; archiving the retrieved data is *not*. | The vintage *queries* are fine; persisting them locally for OPENGEM's leaderboard is the problem. |
| **ECB SDW** | SDMX 2.1 RESTful | None | Unspecified — practical limits via IP-throttling | Permissive; service designed for programmatic access. | Multiple formats (XML/JSON/CSV). |
| **IMF SDMX Central** | SDMX 2.1 / 3.0 RESTful | None / optional | "Throttle accordingly"; ~example: pause after every 10 reqs | Designed for automated access. | Coverage: IFS, WEO, BoP, GFS, etc. |
| **OECD Data API** | SDMX | None / optional | Rate-limited (unspecified numbers); free; ToS acceptance required | Designed for programmatic access. | Includes ORDRA (R02). |
| **BIS Data Portal API** | SDMX | None | Unspecified; "BIS reserves the right to limit or suspend any User's IP" | As-is, monitored; usage can be revoked. | Policy rates, BoP, banking stats. |
| **World Bank WDI / Data360** | REST | None | Generally permissive (no explicit limits surfaced in this round) | Open data; designed for programmatic access. | Annual frequency for most WDI series. |
| **UN Comtrade Plus** | REST | Free user token | **500 calls/day**, 100k records/call (free tier) | Free for "data visualization/analytics" if records-per-call ≤100k; "data extraction" requires premium. | Comtrade lag 1–2y per RSK-009. |

Sources: [FRED API ToS](https://fred.stlouisfed.org/docs/api/terms_of_use.html); [FRED ToS update notice 2024](https://news.research.stlouisfed.org/2024/06/weve-updated-our-terms-of-use-action-requested/); [ECB Data Portal API help](https://data.ecb.europa.eu/help/api/overview); [IMF SDMX guide](https://dsbb.imf.org/content/pdfs/IMFSDMXCentralWebServicesGuide.pdf); [OECD API explainer](https://www.oecd.org/en/data/insights/data-explainers/2024/09/api.html); [BIS Data Portal Legal](https://data.bis.org/help/legal); [Comtrade license agreement](https://comtrade.un.org/licenseagreement.html).

### 2.2 Wider information surface (R06)

| Source | API | Auth | Rate limit | Automated-access ToS |
|---|---|---|---|---|
| **NY Fed GSCPI** | CSV download | None | Trivial — monthly file | Free, no restrictions noted. |
| **IMF PortWatch** | Web + downloadable series | None | n/a | Free; backed by IMF. |
| **Caldara-Iacoviello GPR** | CSV downloads at matteoiacoviello.com | None | Trivial — monthly | Replication code on openICPSR. Free. |
| **GDELT 2.0** | Multiple APIs + bulk on AWS Open Data | None | Free; bulk supported | **"Unlimited and unrestricted use for any academic, commercial, or governmental use of any kind without fee."** Wide open. |
| **GDELT (BigQuery)** | Google BigQuery | Google account | Pay-per-query (BigQuery pricing) | Allowed; cost-managed. |
| **ACLED** | API + bulk | Free for academic / non-commercial | Daily limits | Commercial use requires license; private-non-commercial use likely OK but verify. |
| **OFAC / EU / UN sanctions** | XML/CSV downloads | None | Trivial | Official government data, free. |
| **Bauer-Mertens / SF Fed term-spread tools** | n/a — replication code | None | n/a | Public code. |

Sources: [NY Fed GSCPI page](https://www.newyorkfed.org/research/policy/gscpi); [GPR Iacoviello page](https://www.matteoiacoviello.com/gpr.htm); [GDELT data page](https://www.gdeltproject.org/data.html); [GDELT on AWS Open Data](https://registry.opendata.aws/gdelt/).

### 2.3 Alt-data (originally planned, now mostly optional under R03 rescope)

| Source | Status |
|---|---|
| **VIIRS Night Lights** | NASA EarthData login required (free). Bulk downloads via LAADS DAAC or NOAA. Tractable but heavy. Defer to Block II. |
| **AIS Shipping** | Use **PortWatch** (free, derivative) at IOC. Raw AIS via UN Global Platform (free aggregates) or commercial (Spire/MarineTraffic, paid) only if PortWatch insufficient. |
| **Google Trends** | No official bulk API; `pytrends` reverse-engineering is fragile and against ToS spirit. Skip at IOC. |
| **Electricity load** | ENTSO-E Transparency Platform (EU, free API with registration), EIA (US, free), AEMO (AU, free). Per-region patchwork. |

## 3. The FRED ToS problem — what it means for OPENGEM

The FRED 2024 ToS update is the **single most consequential finding** in R05.

### 3.1 The literal text

Per [St. Louis Fed's June 2024 notice](https://news.research.stlouisfed.org/2024/06/weve-updated-our-terms-of-use-action-requested/) and the current [FRED API Terms](https://fred.stlouisfed.org/docs/api/terms_of_use.html):

> Prohibited: *storing, caching, or archiving any portion of FRED Services or FRED Content*; *providing any stored, cached, or archived portion to any third party*; *incorporating any FRED Content in any database, compilation, archive, cache, or other medium*; *wholesale downloading or accessing of FRED Services or FRED Content*; *use of FRED Services or FRED Content in connection with the development or training of any software program or system or machine learning, including AI*.

### 3.2 What OPENGEM was planning that now conflicts

- **Vintage self-archive** (R02 §5): OPENGEM was to mirror release data and preserve every vintage. Hitting FRED for the *source* and storing the result locally is the literal prohibited activity.
- **ML training**: OPENGEM's L3 ML residual (and any of the R06 ML-based nowcasts) "trains" on data. If FRED is in the training set, ToS is violated.
- **Leaderboard storage**: every published forecast carries a `vintage_hash` of input data (FR-FOR-002). If the inputs include FRED-derived series and they're stored, ToS is violated.

### 3.3 Mitigations (ranked)

1. **Source-of-truth substitution.** For every series OPENGEM wants from FRED, identify the *underlying* upstream source (BEA for NIPA; BLS for CPI; FRB Board for monetary; etc.) and ingest from there directly. FRED is a *mirror* — its underlying data is mostly upstream-public. Use FRED only for *discovery*, not as the persistent data path. **This is the cleanest fix.** Effort: per-series substitution research (maybe 1–2 weeks).
2. **ALFRED-only, for vintages, treated as queries not archive.** Use ALFRED via real-time API calls when a vintage is needed; do not store responses. Bad fit for OPENGEM because we need archived inputs for reproducibility.
3. **Request a separate license / exception** from St. Louis Fed for research-archival use. Possible for academic projects; private-individual project's mileage may vary.
4. **Stop using FRED.** Substitute all FRED dependencies with non-FRED sources. Same as (1) but uniform.

**Recommendation: Mitigation 1 (substitution).** FRED's value is *aggregation convenience*, not unique data. The underlying agencies publish the same series, often via SDMX or REST. OPENGEM should not be ToS-fragile on a non-essential dependency.

### 3.4 Implication for ALFRED

ALFRED is also St. Louis Fed and falls under the same ToS regime. **OPENGEM cannot rely on ALFRED for archived vintages** — only for live queries. The Philadelphia Fed RTDSM (a different institution) and the OECD ORDRA (separate ToS) become the primary vintage paths.

Need to verify Philly Fed RTDSM and OECD ORDRA ToS specifically; both are research-friendly, but explicit confirmation is open work.

## 4. Verdict on H-5

**Holds for ≥10 of the 12 named sources, with one major modification.**

- ✅ ECB SDW, IMF SDMX, OECD Data API, BIS, World Bank, GSCPI, PortWatch, GPR, GDELT, sanctions lists, ENTSO-E/EIA/AEMO, Bauer-Mertens code — all permissive, programmatic, free.
- ⚠️ Comtrade — 500 calls/day cap; manageable but plan around it.
- 🚨 **FRED / ALFRED — incompatible with OPENGEM's archive-and-train design as written.** Substitute with upstream agencies.
- ⏸ VIIRS, AIS direct, Google Trends — deferred / optional / use surrogates.

## 5. Decision implications for the CONOPS

| Source | Current | Proposed change |
|---|---|---|
| **CONOPS §5.3 / Master-doc §5.3.1** | Lists FRED as a core source | Replace "FRED" with "upstream US agency direct: BEA (NIPA), BLS (CPI/unemployment), FRB Board (rates/money), Treasury (rates), Census M3." Use FRED *for discovery only, not persistence.* |
| **CONOPS §5.3 / Master-doc §5.3.1** | Lists ALFRED for vintages | Replace "ALFRED" with "Philadelphia Fed RTDSM" for US vintages. Note that ALFRED queries remain useful but cannot be cached. |
| **FR-DAT-001** | "≥7 named sources including FRED" | Update list to: IMF IFS, WB WDI, OECD MEI/ORDRA, BEA, BLS, FRB Board, ECB SDW, BIS Data Portal, UN Comtrade. (FRED removed from authoritative list; cited as discovery aid only.) |
| **POL-01** "all data sources … licensed for free redistribution" | — | Add: "**OPENGEM does not redistribute FRED Content. FRED Services are used only for series discovery, not persistence.** Upstream agencies are the persistent source of truth." |
| **CONOPS §8.2 D-05** | "Open dataset constraint forecloses some alt-data sources" | Add: "FRED's 2024 ToS forecloses FRED itself as a persistent source. Upstream-substitution is the standard pattern." |
| **RSK-010** "Schema drift in IMF/WB APIs" (L=3 I=3) | — | Add RSK-011: "FRED/ALFRED ToS may further restrict access" (L=2 I=2 since substitution mitigates). |
| **ICD-001 (external data interfaces)** | Per-source row including FRED | Replace FRED row with rows for each upstream agency. |

## 6. Source-of-truth substitution map (US series only)

The substitution targets for series OPENGEM would have pulled from FRED:

| FRED series | Upstream source | Endpoint |
|---|---|---|
| GDP, GDI, NIPA aggregates | BEA | bea.gov/api |
| CPI, PCE, employment | BLS | bls.gov/developers |
| Federal funds, monetary aggregates, Treasury yields | FRB Board (H.15, Z.1) | federalreserve.gov/datadownload |
| Treasury yields (alternate) | Treasury Direct | home.treasury.gov |
| Industrial production, capacity utilization | FRB Board (G.17) | federalreserve.gov/datadownload |
| Census trade (M3) | Census Bureau | census.gov/data/api |

Effort: per-series adapter mapping, ~1–2 weeks. All endpoints are public.

## 7. Open probes

1. **Philly Fed RTDSM ToS** — explicit verification that programmatic archival use is permitted. Likely yes (it's a research dataset by design), but confirm.
2. **OECD ORDRA ToS** — same.
3. **ACLED license for private-non-commercial use** — confirm scope.
4. **ECB SDW redistribution clause** — confirm OPENGEM's caching of derived series is permitted.
5. **Consensus Economics access** — deferred to public-launch round per program owner direction; flagged as a future decision.

## 8. Bottom line

H-5 holds for the data backbone with **one mandatory substitution** (FRED → upstream agencies). All wider-information-surface sources (GSCPI, GPR, GDELT, etc.) are permissive and free. Comtrade's 500/day limit is manageable. The OPENGEM ingestion architecture as designed is feasible, but the source list needs the FRED-substitution rewrite documented in §6.

---

*End of R05 Rev B.*
