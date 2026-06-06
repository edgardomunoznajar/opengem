# opengem-data-ordra

🧪 alpha

OECD MEI Original Release Data and Revisions Analysis adapter — the **vintage
workhorse** for OPENGEM's non-US Tier-V coverage.

ORDRA preserves monthly vintage snapshots of MEI series back to **February 1999**,
covering all OECD member countries + Euro area + China + India + Brazil + South
Africa + Russia. The Dallas Fed historical extension reaches back to **1962** for
26 OECD founders.

Per R07: ORDRA + Dallas Fed = the Tier-V data foundation for ~26–35 countries.

## Access

ORDRA is accessed via the OECD SDMX 2.1 API at https://sdmx.oecd.org. No auth
required; rate-limited but generous.

## Catalog (initial)

OPENGEM canonical series IDs:

- `<country>.OECD.MEI.<variable>.<freq>`
  - e.g., `DE.OECD.MEI.gdp_real.Q`, `FR.OECD.MEI.cpi_headline.M`

Maps to ORDRA's SDMX-style keys:
- `MEI/<country>.<MEI_SUBJECT>.<MEASURE>.<FREQUENCY>` per ORDRA's schema.

## Vintage handling — critical

Unlike US adapters which use `date.today()` as a proxy for `vintage_at`, the
ORDRA adapter retrieves the **specific monthly vintage** keyed by the
`vintage_period` field. Each row from ORDRA carries its own (observed_at,
vintage_at) — true vintage discipline.
