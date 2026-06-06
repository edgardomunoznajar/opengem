# L055 — Shipping: IMF PortWatch, MarineTraffic, AIS Hub, OpenSky

**Loop**: 055 / 300
**Phase**: 1 — Open-source landscape survey (data sources)
**Date**: 2026-06-06
**Verdict**: **ADOPT-NOW IMF PortWatch** (the real prize), **ADOPT-BLOCK-II AISHub + aisstream.io** for vessel-level supplement, **SKIP MarineTraffic / Kpler paid feeds**, **ADOPT-BLOCK-II OpenSky** for air-cargo macro proxy.

---

## One-line take

The fact that the IMF *publishes* PortWatch as an open dataset is the under-told story in macro data of the last three years — it's a satellite-derived, daily, 2,065-port + 28-chokepoint vessel-activity dataset that **replaces 80% of the use case for paid AIS feeds** in a macro context. We adopt PortWatch as the headline shipping layer and reach for AIS only when port-level isn't granular enough.

## What we want shipping data for in OPENGEM

- **Chokepoint flow** (Suez, Panama, Hormuz, Bab-el-Mandeb, Bosphorus) — closures here move oil prices, container rates, and global supply chain pressure within hours.
- **Major-port congestion** (Shanghai, Los Angeles/Long Beach, Rotterdam, Singapore, Antwerp) — congestion here lags by weeks and predicts trade-flow volumes 1–2 months out.
- **Vessel type breakdown** (container, tanker, dry bulk) — tells you which sector is moving (consumer goods vs energy vs commodities).
- **Long-tail port slowdowns** as event signals for scenario trigger (e.g., port strike, hurricane impact).

We do **not** need individual vessel tracking for macro purposes. That's a maritime-domain-awareness use case, not a macro use case.

## IMF PortWatch (the headline)

- **Base URL**: `https://portwatch.imf.org/` (Esri ArcGIS Online platform).
- **Datasets**:
  - **Ports** — 2,065 ports globally with daily port-call counts and preliminary cargo-volume estimates.
  - **Chokepoints** — 28 maritime chokepoints with daily transit calls and transit-trade-volume estimates.
- **API style**: Esri GeoServices REST API (also exposes WMS and WFS for GIS clients). CSV, KML, ZIP, GeoJSON, GeoTIFF, PNG output.
- **Auth**: none. Public ArcGIS hub.
- **Rate limits**: not formally published. Esri ArcGIS Online generally tolerates a few RPS per IP; house rule 1 RPS for OPENGEM.
- **Update cadence**: **daily port-call data updated weekly on Tuesdays**. Chokepoint data daily.
- **Source data**: satellite AIS from UN Global Platform (free to IMF; downstream consumers like us get the *derived* daily/weekly aggregates, not the raw AIS).
- **Coverage**: 90,000 ships globally tracked, classified by type (container / tanker / dry bulk / general cargo / passenger / fishing).
- **License**: IMF terms — open access for non-commercial and research use with attribution, no resale of unmodified bulk. **YELLOW** — usable in the OPENGEM dashboard (we serve derived charts), but cannot ship the raw daily file as a Datasette dump.
- **Vintage**: PortWatch publishes a forward-only series — no archived prior vintages. Daily values get retrospectively revised as the satellite processing catches up; the public file shows the latest at any moment. We snapshot at ingest.

## AIS Hub (the free vessel-level option)

- **Base URL**: `https://www.aishub.net/api/...`
- **API style**: XML / JSON / CSV REST.
- **Auth**: free API access **conditioned on contribution** — you must run an AIS receiver feeding at least 10 vessels (7-day average) at 90% uptime to qualify. This is the "share to get" model.
- **Rate limits**: 1 request per minute hard cap. The service silently returns nothing if you call more frequently.
- **Coverage**: aggregated AIS feed from member contributors. Coverage strong in major maritime regions, sparse in open ocean.
- **License**: free use for contributors, commercial restrictions apply.
- **Verdict**: **ADOPT-BLOCK-II only if** OPENGEM eventually runs an AIS receiver (we wouldn't), otherwise SKIP for our use case.

## aisstream.io (the free websocket option)

- **Base URL**: `wss://stream.aisstream.io/v0/stream`
- **API style**: WebSocket streaming.
- **Auth**: free API key.
- **Rate limits**: free tier streams real-time global AIS. Per-account caps not publicly listed.
- **License**: free for personal and non-commercial; commercial use requires consent.
- **Verdict**: **CITE-ONLY** for OPENGEM's pure-macro stance; revisit in Block II if we add a sit-rep "live ship tracking" widget.

## MarineTraffic / Kpler (paid)

- **Status as of 2025**: MarineTraffic absorbed into Kpler; no public per-tier pricing; enterprise-only sales motion.
- **Free tier**: 3-day historical data, web UI only — no API.
- **Verdict**: **SKIP** for Block I and Block II. PortWatch covers the macro use case.

## Datalastic / VesselFinder / VesselAPI

- Self-serve paid APIs in the $80–$500/month range with free trials.
- **Verdict**: SKIP unless a sovereign-fund LP customer wants per-vessel feed; in that case, charge through.

## OpenSky Network (air cargo as macro proxy)

- **Base URL**: `https://opensky-network.org/api/`
- **API style**: REST.
- **Auth**: anonymous + free registered tiers.
- **Rate limits**: **400 requests/day anonymous, 4,000 requests/day registered, 8,000 requests/day for active contributors** (with their own ADS-B receiver). Anonymous limit: one call per 10 seconds. Rate limits enforced on `/states/all`, `/flights/*`, `/tracks/all`.
- **License**: free for personal and non-profit; commercial use requires consent.
- **What it tracks**: aircraft only (ADS-B). Not ships.
- **OPENGEM macro use case**: air freight tonnage at major cargo hubs (HKG, PVG, MEM, ANC) as a leading indicator for high-value electronics trade. Niche, but for the supply-chain page it's a useful overlay.
- **Verdict**: **ADOPT-BLOCK-II** for an air-cargo tile on the supply-chain page.

## Rate-limit math for OPENGEM

**PortWatch**:
- Daily refresh: 2 calls (ports + chokepoints) per day. Trivial.
- Weekly bulk: 2 ZIP downloads on Tuesdays. Trivial.

**AISHub / aisstream**: not adopted in Block I; if added later, modest cost.

**OpenSky**:
- 4-hub daily air-cargo aggregation: ~20 calls/day for registered tier. Well under 4,000 limit.

**Total adopted shipping budget**: <5 calls/day. **Cheapest adapter in the OPENGEM stack.**

## What PortWatch uniquely gives us

The macro stories that PortWatch makes visible, which weren't visible on the open web before 2023:

- **2024 Red Sea / Bab-el-Mandeb crisis**: PortWatch showed the chokepoint transit collapse and Cape-of-Good-Hope reroute within days.
- **2025 Panama Canal drought**: PortWatch quantified the daily transit drop as a function of water-level constraints.
- **Major port labor actions**: West-Coast lockout signals, Antwerp slowdowns, etc.

These connect directly to GSCPI (already in OPENGEM), CPI energy components, and shipping rates. The "supply chain pulse" page (mentioned in L164 of the queue) is unbuildable without PortWatch.

## Vintage truth

PortWatch values are revised retrospectively as satellite processing completes — typically minor revisions in the first 7–14 days. The IMF publishes only the latest. OPENGEM compromise: snapshot the daily CSV at ingest and tag with retrieval date. This is the same forward-only vintage pattern we use for IFS and BIS.

## Fit-for-OPENGEM verdict

- **ADOPT-NOW**: IMF PortWatch (ports + chokepoints).
- **ADOPT-BLOCK-II**: OpenSky aggregate air-cargo tile; aisstream.io if we want a live ship-tracker widget.
- **CITE-ONLY**: nothing.
- **SKIP**: MarineTraffic, Kpler, Datalastic, VesselFinder for Block I and II.

**Adapter design notes**:

- New package `opengem-data-shipping`.
- Submodule 1: `PortWatchAdapter` — wraps the Esri REST endpoints, pulls daily ports CSV + chokepoints CSV.
- Submodule 2: `OpenSkyAdapter` (Block II) — REST client with anonymous + registered tiers.
- Submodule 3: `AisStreamAdapter` (Block II, optional) — WebSocket client.
- License field on every Observation flags `redistribution_allowed=false` for PortWatch-derived rows.

## Trap log

- **PortWatch license is YELLOW, not GREEN.** We cannot offer "download PortWatch raw" via Datasette. Charts and aggregates are fine. Adapter must enforce the redistribution flag.
- **PortWatch weekly Tuesday update** means our refresh job needs cron-aware retry. Don't schedule the dashboard's "fresh shipping data" claim before Wednesday morning.
- **Chokepoint definitions are fixed by IMF** — 28 named chokepoints. New ones (e.g., emerging Arctic routes) won't appear without IMF methodology update.
- **MarineTraffic discontinued credit-based pricing in January 2025** — old open-source scripts that hit MarineTraffic with stored API keys will now silently fail.
- **AIS Hub's contribution requirement** is enforced — we'd need to deploy an AIS receiver, which is out of scope for OPENGEM.
- **OpenSky's 10-second-per-request anonymous throttle** silently returns 429s. Registered tier is essential for any production use.
- **OpenSky covers aircraft only**; the ECONNREFUSED-laden generic search confusing it with maritime services is a common AI-context error.

## Related

- [[L054]] — Climate (hurricane closes ports, drought lowers Panama)
- [[L053]] — Energy (chokepoint closure → oil price)
- [[L046]] — World Bank Indicators (trade-volume cross-check)
- [[R06]] (existing) — wider information surface
