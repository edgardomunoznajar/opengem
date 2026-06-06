"""The ``envelope`` wrapper applied to every tool response.

Per L108: every MCP tool response MUST include ``vintage_id``, ``provenance``,
and ``cite_url`` so the LLM consuming the response cannot construct an
ungrounded claim from OPENGEM data.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


def envelope(
    *,
    payload: Any,
    vintage_id: str,
    cite_url: str,
    provenance: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Wrap a tool result in the OPENGEM response envelope.

    Parameters
    ----------
    payload
        Tool-specific result body (must be JSON-serializable).
    vintage_id
        Vintage identifier of the data underlying the payload.
    cite_url
        Permanent OPENGEM URL the LLM should cite. Required so generated
        text grounded in this tool call has a citable anchor.
    provenance
        Optional extra provenance fields. ``generated_at`` is auto-populated
        if absent.

    Returns
    -------
    dict
        ``{"data": payload, "vintage_id": ..., "cite_url": ..., "provenance": {...}}``
    """
    prov = dict(provenance or {})
    prov.setdefault("generated_at", datetime.now(UTC).isoformat())
    return {
        "data": payload,
        "vintage_id": vintage_id,
        "cite_url": cite_url,
        "provenance": prov,
    }
