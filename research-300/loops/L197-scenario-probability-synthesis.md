# L197 — Scenario Probability Synthesis

**Loop**: 197 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

A scenario *trigger* (L196) is binary: fired / not fired. A *scenario probability* is a number in [0, 1] saying "how likely is this scenario over the next 12 months?". Triggers and probabilities are related but not identical. This loop pins how triggers roll up into probabilities, how multiple competing scenarios share probability mass, and what is published.

A "Hard Landing — USA" pack with trigger fired today does not mean P(hard landing) = 1; it means the conditions consistent with hard landing are present *now*, which historically have preceded hard landings X% of the time. That X is the scenario probability.

## Three sources of scenario probability

A scenario pack can have its probability assigned by any of three methods:

### Method 1 — Empirical base rate

Count historical episodes that matched the trigger conditions. Compute the fraction that became "hard landings" within 12 months. That fraction is the probability.

```
P(scenario | trigger fired) ≈ (# historical episodes meeting trigger that resolved as scenario) / (# historical episodes meeting trigger)
```

Strength: data-driven, defensible.
Weakness: historical sample is small for rare scenarios; relies on labelled history.

### Method 2 — Direct model prediction

Some scenarios have a *model* that directly predicts their probability. The Bauer-Mertens recession-probability model (R10, `opengem-recession-prob`) directly outputs P(US recession in next 12 months). For scenarios anchored on that endpoint, the probability is the model's output.

```
P(scenario) = bauer_mertens_recession_prob(t)
```

Strength: model-grounded, can be calibrated.
Weakness: only available for scenarios that have a dedicated probabilistic model.

### Method 3 — Expert / specialist prior

For scenarios that lack a model and have insufficient historical data (e.g. "China-Taiwan kinetic escalation"), the pack carries a hand-coded prior that is updated based on observable signals. The prior is a function:

```
P(scenario) = base_rate × adjustments_from_observable_signals
```

with adjustments e.g. "if ACLED conflict-events from China to Taiwan > X then prior multiplies by Y".

Strength: applicable to novel scenarios.
Weakness: subjective; must be explicitly documented as such.

## The chosen synthesis rule

For each pack, the pack metadata declares which method applies:

```yaml
# packs/hard-landing-usa/pack.yaml
id: hard-landing-usa
probability_method: empirical_base_rate
probability_window_years: 60      # use 1965-2025 history
probability_floor: 0.05            # never reported below 5%
probability_ceiling: 0.95          # never reported above 95% — uncertainty must remain
```

```yaml
# packs/oil-shock-90usd/pack.yaml
id: oil-shock-90usd
probability_method: model
model_endpoint: signal(oil_shock_prob, world)
```

```yaml
# packs/china-taiwan-kinetic/pack.yaml
id: china-taiwan-kinetic
probability_method: expert_prior
base_rate: 0.05
adjustments:
  - condition: signal(acled_china_taiwan_strait_events, period=90d) > 20
    multiplier: 2.0
  - condition: data(VIX) > 30 @ persisted_5
    multiplier: 1.3
```

The pack always carries the *current* probability after evaluation, with full method-specific provenance.

## Probability normalisation across scenarios

Multiple scenarios can fire simultaneously. They are not mutually exclusive — a "hard landing" and an "oil shock" can both be active. We do not force probabilities to sum to 1.

But we do publish *exhaustive* scenario probabilities for some indicator families. For the recession outcome specifically, a partition is enforced:

| Scenario | Probability | Compatible with others? |
|---|---|---|
| Hard landing (recession + persistent inflation) | 0.18 | No (mutually exclusive with the next three) |
| Soft landing (no recession, inflation to target) | 0.42 | No |
| No landing (no recession, sticky inflation) | 0.22 | No |
| Stagflation (recession + persistent high inflation) | 0.18 | No |
| (sum = 1.00) | | |

The four landing scenarios are a partition. Their probabilities are estimated jointly (via a multinomial model). The dashboard's "USA economic regime" pie chart shows this partition.

Other scenarios (oil shock, geopolitical event, sovereign default in country X) are *event probabilities* — not exclusive, not summing.

## The synthesis schema

The published probability for any active scenario looks like:

```json
{
  "schema": "opengem.scenario_probability.v1",
  "pack_id": "hard-landing-usa",
  "evaluated_at": "2026-06-06T14:30:00Z",
  "probability": 0.42,
  "probability_band_p10_p90": [0.28, 0.56],
  "method": "empirical_base_rate",
  "evidence": {
    "historical_episodes": 9,
    "of_those_resolved_as_scenario": 4,
    "raw_base_rate": 0.44,
    "applied_adjustments": [
      {"source": "credit_spread_adjustment", "multiplier": 0.95, "rationale": "spreads not yet widening"},
      {"source": "labour_market_strength", "multiplier": 1.0, "rationale": "no signal currently"}
    ],
    "n_episodes_with_uncertainty_band": "wilson_score_ci"
  },
  "trigger_status": "active",
  "trigger_active_since": "2026-06-06T14:30:00Z",
  "partition_member": "USA_landing_partition_v1.0",
  "partition_normalised": false
}
```

For partitioned scenarios:

```json
{
  "schema": "opengem.scenario_partition.v1",
  "partition_id": "USA_landing_partition_v1.0",
  "evaluated_at": "2026-06-06T14:30:00Z",
  "scenarios": [
    {"pack_id": "hard-landing-usa", "probability": 0.18},
    {"pack_id": "soft-landing-usa", "probability": 0.42},
    {"pack_id": "no-landing-usa", "probability": 0.22},
    {"pack_id": "stagflation-usa", "probability": 0.18}
  ],
  "sum_check": 1.00,
  "method": "joint_multinomial_logit",
  "model_card_url": "https://opengem.org/methodology/landing-partition"
}
```

## Calibration: are these probabilities honest?

Scenario probabilities are themselves forecasts and must be calibrated. We score them retrospectively:

- For each historical firing, did the scenario materialise within the 12-month horizon?
- Aggregate Brier score per pack.
- Reliability diagram per pack (L193 binary case).

A pack with consistently overconfident probabilities is flagged and the pack's `probability_method` is reviewed (typically by tightening adjustments).

## The "scenario probability heatmap"

A dashboard panel shows a heatmap of all currently-active scenario probabilities across countries:

```
              Hard land  Soft land  No land  Stag   Oil shock  Geo event
USA           ■■ 18%     ■■■ 42%    ■■ 22%   ■ 18%  ■ 8%       — n/a
EA            ■■ 22%     ■■■ 38%    ■■ 24%   ■ 16%  ■ 8%       — n/a
GBR           ■■ 28%     ■■ 35%     ■■ 21%   ■ 16%  ■ 8%       — n/a
JPN           ■ 12%      ■■■■ 52%   ■■ 24%   ■ 12%  ■ 8%       — n/a
CHN           ■■ 24%     ■■ 32%     ■■ 28%   ■ 16%  ■ 8%       ■ 12% (Tw)
```

Sortable, filterable, with click-through to each pack's detail page.

## Pitfalls

1. **Historical base rates can be misleading** for regime shifts. The pack's methodology page must disclose the historical window and whether structural change in the economy makes the base rate stale.
2. **Adjustments are tunable.** The expert-prior method risks reverse-engineering toward a desired number. *Defence*: every adjustment is in version-controlled YAML; every change is in git history; the model card lists who changed what and when.
3. **Probability inflation under simultaneous firings.** Two correlated scenarios both at 50% does not mean joint 75% — it might mean joint 50% if they are perfectly correlated.
   *Mitigation*: when scenarios are part of a declared partition, joint probability is enforced. Otherwise, the dashboard footnotes: "Scenarios may overlap; probabilities are marginal, not joint."

## Update cadence

- Empirical base rate: recomputed monthly (when a new candidate historical episode resolves, e.g. NBER recession dating update).
- Model: recomputed at the model's natural cadence (Bauer-Mertens: monthly).
- Expert prior: recomputed daily (signal-driven).

## API endpoints

```
GET /v1/scenarios/{pack_id}/probability                  → current probability
GET /v1/scenarios/{pack_id}/probability/history          → time series of probability
GET /v1/scenarios/partitions/{partition_id}              → all members of a partition
GET /v1/scenarios/heatmap                                 → cross-country probability matrix
```

## What this loop produced

- Three probability-assignment methods.
- Per-pack method declaration in YAML.
- Synthesis schema for both standalone scenarios and partitions.
- Calibration discipline (Brier + reliability for probabilities themselves).
- Heatmap UX.
- Update cadence per method.
- API endpoints.

## What comes next

- **L198** — narrative pipeline consumes both triggers and probabilities.
- **L210** — counterfactual scenarios use a related but different scoring approach.

## Related

- [[L196-scenario-triggers]] — the binary fire signal this rolls up.
- [[L198-narrative-pipeline]] — narrative consumer.
- [[L199-trust-signals]] — calibration-of-probabilities badge.
- [[L210-counterfactual-scenarios]] — counterfactual cousin.
- [[opengem-recession-prob]] — Bauer-Mertens endpoint used by Method 2.
- [[R10-ssdd-008-situation]] — Situation Subsystem.
