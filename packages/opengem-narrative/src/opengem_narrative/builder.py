"""build_narrative_request — convert a ScenarioSection + Situation into a NarrativeRequest."""

from __future__ import annotations

from opengem_digest.digest import ScenarioSection, SituationSnapshot

from opengem_narrative.contract import NarrativeRequest


def build_narrative_request(
    section: ScenarioSection,
    *,
    situation: SituationSnapshot,
    user_notes: str = "",
    format: str = "analyst_segment_v1",
) -> NarrativeRequest:
    """Convert a digest ScenarioSection into a paste-ready NarrativeRequest."""
    situation_dict = {
        "recession_probability_us_12m": situation.recession_probability_us_12m,
        "recession_probability_model": situation.recession_probability_model,
        "gpr_global_latest": situation.gpr_global_latest,
        "gpr_global_zscore": situation.gpr_global_zscore,
        "gscpi_latest": situation.gscpi_latest,
        "term_spread_10y_3m_bp": situation.term_spread_10y_3m_bp,
        "vix_latest": situation.vix_latest,
    }
    # Drop None entries
    situation_dict = {k: v for k, v in situation_dict.items() if v is not None}

    return NarrativeRequest(
        pack_id=section.pack_id,
        title=section.title,
        summary=section.summary,
        rationale=section.rationale,
        references=section.references,
        spec_json=section.spec_json,
        situation=situation_dict,
        user_notes=user_notes,
        format=format,
    )
