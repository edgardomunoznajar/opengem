# opengem-narrative

🧪 alpha

The narrative output layer. Per R31 and the program-owner direction
("ChatGPT and nothing else" → "make it beat Stratfor"), OPENGEM doesn't *build*
the LLM narrative layer — it specifies the **system prompt** and **JSON
contract** that turns a grounded ChatGPT into an analyst-grade prose generator.

## What's in it

- **System prompts**: ready-to-paste prompts in `prompts/` (curated, versioned)
  - `analyst_segment_v1.md` — produces a 3-paragraph YouTube video segment
  - `executive_summary_v1.md` — produces a 1-paragraph executive summary
  - `scenario_table_v1.md` — produces a markdown table format for cross-scenario comparison
- **`NarrativeRequest`** — typed input contract (the JSON the user pastes)
- **`NarrativeOutput`** — typed expected output contract (the response format
  the prompt instructs the LLM to follow)
- **`build_narrative_request`** — converts a `Digest` ScenarioSection into a
  paste-ready NarrativeRequest

## Why this exists (not a full LLM wrapper)

Per R31 — the friend already has ChatGPT. OPENGEM's job is to ensure his ChatGPT
session is *grounded in real numbers from real models* rather than the LLM's
training-data guesses. The narrative layer is the contract: structured input →
constrained output.

If/when OPENGEM eventually adds a server-side LLM call (v0.4+), this same
contract is reused.

## Anti-hallucination contract

Every system prompt includes the hard rule:

> Do not invent numbers. Every numerical claim must reference a field in the
> JSON input. If a claim isn't in the input, state "OPENGEM doesn't currently
> model this."
