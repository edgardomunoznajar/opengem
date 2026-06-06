"""End-to-end Stratfor-grade demo.

Demonstrates the full friend-facing workflow:
  news headlines + market signals
  → event detection
  → rule engine fires scenario packs
  → digest builder composes the daily output
  → narrative builder produces paste-ready JSON for ChatGPT
  → renders to markdown

This is the **headline product surface** demonstration — what the friend (the
international-politics YouTuber) will use every morning.
"""

from __future__ import annotations

import json
from datetime import date, datetime

from opengem_digest import DigestBuilder, SituationSnapshot, render_markdown
from opengem_event_detector import (
    Event,
    MarketThresholdDetector,
    NewsKeywordDetector,
    RuleEngine,
)
from opengem_event_detector.market import MarketSignal
from opengem_event_detector.news import Headline
from opengem_narrative import build_narrative_request, get_system_prompt
from opengem_recession_prob import recession_probability
from opengem_scenarios import default_library


def test_full_pipeline_iran_israel_morning() -> None:
    """A morning where Iran-Israel news + Hormuz risk is on the wire.

    Demonstrates:
    1. News detector fires on the headline
    2. Rule engine maps the event to the iran-israel-escalation pack
    3. Digest builder composes the day's digest
    4. Narrative builder produces ChatGPT-ready request JSON
    5. Markdown renders correctly
    """
    as_of = date(2026, 5, 25)

    # 1. Overnight signals
    headlines = [
        Headline(
            "wire-001",
            "Iran-Israel tensions surge after Tehran missile launch; Hormuz risk",
            datetime(2026, 5, 25, 4, 30),
            "Reuters",
        ),
    ]
    market_signals = [
        MarketSignal("term_spread_10y_3m", 15.0, datetime(2026, 5, 25, 6, 0)),
        MarketSignal("vix", 22.0, datetime(2026, 5, 25, 6, 0)),
    ]

    news_detector = NewsKeywordDetector()
    market_detector = MarketThresholdDetector()
    events: list[Event] = list(news_detector.detect(headlines))
    events.extend(market_detector.detect(market_signals))

    # 2. Rule engine fires scenario packs
    lib = default_library()
    engine = RuleEngine(library=lib)
    invocations = list(engine.trigger(events, invoked_at=as_of))
    # Should have triggered iran-israel-escalation
    pack_ids = [inv.pack.pack_id for inv in invocations]
    assert "iran-israel-escalation" in pack_ids

    # 3. Recession probability (Situation Subsystem)
    rec = recession_probability(spread_bp=15.0, as_of=as_of)

    # 4. Compose digest
    situation = SituationSnapshot(
        recession_probability_us_12m=rec.probability,
        recession_probability_model=rec.model_id,
        term_spread_10y_3m_bp=15.0,
        vix_latest=22.0,
    )
    digest = DigestBuilder().build(
        as_of=as_of,
        invocations=invocations,
        situation=situation,
        events_summary=[
            {"severity": e.severity.value.upper(), "title": e.title} for e in events
        ],
        data_sources=("BIS", "FRB", "ORDRA"),
    )

    # 5. Produce narrative request for the Iran-Israel pack
    iran_section = next(s for s in digest.scenarios if s.pack_id == "iran-israel-escalation")
    request = build_narrative_request(iran_section, situation=digest.situation)
    system_prompt = get_system_prompt(request.format)

    # Assertions: the request is paste-ready and self-contained
    assert "Do not invent numbers" in system_prompt
    request_json = request.to_json()
    parsed = json.loads(request_json)
    assert parsed["pack_id"] == "iran-israel-escalation"
    assert "spec_json" in parsed
    assert "shocks" in parsed["spec_json"]
    assert parsed["situation"]["term_spread_10y_3m_bp"] == 15.0

    # 6. Markdown renders the full digest
    md = render_markdown(digest)
    assert "Iran-Israel" in md
    assert "2026-05-25" in md
    assert "```json" in md  # ChatGPT-paste block included


def test_full_pipeline_quiet_morning() -> None:
    """A morning where no events trigger — digest should still render with a 'no scenarios' note."""
    as_of = date(2026, 5, 26)
    headlines = [Headline("h1", "Local bakery wins community award", datetime(2026, 5, 26), "Local News")]
    market_signals = [MarketSignal("vix", 14.0, datetime(2026, 5, 26))]

    events = list(NewsKeywordDetector().detect(headlines))
    events.extend(MarketThresholdDetector().detect(market_signals))

    lib = default_library()
    invocations = list(RuleEngine(library=lib).trigger(events, invoked_at=as_of))
    assert invocations == []

    digest = DigestBuilder().build(
        as_of=as_of,
        invocations=invocations,
        situation=SituationSnapshot(),
    )
    md = render_markdown(digest)
    assert "No scenarios triggered today" in md


def test_full_pipeline_multiple_concurrent_triggers() -> None:
    """A morning with multiple high-severity events: Russia-Ukraine + Taiwan + Fed."""
    as_of = date(2026, 5, 27)
    headlines = [
        Headline("h1", "Putin Donbas escalation; energy markets jolt", datetime(2026, 5, 27, 1), "Reuters"),
        Headline("h2", "Taiwan tensions surge as Beijing announces drills near TSMC", datetime(2026, 5, 27, 2), "FT"),
        Headline("h3", "FOMC minutes signal hawkish shift; Powell says rates higher for longer", datetime(2026, 5, 27, 3), "Bloomberg"),
    ]
    events = list(NewsKeywordDetector().detect(headlines))

    lib = default_library()
    invocations = list(RuleEngine(library=lib).trigger(events, invoked_at=as_of))
    pack_ids = {inv.pack.pack_id for inv in invocations}
    assert "russia-ukraine-energy" in pack_ids
    assert "china-taiwan-disruption" in pack_ids
    assert "fed-plus-100bp" in pack_ids

    digest = DigestBuilder().build(
        as_of=as_of,
        invocations=invocations,
        situation=SituationSnapshot(),
    )
    md = render_markdown(digest)
    # All three triggered packs visible
    assert "Russia-Ukraine" in md
    assert "China-Taiwan" in md
    assert "Fed surprise" in md
