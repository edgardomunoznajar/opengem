# OPENGEM API stub

A FastAPI sketch of the read-side public API. Reads fixtures from the dashboard's `data/` directory and fans them out as REST endpoints.

## Run

```bash
cd research-300/prototypes/api-stub
pip install fastapi uvicorn pydantic
uvicorn main:app --reload --port 8001
```

Then:
- `http://localhost:8001/docs` — Swagger UI
- `http://localhost:8001/openapi.json` — OpenAPI 3.1 spec (auto-generated)
- `http://localhost:8001/v1/health` — liveness
- `http://localhost:8001/v1/situation` — current situation tiles
- `http://localhost:8001/v1/forecasts` — all forecasts
- `http://localhost:8001/v1/forecasts?country=USA&indicator=gdp_yoy` — filtered
- `http://localhost:8001/v1/countries/USA` — country bundle
- `http://localhost:8001/v1/recession-probability?country=USA` — Bauer-Mertens probit nowcast
- `http://localhost:8001/v1/scenarios` — triggered scenarios

## What this is and isn't

**Is**: a working stub that the Next.js dashboard at `../dashboard-next/` can talk to via `OPENGEM_API_URL=http://localhost:8001`.

**Isn't**: the production API. The production design is in `opengem/docs/design/20-interfaces/OG1-ICD-002`. The production implementation will pull from `opengem-vintage` (TimescaleDB) instead of JSON fixtures.

## Companion OpenAPI

A hand-written `openapi-sample.yaml` ships alongside `main.py` documenting the full v0.1 surface — useful for spec reviews and for consumers who want types without running the server.

## CORS

Hard-coded to `http://localhost:3000` for dev. Production tightens to `opengem.org` plus the embed origins whitelist.

## License

Apache-2.0.
