# L004 — JTBDs Map: 25 Atomic Jobs Across Persona × Horizon

**Loop**: 004 / 300
**Phase**: 0 — Strategic framing
**Date**: 2026-06-06

---

## The thesis of this loop

Jobs-to-be-done decomposition forces the team to write product specs that *make sense at the level of a single user-action*. A job is atomic when it can be expressed as `[verb] [object] [for-which] [in-this-time-window]` and tested by asking "did the user finish that one job?" A vague aspiration ("understand the economy") is not a job; a sharp daily action ("pull a chart of US CPI YoY with consensus overlay before 9:00 a.m.") is.

Twenty-five JTBDs sounds arbitrary; it's not. It's the cardinality of "real coverage of the six personas across four time horizons" with one cell tossed out for each axis to keep the matrix tight. We could go to 50 or 100 — we will, in Phase 3 — but the 25 below are the *load-bearing* ones. Every dashboard feature in Phase 5 should map to at least one job in this list. If it doesn't, we either drop the feature or add the job.

## The four horizons

- **NOW** — "in the next 15 minutes." Live, reactive, market-moving-print-just-hit.
- **TODAY** — "before I publish / file / record / brief, today." The daily-publishing rhythm.
- **THIS WEEK / QUARTER** — "for the memo / brief / video / paper / Substack I am writing this week." The compositional rhythm.
- **THIS YEAR** — "for the long-cycle research I am doing." The structural rhythm.

## The 25-cell matrix

| # | Persona | Horizon | The atomic job |
|---|---|---|---|
| 1 | Damian (YouTuber) | NOW | "Show me the US CPI YoY chart with consensus overlay, as a PNG I can paste into Camtasia in 30 seconds, immediately after the BLS release at 8:30 a.m." |
| 2 | Damian (YouTuber) | TODAY | "Tell me which one G20 indicator surprised consensus by the largest standardized deviation today, so I can thumbnail tonight's video around it." |
| 3 | Damian (YouTuber) | THIS WEEK | "Generate a Sunday-night 'what to watch' weekly tearsheet with the upcoming six high-impact releases, their consensus, and the OPENGEM nowcast for each." |
| 4 | Damian (YouTuber) | THIS YEAR | "Pull an embeddable 'Fed funds path: today vs Jan, vs last June' that lives in my pinned Substack post and updates over the year so the post stays current." |
| 5 | Nadia (sovereign LP) | NOW | "Show me the live US Treasury 2s10s curve with the latest Fedspeak event annotations, refreshed every minute on FOMC days, so I can flag dispersion to my PM." |
| 6 | Nadia (sovereign LP) | TODAY | "Reconcile today's BEA Q1 GDP advance estimate against Atlanta GDPNow, OPENGEM nowcast, Bloomberg Economics, and Reuters poll consensus, with each prior vintage timestamped." |
| 7 | Nadia (sovereign LP) | THIS WEEK | "Generate a Brazil tearsheet (rates / FX / fiscal / current account / political calendar) for the monthly memo, with every chart citation-stamped." |
| 8 | Nadia (sovereign LP) | THIS QUARTER | "Pull a quarterly track record of [hedge fund X]'s public macro calls against the actual outcomes, with confidence-weighted scoring, for the LP re-up review." |
| 9 | Nadia (sovereign LP) | THIS YEAR | "Build a saved 'regime monitor' that watches the 10 indicators that historically lead my fund's allocation flips, with alerts on threshold crossings." |
| 10 | Marcus (FT journalist) | NOW | "On the eurozone HICP release, show me the country-level YoY for the four largest member states with the consensus dispersion, in under 90 seconds, ready to paste into the CMS." |
| 11 | Marcus (FT journalist) | TODAY | "Find the one *anomalous* number in today's eurozone release that I can lead with, with a one-line explanation of why it's anomalous (e.g. 'fastest move since 2008')." |
| 12 | Marcus (FT journalist) | THIS WEEK | "Pull a forecast comparison chart (BCE Survey of Professional Forecasters vs Bundesbank vs OPENGEM nowcast) for the column, with each forecaster attributed." |
| 13 | Marcus (FT journalist) | THIS QUARTER | "Embed a live chart in my October column on Italy that updates as the data revises through Q4, with a banner showing latest vintage date." |
| 14 | Lin (NGO researcher) | TODAY | "Show me every SSA country whose latest debt-to-GDP print exceeds the IMF Article IV projection by >5pp, with the date of the IMF projection." |
| 15 | Lin (NGO researcher) | THIS WEEK | "Generate a Zambia debt-sustainability chart for the next brief, with WEO + IMF Article IV + CGD + OPENGEM projections side by side and all vintages timestamped." |
| 16 | Lin (NGO researcher) | THIS QUARTER | "Pull a quarterly cross-country panel of 'WEO forecast revision direction by country' so I can argue the WEO has been systematically biased pessimistic for SSA." |
| 17 | Lin (NGO researcher) | THIS YEAR | "Build the public dataset 'IMF WEO debt-to-GDP forecast, every vintage since 2010, every country' as the citation-target for CGD's 2027 debt agenda." |
| 18 | Greg (Substack-er) | NOW | "Pull a chart of US labor-market 'three-measures-disagreeing' (unemployment vs U6 vs Sahm vs employment-to-pop), one click, click-to-embed for the Wednesday post." |
| 19 | Greg (Substack-er) | TODAY | "Get a one-sentence narrative for what changed in the JOLTS print today, in plain English without finance-jargon, for my Sunday post." |
| 20 | Greg (Substack-er) | THIS WEEK | "Embed three live charts into the Sunday 'what's on my radar' post that update through the week so the post stays correct on Saturday." |
| 21 | Greg (Substack-er) | THIS YEAR | "Get a 'my OPENGEM portfolio' watchlist that aggregates the 8 indicators I write about most and sends me a weekly digest." |
| 22 | Priya (academic) | TODAY | "Pull the real-time vintage of US PCE inflation as it was published on 2019-03-31 to compare to today's revised vintage, for a robustness test in the working paper." |
| 23 | Priya (academic) | THIS WEEK | "Generate a cross-country panel of 'GDP growth forecast at vintage [t-12 months], realized growth, forecast error' for 40 countries since 2000, as a downloadable CSV." |
| 24 | Priya (academic) | THIS QUARTER | "Cite a forecast view using a permanent identifier (DOI-like) that resolves to the exact vintage I saw on 2026-06-06, in the EJ paper's bibliography." |
| 25 | Priya (academic) | THIS YEAR | "Pull a replication-package-grade dataset of 'central bank policy-rate expectations, every vintage, every country' for the new working paper's empirical section." |

## What the matrix reveals

### The verb distribution

Counting the leading verb in each job:

- **Pull / generate / show** (look up a specific thing, *now*): 14 jobs
- **Reconcile / compare** (put two-or-more things next to each other): 4 jobs
- **Embed** (export to an external surface): 4 jobs
- **Alert / monitor** (passive notification): 2 jobs
- **Cite** (create a permanent identifier): 1 job

**Implication.** The dashboard's primary verb is *pull a chart on demand with provenance*. That's 14 of 25 jobs. Every other feature is a derivative of that primitive. The Phase 5 prototyping discipline becomes obvious: get the single-chart-with-provenance pull right before building anything else.

### The horizon distribution

- **NOW**: 4 jobs (all from the three "live publishing" personas: Damian, Nadia, Marcus)
- **TODAY**: 7 jobs (the daily-publishing rhythm; the heaviest cell)
- **THIS WEEK / QUARTER**: 10 jobs (the compositional rhythm; this is where tearsheets live)
- **THIS YEAR**: 4 jobs (the structural rhythm; this is where embed and dataset-citation live)

**Implication.** "Today" is the heaviest cell, which means *the daily-publishing workflow* is the killer app, not the live ticker. OPENGEM does not need to compete with Bloomberg's millisecond-latency feed; it needs to dominate the 8:00-10:00 a.m. window when releases land and the daily publishing humans (Damian, Marcus, Nadia, Greg) are writing.

### The cross-cutting features

Five features cover the majority of the matrix:

1. **The chart pull** with PNG/SVG export and citation stamp (covers jobs 1, 5, 7, 10, 14, 18, 22).
2. **The forecast comparison overlay** with consensus + multiple-model + named-forecaster attribution (covers jobs 6, 8, 12, 15, 16).
3. **The vintage time machine** — "show me this series as it was published on date X" (covers jobs 6, 8, 17, 22, 23, 25).
4. **The live embed** — iframe / oembed that auto-updates (covers jobs 4, 13, 20).
5. **The cite-this-view** permanent identifier (covers jobs 7, 15, 24, 25).

**Five features. Twenty-five jobs.** That's a useful concentration. The Phase 3 IA loops should be organized around these five primitives, not around country-page / indicator-page taxonomies. We build the *primitives* and let the page-taxonomies fall out of where they're composed.

### The credibility-vs-volume asymmetry

The pro/credibility personas (Marcus, Lin, Priya, Nadia) lean heavily on **vintaged history, methodology, citation**. The volume personas (Damian, Greg) lean heavily on **freshness, visual polish, embed-ability**. The two sets share the chart-pull primitive but diverge sharply on what comes next.

This means the dashboard has *two* surfaces from day one:
- A **public surface** optimized for fast pull + screenshot + embed (Damian / Greg).
- A **research surface** optimized for vintaged history + comparison + citation (Marcus / Lin / Priya / Nadia).

They share the data layer. They diverge on the UI affordances. Phase 3 IA must reflect this.

## What this loop produced

- A 25-cell persona × horizon matrix with concrete atomic jobs.
- A verb-count showing "pull a chart with provenance" is 14 of 25 jobs.
- A horizon-count showing "today" is the heaviest cell — the daily-publishing window is the killer app.
- A five-primitive feature distillation that covers the whole matrix.
- A public-surface vs research-surface UX split.

## What comes next

- **L005** picks the north-star metric around the dominant verb ("pull a chart with provenance").
- **L007** translates the daily-publishing window into the distribution thesis.
- **L121–L180** (Phase 3 IA) builds the dashboard around the five primitives.
- **L181–L230** (Phase 4 forecasting) builds the comparison + vintage layer that pro personas need.

## Related

- [[L001-vision-statement]] — three-cohort thesis these 25 jobs instantiate
- [[L003-personas]] — six personas these jobs decompose
- [[L005-north-star-metric]] — the metric chosen from the dominant verb
- [[L007-distribution]] — the channel strategy keyed to the "today" horizon
