# L227 — Election Calendar + Political Risk Page

**Loop**: 227 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The thesis of this loop

Elections are *the* event with the most known timing and the least-priced macro impact. Every election in 2024 was known a year in advance. Every election in 2028 is known today. Yet the macro implications — currency volatility around the date, sovereign-spread widening pre-election, equity-market drawdown probability — are rarely surfaced in a forward-looking calendar. **Polymarket and Kalshi price US elections.** Wisdom-of-crowd polling sites (538, Polling Report, NateSilver.com) publish polls. *No public dashboard combines election dates, current polling spreads, market-implied volatility, historical base-rate macro impact, and incumbent-vs-challenger policy distance into one view.*

OPENGEM's election + political-risk page is the page that, eighteen months before the 2028 US election, displays: the calendar, the candidate field, the rolling polling spread, the market-implied currency vol on election week, the historical 6-month-post-election GDP/CPI/spread response in similar elections, and a "policy-distance" measure between candidates. It is the page that, when a Mexican peso collapse is brewing pre-AMLO-successor election, becomes the *receipt* for the trade.

This loop **decides** the page structure (calendar + polling + market-implied + base-rate), the political-risk scoring methodology, and the integration with V-Dem democracy data for institutional context.

## The four panels

1. **Global calendar** — every national election (executive + legislative) for the next 24 months, sortable and filterable.
2. **Polling + market-implied** — per election, polling spread, prediction-market implied probability, options-implied event vol.
3. **Base-rate impact** — historical impact of similar elections (incumbent loss, polarization spike, status quo win) on local FX, equity, sovereign spread.
4. **Institutional context** — V-Dem democracy indices, freedom-of-press, polity score, electoral integrity — the "is this election even a real election?" filter.

## Page structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ ELECTIONS + POLITICAL RISK                                           │
│ Calendar, polls, market-implied, V-Dem context.                      │
└──────────────────────────────────────────────────────────────────────┘

[Tabs]
 [Global calendar]  [Per-election]  [Polling tracker]  [Country pol-risk]

╔══════════════════════════════════════════════════════════════════════╗
║ GLOBAL CALENDAR                                                       ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Calendar grid (next 24 months) ───────────────────────────────────┐
│ Date       │ Country │ Type      │ Tier│ Pol-risk│ Mkt vol implied  │
│ 2026-06-15 │ MEX     │ State-Edomex│ T2 │ moderate│ low              │
│ 2026-09-13 │ DEU     │ Bundestag  │ T1  │ low     │ low              │
│ 2026-09-20 │ ITA     │ Region-EU  │ T2  │ moderate│ low              │
│ 2026-10-25 │ ARG     │ Mid-term   │ T2  │ high    │ moderate         │
│ 2026-11-03 │ USA     │ Mid-term   │ T1  │ high    │ moderate         │
│ 2027-02-14 │ KOR     │ Presidentl │ T1  │ moderate│ moderate         │
│ 2027-04-19 │ FRA     │ Presidentl │ T1  │ high    │ high             │
│ 2027-06-13 │ JPN     │ Upper Hs   │ T1  │ low     │ low              │
│ 2027-10-16 │ CAN     │ Federal    │ T1  │ moderate│ moderate         │
│ 2028-01-20 │ TWN     │ Presidentl │ T1  │ extreme │ extreme          │
│ 2028-05-06 │ IDN     │ Local      │ T2  │ low     │ low              │
│ 2028-11-07 │ USA     │ Presidentl │ T1  │ extreme │ extreme          │
│ ...                                                                   │
│                                                                       │
│ Tier definitions:                                                    │
│  T1: national executive or legislative (currency-moving)             │
│  T2: subnational or mid-cycle                                        │
│                                                                       │
│ Sort by: date / pol-risk / vol-implied                                │
│ Filter by: country group / tier / pol-risk threshold                  │
└─────────────────────────────────────────────────────────────────────┘

┌─ Calendar visualization (Gantt-style) ─────────────────────────────┐
│  Horizontal time axis 2026-2028, countries as rows                  │
│  Each election = a vertical marker, colored by pol-risk             │
│  Hover → tooltip with current poll spread + implied vol              │
│  Click → opens per-election detail                                   │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ PER-ELECTION DETAIL                                                   ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Selected: USA 2028 Presidential Election ─────────────────────────┐
│                                                                      │
│ Election date: 2028-11-07                                            │
│ Days to election: 510                                                │
│ Candidates (declared):                                               │
│   - Democratic: [TBD] (primary in spring 2028)                       │
│   - Republican: [TBD] (primary in spring 2028)                       │
│   - Third party: ...                                                 │
│                                                                      │
│ Polling tracker (when available):                                    │
│   - 538 aggregate: not yet                                           │
│   - Polymarket implied: GOP 52% / DEM 44% / Other 4% (current)       │
│   - Kalshi implied:    GOP 50% / DEM 46% / Other 4%                  │
│                                                                      │
│ Market-implied volatility on election week:                          │
│   - 1m USDJPY ATM vol, fwd 510d:  8.4 (vs 6.5 baseline)              │
│   - 1m S&P ATM vol, fwd 510d:    24.5 (vs 17.0 baseline)             │
│   - 1m 10y yield vol, fwd 510d:  +35bp (vs +18bp baseline)           │
│   → Currency mkts pricing 2.0x normal vol, equity 1.4x, rates 1.9x   │
│                                                                      │
│ Historical base rates (similar elections):                           │
│   - Incumbent re-elected: 60% historical, current pricing 48%         │
│   - 6m-post FX move on similar outcomes: ±3.1% median                 │
│   - 6m-post equity move: ±5.8% median                                 │
│                                                                      │
│ Policy distance index (declared candidates):                         │
│   - GOP-DEM policy distance: 0.78 (high; 2020=0.65, 2016=0.72)       │
│   - Drivers: trade policy, immigration, energy                       │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ POLLING TRACKER                                                       ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Polling trajectory (per election) ────────────────────────────────┐
│  Y: vote-share % for each candidate                                  │
│  X: months out from election                                         │
│  Lines: one per candidate                                            │
│  Band: aggregator confidence interval                                │
│  Annotations: debates, scandals, endorsements                        │
└─────────────────────────────────────────────────────────────────────┘

┌─ Prediction-market vs poll spread ─────────────────────────────────┐
│  Per election: time series of Polymarket implied % vs poll-based %  │
│  Reveals: which one was right when, by how much, in retrospect      │
│  This is the *meta-accountability* layer                            │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ COUNTRY POLITICAL RISK                                                ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Per-country political risk score ─────────────────────────────────┐
│ Country │ Pol-risk│ V-Dem │ Polity│ Election│ Drivers              │
│         │ score   │ libdem│ score │ in 12m? │                      │
│ NGA     │ 78      │ 0.42  │ 4     │ No      │ Elections distant    │
│ ARG     │ 72      │ 0.59  │ 8     │ Yes     │ Mid-term Oct'26      │
│ TUR     │ 71      │ 0.30  │ -4    │ No      │ Democracy erosion    │
│ IND     │ 64      │ 0.42  │ 5     │ Yes     │ State elections      │
│ BRA     │ 58      │ 0.62  │ 8     │ No      │ Lula stability       │
│ MEX     │ 55      │ 0.53  │ 8     │ Yes     │ State elections      │
│ USA     │ 48      │ 0.78  │ 10    │ Yes     │ Polarization extreme │
│ FRA     │ 45      │ 0.81  │ 9     │ Yes     │ Pres 2027 ahead      │
│ GBR     │ 38      │ 0.85  │ 10    │ No      │ Govt stable          │
│ DEU     │ 35      │ 0.88  │ 10    │ Yes     │ Bundestag Sep'26     │
│ JPN     │ 28      │ 0.80  │ 10    │ Yes     │ Routine              │
│ ...                                                                  │
└─────────────────────────────────────────────────────────────────────┘
```

## Political risk scoring

The per-country political-risk score (0-100) is a weighted composite of:

- **Election proximity** (0-25 points): how close is the next major election?
- **Polling spread** (0-25 points): how narrow is the polling lead? Narrow = high risk.
- **Policy distance** (0-15 points): how far apart are the main candidates' platforms?
- **Institutional quality (V-Dem)** (0-15 points): low V-Dem libdem index → higher risk.
- **Historical base rate** (0-10 points): countries with history of post-election crises.
- **Sanctions / sovereign-credit pressure** (0-10 points): pre-existing macro stress amplifies political risk.

The composite is **vintaged** — refreshed weekly — and the components are openly shown. The page does not pretend to predict outcomes; it scores how *risky* the country's political pipeline is over the next 12 months.

## The market-implied vol decomposition

For T1 elections (national executive / legislative), OPENGEM pulls FX options for the election-week tenor and decomposes:

- **Calendar vol bump** = implied vol around the date - baseline vol (one month out either side).
- **Skew shift** = put-call skew change vs baseline.
- **Risk-reversal** = 25-delta RR signaling directional bias.

Where options data is open (CME for USDJPY, USDMXN, EURUSD; LCH for some EM), we publish daily. Where closed (most EM-pair options), we fall back to realized vol pre-election historical comparison.

## The base-rate panel — the most useful single feature

For each upcoming election, the page surfaces base-rate statistics from analogous historical elections:

- "When the incumbent president has had a 45-50% approval rating 6m pre-election, the incumbent has won 38% of comparable elections."
- "6m-post-election FX moves following an incumbent loss with policy-distance >0.7 have been -4.2% median (range -12% to +3%)."
- "Equity drawdowns 3m pre-election in high-polarization elections have been -3.1% median."

This is *the* page's accountability feature: it doesn't predict, it surfaces what *has historically happened* in similar setups, with the analog elections named and clickable.

## Data sources / adapter dependencies

| Input | Source | Adapter | Status |
|---|---|---|---|
| Election dates | IFES Election Guide + national EMBs | `opengem-data-ifes` ⚠️ NOT YET BUILT | gap |
| Polls (US) | 538 aggregator, polling firms | `opengem-data-538` ⚠️ NOT YET BUILT | gap |
| Polls (international) | Reuters Poll, national pollsters | `opengem-data-pollster-meta` ⚠️ NOT YET BUILT | gap |
| Prediction markets | Polymarket, Kalshi APIs | `opengem-data-polymarket` ⚠️ NOT YET BUILT, `opengem-data-kalshi` ⚠️ NOT YET BUILT | gap |
| FX options vols | CME, LCH (closed) — proxy via spot vol | `opengem-data-cme` ⚠️, proxy | partial |
| V-Dem democracy data | V-Dem Institute (Sweden) | `opengem-data-vdem` ⚠️ NOT YET BUILT | gap |
| Polity scores | Center for Systemic Peace | `opengem-data-polity` ⚠️ NOT YET BUILT | gap |
| Freedom House | Freedom House | `opengem-data-fh` ⚠️ NOT YET BUILT | gap |
| Policy distance | manual NLP on platforms (LLM-mediated) | `opengem-policy-distance-llm` ⚠️ NOT YET BUILT | gap |

**Identified gaps**: IFES (election calendar), V-Dem and Polity (institutional quality), Polymarket and Kalshi (prediction markets), 538 (polling). V-Dem is the *most leveraged* — it provides decades of cross-country democracy scoring as open data.

## JSON contract — per-election

```json
{
  "election_id": "usa-2028-presidential",
  "country": "USA",
  "date": "2028-11-07",
  "type": "presidential",
  "tier": "T1",
  "days_to_election": 510,
  "candidates": [
    {"name": "TBD", "party": "Democratic", "policy_vector": [...]},
    {"name": "TBD", "party": "Republican", "policy_vector": [...]}
  ],
  "polling_aggregate": {"democratic": null, "republican": null, "n_polls": 0},
  "prediction_markets": {
    "polymarket": {"democratic": 0.44, "republican": 0.52, "other": 0.04, "as_of": "2026-06-06T08:00:00Z"},
    "kalshi": {"democratic": 0.46, "republican": 0.50, "other": 0.04, "as_of": "2026-06-06T08:00:00Z"}
  },
  "market_implied_event_vol": {
    "usdjpy_1m_atm_event_week": 8.4,
    "spx_1m_atm_event_week": 24.5,
    "ust10_1m_vol_event_week_bp": 35
  },
  "policy_distance_index": 0.78,
  "historical_base_rates": {
    "n_analog_elections": 8,
    "incumbent_win_rate_pct": 60,
    "post_6m_fx_median_pct": null,
    "post_6m_equity_median_pct": null
  },
  "pol_risk_score": 76,
  "cite_this": "https://opengem.org/elections/usa-2028?v=2026-06-06"
}
```

## What this loop produced

- The four-panel layout: calendar + per-election + polling tracker + country pol-risk.
- A six-component political-risk composite score with explicit weights.
- A market-implied event-vol decomposition (calendar vol bump + skew shift + risk-reversal).
- The base-rate panel — analog historical elections with statistics.
- Eight adapter gaps named (IFES, V-Dem, Polity, Freedom House, Polymarket, Kalshi, 538, NLP).

## What comes next

- **L228** conflict tracker (post-electoral violence overlap).
- **L225** alliances + sanctions (electoral outcomes shift alliances).
- **L229** sentiment / news tone — pre-election media analysis.

## Related

- [[L001-vision-statement]]
- [[L229-sentiment-news-tone]]
- [[L225-alliances-sanctions]]
- [[L228-conflict-tracker]]
- [[L216-sovereign-risk]] — political risk feeds sovereign risk
- [[L146-iconography-system]] — `vote`, `flag`, `gauge`
