"""Conditional[T] — universal epistemic-honesty wrapper.

The OPENGEM contract: **every quantitative output is framed as "based on X, this
could happen" — never as "this WILL happen."** This module codifies that.

Every model output, every scenario IRF, every recession probability, every
emerging-tech indicator, every leader-behavior base rate is returned wrapped in
a Conditional[T]. The wrapper carries:

- the value (T)
- the basis (the evidence / model / data the value rests on)
- the confidence framing (point | range | distribution | base-rate)
- explicit caveats (what's NOT captured)

This is not optional decoration — it's enforced at API boundaries and rendered
in every output surface (digest, narrative, MCP tools).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum
from typing import Generic, TypeVar

T = TypeVar("T")


class ConfidenceKind(StrEnum):
    """How the value should be interpreted."""

    POINT = "point"  # single value, e.g., today's closing yield
    RANGE = "range"  # interval, e.g., 4Q GDP between -0.5 and +0.5
    DISTRIBUTION = "distribution"  # density forecast (P10/P50/P90)
    BASE_RATE = "base_rate"  # historical frequency, e.g., "in past 20 episodes, X happened 60%"
    SCENARIO_PATH = "scenario_path"  # one path within a scenario, not a forecast


@dataclass(frozen=True, slots=True)
class Basis:
    """The evidence a Conditional rests on.

    Designed so that any value can be defended: 'we say X, because Y, citing Z.'
    """

    model_or_method: str  # e.g., "bauer_mertens_us_12m_v1", "OECD ORDRA vintage", "ACLED event count"
    inputs_description: str = ""  # human-readable: what data went in
    inputs_hash: str | None = None  # sha256 of canonical inputs, for reproducibility
    as_of: date | None = None
    citations: tuple[str, ...] = field(default_factory=tuple)
    caveats: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class Conditional(Generic[T]):
    """A value wrapped with its epistemic basis.

    The OPENGEM contract: anything OPENGEM exposes that could be misread as a
    confident prediction MUST be wrapped in Conditional[T] before leaving the
    process boundary. Internal computations may use bare T; API surfaces may not.

    Use the `framed_as` field to make the conditional framing explicit in human
    text. Default templates:
        - POINT: "{value} (based on {basis.model_or_method})"
        - DISTRIBUTION: "{P10}–{P90} based on {basis.model_or_method}"
        - BASE_RATE: "In past analogous contexts, {value:.0%} based on {basis.inputs_description}"
        - SCENARIO_PATH: "If {assumption}, then {value} (model: {basis.model_or_method})"
    """

    value: T
    basis: Basis
    confidence: ConfidenceKind
    framed_as: str | None = None  # explicit human-text framing
    conditional_on: tuple[str, ...] = field(default_factory=tuple)  # explicit antecedents

    def __post_init__(self) -> None:
        if self.basis.model_or_method == "":
            raise ValueError("Conditional.basis.model_or_method must be non-empty")

    def render_human(self) -> str:
        """Render a one-sentence conditional framing."""
        if self.framed_as:
            return self.framed_as
        match self.confidence:
            case ConfidenceKind.POINT:
                return f"{self.value} (based on {self.basis.model_or_method})"
            case ConfidenceKind.RANGE:
                return f"{self.value} (range; based on {self.basis.model_or_method})"
            case ConfidenceKind.DISTRIBUTION:
                return f"density {self.value} (based on {self.basis.model_or_method})"
            case ConfidenceKind.BASE_RATE:
                return (
                    f"In past analogous contexts: {self.value} "
                    f"(based on {self.basis.inputs_description})"
                )
            case ConfidenceKind.SCENARIO_PATH:
                ifs = " and ".join(self.conditional_on) if self.conditional_on else "the scenario assumptions"
                return f"If {ifs}, then {self.value} (model: {self.basis.model_or_method})"
        return str(self.value)
