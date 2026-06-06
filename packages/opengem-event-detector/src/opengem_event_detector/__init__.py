"""Event detection + scenario-pack triggering."""

from opengem_event_detector.event import Event, EventSeverity, EventSource
from opengem_event_detector.market import MarketThresholdDetector
from opengem_event_detector.news import NewsKeywordDetector
from opengem_event_detector.rules import RuleEngine, TriggerRule

__all__ = [
    "Event",
    "EventSeverity",
    "EventSource",
    "MarketThresholdDetector",
    "NewsKeywordDetector",
    "RuleEngine",
    "TriggerRule",
]
__version__ = "0.1.0"
