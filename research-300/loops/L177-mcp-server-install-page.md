# L177 — MCP-Server Install Page

**Loop**: 177 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

MCP (Model Context Protocol) is the long-term distribution channel for OPENGEM. An MCP server lets ChatGPT, Claude, Cursor, Cline, and every future LLM chat ground itself in OPENGEM forecasts without OPENGEM building a chat product.

The install page is one-click for each major host. Setup snippets included.

## URL

`/mcp`

Linked from:
- Top nav under "Developers" submenu
- Command palette: "MCP install"
- Footer
- The home page: "Use with ChatGPT, Claude, Cursor →"

## The page

```
   ┌────────────────────────────────────────────────┐
   │  Use OPENGEM with your LLM                       │
   │  ──────────────────────────────────────────    │
   │                                                  │
   │  Connect ChatGPT, Claude, Cursor, Cline, or     │
   │  any MCP-compatible chat to OPENGEM. Your LLM   │
   │  can pull forecasts, indicators, scenarios,     │
   │  and accountability data on demand.              │
   │                                                  │
   │  Choose your host:                               │
   │                                                  │
   │  [Claude Desktop] [ChatGPT Pro] [Cursor]        │
   │  [Cline (VS Code)] [Continue.dev] [Aider]       │
   │  [Generic MCP] [stdio]                           │
   │                                                  │
   │  ──────────────────────────────────────────    │
   │  [Selected: Claude Desktop]                      │
   │                                                  │
   │  ## Step 1: Copy this snippet                    │
   │  Add to ~/Library/Application Support/Claude/   │
   │       claude_desktop_config.json:                │
   │                                                  │
   │  ```json                                         │
   │  {                                                │
   │    "mcpServers": {                                │
   │      "opengem": {                                 │
   │        "command": "npx",                          │
   │        "args": ["-y", "@opengem/mcp"],            │
   │        "env": {                                   │
   │          "OPENGEM_API_KEY": "og_xxx"               │
   │        }                                          │
   │      }                                            │
   │    }                                              │
   │  }                                                │
   │  ```                                              │
   │                                                  │
   │  ## Step 2: Restart Claude                       │
   │                                                  │
   │  ## Step 3: Try it                                │
   │  Ask Claude: "What's OPENGEM's latest US CPI    │
   │  forecast?"                                       │
   │                                                  │
   │  [ Copy snippet ] [ Open install doc → ]         │
   │                                                  │
   └────────────────────────────────────────────────┘
```

## Per-host install snippets

### Claude Desktop

```json
{
  "mcpServers": {
    "opengem": {
      "command": "npx",
      "args": ["-y", "@opengem/mcp"],
      "env": {
        "OPENGEM_API_KEY": "og_xxx"
      }
    }
  }
}
```

Config path:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

### ChatGPT Pro / Custom GPT

ChatGPT Pro supports MCP via the "Connectors" tab. Walk the user through:

1. Open Settings → Connectors
2. Add custom MCP server
3. URL: `https://mcp.opengem.app/sse`
4. Auth: paste API key as Bearer token
5. Enable

### Cursor

```json
// .cursor/mcp.json (project) or ~/.cursor/mcp.json (global)
{
  "mcpServers": {
    "opengem": {
      "command": "npx",
      "args": ["-y", "@opengem/mcp"],
      "env": {
        "OPENGEM_API_KEY": "og_xxx"
      }
    }
  }
}
```

### Cline (VS Code)

```json
// .vscode/cline.config.json
{
  "mcpServers": {
    "opengem": {
      "command": "npx",
      "args": ["-y", "@opengem/mcp"],
      "env": {
        "OPENGEM_API_KEY": "og_xxx"
      }
    }
  }
}
```

### Continue.dev

```yaml
# ~/.continue/config.yaml
mcpServers:
  - name: opengem
    command: npx
    args: ["-y", "@opengem/mcp"]
    env:
      OPENGEM_API_KEY: og_xxx
```

### Aider

```bash
aider --mcp opengem=npx,-y,@opengem/mcp
```

### Generic stdio

```bash
npx -y @opengem/mcp
```

Or, for SSE (hosted):

```
https://mcp.opengem.app/sse
Bearer: og_xxx
```

## The tools exposed by the MCP server

```
   ┌────────────────────────────────────────────────┐
   │  Tools exposed                                    │
   │  ────────────────────                            │
   │                                                  │
   │  Indicator                                        │
   │   • indicator.list (filter by country, etc.)    │
   │   • indicator.get (single)                        │
   │   • indicator.series (time series)                │
   │                                                  │
   │  Country                                          │
   │   • country.get                                   │
   │   • country.snapshot (4 KPI summary)              │
   │                                                  │
   │  Forecast                                         │
   │   • forecast.list                                 │
   │   • forecast.get                                  │
   │   • forecast.diff (vintage A vs B)                │
   │                                                  │
   │  Scenario                                         │
   │   • scenario.list                                 │
   │   • scenario.get                                  │
   │                                                  │
   │  Accountability                                   │
   │   • accountability.summary                        │
   │   • accountability.misses (recent)                │
   │   • accountability.score                          │
   │                                                  │
   │  News & feed                                      │
   │   • feed.top_of_mind                              │
   │   • news.search                                   │
   │                                                  │
   │  Search                                           │
   │   • search.universal (BM25 across all entities)  │
   │                                                  │
   │  Methodology & glossary                          │
   │   • methodology.summary                          │
   │   • methodology.full                              │
   │   • glossary.lookup                              │
   │                                                  │
   │  Cite                                             │
   │   • cite.lookup                                   │
   │   • cite.list                                     │
   │                                                  │
   │  Resources (read-only)                            │
   │   • resource://opengem/indicator/<id>            │
   │   • resource://opengem/country/<iso3>            │
   │   • resource://opengem/forecast/<id>             │
   │                                                  │
   └────────────────────────────────────────────────┘
```

Documented in OpenAPI at `/api/v1/openapi.json` and MCP capability negotiation.

## The "try it" prompts

A section showing what to ask:

```
   Try these prompts:

   • "What's the latest US CPI year-over-year and
      OPENGEM's nowcast?"
   • "Compare Germany and France GDP growth in 2025."
   • "What's OPENGEM's track record on EUR inflation
      forecasts?"
   • "Show me the top 10 most surprising data prints
      this week globally."
   • "Walk me through OPENGEM's recession-probability
      methodology for the US."
   • "Generate a markdown summary of OPENGEM's
      Q1 2026 retrospective."
```

These work out of the box once the server is connected.

## Auth via dynamic-client-registration

For hosts that support DCR (ChatGPT Custom GPT, future Claude integrations), the MCP server supports OAuth 2.0 with:
- Client registration endpoint: `/oauth/register`
- Authorization endpoint: `/oauth/authorize`
- Token endpoint: `/oauth/token`

This means: a user enables OPENGEM in their ChatGPT, gets bounced to an OPENGEM consent page, clicks "Allow," and is back in chat with the server installed.

V1: API-key flow (simpler). V2: full OAuth + DCR.

## The "no key required" path

Anonymous tier MCP works without a key — limited rate. The server transparently uses the IP-derived rate bucket. Useful for users trying it out.

```json
{
  "mcpServers": {
    "opengem": {
      "command": "npx",
      "args": ["-y", "@opengem/mcp"]
    }
  }
}
```

No `env` block needed for the free anonymous tier.

## "Update OPENGEM" affordance

When `@opengem/mcp` has a new release:
- The MCP server announces a "OPENGEM has been updated" notification to the host
- The host prompts the user to `npm i -g @opengem/mcp@latest`
- Or, if they're using `npx`, it's automatic (npx pulls latest)

## Testing tool

A small section: "Test your install"

```
   curl -X POST https://mcp.opengem.app/test \
     -H "Authorization: Bearer og_xxx" \
     -d '{"tool": "indicator.get", "args": {"id": "cpi-yoy"}}'
```

Returns 200 with sample data if the key is valid.

## The "show me what's installed" command

In a chat, the user asks the LLM:

```
   User: "What OPENGEM tools do you have access to?"
   LLM:  "I have these OPENGEM tools available: ..."
         [lists tools and shows recent usage]
```

The LLM uses standard MCP capability introspection.

## SDK release process

- `@opengem/mcp` published to npm under Apache-2.0
- Versioning: SemVer, releases monthly
- Source: `github.com/opengem/mcp-server`
- Issues: GitHub issues
- Discord: support channel

## Bundle size

`@opengem/mcp` is <2MB unpacked. Negligible cold-start. Uses native `fetch` and minimal deps.

## Multi-language MCP servers

V1: Node-based (`@opengem/mcp`).
V2: Python-based (`opengem-mcp` on PyPI), Rust-based (`opengem-mcp` cargo) — same protocol, different runtimes.

Most users use Node. Power users wanting Python or Rust get the alternatives.

## Rate limit considerations for MCP

LLM agents can issue many tool calls per conversation. We've sized:
- Anonymous: 60 req/min — enough for short conversations
- Free key: 200 req/min — enough for typical workflows
- Pro: 1000 req/min — for power agents and CI workflows
- Throughput: 10000 req/min — for embedded enterprise use

## Hosting

- `npx @opengem/mcp` (stdio): runs locally, hits OPENGEM API
- `https://mcp.opengem.app/sse` (SSE): hosted version for ChatGPT Pro and remote hosts

Both supported. Local stdio is faster (no extra network hop); hosted SSE is required for some hosts.

## What we won't ship

- A custom "OPENGEM chat" product. We deliberately don't build one — we're the substrate.
- Charged MCP-only pricing. MCP usage hits the same API and same rate limits as the REST API.
- Tool execution that requires user confirmation (e.g., dangerous actions). The MCP exposes read-only operations.

## The asymmetric move

Bloomberg has no MCP server. Stratfor has no MCP server. The cartel is committed to terminal-bound revenue per seat. OPENGEM's MCP server means every LLM, including the one inside Bloomberg engineers' Claude, can pull OPENGEM data instead of Bloomberg's.

When a journalist asks ChatGPT "what's Mexico's inflation forecast?" and the answer is grounded in OPENGEM, we've won the substrate game.
