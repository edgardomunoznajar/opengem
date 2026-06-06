# L020 — FinGPT / FinNLP / FinRL / FinRobot: LLM-for-Finance Toolkits

**Loop**: 020 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## The AI4Finance Foundation family

[AI4Finance-Foundation](https://github.com/AI4Finance-Foundation) is the leading academic/community OSS group for LLM/RL applications in finance, anchored by faculty and PhD students from Columbia, NYU, and contributors from industry. Five repos matter for OPENGEM:

| Repo | Stars | License | Last commit | Focus |
|---|---|---|---|---|
| **[FinGPT](https://github.com/AI4Finance-Foundation/FinGPT)** | 20.4k | MIT | June 2026 | Open-source financial LLMs (LoRA fine-tunes of Llama / Falcon / ChatGLM / Qwen) |
| **[FinRL](https://github.com/AI4Finance-Foundation/FinRL)** | 15.4k | MIT | May 2026 | Reinforcement learning for trading (DOW 30, crypto, portfolios) |
| **[FinRobot](https://github.com/AI4Finance-Foundation/FinRobot)** | 7.2k | Apache-2.0 | June 2026 | Multi-agent platform for financial analysis (AutoGen + LangChain) |
| **[ElegantRL](https://github.com/AI4Finance-Foundation/ElegantRL)** | 4.3k | Apache-2.0 | Active | Massively-parallel deep RL infrastructure |
| **[FinNLP](https://github.com/AI4Finance-Foundation/FinNLP)** | 1.5k | MIT | Jul 2024 | Financial NLP toolkit (news scraping, sentiment datasets) |

Plus their dataset/env repo:
- **[FinRL-Meta](https://github.com/AI4Finance-Foundation/FinRL-Meta)** — ~1.9k stars, datasets + gym environments.

## What each one is, in honest terms

### FinGPT — "BloombergGPT but free and LoRA"

The pitch: Bloomberg spent ~$3M training BloombergGPT on a proprietary corpus. FinGPT does ~$300 LoRA fine-tunes of open base models (Llama 2/3, Falcon, ChatGLM2, MPT, Qwen) on financial text. Tasks supported: sentiment analysis, headline classification, relation extraction, NER, financial Q&A, stock-movement forecasting via FinGPT-Forecaster.

What's actually reusable: the **FinBench evaluation suite** (sentiment/headline/NER datasets in a standardized format), the **LoRA adapters published on HuggingFace** (we could potentially merge them into our narrative-generation model without retraining), and the **prompt templates** for tasks like "extract economic indicator from news headline."

What's *not* useful: FinGPT-Forecaster's stock-prediction LoRA. Wrong asset class (equities), wrong horizon (next-day), wrong evaluation (directional accuracy on individual tickers). The methodology is fine, the target variable is irrelevant to OPENGEM.

### FinRL — RL for equity / crypto trading

Pure equity-and-crypto reinforcement learning. State = market features, action = portfolio weights, reward = Sharpe-flavored return. The "applications" folder is DOW 30 trading, portfolio allocation, crypto trading. **Macro is absent.** Re-using FinRL as a substrate would require redefining state (macro indicator panel), action (forecast point + bands), and reward (CRPS / log-score), which is essentially rewriting the framework. We don't.

The interesting piece is **ElegantRL** underneath — a massively-parallel DRL framework. If we ever needed scaled-up RL for, say, "learn the optimal model-combination weights across scenarios" (L189, L202), ElegantRL is the closest open-source substrate. That's a 2027+ question.

### FinRobot — the AGI-for-equity-research play

Multi-agent platform built on Microsoft AutoGen + LangChain. Agents include: market forecaster, document analyzer, trading strategist, equity research report generator. The architecture is exactly what you'd guess from a 2024-2025 vintage agentic-LLM paper: four layers (agents → algorithms → LLMOps → foundation models), Chain-of-Thought decomposition, function-calling against Finnhub/FMP APIs, generates a multi-page equity research report with charts and DCF tables.

**Why this matters for OPENGEM**: FinRobot is the closest existing OSS template for "LLM agent + structured data → narrative report." Their equity-research-report pipeline is *structurally* what OPENGEM needs for **L198 (forecast-to-narrative)** and **L295 (YouTube content engine)** — except aimed at countries and indicators instead of tickers.

The agents are AutoGen-based (each agent = a Python function decorated with `@register_function`). Pluggable LLM backend (defaults to GPT-4, supports Anthropic, OpenRouter, local Ollama). The grounding story is: data fetched via API → injected as structured JSON into the prompt → agent generates a section → next agent reviews / extends → final agent assembles markdown report.

**This is salvageable.** The agent orchestration patterns transfer; the data-source layer is replaced with OPENGEM's MCP server tools.

### FinNLP — data downloaders, mostly dormant

Last meaningful commit was July 2024. It's a collection of news/social-media scrapers (Yahoo, Reuters, Seeking Alpha, Sina Finance, Twitter/X, StockTwits, Reddit, Weibo) plus the **AShare news corpus** (3,680 Chinese stocks, 2018-2021, ~3M articles) and **stocknet tweets**. License: MIT.

For OPENGEM, the scrapers are *interesting but legally fragile* (most of these sites have stricter ToS in 2026 than in 2024 when the scrapers were written; using them as-is invites cease-and-desist). The AShare corpus is the actually-valuable asset — but it's Chinese-equity-news, the wrong domain. Skip.

### FinRL-Meta — datasets and environments

A standardized container for paper datasets and gym environments used in FinRL papers. Useful for benchmarking RL methods. Not useful for OPENGEM directly.

## What's reusable for OPENGEM narrative generation?

**The core OPENGEM narrative pipeline (L198) needs to do something like:**

```
forecast vintage JSON
  + model card metadata
  + provenance lineage
  + historical miss-rates
  → markdown report:
     - lede: "OPENGEM's June 2026 vintage projects euro-area Q4 CPI at 2.6% (P10-P90: 2.1-3.2),
       0.3pp above WEO's April 2026 figure and 0.1pp below the ECB SPF Q2 median."
     - methodology pop-up
     - track record overlay
     - "what would change our view" section
```

This is a *table-to-text* problem with strict factuality constraints. The forecast numbers must round-trip exactly. Hallucination is brand-fatal: if our narrative says "P50 is 2.6%" but the underlying JSON says 2.7%, we've broken the accountability thesis (L001) in the most embarrassing way possible.

### What FinGPT / FinRobot contribute

| Pattern | Source | OPENGEM use |
|---|---|---|
| LoRA-tune base model on financial register vocabulary | FinGPT | Optional v2: fine-tune Llama 3 on our own forecast-report archive |
| Multi-agent orchestration via AutoGen | FinRobot | The orchestration shape for our pipeline (data-fetch agent → draft agent → review agent → fact-check agent) |
| Function-calling against structured-data APIs | FinRobot | Direct: our MCP server tools become the agent's callable functions |
| Prompt templates for "extract economic indicator from text" | FinGPT FinBench | Direct: useful for reading central-bank speeches into structured features |
| Chain-of-Thought decomposition for financial analysis | FinRobot | Direct: forces grounding before narrative |
| FinBench eval suite | FinGPT | Reference for our own narrative-faithfulness eval |

### What we explicitly do NOT take

- **No FinGPT-Forecaster** — wrong target.
- **No FinRL agents** — wrong asset class.
- **No FinNLP scrapers** — legally fragile + wrong domain.
- **No FinRobot's equity-DCF-table generator** — wrong analytical artifact.
- **No claim of "we use FinGPT/FinRobot as a substrate"** — we *borrow patterns* and *cite the lineage*; we do not adopt their stack wholesale.

## The build vs steal pattern

The right OPENGEM narrative stack, drawing FinGPT / FinRobot lessons but not their code:

1. **Base LLM**: Claude Sonnet / GPT-4o / local Llama 3 (configurable, MCP-routed).
2. **Grounding layer**: every numeric claim flows from a structured JSON object via Jinja2 or similar; we never let the LLM emit a number it didn't receive verbatim. Pattern stolen from FinRobot's CoT.
3. **Orchestration**: lightweight (we may use AutoGen or just LangGraph — but not FinRobot's specific Agent classes). Three agents: `fetch`, `draft`, `verify`.
4. **Faithfulness eval**: every generated paragraph passes through a numeric-extraction check (regex + LLM-as-judge against the JSON). Failures route to human review. Pattern parallel to FinGPT's FinBench evaluation discipline.
5. **Optional fine-tune**: if we accumulate 1000+ human-curated reports, do a LoRA on a base Llama for register-matching. Pattern stolen from FinGPT.

Total dev effort: ~3 weeks for v1 narrative pipeline. Adding LoRA fine-tune: +2 weeks if we want it.

## License and citation hygiene

All five repos are **MIT or Apache 2.0** — compatible with our Apache 2.0 thesis. The clean license is part of why this family is more useful than, say, BloombergGPT (closed) or HuggingFace's Llama-based finance models (some carry Meta's Llama Acceptable Use clause).

**We owe citation** to FinGPT / FinRobot in our methodology page (L135) and model card (L172) for the patterns borrowed. That's not a legal obligation; it's an accountability obligation. The OPENGEM thesis is asymmetric *because* we cite the lineage of every part.

## Surprise of the loop

**FinRobot, not FinGPT, is the strategically important repo here.** The headlines all go to FinGPT (open BloombergGPT! free LoRA! 20k stars!), but FinGPT is a *model family*, not a *system*. FinRobot is a *system* — it shows what a working agent-orchestrated, table-grounded, multi-step financial-report pipeline looks like in 2026. For OPENGEM, where the product is the report (not the model), the system patterns matter more than the model weights. FinRobot is the salvageable piece.

A second surprise: **the family does not solve the macro problem.** None of these projects materially address macroeconomic forecasting or narrative. The center of mass is equity / crypto / sentiment / single-firm fundamentals. OPENGEM's macro-with-LLM-narrative niche is genuinely open — there is no AI4Finance-style flagship for it. That's a real moat opportunity if we ship a clean reference implementation.

## Cost-benefit

| Action | Cost | Benefit |
|---|---|---|
| Steal FinRobot's multi-agent CoT pattern for L198 pipeline | 0.5 week study + 2 week build | The right structural template |
| LoRA-tune Llama 3 on financial-report corpus | 2 weeks (after we have 1000 reports) | Better register match; defer |
| Adopt FinGPT's FinBench eval pattern for our faithfulness check | 1 week | Industry-standard methodology |
| Integrate any AI4Finance repo directly | 4-6 weeks + ongoing | Net negative — wrong asset class |
| Cite the lineage in L135 / L172 | 0.1 week | Accountability discipline |

## What this loop produced

- Family map of five AI4Finance repos with license, stars, last-commit, focus.
- Clear pattern-vs-substrate breakdown: pattern yes, substrate no.
- Identification of FinRobot (not FinGPT) as the strategically relevant repo.
- Proposed OPENGEM narrative pipeline (v1: 3 weeks; v2 LoRA: +2 weeks).
- Recognition that the macro+LLM-narrative niche is genuinely open.

## What comes next

- **L044** — Nixtla / neuralforecast / darts: the forecast substrate this narrative consumes.
- **L108** — MCP server contract: function-calling targets for the narrative agent.
- **L135** — Methodology page: home of the citation lineage.
- **L172** — Methodology pop-up on every chart: where the narrative manifests in UI.
- **L198** — Forecast-to-narrative pipeline: the build downstream from this loop.
- **L295** — YouTube content engine plan: scripted narrative for video.

## Related

- [[L001-vision-statement]] — "Generative narrative on top of grounded numbers, never instead of them" is the binding constraint of this loop.
- [[L011-openbb-terminal]] — different OSS-finance gravity well, also in the agent / MCP neighborhood.
- [[L017-awesome-quant-roundup]] — AI4Finance repos appeared there; this loop is the deep dive.
- [[L018-pdf-table-tools]] — docling extracted Markdown is one input to this narrative pipeline.
- [[L198-narrative-pipeline]] — direct build downstream.
