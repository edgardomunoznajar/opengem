# L060 — Crypto on-chain as macro proxy: CoinMetrics Community, DeFiLlama, Blockchain.com

**Loop**: 060 / 300
**Phase**: 1 — Open-source landscape survey (data sources)
**Date**: 2026-06-06
**Verdict**: **ADOPT-NOW CoinMetrics Community + DeFiLlama + Blockchain.com charts** for the macro-relevant subset. **CITE-ONLY Glassnode free tier** (too thin). **SKIP** paid Glassnode and similar — not worth the budget for OPENGEM's macro use case.

---

## One-line take

Crypto is interesting to OPENGEM **only as a macro signal layer**, not as a trading product. The on-chain narrative — Bitcoin as inflation hedge, stablecoin supply as dollar-shadow-banking proxy, DeFi TVL as risk-on barometer — is the part that matters. Three free, GREEN/YELLOW sources cover this completely: **CoinMetrics Community for daily Bitcoin/Ethereum on-chain metrics with CC license**, **DeFiLlama for cross-chain TVL and stablecoin flow data**, and **Blockchain.com charts for canonical Bitcoin network statistics**.

## Why crypto data in a macro dashboard at all

Three documented macro channels:

1. **Stablecoin supply (USDT + USDC + DAI + others)** ≈ shadow-banking dollar liquidity. Total stablecoin supply has correlated with EM dollar liquidity conditions since ~2019. A stablecoin redemption wave is a tightening signal. Important for sovereign-risk overlay.
2. **Bitcoin as an inflation hedge / store of value / "digital gold"** narrative — whether or not it actually works as one, the *narrative* affects macro flows. Bitcoin price is now a watched macro variable.
3. **DeFi TVL (Total Value Locked)** as a risk-on barometer. TVL contraction by 50%+ in a month signals broader crypto-financial stress, which spills into traditional finance via prop trading desks, FTX-style failures, and crypto-friendly bank failures (SVB / Signature 2023).

None of these need real-time on-chain analytics. **Daily aggregates are sufficient.**

## CoinMetrics Community Network Data

- **Base URL**: `https://community-api.coinmetrics.io/v4/` (or `https://api.coinmetrics.io/v4/` with the same endpoints, just enforcing community tier without key).
- **API style**: REST. JSON + CSV (via `format=csv`).
- **Auth**: **none required** for community endpoints.
- **Coverage**: ~30 on-chain metrics across ~10 assets (BTC, ETH, BCH, LTC, XMR, XRP, ZEC, plus a handful). Daily resolution.
- **Metrics included**: active addresses, transaction count, transaction volume, hash rate, miner revenue, supply, fee rate distribution, realized cap, market cap, MVRV ratio, NVT ratio.
- **Update cadence**: daily, T+1d.
- **Rate limits**: undocumented for community tier; community-tested at sub-1 RPS.
- **License**: **Creative Commons Attribution-NonCommercial 4.0 (CC-BY-NC 4.0)**. **YELLOW**. NonCommercial clause matters: we can show the data on the free dashboard tier; the **paid API tier** of OPENGEM cannot include CoinMetrics community data without explicit Pro subscription.
- **Vintage**: published values are not retroactively revised once finalized; trivial vintage.

## DeFiLlama

- **Base URL**: `https://api.llama.fi/` (also `https://api.defillama.com/`).
- **API style**: REST. JSON.
- **Auth**: open API, no key required.
- **Coverage**: protocol-level TVL across ~3,000 DeFi protocols × ~200 chains. Daily resolution. Also stablecoins, DEX volumes, fees, treasury, governance, and a "yields" sub-product.
- **Endpoints we want**: `/protocols` (list), `/protocol/{name}` (TVL history), `/stablecoins`, `/chains`.
- **Update cadence**: real-time to hourly.
- **Rate limits**: free tier is "open and free"; the DeFiLlama Pro tier offers higher quotas and additional endpoints.
- **License**: **DeFiLlama API is "open" and citing as source is "much appreciated"**. Not formally CC-BY in the announcement, but the spirit of the project is open-source / open-data. **GREEN with attribution** in OPENGEM's practical interpretation.
- **Vintage**: historical TVL is recomputed when contract data changes (a rare event); adapter snapshots.

## Blockchain.com Charts API

- **Base URL**: `https://api.blockchain.info/charts/{metric}?format=json` (the legacy stable endpoint).
- **API style**: REST. JSON.
- **Auth**: none.
- **Coverage**: Bitcoin only. Hash rate, difficulty, block size, transaction count, mempool size, fee, miner revenue, total supply.
- **Update cadence**: per-block to daily.
- **License**: free use, attribution requested.
- **Verdict**: **GREEN with attribution**.

## Glassnode

- **Free tier**: weekly delayed snapshots of MVRV, SOPR, exchange flows. Very thin.
- **Paid tiers**: Advanced + Professional run hundreds of dollars per month.
- **Verdict**: **CITE-ONLY free; SKIP paid** for Block I. The CoinMetrics Community + DeFiLlama combination covers OPENGEM's macro use case without the cost.

## CoinGecko / CryptoCompare

- Both offer free tiers with API keys, 10-50 calls/min. CoinGecko free tier is the standard for spot price + market cap data.
- **Verdict for OPENGEM**: **ADOPT-BLOCK-II CoinGecko** if we want a "crypto market overview" tile (top-10 by market cap, 24h change). Not strictly necessary because price data is already in CoinMetrics Community.

## Rate-limit math for OPENGEM

**CoinMetrics Community**:
- Daily refresh: ~30 metrics × ~10 assets = ~300 cells. With endpoint batching, ~10 calls/day.
- Backfill: ~30 calls per asset per metric ÷ batched = ~30 calls.
- Total: trivial.

**DeFiLlama**:
- Daily refresh: ~5 calls per day for protocol TVL aggregates + 1 call for stablecoin totals.
- Backfill: 1-2 calls.

**Blockchain.com Charts**:
- 1 call per metric per day × ~10 metrics = 10 calls/day.

**Total crypto adapter budget**: ~25 calls/day. Negligible.

## The CC-BY-NC trap on CoinMetrics

CoinMetrics Community is **NC** (NonCommercial). This is the same trap we hit with IEA WEO Free Dataset (L053). For OPENGEM:

- **Free public dashboard**: showing CoinMetrics community data is non-commercial use → allowed.
- **Paid API tier**: if a sovereign-fund LP pays $X/month and OPENGEM's response includes CoinMetrics-derived values, that is arguably commercial use → **not allowed without a Pro subscription**.

Concrete OPENGEM rule: **CoinMetrics community data is GREEN for free public dashboard surface, YELLOW for paid API**. The adapter must tag each Observation with `license=cc_by_nc_4.0` and the API tier must filter NC-tagged values out (or substitute with Blockchain.com / DeFiLlama equivalents).

This is the same enforcement pattern we apply to PortWatch in L055.

## Fit-for-OPENGEM verdict

- **ADOPT-NOW**: CoinMetrics Community (for free tier), DeFiLlama (everywhere), Blockchain.com Charts (everywhere).
- **ADOPT-BLOCK-II**: CoinGecko for a "crypto market overview" tile.
- **CITE-ONLY**: Glassnode free.
- **SKIP**: Glassnode paid, CryptoQuant paid, Nansen, Lookonchain commercial. Not worth the spend for OPENGEM's macro stance.

**Adapter design notes**:

- New package `opengem-data-crypto`.
- Submodule 1: `CoinMetricsCommunityAdapter` — REST client. License flag `cc_by_nc_4.0` on every Observation.
- Submodule 2: `DeFiLlamaAdapter` — REST client. Open license attribution.
- Submodule 3: `BlockchainComChartsAdapter` — REST client for legacy chart endpoints.
- Provenance: every Observation records `source=coinmetrics_community|defillama|blockchain_com`, `metric=...`, `license=...`.
- API-tier filter: when serving the paid API, exclude rows where `license=cc_by_nc_4.0` unless we've separately licensed.

## What this enables on the dashboard

- **Sovereign-risk page overlay**: stablecoin supply growth as EM dollar-liquidity proxy.
- **Inflation page overlay**: Bitcoin price vs M2 growth vs gold.
- **Financial-conditions page overlay**: DeFi TVL contraction as risk-on/risk-off signal.
- **Sit-rep events**: large stablecoin redemption (>$1B in a day) as event-detector trigger.

These add credible-but-novel angles to OPENGEM's macro pages. No paid data, no markets-data terminal — just CC and open-source aggregations of public blockchain data.

## Vintage truth

On-chain data is observed on-chain and immutable. **Revisions are conceptually impossible** at the chain level. The exception: address-clustering and entity-adjustment metrics (where CoinMetrics or others label addresses as belonging to known entities). Those classifications evolve, and the metric values shift retroactively.

Adapter must record `address_clustering_version` for entity-adjusted metrics.

## Trap log

- **CoinMetrics CC-BY-NC license is binding**. NC clause prevents inclusion in the paid OPENGEM API tier without a Pro subscription. Adapter must tag and the API gateway must filter.
- **DeFiLlama protocol IDs occasionally rename** when a protocol forks or rebrands; adapter must maintain a stable mapping or accept the rename.
- **DeFiLlama TVL methodology debates** — some protocols dispute their reported TVL; we publish the DeFiLlama value but the value is best understood as "DeFiLlama-reported TVL," not ground truth.
- **Blockchain.com charts are Bitcoin-only.** For Ethereum, use CoinMetrics Community + DeFiLlama.
- **Stablecoin supply is fragmented across chains** — USDT lives on Ethereum, Tron, Solana, BSC, Avalanche. Total supply requires summing. DeFiLlama and CoinMetrics both pre-aggregate; trust the pre-aggregated value, don't re-sum.
- **Bitcoin-as-inflation-hedge narrative is contested**; OPENGEM should publish the data with the narrative as a *cited claim*, not as our editorial position.
- **On-chain analytics has a methodology-disclosure problem**: many "professional" providers define metrics differently. CoinMetrics has the most transparent methodology docs of the open providers; prefer it where definitions conflict.
- **DeFiLlama stablecoin endpoint requires unwrapping by issuer** to get the "real" supply (some stablecoins are wrapped versions of others; double-counting risk).

## Related

- [[L056]] — Commodity prices (gold is the "real-world" inflation hedge comparator)
- [[L057]] — FX free APIs (USD-stablecoin relationship)
- [[L049]] — BIS (cross-border banking; stablecoin is a shadow flow)
- [[L053]] — Energy (Bitcoin mining electricity demand is real)
