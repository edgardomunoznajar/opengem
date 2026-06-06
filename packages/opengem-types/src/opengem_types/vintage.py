"""VintageSnapshot — manifest of a vintage pull, with content hash."""

from __future__ import annotations

import hashlib
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime

from opengem_types.observation import Observation


@dataclass(frozen=True, slots=True)
class VintageSnapshot:
    """Manifest of a vintage pull.

    The `vintage_hash` is deterministic over the canonical serialization of the
    observations (sorted by series_id then observed_at then vintage_at).
    """

    vintage_hash: str  # 'sha256:<hex>'
    pulled_at: datetime
    source_id: str
    series_count: int
    observation_count: int
    manifest: dict[str, int] = field(default_factory=dict)  # series_id -> obs_count

    @classmethod
    def from_observations(
        cls, observations: Iterable[Observation], source_id: str, pulled_at: datetime
    ) -> VintageSnapshot:
        """Compute a deterministic snapshot manifest from a collection of observations."""
        obs_list = sorted(
            observations,
            key=lambda o: (str(o.series_id), o.observed_at.isoformat(), o.vintage_at.isoformat()),
        )

        canonical_lines = [
            f"{o.series_id}|{o.observed_at.isoformat()}|{o.vintage_at.isoformat()}|{_canon_value(o.value)}"
            for o in obs_list
        ]
        canonical = "\n".join(canonical_lines).encode("utf-8")
        digest = hashlib.sha256(canonical).hexdigest()

        manifest: dict[str, int] = {}
        for o in obs_list:
            sid = str(o.series_id)
            manifest[sid] = manifest.get(sid, 0) + 1

        return cls(
            vintage_hash=f"sha256:{digest}",
            pulled_at=pulled_at,
            source_id=source_id,
            series_count=len(manifest),
            observation_count=len(obs_list),
            manifest=manifest,
        )


def _canon_value(v: float | None) -> str:
    """Canonical string for a value — None becomes 'NA'; floats use repr() for IEEE-exact roundtrip."""
    if v is None:
        return "NA"
    # repr() of a finite Python float is the shortest string that roundtrips exactly via float().
    return repr(float(v))
