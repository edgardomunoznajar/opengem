"""Tool: get_gpr_nowcast — Caldara-Iacoviello GPR nowcast (global or country)."""

from __future__ import annotations

from typing import Any

from opengem_mcp.envelope import envelope

SCHEMA = {
    "name": "get_gpr_nowcast",
    "description": (
        "Get OPENGEM's Geopolitical Risk (GPR) nowcast. Built from POLECAT + GDELT + UCDP "
        "composite extending Caldara-Iacoviello GPR. Returns global or per-country value."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "country": {
                "type": "string",
                "minLength": 3,
                "maxLength": 3,
                "description": "Optional ISO-3 — omit for global GPR.",
            },
        },
        "required": [],
    },
}


def call(args: dict[str, Any], client) -> dict[str, Any]:
    country = args.get("country")
    params = {"country": country} if country else {}
    body = client.get("/v1/gpr-nowcast", params=params)
    scope = country or "world"
    return envelope(
        payload={"gpr_nowcast": body},
        vintage_id=body.get("as_of") or "unknown",
        cite_url=f"https://opengem.org/methodology/gpr-nowcast#{scope}",
        provenance={"methodology": "OPENGEM composite (POLECAT + GDELT + UCDP)"},
    )
