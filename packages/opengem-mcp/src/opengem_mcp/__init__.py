"""opengem-mcp — MCP server for OPENGEM.

Public API is the ``server.main`` CLI entry point. The tool implementations
are exposed via ``opengem_mcp.tools`` for direct unit testing.
"""

from opengem_mcp.envelope import envelope
from opengem_mcp.tools import ALL_TOOLS, tool_schema

__all__ = ["ALL_TOOLS", "envelope", "tool_schema"]
__version__ = "0.1.0"
