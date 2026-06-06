"""Tool: get_leaderboard — CRPS-ranked forecast leaderboard."""

from __future__ import annotations

from typing import Any

from opengem_mcp.envelope import envelope

SCHEMA = {
    "name": "get_leaderboard",
    "description": (
        "Get the forecast leaderboard for an indicator × horizon. Models are ranked "
        "by Stacked Skill Score (CRPS-based, OPENGEM Index v2.0). Includes RW and AR(1) "
        "baselines plus consensus forecasters where available."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "indicator": {"type": "string"},
            "horizon": {
                "type": "string",
                "enum": ["nowcast", "1Q", "4Q", "2Y", "5Y"],
                "default": "4Q",
            },
        },
        "required": ["indicator"],
    },
}


def call(args: dict[str, Any], client) -> dict[str, Any]:
    indicator = args["indicator"]
    horizon = args.get("horizon", "4Q")
    body = client.get(
        "/v1/leaderboard",
        params={"indicator": indicator, "horizon": horizon},
    )
    items = body.get("items") or body.get("leaderboard") or []
    return envelope(
        payload={"indicator": indicator, "horizon": horizon, "leaderboard": items},
        vintage_id=body.get("as_of") or "unknown",
        cite_url=f"https://opengem.org/leaderboard?indicator={indicator}&horizon={horizon}",
    )
