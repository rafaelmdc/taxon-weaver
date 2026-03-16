"""Lineage access helpers.

Phase 2 and Phase 5 will populate and query lineage data from the taxonomy DB.
"""

from __future__ import annotations

from pathlib import Path

from .db import fetch_lineage_entries
from .schemas import LineageEntry


def get_lineage_for_taxid(db_path: str | Path, taxid: int) -> list[LineageEntry]:
    """Return cached lineage entries for a taxid."""

    return [
        LineageEntry(
            taxid=int(entry["taxid"]),
            rank=str(entry["rank"]),
            name=str(entry["name"]),
        )
        for entry in fetch_lineage_entries(db_path, taxid)
    ]
