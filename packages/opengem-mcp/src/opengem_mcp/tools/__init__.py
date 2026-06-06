"""All MCP tool implementations.

Each tool exposes a ``call(args, client) -> dict`` function and a ``SCHEMA``
constant describing its JSON-Schema-shaped input. The ``ALL_TOOLS`` mapping
is what the server registers.
"""

from opengem_mcp.tools import (
    cite_this_view,
    compare_forecasts,
    get_forecast,
    get_gpr_nowcast,
    get_leaderboard,
    get_recession_probability,
    list_misses,
    list_scenarios,
    rewind_vintage,
    subscribe_events,
)


ALL_TOOLS = {
    "get_forecast": get_forecast,
    "compare_forecasts": compare_forecasts,
    "list_scenarios": list_scenarios,
    "get_recession_probability": get_recession_probability,
    "get_gpr_nowcast": get_gpr_nowcast,
    "rewind_vintage": rewind_vintage,
    "get_leaderboard": get_leaderboard,
    "list_misses": list_misses,
    "subscribe_events": subscribe_events,
    "cite_this_view": cite_this_view,
}


def tool_schema(name: str) -> dict:
    return ALL_TOOLS[name].SCHEMA


__all__ = ["ALL_TOOLS", "tool_schema"]
