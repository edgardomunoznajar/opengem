"""Event — a normalized event record from any detector source."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


class EventSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EventSource(StrEnum):
    MARKET = "market"
    NEWS = "news"
    GPR = "gpr"
    GDELT = "gdelt"
    MANUAL = "manual"


@dataclass(frozen=True, slots=True)
class Event:
    """A detected event normalized across sources."""

    event_id: str
    detected_at: datetime
    source: EventSource
    severity: EventSeverity
    title: str
    summary: str
    tags: tuple[str, ...] = field(default_factory=tuple)
    related_countries: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, str] = field(default_factory=dict)
