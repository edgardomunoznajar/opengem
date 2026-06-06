# L214 — Inflation Regime Classifier Page

**Loop**: 214 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The thesis of this loop

"Regime" is the macroeconomist's word for "the rules just changed." 2021 was not a normal demand-led CPI rise — it was a regime shift from "anchored near 2%" to "supply-shock-plus-overheating." 2024 was a regime shift back. Macro investors trade *regimes*, not point inflation. Yet no public dashboard publishes a clean per-country regime label with persistence statistics. Bloomberg has nothing like this. The Cleveland Fed has a one-country inflation nowcast. The IMF WEO has no concept of regime at all.

OPENGEM's inflation regime page does what every macro shop does internally — runs a Markov-switching / HMM-style classifier on country-level CPI dynamics, labels each month with a regime, computes persistence, and publishes the result. The payoff for the user is **massive**: with one click they see "Brazil entered Sticky-High in 2022Q3, has been there 11 quarters, prior episodes lasted on average 7 quarters with a 65% chance of moving to Disinflationary next." That is decision-grade information.

This loop **decides** the regime taxonomy, the model, the page structure (label timeline + transition matrix + persistence stats), and the cross-country sorting UX.

## The five regimes (canonical taxonomy)

The taxonomy must be small enough to be readable in a sparkline grid, large enough to be useful. We **decide** five labels:

| Regime | Definition | Heuristic |
|---|---|---|
| **Disinflationary** | YoY CPI falling AND below target | 3m trend < 0, level < target |
| **Anchored** | YoY CPI within ±0.5pp of target, low vol | rolling std < threshold, level near target |
| **Demand-led overheating** | YoY CPI > target, demand indicators hot | level > target, output gap > 0, services CPI hot |
| **Supply-shock-driven** | YoY CPI > target, supply indicators hot | level > target, energy/food CPI dominant, output gap ≈ 0 |
| **Sticky-high (entrenched)** | YoY CPI persistently > target, trimmed-mean CPI > target, expectations un-anchored | level > target for ≥6m, expectations break |

Labels are *not mutually exclusive with confidence* — the model emits a probability distribution over regimes, and the headline label is `argmax`. The probability vector is one click away.

## The model

A Bayesian Markov-switching model on a per-country basis, with five hidden states (the five regimes) and observed variables: (1) headline CPI YoY, (2) trimmed-mean CPI YoY, (3) services-ex-energy CPI YoY, (4) goods-ex-energy CPI YoY, (5) 5y5y inflation swap (where available), (6) inflation surprise vs consensus, (7) output gap proxy.

The model is **trained pooled across countries** with a hierarchical prior — countries share parameters but allow country-specific deviation — to handle EM countries with short data histories. For each country and each month, we publish: the regime label, the probability vector, the smoothed posterior, and the implied transition probabilities to other regimes.

## Page structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ INFLATION REGIME CLASSIFIER                                          │
│ Per-country, per-month. Five regimes, Markov-switching, vintaged.    │
└──────────────────────────────────────────────────────────────────────┘

[Selector strip]
 [Country group: G20 ▼]   [Sort: by current regime ▼]   [Vintage: latest ▼]   [View: timeline / matrix / persistence ▼]

┌─ Current regime grid ──────────────────────────────────────────────┐
│ Each cell = one country.                                            │
│ Color encoding:                                                     │
│   GREEN  = Disinflationary                                          │
│   BLUE   = Anchored                                                 │
│   ORANGE = Demand overheating                                       │
│   RED    = Supply shock                                             │
│   PURPLE = Sticky-high                                              │
│ Each cell shows: country code, regime label, P(regime), months in   │
│ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐         │
│ │ USA  ANCH  │ │ EA   DISI  │ │ JPN  ANCH  │ │ GBR  STKY  │         │
│ │ P=0.78  9m │ │ P=0.65 5m  │ │ P=0.71 24m │ │ P=0.62 18m │         │
│ └────────────┘ └────────────┘ └────────────┘ └────────────┘         │
│ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐         │
│ │ TUR  STKY  │ │ ARG  STKY  │ │ BRA  ANCH  │ │ MEX  DEMD  │         │
│ │ P=0.91 34m │ │ P=0.86 60m │ │ P=0.55 4m  │ │ P=0.61 7m  │         │
│ └────────────┘ └────────────┘ └────────────┘ └────────────┘         │
│ ... 30+ more, sortable, filterable                                  │
└─────────────────────────────────────────────────────────────────────┘

┌─ Country detail (selected: GBR) ───────────────────────────────────┐
│ ┌─ Regime timeline (10y) ─────────────────────────────────────────┐│
│ │  Each month = one colored vertical stripe                       ││
│ │  2016: ANCH ANCH ANCH ... 2020: DISI ... 2021: SUP SUP SUP ...  ││
│ │  2022: DEMD ... 2023: STKY STKY STKY STKY STKY ...              ││
│ │  Current: STKY (18 months in)                                   ││
│ │  Annotations: BoE rate hikes, Brexit, COVID, Truss budget       ││
│ └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
│ ┌─ Probability stacked-area chart ────────────────────────────────┐│
│ │  Y: 0-100%, X: time                                              ││
│ │  Stacked area showing the *posterior probability* of each       ││
│ │  regime over time. Reveals "uncertain transitions."             ││
│ └─────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘

┌─ Transition matrix view ───────────────────────────────────────────┐
│                                                                     │
│                  TO regime →                                        │
│                ┌──────┬──────┬──────┬──────┬──────┐                 │
│                │ DISI │ ANCH │ DEMD │ SUPP │ STKY │                 │
│  ┌─────────┬───┼──────┼──────┼──────┼──────┼──────┤                 │
│  │ DISI    │   │ 0.78 │ 0.18 │ 0.02 │ 0.01 │ 0.01 │                 │
│  │ ANCH    │   │ 0.05 │ 0.85 │ 0.05 │ 0.04 │ 0.01 │                 │
│  │ DEMD    │   │ 0.03 │ 0.20 │ 0.55 │ 0.10 │ 0.12 │                 │
│  │ SUPP    │   │ 0.04 │ 0.05 │ 0.10 │ 0.65 │ 0.16 │                 │
│  │ STKY    │   │ 0.02 │ 0.03 │ 0.05 │ 0.05 │ 0.85 │                 │
│  └─────────┴───┴──────┴──────┴──────┴──────┴──────┘                 │
│                                                                     │
│  Implied half-life in STKY: ~4.6 months (1/(1-0.85) months).        │
│  Per-country override: filter to single country shows that country's│
│  transition probabilities, not the pooled average.                  │
└─────────────────────────────────────────────────────────────────────┘

┌─ Persistence stats panel ──────────────────────────────────────────┐
│ Per country: avg duration of each regime, last 25 years.            │
│ Sortable. Quickly identify "sticky-prone" vs "fast-flipping" econs. │
└─────────────────────────────────────────────────────────────────────┘
```

## Cross-country sorting UX

Five sort modes:

1. **By current regime**: group countries by their current label. Bloomberg-mosaic feel.
2. **By P(regime)**: rank by confidence. Tells the user where the model is *certain* vs where it's hedging.
3. **By time in regime**: tells the user where the regime is freshly minted vs entrenched.
4. **By implied half-life to exit**: tells the user where the regime is about to flip.
5. **By divergence from prior 5y mean**: tells the user where things are most "off."

Sort mode is shareable via URL parameter.

## The accountability hook

The page carries a "Regime call accuracy" panel — for each country, retrospectively, how often the OPENGEM regime label *agreed with* a panel of CB-economist-derived regime labels (we curate a hand-labeled set for the OECD-major countries, 2000-2024). This is the Brier-equivalent for regime labels. **A regime model that has been right 85% of the time on US since 2000 is a model worth paying attention to.** A model that's been right 60% gets shown alongside its confidence interval and a humble disclaimer.

## Data sources / adapter dependencies

| Input | Source | Adapter | Status |
|---|---|---|---|
| US CPI | BLS | `opengem-data-bls` | ✅ |
| Euro-area HICP | Eurostat + ECB | `opengem-data-ecb` (extend), `opengem-data-eurostat` ⚠️ NOT YET BUILT | partial |
| UK CPI | ONS | `opengem-data-ons` ⚠️ NOT YET BUILT | gap |
| Japan CPI | MIC | `opengem-data-mic-jp` ⚠️ NOT YET BUILT | gap |
| EM CPI | IMF + national stats | `opengem-data-imf` | partial |
| Inflation swaps 5y5y | ICAP / Tullett (closed) — proxy: Bloomberg or open via national breakeven | `opengem-data-frb` (US TIPS BEI) ✅, others ⚠️ NOT YET BUILT | mostly gap |
| Trimmed-mean / sticky CPI | Cleveland Fed (US), CB equivalents elsewhere | `opengem-data-clev-fed` ⚠️ NOT YET BUILT | gap |
| Inflation expectations surveys | UMich + NY Fed (US), ECB SPF (EA), BoJ Tankan (JP) | `opengem-data-umich` ⚠️ NOT YET BUILT, etc. | gap |

**Identified gaps**: Eurostat, ONS, MIC-JP, Cleveland Fed, UMich adapters. Inflation expectations data is a structural gap — most are open-data but not yet adapted.

## JSON contract

```json
{
  "country": "GBR",
  "vintage": "2026-06-06",
  "current_month": "2026-04",
  "regime_label": "sticky_high",
  "regime_probability": 0.62,
  "regime_probability_vector": {
    "disinflationary": 0.05,
    "anchored": 0.18,
    "demand_overheating": 0.10,
    "supply_shock": 0.05,
    "sticky_high": 0.62
  },
  "months_in_current_regime": 18,
  "regime_history_120m": [
    {"month": "2016-05", "label": "anchored", "p": 0.81},
    ...
  ],
  "implied_transition_probs_next_12m": {
    "to_disinflationary": 0.08,
    "to_anchored": 0.22,
    "to_demand_overheating": 0.06,
    "to_supply_shock": 0.04,
    "to_sticky_high": 0.60
  },
  "persistence_stats": {
    "avg_duration_months_sticky_high": 14.3,
    "avg_duration_months_anchored": 42.1,
    "this_regime_vs_history_pp": +4
  },
  "accuracy_vs_curated_labels_last_5y": 0.82,
  "cite_this": "https://opengem.org/inflation-regime/gbr?v=2026-06-06"
}
```

## What this loop produced

- The five-regime taxonomy (disinflationary, anchored, demand overheating, supply shock, sticky-high).
- A pooled Bayesian Markov-switching model with hierarchical priors.
- The page structure: grid + timeline + probability stacked area + transition matrix + persistence stats.
- Five cross-country sort modes.
- A retrospective "regime call accuracy" rib.
- Six adapter gaps named.

## What comes next

- **L215** is the financial conditions index page — adjacent because FCI conditions show up as a regime input.
- **L167** is the inflation nowcast tile (companion home-screen tile).
- **L213** is the recession-prob page (same cross-country grid pattern).

## Related

- [[L001-vision-statement]]
- [[L213-recession-probability]] — same grid pattern, different signal
- [[L215-financial-conditions]] — adjacent: FCI feeds inflation regime
- [[L167-inflation-nowcast-tile]]
- [[L146-iconography-system]] — `flame`, `gauge`, `info`
