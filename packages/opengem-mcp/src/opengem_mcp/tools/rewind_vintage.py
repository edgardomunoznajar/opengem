"""Tool: rewind_vintage — replay any historical forecast at any vintage date."""

from __future__ import annotations

from typing import Any

from opengem_mcp.envelope import envelope

SCHEMA = {
    "name": "rewind_vintage",
    "description": (
        "Replay OPENGEM forecasts at a historical vintage date. Per the editorial "
        "discipline of vintage permanence, every forecast OPENGEM ever published "
        "is permanently addressable by its vintage_id."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "description": "Vintage date YYYY-MM-DD.",
            },
            "what": {
                "type": "string",
                "enum": ["forecasts", "scenarios", "situation"],
                "default": "forecasts",
                "description": "What to replay.",
            },
            "country": {
                "type": "string",
                "minLength": 3,
                "maxLength": 3,
                "description": "Optional ISO-3 filter.",
            },
        },
        "required": ["date"],
    },
}


def call(args: dict[str, Any], client) -> dict[str, Any]:
    vintage_date = args["date"]
    what = args.get("what", "forecasts")
    country = args.get("country")
    path_map = {
        "forecasts": "/v1/forecasts",
        "scenarios": "/v1/scenarios",
        "situation": "/v1/situation",
    }
    path = path_map[what]
    params: dict[str, Any] = {"vintage": vintage_date}
    if country:
        params["country"] = country
    body = client.get(path, params=params)
    items = body.get("items") or body.get(what) or []
    return envelope(
        payload={"vintage": vintage_date, "what": what, what: items, "count": len(items)},
        vintage_id=vintage_date,
        cite_url=f"https://opengem.org/vintage/{vintage_date}/{what}"
        + (f"?country={country}" if country else ""),
    )
