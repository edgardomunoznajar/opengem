"""Narrative output layer for OPENGEM."""

from opengem_narrative.contract import NarrativeOutput, NarrativeRequest
from opengem_narrative.builder import build_narrative_request
from opengem_narrative.prompts import (
    ANALYST_SEGMENT_SYSTEM_PROMPT_V1,
    EXECUTIVE_SUMMARY_SYSTEM_PROMPT_V1,
    FORBIDDEN_PREDICTIVE_PHRASES,
    REQUIRED_CONDITIONAL_MARKERS,
    SCENARIO_TABLE_SYSTEM_PROMPT_V1,
    get_system_prompt,
    lint_narrative_text,
)

__all__ = [
    "ANALYST_SEGMENT_SYSTEM_PROMPT_V1",
    "EXECUTIVE_SUMMARY_SYSTEM_PROMPT_V1",
    "FORBIDDEN_PREDICTIVE_PHRASES",
    "NarrativeOutput",
    "NarrativeRequest",
    "REQUIRED_CONDITIONAL_MARKERS",
    "SCENARIO_TABLE_SYSTEM_PROMPT_V1",
    "build_narrative_request",
    "get_system_prompt",
    "lint_narrative_text",
]
__version__ = "0.2.0"
