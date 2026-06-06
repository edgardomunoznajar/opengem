from __future__ import annotations

import json
from datetime import date

import pytest

from opengem_digest import DigestBuilder, SituationSnapshot
from opengem_scenarios import ScenarioInvocation, default_library

from opengem_narrative import (
    NarrativeOutput,
    NarrativeRequest,
    build_narrative_request,
    get_system_prompt,
)


def test_system_prompts_known() -> None:
    p1 = get_system_prompt("analyst_segment_v1")
    p2 = get_system_prompt("executive_summary_v1")
    p3 = get_system_prompt("scenario_table_v1")
    assert "Do not invent numbers" in p1
    assert "executive summary" in p2.lower()
    assert "comparison" in p3.lower()


def test_system_prompt_unknown_rejected() -> None:
    with pytest.raises(KeyError):
        get_system_prompt("nonexistent_format")


def test_build_narrative_request_from_digest() -> None:
    lib = default_library()
    inv = ScenarioInvocation(pack=lib.get("china-taiwan-disruption"), invoked_at=date(2026, 5, 25))
    builder = DigestBuilder()
    digest = builder.build(
        as_of=date(2026, 5, 25),
        invocations=[inv],
        situation=SituationSnapshot(
            recession_probability_us_12m=0.22,
            recession_probability_model="bauer_mertens",
            gpr_global_latest=180.0,
        ),
    )
    req = build_narrative_request(digest.scenarios[0], situation=digest.situation)
    assert req.pack_id == "china-taiwan-disruption"
    assert req.format == "analyst_segment_v1"
    assert req.spec_json["scenario_id"].startswith("china-taiwan-disruption")
    assert req.situation["recession_probability_us_12m"] == 0.22
    assert req.situation["gpr_global_latest"] == 180.0


def test_narrative_request_round_trips_json() -> None:
    lib = default_library()
    inv = ScenarioInvocation(pack=lib.get("fed-plus-100bp"), invoked_at=date(2026, 5, 25))
    builder = DigestBuilder()
    digest = builder.build(as_of=date(2026, 5, 25), invocations=[inv], situation=SituationSnapshot())
    req = build_narrative_request(digest.scenarios[0], situation=digest.situation)
    text = req.to_json()
    d = json.loads(text)
    # The fields are present
    assert d["pack_id"] == "fed-plus-100bp"
    assert "spec_json" in d
    assert "format" in d


def test_narrative_output_from_dict() -> None:
    """The expected LLM response format parses cleanly."""
    response = {
        "title": "Fed +100bp surprise — what it means",
        "paragraphs": [
            "The Fed's surprise +100bp hike shifts the curve...",
            "OPENGEM models US real GDP -1pp at 4Q...",
            "Caveats: identification relies on...",
        ],
        "caveats": ["Identification via structural restriction"],
        "citations": ["Romer & Romer (2004) AER"],
    }
    out = NarrativeOutput.from_dict(response)
    assert len(out.paragraphs) == 3
    assert "Fed" in out.title


def test_narrative_request_respects_user_notes() -> None:
    lib = default_library()
    inv = ScenarioInvocation(pack=lib.get("opec-supply-cut"), invoked_at=date(2026, 5, 25))
    builder = DigestBuilder()
    digest = builder.build(as_of=date(2026, 5, 25), invocations=[inv], situation=SituationSnapshot())
    req = build_narrative_request(
        digest.scenarios[0],
        situation=digest.situation,
        user_notes="Focus on EU inflation pass-through for the video angle.",
    )
    assert "EU inflation" in req.user_notes
    d = req.to_dict()
    assert "user_notes" in d
