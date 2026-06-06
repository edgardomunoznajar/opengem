# L002 — Competitive Landscape Map

**Loop**: 002 / 300
**Phase**: 0 — Strategic framing
**Date**: 2026-06-06

---

## The thesis of this loop

There is no single competitor to OPENGEM. There is a *cartel of overlapping incumbents*, each of which solves a slice of the world-economy-information problem, and each of which has a structural reason it cannot solve the other slices. Map them honestly, name the moat, name the weak point, and OPENGEM's positioning falls out almost mechanically.

The point of this loop is not to flatter ourselves. It is to write the obituary the incumbents will refuse to write about themselves.

## The twelve

### 1. Bloomberg Terminal

- **Business model**: ~$28k/seat/year, ~325k seats, ~$10B+ revenue. Bundled package: market data + news + analytics + Bloomberg Chat + IB execution rails.
- **Moat**: Network effects via Bloomberg Chat (you can't leave the terminal because your counterparties live there), proprietary news desk, the Bloomberg ID as financial-industry identity, decades of relationship rails.
- **Weak point OPENGEM exploits**: Macro analysis is the *least* differentiated layer of the terminal — Bloomberg Economics produces nowcasts and forecasts that are not meaningfully better than the open-source frontier, but they cost $28k. The macro-curious, the journalist, the NGO, the academic, the prosumer cannot afford the bundle and don't need the Chat or the IB rails. We carve off the macro slab.
- **Where the dashboard learns from them**: Information density. The Bloomberg screen shows more numbers per cm² than any other product in the industry, and it works because consistent grids, sparklines, lozenges, and four-letter mnemonics are *more* readable than whitespace-luxury layouts once you commit to terminal-feel. OPENGEM should steal the density and reject the secrecy.

### 2. Reuters Eikon / LSEG Workspace

- **Business model**: ~$22k/seat/year, ~190k seats, ~$3B revenue. Same bundle as Bloomberg, weaker chat, stronger commodities + FX news.
- **Moat**: Reuters newswire (the original), exclusive partnerships (LSE order book, some sovereign data), legacy seat penetration in newsrooms and central banks.
- **Weak point**: Eikon is the perennial #2 — every customer they have is one Bloomberg promo away from churn. They cannot publicly publish a track record because it would invite head-to-head with Bloomberg Economics and lose. They have less to lose by *partnering* with an open substrate than Bloomberg does, which makes them a potential ally in Y2-Y3.
- **Where we learn from them**: The Reuters wire's structured-event tagging schema (CRACT, RICs) is a serious piece of data-engineering and the closest thing to a working ontology of geopolitical events outside GDELT. We don't need their content; we need to remember that *events deserve a schema*.

### 3. FactSet

- **Business model**: ~$13k/seat/year, ~210k seats, ~$2B revenue. Heavier on buy-side equity research workflow than Bloomberg.
- **Moat**: Deep integration with PortfolioManager, factor models, ownership data; buy-side analyst workflow lock-in.
- **Weak point**: FactSet has essentially no macro forecasting product worth a damn. Their macroeconomic data is a thin layer over Haver Analytics. A buy-side macro analyst supplements FactSet with Bloomberg precisely because FactSet's macro is weak. OPENGEM can become the *macro sidecar* that a FactSet user pulls into their workflow via Excel/MCP, replacing the second Bloomberg seat.
- **Where we learn from them**: The PA (Portfolio Analytics) report layout — multi-page, dense, citation-stamped, exportable to PDF and PPT — is the template for OPENGEM's tearsheet output. Pros want printable artifacts they can hand to the IC.

### 4. Stratfor (now RANE)

- **Business model**: Subscription geopolitics, ~$300-3000/year/seat depending on tier, plus corporate intelligence contracts. Editorial cadence: weekly forecast, daily intelligence brief.
- **Moat**: Brand association with George Friedman's long-cycle geopolitical thesis, retained corporate clients in oil-and-gas + defense + insurance, OSINT network.
- **Weak point**: Their forecasts are *narratives* not *numbers*. There is no track record because there is nothing measurable to score. When they get a forecast wrong, they rewrite the narrative; when they get one right, they take a victory lap. OPENGEM exploits this directly by publishing geopolitical risk as a *quantified, scored, vintaged series* alongside narrative interpretation. The Stratfor reader who wants a number to defend at the board level will adopt OPENGEM as the receipt.
- **Where we learn from them**: Editorial rhythm. Stratfor's weekly-forecast-plus-daily-pulse cadence is the right tempo for a non-real-time macro product. We steal the cadence and reject the closed track record.

### 5. OurWorldInData (OWID)

- **Business model**: Nonprofit, Oxford-affiliated, donor + grant funded, CC-BY licensed.
- **Moat**: Editorial standards (Max Roser's brand), pedagogical clarity, deep relationships with Wikipedia + textbooks + UN agencies, Google grants for traffic and search ranking.
- **Weak point**: OWID is a *long-arc educational* product — pandemics, poverty, climate, demographics on multi-decade scales. They explicitly do not do current macro, do not do forecasting, do not do near-term economic policy commentary. They have the brand and the pedagogy; they don't have the velocity. OPENGEM is the *daily, scored, forecasting* complement to OWID's *decadal, descriptive, explainer* substrate.
- **Where we learn from them**: Chart design as pedagogy. OWID charts are the gold standard of explain-it-as-you-show-it. Every OPENGEM chart should aim for OWID's annotation density and OWID's "click-through to download the data" trust signal. They are also our most plausible *brand reference partner* — neither of us competes with the other.

### 6. TradingEconomics

- **Business model**: Freemium API, ~$500-5000/year API tiers, ~$50/mo individual. Ad-supported web product. Estimated revenue $20-50M.
- **Moat**: SEO. They have a country page for every indicator for every country and they rank #1 on Google for almost every "[country] [indicator]" query. Brutal SEO discipline plus a 10-year head start.
- **Weak point**: The data is a thin scrape over public sources with no provenance, no vintage history, no methodology, and no forecasts beyond a single naive auto-projection. The brand is "the cheap Bloomberg" and that's a ceiling, not a floor. Pros do not trust TE for real decisions. OPENGEM positions as "TradingEconomics with provenance, vintaging, and forecasts you can audit" — which is what TE customers actually want when they grow up.
- **Where we learn from them**: SEO. TE proves that the country×indicator page is *the* atomic SEO unit for macro data and that you win the long tail by having every cell of the matrix filled. Phase 5 of the dashboard prototyping must commit to this matrix-fill discipline from week one.

### 7. Macrobond

- **Business model**: ~$12-20k/seat/year, sells primarily to central banks, sovereign wealth funds, treasury offices, and macro hedge funds. Estimated revenue $200M.
- **Moat**: The single most comprehensive macro time-series catalog in the world (1M+ series across 1000+ sources), the data engineering operation to keep them fresh, an Excel-and-Word-add-in workflow that economists actually use, and a tight CB-incumbency relationship.
- **Weak point**: Closed catalog, no API beyond their own client, no public track record on any derived series, and the addressable market is *physically capped* by the number of macroeconomists at central banks and sovereign funds (~50k humans worldwide, of which they have ~30k). They cannot expand because their pricing is calibrated to institutional buyers; they cannot open up without cannibalizing the institutional pricing.
- **Where we learn from them**: Series identity discipline. Every Macrobond series has a stable mnemonic, a vintage history, and a documented methodology. OPENGEM's series identifiers must be stable in the same way — once published, never re-keyed.

### 8. OECD Data Portal (incl. ORDRA / OECD Data Explorer)

- **Business model**: Free, taxpayer-funded, member-states.
- **Moat**: Authority — OECD numbers are the citation of record for member-state macro statistics. Coverage of OECD + key partner countries is deep.
- **Weak point**: The interface is a bureaucratic UX nightmare, the data refresh cadence is slow (some series quarterly with multi-month publication lag), the cross-country comparisons are clumsy, and there is essentially no forecasting layer beyond the twice-yearly EO. The data is good; the experience is terrible.
- **Where we learn from them**: SDMX. The OECD's SDMX endpoints are the actual underlying API that everyone scraping macro data is hitting. OPENGEM should be SDMX-native at the ingestion layer, then expose a *humane* layer on top.

### 9. Statista

- **Business model**: ~$1-3k/seat/year, 1M+ subscribers, ~$300M revenue. Industry-vertical statistics aggregator + chart library.
- **Moat**: SEO + chart-marketplace for marketing teams + paywall-gating the "free preview" so corporate buyers convert. Brand association with "official-looking chart for my deck."
- **Weak point**: A huge chunk of Statista's catalog is repackaged public-source data with a Statista watermark, sold at a price that's hard to justify if the buyer realized the underlying source was free. The product is for *people who don't know where the data came from* — which is exactly the audience that LLMs are now serving better and cheaper. Statista's moat is eroding monthly.
- **Where we learn from them**: The chart marketplace is a model. OPENGEM should let any chart be embedded in a deck/post/article with a clean attribution stamp and a "data updates live" promise. Statista charges for the watermark; OPENGEM gives it away in exchange for the backlink.

### 10. TradingView

- **Business model**: Freemium $0/$15/$30/$60 per month tiers, ~600k+ paid users, ~$300M+ revenue.
- **Moat**: The single best charting library on the web, an enormous social-script community (Pine Script), and a browser-first product that markets-Twitter linked-in to.
- **Weak point**: Almost entirely market-data focused (equities, FX, crypto). Macro indicators are a token sidebar. Forecasting is community-script, not institutional-grade. Geopolitics is essentially absent.
- **Where we learn from them**: Lightweight Charts (the open-source charting library TradingView publishes) is the right primitive for OPENGEM's chart layer. We use their tools and skip their domain.

### 11. S&P Capital IQ / IHS Markit (now S&P Global Market Intelligence)

- **Business model**: ~$15-25k/seat/year, enterprise sales to corporate development + investment banking + credit teams. Revenue layered inside S&P Global ($13B total).
- **Moat**: Private-company data, M&A deal database, corporate hierarchies, IHS-legacy macro forecasting (Global Insight), credit-rating-adjacent data.
- **Weak point**: Capital IQ is a corporate-finance tool that happens to have macro data; the macro is not the product. The Global Insight macro forecasts are paywalled and unvintaged in public view. The buyer is the M&A analyst, not the macro analyst.
- **Where we learn from them**: The taxonomy of corporate entities (ticker, ISIN, LEI, parent-subsidiary tree) is the right schema for the *corporate layer* OPENGEM might add in Y2-Y3 if we extend from macro into sovereign credit / EM-corp coverage.

### 12. Refinitiv (now LSEG, post-merger)

- **Business model**: Folded into LSEG; Eikon + Datastream + Refinitiv data feeds. Cross-referenced with #2.
- **Moat**: Datastream macro historical archive (40+ years of every indicator the central banks ever published), Reuters newswire, FX rates.
- **Weak point**: Same as Eikon — perennial #2, no public track record, customer churn risk from Bloomberg. The Datastream archive is the crown jewel but is closed and priced out of reach for non-institutional users.
- **Where we learn from them**: Datastream's historical depth is the *gold standard for vintage history* — they record the actual sequence of revisions for every series. OPENGEM's vintage store should aspire to match Datastream's depth for the most important ~500 series, even if we can't match the breadth.

## The 2x2 positioning map

The cleanest axis split:

- **X-axis: Open ↔ Closed** (license + data accessibility)
- **Y-axis: Dashboard ↔ Report** (continuous-live-product vs episodic-publication)

```
                            DASHBOARD (live, queryable, embeddable)
                                          │
                                          │
                 TradingEconomics ◆        │        ◆ Bloomberg Terminal
                                          │        ◆ Reuters Eikon
            TradingView ◆                  │        ◆ FactSet
                                          │        ◆ Capital IQ
                                          │        ◆ Macrobond
                            ▶ OPENGEM ◀   │
                                          │
       OPEN ◀────────────────────────────┼────────────────────────────▶ CLOSED
                                          │
                 OECD Data Portal ◆        │        ◆ Refinitiv Datastream
                                          │
                                          │        ◆ Stratfor / RANE
            OurWorldInData ◆               │        ◆ Statista
                                          │
                                          │
                            REPORT (episodic, narrative, static)
```

The OPEN × DASHBOARD quadrant is *empty*. OWID lives in OPEN × REPORT (educational, episodic). TradingEconomics lives in MIXED × DASHBOARD (free tier exists but provenance is closed). OECD lives in OPEN × REPORT (data is free but the interface is a report-generator, not a dashboard). Every closed competitor is in CLOSED × DASHBOARD.

**OPENGEM colonizes the empty quadrant.** Open license, open code, open vintage history, dashboard-first, machine-readable. There is no incumbent in this square because the incumbent business models require the other three.

## What this loop produced

- Twelve incumbents profiled with business model + moat + weak point + lesson.
- A 2x2 positioning map locating the empty quadrant OPENGEM occupies.
- A repeatable structural read: every closed incumbent's moat is exactly its incapacity to publish a track record.

## What comes next

- **L003** turns these incumbents into the *triggers* that push real personas to switch.
- **L007** translates the lessons-from-incumbents into the distribution thesis.
- **L008** crystallizes the differentiation into five promises no incumbent can credibly make.

## Related

- [[L001-vision-statement]] — the "publish your mistakes" thesis that the empty quadrant rewards
- [[L003-personas]] — the humans living inside the incumbent products today
- [[L008-differentiation]] — the five promises that follow from the empty quadrant
- [[R100-vision]] — the original five-year arc that anticipated this gap
