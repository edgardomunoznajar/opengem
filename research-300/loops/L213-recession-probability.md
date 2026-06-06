# L213 — Recession Probability Page (Cross-Country)

**Loop**: 213 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The thesis of this loop

The single most-asked question in macro is "is X country heading into recession?" Every CB, every fund, every newsletter spends a quarter-hour a day asking it. The single most-respected answer is *Bauer-Mertens* (2018, FRBSF Economic Letter; later "term spread as the leading indicator," Fed-house extensions through 2022) — a probit on the 10y-3m term spread, augmented in modern variants with the near-term forward spread (Engstrom-Sharpe, FRB 2018) and now with macro-finance combinations (Cogley-Sargent style ensembles).

The number is famous in the US — the *NY Fed's* page showing "12-month-ahead recession probability" gets hundreds of thousands of pageviews a month. **No one publishes a cross-country, sortable, vintaged, comparable equivalent.** Bloomberg has a per-country probit, but it's not free and not embeddable. TradingEconomics has nothing serious. OECD has a "leading indicator" that's slow and bad. OPENGEM's recession-probability page is the page that — if it ships sortable, vintaged, free, with an MCP endpoint — becomes the *citable* recession probability for the entire macro internet.

This loop **decides** the page structure, the model lineup (Bauer-Mertens + three extensions), the sort/filter UX, and the per-country backtest payoff.

## The four models we run, per country

1. **BM-classic**: Bauer-Mertens probit on 10y-3m term spread. Single-variable, well-understood, easily explained, *publicly defensible*.
2. **ES-NTFS**: Engstrom-Sharpe near-term forward spread (6-quarter-ahead 3m fwd minus current 3m). Modestly outperforms BM in real-time US.
3. **MF-combo**: Macro-finance combination of term spread + ISM-style PMI + financial stress index (FSI). Pooled cross-country via Bayesian hierarchical probit.
4. **CL-neural**: Lightweight neural classifier (small MLP) over a 12-variable monthly panel — included as the *baseline* against which the structural models are scored. If neural beats structural, we report that openly.

For each model × country, we publish: (a) current 12m-ahead probability, (b) confidence band, (c) backtest hit-rate (Brier score, AUROC), (d) the last 24 months of probability history, (e) a calibration plot.

The headline number on the page is the **BMA (Bayesian Model Average)** across the four, weighted by recent CRPS — but every input model is one click away.

## Page structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ RECESSION PROBABILITY — Cross-country                                │
│ 12 months ahead. Four models, BMA combined. Vintaged, backtested.    │
└──────────────────────────────────────────────────────────────────────┘

[Filter bar — sticky]
 [Horizon: 12m ▼]   [Country group: G20 ▼]   [Model: BMA ▼]   [Sort: Highest first ▼]   [Vintage: latest ▼]

┌─ Headline cards (top 5 highest) ───────────────────────────────────┐
│ ╔════════╗ ╔════════╗ ╔════════╗ ╔════════╗ ╔════════╗               │
│ ║ TUR    ║ ║ ARG    ║ ║ DEU    ║ ║ GBR    ║ ║ JPN    ║               │
│ ║ 72%    ║ ║ 58%    ║ ║ 41%    ║ ║ 38%    ║ ║ 33%    ║               │
│ ║ ▲ +8pp ║ ║ ▲ +12pp║ ║ ▲ +5pp ║ ║ ▲ +2pp ║ ║ ─      ║               │
│ ║ since  ║ ║ since  ║ ║ since  ║ ║ since  ║ ║ since  ║               │
│ ║ 30d ago║ ║ 30d ago║ ║ 30d ago║ ║ 30d ago║ ║ 30d ago║               │
│ ╚════════╝ ╚════════╝ ╚════════╝ ╚════════╝ ╚════════╝               │
└─────────────────────────────────────────────────────────────────────┘

┌─ Main grid (sortable, filterable) ─────────────────────────────────┐
│ [Country] [P_rec %] [30d Δ] [Sparkline 24m] [Spread] [PMI] [FSI] [last update] [vintage diff] │
│ TUR       72%       +8pp    ▁▂▃▄▅▆▇█        -340bp   42.1   2.8   2026-06-04  vs WEO +18pp    │
│ ARG       58%       +12pp   ▁▁▂▃▅▆▇▇        -210bp   45.0   2.1   2026-06-04  vs WEO +22pp    │
│ DEU       41%       +5pp    ▂▃▄▅▆▆▇▇        -85bp    47.5   1.8   2026-06-04  vs WEO +8pp     │
│ ...                                                                                            │
│ (sortable on every column; click a row → modal with full country view)                         │
└────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─ World map view (toggle) ──────────────────────────────────────────┐
│ Choropleth: countries shaded by P_rec, red→green                    │
│ Click a country → flies to its row + opens detail                   │
└─────────────────────────────────────────────────────────────────────┘

┌─ Detail (modal or below grid) ─────────────────────────────────────┐
│ Country: Turkey                                                     │
│ ┌─ 24m probability history chart ─────────────────────┐             │
│ │  ───── BMA composite                                │             │
│ │  - - - BM-classic                                   │             │
│ │  ----- ES-NTFS                                      │             │
│ │  ····· MF-combo                                     │             │
│ │  ----- CL-neural                                    │             │
│ │  ▒▒▒▒ band                                          │             │
│ │  ▼▼   recession dates (NBER-style chronology)       │             │
│ └─────────────────────────────────────────────────────┘             │
│                                                                     │
│ ┌─ Calibration plot ─┐  ┌─ Variable contributions ─┐                │
│ │ obs vs predicted   │  │ Stacked bar: which       │                │
│ │ frequency, 0-100%  │  │ variable contributed     │                │
│ │ buckets            │  │ how many bp to current   │                │
│ │                    │  │ P_rec                    │                │
│ └────────────────────┘  └──────────────────────────┘                │
└─────────────────────────────────────────────────────────────────────┘
```

## Sort + filter UX — concrete

- **Sort axes**: P_rec, 30d-Δ, 90d-Δ, vs-WEO-diff, vs-consensus-diff, vs-last-recession (how high we are vs historical pre-recession peak), spread-only, model-disagreement (variance across the four).
- **Filter axes**: country group (G20, G7, EU27, ASEAN, BRICS, EM, frontier), horizon (3m, 6m, 12m, 24m), model (BMA, BM-classic, ES-NTFS, MF-combo, CL-neural), vintage (latest, 30d ago, 90d ago, 1y ago, custom).
- **Highlight bands**: "elevated" (>40%) gets a yellow lozenge, "high" (>60%) red lozenge, "imminent" (>80%) red-and-flashing lozenge with a `siren` icon. These are picky lines on purpose — calibrated to Brier scores, not vibes.
- **Hidden columns** (revealed via column-picker): predictive intervals at 10/25/75/90, individual-model probabilities, calibration AUROC, current PMI, current FSI, term-spread bp, NTFS bp.

## Vintage-time-machine integration

The vintage selector on the page lets the user say "show me what the recession probability looked like one year ago." This is *the* page where vintaging earns its keep. The user can confirm OPENGEM was calling Germany recession 8 months before Bloomberg consensus moved — *or* OPENGEM was wrong and the page shows that openly. Each vintage carries a side-link to "what happened next" so the user sees realized vs predicted.

## Backtest payoff on the page itself

Every row carries a small `gauge` icon. Click → opens a popover showing this country × this model's calibration: Brier score, AUROC, calibration plot. This is the **accountability rib** of the page. A row that's red-flashing with a Brier score of 0.34 means OPENGEM is calling recession AND the model has been right 67% of the time historically. A row that's red-flashing with a Brier of 0.49 means OPENGEM is calling but the model is barely better than a coin flip. The user gets to choose how to weight the call.

## Data sources / adapter dependencies

| Input | Source | Adapter | Status |
|---|---|---|---|
| US term spread | FRB H.15 | `opengem-data-frb` | ✅ |
| Euro-area term spreads | ECB SDW + Eurostat | `opengem-data-ecb` | ⚠️ NOT YET BUILT (named in roster, not built) |
| UK/JP/CA/AU term spreads | OECD ORDRA + national CBs | `opengem-data-ordra` | ✅ |
| EM term spreads | BIS + IMF | `opengem-data-bis`, `opengem-data-imf` | ⚠️ NOT YET BUILT (named in roster) |
| PMI (ISM-style) | ISM (US), S&P Global PMI (cross-country) | `opengem-data-spglobal-pmi` ⚠️ NOT YET BUILT | gap |
| FSI | Kansas City FSI (US), ECB CISS, custom for EMs | `opengem-data-kcfsi` ⚠️ NOT YET BUILT, `opengem-data-ecb` | partial |
| Recession chronology | NBER + OECD CLI + ECRI proprietary (not used) | `opengem-data-nber` ⚠️ NOT YET BUILT (US), OECD ORDRA (others) | partial |

**Identified gaps**: S&P Global PMI adapter, Kansas-City FSI adapter, NBER chronology adapter, ECB and BIS adapter buildout. The recession-probability page is a forcing function to commission all of these.

## JSON contract (per-country-per-vintage)

```json
{
  "country": "DEU",
  "vintage": "2026-06-06",
  "horizon_months": 12,
  "p_recession_bma": 0.41,
  "p_recession_bma_p10": 0.32,
  "p_recession_bma_p90": 0.51,
  "delta_30d_pp": +5,
  "delta_90d_pp": +9,
  "model_probabilities": {
    "bm_classic":   {"p": 0.43, "weight": 0.30},
    "es_ntfs":      {"p": 0.38, "weight": 0.25},
    "mf_combo":     {"p": 0.44, "weight": 0.30},
    "cl_neural":    {"p": 0.36, "weight": 0.15}
  },
  "inputs_now": {
    "term_spread_bp_10y_3m": -85,
    "ntfs_bp": -52,
    "pmi_manuf": 47.5,
    "pmi_services": 49.8,
    "financial_stress_index": 1.8
  },
  "calibration": {
    "brier_score_last_3y": 0.18,
    "auroc_full_sample": 0.79,
    "n_recessions_in_sample": 6
  },
  "consensus_compare": {
    "weo_oct2025_p_recession_implied": 0.33,
    "spf_aprfeb2026_p_recession": 0.36,
    "opengem_diff_vs_consensus_pp": +5
  },
  "history_24m": [0.18, 0.22, 0.25, 0.27, 0.29, 0.31, 0.33, 0.34, 0.35, 0.36, 0.36, 0.36, 0.36, 0.37, 0.38, 0.39, 0.39, 0.40, 0.41, 0.41, 0.41, 0.41, 0.41, 0.41],
  "cite_this": "https://opengem.org/recession/deu?v=2026-06-06&h=12m"
}
```

## What this loop produced

- The four-model lineup (BM-classic, ES-NTFS, MF-combo, CL-neural) and the BMA wrapper.
- The page structure with headline cards, sortable grid, world map, and per-country detail with calibration plot.
- The sort/filter axes spelled out — eight sort modes, six filter groups.
- A backtest rib on every row, not hidden in a methodology PDF.
- Five adapter gaps named (ECB, BIS, S&P Global PMI, KC FSI, NBER chronology).

## What comes next

- **L214** is the *companion* page — inflation regime classifier, same cross-country grid pattern.
- **L191** is the surprise index per indicator (general-purpose version of this page's "vs consensus diff").
- **L236** is the recession-prob tile prototype that displays on the home screen.

## Related

- [[L001-vision-statement]] — open ledger, vintaged forecasts, named methodology
- [[L166-recession-probability-tile]] — the home-screen tile that links here
- [[L211-shock-library]] — recession-prob informs which shock is "in the air"
- [[L191-surprise-index]] — the vs-consensus column
- [[L236-recession-prob-tile-prototype]]
- [[L146-iconography-system]] — `siren`, `gauge`, `flag`
