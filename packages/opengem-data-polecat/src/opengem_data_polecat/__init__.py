"""POLECAT (Cline Center) PLOVER-coded political event data adapter.

Per L021–L030 of the 300-loop research round, POLECAT is OPENGEM's strategic
substitute for ACLED — CC0 license, weekly cadence, PLOVER-coded events from
the Cline Center at the University of Illinois, hosted on Harvard Dataverse.

Public API:
    POLECATAdapter — pull weekly POLECAT releases, aggregate to country-month
    POLECAT_CATALOG — SeriesCatalog with the four derived series per country
    POLECAT_COUNTRIES — the country coverage tuple
"""

from opengem_data_polecat.adapter import POLECATAdapter
from opengem_data_polecat.catalog import POLECAT_CATALOG, POLECAT_COUNTRIES

__all__ = ["POLECAT_CATALOG", "POLECAT_COUNTRIES", "POLECATAdapter"]
__version__ = "0.1.0"
