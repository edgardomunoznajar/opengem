"""DigestBuilder — composes a Digest from triggered ScenarioInvocations + situation data."""

from __future__ import annotations

from datetime import date
from typing import Any

from opengem_scenarios import ScenarioInvocation
from opengem_scenarios.serialize import _spec_to_dict

from opengem_digest.digest import Digest, ScenarioSection, SituationSnapshot


class DigestBuilder:
    """Composes a Digest. Stateless; safe to instantiate per build."""

    def build(
        self,
        *,
        as_of: date,
        invocations: list[ScenarioInvocation],
        situation: SituationSnapshot,
        events_summary: list[dict[str, Any]] | None = None,
        previous_pack_ids: set[str] | None = None,
        data_sources: tuple[str, ...] = (),
    ) -> Digest:
        """Build a Digest.

        `previous_pack_ids`: pack ids that were in yesterday's digest, used to
        annotate `diff_from_yesterday` ('new' vs 'unchanged').
        """
        previous = previous_pack_ids or set()
        sections: list[ScenarioSection] = []
        for inv in invocations:
            spec = inv.resolve()
            sections.append(
                ScenarioSection(
                    pack_id=inv.pack.pack_id,
                    title=inv.pack.title,
                    summary=inv.pack.summary,
                    invoked_at=inv.invoked_at,
                    spec_json=_spec_to_dict(spec),
                    rationale=inv.pack.rationale,
                    references=inv.pack.references,
                    diff_from_yesterday=(
                        "unchanged" if inv.pack.pack_id in previous else "new"
                    ),
                    notes=inv.notes,
                )
            )

        digest_id = as_of.strftime("%Y%m%d")
        return Digest(
            digest_id=digest_id,
            as_of=as_of,
            situation=situation,
            scenarios=tuple(sections),
            events_summary=tuple(events_summary or ()),
            data_sources=data_sources,
        )
