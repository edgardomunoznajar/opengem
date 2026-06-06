# L210 — Counterfactual Scenarios: Sanctions, Oil Shocks, Geopolitical Events

**Loop**: 210 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

A *counterfactual scenario* asks: "If event X occurs (or had occurred), what does the conditional outlook look like?" Examples:

- "If Iran-US escalates to kinetic and oil rises to $120, what does USA CPI look like over the next 8 quarters?"
- "If sanctions tighten on Russia and natural-gas supply to Europe halves, what is the conditional path for euro area GDP?"
- "If China's housing crisis worsens and credit growth halves, what is the conditional path for Asia?"

This loop pins the methodology, the structural-model dependency, the publication caveat, and the connection to the scenario subsystem (L196) and causal-claims taxonomy (L209).

Counterfactuals are the most epistemically loaded surface in OPENGEM. They look like causation. The loop spec is about doing them honestly.

## What counts as a counterfactual

A counterfactual scenario has three components:

1. **Antecedent specification**: an explicit, observable event or path (e.g. "oil = $120 sustained 4Q").
2. **Structural model**: an identified shock-propagation structure that maps the antecedent into changes in observable variables (e.g. an L2-BGVAR with sign-restricted oil-shock identification).
3. **Conditional density**: the predictive distribution of target variables conditional on the antecedent.

The output is a `forecast.v1` JSON tagged with `counterfactual: true` and a `conditioning_event` field explaining what antecedent is assumed.

```json
{
  "schema": "opengem.forecast.v1",
  "forecast_id": "fcst_2026-06-06_USA_CPI_4Q_counterfactual_oil-120_v1.0",
  "country": "USA",
  "indicator": {"id": "CPI-headline-yoy", "label": "CPI YoY (headline)"},
  "horizon": {"h": 4, "unit": "Q"},
  "is_counterfactual": true,
  "conditioning_event": {
    "antecedent": "oil_price_assumption",
    "antecedent_value": 120.0,
    "antecedent_unit": "USD per barrel",
    "antecedent_duration": "4Q sustained from 2026-Q3",
    "structural_model": "L2-BGVAR-v1.1",
    "identification_strategy": "sign restrictions on oil supply shock (Kilian 2009)",
    "model_card_url": "https://opengem.org/methodology/counterfactuals/oil-shock"
  },
  "baseline_forecast_id": "fcst_2026-06-06_USA_CPI_4Q_OPENGEM-L3-BMA_v3.2.1",
  "delta_from_baseline_point": 1.6,
  "point": 4.1,
  "bands": {"p10": 2.8, "p50": 4.1, "p90": 5.5},
  "narrative_note": "Conditional on the oil-price antecedent holding, the median CPI forecast rises 1.6 pp from baseline.",
  "epistemic_caveat": "The L2-BGVAR identification rests on sign-restriction assumptions reviewed in the methodology page. Alternative identification strategies could shift the conditional path. Refer to the counterfactual methodology page for the full sensitivity analysis."
}
```

The `epistemic_caveat` is mandatory on every counterfactual publication. The dashboard renders it inline.

## The structural-model dependency

Counterfactuals require identification of *which shock* propagates the antecedent. OPENGEM's L2 BGVAR (R03 / R11) provides shock identification for global spillovers; L1 (US semi-structural) provides US-specific identified shocks.

Without one of these structural layers, a "counterfactual" reduces to a *forecast under arbitrary alternative inputs*, which is technically possible but epistemically thin.

At IOC, OPENGEM's counterfactual catalogue includes:

| Counterfactual | Antecedent | Structural source | Status |
|---|---|---|---|
| Oil shock to $120 | Oil price sustained 4Q | L2-BGVAR sign restrictions | Ready |
| Oil shock to $60 (downside) | Oil price sustained 4Q | L2-BGVAR sign restrictions | Ready |
| USD reserve-status shock | DXY -15% sustained | L2-BGVAR + macro spillovers | Ready (caveat-heavy) |
| Russia-EU sanctions tighten | Natural-gas supply halved | L2-BGVAR + EA-specific | Ready |
| China housing crisis deepens | Credit growth halved | L2-BGVAR + China-specific | Ready (caveat-heavy) |
| Generic monetary policy +100 bp | Policy rate shock | L1-US-Core | US only, ready |
| Sanctions hit on Iran-related shipping | Strait of Hormuz disruption | Manual / scenario hybrid | Block II planned |
| Climate transition policy | Carbon tax $100/t | Block III planned |

Each item has its own methodology page disclosing identification, sensitivity, and historical performance.

## The IRF generation flow

For each counterfactual, the flow:

```
1. Antecedent specified (e.g. "oil to $120 sustained 4 quarters").
2. Map antecedent to identified shock: which structural shock, magnitude.
3. Apply L2-BGVAR / L1 structural model to propagate the shock.
4. Compute IRF (Impulse Response Function) per target indicator per country.
5. Generate Monte Carlo paths from posterior shock distribution.
6. Aggregate to predictive density per (country, indicator, horizon).
7. Compute delta from L3 baseline forecast.
8. Publish forecast.v1 with `is_counterfactual: true` and full conditioning_event.
```

The aggregate step uses the L207 sample-level machinery so cross-country correlation is preserved.

## Update cadence

- Counterfactual outputs are recomputed **monthly** when the baseline L3 forecast updates. The conditional shift from baseline updates as baseline drifts.
- Re-estimation of the structural model is **annual** (matching L2-BGVAR cadence per R99).
- A new counterfactual scenario can be added at any time via a PR to `opengem-scenarios` with its methodology page.

## Dashboard surfacing

Counterfactuals do not appear by default. They live in a dedicated `Counterfactuals` tab on each country/indicator page:

```
USA · CPI YoY · 4Q ahead
[Tabs:  Chart  |  Data  |  Sources  |  Methodology  |  Counterfactuals  ]
                                                       ─────────────────

COUNTERFACTUALS
─────────────────────────────────────────────────────────────────────────
Baseline forecast: 2.5%
                                                       Δ from baseline
Oil shock to $120 sustained 4Q                  4.1%   +1.6 pp
Oil shock to $60 downside                       1.6%   -0.9 pp
USD reserve-status shock (-15% DXY)             3.4%   +0.9 pp
Generic monetary policy +100 bp                 2.0%   -0.5 pp
...

Each counterfactual links to:
- Conditional density chart with baseline overlay.
- Methodology page (identification, sensitivity, model card).
- Recent historical comparator episodes.
```

Hovering any row → tooltip with antecedent, identification, caveat.

## The counterfactual is a *hypothesis*, not a forecast

The reader must understand the distinction. We enforce this via:

- The "Counterfactuals" tab is separate from the default chart.
- Every counterfactual carries `is_counterfactual: true` in its JSON.
- The narrative pipeline (L198) is forbidden from including counterfactual values in the default 3-paragraph segment. Counterfactual narrative requires a separate prompt and a separate UI surface ("Counterfactual analysis: under the oil-to-$120 antecedent, ...").
- The leaderboard (L184) *does not score* counterfactuals. They are not testable forecasts because the antecedent rarely holds exactly.

## Scoring counterfactuals

If the antecedent *does* hold (e.g. oil really does sustain $120 for 4 quarters), the counterfactual becomes a *backtest-able forecast* and is scored retroactively against actuals. The scoring is honest: PIT-KS + CRPS computed only on counterfactuals where the antecedent was realised.

A counterfactual with consistently-mis-realised conditional paths (the antecedent held, but outcomes differed materially from the conditional) earns a "structural model mismatch" badge and triggers methodology review.

## Connection to scenario subsystem

L196 scenarios fire when triggers match. Some scenarios *include* counterfactual content: a "Hard Landing" scenario pack carries a counterfactual conditional density under the hard-landing antecedent. When the trigger fires, the counterfactual is surfaced as part of the scenario page.

But: counterfactuals can also exist *without* an active firing. A reader can ask "what does an oil shock to $120 do to USA CPI?" even if no oil-shock scenario is firing today. The counterfactual layer is permanently available.

## Causality framing

Per L209, counterfactuals are *the most causal* surface OPENGEM exposes. The framing is:

> "Under model M with identification strategy I, conditional on antecedent A, the predicted density of Y is f. Alternative identification strategies, listed in the methodology page, yield alternative conditional densities."

This is the *Lucas-critique-aware* causal framing. The model M and identification I are explicit; the conditional density is not absolute truth.

## Anti-pitfalls

1. **Cherry-picked counterfactuals.** The catalogue must be *complete* in the sense that both upside and downside antecedents are published for each shock type. We do not publish only the headline "oil to $120" without also publishing "oil to $60". Symmetry of catalogue is a public-trust constraint.

2. **Antecedent ambiguity.** "Oil to $120" — for how long? Starting when? Real or nominal? *Mitigation*: antecedent specification is mandatory and structured (see schema above). No vague antecedents.

3. **Confounding readers about probability.** A counterfactual is not a forecast and does not carry a probability of the antecedent. *Mitigation*: counterfactual chart never shows a P5/P95 of the *antecedent*; only the conditional density of the target. The reader knows: we are not saying it will happen.

4. **Model uncertainty.** The structural model embodies its own uncertainty. *Mitigation*: methodology page publishes alternative-identification results side by side. Reader sees the sensitivity envelope.

## What this loop produced

- Counterfactual definition (antecedent + structural model + conditional density).
- IOC catalogue of 6 ready + 2 planned counterfactuals.
- IRF flow.
- `forecast.v1` schema extension with `is_counterfactual` + `conditioning_event` + `epistemic_caveat`.
- Dedicated "Counterfactuals" tab UX.
- Refusal of leaderboard scoring (until antecedent realisation).
- Causality framing per L209.
- Symmetry-of-catalogue discipline.

## What comes next

This is L210, the close of the L181-L210 sub-arc on forecasting mechanics. Subsequent loops (L211+) move into generic shock libraries, stress tests, recession-probability cross-country views, regime classifiers, and financial-conditions pages — all consumers of the machinery designed in this arc.

## Related

- [[L196-scenario-triggers]] — scenario subsystem that hosts counterfactuals.
- [[L197-scenario-probability-synthesis]] — distinct concept (this is conditional, not probabilistic).
- [[L207-density-aggregation]] — sample-level joint draws for cross-country counterfactuals.
- [[L208-tail-forecasts]] — marginal tails complement conditional counterfactuals.
- [[L209-causal-vs-forecast-claims]] — taxonomy governing the causal framing.
- [[R11-scenario-invocation]] — L1/L2 invocation paths.
- [[R03-hybrid-evidence]] — L2-BGVAR as structural source.
