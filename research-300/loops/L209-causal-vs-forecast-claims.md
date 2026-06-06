# L209 — Causal vs Forecast Claims: Taxonomy

**Loop**: 209 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

A *forecast claim* says: "given today's information, the predicted value of Y at time T is X." A *causal claim* says: "Z caused Y" or "if Z had been different, Y would have been Y'." These are different claims, supported by different evidence, and confused at OPENGEM's peril.

The dashboard, the API, the MCP tool, the narrative pipeline, and the failure-log post-mortems must all enforce the taxonomy. This loop pins which claims live where, what counts as evidence for each, and the explicit refusal scope where OPENGEM will not make a causal claim.

## The taxonomy

| Claim type | Statement form | Evidence required | OPENGEM's posture |
|---|---|---|---|
| **Pure forecast** | "OPENGEM forecasts Y at T to be X (P10-P90: A to B)." | Model + V&V matrix evidence; calibration | Always permitted; default content |
| **Comparative forecast** | "OPENGEM's forecast is below WEO's forecast at T." | Consensus data; horizon match | Always permitted |
| **Conditional forecast** | "If Z evolves as scenario S describes, then conditional on S, P50 of Y at T is X'." | Scenario pack with explicit conditioning | Permitted under scenario subsystem (L196) |
| **Counterfactual** | "If Z had been Z' historically, Y would have been Y'." | Identified shock + structural model | Permitted only under L210 with explicit caveats |
| **Causal forward statement** | "Z causes Y" or "Higher Z will cause higher Y." | Identification strategy + structural evidence | **Refused** at IOC. Reserved for narrative under explicit pop-up acknowledgement. |
| **Attribution** | "The 2026-Q1 GDP miss was caused by Z." | Time-series decomposition + literature | Permitted with caveats in failure-log post-mortems only (L200) |
| **Policy prescription** | "X should do Y." | Welfare analysis + values judgment | **Refused.** Out of mission scope. |

## The rule

> **OPENGEM publishes forecast and comparative claims as primary content. It publishes conditional, counterfactual, and attribution claims only inside scenario packs (L196/L210) or failure-log post-mortems (L200), with explicit caveats. It refuses causal forward statements and policy prescriptions across all surfaces.**

This is encoded as a `claim_type` enum in the schema, surfaced in the narrative-pipeline prompt (L198), and enforced by the publication validator.

## Why refuse causal forward statements

Three reasons:

1. **The evidence is harder.** Identifying a forward causal claim requires either a randomised experiment (impossible at macro scale) or a strong structural identification strategy (Cholesky / sign-restriction / external instruments). The structural models in OPENGEM's L1 / L2 layers do this *for scenarios* but the inference is conditional, not unconditional.

2. **The downside is catastrophic.** A wrong causal claim — "higher rates cause recessions" — is read as policy guidance and influences real decisions. A wrong forecast — "we predict recession" — is just a forecast we then log as a miss.

3. **The competitive surface is already strong without causality.** OPENGEM's value is in calibrated forecasts and open evidence. Adding shaky causal claims would dilute that.

## Why conditional and counterfactual claims are permitted

The scenario subsystem (L196, L197, L210) is *explicit* about its conditioning. A scenario pack says "*if* the trigger conditions hold *then* the conditional forecast is X." The reader sees the antecedent; the claim is conditional, not unconditional. This is the cleanest way to publish "what would happen if" claims without slipping into causation.

The counterfactual layer (L210) goes further: it uses structural models to ask "what would have happened if Z had been Z'." This *is* a causal claim, but framed as a hypothesis under a specific structural model, with the model card disclosing the identification strategy. It is published under "Scenario / Counterfactual" badges, not next to the main forecast.

## Surface-by-surface enforcement

| Surface | Permitted claim types | Refused |
|---|---|---|
| Forecast chart (L195) | Pure forecast, comparative | Causal forward, prescriptive |
| Coverage page (L194) | Pure forecast (metadata) | All others |
| Calibration plot (L193) | Pure (about the model itself) | All others |
| Surprise index (L191) | Pure forecast error | Causal forward |
| Leaderboard (L184) | Comparative | Causal forward |
| Scenario page (L196) | Conditional, counterfactual (L210) | Causal forward (unconditional) |
| Failure log post-mortem (L200) | Attribution with caveats, counterfactual | Forward causal forecasts |
| Narrative pipeline (L198) | Pure forecast + comparative; scenario summary | Causal forward, prescriptive |

## The narrative refusal in the prompt

The system prompt (L198) explicitly says:

> Every claim about causality must be marked uncertain ("likely", "consistent with", "suggests") unless the JSON's `causal_basis` field permits otherwise (currently always false).

This is the hard floor. The narrative cannot claim "rate hikes caused the slowdown"; it can claim "the forecast is consistent with the empirical pattern observed in past tightening cycles." Same content, different epistemic posture.

The validator (L198) regexes for banned causal phrases: "caused", "results in", "leads to", "drives", "X explains Y" (in the active voice with X subject). When found, regeneration fires.

## The `causal_basis` field

Some forecasts *do* have a causal-claim authorisation, via an identified structural model. The forecast.v1 schema carries an optional `causal_basis` block:

```json
{
  "causal_basis": {
    "permitted": true,
    "structural_model": "L1-US-Core-v1.0",
    "identification_strategy": "Cholesky ordering",
    "identified_shocks": ["monetary_policy", "demand", "supply"],
    "model_card_url": "https://opengem.org/methodology/l1-us-core/identification"
  }
}
```

This is *only* populated by L1 structural-model outputs (rare; US-only at IOC). When present, the narrative pipeline is permitted to make conditional causal statements *about the identified shocks* — e.g., "the model attributes 35% of the 4Q forecast revision to a tightening-of-monetary-policy shock."

Without `causal_basis: permitted=true`, every causal claim is refused.

## Attribution claims in post-mortems

Failure-log post-mortems (L200) are permitted to use attribution language:

> "The Q1-2024 GDP miss was primarily due to underweighted labour-market acceleration..."

This is attribution to a *model failure mode*, not to an economic mechanism. The distinction matters: we are explaining why our forecast was wrong, which requires identifying which inputs or weights misled us; we are not claiming a structural mechanism in the real economy.

Even in post-mortems, real-economy causal claims must be hedged: "consistent with", "suggests", "the literature attributes such episodes to...". Plain causal statements are refused.

## Hard refusal: policy prescription

OPENGEM does not say "the Fed should cut", "Germany should expand fiscal", "China should rebalance". These are policy prescriptions, requiring welfare analysis and values judgments outside the mission scope (L001 — "neither real-time trading data nor opinion publisher").

The narrative prompt's banned-token list includes "should", "must", "needs to", "ought to" in policy-prescriptive context. The validator strips and regenerates.

## The taxonomy as a public commitment

The taxonomy is published as a methodology page (`opengem.org/methodology/claim-types`) with worked examples of each claim type and the literature support for the refusals. This is the L001 "publishes its mistakes" principle applied to *what we claim* — not just *what we predict*.

The page is the central reference. Editors, contributors, and LLM-narrative outputs are all bound by it.

## Pitfalls

1. **Causal language is natural.** It is hard for an LLM, or a human writer, to discuss forecasts without slipping into causal phrasing. Constant linter pressure helps; periodic audits of published narrative against the taxonomy catch drift.

2. **The reader will misread.** Even with hedged language, some readers will infer causal claims. We cannot fully prevent that. The mission is to be *epistemically clean in our own claims*, not to control the reader's interpretation.

3. **Some claims are genuinely on the boundary.** "OPENGEM's GDP forecast was revised down 0.12 pp after the GDP advance estimate came in soft." Is the *advance estimate* the cause? No — the advance estimate is *information*, not a cause. The phrasing must reflect "in light of softer input data" rather than "because the advance estimate was soft."

## What this loop produced

- 7-row taxonomy of claim types.
- Refusal scope (causal forward, policy prescription).
- Surface-by-surface permission matrix.
- Narrative pipeline enforcement (banned phrases, regex, regenerate).
- `causal_basis` schema field for the rare permitted cases.
- Public methodology page commitment.
- Pitfalls: language drift, reader misinterpretation, boundary cases.

## What comes next

- **L210** — counterfactual scenarios are the *most permissive* causal surface; this taxonomy gates them.

## Related

- [[L181-forecast-object-schema]] — `causal_basis` field.
- [[L198-narrative-pipeline]] — enforcement.
- [[L196-scenario-triggers]] — conditional claims live here.
- [[L210-counterfactual-scenarios]] — counterfactual surface.
- [[L200-failure-log]] — attribution claims.
- [[L001-vision-statement]] — "Not a black-box AI forecast" foundation.
