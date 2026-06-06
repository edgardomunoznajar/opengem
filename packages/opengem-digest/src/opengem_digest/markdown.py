"""Markdown rendering of a Digest — what the friend skims in the morning."""

from __future__ import annotations

import json
from io import StringIO

from opengem_digest.digest import Digest


def render_markdown(digest: Digest) -> str:
    """Render a Digest to markdown."""
    buf = StringIO()
    w = buf.write

    w(f"# OPENGEM Daily Digest — {digest.as_of.isoformat()}\n\n")
    w(f"`digest_id: {digest.digest_id}`\n\n")

    # Situation panel
    w("## Situation\n\n")
    w(
        "_Every value below is **conditional** — frame as 'could happen based on X', "
        "not as a prediction. OPENGEM produces scenarios grounded in stated models, "
        "not forecasts._\n\n"
    )
    sit = digest.situation
    rows: list[tuple[str, str]] = []
    if sit.recession_probability_us_12m is not None:
        rows.append(
            (
                "Recession probability (US, 12m)",
                f"{sit.recession_probability_us_12m:.1%} — could happen based on "
                f"{sit.recession_probability_model or 'unknown'} (term-spread signal)",
            )
        )
    if sit.term_spread_10y_3m_bp is not None:
        rows.append(("Term spread 10y-3m (bp)", f"{sit.term_spread_10y_3m_bp:.1f}"))
    if sit.gpr_global_latest is not None:
        zs = f" (z={sit.gpr_global_zscore:+.2f})" if sit.gpr_global_zscore is not None else ""
        rows.append(("Geopolitical Risk (global)", f"{sit.gpr_global_latest:.1f}{zs}"))
    if sit.gscpi_latest is not None:
        rows.append(("Global Supply Chain Pressure", f"{sit.gscpi_latest:+.2f}"))
    if sit.vix_latest is not None:
        rows.append(("VIX", f"{sit.vix_latest:.1f}"))

    if rows:
        w("| Indicator | Value |\n|---|---|\n")
        for label, val in rows:
            w(f"| {label} | {val} |\n")
        w("\n")
    else:
        w("_No situation data available._\n\n")

    # Events
    if digest.events_summary:
        w("## Events detected\n\n")
        for ev in digest.events_summary:
            severity = ev.get("severity", "?")
            title = ev.get("title", "")
            w(f"- **[{severity}]** {title}\n")
        w("\n")

    # Scenarios
    w(f"## Scenarios ({len(digest.scenarios)})\n\n")
    w(
        "_Each scenario below describes **what could happen** under stated "
        "assumptions and a named model. Not a prediction. Read every IRF as "
        "'under this shock specification, the L2 BGVAR suggests...'._\n\n"
    )
    if not digest.scenarios:
        w("_No scenarios triggered today._\n\n")
    for sec in digest.scenarios:
        diff_tag = {"new": "🆕 NEW", "unchanged": "↻ ongoing", "magnitude_changed": "Δ revised"}.get(
            sec.diff_from_yesterday, sec.diff_from_yesterday
        )
        w(f"### {sec.title} `{diff_tag}`\n\n")
        w(f"**Pack:** `{sec.pack_id}`\n\n")
        w(f"{sec.summary}\n\n")
        w(f"**Rationale:** {sec.rationale}\n\n")
        if sec.notes:
            w(f"**Notes:** {sec.notes}\n\n")
        if sec.references:
            w("**References:**\n")
            for r in sec.references:
                w(f"- {r}\n")
            w("\n")
        # JSON block ready for ChatGPT paste
        w("**Paste this JSON into ChatGPT with the OPENGEM prompt:**\n\n")
        w("```json\n")
        w(json.dumps(sec.spec_json, indent=2))
        w("\n```\n\n")

    # Data sources footer
    if digest.data_sources:
        w("---\n\n")
        w("**Data sources:** ")
        w(", ".join(digest.data_sources))
        w("\n")

    return buf.getvalue()
