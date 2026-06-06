# OPENGEM Epistemic Contract

**The contract**: every quantitative output OPENGEM exposes is framed as
**"this could happen based on X"** — never as **"this WILL happen."**

This is not a stylistic preference. It is the **load-bearing claim** that
distinguishes OPENGEM from ChatGPT-alone, Stratfor, NiGEM, and every other
geopolitical-economic information source. Strip this contract and OPENGEM's
value collapses.

---

## Why this matters

Three audiences read OPENGEM outputs:

1. **The friend** (international-politics YouTuber, alpha customer). He cites
   OPENGEM on camera. If OPENGEM ever says "X will happen" and X doesn't, his
   credibility takes the hit. He needs OPENGEM to say *"under these assumptions,
   based on this model, X could happen"* — defensible whether X happens or not.

2. **Future external readers** (any audience the friend reaches, and eventual
   broader users). The same logic scales.

3. **Future-self of the maintainer**, six months from now, reviewing the
   archive. Did OPENGEM say something that aged badly? If every claim was
   conditional and basis-cited, the answer is *"the conditional held; the
   antecedent did/didn't manifest"* — not *"we were wrong."*

## The rule

Every quantitative output that leaves OPENGEM's process boundary MUST be
wrapped in a `Conditional[T]` (see `opengem-types/conditional.py`) with:

1. **value** (the number / quantile / probability / decision)
2. **basis.model_or_method** — non-empty, names what produced the value
3. **basis.inputs_description** — human-readable account of inputs
4. **confidence** (POINT | RANGE | DISTRIBUTION | BASE_RATE | SCENARIO_PATH)
5. **conditional_on** — explicit antecedents (when applicable)
6. **basis.caveats** — what's NOT captured

Internal computations may use bare values. API surfaces may not.

## Forbidden language

| ✗ Forbidden | ✓ Required |
|---|---|
| "GDP will fall 1pp" | "Based on the L2 BGVAR IRF, GDP could fall ~1pp under this shock" |
| "Iran is going to escalate" | "In past N analogous episodes, 40% escalated within 3 months" |
| "The Fed will cut rates" | "OIS-implied policy path suggests one cut in Q4; market-implied probability 65%" |
| "Markets are heading for a crash" | "Term-spread + VIX cross indicate recession-regime conditions, per Bauer-Mertens" |
| "Inflation is going to surge" | "GSCPI is at +1.4σ; supply-chain pressure correlates historically with +1pp PPI at 4Q" |

See `opengem-narrative.FORBIDDEN_PREDICTIVE_PHRASES` for the enforced list.

## Required conditional markers

A non-trivial narrative (>200 chars) must contain **≥2** of:

`could`, `would`, `based on`, `suggests`, `implies`, `if `, `in past`, `model`,
`scenario`, `probability`.

See `opengem-narrative.REQUIRED_CONDITIONAL_MARKERS`.

## Where the contract is enforced

| Layer | Enforcement |
|---|---|
| **opengem-types** | `Conditional[T]` requires non-empty `basis.model_or_method`; `render_human` emits conditional phrasing by default |
| **opengem-narrative** | System prompts include the EPISTEMIC CONTRACT clause verbatim; `lint_narrative_text` scans LLM responses for forbidden phrases and insufficient conditional markers |
| **opengem-recession-prob** | `RecessionProbabilityResult.to_conditional()` wraps the output with explicit antecedents (current spread, historical signal-to-recession mapping) |
| **opengem-digest** | Markdown renderer prefixes both the Situation panel and the Scenarios section with the "every value below is conditional" disclaimer; recession-probability row says "could happen based on {model}" |
| **opengem-scenarios** | Pack templates carry `rationale` and `references` fields; scenario IDs include the `@invoked_at` timestamp to make "as-of" clear |

## Tests that protect the contract

- `opengem-types/tests/test_conditional.py` — Conditional construction + framing
- `opengem-narrative/tests/test_epistemic.py` — every forbidden phrase is caught by the linter; every system prompt contains the EPISTEMIC CONTRACT clause
- `opengem-recession-prob/tests/test_model.py::test_to_conditional_frames_correctly` — the recession-prob result renders conditionally with explicit antecedents
- `opengem-digest/tests/test_digest.py::test_render_markdown_conditional_framing_present` — the daily digest renders "conditional" + "could happen based on" prominently

## The leader-behavior pillar (extra caution)

When the leader-behavior pillar (`opengem-leader-actions`, `opengem-leader-patterns`)
is built, this contract gets stricter:

- **No psychological speculation** (no "X is paranoid/narcissistic/strategic")
- **Base-rates only**: outputs use `ConfidenceKind.BASE_RATE`
- **Explicit framing**: "In past N analogous contexts, leader X chose action A
  in K% of cases. The current context shares M of the analogous features."
- **Never** "X will do Y" — even with "probably."

See `docs/research/R31-observatory-design.md` (TBD) for the full leader-pillar guardrails.

## Failure mode

If an LLM response passes through OPENGEM with a violation:
- `lint_narrative_text` returns it in `violations`
- The narrative API will, in v0.4+, either reject the response or auto-retry
  with a stricter prompt. At IOC, the lint output is surfaced in the digest as
  a warning ("Narrative contains predictive phrasing — review before posting").

## Versioning

This contract is **v1.0**. Changes require:
- ADR-style memo in `docs/research/` explaining the change
- A new version of `opengem-narrative` system prompts
- A migration plan for the affected packages

The contract is not allowed to weaken without explicit owner sign-off.

---

*This document is enforced at the code level, not just in spirit. Read the test
suite for the executable form.*
