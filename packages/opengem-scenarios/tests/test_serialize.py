from __future__ import annotations

import json

from opengem_scenarios import default_library, pack_from_dict, pack_to_dict


def test_round_trip_each_pack() -> None:
    """Every pack in the default library must round-trip through JSON without loss."""
    lib = default_library()
    for pack in lib:
        d = pack_to_dict(pack)
        # JSON-safe?
        text = json.dumps(d)
        roundtrip_d = json.loads(text)
        restored = pack_from_dict(roundtrip_d)
        assert restored.pack_id == pack.pack_id
        assert restored.title == pack.title
        assert restored.tags == pack.tags
        # Shock comparisons
        assert len(restored.template.shocks) == len(pack.template.shocks)
        for s_a, s_b in zip(restored.template.shocks, pack.template.shocks, strict=True):
            assert s_a.country == s_b.country
            assert s_a.variable == s_b.variable
            assert s_a.magnitude == s_b.magnitude
            assert s_a.start_period == s_b.start_period


def test_serialized_pack_is_json_safe() -> None:
    lib = default_library()
    for pack in lib:
        d = pack_to_dict(pack)
        json.dumps(d)  # must not raise
