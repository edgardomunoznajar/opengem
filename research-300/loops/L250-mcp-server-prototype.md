# L250 — MCP server prototype (extends OPENGEM scenarios)

**Loop**: 250 / 300
**Phase**: 5 — Code prototypes
**Date**: 2026-06-06
**Artifacts**: `prototypes/dashboard-next/app/mcp/page.tsx` (install page) + design below

---

## What was built

The `/mcp` install page enumerates eight tools and provides install snippets for Claude Desktop, Cursor, ChatGPT (via Connectors), and VS Code (via Continue.dev). The actual MCP server is a planned extension of the existing `opengem-scenarios` package — see "Architecture" below.

## The 8 tools (v0.1 surface)

```
get_forecast(country: str, indicator: str, horizon: str) -> Forecast
compare_forecasts(country: str, indicator: str, horizon: str) -> CompareResult  # OPENGEM vs WEO/OECD/SEP/SPF
list_scenarios(threshold: float = 0.10) -> list[Scenario]
get_recession_probability(country: str) -> SituationTile
get_gpr_nowcast(country: str | None = None) -> SituationTile
rewind_vintage(date: str, what: str = "forecasts", country: str | None = None) -> ReplayBundle
get_leaderboard(indicator: str, horizon: str = "4Q") -> list[LeaderboardRow]
list_misses(indicator: str | None = None, since: str | None = None) -> list[MissRecord]
```

Every tool response **MUST include**:

- `vintage_id` (the data snapshot)
- `provenance` (git_sha, container_digest, generated_at)
- `model_card_url` (for forecast-producing tools)
- `miss_log_url` if there's any historical miss for the cell

This is non-negotiable. It's what makes OPENGEM responses chain-of-trust to the LLM consumer.

## Architecture — packaging

```
packages/opengem-mcp/
├── pyproject.toml         # depends on: opengem-vintage, opengem-scenarios, opengem-digest, opengem-types
├── src/opengem_mcp/
│   ├── __init__.py
│   ├── server.py          # stdio + SSE transports
│   ├── tools/             # one module per tool, each exporting a `register(server)` function
│   │   ├── get_forecast.py
│   │   ├── compare_forecasts.py
│   │   ├── list_scenarios.py
│   │   ├── ...
│   ├── schemas.py         # JSON-Schema for tool inputs/outputs (mirrors opengem-types via Zod-equivalent)
│   └── auth.py            # API-key-aware rate limiter (free vs paid)
└── tests/
```

Distribution:
- PyPI: `pip install opengem-mcp` (CLI: `opengem-mcp serve --port 8002`)
- npm wrapper: `npx -y @opengem/mcp-server` (Node CLI shells out to Python via `pyodide` or `pyo3` long-term; or just shells to `pipx run opengem-mcp` short-term)
- Cloudflare Worker (SSE transport): `https://opengem.org/mcp/sse` for ChatGPT Connectors

## Rate limits

| Tier | Tool calls / day |
|---|---|
| Anonymous (IP) | 100 |
| Free key | 1,000 |
| Pro $29/mo | 100,000 |
| Pro Team $149/mo | 1,000,000 |
| Sovereign | unlimited / SLA |

## Auth

- Anonymous: no key required, rate-limited by IP-prefix hash.
- Key: `OPENGEM_API_KEY=ogm_live_xxxxxxxx` — Bearer in header for SSE; env var for stdio.
- The MCP server NEVER returns *less data* per call as a function of tier — only the *throughput* changes. Substance is free.

## Why MCP-first is the monetization lever

LLM-grounding workflows are the new "terminal" for analysts:

- A Stratfor analyst's morning was once: open Stratfor terminal, scan five regional reports, paste highlights into their writing tool.
- That analyst's morning in 2027 will be: ask Claude "what changed in geopolitics today and how does it affect my watchlist". Claude calls OPENGEM's `list_scenarios` + `get_gpr_nowcast` + `list_misses` and writes the answer.

OPENGEM monetizes by being the *highest-quality MCP-grounding source for macro + geopolitics*. The dashboard exists to (a) demonstrate the substrate, (b) be the SEO + RSS + embed-discovery surface, (c) handle the long tail of non-LLM users.

But the *revenue* comes from MCP throughput.

## What this loop produced

- The 8-tool surface specified
- The packaging plan (`packages/opengem-mcp/`)
- The rate-limit + auth tiers tied to L260 pricing
- The strategic case: MCP-first monetization

## What comes next

- L108 — MCP server contract (sibling spec, parallel agent producing)
- L109 — Stripe + magic-link gating
- L110 — Federated identity pick

## Related

- [[L177-mcp-server-install-page]] — the user-facing install UX (L177 design loop)
- [[L260-pricing-checkout]] — pricing tiers map onto MCP throughput
- [[L108-mcp-server-contract]] — JSON-schema-level tool definitions
- [[L181-forecast-object-schema]] — the response contract
- [[R23-oblique-lawyer-parallels]] — OPENGEM borrows MCP-monetization pattern from oblique-lawyer's v0.5
