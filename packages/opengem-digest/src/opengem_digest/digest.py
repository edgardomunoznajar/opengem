"""Digest — typed daily output for the OPENGEM friend-facing surface."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any


@dataclass(frozen=True, slots=True)
class SituationSnapshot:
    """Current Situation Subsystem state at digest time."""

    recession_probability_us_12m: float | None = None
    recession_probability_model: str | None = None
    gpr_global_latest: float | None = None
    gpr_global_zscore: float | None = None
    gscpi_latest: float | None = None
    term_spread_10y_3m_bp: float | None = None
    vix_latest: float | None = None


@dataclass(frozen=True, slots=True)
class ScenarioSection:
    """One scenario in the daily digest."""

    pack_id: str
    title: str
    summary: str
    invoked_at: date
    spec_json: dict[str, Any]
    rationale: str
    references: tuple[str, ...]
    diff_from_yesterday: str = "new"  # "new", "unchanged", "magnitude_changed"
    notes: str = ""


@dataclass(frozen=True, slots=True)
class Digest:
    """A daily OPENGEM digest, ready to render to markdown or feed to ChatGPT."""

    digest_id: str  # 'YYYYMMDD'
    as_of: date
    situation: SituationSnapshot
    scenarios: tuple[ScenarioSection, ...]
    events_summary: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    data_sources: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-safe dict suitable for paste-into-ChatGPT use."""
        return {
            "digest_id": self.digest_id,
            "as_of": self.as_of.isoformat(),
            "situation": {
                "recession_probability_us_12m": self.situation.recession_probability_us_12m,
                "recession_probability_model": self.situation.recession_probability_model,
                "gpr_global_latest": self.situation.gpr_global_latest,
                "gpr_global_zscore": self.situation.gpr_global_zscore,
                "gscpi_latest": self.situation.gscpi_latest,
                "term_spread_10y_3m_bp": self.situation.term_spread_10y_3m_bp,
                "vix_latest": self.situation.vix_latest,
            },
            "scenarios": [
                {
                    "pack_id": s.pack_id,
                    "title": s.title,
                    "summary": s.summary,
                    "invoked_at": s.invoked_at.isoformat(),
                    "spec_json": s.spec_json,
                    "rationale": s.rationale,
                    "references": list(s.references),
                    "diff_from_yesterday": s.diff_from_yesterday,
                    "notes": s.notes,
                }
                for s in self.scenarios
            ],
            "events_summary": list(self.events_summary),
            "data_sources": list(self.data_sources),
        }
