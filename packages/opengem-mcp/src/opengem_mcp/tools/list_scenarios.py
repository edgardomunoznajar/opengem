"""Tool: list_scenarios — currently-triggered scenarios with probability."""

from __future__ import annotations

from typing import Any

from opengem_mcp.envelope import envelope

SCHEMA = {
    "name": "list_scenarios",
    "description": (
        "List currently-triggered OPENGEM scenarios with their probabilities, "
        "trigger summaries, and affected countries. Optionally filter to scenarios "
        "above a probability threshold."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "threshold": {
                "type": "number",
                "minimum": 0,
                "maximum": 1,
                "default": 0.05,
                "description": "Minimum probability to include (default 0.05).",
            },
            "country": {
                "type": "string",
                "minLength": 3,
                "maxLength": 3,
                "description": "Optional ISO-3 — only include scenarios affecting this country.",
            },
        },
        "required": [],
    },
}


def call(args: dict[str, Any], client) -> dict[str, Any]:
    threshold = float(args.get("threshold", 0.05))
    country = args.get("country")
    body = client.get("/v1/scenarios")
    items = body.get("items") or body.get("scenarios") or []
    filtered = [s for s in items if float(s.get("probability", 0)) >= threshold]
    if country:
        filtered = [s for s in filtered if country in (s.get("affected_countries") or [])]
    # Sort by probability descending
    filtered.sort(key=lambda s: -float(s.get("probability", 0)))
    return envelope(
        payload={"scenarios": filtered, "count": len(filtered)},
        vintage_id=(filtered[0].get("triggered_at") if filtered else "unknown"),
        cite_url="https://opengem.org/scenarios",
    )
