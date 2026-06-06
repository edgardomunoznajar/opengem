# L249 — OpenAPI spec for public API

**Loop**: 249 / 300
**Phase**: 5 — Code prototypes
**Date**: 2026-06-06
**Artifact**: `prototypes/api-stub/main.py` (FastAPI auto-generates /docs at /openapi.json)

---

## What was built

`prototypes/api-stub/main.py` — a FastAPI service stub the Next.js dashboard talks to.

FastAPI auto-emits an OpenAPI 3.1 spec at `/openapi.json` and Swagger UI at `/docs`, so we get the OpenAPI artifact for free without hand-writing YAML. The endpoints below are stubbed; the spec hardens once they're real.

## Endpoints (v0.1)

| Path | Method | Purpose |
|---|---|---|
| `/v1/health` | GET | Stub liveness; includes version + as_of |
| `/v1/situation` | GET | All situation tiles (recession_prob, gpr, gscpi, fci, nowcasts) |
| `/v1/scenarios` | GET | All triggered scenarios with probability |
| `/v1/forecasts` | GET | All forecasts, filterable by `country`, `indicator`, `horizon` |
| `/v1/countries/{iso3}` | GET | Country bundle: situation + forecasts |
| `/v1/recession-probability` | GET | Per-country Bauer-Mertens nowcast |
| `/v1/gpr-nowcast` | GET | Global or per-country GPR nowcast |
| `/v1/leaderboard` | GET | Forecast leaderboard per indicator × horizon |
| `/v1/accountability/summary` | GET | Published / scored / missed / pending counts |

## Contract guarantees

- **Vintage stamping**: every response carries `as_of` or per-object `vintage_id`.
- **CORS open to localhost:3000** in dev; tightens to `opengem.org` and embed origins in prod.
- **No auth on public read endpoints** — rate-limited by IP. Paid keys lift the limit; they do not unlock data.
- **Schemas mirror types/forecast.ts** — same Zod shapes on both sides, validated at boundaries.

## Production migration path

The stub uses fixture JSON from the dashboard's `data/` folder. In production:

1. Replace `_load()` with calls into `opengem-vintage` (TimescaleDB).
2. Add `Last-Modified` + `ETag` headers driven by vintage_id.
3. Add WebSocket endpoint `/v1/stream` for the live event ticker.
4. Add JSON-LD + schema.org metadata to support SEO of the public ledger.

## Hosting

| Phase | Choice |
|---|---|
| Prototype | local uvicorn — `uvicorn main:app --reload --port 8001` |
| v0.x | Cloud Run (Python) behind Cloudflare proxy |
| v1.x | Fly.io or Cloud Run, with R2/S3 for cold vintage tier |
| v2.x | Behind an Envoy gateway with paid-tier rate-limit enforcement |

## What this loop produced

- Working FastAPI stub at `prototypes/api-stub/main.py`
- Auto-generated OpenAPI 3.1 spec when run
- Endpoint inventory mapped to Next.js dashboard fetches

## What comes next

- L250 — MCP server prototype (extends scenarios package's MCP work)
- L253 — Datasette mounted at `/data` for raw access (separate read path)

## Related

- [[L231-nextjs-scaffold]] — the dashboard the API serves
- [[L181-forecast-object-schema]] — Forecast contract
- [[L108-mcp-server-contract]] — MCP tools that wrap these endpoints
- [[L176-public-api-rate-limit-ux]] — UX for the API key + paid tier
