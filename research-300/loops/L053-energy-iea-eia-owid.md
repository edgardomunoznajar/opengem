# L053 — Energy: IEA paywalled, EIA open & deep, OWID free CC-BY layer cake

**Loop**: 053 / 300
**Phase**: 1 — Open-source landscape survey (data sources)
**Date**: 2026-06-06
**Verdict**: **ADOPT-NOW EIA + OWID-energy**, **ADOPT-BLOCK-II WEO Free Dataset (CC-BY-NC-SA limits us)**, **SKIP IEA Statistics Package** (paid, license incompatible with our redistributable stance).

---

## One-line take

The IEA's core data is paywalled and licensed CC-BY-NC-SA — incompatible with OPENGEM's CC-BY-4.0 redistribution stance. EIA is U.S.-centric but has a **clean, free, deep international energy module** that often gets overlooked. OWID-energy is a curated, GitHub-distributed, CC-BY 4-decade global energy panel that synthesizes EIA + BP Statistical Review + IRENA + Ember into one CSV — the right baseline for OPENGEM's global energy page.

## Why this combination

OPENGEM's friend-the-YouTuber needs to talk about:
- US-centric oil & gas (weekly EIA STEO, weekly petroleum balances, monthly STEO forecasts).
- Global electricity generation mix by country (renewables vs fossil; key for energy-transition narrative).
- Global oil supply/demand balance (OPEC vs non-OPEC; key for inflation pass-through).

EIA covers (1) and (3) well from the US perspective with open APIs. OWID-energy synthesizes the cross-country layer for (2). The IEA has the most authoritative cross-country panel but is paywalled and license-incompatible.

## EIA (U.S. Energy Information Administration)

- **Base URL**: `https://api.eia.gov/v2/`
- **API style**: REST. JSON default, XML optional. Hierarchical category tree (petroleum, electricity, natural gas, coal, **international energy statistics**, total energy, nuclear, biofuels, renewable, CO2 emissions).
- **Auth**: requires free API key (`?api_key=XXX` query param). Registration at `eia.gov/opendata/register.php`. No payment, no quotas attached to registration.
- **Rate limits**: documented as "throttle per second and per hour"; sustained 5 RPS sees occasional throttles; bursts to 10 RPS sometimes flagged. Hard caps: **5,000 rows per JSON response**, **300 rows per XML response**. Pagination via `offset` + `length`.
- **Coverage**:
  - **Petroleum**: weekly prices, weekly supply/demand balance, monthly STEO (Short-Term Energy Outlook), refinery rates. **Best-in-class open oil data.**
  - **Electricity**: monthly + hourly US generation, sales, retail prices. State-level breakdown.
  - **Natural gas**: weekly storage (the Thursday EIA Storage report — market-moving), monthly production, prices.
  - **Coal**: monthly production, distribution.
  - **International energy statistics**: **annual country-level total primary energy, oil, gas, coal, renewables, electricity** for ~200 countries 1980-current. T+12mo cadence.
- **License**: U.S. federal government data — **public domain (effectively CC0)**. **GREEN — no restrictions, no attribution required (but courtesy-requested).**
- **Vintage**: EIA STEO publishes monthly forecasts back to 1997; archive available. EIA Weekly Petroleum Status Report archived weekly back to 1990. **The cleanest open energy vintage archive in existence.**

## OWID-energy (Our World in Data — energy synthesis)

- **Base URL / file**: `https://owid-public.owid.io/data/energy/owid-energy-data.csv` (CSV); GitHub mirror at `github.com/owid/energy-data`; XLSX and JSON variants.
- **API style**: static file. No API. Update via GitHub commit history.
- **Auth**: none.
- **Rate limits**: none (it's a CSV download).
- **Coverage**: 200+ countries, 1900-current, ~120 columns per row (primary energy by source, electricity mix by source, per-capita, growth rates, share-of-mix, CO2 from energy).
- **Source synthesis**: combines **EIA international, BP Statistical Review (Energy Institute since 2023), IRENA renewables, Ember electricity, Smil long-historical**. OWID's value-add: harmonizing country definitions, applying consistent units, filling gaps.
- **Update cadence**: continuous (weekly commits to GitHub); annual major refresh in June with the new Energy Institute Statistical Review release.
- **License**: **CC-BY 4.0**. GREEN, fully redistributable.

## WEO 2025 Free Dataset (IEA)

- **Coverage**: world-aggregated CPS/STEPS/NZE scenarios + selected key regions/countries for 2035, 2040, 2050 + historical 2010 / 2023 / 2024.
- **Granularity**: shallow. Region-level, not country-level. Selected indicators only.
- **License**: **CC-BY-NC-SA 4.0** — NonCommercial-ShareAlike. **Incompatible with OPENGEM's CC-BY-4.0 redistribution stance.** NC clause blocks our paid API tier from including this data even derivatively.
- **Verdict**: CITE-ONLY. We can talk about IEA scenarios on the dashboard, link to the IEA pages, even reproduce a chart for editorial purposes — but cannot ingest into our open data layer.

## IEA Statistics Package / World Energy Statistics

- **Coverage**: 156 countries × 35 regional aggregates, 1971-current, every energy carrier in original units.
- **License**: full subscription required. Pricing not publicly listed; institutional licenses run $10k+/year per organization based on past public references.
- **Verdict**: **SKIP** for Block I. Revisit only if a sovereign-fund LP customer demands IEA-quality cross-country detail and is willing to pay through the API tier.

## Rate-limit math for OPENGEM

**EIA**:
- US petroleum weekly: ~10 series × 1 weekly call = 10 calls/week.
- EIA STEO monthly: 1 file download / 1 API call per refresh.
- International energy annual: ~20 series × 200 countries; with batching, ~20 calls/year.
- Total monthly steady-state: ~50 calls. Trivial.
- Backfill: full international historical scrape ~500 calls.

**OWID-energy**:
- 1 CSV download per refresh. ~15 MB. Daily refresh = 1 download/day = trivial.

**Both adapters fit inside any reasonable rate budget.**

## Vintage truth

- **EIA**: STEO archive at `eia.gov/outlooks/steo/archives/` — every monthly release preserved, all forecast vintages 1997-current downloadable. This is **as clean as ALFRED for energy**. Critical for forecast backtesting.
- **OWID-energy**: GitHub commit history is the vintage archive. `git checkout` any commit for the energy data as-of that date. Clean and free.
- **EIA weekly petroleum** vintage from weekly release archive: same archive pattern, weekly granularity.

The EIA vintage archive is one of the under-known gems of open energy data.

## Fit-for-OPENGEM verdict

- **ADOPT-NOW**: EIA API v2 (petroleum, electricity, international energy, STEO archive) + OWID-energy CSV.
- **ADOPT-BLOCK-II**: EIA AEO (Annual Energy Outlook) archive ingest.
- **CITE-ONLY**: IEA WEO Free Dataset (NC license blocks ingestion; we link to it).
- **SKIP**: IEA Statistics Package (paid, license incompatible).

**Adapter design notes**:

- New package `opengem-data-energy`.
- Submodule 1: `EIAAdapter` — wraps the API key, handles 5,000-row pagination, exposes `fetch_petroleum_weekly()`, `fetch_steo_monthly()`, `fetch_steo_archive(release)`, `fetch_international_annual()`.
- Submodule 2: `OWIDEnergyAdapter` — downloads the CSV, caches with content-hash, exposes typed columns.
- API key from `OPENGEM_EIA_API_KEY` env var. Adapter degrades to OWID-only if key missing.
- Provenance: every Observation records `source=eia` or `source=owid_energy`, `release_id=...`, `dataset_path=...`, `license=public_domain` or `cc_by_4.0`.

## Trap log

- **IEA WEO Free Dataset CC-BY-NC-SA license is a trap**. It looks free at the data-portal level; the NC clause makes it unsafe to ingest into a derivative dataset that any paid tier of OPENGEM would touch. NC also makes the ShareAlike viral.
- **EIA "International Energy Statistics" 12-month lag is real** — country-level rollups for year T appear ~late T+12. For nowcasting, you need OWID (which back-fills via Ember monthly electricity mix) or the IEA paywalled monthly oil data.
- **OWID-energy units are harmonized to TWh and exajoules**; the EIA international panel uses quadrillion BTU and short tons. Pre-aggregate any cross-source view to a common unit at adapter level.
- **EIA Storage Report Thursday 10:30 ET release** is one of the most market-moving free data points in the world for natural gas; our weekly refresh should land within an hour of release for the energy page to be useful.
- **OWID's BP-source columns were rebranded "Energy Institute"** after BP sold the data product in 2023. Historical references to "BP Statistical Review of World Energy" now point to "Statistical Review of World Energy" from the Energy Institute. Adapter should accept both column name patterns.
- **EIA STEO sometimes back-revises** old years when methodology changes; archive ingest must keep every vintage to preserve the original "what we thought in March 2020" answer.

## Related

- [[L054]] — Climate/weather (energy demand correlates heavily with degree days)
- [[L056]] — Commodity prices (energy is the lead commodity)
- [[L046]] — World Bank Indicators (`EG.USE.*` codes complement but don't replace)
- [[R06]] (existing) — wider information surface
