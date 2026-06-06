"""RunProvenance — the hash quintuple that makes every forecast reproducible."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class RunProvenance:
    """The hash quintuple anchoring every published forecast.

    `run_id` is a human-friendly canonical short reference, typically
    `YYYYMMDD-<short_posterior_hash>`.
    """

    run_id: str
    code_sha: str  # git commit SHA + lockfile hash
    vintage_hash: str  # 'sha256:...'
    prior_hash: str  # 'sha256:...'
    posterior_hash: str  # 'sha256:...'
    started_at: datetime
    completed_at: datetime
    superseded_by: str | None = None  # later run_id if this one was corrected

    def __post_init__(self) -> None:
        if not self.run_id:
            raise ValueError("run_id required")
        for h in (self.vintage_hash, self.prior_hash, self.posterior_hash):
            if not h.startswith("sha256:"):
                raise ValueError(f"Hash must start with 'sha256:', got {h!r}")
