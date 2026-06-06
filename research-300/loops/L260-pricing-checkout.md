# L260 — Pricing page + checkout

**Loop**: 260 / 300
**Phase**: 5 — Code prototypes
**Date**: 2026-06-06
**Artifact**: `prototypes/dashboard-next/app/pricing/page.tsx` (UI), `app/mcp/page.tsx` (MCP install)

---

## What was built

Four-tier pricing page with:

| Tier | Price | Critical line |
|---|---|---|
| **Public** | Free forever | "It's already running" |
| **Pro** | $29/mo | 1000 req/min API + 100k MCP/day + white-label embeds |
| **Pro Team** | $149/mo, 10 seats | 10k req/min + SSO + Slack/Teams + priority support |
| **Sovereign/Enterprise** | from $2k/mo | On-prem deploy + custom adapters + audit trail |

## The pricing philosophy (the "Never charge for X" block)

We charge for **velocity and fit**, never **substance**. That block is on the pricing page itself, not buried in a FAQ:

- The full forecast track record. **Free.**
- Reading any historical vintage. **Free.**
- Reading the miss log. **Free.**
- Reading the methodology. **Free.**
- Forking the codebase. **Apache-2.0.**
- Republishing derived metrics. **CC-BY-4.0.**

This is the answer to "what's the catch?" — and it's on the pricing page in the same visual weight as the tier comparison. Bloomberg's pricing page hides cost; OPENGEM's pricing page hides nothing.

## Checkout

Marked as `/checkout?plan=pro` — Stripe Checkout sessions with test-mode keys for the prototype. Three-step flow:

1. Email + role tag (the L139 onboarding flow)
2. Stripe Checkout (card / Apple Pay / Google Pay)
3. Confirmation + API key reveal + MCP server snippet

In v0.x: a single-page Stripe Element. In v1.x: Apple/Google Pay; SSO for Team tier; in v2.x: invoicing for Sovereign tier with NET-30.

## Unit economics (quick check)

- COGS: ~$0.03/user/month at Pro tier (Cloud Run + R2 + AI usage) — *Estimate; revisit with [oblique-accountant](https://opengem.org/methodology/cloud-costs).*
- Gross margin at $29/mo: ~99% (within the noise of payment processing).
- The constraint isn't COGS — it's the *honest* throughput we promise. 100k MCP calls/day is meaningful for an LLM-grounding workflow.
- Pro tier ARR target Y1: 30 paying users × $290/yr = $8.7k. Pro Team: 5 teams × $1490/yr = $7.5k. Sovereign: 1 × $24k = $24k. Total: ~$40k MRR-equivalent. Not a real business; that's fine — it pays the cloud bill and validates the model.
- Pro tier ARR target Y3: 500 × $290 = $145k + Team 30 × $1490 = $45k + Sovereign 5 × $24k = $120k = $310k ARR. Now it's a guerrilla-developer salary.
- Pro tier ARR target Y5: 5000 × $290 + Team 200 × $1490 + Sovereign 25 × $50k = $1.45M + $298k + $1.25M = ~$3M ARR.

## Companion: MCP install page (`app/mcp/page.tsx`)

Adjacent to pricing, but separate URL. Contains:

- Install snippets for Claude Desktop, Cursor, ChatGPT, VS Code
- The 8 tools exposed (get_forecast, compare_forecasts, list_scenarios, get_recession_probability, get_gpr_nowcast, rewind_vintage, get_leaderboard, list_misses)
- "The MCP guarantee" — every tool response includes vintage_id and provenance

This is the single most important monetization page because **the MCP tier is where the ARPU is** in a world of LLM-grounding workflows. Bloomberg charges $2k/seat/month because its terminal is the data interface. OPENGEM charges $29/mo because the *user's* LLM is the data interface — we just expose tools.

## What this loop produced

- `app/pricing/page.tsx` — four-tier pricing UI
- `app/mcp/page.tsx` — MCP install / tools / guarantee page
- The "what we never charge for" public commitment

## What comes next

- L261 — Onboarding flow prototype (3-step: email + role + watchlist)
- L262 — Dark/light theme toggle
- L109 — Stripe + magic-link gating implementation

## Related

- [[L006-pricing-thesis]] — the strategy
- [[L138-pricing-page]] — the design spec
- [[L177-mcp-server-install-page]] — design spec for MCP page
- [[L108-mcp-server-contract]] — the tools exposed
- [[L008-differentiation]] — what we never charge for
