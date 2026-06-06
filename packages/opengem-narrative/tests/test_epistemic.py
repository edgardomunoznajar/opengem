"""Tests for the epistemic contract — prompts contain the right framing,
and lint_narrative_text catches violations."""

from __future__ import annotations

import pytest
from opengem_narrative import (
    ANALYST_SEGMENT_SYSTEM_PROMPT_V1,
    EXECUTIVE_SUMMARY_SYSTEM_PROMPT_V1,
    FORBIDDEN_PREDICTIVE_PHRASES,
    SCENARIO_TABLE_SYSTEM_PROMPT_V1,
    lint_narrative_text,
)


def test_all_prompts_contain_epistemic_contract() -> None:
    for prompt in (
        ANALYST_SEGMENT_SYSTEM_PROMPT_V1,
        EXECUTIVE_SUMMARY_SYSTEM_PROMPT_V1,
        SCENARIO_TABLE_SYSTEM_PROMPT_V1,
    ):
        assert "EPISTEMIC CONTRACT" in prompt
        assert "FORBIDDEN" in prompt
        assert "could" in prompt.lower()
        assert "based on" in prompt.lower()


def test_lint_flags_predictive_text() -> None:
    bad = (
        "Equities will surge once the Fed cuts. The market is heading for "
        "a crash. The economy is going to contract sharply."
    )
    violations, _missing = lint_narrative_text(bad)
    assert "will surge" in violations
    assert "is heading for" in violations
    assert "is going to" in violations
    assert len(violations) >= 3


def test_lint_passes_conditional_text() -> None:
    good = (
        "Based on the L2 BGVAR posterior, EU GDP could fall by approximately "
        "0.5pp at 4Q under this scenario. The model suggests that if Russia "
        "gas exports drop by 50%, the spillover would be most acute in "
        "Germany. In past analogous oil-price episodes, similar impacts have "
        "materialized within 2-3 quarters."
    )
    violations, missing = lint_narrative_text(good)
    assert violations == []
    assert missing == []


def test_lint_flags_text_lacking_conditionals() -> None:
    """A long text with no conditional markers should be flagged."""
    bad = (
        "The country has experienced significant economic stress. The data shows "
        "elevated unemployment, declining industrial production, and weakening "
        "consumer demand. The labor market continues to deteriorate. Inflation "
        "remains elevated. Trade balance has narrowed. Manufacturing PMI is in "
        "contraction territory across multiple sectors of the economy."
    )
    _violations, missing = lint_narrative_text(bad)
    assert len(missing) >= 1


def test_lint_passes_short_neutral_text() -> None:
    """Short statements that don't trigger length-based marker requirements."""
    violations, missing = lint_narrative_text("Term spread is -15bp.")
    assert violations == []
    assert missing == []


@pytest.mark.parametrize("phrase", FORBIDDEN_PREDICTIVE_PHRASES)
def test_each_forbidden_phrase_caught(phrase: str) -> None:
    text = f"Some preamble. {phrase} something. More text to make it long enough."
    violations, _ = lint_narrative_text(text)
    assert phrase in violations
