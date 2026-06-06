from __future__ import annotations

from datetime import date, datetime

from opengem_event_detector import (
    Event,
    EventSeverity,
    EventSource,
    MarketThresholdDetector,
    NewsKeywordDetector,
    RuleEngine,
)
from opengem_event_detector.market import MarketSignal
from opengem_event_detector.news import Headline
from opengem_scenarios import default_library


def test_market_detector_term_spread_inverted() -> None:
    det = MarketThresholdDetector()
    events = list(
        det.detect(
            [
                MarketSignal("term_spread_10y_3m", -30.0, datetime(2026, 5, 25, 12, 0)),
                MarketSignal("term_spread_10y_3m", 50.0, datetime(2026, 5, 24, 12, 0)),
            ]
        )
    )
    assert len(events) == 1
    assert "recession" in events[0].tags


def test_market_detector_vix_spike() -> None:
    det = MarketThresholdDetector()
    events = list(det.detect([MarketSignal("vix", 42.0, datetime(2026, 5, 25))]))
    assert len(events) == 1
    assert events[0].severity == EventSeverity.HIGH
    assert "volatility" in events[0].tags


def test_market_detector_no_trigger() -> None:
    det = MarketThresholdDetector()
    events = list(
        det.detect(
            [
                MarketSignal("vix", 18.0, datetime(2026, 5, 25)),
                MarketSignal("term_spread_10y_3m", 75.0, datetime(2026, 5, 25)),
            ]
        )
    )
    assert events == []


def test_news_detector_ukraine() -> None:
    det = NewsKeywordDetector()
    headlines = [
        Headline("h1", "Putin announces partial mobilization in Donbas region", datetime(2026, 5, 25), "Reuters"),
    ]
    events = list(det.detect(headlines))
    assert len(events) >= 1
    assert any("russia" in e.tags for e in events)


def test_news_detector_taiwan() -> None:
    det = NewsKeywordDetector()
    headlines = [Headline("h2", "TSMC reports Taiwan production disruption", datetime(2026, 5, 25), "FT")]
    events = list(det.detect(headlines))
    assert len(events) >= 1
    assert any("taiwan" in e.tags for e in events)


def test_news_detector_unrelated_headline() -> None:
    det = NewsKeywordDetector()
    headlines = [Headline("h3", "Local bakery wins award", datetime(2026, 5, 25), "Local News")]
    events = list(det.detect(headlines))
    assert events == []


def test_rule_engine_triggers_pack() -> None:
    """A high-severity Ukraine event should fire the russia-ukraine-energy pack."""
    lib = default_library()
    engine = RuleEngine(library=lib)
    events = [
        Event(
            event_id="e1",
            detected_at=datetime(2026, 5, 25),
            source=EventSource.NEWS,
            severity=EventSeverity.HIGH,
            title="t",
            summary="s",
            tags=("russia", "ukraine"),
            related_countries=("RU", "UA"),
        )
    ]
    invocations = list(engine.trigger(events, invoked_at=date(2026, 5, 25)))
    assert len(invocations) == 1
    assert invocations[0].pack.pack_id == "russia-ukraine-energy"


def test_rule_engine_severity_floor() -> None:
    """LOW-severity events should not trigger HIGH-only rules."""
    lib = default_library()
    engine = RuleEngine(library=lib)
    events = [
        Event(
            event_id="e1",
            detected_at=datetime(2026, 5, 25),
            source=EventSource.NEWS,
            severity=EventSeverity.LOW,  # below the iran-israel min HIGH
            title="t",
            summary="s",
            tags=("iran", "israel"),
        )
    ]
    invocations = list(engine.trigger(events, invoked_at=date(2026, 5, 25)))
    assert invocations == []


def test_rule_engine_dedupes() -> None:
    """Multiple events for same pack should yield only one invocation."""
    lib = default_library()
    engine = RuleEngine(library=lib)
    events = [
        Event(
            event_id=f"e{i}",
            detected_at=datetime(2026, 5, 25),
            source=EventSource.NEWS,
            severity=EventSeverity.HIGH,
            title="t",
            summary="s",
            tags=("russia", "ukraine"),
        )
        for i in range(3)
    ]
    invocations = list(engine.trigger(events, invoked_at=date(2026, 5, 25)))
    assert len(invocations) == 1
