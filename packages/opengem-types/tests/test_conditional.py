from __future__ import annotations

import pytest
from opengem_types import Basis, Conditional, ConfidenceKind


def test_conditional_point() -> None:
    c = Conditional(
        value=0.18,
        basis=Basis(
            model_or_method="bauer_mertens_us_12m_v1",
            inputs_description="10y-3m spread 42bp as of 2026-05-25",
        ),
        confidence=ConfidenceKind.POINT,
    )
    text = c.render_human()
    assert "0.18" in text
    assert "bauer_mertens" in text
    assert "based on" in text


def test_conditional_distribution() -> None:
    c = Conditional(
        value="P10=0.012, P50=0.024, P90=0.038",
        basis=Basis(
            model_or_method="opengem-l3-bma-v0.1",
            inputs_description="US Tier-V vintage 2026-Q1",
        ),
        confidence=ConfidenceKind.DISTRIBUTION,
    )
    text = c.render_human()
    assert "density" in text
    assert "P10" in text


def test_conditional_base_rate_framing() -> None:
    """The leader-behavior framing: 'In past N similar contexts, X happened Y%.'"""
    c = Conditional(
        value="40%",
        basis=Basis(
            model_or_method="leader-action-base-rate",
            inputs_description="22 analogous tariff-escalation episodes 2010–2024",
        ),
        confidence=ConfidenceKind.BASE_RATE,
    )
    text = c.render_human()
    assert "In past analogous contexts" in text
    assert "40%" in text
    assert "22 analogous" in text


def test_conditional_scenario_path() -> None:
    c = Conditional(
        value="-0.6pp EA GDP at 4Q",
        basis=Basis(model_or_method="L2-BGVAR-2026"),
        confidence=ConfidenceKind.SCENARIO_PATH,
        conditional_on=("Russia gas exports drop 50%", "ECB raises 50bp"),
    )
    text = c.render_human()
    assert "If Russia gas exports drop 50%" in text
    assert "ECB raises 50bp" in text
    assert "-0.6pp" in text


def test_conditional_explicit_framing_wins() -> None:
    c = Conditional(
        value=0.18,
        basis=Basis(model_or_method="x"),
        confidence=ConfidenceKind.POINT,
        framed_as="Recession probability 18% (could happen based on inverted curve signal)",
    )
    assert "could happen" in c.render_human()


def test_basis_rejects_empty_model() -> None:
    """Conditional must have a named basis — never bare predictions."""
    with pytest.raises(ValueError, match="model_or_method must be non-empty"):
        Conditional(
            value=0.18,
            basis=Basis(model_or_method="", inputs_description="x"),
            confidence=ConfidenceKind.POINT,
        )


def test_basis_carries_caveats() -> None:
    b = Basis(
        model_or_method="opengem-tech-arxiv-flow-v1",
        inputs_description="arXiv CS.AI submissions 2024-2026",
        citations=("arXiv submission API",),
        caveats=(
            "Submission count is a noisy proxy for capability progress",
            "Field boundaries are contested",
        ),
    )
    c = Conditional(value=145, basis=b, confidence=ConfidenceKind.POINT)
    assert len(c.basis.caveats) == 2


def test_conditional_is_frozen() -> None:
    c = Conditional(
        value=1.0,
        basis=Basis(model_or_method="x"),
        confidence=ConfidenceKind.POINT,
    )
    with pytest.raises(Exception):  # FrozenInstanceError
        c.value = 2.0  # type: ignore[misc]


def test_conditional_generic_preserves_type() -> None:
    """Conditional[T] holds any T."""
    c_float: Conditional[float] = Conditional(
        value=0.18,
        basis=Basis(model_or_method="x"),
        confidence=ConfidenceKind.POINT,
    )
    c_str: Conditional[str] = Conditional(
        value="recession likely",
        basis=Basis(model_or_method="x"),
        confidence=ConfidenceKind.POINT,
    )
    c_tuple: Conditional[tuple[float, ...]] = Conditional(
        value=(0.1, 0.2, 0.3),
        basis=Basis(model_or_method="x"),
        confidence=ConfidenceKind.DISTRIBUTION,
    )
    assert c_float.value == 0.18
    assert c_str.value == "recession likely"
    assert c_tuple.value == (0.1, 0.2, 0.3)
