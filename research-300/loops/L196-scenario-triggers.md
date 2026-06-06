# L196 — Scenario Triggers: Rule Grammar

**Loop**: 196 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

OPENGEM has a library of scenario packs (R11, `opengem-scenarios`: ~10 canonical packs at IOC, expanding to ~30). A scenario pack is fired by a *trigger* — a boolean rule over the live data surface. This loop pins the rule grammar, the trigger evaluation engine, and the pack-firing protocol.

The point is *non-discretionary surfacing*: when global conditions match a scenario pack's triggers, OPENGEM publishes the scenario automatically, without a human making the call. That removes the editorial-cadence vulnerability that Stratfor-style products carry (L001, "the cartel is brittle").

## The rule grammar

A trigger is a boolean expression over named data atoms. Atoms are typed and resolvable against the vintage store, the surprise index, the recession-probability endpoint, or any other Situation Subsystem signal.

### Atom types

```
DataAtom    := "data" "(" series_id ")" temporal_op value
              | "data" "(" series_id ")" temporal_op "data" "(" series_id ")"
SignalAtom  := "signal" "(" signal_name ")" [scope] comparison value
EventAtom   := "event" "(" event_type [country] [keyword] ")" temporal_op
ForecastAtom := "forecast" "(" country indicator horizon ")" temporal_op value
```

Examples of each:

```
data(BIS-CBPOL-USA) > 5.50                                 # USD policy rate above 5.5%
data(BEA-T10101-A191RL) % "MoM" < -0.5                     # MoM GDP fall > 0.5%
signal(recession_prob_12m, USA) > 0.30                     # USA 12-month recession prob > 30%
signal(surprise_index, EA) < -1.5                          # Euro-area surprise below -1.5 z
event(geopolitical_strike, country=ISR, keyword="kinetic")
forecast(USA, GDP-real-yoy, 4Q) % "delta_vintage" < -0.5   # GDP forecast revised down > 0.5pp
```

### Logical composition

```
Trigger := Atom
         | "NOT" Trigger
         | Trigger "AND" Trigger
         | Trigger "OR" Trigger
         | Trigger "WITHIN" duration       # any sub-trigger fires within window
```

Parentheses for grouping.

### Temporal operators

```
%"MoM"         # month-over-month change in the atomic series
%"QoQ"         # quarter-over-quarter change
%"YoY"         # year-over-year change
%"delta_vintage" # change between consecutive published vintages
@"persisted_N" # condition has held for N consecutive observations
```

## A worked example

The scenario pack "Hard Landing — USA":

```yaml
trigger:
  AND:
    - signal(recession_prob_12m, USA) > 0.40
    - data(FRB-H15-T10Y3M) < -0.5 @ persisted_3   # 10y-3m inverted 3 consecutive months
    - OR:
        - signal(surprise_index, USA) < -1.0 @ persisted_2  # macro surprises persistently negative
        - data(BLS-UNRATE) %"MoM" > 0.2 @ persisted_2       # UR rising 0.2pp/mo for 2 months
    - NOT signal(banking_stress, USA) > 0.70               # already-banking-stress fires a different pack
```

When this evaluates true, the scenario pack "Hard Landing — USA" fires. The pack's content (forecast revisions, narrative skeleton, prerequisite series, expected dynamics, historical analogues) becomes a live surfaced object on the dashboard with a "trigger active" badge.

## Trigger evaluation engine

A Python rule engine (the existing `opengem-event-detector` package, extended) evaluates triggers:

```python
class TriggerEngine:
    def __init__(self, vintage_store, signal_store, event_store):
        self.vintage = vintage_store
        self.signals = signal_store
        self.events = event_store

    def evaluate(self, trigger: Trigger, as_of: datetime) -> EvaluationResult:
        """Returns (fired, evidence, atom_values)."""
        ...

    def evaluate_all(self, packs: list[ScenarioPack], as_of: datetime) -> list[FiringResult]:
        """Evaluate all loaded packs; return the firing list."""
        ...
```

Evaluation cadence:

- **Daily at 06:00 UTC** — full sweep over all packs.
- **On data arrival** — re-evaluate any pack whose trigger references a series that just received a new vintage.
- **On forecast publication** — re-evaluate any pack whose trigger references a forecast atom.

Average sweep time: <1 second per pack at IOC; full sweep ~30 seconds for 30 packs.

## What "firing" means

A firing is a transition from "trigger evaluated false" to "trigger evaluated true". Firings are immutable events; once a pack fires, the firing is recorded:

```json
{
  "schema": "opengem.scenario_firing.v1",
  "firing_id": "fire_2026-06-06T14:30:00Z_hard-landing-usa",
  "pack_id": "hard-landing-usa",
  "pack_version": "1.2.0",
  "fired_at": "2026-06-06T14:30:00Z",
  "evidence": {
    "atom_values": {
      "signal(recession_prob_12m, USA)": 0.43,
      "data(FRB-H15-T10Y3M) @ persisted_3": -0.62,
      "signal(surprise_index, USA) @ persisted_2": -1.21,
      "signal(banking_stress, USA)": 0.32
    },
    "trigger_expression": "AND(signal>0.40, T10Y3M<-0.5 persist 3, OR(surprise<-1 persist 2, UR-mom>0.2 persist 2), NOT banking_stress>0.7)",
    "rule_source_url": "github.com/opengem/opengem-scenarios/blob/v1.2.0/packs/hard-landing-usa/trigger.yaml"
  },
  "scenario_probability": 0.78,    # see L197
  "pack_payload_url": "https://opengem.org/scenarios/hard-landing-usa",
  "expires_at_unless_renewed": "2026-07-06T14:30:00Z"
}
```

Firings expire if the trigger is no longer satisfied after 30 days; if still satisfied, they renew. This prevents stale firings from staying surfaced.

## Anti-spam guards

Triggers can be noisy if poorly defined. Guards:

| Guard | Mechanism |
|---|---|
| **Hysteresis** | Once a pack fires, its un-fire threshold is shifted (e.g. recession_prob must drop below 0.35, not 0.40, before "Hard Landing — USA" un-fires). |
| **Minimum persistence** | A trigger must evaluate true for at least 1 hour before publication; flickers don't trigger. |
| **Maximum firings per pack per quarter** | 1 active firing at a time; subsequent firings before un-firing extend the existing firing. |
| **Manual cooldown override** | The maintainer can mute a pack for N days if it is mis-firing; mute is logged with rationale. |

## Pack-author contract

Each scenario pack is a directory with:

```
packs/hard-landing-usa/
├── pack.yaml          # metadata, version, owner
├── trigger.yaml       # the rule grammar above
├── narrative.md       # human-readable scenario description, prerequisites, expected dynamics
├── forecasts.yaml     # forecast.v1-style payload — what the scenario implies for indicators
├── historical-analogues.md   # past episodes that match this scenario
├── methodology.md     # how the trigger was chosen
└── tests/
    ├── fixture_2008_q3.json   # known-firing test case (GFC)
    ├── fixture_2020_q1.json   # known-firing test case (COVID)
    └── fixture_2024_q1.json   # known-non-firing test case
```

Each pack ships with at least one historical-firing test and one historical-non-firing test. CI replays the pack against vintage data from those dates and asserts the trigger fires or does not, byte-identically. This is the integrity gate before a new pack ships.

## Pack registry

Packs are registered in `packs.yaml`:

```yaml
packs:
  - id: hard-landing-usa
    version: 1.2.0
    owner: edgardo
    status: active
    category: macro
    triggered_by: recession_prob + yield_curve + surprise
  - id: oil-shock-90usd
    version: 1.0.0
    owner: edgardo
    status: active
    category: commodity
  ...
```

The registry is in `opengem-scenarios` package and versioned in git.

## Surface on the dashboard

When a pack fires, the dashboard:

1. Surfaces a banner: "▲ Scenario active: Hard Landing — USA — triggered 2026-06-06 14:30 UTC."
2. Adds the pack to the "Active scenarios" panel on the home page.
3. Cross-links from the relevant country pages (USA) and indicator pages.
4. Sends an RSS feed entry, a webhook to subscribers, and (paid tier) an email alert.
5. Adds a "trigger active" badge to all USA forecasts.

The narrative pipeline (L198) consumes the firing event to produce the human-readable scenario brief.

## API contract

```
GET /v1/scenarios/active                            → list of currently-active firings
GET /v1/scenarios/{pack_id}                         → pack payload
GET /v1/scenarios/{pack_id}/firings                 → firing history
GET /v1/scenarios/{pack_id}/evaluate-as-of?at=...  → "would this pack have fired at date X?"
```

The `evaluate-as-of` endpoint is the public replay tool — anyone can verify that the pack would have fired during the 2008 GFC or 2020 COVID episode.

## What this loop produced

- Trigger grammar (atoms, operators, temporal ops).
- Worked example of a multi-atom trigger.
- Evaluation engine sketch with cadence.
- Firing record schema.
- Anti-spam guards (hysteresis, persistence, cooldown).
- Pack-author file layout with mandatory historical fixtures.
- Pack registry.
- Dashboard surfacing + API contract.

## What comes next

- **L197** — probability synthesis (how many triggers map to a "scenario probability").
- **L198** — narrative pipeline consuming firings.
- **L210** — counterfactual scenarios (the "if X then Y" hypothesis layer).

## Related

- [[opengem-scenarios]] — existing package this extends.
- [[opengem-event-detector]] — existing rule engine.
- [[L197-scenario-probability-synthesis]] — probability rollup.
- [[L198-narrative-pipeline]] — narrative consumer.
- [[L210-counterfactual-scenarios]] — counterfactual variant.
- [[R10-ssdd-008-situation]] — Situation Subsystem signals atom-resolve to.
- [[R11-scenario-invocation]] — L1/L2 invocation paths.
