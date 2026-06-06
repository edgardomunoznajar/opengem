# opengem-data-polecat

POLECAT (POLitical Event Classification and Analysis Toolkit) adapter — CC0 from Harvard Dataverse.

Per L021–L030 of the 300-loop research round, POLECAT is OPENGEM's strategic substitute for ACLED:
weekly PLOVER-coded political events, public domain, 2018-present, weekly cadence.

This adapter pulls the latest POLECAT release, aggregates events to a country-month panel weighted
by the PLOVER Goldstein-Scale equivalent, and emits `Observation` rows compatible with the rest of
the OPENGEM data plane.

## Composite output

OPENGEM does not republish raw POLECAT events. Per L021–L030 license discipline (CC0 is permissive,
but parsimony is the editorial virtue), we publish **derived monthly composites**:

- `<ISO3>.POLECAT.event_count.country.M` — count of events in country per month
- `<ISO3>.POLECAT.goldstein_weighted.country.M` — Goldstein-Scale-weighted sum
- `<ISO3>.POLECAT.material_conflict.country.M` — material-conflict subset count
- `<ISO3>.POLECAT.verbal_conflict.country.M` — verbal-conflict subset count

## License

POLECAT raw data: CC0 (public domain). Cline Center attribution is included in every derived
Observation's `metadata` field as `source_attribution`.

OPENGEM derived series: CC-BY-4.0 (composite metrics) per repo policy.

## See also

- `opengem-data-gpr` — sibling Caldara-Iacoviello GPR adapter
- `opengem-data-gdelt` (pending) — sibling GDELT GKG adapter
- L024 — GPR/POLECAT/UCDP composite design
