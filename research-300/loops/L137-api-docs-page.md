---
loop: 137
phase: 3
title: API Docs Page — Framework Selection
date: 2026-06-06
status: decided
---

# L137 — API Docs Page (OpenAPI + MCP)

**Loop**: 137 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design `/docs`. Pick the documentation framework — Scalar? Redoc? Stainless? Mintlify? Hand-rolled? Pick one. Argue.

The /docs surface must cover three things:
1. **OpenAPI** for the REST surface (Spring Boot, per existing repo).
2. **MCP** for the chat-grounding surface (opengem-mcp, planned).
3. **SDK / client libraries** in Python, TypeScript, R (Block II target).

The framework must support live, interactive testing. It must support code samples in multiple languages. It must support deep-linking to specific endpoints. It must not look like generic Swagger output.

## Candidates considered

### Scalar (scalar.com / @scalar/api-reference)

Strengths:
- Modern UI inspired by Stripe docs. Clean. Branded.
- Open source. Self-hostable.
- Built on standard OpenAPI 3.1.
- Three-pane layout (nav + content + try-it).
- Free.

Weaknesses:
- Newer (less battle-tested than Redoc).
- Themeability is decent but not as deep as a hand-rolled solution.
- MCP integration would be custom.

### Redoc (redocly.com)

Strengths:
- Battle-tested. Industry standard for OpenAPI rendering.
- Three-pane layout.
- Strong typography.
- Free OSS version, hosted Pro for richer features.

Weaknesses:
- Aesthetics feel a bit dated (very Redoc-y).
- Try-it-now requires Pro tier or Postman embed.
- MCP integration custom.

### Stainless

Strengths:
- Generates SDK code in multiple languages from OpenAPI spec.
- High quality SDK output (used by Anthropic, Cloudflare, Cresta, …).
- API reference is generated alongside SDKs.

Weaknesses:
- Closed-source SaaS. Pricing scales with revenue.
- We need to host docs ourselves; Stainless is more SDK-focused.
- MCP not natively supported.

### Mintlify

Strengths:
- Premium-feeling docs UI. Widely used (Anthropic, Honcho, Resend, …).
- Strong code-sample story.
- Good navigation.

Weaknesses:
- Closed-source. Hosted SaaS.
- Less control over output.
- Pricing.
- MCP not native.

### Hand-rolled (Next.js + MDX)

Strengths:
- Maximum control over branding, layout, voice.
- Native integration with the OPENGEM site (same Next.js codebase, same components, same theme).
- MCP docs can be first-class, not bolted on.
- No external dependency.

Weaknesses:
- Reinvents OpenAPI rendering.
- More maintenance.
- Risk of slow start (Phase 5 prototype effort).

## The decision — Scalar (REST) + hand-rolled MCP shell, integrated under one Next.js app

**Pick Scalar for the OpenAPI surface.** Embed it as a React component into the OPENGEM Next.js app. Use the Scalar component's theming hooks to match the OPENGEM terminal-orange theme (per L145). For the MCP and SDK sections, hand-roll under `/docs/mcp` and `/docs/sdks` using the same Next.js + MDX setup as the marketing site.

This is the hybrid: leverage Scalar's mature OpenAPI rendering for the REST docs, control everything else.

Why this and not pure Scalar:

- **MCP is a first-class surface for OPENGEM.** The MCP server is co-equal with the REST API. Scalar does not yet have native MCP docs rendering; hand-rolling MCP docs lets us showcase tools, prompts, resources, and example invocations in a custom layout.
- **SDK docs need code-sample richness.** A hand-rolled MDX surface can embed runnable Python / TypeScript / R examples with the OPENGEM theme.

Why this and not pure hand-rolled:

- **Reinventing OpenAPI rendering is expensive and low-value.** Scalar already does try-it-now, schema rendering, auth flows, code-sample generation across ~15 languages. Building this in MDX would burn weeks.

Why this and not Stainless / Mintlify:

- **Pricing.** Both scale with revenue / seats / page views. At v1 launch we are pre-revenue and need predictable cost.
- **Self-host requirement.** OPENGEM's deployment story (Cloudflare Pages + Workers) does not need external doc hosting.
- **Open-source commitment.** Stainless and Mintlify are closed-source; Scalar is OSS.

## The page structure

```
+--------------------------------------------------------------------------+
| OPENGEM > Docs                                                           |
| /docs                                                                    |
+--------------------------------------------------------------------------+
| LEFT NAV                          | CONTENT                              |
|                                    |                                      |
| Introduction                       | OPENGEM API                           |
| Authentication                     |                                      |
| Rate limits                        | The OPENGEM public API gives you      |
| Error handling                     | machine-readable access to every     |
| Versioning                         | forecast, indicator, scenario, and  |
|                                    | ledger cell on the dashboard.        |
| REST API (Scalar)                  |                                      |
|   ▸ /v1/forecasts                  | Three surfaces:                       |
|   ▸ /v1/indicators                 |  1. REST (OpenAPI 3.1)                |
|   ▸ /v1/scenarios                  |  2. MCP server                        |
|   ▸ /v1/countries                  |  3. SDK clients                       |
|   ▸ /v1/events                     |                                      |
|   ▸ /v1/ledger                     | All three serve the same data via    |
|   ▸ /v1/recession-probability      | different transports.                 |
|   ▸ /v1/gpr-nowcast                |                                      |
|                                    | [Try the API now → playground]        |
| MCP Server                         |                                      |
|   ▸ Install                        |                                      |
|   ▸ Tools                          |                                      |
|   ▸ Resources                      |                                      |
|   ▸ Prompts                        |                                      |
|   ▸ Examples                       |                                      |
|                                    |                                      |
| SDK Clients                        |                                      |
|   ▸ Python (opengem-py)            |                                      |
|   ▸ TypeScript (opengem-ts)        |                                      |
|   ▸ R (opengem-r) (Block II)       |                                      |
|   ▸ CLI                             |                                      |
|                                    |                                      |
| Recipes                            |                                      |
|   ▸ "World economy in 5 lines"     |                                      |
|   ▸ "Compare two forecasts"       |                                      |
|   ▸ "Subscribe to scenario fires"  |                                      |
|   ▸ "Replay a forecast"            |                                      |
|   ▸ "Build a watchlist via API"   |                                      |
|                                    |                                      |
| Reference                          |                                      |
|   ▸ Glossary                        |                                      |
|   ▸ Indicator catalog               |                                      |
|   ▸ Country catalog                 |                                      |
|   ▸ Scenario catalog                |                                      |
|   ▸ License                         |                                      |
+------------------------------------+--------------------------------------+
```

## REST API section (Scalar-rendered)

Each endpoint renders via Scalar with:
- Path, method, summary.
- Request schema (auto-generated from OpenAPI spec).
- Response schema with examples.
- Code samples in: curl, Python (requests), Python (opengem-py SDK), TypeScript (fetch), TypeScript (opengem-ts SDK), R (httr), Go, Rust.
- Try-it-now playground (calls the live API; requires sign-in for auth-required endpoints; free endpoints have anonymous-friendly playground).

Auth section explains:
- Anonymous access (rate-limited).
- API tokens (free tier: 1000 req/day; pro: 100k req/day; team: 1M req/day).
- Token management at `/settings/tokens`.

Error handling section enumerates error codes with semantic causes:
- `400 BadRequest` — schema validation error.
- `401 Unauthorized` — missing or invalid token.
- `403 RateLimited` — exceeded tier limit.
- `404 NotFound` — record does not exist (often a vintage that has not been published yet).
- `410 Gone` — record was withdrawn (rare; cite the vintage diff for the reason).
- `503 Stale` — adapter for this data source is degraded; data is older than SLA.

Versioning section:
- `v1` is the current major version.
- New endpoints can ship without major-version bump.
- Breaking changes only on major-version bump.
- Deprecation policy: minimum 6 months between deprecation announcement and removal.
- Per-endpoint version pinning: clients can use `Opengem-API-Version: 2026-06-01` header for date-locked behavior.

## MCP section (hand-rolled)

```
+--------------------------------------------------------------------------+
| MCP Server                                                               |
+--------------------------------------------------------------------------+
| Install                                                                  |
|                                                                          |
| ChatGPT:                                                                 |
|   Settings → Connectors → Add MCP server                                |
|   URL: https://mcp.opengem.world/v1                                     |
|   [one-click install button]                                            |
|                                                                          |
| Claude Desktop:                                                         |
|   ~/.config/claude/mcp.json:                                            |
|     {"opengem": {"url": "https://mcp.opengem.world/v1"}}                |
|   [copy snippet]                                                        |
|                                                                          |
| Gemini, Mistral, local clients:                                         |
|   Use the standard MCP transport.                                       |
|   [client setup guides →]                                                |
+--------------------------------------------------------------------------+
| Tools                                                                    |
|                                                                          |
| opengem.country({iso3, indicator?, vintage?})                            |
|   Get country state with optional indicator filter.                     |
|                                                                          |
| opengem.forecast({indicator, country, horizon, vintage?})                |
|   Get a single forecast P10/P50/P90 + bands + miss log summary.       |
|                                                                          |
| opengem.scenarios.list({fired_only?, country?, vintage?})                |
|   List active or recent scenarios.                                       |
|                                                                          |
| opengem.scenario.detail({pack_id, vintage?})                             |
|   Full scenario state including affected countries and probability.    |
|                                                                          |
| opengem.compare({a, b, indicator?, horizon?, vintage?})                  |
|   Side-by-side comparison of two records.                                |
|                                                                          |
| opengem.events.recent({country?, severity?, since?, until?})            |
|   GDELT-driven event stream.                                            |
|                                                                          |
| opengem.recession_probability({country, vintage?})                       |
|   Bauer-Mertens probit output.                                          |
|                                                                          |
| opengem.gpr_nowcast({country?, vintage?})                                |
|   GPR Index reading and nowcast.                                        |
|                                                                          |
| opengem.ledger.cell({indicator, horizon, country?})                      |
|   Track-record cell with CRPS, PIT, miss log.                          |
|                                                                          |
| opengem.search({query, kind?, limit?})                                   |
|   Fuzzy search across records.                                          |
+--------------------------------------------------------------------------+
| Resources                                                                |
|                                                                          |
| opengem://schema.json                                                    |
|   Full OpenAPI 3.1 spec.                                                |
| opengem://indicators.json                                                |
|   Indicator catalog with definitions.                                   |
| opengem://countries.json                                                 |
|   Country catalog with ISO codes and groupings.                         |
| opengem://scenarios.json                                                 |
|   Scenario pack catalog with current state.                             |
| opengem://changelog.md                                                   |
|   Project changelog.                                                    |
+--------------------------------------------------------------------------+
| Prompts                                                                  |
|                                                                          |
| Pre-built prompts callable via the MCP server:                           |
|                                                                          |
| opengem.prompt.daily_briefing({country?})                                |
|   Returns a 3-paragraph analyst-grade briefing for a country / global.  |
|                                                                          |
| opengem.prompt.scenario_narrative({pack_id})                             |
|   Returns the auto-generated 3-paragraph narrative for a scenario.      |
|                                                                          |
| opengem.prompt.miss_postmortem({forecast_id, vintage})                   |
|   Returns a templated miss post-mortem.                                |
+--------------------------------------------------------------------------+
| Examples                                                                 |
|                                                                          |
| Tested with ChatGPT, Claude (Desktop + via API), Gemini, Mistral Le Chat.|
|                                                                          |
| ChatGPT: "Using OPENGEM, what is the recession probability for the US    |
|           and how has it changed since the start of the year?"          |
|                                                                          |
| Claude: "Using OPENGEM, compare the CPI forecasts for the US and the    |
|          EZ at 4Q ahead and explain the difference in 3 sentences."     |
|                                                                          |
| [See more examples →]                                                    |
+--------------------------------------------------------------------------+
```

## SDK section

Each SDK page covers:
- Install (pip / npm / cran / brew).
- Quickstart (5-line example).
- Auth setup.
- Core methods (mirror of MCP tools).
- Error handling.
- Pagination.
- Webhooks consumption (if applicable).
- Type definitions.

Python and TypeScript SDKs are generated from the OpenAPI spec via Stainless or hand-tuned. R is hand-rolled in Block II.

## Recipes section

Five canonical recipes, each as a single MDX page with copyable code:

1. **"World economy in 5 lines"** — fetch G7 forecasts and print to console.
2. **"Compare two forecasts"** — Compare-2 via API + render output.
3. **"Subscribe to scenario fires"** — webhook receiver in Python Flask.
4. **"Replay a forecast"** — call the replay-and-diff endpoint.
5. **"Build a watchlist via API"** — programmatic watchlist construction.

Recipes are tested in CI against the live API to prevent doc drift.

## Reference section

- **Glossary** — terms used across the dashboard (CRPS, PIT, vintage, …).
- **Indicator catalog** — every indicator we publish with definition + source.
- **Country catalog** — Tier-V vs Tier-T + groupings.
- **Scenario catalog** — every pack with one-line description and methodology link.
- **License** — Apache-2.0 + CC-BY-4.0 details.

## Interactive playground

The "try it now" feature uses Scalar's playground for REST. For MCP, we provide a `/docs/mcp/playground` page that uses a hosted MCP client to test tools in-browser.

The playground requires sign-in for any state-changing endpoint (which is rare in OPENGEM — most data is read-only).

## Search

Documents are indexed for site-wide search via Algolia DocSearch (free for open-source projects). Search results pre-filter by docs scope when the user is on `/docs`.

## Versioning the docs themselves

The docs are versioned alongside the API. `/docs/v1` is the current version; `/docs/v0` (pre-launch beta) is preserved. Each docs version is git-tagged.

## What this loop produced

- Framework decision: Scalar for REST docs, hand-rolled (Next.js + MDX) for MCP + SDK + recipes.
- All under one Next.js app, themed consistently with the main dashboard.
- 11 MCP tools enumerated (country, forecast, scenarios.list, scenario.detail, compare, events.recent, recession_probability, gpr_nowcast, ledger.cell, search).
- 5 MCP resources (schema, indicators, countries, scenarios, changelog).
- 3 pre-built MCP prompts (daily_briefing, scenario_narrative, miss_postmortem).
- 5 canonical recipes.
- Reference catalog (glossary + indicators + countries + scenarios + license).
- Algolia DocSearch for site search.
- API version pinning via header.

## What comes next

- **L177** designs the MCP-server install page (one-click prompt).
- **L138** designs the pricing page (tier limits referenced here).
- **L176** designs the API rate-limit and key UX.
- **L249** prototypes the OpenAPI spec.
- **L250** prototypes the MCP server.

## Related

- [[L121-information-architecture]] — /docs URL space
- [[L136-about-governance-changelog]] — links contribute/CONTRIBUTING.md
- [[L138-pricing-page]] — rate-limit tiers documented here
- [[L176-api-rate-limit-key-ux]] — token management
- [[L177-mcp-install-page]] — one-click MCP install
- [[L250-mcp-server-prototype]] — MCP server code
