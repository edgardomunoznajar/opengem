"""
OPENGEM API stub — what the dashboard talks to.

This is a FastAPI sketch of the read-side public API. It pulls from
opengem-digest (already in the repo) for the daily JSON digest and
fans it out as REST endpoints + a tiny WebSocket stream for live ticker.

It is NOT the production API — the production design is in
docs/design/20-interfaces/OG1-ICD-002. This stub exists so the dashboard
prototype has a working endpoint to develop against.

Run:
    pip install fastapi uvicorn pydantic
    uvicorn main:app --reload --port 8001
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import json
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


HERE = Path(__file__).parent
FIXTURES = HERE.parent / "dashboard-next" / "data"

app = FastAPI(
    title="OPENGEM Public API (stub)",
    description=(
        "Read-only public surface for the OPENGEM World Dashboard. "
        "Every response is vintage-stamped. Every model has a model card."
    ),
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


def _load(filename: str) -> Any:
    p = FIXTURES / filename
    if not p.exists():
        return []
    return json.loads(p.read_text())


class HealthResponse(BaseModel):
    ok: bool
    version: str
    as_of: str


@app.get("/v1/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        ok=True,
        version="0.1.0-stub",
        as_of=datetime.now(timezone.utc).isoformat(),
    )


@app.get("/v1/situation")
def situation() -> list[dict[str, Any]]:
    return _load("fixtures.situation.json")


@app.get("/v1/scenarios")
def scenarios() -> list[dict[str, Any]]:
    return _load("fixtures.scenarios.json")


@app.get("/v1/forecasts")
def forecasts(
    country: str | None = Query(default=None),
    indicator: str | None = Query(default=None),
    horizon: str | None = Query(default=None),
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = _load("fixtures.forecasts.json")
    if country:
        items = [x for x in items if x.get("country") == country]
    if indicator:
        items = [x for x in items if x.get("indicator") == indicator]
    if horizon:
        items = [x for x in items if x.get("horizon") == horizon]
    return items


@app.get("/v1/countries/{iso3}")
def country(iso3: str) -> dict[str, Any]:
    situation = [x for x in _load("fixtures.situation.json") if x.get("country") in (iso3, None)]
    forecasts = [x for x in _load("fixtures.forecasts.json") if x.get("country") == iso3]
    if not forecasts and not situation:
        raise HTTPException(status_code=404, detail=f"Country {iso3} not covered")
    return {
        "iso3": iso3,
        "situation": situation,
        "forecasts": forecasts,
    }


@app.get("/v1/recession-probability")
def recession_prob(country: str = Query(...)) -> dict[str, Any]:
    items = [
        x for x in _load("fixtures.situation.json")
        if x.get("kind") == "recession_prob" and x.get("country") == country
    ]
    if not items:
        raise HTTPException(status_code=404, detail=f"No recession nowcast for {country}")
    return items[0]


@app.get("/v1/gpr-nowcast")
def gpr_nowcast(country: str | None = Query(default=None)) -> dict[str, Any]:
    items = [
        x for x in _load("fixtures.situation.json")
        if x.get("kind") == "gpr_nowcast" and (country is None or x.get("country") == country)
    ]
    if not items:
        raise HTTPException(status_code=404, detail="No GPR nowcast")
    return items[0]


@app.get("/v1/leaderboard")
def leaderboard(indicator: str = Query(...), horizon: str = Query("4Q")) -> list[dict[str, Any]]:
    # Stub data
    return [
        {"rank": 1, "model": "opengem-l3-dfm-bma-v0.4", "indicator": indicator, "horizon": horizon, "crps": 0.42, "pit": 0.78, "hit_rate": 0.61, "n": 96},
        {"rank": 2, "model": "WEO Apr-2026", "indicator": indicator, "horizon": horizon, "crps": 0.48, "pit": 0.71, "hit_rate": 0.58, "n": 96},
        {"rank": 3, "model": "OECD EO Mar-2026", "indicator": indicator, "horizon": horizon, "crps": 0.51, "pit": 0.69, "hit_rate": 0.56, "n": 96},
        {"rank": 4, "model": "RW (random-walk)", "indicator": indicator, "horizon": horizon, "crps": 0.65, "pit": 0.55, "hit_rate": 0.50, "n": 96},
        {"rank": 5, "model": "AR(1)", "indicator": indicator, "horizon": horizon, "crps": 0.62, "pit": 0.58, "hit_rate": 0.51, "n": 96},
    ]


@app.get("/v1/accountability/summary")
def accountability_summary() -> dict[str, Any]:
    return {
        "published": 14_283,
        "scored": 11_902,
        "missed": 2_117,
        "pending": 264,
        "miss_rate_at_80pct_band": 0.178,
        "target_miss_rate": 0.20,
        "since": "2024-Q1",
    }
