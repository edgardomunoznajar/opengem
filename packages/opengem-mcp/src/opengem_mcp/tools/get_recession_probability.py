"""Tool: get_recession_probability — Bauer-Mertens 12m nowcast."""

from __future__ import annotations

from typing import Any

from opengem_mcp.envelope import envelope

SCHEMA = {
    "name": "get_recession_probability",
    "description": (
        "Get OPENGEM's 12-month recession probability nowcast for a country, "
        "replicating the Bauer-Mertens term-spread probit (Federal Reserve Bank of San Francisco)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "country": {
                "type": "string",
                "minLength": 3,
                "maxLength": 3,
            },
        },
        "required": ["country"],
    },
}


def call(args: dict[str, Any], client) -> dict[str, Any]:
    country = args["country"]
    body = client.get("/v1/recession-probability", params={"country": country})
    return envelope(
        payload={"recession_probability": body},
        vintage_id=body.get("as_of") or "unknown",
        cite_url=f"https://opengem.org/methodology/recession-prob-{country.lower()}",
        provenance={"methodology": "Bauer-Mertens term-spread probit"},
    )
