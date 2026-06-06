"""Tool: get_forecast — fetch a single OPENGEM forecast object."""

from __future__ import annotations

from typing import Any

from opengem_mcp.envelope import envelope

SCHEMA = {
    "name": "get_forecast",
    "description": (
        "Fetch a single OPENGEM forecast for a country × indicator × horizon. "
        "Response includes the canonical P10/P50/P90 band plus the consensus "
        "overlay (WEO, OECD EO, FRB SEP, ECB SPF) when available. Every response "
        "is vintage-stamped and carries provenance for replay."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "country": {
                "type": "string",
                "minLength": 3,
                "maxLength": 3,
                "description": "ISO-3166-1 alpha-3 country code (e.g. 'USA').",
            },
            "indicator": {
                "type": "string",
                "description": "OPENGEM indicator code (e.g. 'gdp_yoy', 'cpi_yoy', 'policy_rate').",
            },
            "horizon": {
                "type": "string",
                "enum": ["nowcast", "1Q", "4Q", "2Y", "5Y"],
                "default": "4Q",
                "description": "Forecast horizon.",
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
            payload={"forecast": None, "reason": "no_match"},
            vintage_id="unknown",
            cite_url=f"https://opengem.org/countries/{country}",
        )
    record = items[0]
    return envelope(
        payload={"forecast": record},
        vintage_id=record.get("vintage_id", "unknown"),
        cite_url=(
            f"https://opengem.org/forecasts/{record.get('vintage_id', 'latest')}/"
            f"{country}/{indicator}/{horizon}"
        ),
        provenance=record.get("provenance") or {},
    )
