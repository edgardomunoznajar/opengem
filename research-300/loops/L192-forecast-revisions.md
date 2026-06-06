# L192 — Forecast Revisions: Per-Vintage Diff

**Loop**: 192 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

A forecast for "USA Real GDP YoY at 2027-Q1" is republished many times as the world updates. The vintage from January 2026 was 2.5%; the vintage from April 2026 was 2.3%; the vintage from June 2026 was 2.18%. **These revisions are themselves a publishable artefact.** This loop pins the per-vintage diff schema and designs the "revision arrow" overlay that surfaces it on the chart.

The accountability discipline is symmetric: we publish the latest forecast, and we publish every *revision* to it. Forecasters who silently drift their numbers month over month get caught.

## The revision record

For every successive vintage of the same `(country, indicator, horizon, scoring_period)`, we emit a revision record:

```json
{
  "schema": "opengem.forecast_revision.v1",
  "revision_id": "rev_2026-06-06_USA_GDP_target-2027Q1",
  "country": "USA",
  "indicator": "GDP-real-yoy",
  "scoring_period": "2027-Q1",
  "previous_forecast_id": "fcst_2026-04-15_USA_GDP_4Q_OPENGEM-L3-BMA_v3.2.0",
  "current_forecast_id": "fcst_2026-06-06_USA_GDP_4Q_OPENGEM-L3-BMA_v3.2.1",
  "previous_point": 2.30,
  "current_point": 2.18,
  "delta_point": -0.12,
  "previous_p10": 1.15,
  "current_p10": 1.04,
  "previous_p90": 3.40,
  "current_p90": 3.28,
  "delta_p90_minus_p10": -0.13,
  "previous_released_at": "2026-04-15T00:00:00Z",
  "current_released_at": "2026-06-06T08:00:00Z",
  "days_between_vintages": 52,
  "revision_decomposition": {
    "data_input_contribution": -0.08,
    "model_code_contribution": -0.02,
    "weights_update_contribution": -0.01,
    "config_change_contribution": 0.00,
    "residual": -0.01
  },
  "drivers": [
    {"series": "BEA-T10101-A191RL", "vintage_at_prev": "2026-03-30T16:30:00Z", "vintage_at_curr": "2026-05-29T16:30:00Z", "revision_to_input": -0.4},
    {"series": "FRB-H15-DGS10", "vintage_at_prev": "2026-04-14T07:15:00Z", "vintage_at_curr": "2026-06-06T07:15:00Z", "revision_to_input": 0.3}
  ],
  "narrative": "Forecast revised down 12 bp on weaker 2026-Q1 GDP advance estimate (-0.4 pp lower than previous data vintage); partially offset by higher long-yield path lifting financial conditions inputs."
}
```

The schema requires the **revision decomposition** — what fraction of the change was due to (a) new input data, (b) new model code, (c) updated BMA weights, (d) config change, (e) residual / numerical noise.

## Computing the decomposition

For each `(prev_forecast_id, curr_forecast_id)` pair, run the L3 pipeline four times:

1. With previous data, previous code, previous weights, previous config → produces prev_point (verify equals previous_point).
2. With **current data**, previous code, previous weights, previous config → produces point_d.
3. With current data, **current code**, previous weights, previous config → produces point_dc.
4. With current data, current code, **current weights**, previous config → produces point_dcw.
5. With current data, current code, current weights, **current config** → produces point_dcwf (verify equals current_point).

Then:

```
data_input_contribution     = point_d   - prev_point
model_code_contribution     = point_dc  - point_d
weights_update_contribution = point_dcw - point_dc
config_change_contribution  = point_dcwf - point_dcw
residual                    = current_point - point_dcwf
```

Residual should be near zero (rounding only). If residual exceeds 0.01% in absolute value, we flag the decomposition as suspicious and surface a "decomposition uncertain" badge.

This *Shapley-style* attribution is one of several possible orderings; we pin to this ordering (data → code → weights → config) and disclose the ordering in the methodology page. Alternative orderings produce different attributions but the same total.

## The "revision arrow" chart overlay

The forecast chart shows the *current* forecast as the headline. The revision arrow shows where the forecast was the prior vintage and where it is now:

```
                                                     CURRENT  (P50 = 2.18)
                                                     ●═══════════
                                                                  
   PREVIOUS  (P50 = 2.30, dotted line and lighter colour)         
   ●═════════════                                                 
                                                                  
   ──────────────●───►───●───►───●───●─────────────────────────────────►
                 1Q     2Q     3Q     4Q  (4Q horizon target = 2027-Q1)
                                                                  
                 ↑  arrow from previous to current, with magnitude:
                    -0.12 pp (data: -0.08, code: -0.02, weights: -0.01, residual: -0.01)
```

The arrow renders only when the user is on the "vs. prior vintage" view (toggle). Defaults to off on first load to keep the chart clean. The toggle is sticky in user settings.

## Revision arrows on multiple prior vintages

For the "vs. history" view, the chart can show all prior vintages of a target, each as a faded P50 line:

```
   2026-01 vintage ────●──── 2.55
   2026-02 vintage ────●──── 2.50  (drift down begins)
   2026-03 vintage ────●──── 2.40
   2026-04 vintage ────●──── 2.30
   2026-05 vintage ────●──── 2.22
   2026-06 vintage ────●──── 2.18  ← current

   target 2027-Q1
```

This is *the revision trajectory*. It surfaces gradual drift that would be invisible if only the latest forecast were shown. A common pattern is "consensus drifts toward the realised value as the date approaches" — OPENGEM publishes its own drift transparently.

## Revision detection rules

A revision record is created automatically when any of these triggers fire for the same `(country, indicator, horizon, scoring_period)`:

| Trigger | Frequency |
|---|---|
| New scheduled re-forecast at cadence | Cadence-driven (L187) |
| Input data revision lands (e.g. BEA Q1 GDP revised second estimate) | Event-driven |
| Code release (new `git_tag`) | Release-driven |
| Weights epoch boundary | Quarterly + ad hoc |
| Manual re-run (incident response) | Rare; flagged |

Every revision goes through the same L186 envelope and the same lineage record (L182). Revisions are not "edits in place" — they are new immutable forecasts with a back-pointer.

## Revision history API

```
GET /v1/forecasts/history?country=USA&indicator=GDP-real-yoy&scoring_period=2027-Q1
→ {
    "schema": "opengem.forecast_history.v1",
    "target": {"country": "USA", "indicator": "GDP-real-yoy", "scoring_period": "2027-Q1"},
    "n_vintages": 6,
    "vintages": [
      {"forecast_id": "...", "released_at": "2026-01-15", "point": 2.55, "p10": 1.40, "p90": 3.70},
      {"forecast_id": "...", "released_at": "2026-02-15", "point": 2.50, ...},
      ...
      {"forecast_id": "...", "released_at": "2026-06-06", "point": 2.18, ...}
    ],
    "revisions": [
      {"from": "2026-01-15", "to": "2026-02-15", "delta_point": -0.05, "drivers": [...]},
      ...
    ]
  }
```

This is the public revision ledger. Anyone can read it; LLMs ground their "what did OPENGEM say about USA GDP for 2027?" answers in this exact response.

## The "miss-anticipating" view

A particularly useful chart shows revisions plotted against realised outcomes. Once the scoring period passes, the realised value joins the chart as a horizontal line, and the user sees whether OPENGEM converged toward the truth:

```
                          realised 2.85 ───────────────────
   2.55 ●                                                   
   2.50 ●                                                   
   2.40 ●  drift                                            
   2.30 ●  toward                                           
   2.18 ●  truth                                            
        2026-01     2026-06     2027-Q1
                                  scoring period
```

This pattern — drift in the right direction — earns an "early-anticipator" badge. A pattern of drift *away* from truth earns a "drift-toward-error" warning surfaced on the model card.

## What this loop produced

- `forecast_revision.v1` schema with Shapley-style attribution.
- Decomposition procedure (4-step rebuild).
- Chart revision arrow rendering (single-prior view).
- Multi-vintage trajectory view.
- Revision triggers + cadence rules.
- Revision history API.
- Miss-anticipation view + badge.

## What comes next

- **L195** — full chart UI integrates the revision arrow.
- **L200** — failure log incorporates persistent revision-away-from-truth patterns.

## Related

- [[L181-forecast-object-schema]] — forecast.v1 each revision instantiates.
- [[L182-forecast-vintage-lineage]] — lineage of each revision.
- [[L186-reproducibility-envelope]] — envelope per revision.
- [[L195-forecast-ui-spec]] — chart spec.
- [[L200-failure-log]] — drift-toward-error captures.
