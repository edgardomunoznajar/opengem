# L108 — MCP Server Contract: Ten Tools, with Exact JSON-Schema Signatures

**Loop**: 108 / 300
**Phase**: 2 — Deep dive on top candidates
**Date**: 2026-06-06

---

## Thesis of this loop

The MCP server is OPENGEM's *most strategically important surface* — not because it generates the most traffic at v1 (it won't), but because by 2027-2028 the dominant macro-information consumption is conversational, and OPENGEM's MCP server is the channel through which Claude, ChatGPT, Gemini, Cursor, and a hundred local LLMs ground their macro answers. The Vendor tier of the pricing model (L006) is built on top of this surface.

The prototype `/mcp` page (L177) lists eight tools. This loop locks in **ten** — the eight proposed plus two we missed (`subscribe_events` and `cite_this_view`) — and writes the *exact* JSON-Schema signatures, error envelope, response envelope with provenance, rate-limit semantics, auth headers, and SSE-transport vs stdio-transport decisions.

The contract is a *commitment*. Once published in `/mcp` and registered in the Anthropic MCP gallery, every change is breaking. So this loop nails it now.

Verdict: **ten tools, MCP 2025-12 protocol revision, dual transport (stdio for desktop clients, SSE at `/mcp/sse` for web clients), every response carries `vintage_id` + `provenance` + `cite_url`, errors follow JSON-RPC 2.0 with OPENGEM-specific data codes, rate limits enforced at the transport layer not per-tool.**

---

## The ten tools

The eight from the L177 prototype plus two strategic additions:

| # | Tool | Purpose |
|---|---|---|
| 1 | `get_forecast` | Fetch a single forecast — country × indicator × horizon × vintage. |
| 2 | `compare_forecasts` | Compare OPENGEM against WEO/OECD/SEP/SPF consensus. |
| 3 | `list_scenarios` | Currently-triggered scenarios with probabilities. |
| 4 | `get_recession_probability` | Bauer-Mertens 12m probability per Tier-V country. |
| 5 | `get_gpr_nowcast` | Caldara-Iacoviello GPR — global or per-country. |
| 6 | `rewind_vintage` | Replay any historical vintage. |
| 7 | `get_leaderboard` | Forecast leaderboard per indicator × horizon. |
| 8 | `list_misses` | Recent forecast misses with post-mortem URLs. |
| **9** | **`subscribe_events`** | **Long-lived SSE-style stream of new ticker events (NEW)** |
| **10** | **`cite_this_view`** | **Generate a stable citation string for any OPENGEM URL (NEW)** |

The two additions matter:

- `subscribe_events` makes OPENGEM a *first-class real-time citizen* inside an LLM session. The user can ask "tell me when something material happens in EM debt markets" and the assistant subscribes once; the conversation gets updates without the user re-asking.
- `cite_this_view` is the *brand reinforcer*. Every time an LLM uses an OPENGEM fact, it should produce a citation string ("OPENGEM 2026-06-06: USA CPI YoY 3.2%, https://opengem.org/cite/...") — and now the LLM has a single tool to call that *guarantees* the citation has the right format and a permanent URL.

---

## The shared response envelope

Every tool returns an object shaped like:

```json
{
  "data": { /* tool-specific payload */ },
  "vintage_id": "2026-06-06T00:00:00Z",
  "provenance": {
    "model": "cf_nowcast_v3.1",
    "model_card_url": "https://opengem.org/methodology/cf-nowcast-v3",
    "inputs": ["fred:CPIAUCSL", "bls:CPIAUCSL"],
    "generated_at": "2026-06-06T13:42:11Z",
    "code_version": "git+a3f2b8e",
    "license": "CC-BY-4.0"
  },
  "cite_url": "https://opengem.org/cite/USA-cpi_yoy-2026-06-06",
  "rate_limit": {
    "limit": 100,
    "remaining": 97,
    "reset_at": "2026-06-07T00:00:00Z"
  }
}
```

This shape is hard-required for every response, every tool. The LLM consuming the response *cannot* miss the provenance — it's right there next to the data.

---

## The signatures (JSON-Schema)

### 1. `get_forecast`

```json
{
  "name": "get_forecast",
  "description": "Fetch a single OPENGEM forecast — country × indicator × horizon × vintage. Returns the point forecast, band quantiles (P10/P50/P90), the methodology pointer, and full provenance.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "country": { "type": "string", "pattern": "^[A-Z]{3}$", "description": "ISO-3 country code (e.g. 'USA', 'BRA')" },
      "indicator": { "type": "string", "enum": ["cpi_yoy", "gdp_yoy", "unemployment", "policy_rate", "trade_balance", "..."] },
      "horizon": { "type": "string", "enum": ["nowcast", "1q", "4q", "2y", "5y"] },
      "vintage": { "type": "string", "format": "date", "description": "ISO 8601 date (e.g. '2026-06-06'). Default: latest." }
    },
    "required": ["country", "indicator", "horizon"]
  }
}
```

### 2. `compare_forecasts`

```json
{
  "name": "compare_forecasts",
  "description": "Compare OPENGEM's forecast for a country × indicator × horizon against named consensus sources (WEO, OECD EO, FRB SEP, ECB SPF, Bloomberg consensus if available). Returns each source's point + band + last-updated date.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "country": { "type": "string", "pattern": "^[A-Z]{3}$" },
      "indicator": { "type": "string" },
      "horizon": { "type": "string", "enum": ["nowcast", "1q", "4q", "2y", "5y"] },
      "sources": {
        "type": "array",
        "items": { "type": "string", "enum": ["opengem", "weo", "oecd_eo", "frb_sep", "ecb_spf", "bloomberg_consensus"] },
        "default": ["opengem", "weo", "oecd_eo"]
      }
    },
    "required": ["country", "indicator", "horizon"]
  }
}
```

### 3. `list_scenarios`

```json
{
  "name": "list_scenarios",
  "description": "List currently-triggered OPENGEM scenarios, each with its probability, the date triggered, affected countries, and a link to its methodology.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "active_only": { "type": "boolean", "default": true },
      "country": { "type": "string", "pattern": "^[A-Z]{3}$", "description": "Filter to scenarios affecting this country" },
      "min_probability": { "type": "number", "minimum": 0, "maximum": 1, "default": 0.05 }
    }
  }
}
```

### 4. `get_recession_probability`

```json
{
  "name": "get_recession_probability",
  "description": "12-month recession probability for a Tier-V country, per the Bauer-Mertens (2018) probit model on the 10Y-3M Treasury spread, with cross-country pooling. Returns the probability, the spread input, and the comparison to last vintage.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "country": { "type": "string", "pattern": "^[A-Z]{3}$" },
      "vintage": { "type": "string", "format": "date" }
    },
    "required": ["country"]
  }
}
```

### 5. `get_gpr_nowcast`

```json
{
  "name": "get_gpr_nowcast",
  "description": "Caldara-Iacoviello GPR (Geopolitical Risk) nowcast. Global series if no country given; country-specific series for one of the 44 Caldara-Iacoviello countries if provided.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "country": { "type": "string", "pattern": "^[A-Z]{3}$" },
      "window": { "type": "string", "enum": ["daily", "monthly"], "default": "monthly" }
    }
  }
}
```

### 6. `rewind_vintage`

```json
{
  "name": "rewind_vintage",
  "description": "Replay any historical OPENGEM forecast at any prior vintage date. Returns the forecast object exactly as it was published at that vintage — no retrospective revision.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "country": { "type": "string", "pattern": "^[A-Z]{3}$" },
      "indicator": { "type": "string" },
      "horizon": { "type": "string", "enum": ["nowcast", "1q", "4q", "2y", "5y"] },
      "vintage": { "type": "string", "format": "date", "description": "REQUIRED — vintage to replay" }
    },
    "required": ["country", "indicator", "horizon", "vintage"]
  }
}
```

### 7. `get_leaderboard`

```json
{
  "name": "get_leaderboard",
  "description": "Forecast leaderboard for an indicator × horizon, CRPS-ranked across all tracked sources (OPENGEM, WEO, OECD, etc.) over a configurable lookback.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "indicator": { "type": "string" },
      "horizon": { "type": "string", "enum": ["nowcast", "1q", "4q", "2y", "5y"] },
      "lookback_quarters": { "type": "integer", "minimum": 1, "maximum": 40, "default": 8 },
      "country_set": { "type": "string", "enum": ["g7", "g20", "tier_v", "all"], "default": "tier_v" }
    },
    "required": ["indicator", "horizon"]
  }
}
```

### 8. `list_misses`

```json
{
  "name": "list_misses",
  "description": "Recent forecast misses from the accountability ledger, with post-mortem URLs. Honesty surface — for LLMs to cite when reporting on OPENGEM's track record.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "since": { "type": "string", "format": "date" },
      "indicator": { "type": "string" },
      "country": { "type": "string", "pattern": "^[A-Z]{3}$" },
      "min_severity": { "type": "string", "enum": ["low", "medium", "high"], "default": "low" }
    }
  }
}
```

### 9. `subscribe_events`

```json
{
  "name": "subscribe_events",
  "description": "Subscribe to a stream of new OPENGEM ticker events — forecast revisions, scenario triggers, event bursts, miss logs. Streamed via SSE in the response; client receives one event per data chunk. Subscription ends when the client disconnects.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "kinds": {
        "type": "array",
        "items": { "type": "string", "enum": ["indicator_update", "forecast_revision", "scenario_trigger", "event_burst", "miss_logged"] }
      },
      "countries": { "type": "array", "items": { "type": "string", "pattern": "^[A-Z]{3}$" } },
      "indicators": { "type": "array", "items": { "type": "string" } },
      "since": { "type": "string", "description": "ULID to resume from (optional)" }
    }
  }
}
```

### 10. `cite_this_view`

```json
{
  "name": "cite_this_view",
  "description": "Generate a stable, permanent citation string for any OPENGEM URL or forecast/indicator/country/scenario reference. Returns APA, MLA, BibTeX, and a structured Citation object.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "url": { "type": "string", "format": "uri", "description": "Any opengem.org URL — preferred input" },
      "country": { "type": "string", "pattern": "^[A-Z]{3}$" },
      "indicator": { "type": "string" },
      "vintage": { "type": "string", "format": "date" },
      "formats": {
        "type": "array",
        "items": { "type": "string", "enum": ["apa", "mla", "bibtex", "structured"] },
        "default": ["apa", "structured"]
      }
    }
  }
}
```

---

## Transport: dual stdio + SSE

- **stdio transport** (desktop clients: Claude Desktop, Cursor, VS Code/Continue) — `@opengem/mcp-server` npm package launches a Node.js process that speaks JSON-RPC over stdin/stdout. Authentication is via `OPENGEM_API_KEY` env var.

- **SSE transport** (web clients: ChatGPT Connectors, Gemini Extensions, custom LLM apps) — at `https://opengem.org/mcp/sse`. The client makes a GET with `Authorization: Bearer <key>`, receives a session-id, then POSTs tool invocations to `/mcp/messages?session=<id>` and reads streamed responses via the SSE channel.

Both transports use the *same* tool implementations behind a transport abstraction. No tool reimplementation per transport.

---

## Errors: JSON-RPC 2.0 with OPENGEM data codes

```json
{
  "jsonrpc": "2.0",
  "id": "..." ,
  "error": {
    "code": -32001,
    "message": "Indicator not available for country",
    "data": {
      "opengem_code": "indicator_not_covered",
      "country": "TUV",
      "indicator": "policy_rate",
      "suggestion": "Try 'central_bank_rate' or omit indicator for coverage list",
      "coverage_url": "https://opengem.org/coverage/TUV"
    }
  }
}
```

OPENGEM-specific codes: `indicator_not_covered`, `vintage_out_of_range`, `country_unsupported`, `rate_limit_exceeded`, `auth_required_for_paid_indicator`, `internal_error_with_post_mortem_url`.

---

## Rate limits at the transport layer

Per-tool quotas would be opaque to LLMs (they'd hit a limit on one tool and not understand they could call another). Instead: a single per-session quota: **100 tool calls / day / IP (free tier)**, **10,000 / day / key (Studio tier)**, **100,000 / day / key (Newsroom)**, **1,000,000 / day / key (Institutional)**, custom (Vendor).

The `rate_limit` object in every response shows the current state, so the LLM can pace itself.

---

## Next-step: the FastMCP skeleton

```python
# mcp/server.py
from fastmcp import FastMCP, Tool
from pydantic import BaseModel, Field
from typing import Literal

mcp = FastMCP("OPENGEM", "1.0.0")

class ForecastResult(BaseModel):
    point: float
    band: dict
    vintage_id: str
    provenance: dict
    cite_url: str

@mcp.tool()
async def get_forecast(
    country: str = Field(..., pattern="^[A-Z]{3}$"),
    indicator: str = Field(...),
    horizon: Literal["nowcast", "1q", "4q", "2y", "5y"] = "nowcast",
    vintage: str | None = None,
) -> ForecastResult:
    """Fetch a single OPENGEM forecast..."""
    row = await fetch_forecast_row(country, indicator, horizon, vintage)
    return ForecastResult(
        point=row.point,
        band={"p10": row.p10, "p50": row.p50, "p90": row.p90},
        vintage_id=row.vintage_id,
        provenance=row.provenance,
        cite_url=f"https://opengem.org/cite/{country}-{indicator}-{row.vintage_id}",
    )

if __name__ == "__main__":
    mcp.run()
```

---

## What this loop produced

- A locked-in ten-tool contract (eight prototyped + two strategic additions).
- Exact JSON-Schema signatures for each tool.
- A shared response envelope guaranteeing `vintage_id` + `provenance` + `cite_url`.
- Dual stdio + SSE transport design.
- JSON-RPC 2.0 error format with OPENGEM data codes.
- Transport-layer rate limits.
- A FastMCP skeleton ready for the prototype.

## What comes next

- **L177** — MCP-server install page UI design pairs with this.
- **L249** — OpenAPI spec for the REST surface mirrors these signatures.
- **L250** — MCP server prototype implementation.

## Related

- [[L006-pricing-thesis]] — Vendor tier is built on this surface
- [[L177-mcp-server-install-page]] — the UI for adopting this MCP
- [[L249-openapi-spec]] — REST analog of these schemas
- [[L103-fastapi-websocket]] — `subscribe_events` consumes the SSE stream
- [[L158-cite-this-view]] — `cite_this_view` reuses the citation generator
