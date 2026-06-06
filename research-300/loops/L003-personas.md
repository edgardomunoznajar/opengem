# L003 — Six Personas in Depth

**Loop**: 003 / 300
**Phase**: 0 — Strategic framing
**Date**: 2026-06-06

---

## The thesis of this loop

A persona is not a marketing trope. A persona is a *daily workflow* that produces or consumes macro information under a specific set of pressures — time pressure, audience pressure, accuracy pressure, brand pressure. The personas below are the six concrete humans OPENGEM is built for, written specifically enough that any product decision can be tested by asking "would Damian use this? would Nadia trust this? would Priya cite this?"

Each persona below carries: one paragraph of context, five atomic jobs-to-be-done they execute *on a given day*, three tools they currently use, and the one specific trigger that makes them switch to OPENGEM.

---

## Persona 1 — Damian, the macro-curious YouTuber

**Context.** Damian is 31, runs a 47k-subscriber YouTube channel ("MacroFundamentals") and an attached Substack with 8k free / 600 paid subscribers ($8/mo). He films two videos a week: one Sunday-night "what to watch this week" and one Thursday "what just moved." He has no economics degree but reads constantly, has a strong on-camera presence, and his audience is split between US retail traders, expat finance professionals, and EM-curious 22-30 year olds. His revenue is YouTube AdSense ($3-5k/mo) + Substack ($4.8k/mo) + occasional sponsorship from brokers ($1-3k per slot). He needs **citable, screenshot-friendly, fresh macro charts** more than anything else, and he needs them in the 2-hour window between dinner and recording.

**Five daily JTBDs.**
1. Pull a chart of "[country] inflation YoY vs consensus, last 24 months" that he can paste into a Camtasia overlay in under 60 seconds without re-charting in Excel.
2. Find one macro indicator that "surprised" today across the G20 to anchor a thumbnail.
3. Get a one-sentence narrative for a yield-curve move that he can read on camera without sounding like he's reading.
4. Compare today's market-implied path of Fed funds to where it was 30 days ago, with the visual delta obvious.
5. Find a Substack-embeddable chart that updates live, so his weekly post stays current without him re-uploading.

**Three tools today.**
- TradingView (free tier) for FX/equity charts, hits the paywall for fundamentals.
- TradingEconomics for screen-grabs of country pages — fast but he doesn't trust the methodology and his audience increasingly asks "where's that from?"
- Twitter/X feeds of @CelesteHQ, @charlieBilello, @SpencerHakimian for chart references he then redraws.

**One switching trigger.** A comment under one of his videos saying "your TradingEconomics chart had the wrong vintage, the BEA revised this number last week" — followed by a chart from OPENGEM in the replies *with the revision history visible*. He realizes his audience can fact-check him with OPENGEM faster than he can produce content with TradingEconomics. From that point on, every chart he uses needs a provenance stamp, and OPENGEM is the only free source that provides one.

---

## Persona 2 — Nadia, the sovereign-fund LP analyst

**Context.** Nadia is 36, works at an Abu Dhabi-based sovereign wealth fund as a senior associate on the "external macro" team. Her formal job is to monitor the macro environment for the fund's $400M+ of allocations to discretionary global-macro hedge funds and to write a monthly memo recommending allocation shifts. She has a Bloomberg seat ($28k/year, paid by the fund), a Macrobond license shared with two colleagues, and a personal Eikon login from a previous job. She has an econ master's from LSE. Her boss reads three pages: a one-page summary, a one-page chart, and one page of "what changed since last month." Nadia's career depends on calling regime shifts early — and *defending* the call when it's wrong. She works 12-hour days. She does not have time for tools that don't save her at least 30 minutes per use.

**Five daily JTBDs.**
1. Reconcile the IMF WEO inflation forecast, Bloomberg Economics' inflation nowcast, and consensus from the Reuters poll for the next two CPI prints in five G20 countries — and write three sentences on the dispersion.
2. Pull a vintaged time series of "what people thought 2024 US GDP growth would be, looking from each month of 2023" — to argue to her boss that consensus has been systematically pessimistic on US growth for 18 months.
3. Find the most recent track record of three named macro hedge funds against the same indicators they claim to forecast, to support a re-up decision.
4. Generate a tearsheet for one country (Brazil this week) covering: rates, FX, fiscal, current account, political event calendar — formatted to paste into a memo.
5. Get an alert when any G20 country's recession-probability tile crosses a threshold she set last quarter, with the underlying model named.

**Three tools today.**
- Bloomberg Terminal (ECFC, ECST, FXFA functions; Bloomberg Economics nowcasts).
- Macrobond (for the vintaged time series and cross-country plots).
- Internal Sharepoint where she manually maintains "what consensus said when" spreadsheets because no vendor gives her that.

**One switching trigger.** OPENGEM publishes a public track record of its own GDP nowcast against the actual print, alongside Bloomberg Economics' nowcast, alongside consensus. Bloomberg's nowcast was off by 0.4pp; OPENGEM's was off by 0.2pp; both vintages are timestamped. Nadia's boss asks her "why are we paying for a Bloomberg nowcast that's worse than the free one?" She doesn't recommend dropping Bloomberg (the seat is sticky), but she puts OPENGEM into her *defensible-evidence* workflow on the spot. Three months later, the renewal of the $400M hedge-fund allocation references OPENGEM's track record in the memo.

---

## Persona 3 — Marcus, the FT/Reuters journalist

**Context.** Marcus is 44, a senior economics correspondent at the Financial Times. He has been at the FT for 12 years, covered the eurozone debt crisis, has good central-bank sources, and writes 2-3 pieces a week plus a Sunday column. His editor wants every piece to (a) hit before the wire, (b) include at least one chart that's defensible to the readers' commenters, and (c) carry forward to the news desk's broader narrative. He has Eikon, Bloomberg, and Datastream access; he has the FT's own data team for big charts but no bandwidth from them for daily filings. He writes in markdown into the FT CMS. The audience he most fears is *other macro economists who will mock him on Bluesky if his chart is wrong*. He has been burned three times by stale TradingEconomics screenshots; he no longer trusts them.

**Five daily JTBDs.**
1. Pull a chart of "Italian sovereign spread vs German bunds, last 5 years, with three labeled events" — in under 5 minutes, with the source citation auto-generated.
2. Verify a number a central-bank press release just put out by comparing it against the historical series and three forecasters' expectations.
3. Get a sentence-length nudge on what's anomalous in today's eurozone HICP print so he can frame his lede.
4. Pull a *credible* forecast for a future indicator (e.g. "what is the consensus for German Q2 GDP nowcast?") that he can attribute to a named source.
5. Embed a live-updating chart into the FT CMS so his piece stays correct even if the data revises after publication — without re-editing.

**Three tools today.**
- Eikon (his primary; muscle memory).
- Bloomberg (when Eikon doesn't have it).
- The FT's internal data warehouse (slow, requires data-team handoff).

**One switching trigger.** During a 9:30am eurozone HICP print, his Eikon chart is 30 minutes behind the actual release. He tries TradingEconomics; the chart is stale. He tries OPENGEM and gets the updated number, the prior consensus, the revision flag, and a citation link he can paste into his article — in 90 seconds. His piece publishes before the wire. The OPENGEM chart embeds and updates as later revisions come in. His editor notices. Marcus's bookmark bar reorders itself.

---

## Persona 4 — Lin, the NGO / policy researcher

**Context.** Lin is 39, works at the Center for Global Development on debt sustainability in low-income countries. She has a PhD in development economics from Johns Hopkins SAIS. She publishes 4-6 policy briefs a year, comments on IMF Article IV consultations, and gives expert testimony to the House Financial Services subcommittee twice a year. Her work is read by Treasury staffers, World Bank country teams, and journalists. She does not have Bloomberg; she has World Bank Open Data, IMF DataMapper, and a personal Datastream login from a partner university. Her budget for tools is $0 — CGD pays for nothing she can't justify against an existing grant line. Her credibility comes from being *visibly more careful* than the IMF country team in calling debt distress. She publishes vintaged spreadsheets of her own debt projections on Github and is one of the few policy economists who does so.

**Five daily JTBDs.**
1. Pull the latest WEO debt-to-GDP projection for Zambia + the IMF Article IV projection + her own model's projection, side by side with the actual realizations, going back 8 vintages.
2. Find every country in SSA where the gap between WEO forecast and realized GDP growth has been > 1.5pp for two years running.
3. Generate a country-debt-sustainability summary chart for a House testimony footnote.
4. Get an alert when the African Development Bank or the World Bank quietly revises a country's outlook between annual reports.
5. Find an open dataset of bilateral debt service flows to China that she can cite without violating the Chinese MOF non-disclosure.

**Three tools today.**
- IMF DataMapper / WEO API (slow, clunky, but authoritative).
- World Bank IDS (International Debt Statistics).
- Her own GitHub repo of forked + corrected datasets (her actual workflow).

**One switching trigger.** OPENGEM publishes a *public* vintaged time series of the IMF WEO forecast for every country since 2010, with every vintage timestamped — something the IMF itself does not make easy to query. Lin can now write "the WEO forecast for [country] has been revised downward in every vintage since [date]" with a single API call. Her next CGD brief has a chart sourced "WEO via OPENGEM" and the methodology appendix links to the OPENGEM vintage store. The IMF country team reads the brief. Lin's stature compounds. From there, every debt-related chart she publishes points to OPENGEM.

---

## Persona 5 — Greg, the retail prosumer / Substack-er

**Context.** Greg is 52, semi-retired ex-tech-PM in Austin, has $1.4M in a self-directed portfolio, runs a 1200-subscriber Substack ("Greg's Macro Notes") with 80 paid at $5/mo. He posts twice a week — Sunday "what's on my radar" and Wednesday "one chart I'm thinking about." He thinks of himself as a serious amateur, reads Brad DeLong + Joey Politano + Skanda Amarnath, and is allergic to "chart-with-no-source" content. He uses FRED religiously, has a free TradingView account, and pays $96/year for ZeroHedge Pro (which he keeps quiet about because his audience would mock him). He has no Bloomberg, no Eikon, no Macrobond, and no inclination to pay $1000+/year for any tool. He wants the prosumer-tier of macro and he wants it to *look* serious, not retail.

**Five daily JTBDs.**
1. Find a chart that lets him argue "the labor market is still tight by [specific measure] but loosening by [another specific measure]" without redrawing from FRED in Excel.
2. Compare US recession-probability across four named models (Sahm, Mertens, Estrella, NY Fed) in a single chart.
3. Get a *credible-looking* chart for his Substack header that wasn't ripped from Bloomberg or Bilello's Twitter.
4. Quote a number with provenance — "according to OPENGEM, the consensus 2026 Fed-funds path is X, down from Y last month" — so his readers stop emailing him asking for the source.
5. Watch a few EM country tearsheets weekly so he can occasionally surprise his readers with a non-US take.

**Three tools today.**
- FRED (his bedrock).
- TradingView (free tier).
- A Substack-embedded screenshot from his Sunday research session (which means his posts are static and date-stamped).

**One switching trigger.** OPENGEM lets him paste a single iframe into Substack and the chart updates live. His "Wednesday chart" post from last week is still correct this week because the chart re-renders against the current vintage. A subscriber emails: "this is the best macro Substack I read, partly because the charts stay fresh." Greg converts every chart-of-the-week post to an OPENGEM embed. His paid subscriber count starts compounding because his archive is alive, not embalmed. He never writes a post without an OPENGEM chart again.

---

## Persona 6 — Priya, the academic econ PhD

**Context.** Priya is 33, a post-doc at LSE's CEPR-affiliated macro group, working on heterogeneous-agent monetary policy models. She publishes in EJ, AEJ:Macro, Journal of Monetary Economics. She has the LSE library's Datastream and FactSet access, uses the IMF/OECD APIs for replication packages, and is mid-job-market. Her time is split between research (60%), teaching (20%), and replicating-other-people's-stuff (20%). She is a *connoisseur of provenance*: a chart without a source in a paper draft makes her stop reading. She publishes her replication code on Github and accepts that nobody runs it. She wants tools that produce *citable, reproducible, methodology-documented* numbers — and she has zero patience for "trust me, the chart is right."

**Five daily JTBDs.**
1. Pull the latest vintage of US PCE inflation alongside the *real-time* vintage of US PCE inflation as it was published in 2019, to test whether her published paper's reduced-form result is robust to data revisions.
2. Generate a cross-country panel of policy-rate expectations from each central bank's published "implied path" series, with citations to each central bank's methodology.
3. Find a replication-package-grade dataset of "GDP growth, consensus forecast at each vintage, realized" for 40 countries since 2000.
4. Cite a forecast that has a DOI-like permanent identifier she can put in a paper bibliography.
5. Verify whether a working-paper's claim about a forecast revision matches the actual public vintage history.

**Three tools today.**
- FRED + ALFRED (for vintage US data).
- OECD/IMF SDMX APIs (for cross-country).
- Her own Github repo of cleaned panel data shared with three coauthors.

**One switching trigger.** OPENGEM ships a "cite this view" feature — a permanent URL that resolves to the exact vintage of the exact series she was looking at, with a DOI-like identifier and a `.bib` entry on tap. Her next working paper has bibliography entries that resolve to OPENGEM vintage URLs. The CEPR editorial team adopts the cite-this-view pattern. A graduate student emails her: "your paper is the first one I've replicated without breaking on revisions." Priya's department orders the LSE library to write a data-management note recommending OPENGEM. The academic flywheel starts.

---

## What this loop produced

- Six personas with concrete daily workflow, five atomic JTBDs each, named tools, and the specific switching trigger.
- A pattern: every persona switches when OPENGEM solves a *provenance + freshness + cite-ability* problem their current tool cannot solve.
- Three "credibility anchors" (Marcus, Lin, Priya) and three "volume drivers" (Damian, Nadia, Greg), aligned with L001's three-cohort thesis.

## What comes next

- **L004** turns these into a 25-JTBD matrix across persona × time horizon.
- **L005** picks the north-star metric that captures the *common verb* across all six personas (citation, embed, alert, drilldown, lookup).
- **L008** crystallizes the "five promises" framed against the personas' switching triggers.

## Related

- [[L001-vision-statement]] — three-cohort thesis these six personas instantiate
- [[L002-competitive-landscape]] — incumbents these personas currently use
- [[L004-jtbd-map]] — the 25-cell matrix derived from these six personas
- [[L009-anti-personas]] — who deliberately does NOT appear here
