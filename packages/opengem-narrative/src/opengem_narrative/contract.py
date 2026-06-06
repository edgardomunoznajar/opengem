"""NarrativeRequest / NarrativeOutput — typed contracts for the LLM boundary."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class NarrativeRequest:
    """The structured input the user pastes into ChatGPT.

    Carries the scenario pack info, the resolved ScenarioSpec, situation context,
    references, and any user notes. The system prompt instructs the LLM to use
    *only* these fields for numerical claims.
    """

    pack_id: str
    title: str
    summary: str
    rationale: str
    references: tuple[str, ...]
    spec_json: dict[str, Any]
    situation: dict[str, Any] = field(default_factory=dict)
    user_notes: str = ""
    format: str = "analyst_segment_v1"  # which prompt to pair with

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": self.format,
            "pack_id": self.pack_id,
            "title": self.title,
            "summary": self.summary,
            "rationale": self.rationale,
            "references": list(self.references),
            "spec_json": self.spec_json,
            "situation": self.situation,
            "user_notes": self.user_notes,
        }

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


@dataclass(frozen=True, slots=True)
class NarrativeOutput:
    """The expected format the LLM is instructed to return.

    Used for downstream parsing and for tests of the contract.
    """

    title: str
    paragraphs: tuple[str, ...]
    caveats: tuple[str, ...] = field(default_factory=tuple)
    citations: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> NarrativeOutput:
        return cls(
            title=str(d.get("title", "")),
            paragraphs=tuple(str(p) for p in d.get("paragraphs", [])),
            caveats=tuple(str(c) for c in d.get("caveats", [])),
            citations=tuple(str(r) for r in d.get("citations", [])),
        )
