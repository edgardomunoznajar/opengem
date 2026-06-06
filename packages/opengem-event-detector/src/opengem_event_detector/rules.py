"""RuleEngine — maps detected events to scenario-pack invocations."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import date

from opengem_scenarios import ScenarioInvocation, ScenarioLibrary
from opengem_scenarios.pack import ScenarioPack

from opengem_event_detector.event import Event, EventSeverity


@dataclass(frozen=True, slots=True)
class TriggerRule:
    """When `any_tag` matches an event tag, invoke `pack_id` at given scale."""

    any_tag: tuple[str, ...]
    pack_id: str
    min_severity: EventSeverity = EventSeverity.MEDIUM
    magnitude_scale: float = 1.0
    notes: str = ""


# IOC trigger map: event tags → scenario packs
DEFAULT_TRIGGER_RULES: tuple[TriggerRule, ...] = (
    TriggerRule(
        any_tag=("russia", "ukraine", "energy"),
        pack_id="russia-ukraine-energy",
        notes="auto-triggered from RU/UA news",
    ),
    TriggerRule(
        any_tag=("taiwan", "china",),
        pack_id="china-taiwan-disruption",
        min_severity=EventSeverity.HIGH,
        notes="auto-triggered from Taiwan headlines",
    ),
    TriggerRule(
        any_tag=("iran", "israel", "hormuz"),
        pack_id="iran-israel-escalation",
        min_severity=EventSeverity.HIGH,
        notes="auto-triggered from Iran-Israel events",
    ),
    TriggerRule(
        any_tag=("opec",),
        pack_id="opec-supply-cut",
        notes="auto-triggered from OPEC announcements",
    ),
    TriggerRule(
        any_tag=("fed", "monetary", "rates"),
        pack_id="fed-plus-100bp",
        notes="auto-triggered from Fed-related news",
    ),
    TriggerRule(
        any_tag=("recession", "yield-curve"),
        pack_id="global-recession-trigger",
        min_severity=EventSeverity.HIGH,
        notes="auto-triggered from term-spread inversion",
    ),
)


_SEVERITY_RANK = {
    EventSeverity.LOW: 0,
    EventSeverity.MEDIUM: 1,
    EventSeverity.HIGH: 2,
    EventSeverity.CRITICAL: 3,
}


class RuleEngine:
    """Maps Events to ScenarioInvocations via configurable rules."""

    def __init__(
        self,
        library: ScenarioLibrary,
        rules: tuple[TriggerRule, ...] = DEFAULT_TRIGGER_RULES,
    ) -> None:
        self._library = library
        self._rules = rules

    def trigger(self, events: list[Event], *, invoked_at: date) -> Iterator[ScenarioInvocation]:
        """Yield ScenarioInvocations for events that match trigger rules.

        Deduplicates: at most one invocation per pack_id per call.
        """
        emitted: set[str] = set()
        for event in events:
            event_rank = _SEVERITY_RANK[event.severity]
            for rule in self._rules:
                if rule.pack_id in emitted:
                    continue
                if event_rank < _SEVERITY_RANK[rule.min_severity]:
                    continue
                if not _any_tag_overlap(event.tags, rule.any_tag):
                    continue
                pack = self._library.get(rule.pack_id)
                emitted.add(rule.pack_id)
                yield ScenarioInvocation(
                    pack=pack,
                    invoked_at=invoked_at,
                    magnitude_scale=rule.magnitude_scale,
                    notes=rule.notes,
                )


def _any_tag_overlap(a: tuple[str, ...], b: tuple[str, ...]) -> bool:
    a_low = {x.lower() for x in a}
    b_low = {x.lower() for x in b}
    return bool(a_low & b_low)
