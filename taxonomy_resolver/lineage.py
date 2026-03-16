"""Lineage access helpers.

Phase 2 and Phase 5 will populate and query lineage data from the taxonomy DB.
"""

from __future__ import annotations

from .schemas import LineageEntry


def get_lineage_for_taxid(_taxid: int) -> list[LineageEntry]:
    """Return a lineage list for the requested taxid when implemented."""

    return []
