"""opengem-datasette — export OPENGEM vintages to SQLite for public publication.

Public API:
    snapshot_to_sqlite    — write a self-contained .db given a vintage store
    write_metadata        — emit Datasette metadata.yaml
"""

from opengem_datasette.snapshot import snapshot_to_sqlite, write_metadata

__all__ = ["snapshot_to_sqlite", "write_metadata"]
__version__ = "0.1.0"
