# L054 — Climate/weather as macro signal: NOAA CDO, ERA5, GHCN

**Loop**: 054 / 300
**Phase**: 1 — Open-source landscape survey (data sources)
**Date**: 2026-06-06
**Verdict**: **ADOPT-NOW NOAA CDO + GHCN daily** (free, GREEN, lightweight) for energy-demand and crop-yield overlays. **ADOPT-BLOCK-II ERA5 via CDS API** for reanalysis-grade gridded data when the dashboard needs heat-stress maps. **SKIP** the paid ECMWF MARS direct access — CDS subset is sufficient.

---

## One-line take

OPENGEM should treat climate as a **macro covariate stream** — feeding heat-stress signals into energy-demand and labor-productivity tiles, freeze-event signals into commodity-price tiles, drought signals into food-inflation and shipping-disruption tiles. The free open-data layer (NOAA CDO + GHCN daily + ERA5 via CDS) is more than enough. The cost is **storage**, not API budget.

## What "climate as macro signal" means concretely

Three known channels into macro forecasting:

1. **Heat stress → energy demand → electricity prices → core CPI energy component.** A heat-dome on the US southwest in July reliably blows out peak load. The same heat-dome two summers in a row shifts air-conditioning capex into the inflation basket.
2. **Drought → crop yield → soft-commodity prices → headline CPI food.** A US plains drought hits corn, soybeans, wheat at planting. Mediterranean drought hits olive oil, durum wheat. Indian monsoon shortfall hits rice and sugar.
3. **Freeze / hurricane / flood → infrastructure shock → industrial-production lag.** Texas Feb-2021 freeze took out US semiconductor capacity for weeks. A hurricane through the Gulf takes refinery capacity offline. Floods in Pakistan or Thailand take out textile and electronics.

These are documented in the literature (Burke et al on temperature-GDP; Auffhammer on climate-energy; Hsiang on hurricanes-and-growth). OPENGEM doesn't need to recreate the models — it needs to publish the *signal series* (degree days, drought index, heat-stress index) so the dashboard can show them alongside the macro response.

## NOAA Climate Data Online (CDO)

- **Base URL**: `https://www.ncei.noaa.gov/cdo-web/api/v2/`
- **API style**: REST. JSON.
- **Auth**: free token, requested via email registration at `ncdc.noaa.gov/cdo-web/token`. Header: `token: XXX`.
- **Rate limits**: **5 requests/sec, 10,000 requests/day per token**. Hard, enforced.
- **Datasets accessible via API**:
  - **GHCND** (Global Historical Climatology Network Daily) — station-level daily summaries.
  - **GHCNM** (GHCN monthly) — station monthly summaries.
  - **GSOM / GSOY** (Global Summary of the Month / Year) — pre-aggregated.
  - **NORMAL_HLY** / **NORMAL_DLY** / **NORMAL_MLY** — 30-year climatology normals.
  - **PRECIP_15** / **PRECIP_HLY** — high-frequency precipitation.
- **Output**: per-station + per-date + per-element (TMAX, TMIN, PRCP, SNOW, AWND, etc.).
- **License**: U.S. federal government — **public domain (CC0-equivalent)**. GREEN.

## GHCN Daily — the bulk path

For OPENGEM's overlay needs we don't want to hammer the API one station at a time. The right pattern is **bulk via the NOAA NCEI HTTP file path or AWS Open Data mirror**.

- **HTTP**: `https://www.ncei.noaa.gov/pub/data/ghcn/daily/`
- **AWS S3 mirror**: `s3://noaa-ghcn-pds/` (Registry of Open Data on AWS — `aws s3 cp s3://noaa-ghcn-pds/csv/by_year/2026.csv -`)
- **Bulk artifacts**:
  - `ghcnd-stations.txt` — metadata for ~100k stations in 180 countries.
  - `ghcnd-all.tar.gz` — every station's full history (~5 GB).
  - `ghcnd-gsn.tar.gz` — GCOS Surface Network subset (~few hundred MB).
  - `ghcnd-hcn.tar.gz` — US Historical Climatology Network subset.
  - `by_year/{YYYY}.csv` — single-year CSV with all stations × all elements.
- **Bandwidth**: full historical ~5 GB; annual increment ~150 MB. Cheap.

For OPENGEM's purposes, **the `by_year/{YYYY}.csv` files via AWS are the right ingest pattern**. We pull the current-year file weekly, the prior 5 years monthly, the deep history once at bootstrap.

## ERA5 reanalysis via Copernicus CDS

- **Base URL**: `https://cds.climate.copernicus.eu/api` (CDS API via the `cdsapi` Python client).
- **Auth**: free CDS account; per-account API key.
- **Rate limits**: per-request size caps — **120,000 fields per ERA5-hourly request**, **10,000 fields per ERA5-monthly request**. ("Fields" = variable × level × timestep.) Concurrent request limit per account (not documented; community-tested at ~4 active jobs).
- **Job model**: each request enters a queue, processed asynchronously, results returned as a downloadable GRIB/NetCDF file. Average wait ~minutes to hours depending on dataset and queue depth.
- **Coverage**: hourly global gridded reanalysis 0.25° × 0.25° from 1940-present. ~250+ variables (temperature, precipitation, humidity, wind, soil moisture, etc.). Land + ocean + atmosphere.
- **License**: **Copernicus License** — equivalent to CC-BY-4.0 with attribution to "Copernicus Climate Change Service (C3S)" and version-and-modification-disclosure. GREEN with attribution.
- **Storage**: ERA5 native GRIB files are big. A single global variable for a single year at hourly cadence is ~100 GB. **OPENGEM cannot mirror ERA5; we extract small subsets only.**

## Practical OPENGEM use case: degree days + drought index

The signal series we actually want on the dashboard:

1. **Heating degree days (HDD) and cooling degree days (CDD)** per major economic region (US Census divisions, EU NUTS-2 regions, India states, China provinces). Computed from GHCN daily TMAX/TMIN. Monthly aggregation. Updates daily.
2. **PDSI (Palmer Drought Severity Index) or SPI** per agricultural region. NOAA publishes US-only via CDO; global via ERA5-derived datasets in Copernicus.
3. **Heat-stress days** (T_max > 35°C, T_min > 25°C overnight) per region. Computed from GHCN.
4. **Hurricane / cyclone tracks** — NOAA HURDAT2 dataset (free, public domain, separate small download).

These are all derivable from GHCN daily + ERA5 monthly aggregates. We don't need real-time gridded data.

## Rate-limit math for OPENGEM

**NOAA CDO API**:
- Aggregation pre-computation runs on local cache (GHCN bulk CSV), so live API calls are minimal.
- Spot lookups only: ~50 stations × 1 call/day = 50 calls/day. Well under 10k limit.

**GHCN bulk via AWS**:
- 1 download of current-year CSV per week + monthly trail of 5 years. Total ~5 file pulls/week. Trivial.

**ERA5 via CDS**:
- Monthly heat-stress signal for ~50 economic regions × 1 year request per region = ~50 CDS jobs per month. Each job <10,000 fields. Total budget: ~50 queue submissions/month, run overnight.
- Backfill: ERA5 1980-current for 50 regions = ~500 jobs. Spread over a week, no problem.

## Vintage truth

- **NOAA GHCN**: each station's record gets back-revised when QC flags fire. Bulk CSVs are wholesale replacement; we snapshot at ingest and treat each pull as a vintage.
- **ERA5**: reanalysis is "frozen" for any given date — but ERA5 itself has been re-released (ERA5.1 corrections). When ERA5T (preliminary near-real-time) gets replaced by final ERA5, the values change ~5 days later. Adapter must distinguish ERA5T vs ERA5.

## Fit-for-OPENGEM verdict

- **ADOPT-NOW**: NOAA CDO for spot lookups + GHCN bulk CSV via AWS S3 for full daily history.
- **ADOPT-BLOCK-II**: ERA5 via CDS API for gridded heat-stress and drought maps.
- **CITE-ONLY**: paid ECMWF / NOAA partners.
- **SKIP**: full hi-resolution ERA5 mirror (storage cost prohibitive for our scope).

**Adapter design notes**:

- New package `opengem-data-climate`.
- Submodule 1: `NOAAGHCNBulkAdapter` — downloads year CSVs from AWS, processes into per-region aggregates (HDD/CDD, heat-stress days, freeze events).
- Submodule 2: `NOAACDOAdapter` — REST client for ad-hoc spot lookups, used by the dashboard's "weather context for date X" feature.
- Submodule 3: `ERA5CDSAdapter` — wraps `cdsapi` Python client, submits jobs, polls, downloads results. Optional dependency.
- Provenance: every Observation records `source=ghcn|cdo|era5`, `variable=...`, `region=...`, `version=...`.

## The macro link — concrete dashboard features

- **Energy page**: chart of monthly HDD/CDD per region overlaid on natural-gas and electricity demand series. Heating-demand attribution on European gas storage drawdown.
- **Commodity page**: chart of growing-season SPI for top-10 corn/wheat/soy producing regions overlaid on futures prices. Drought-attribution on grain export collapses.
- **Industrial-production page**: chart of hurricane/freeze count by region overlaid on monthly IP. Shock-attribution on regional manufacturing dips.
- **Labor-productivity page** (Block II): heat-stress days per region overlaid on hours-worked.

These are the kinds of chart that **no other open dashboard ships today** in a coherent macro context. Bloomberg has the weather data but not in a macro-linked product. OWID has the climate data but not in a macro-linked product. **OPENGEM has the opportunity to be the first.**

## Trap log

- **GHCN station coverage is uneven** — US, EU, Australia have dense networks; Africa and central Asia are sparse. Region aggregates need to weight by station density or use ERA5 reanalysis as the fallback.
- **NOAA CDO token rate limit is per-token, not per-IP**. Multiple OPENGEM processes sharing one token will hit the 5 RPS / 10k RPD cap together. Use separate tokens per adapter instance if scaling.
- **ERA5T vs ERA5 final** is a 5-day rolling delay; adapter must record which version it got.
- **Copernicus License attribution** has a specific verbatim form required — adapter should emit it as a constant string in provenance.
- **ERA5 GRIB files require `cfgrib` / `ecCodes`** to parse; pure-Python NetCDF can't do them. NetCDF subset requests are slower than GRIB but easier to parse — use NetCDF for ingestion unless you need the full variable set.
- **Local Climate Data Online endpoints (`api.weather.gov`, NWS)** are a *different* API for US-only forecasts/observations; don't confuse with CDO historical.

## Related

- [[L053]] — Energy (HDD/CDD drives gas demand)
- [[L056]] — Commodity prices (drought drives grain)
- [[L055]] — Shipping (hurricane closes ports)
- [[R06]] (existing) — wider information surface
