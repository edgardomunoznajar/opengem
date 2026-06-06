from __future__ import annotations

import json
from datetime import date

from opengem_scenarios import ScenarioInvocation, default_library

from opengem_digest import Digest, DigestBuilder, SituationSnapshot, render_markdown


def test_digest_build_basic() -> None:
    lib = default_library()
    pack = lib.get("fed-plus-100bp")
    inv = ScenarioInvocation(pack=pack, invoked_at=date(2026, 5, 25), magnitude_scale=1.0)

    builder = DigestBuilder()
    digest = builder.build(
        as_of=date(2026, 5, 25),
        invocations=[inv],
        situation=SituationSnapshot(
            recession_probability_us_12m=0.18,
            recession_probability_model="bauer_mertens_us_12m",
            term_spread_10y_3m_bp=42.0,
        ),
        data_sources=("BEA", "BLS", "FRB", "BIS"),
    )
    assert digest.digest_id == "20260525"
    assert len(digest.scenarios) == 1
    assert digest.scenarios[0].pack_id == "fed-plus-100bp"
    assert digest.scenarios[0].diff_from_yesterday == "new"


def test_digest_diff_unchanged_when_in_previous() -> None:
    lib = default_library()
    pack = lib.get("fed-plus-100bp")
    inv = ScenarioInvocation(pack=pack, invoked_at=date(2026, 5, 25))

    builder = DigestBuilder()
    digest = builder.build(
        as_of=date(2026, 5, 25),
        invocations=[inv],
        situation=SituationSnapshot(),
        previous_pack_ids={"fed-plus-100bp"},
    )
    assert digest.scenarios[0].diff_from_yesterday == "unchanged"


def test_digest_to_dict_json_safe() -> None:
    lib = default_library()
    inv = ScenarioInvocation(pack=lib.get("russia-ukraine-energy"), invoked_at=date(2026, 5, 25))

    builder = DigestBuilder()
    digest = builder.build(
        as_of=date(2026, 5, 25),
        invocations=[inv],
        situation=SituationSnapshot(recession_probability_us_12m=0.5),
    )
    d = digest.to_dict()
    text = json.dumps(d)  # must not raise
    assert "20260525" in text
    assert "russia-ukraine-energy" in text


def test_render_markdown_contains_essentials() -> None:
    lib = default_library()
    inv = ScenarioInvocation(pack=lib.get("china-taiwan-disruption"), invoked_at=date(2026, 5, 25))

    builder = DigestBuilder()
    digest = builder.build(
        as_of=date(2026, 5, 25),
        invocations=[inv],
        situation=SituationSnapshot(
            recession_probability_us_12m=0.18,
            recession_probability_model="bauer_mertens_us_12m",
            gpr_global_latest=142.0,
            gpr_global_zscore=1.5,
        ),
        data_sources=("BIS", "ORDRA"),
    )
    md = render_markdown(digest)
    assert "OPENGEM Daily Digest" in md
    assert "2026-05-25" in md
    assert "Situation" in md
    assert "Recession probability" in md
    assert "Scenarios" in md
    assert "China-Taiwan" in md
    assert "```json" in md  # the paste-into-ChatGPT block
    assert "BIS" in md
    assert "ORDRA" in md


def test_render_markdown_handles_empty_situation() -> None:
    builder = DigestBuilder()
    digest = builder.build(
        as_of=date(2026, 5, 25),
        invocations=[],
        situation=SituationSnapshot(),
    )
    md = render_markdown(digest)
    assert "No situation data available" in md
    assert "No scenarios triggered today" in md


def test_render_markdown_with_events() -> None:
    builder = DigestBuilder()
    digest = builder.build(
        as_of=date(2026, 5, 25),
        invocations=[],
        situation=SituationSnapshot(),
        events_summary=[
            {"severity": "HIGH", "title": "Iran-Israel escalation overnight"},
        ],
    )
    md = render_markdown(digest)
    assert "Events detected" in md
    assert "Iran-Israel" in md
    assert "HIGH" in md


def test_render_markdown_conditional_framing_present() -> None:
    """The digest renders the epistemic contract: every value conditional + based-on."""
    lib = default_library()
    inv = ScenarioInvocation(pack=lib.get("fed-plus-100bp"), invoked_at=date(2026, 5, 25))
    builder = DigestBuilder()
    digest = builder.build(
        as_of=date(2026, 5, 25),
        invocations=[inv],
        situation=SituationSnapshot(
            recession_probability_us_12m=0.18,
            recession_probability_model="bauer_mertens_us_12m_v1",
        ),
    )
    md = render_markdown(digest)
    assert "conditional" in md.lower()
    assert "could happen" in md.lower()
    # The recession-probability row should carry "based on"
    assert "based on bauer_mertens" in md.lower()
