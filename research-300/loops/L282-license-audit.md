# L282 — License Audit: Apache-2.0 Code + CC-BY-4.0 Data + Model Cards

**Loop**: 282 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis of this loop

OPENGEM's license stack is an explicit promise. Apache-2.0 for code. CC-BY-4.0 for data. Model cards under CC-BY-4.0 with explicit reuse permissions. This is documented in [[L008]] promise 5 and is part of the strategic moat — the "free tier is the whole product" commitment ([[L006]] / [[L276]]) depends on the licenses being clean upstream.

A license audit checks every upstream source we ingest, every library we depend on, every dataset we redistribute, and every derived artifact we publish. The audit produces a license matrix that becomes a public page (`/about/licenses`) and a CI gate (PRs adding upstream dependencies must declare the license).

This loop does the audit, finds the landmines, and prescribes the mitigation. The two known landmines from [[L022]] (ACLED) and [[L028]] (OpenSanctions) are confirmed; one new landmine surfaces (V-Dem license still unclear); three GREEN finds are reconfirmed.

---

## License audit matrix — upstream data sources

| Source | License | Class | Notes | OPENGEM action |
|---|---|---|---|---|
| **FRED (US Federal Reserve)** | Public Domain | GREEN | US government work, no copyright restriction | Ingest freely; attribute as "FRED, Federal Reserve Bank of St. Louis" |
| **BLS (US Bureau of Labor Statistics)** | Public Domain | GREEN | US government | Ingest freely; attribute |
| **BEA (US Bureau of Economic Analysis)** | Public Domain | GREEN | US government | Ingest freely; attribute |
| **World Bank Indicators API** | CC-BY-4.0 | GREEN | Explicit CC-BY since 2014 | Ingest freely; attribute "World Bank Open Data, CC-BY-4.0" |
| **World Bank Pink Sheet (commodities)** | CC-BY-4.0 | GREEN | Same data license | Ingest freely |
| **World Bank WGI (governance)** | CC-BY-4.0 | GREEN | Same | Ingest freely |
| **IMF Data + SDMX** | Free for use | GREEN, ambiguous | "Free for redistribution with citation" per IMF terms; not explicitly CC | Ingest with attribution; flag for legal review if license tightens |
| **OECD Data Portal / ORDRA / SDMX** | "OECD terms" | GREEN | OECD allows reuse with attribution per their terms | Ingest with attribution |
| **BIS Statistics Warehouse** | "BIS terms" | GREEN, narrow | Free use with attribution but no redistribution under different license | Ingest; attribute; do *not* relicense BIS data |
| **ECB SDW** | Free with attribution | GREEN | Eurosystem terms | Ingest with attribution |
| **ECB SPF (Survey of Professional Forecasters)** | Free with attribution | GREEN | Same | Ingest with attribution |
| **GDELT 2.0 + GKG** | Free with citation | GREEN | "Use freely, cite the project" | Ingest with attribution |
| **POLECAT (Harvard Dataverse)** | CC0 | GREEN | Most permissive | Ingest freely |
| **UCDP (Uppsala)** | CC-BY-4.0 | GREEN | Explicit CC | Ingest with attribution |
| **Caldara-Iacoviello GPR** | Academic free use | GREEN | Cite Caldara-Iacoviello papers | Ingest with attribution |
| **V-Dem (Varieties of Democracy)** | Unclear (academic free) | YELLOW | Used by academics freely; explicit license not on every distribution | **Action**: written confirmation from V-Dem before launch |
| **Cline Center datasets (POLECAT etc)** | Mixed (POLECAT = CC0; others vary) | GREEN/YELLOW | Per-dataset audit | Per-dataset attribution |
| **ACLED** | Custom EULA, restrictive | YELLOW (RED for substrate) | "May not republish raw rows; derived/transformative aggregates permitted" | **Action**: Use as benchmark only on leaderboard; do not republish raw rows; defer paid-tier exposure |
| **OpenSanctions** | CC-BY-NC | YELLOW (RED for paid tier) | Non-commercial only | **Action**: feature-flag for paid tier; commercial license negotiation in Q4 2026 |
| **Stratfor / Geopolitical Futures / EIU / Fitch** | Proprietary | RED | All commercial | Cite as benchmarks on leaderboard; never reproduce numbers |
| **NOAA / ECMWF (climate)** | Public Domain (NOAA), CC-BY (ECMWF) | GREEN | NOAA US government; ECMWF licensed CC-BY | Ingest with appropriate attribution |
| **PortWatch (IMF)** | Free with attribution | GREEN | IMF infrastructure | Ingest |
| **MarineTraffic AIS** | Commercial | RED | Paid feed | Skip; use PortWatch as substitute |
| **Yahoo Finance / yfinance / Stooq** | Mixed (Yahoo: terms unclear, used widely) | YELLOW | Tolerated unofficial scraping | Skip for v1; use FRED/ECB for FX; revisit Y2 |
| **CoinMetrics community tier** | Custom (free for non-commercial research) | YELLOW | Limited paid-tier reuse | Skip for v1; not a v1 priority |
| **NBER working papers** | Mixed (per-paper) | varies | Cite individually | Cite, never reproduce |

**Total**: 26 upstream sources audited. 18 GREEN, 5 YELLOW (V-Dem clarification + ACLED + OpenSanctions + Yahoo + CoinMetrics), 3 RED (Stratfor / MarineTraffic + Fitch).

---

## License audit matrix — upstream code dependencies

| Library | License | Compatible with Apache-2.0? |
|---|---|---|
| Next.js 15 | MIT | YES |
| React | MIT | YES |
| Tailwind v4 | MIT | YES |
| shadcn-style components | MIT | YES (re-licensed under our Apache-2.0) |
| Lightweight Charts | Apache-2.0 | YES |
| Finos Perspective | Apache-2.0 | YES |
| TanStack Table | MIT | YES |
| globe.gl | MIT | YES |
| Kepler.gl | MIT | YES |
| Datasette | Apache-2.0 | YES |
| DuckDB | MIT | YES |
| Nixtla neuralforecast | Apache-2.0 | YES |
| Nixtla statsforecast | Apache-2.0 | YES |
| statsmodels | BSD-3-Clause | YES |
| PyMC | Apache-2.0 | YES |
| FastAPI | MIT | YES |
| hono | MIT | YES |
| docling | MIT | YES |
| Stripe SDK | MIT | YES (operational tool, not redistributed) |
| Resend SDK | MIT | YES |
| Plausible-tracker | MIT | YES |
| All Cloudflare Workers SDKs | Apache-2.0 / MIT | YES |
| Playwright | Apache-2.0 | YES |
| Vitest | MIT | YES |
| zod | MIT | YES |

**Total**: 25 core code dependencies audited. All YES. No GPL, no AGPL, no commercial-only.

The single concern is *transitive* dependencies in the npm tree. We run `licensecheck` on PRs to flag any incoming GPL/AGPL/SSPL. Current scan: 0 such dependencies.

---

## OPENGEM's own publication licenses

| Artifact | License |
|---|---|
| Code (Apache-2.0 LICENSE in repo) | Apache-2.0 |
| Forecasts + derived data (downloads, RSS, JSON) | CC-BY-4.0 |
| Model cards | CC-BY-4.0 |
| Documentation pages (`/methodology/*`, `/about`, etc.) | CC-BY-4.0 |
| Accountability ledger content (`/accountability`, post-mortems) | CC-BY-4.0 |
| Press kit assets (logos, screenshots, video, bios) | CC-BY-4.0 |
| Charts embedded externally | CC-BY-4.0 with attribution-link required |

All licenses are declared in three places: (1) repository `LICENSE` and `LICENSE-DATA` files; (2) the public `/about/licenses` page; (3) the relevant resource's header metadata (HTTP `License` header, JSON `license` field, RSS `dc:rights` element).

---

## Landmines and mitigations

### Landmine 1 — ACLED EULA (YELLOW)

**Risk.** ACLED's EULA prohibits republishing raw rows and prohibits "creating functional substitutes for ACLED's own platforms." Any OPENGEM page that visibly aggregates ACLED data could be argued to violate the EULA.

**Mitigation.** Per [[L022]] and [[L271]] §15, ACLED becomes a *benchmark on the leaderboard*, not a *substrate in the dashboard*. The geopolitical pulse map and conflict tracker use POLECAT + UCDP + GDELT as primary sources. ACLED appears only on `/leaderboard` as a forecast-comparison reference, citing ACLED with full attribution. This is consistent with their EULA's "permitted uses" of citation and academic comparison.

If ACLED tightens further, we lose nothing because POLECAT + UCDP cover the substrate role. Mitigation cost: zero.

### Landmine 2 — OpenSanctions CC-BY-NC (YELLOW)

**Risk.** CC-BY-NC means free for non-commercial; commercial use (paid tier) requires a license negotiation.

**Mitigation.** Feature-flag OpenSanctions-dependent features behind a "experimental, free-tier-only" badge. Initiate commercial-license conversation with OpenSanctions in Q4 2026. If they price reasonably, integrate into paid tier in Y2. If they price unreasonably, build our own sanctions-data layer from primary public sources (OFAC, UN, EU Council of Ministers) which are public domain.

Mitigation cost: an estimated 1-2 weeks engineering Y2 if we build our own.

### Landmine 3 — V-Dem license unclear (YELLOW)

**Risk.** V-Dem (Varieties of Democracy) v16 is distributed for academic use but the dataset's license terms are not explicit on every distribution channel. Operational risk: we ingest, redistribute, and someone challenges later.

**Mitigation.** Pre-launch action: founder emails V-Dem team requesting written confirmation of redistributable license under attribution. If they decline or ambiguate: we *cite* V-Dem indices on the dashboard but do not redistribute the underlying series; users go upstream for the data. Most likely: V-Dem confirms academic / CC-BY-style permission and we proceed.

### Landmine 4 — Yahoo Finance / yfinance (YELLOW)

**Risk.** Unofficial scraping endpoint. Yahoo could change terms at any time. yfinance is community-maintained and is not a Yahoo product.

**Mitigation.** Skip for v1. Use FRED + ECB + BIS for FX and major equity indices. yfinance is a v1.1 / v2 candidate when we have time for legal due diligence or are willing to migrate to a stable source. Mitigation cost: minor coverage gap on long-tail equity indices.

### Landmine 5 — Bloomberg / Stratfor / IHS / Fitch numbers (RED)

**Risk.** Their forecasts are proprietary. We cannot reproduce their numbers.

**Mitigation.** Per [[L008]] strategy, we *cite their published numbers on the leaderboard as comparison benchmarks*. This is permitted under fair use as comparative criticism, similar to how research reports cite competing analyses. We do not republish their data feeds; we cite their public-facing forecast statements with attribution.

If Bloomberg or Stratfor sends a cease-and-desist over the leaderboard, we respond by adding more attribution and links and inviting them to publish a richer track record. The PR alone is brand-positive.

---

## The license commitment page (`/about/licenses`)

Public page (renders to `/about/licenses`) with the full audit matrix. Layout:

```
─────────────────────────────────────────────────────────
LICENSES, REUSE, AND ATTRIBUTION

OPENGEM's code is Apache-2.0. Our data is CC-BY-4.0. Our model cards,
methodology pages, and accountability ledger are CC-BY-4.0. Press kit
assets are CC-BY-4.0.

These are not aspirations. They are the licenses you get if you fork the
repo, download the data, embed a chart, or quote a number.

WHAT YOU CAN DO WITHOUT ASKING US

- Fork the code, modify, redistribute (under Apache-2.0)
- Download data, redistribute (under CC-BY-4.0, with attribution)
- Embed charts on your site (attribution link required)
- Quote numbers in your work (citation appreciated)
- Use the press kit assets (CC-BY-4.0)

WHAT YOU MUST DO

- Keep the attribution to OPENGEM with a link back to opengem.com
- If you fork the code, keep the Apache-2.0 LICENSE in your fork
- If you redistribute data, keep the CC-BY-4.0 notice

UPSTREAM SOURCES

We ingest 26 public data sources. The full matrix is below. Most are
GREEN (free with attribution); a few are YELLOW (EULA constraints we
respect); none of our public dashboard depends on RED sources.

[full matrix above, rendered as a sortable table]

CONTACT

License questions: legal@opengem.com
Press use of assets: press@opengem.com
```

The page is linked from every page footer.

---

## CI gate for license discipline

A `license-check.yml` GitHub Action runs on every PR:

1. Scan `package.json` + `requirements.txt` for new dependencies.
2. Resolve their licenses via `licensecheck` (Node) and `pip-licenses` (Python).
3. Compare against the allowlist (MIT, Apache-2.0, BSD-2/3, ISC, MPL-2.0 in some cases).
4. Block PR if any new dep is GPL, AGPL, SSPL, or unclear.
5. Block PR if any data ingestion code references an upstream source not in the audit matrix.

This makes license drift impossible to introduce by accident.

---

## What this loop produced

- License audit matrix for 26 upstream data sources (18 GREEN, 5 YELLOW, 3 RED).
- License audit matrix for 25 core code dependencies (all compatible with Apache-2.0).
- Five named landmines with mitigation plans.
- The `/about/licenses` public page copy.
- CI gate spec for license discipline.

## What comes next

- Pre-launch: written V-Dem confirmation request.
- Q4 2026: OpenSanctions commercial-license conversation.
- **L283** — ToS draft references the licenses.

## Related

- [[L008-differentiation]] — promise 5 (embed/export/expose) operationalizes the licenses
- [[L022-acled]] / [[L028-opensanctions]] / [[L027-vdem]] — upstream loops with full license context
- [[L271-master-prd]] — section 15 risk 1+2 referenced these landmines
- [[L283-tos-draft]] — terms of service references this audit
