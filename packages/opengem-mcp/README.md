# opengem-mcp

OPENGEM MCP server — 10 tools that wrap the OPENGEM public API for LLM grounding.

Per L108 (research-300 deep dive): every tool response is vintage-stamped and includes
provenance, so any LLM consuming it cannot hallucinate a forecast without contradicting
its own tool output.

## Tools

| Tool | What it does |
|---|---|
| `get_forecast`            | Fetch a single forecast object — country × indicator × horizon |
| `compare_forecasts`       | OPENGEM vs WEO / OECD EO / FRB SEP / ECB SPF |
| `list_scenarios`          | Currently-triggered scenarios with probability |
| `get_recession_probability` | Bauer-Mertens 12-month nowcast per country |
| `get_gpr_nowcast`         | Geopolitical Risk nowcast (global or per-country) |
| `rewind_vintage`          | Replay any historical forecast at any vintage date |
| `get_leaderboard`         | Forecast leaderboard per indicator × horizon (CRPS-ranked) |
| `list_misses`             | Recent forecast misses with post-mortem URLs |
| `subscribe_events`        | Long-lived SSE stream of macro + geopolitical events |
| `cite_this_view`          | Emit a guaranteed citation format for any OPENGEM page |

## Install

```bash
pip install opengem-mcp
```

Or via npx (the npm wrapper shells to `pipx run opengem-mcp`):

```bash
npx -y @opengem/mcp-server
```

## Configure (Claude Desktop)

```json
{
  "mcpServers": {
    "opengem": {
      "command": "npx",
      "args": ["-y", "@opengem/mcp-server"],
      "env": { "OPENGEM_API_KEY": "" }
    }
  }
}
```

## CLI

```bash
opengem-mcp serve                # stdio transport, default
opengem-mcp serve --sse --port 8002   # SSE transport for ChatGPT Connectors
```

## Rate limits

| Tier | Tool calls / day |
|---|---|
| Anonymous (IP) | 100 |
| Free key | 1,000 |
| Pro $29/mo | 100,000 |
| Pro Team $149/mo | 1,000,000 |
| Sovereign | unlimited / SLA |

## Architecture

`server.py` implements both stdio and SSE transports against the JSON-RPC 2.0
MCP protocol. Each tool is a separate module under `tools/` exposing a single
`call(args, ctx) -> dict` function.

All tool responses are wrapped by `_envelope()` which guarantees:
- `vintage_id` field
- `provenance` object (git_sha, container_digest, generated_at)
- `cite_url` permanent OPENGEM URL

## See also

- L108 — MCP server contract
- L250 — MCP server prototype
- L260 — pricing tiers map onto MCP throughput
