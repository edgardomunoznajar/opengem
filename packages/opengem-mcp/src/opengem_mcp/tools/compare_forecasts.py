"""Tool: compare_forecasts — OPENGEM vs WEO / OECD / FRB SEP / ECB SPF."""

from __future__ import annotations

from typing import Any

from opengem_mcp.envelope import envelope

SCHEMA = {
    "name": "compare_forecasts",
    "description": (
        "Compare OPENGEM's forecast for a given country × indicator × horizon "
        "against the major consensus forecasters (WEO, OECD EO, FRB SEP, ECB SPF). "
        "Returns the OPENGEM value, each consensus value, and the per-source delta. "
        "Useful when an LLM needs to ground a 'how does OPENGEM differ from consensus' claim."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "country": {"type": "string", "minLength": 3, "maxLength": 3},
            "indicator": {"type": "string"},
            "horizon": {
                "type": "string",
                "enum": ["nowcast", "1Q", "4Q", "2Y", "5Y"],
                "default": "4Q",
            },
        },
        "required": ["country", "indicator"],
    },
}


def call(args: dict[str, Any], client) -> dict[str, Any]:
    country = args["country"]
    indicator = args["indicator"]
    horizon = args.get("horizon", "4Q")
    body = client.get(
        "/v1/forecasts",
        params={"country": country, "indicator": indicator, "horizon": horizon},
    )
    items = body.get("items") or body.get("forecasts") or []
    if not items:
        return envelope(
            payload={"comparison": None, "reason": "no_forecast_at_vintage"},
            vintage_id="unknown",
            cite_url=f"https://opengem.org/countries/{country}",
        )
    fc = items[0]
    overlay = fc.get("consensus_overlay") or {}
    point = fc.get("point")
    comparisons = []
    for source, value in overlay.items():
        if value is None:
            continue
        comparisons.append(
            {
                "source": source,
                "value": value,
                "delta": (point - value) if point is not None else None,
            }
        )
    return envelope(
        payload={
            "opengem": {
                "point": point,
                "bands": fc.get("bands"),
                "model_id": fc.get("model_id"),
            },
            "comparisons": comparisons,
        },
        vintage_id=fc.get("vintage_id", "unknown"),
        cite_url=(
            f"https://opengem.org/forecasts/{fc.get('vintage_id', 'latest')}/"
            f"{country}/{indicator}/{horizon}"
        ),
        provenance=fc.get("provenance") or {},
    )
