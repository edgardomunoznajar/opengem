# L198 — Narrative Pipeline: Forecast JSON → 3-Paragraph Segment

**Loop**: 198 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

The dashboard's headline product is *numbers* (forecasts, bands, scenarios). But the YouTuber persona's "morning paste-into-ChatGPT" workflow wants those numbers in *prose*. The narrative pipeline takes the forecast.v1 JSON (and the scenario firing record, and the surprise index) and produces a 3-paragraph segment grounded in the open numbers.

This loop pins the prompt engineering rules, the model selection policy, the human-in-the-loop checkpoints, the failure modes we refuse, and the licensing posture.

The package `opengem-narrative` exists (R99 §3.1 / README). This loop sharpens it for the dashboard surface.

## Inputs to the narrative

For a given country at a given moment, the narrative pipeline consumes:

1. The country's forecast bundle (forecast.v1 JSON per indicator × horizon — typically 8-20 forecasts).
2. The surprise index history (last 30 days).
3. The currently-active scenarios + probabilities.
4. The latest realised data points (with vintage timestamps).
5. The track record (calibration status, recent misses).

These come from the same `/v1/forecast-card`, `/v1/surprise`, `/v1/scenarios/active`, `/v1/realised` endpoints the dashboard chart uses (L195). The narrative is *downstream* of the numbers, not parallel.

## The system prompt

```
You are an OPENGEM analyst. You write a 3-paragraph segment grounded entirely
in the JSON I will provide. Your audience is a quantitatively-literate adult
who is comfortable with numbers but not an econometrician.

CONTRACT:
1. Every number in your prose must appear in the JSON. Do not invent.
2. Every claim about causality must be marked uncertain ("likely", "consistent
   with", "suggests") unless the JSON's `causal_basis` field permits otherwise
   (currently always false).
3. Paragraph 1: state the headline forecast and band. Identify what changed
   from the prior vintage if the revision-arrow data is in the JSON.
4. Paragraph 2: situate the forecast against consensus (WEO, OECD EO, FRB SEP,
   ECB SPF). State whether OPENGEM is above, in line, or below; quantify.
5. Paragraph 3: name the scenarios that are currently active with probability
   > 15%, in descending probability order. For each, give the trigger
   condition in plain language.

STYLE:
- Plain English, no jargon a numerate undergraduate would not know.
- No "could", "may potentially", or other weasel. Use "likely" or "is".
- Sentences ≤ 25 words.
- No more than one decimal place unless the JSON has more precision.
- Cite every metric inline like: "GDP YoY forecast 2.18% (P10-P90: 1.04% to 3.28%)".
- Avoid metaphors and editorial framing ("rosy", "ominous", "the market
  is signalling"). Stay clinical.

OUT OF SCOPE:
- Do not recommend trades, do not say "we expect" — say "OPENGEM forecasts".
- Do not predict politics. Do not mention any individual policymaker by name.
- Do not name any single news event from outside the JSON.
```

This prompt is versioned with the `opengem-narrative` package. Changes go through the same PR/review process as code.

## Model selection policy

Two routes:

### Local (default): a frontier model via API

The dashboard backend submits the system prompt + JSON to a frontier LLM (Anthropic Claude 4.7 1M context, OpenAI GPT-5, Google Gemini 2.5 Pro — selectable per call). The result is the narrative.

We do not run a small local model for the narrative because the public dashboard renders ~50,000 narratives per day at peak and small-model failure modes (hallucination, off-prompt) are too costly. Frontier API at ~$0.0005/call is cheaper than maintaining a local serving stack.

### Self-host (paid tier): user's choice of model

For Pro and Institutional tier users, the dashboard offers "bring your own key" mode. The user supplies their OpenAI/Anthropic/Google API key; the narrative is generated against the user's account; OPENGEM never sees the key in plaintext (it is forwarded server-to-API with a short-lived ephemeral token, never logged).

### MCP route (third party LLM): the friend's workflow

The friend (R99, README) pastes the JSON block into ChatGPT directly. The system prompt is hosted at `opengem.org/narrative-prompt.md` and the friend's saved instruction set references it. This is the L001 distribution play: OPENGEM does not need to host the LLM; we host the prompt.

## The output schema

```json
{
  "schema": "opengem.narrative.v1",
  "narrative_id": "narr_2026-06-06T08:00:00Z_USA",
  "scope": {"country": "USA", "as_of": "2026-06-06T08:00:00Z"},
  "model_used": "anthropic-claude-4.7-1m",
  "model_temperature": 0.3,
  "prompt_version": "v2.1",
  "input_hash": "sha256:...",  // hash of inputs JSON
  "output_hash": "sha256:...",  // hash of the produced text
  "paragraphs": [
    "OPENGEM forecasts USA real GDP year-over-year at 2.18% for 2027-Q1, with an 80% band of 1.04% to 3.28%. The forecast revised down 12 basis points from the April vintage (2.30%), driven primarily by softer 2026-Q1 GDP advance estimate (-0.4 pp lower than prior vintage) and partially offset by a higher long-yield path lifting financial conditions inputs.",
    "Against consensus, OPENGEM sits slightly above IMF WEO (2.10%) and OECD EO (2.05%), and roughly in line with the Federal Reserve SEP (2.20%). The gap to WEO is 8 basis points and has remained inside that range since October 2025.",
    "Two scenarios are currently active for USA. Soft landing (42% probability) — the term-spread has steepened modestly and surprise-index has trended toward zero. Hard landing (18% probability) — the 10y-3m spread remains below -0.5%, sustained for the past 4 months."
  ],
  "verifications": {
    "every_number_in_input_json": true,
    "no_causal_claim_above_threshold": true,
    "all_active_scenarios_listed": true,
    "paragraph_count": 3
  },
  "license": "CC-BY-4.0",
  "citation": "OPENGEM (2026). USA macroeconomic situation narrative, 2026-06-06.",
  "regenerate_url": "/v1/narrative/USA?regenerate=1"
}
```

## Output verification

After generation, the narrative is verified before publication:

| Check | Method | Failure action |
|---|---|---|
| Every numeric token in output appears in input JSON | Regex extract all numbers; check each against input JSON | Reject; regenerate up to 3 times; fall back to template-only |
| No paragraph exceeds 25 words/sentence | Spacy or regex sentence split | Reject; regenerate |
| 3 paragraphs exactly | Split on blank line | Reject; regenerate |
| No banned tokens (named policymakers, predictions of trades, named individuals) | Keyword denylist | Reject; regenerate |
| Active scenarios > 15% prob mentioned | Cross-reference scenario probability JSON | Reject; regenerate |

If three regenerations fail, fall back to a *template-only* narrative — a deterministic Mustache template that fills slots from the JSON. Less elegant but byte-deterministic.

## The template fallback

```
OPENGEM forecasts {country} {indicator} at {point}% for {scoring_period},
with an 80% band of {p10}% to {p90}%. The forecast {direction} from the
{prior_vintage_date} vintage ({prior_point}%).

Against consensus, OPENGEM sits {comparison_direction} IMF WEO ({weo}%) and
{comparison_direction_oecd} OECD EO ({oecd}%).

{n_active_scenarios} scenarios are currently active for {country}: {scenario_list}.
```

Filled from the JSON, no LLM call needed. Used when LLM generation fails verification or when the user explicitly wants a "no-LLM, deterministic" narrative.

## Cadence

- Each country's narrative is regenerated on every forecast publication (matching L187 cadence per indicator).
- Narratives are cached for 1 hour to avoid LLM cost on every page load.
- The "regenerate" button on the dashboard explicitly forces a re-run; clicking it costs OPENGEM ~$0.0005 in LLM API fees.

## Pitfalls and the refusal scope

1. **Hallucinated numbers.** Frontier LLMs occasionally insert plausible numbers that are not in the input. The verification regex catches most; the regeneration loop handles the rest. The template fallback handles total failure.
2. **Editorial drift.** LLMs trend toward editorialising ("the economy is showing signs of strain"). The prompt explicitly forbids this; the verification denylist enforces.
3. **Plagiarised paragraph structure.** Across many countries on the same day, the same model produces near-identical paragraph templates. We accept this — the template-like quality is actually a *feature* (the narrative reads like a standardised report), not a bug.
4. **Causality claims.** A hard refusal: the narrative may say "consistent with X" but may not say "X caused Y" unless the input JSON explicitly authorises a causal claim. L209 defines the taxonomy of when causal claims are permitted. As of v1.0, the answer is: never.

## Licensing

The narrative output is CC-BY-4.0 like all OPENGEM content. The system prompt is Apache-2.0. Anyone can fork the prompt, run it through their own LLM, and produce derivative narratives — but the JSON contract anchors the numbers.

The LLM provider's terms apply to the *generation*: OpenAI/Anthropic ToS govern the call. The *output text* under those ToS is OPENGEM's to license.

## The friend-mode prompt

The README's "friend workflow" specifically supports paste-into-ChatGPT. The friend opens the daily digest (`docs/example-digest.md`), copies the JSON block at the bottom, and pastes into ChatGPT with the system prompt hosted at the public URL. This is the simplest path to a 3-paragraph YouTube segment.

## What this loop produced

- System prompt v2.1 with contract.
- Three model-selection routes (server frontier API, BYOK, MCP/paste).
- Output schema with verification fields.
- Six verification checks + regenerate loop + template fallback.
- Caching cadence.
- Refusal scope (causality, named policymakers, trades).
- Licensing.

## What comes next

- **L199** — trust signals shown alongside narrative.
- **L209** — causal-vs-forecast taxonomy that governs the prompt.

## Related

- [[opengem-narrative]] — existing package this extends.
- [[L181-forecast-object-schema]] — input JSON.
- [[L191-surprise-index]] — input.
- [[L196-scenario-triggers]] — input.
- [[L197-scenario-probability-synthesis]] — input.
- [[L209-causal-vs-forecast-claims]] — refusal rules.
- [[L001-vision-statement]] — "grounded narrative, never instead of numbers".
