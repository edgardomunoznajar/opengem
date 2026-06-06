# L241 — Live news feed prototype

**Loop**: 241 / 300
**Phase**: 5 — Code prototypes
**Date**: 2026-06-06
**Artifact**: `prototypes/dashboard-next/app/events/page.tsx`

---

## What was built

`/events` page showing a chronological stream of macro + geopolitical events with attribution to source + an explicit "→ why this matters" line ("Triggers US recession scenario probability ↑ to 34%").

Header includes Atom + RSS pills so power users can subscribe directly.

## Event card structure

Each card surfaces:

- **Timestamp** (UTC, mono, minute-precision)
- **Severity pill** (high / medium / low — pill colored bad / warn / info)
- **Tag pill** (geopolitics / central-bank / macro-print / energy / …)
- **Source** (e.g. "via GDELT GKG" — link-out)
- **Headline** (sm body text)
- **"→ why" line** in italic ink-muted — the editorial connection to OPENGEM's forecasts and scenarios
- **Affected countries** as clickable flag+ISO3 chips routing to country pages

## Editorial discipline

The "→ why" line is the entire editorial product. Without it, this page is just another news ticker — and there are 1000 of those. With it, each event becomes a link in the chain "X happened → Y nowcast changed → scenario Z probability moved." That chain is the value.

## Source mix

| Source class | Examples | Tag |
|---|---|---|
| Agency releases | BLS CPI, BEA NIPA, Census M3 | macro-print |
| Central banks | FOMC minutes, ECB statements, BoE press conference | central-bank |
| Geopolitical events | GDELT GKG (Goldstein-Scale weighted), POLECAT | geopolitics |
| Market data | Brent, FX, yield curves | energy / fx / rates |
| Sanctions / OFAC | OpenSanctions diff (NC tier) | sanctions |

## Distribution

The events page is RSS + Atom first-class. We expect:
- macroeconomics Substacks to subscribe
- Macro Reddit communities to follow the RSS
- LLM agents (via MCP) to subscribe via `/v1/stream` WebSocket for live events
- A daily digest email that bundles the day's high-severity events with the resulting forecast moves

## Implementation notes

- Prototype uses hand-curated event fixtures.
- Production source: opengem-event-detector pkg (already in repo) → events table → REST `/v1/events` + WebSocket `/v1/stream`.
- Severity classification: rule-engine driven (impact-score thresholds), not LLM-driven.
- Dedup logic: GDELT-derived events are clustered by URL canonicalization + event-kind + 30-minute window.

## What this loop produced

- Working `/events` page with curated event cards
- The "→ why" editorial discipline made visible
- Atom + RSS distribution surface in the header

## What comes next

- L114 — Discord/Telegram bot for alerts (consumes events stream)
- L127 — Event/news stream page design (sibling spec)
- L170 — Top-of-mind feed (ranked variant on home page)

## Related

- [[L127-event-news-stream-page]] — design spec
- [[L170-top-of-mind-feed]] — ranked variant on home
- [[L106-rss-atom-feeds]] — distribution channel design
- [[L008-differentiation]] — editorial discipline as moat
- [[L021-gdelt-gkg]] — primary geopolitical source
- [[L025-cline-center]] — POLECAT secondary source
