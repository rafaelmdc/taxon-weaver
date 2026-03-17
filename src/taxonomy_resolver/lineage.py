"""Lineage access helpers.

Phase 2 and Phase 5 will populate and query lineage data from the taxonomy DB.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .db import fetch_lineage_entries
from .schemas import LineageEntry

DatabaseHandle = sqlite3.Connection | str | Path


def lineage_entries_from_json(lineage_json: str | None) -> list[LineageEntry]:
    """Deserialize lineage JSON already fetched with a candidate row."""

    if not lineage_json:
        return []
    return [
        LineageEntry(
            taxid=int(entry["taxid"]),
            rank=str(entry["rank"]),
            name=str(entry["name"]),
        )
        for entry in json.loads(lineage_json)
    ]


def get_lineage_for_taxid(db_path: DatabaseHandle, taxid: int) -> list[LineageEntry]:
    """Return cached lineage entries for a taxid."""

    return [
        LineageEntry(
            taxid=int(entry["taxid"]),
            rank=str(entry["rank"]),
            name=str(entry["name"]),
        )
        for entry in fetch_lineage_entries(db_path, taxid)
    ]
