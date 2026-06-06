"""NewsKeywordDetector — keyword-based event detection from news headlines."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime
from typing import NamedTuple

from opengem_event_detector.event import Event, EventSeverity, EventSource


class Headline(NamedTuple):
    headline_id: str
    text: str
    published_at: datetime
    source: str  # outlet name


@dataclass(frozen=True, slots=True)
class KeywordRule:
    """Match rule mapping a keyword cluster to an event tag/severity."""

    name: str
    any_of: tuple[str, ...]  # at least one keyword must match
    all_of: tuple[str, ...] = ()  # all of these must also match
    severity: EventSeverity = EventSeverity.MEDIUM
    tags: tuple[str, ...] = ()
    countries: tuple[str, ...] = ()


# IOC rule set — mapped to scenario packs in the rule engine
DEFAULT_NEWS_RULES: tuple[KeywordRule, ...] = (
    KeywordRule(
        name="russia-ukraine-escalation",
        any_of=("Ukraine", "Kyiv", "Donbas", "Putin", "Zelensky"),
        all_of=(),
        severity=EventSeverity.HIGH,
        tags=("russia", "ukraine", "war", "energy"),
        countries=("RU", "UA"),
    ),
    KeywordRule(
        name="taiwan-strait",
        any_of=("Taiwan", "TSMC", "Taipei", "Taiwan Strait"),
        all_of=(),
        severity=EventSeverity.HIGH,
        tags=("china", "taiwan", "semiconductors", "supply-chain"),
        countries=("CN", "TW"),
    ),
    KeywordRule(
        name="iran-israel",
        any_of=("Iran", "Tehran", "Hormuz"),
        all_of=(),
        severity=EventSeverity.HIGH,
        tags=("iran", "israel", "oil", "middle-east"),
        countries=("IR", "IL"),
    ),
    KeywordRule(
        name="opec-announcement",
        any_of=("OPEC", "Saudi Arabia oil", "OPEC+"),
        all_of=(),
        severity=EventSeverity.MEDIUM,
        tags=("opec", "oil", "supply", "saudi"),
        countries=("SA",),
    ),
    KeywordRule(
        name="fed-meeting",
        any_of=("FOMC", "Federal Reserve", "Powell", "Fed funds"),
        all_of=(),
        severity=EventSeverity.MEDIUM,
        tags=("fed", "monetary", "us", "rates"),
        countries=("US",),
    ),
    KeywordRule(
        name="ecb-meeting",
        any_of=("ECB", "Lagarde", "Frankfurt rate"),
        all_of=(),
        severity=EventSeverity.MEDIUM,
        tags=("ecb", "monetary", "eu", "rates"),
        countries=("EA",),
    ),
)


class NewsKeywordDetector:
    """Detect events by matching news headlines against keyword rules."""

    def __init__(self, rules: tuple[KeywordRule, ...] = DEFAULT_NEWS_RULES) -> None:
        self._rules = rules

    def detect(self, headlines: list[Headline]) -> Iterator[Event]:
        for h in headlines:
            text_lower = h.text.lower()
            for rule in self._rules:
                if not any(kw.lower() in text_lower for kw in rule.any_of):
                    continue
                if rule.all_of and not all(kw.lower() in text_lower for kw in rule.all_of):
                    continue
                yield Event(
                    event_id=f"news.{rule.name}.{h.headline_id}",
                    detected_at=h.published_at,
                    source=EventSource.NEWS,
                    severity=rule.severity,
                    title=h.text[:140],
                    summary=f"News matched rule '{rule.name}' from {h.source}",
                    tags=rule.tags,
                    related_countries=rule.countries,
                    metadata={"rule": rule.name, "outlet": h.source},
                )
