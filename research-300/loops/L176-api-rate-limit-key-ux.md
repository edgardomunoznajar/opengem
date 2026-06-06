# L176 — Public-API Rate-Limit & Key UX

**Loop**: 176 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

The public API is the long-game distribution channel. A YouTuber making a video, a journalist embedding a chart, an LLM grounding its answer — all of them hit the API. The rate-limit + key UX must be frictionless for the prosumer and high-enough-throughput for the paying user.

## The four tiers

| Tier | Auth | Limits | Price |
|---|---|---|---|
| **Anonymous** | none | 60 req/min, 1000/day | free |
| **Free key** | email-verified | 200 req/min, 5000/day | free |
| **Pro** | paid | 1000 req/min, 50000/day | $99/mo |
| **Throughput** | paid | 10000 req/min, 1M/day | $499/mo |
| **Enterprise** | contracted | custom | custom |

Tiers gate by rate, not by data. Every endpoint is available to every tier.

## The "Get a key" page

`/api/key`:

```
   ┌────────────────────────────────────────────────┐
   │  Get an OPENGEM API key                          │
   │  ──────────────────────────────────────────    │
   │                                                  │
   │  Your free tier:                                  │
   │   • 200 requests / minute                         │
   │   • 5000 requests / day                           │
   │   • All endpoints                                 │
   │                                                  │
   │  No payment required. Verify your email.         │
   │                                                  │
   │  ┌────────────────────────────────────────┐    │
   │  │ Email: [________________________]      │    │
   │  └────────────────────────────────────────┘    │
   │                                                  │
   │  [ Send verification ]                           │
   │                                                  │
   │  ──────────────────────────────────────────    │
   │                                                  │
   │  Need more? See pricing →                        │
   │                                                  │
   └────────────────────────────────────────────────┘
```

Magic-link flow. No password. After verification:

```
   ┌────────────────────────────────────────────────┐
   │  Your API key                                    │
   │  ──────────────────────────────────────────    │
   │                                                  │
   │  og_4f2a8c9d7e1b3a6d2f8e1c4a7b3e9d8c             │
   │  [ Copy ] [ Rotate ] [ Delete ]                  │
   │                                                  │
   │  ⚠ Store this somewhere safe. It won't be       │
   │  shown again in full.                            │
   │                                                  │
   │  Quick start:                                    │
   │  curl -H "Authorization: Bearer og_4f2a8c9d..." \│
   │    https://opengem.app/api/v1/indicator/cpi-yoy  │
   │                                                  │
   │  [ Python ] [ TypeScript ] [ R ] [ curl ]        │
   │                                                  │
   │  ──────────────────────────────────────────    │
   │  Usage this month: 0 / 5000 requests             │
   └────────────────────────────────────────────────┘
```

## Per-language quick-start

Tabbed code snippets:

### curl
```
   curl -H "Authorization: Bearer og_xxx" \
     "https://opengem.app/api/v1/indicator/cpi-yoy?countries=usa"
```

### Python
```python
   import opengem
   og = opengem.Client(api_key="og_xxx")
   data = og.indicator("cpi-yoy", countries=["usa"])
```

### TypeScript
```typescript
   import { OpenGem } from "@opengem/sdk"
   const og = new OpenGem({ apiKey: "og_xxx" })
   const data = await og.indicator("cpi-yoy", { countries: ["usa"] })
```

### R
```r
   library(opengem)
   og <- opengem(api_key = "og_xxx")
   data <- og %>% indicator("cpi-yoy", countries = "usa")
```

## The dashboard

`/api/keys` (logged in):

```
   ┌────────────────────────────────────────────────┐
   │  API keys                                        │
   │  ──────────────────────────────────────────    │
   │                                                  │
   │  Active keys                                     │
   │  ────────────────                                │
   │  • Personal key                                  │
   │    og_4f2a...d8c (Pro tier)                     │
   │    Created 2026-04-12 · Last used 2 min ago     │
   │    [Rotate] [Delete]                             │
   │                                                  │
   │  • youtube-ben                                   │
   │    og_8a3b...e7f (Free tier)                    │
   │    Created 2026-05-22 · Last used 1 day ago     │
   │    [Rotate] [Delete]                             │
   │                                                  │
   │  [ + Create new key ]                            │
   │                                                  │
   │  ──────────────────────────────────────────    │
   │                                                  │
   │  USAGE (Personal key, this month)                │
   │  Requests:    23,456 / 1,500,000                 │
   │  Top endpoints:                                  │
   │   • indicator: 18,200                            │
   │   • country: 3,100                                │
   │   • forecast: 2,156                               │
   │                                                  │
   │  Rate limit hits: 0                              │
   │                                                  │
   │  [ Usage details → ]                             │
   └────────────────────────────────────────────────┘
```

Users can have multiple named keys (e.g., for different projects or devices).

## Rate-limit response

When a rate limit is hit:

```
   HTTP/1.1 429 Too Many Requests
   X-RateLimit-Limit: 200
   X-RateLimit-Remaining: 0
   X-RateLimit-Reset: 1717687200
   Retry-After: 30

   {
     "error": "rate_limit_exceeded",
     "message": "200 requests per minute exceeded. Retry in 30s or upgrade.",
     "upgrade_url": "https://opengem.app/pricing"
   }
```

Headers on every response (not just 429):
- `X-RateLimit-Limit`: tier limit
- `X-RateLimit-Remaining`: requests remaining in window
- `X-RateLimit-Reset`: unix timestamp when window resets

Clients can be polite by inspecting headers.

## Endpoints (top-level)

```
   GET  /api/v1/country/<iso3>
   GET  /api/v1/indicator/<id>
   GET  /api/v1/scenario/<id>
   GET  /api/v1/forecast/<id>
   GET  /api/v1/news?since=&country=
   GET  /api/v1/feed?cohort=
   GET  /api/v1/leaderboard
   GET  /api/v1/accountability?indicator=
   GET  /api/v1/cite/<cite-id>
   GET  /api/v1/methodology/<id>
   GET  /api/v1/glossary?term=

   POST /api/v1/forecast/score (paid only)
   POST /api/v1/notebook/export
   POST /api/v1/share/png
   POST /api/v1/share/gif
```

OpenAPI spec at `/api/v1/openapi.json`. Swagger UI at `/api/docs`.

## Caching

Every GET response includes:
- `Cache-Control` with sensible TTL
- `ETag` for conditional requests
- `Last-Modified` with vintage date

The CDN (Cloudflare) caches public endpoints aggressively. Authenticated endpoints (with key) bypass CDN for accuracy.

## Authentication patterns

- `Authorization: Bearer og_xxx` (preferred)
- `?api_key=og_xxx` (legacy; tolerated, not encouraged)
- For browsers (CORS): same `Authorization` header; CORS is open for public endpoints

API keys never accepted in URL params for paid tiers (security — URL params get logged in CDN).

## Quota counting

A request counts as 1, with exceptions:
- Bulk endpoints (e.g., all G7 indicators in one call) count by complexity — published in the docs
- Notebook export counts as 5 (compute-heavy)
- Image generation counts as 2

Free tier has a "complexity budget" too — heavy queries hit limits faster.

## Upgrade flow

When near a limit:

```
   You've used 4,500 / 5,000 daily requests.
   Upgrade to Pro (1M/month) for $99 →
```

When a 429 is returned, the JSON includes the upgrade URL.

Stripe checkout handles upgrades. Per L260.

## Documentation

`/api`:

```
   ┌────────────────────────────────────────────────┐
   │  OPENGEM API                                      │
   │  ──────────────────────────────────────────    │
   │                                                  │
   │  - Authentication                                 │
   │  - Rate limits                                    │
   │  - Endpoints                                      │
   │  - Errors                                         │
   │  - SDKs (Python, TypeScript, R)                  │
   │  - MCP support                                    │
   │  - Examples                                       │
   │  - Changelog                                      │
   │                                                  │
   │  Try in browser ↓                                 │
   │  [Interactive Swagger UI]                         │
   │                                                  │
   └────────────────────────────────────────────────┘
```

The Swagger UI is loaded with a free anonymous key; users can paste their own.

## CORS

Open for GET endpoints on public data. POST endpoints restricted to authenticated.

## Webhooks (paid)

Pro tier: webhooks for new vintages, new methodology versions, alerts. Configured via `/api/webhooks`.

## SDK release cadence

- Python: monthly release, SemVer
- TypeScript: monthly
- R: quarterly
- All Apache-2.0 on GitHub

## Anonymous tier rationale

Why anonymous works:
- 60 req/min is enough for casual exploration
- Caching at CDN means most anonymous traffic is cache-hit (no backend hit)
- Abuse mitigated by IP-level rate limiting + CDN bot detection

Why not no-anonymous-tier:
- Adding auth friction kills the YouTuber-paste-the-API-into-Substack use case
- The cohort 1 user (per L003) won't sign up for the first try

## Educational pricing

Universities, journalists, non-profits: free Pro tier on request. Email `educational@opengem.app`, get upgraded.

## Implementation

- Auth: Lucia (or Auth.js) with magic-link
- Keys: stored hashed (Argon2id), only the prefix `og_xxx...` shown after creation
- Rate limit: Redis-backed sliding window via Cloudflare Workers
- Quota tracking: ClickHouse for per-key usage analytics
- Webhooks: queue → background worker → HMAC-signed POST

## Performance

- Rate limit check: <2ms at CDN edge
- Auth check: <5ms at edge
- Key rotation: instant

## Mobile

The dashboard works on mobile. Most users will use it from desktop (developers).

## What we won't ship

- Per-endpoint rate limits in V1 (single global limit per tier)
- IP-based rate limits as the primary (just a backup for anonymous)
- Hidden tier-specific endpoints (every tier sees every endpoint)
- "Trial" tier that expires (free tier is permanent)

## The asymmetric move

Bloomberg's API requires a $25K/year terminal + a separate API contract + a NDA. Refinitiv similar. OPENGEM's free tier needs only an email.

This is the public-substrate thesis (L001). The API isn't a paywall around the dashboard — it's a separate distribution channel that's free for low-volume users.
