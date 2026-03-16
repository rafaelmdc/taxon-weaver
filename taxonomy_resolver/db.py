"""SQLite access layer for taxonomy reference and cache state.

The resolver should keep SQL localized here so service and policy code remain
readable and testable.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

DEFAULT_DB_PATH: Path | None = None

SCHEMA_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS taxa (
        taxid INTEGER PRIMARY KEY,
        parent_taxid INTEGER NOT NULL,
        rank TEXT NOT NULL,
        is_root INTEGER NOT NULL DEFAULT 0,
        source_node_embl_code TEXT,
        division_id INTEGER,
        inherited_div_flag INTEGER,
        genetic_code_id INTEGER,
        inherited_gc_flag INTEGER,
        mitochondrial_genetic_code_id INTEGER,
        inherited_mgc_flag INTEGER,
        genbank_hidden_flag INTEGER,
        hidden_subtree_root_flag INTEGER,
        comments TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS taxon_names (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        taxid INTEGER NOT NULL,
        name_txt TEXT NOT NULL,
        unique_name TEXT,
        name_class TEXT NOT NULL,
        normalized_name TEXT NOT NULL,
        FOREIGN KEY (taxid) REFERENCES taxa(taxid)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS lineage_cache (
        taxid INTEGER PRIMARY KEY,
        lineage_json TEXT NOT NULL,
        superkingdom TEXT,
        phylum TEXT,
        class_name TEXT,
        order_name TEXT,
        family TEXT,
        genus TEXT,
        species TEXT,
        FOREIGN KEY (taxid) REFERENCES taxa(taxid)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS metadata (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS reviewed_mappings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_name TEXT NOT NULL,
        normalized_name TEXT NOT NULL,
        provided_level TEXT,
        resolved_taxid INTEGER,
        matched_scientific_name TEXT,
        match_type TEXT NOT NULL,
        status TEXT NOT NULL,
        score REAL,
        decision_action TEXT NOT NULL,
        taxonomy_build_version TEXT NOT NULL,
        reviewer TEXT,
        warnings_json TEXT NOT NULL,
        notes TEXT,
        created_at TEXT NOT NULL
    )
    """,
]

INDEX_STATEMENTS = [
    "CREATE INDEX IF NOT EXISTS idx_taxa_parent_taxid ON taxa(parent_taxid)",
    "CREATE INDEX IF NOT EXISTS idx_taxon_names_taxid ON taxon_names(taxid)",
    "CREATE INDEX IF NOT EXISTS idx_taxon_names_name_txt ON taxon_names(name_txt)",
    "CREATE INDEX IF NOT EXISTS idx_taxon_names_normalized_name ON taxon_names(normalized_name)",
    "CREATE INDEX IF NOT EXISTS idx_taxon_names_name_class ON taxon_names(name_class)",
    "CREATE INDEX IF NOT EXISTS idx_reviewed_mappings_norm_level ON reviewed_mappings(normalized_name, provided_level)",
]


def connect(db_path: Path | str | None = None) -> sqlite3.Connection:
    """Open a SQLite connection with row access by column name."""

    global DEFAULT_DB_PATH
    resolved_path = Path(db_path) if db_path is not None else get_default_db_path()
    connection = sqlite3.connect(resolved_path)
    connection.row_factory = sqlite3.Row
    DEFAULT_DB_PATH = resolved_path
    return connection


def get_default_db_path() -> Path:
    """Return the last database path used by the current process."""

    if DEFAULT_DB_PATH is None:
        raise RuntimeError("No default database path is set for the current process.")
    return DEFAULT_DB_PATH


def initialize_database(db_path: Path | str) -> None:
    """Create the reference and cache schema in a new or existing database."""

    with connect(db_path) as connection:
        for statement in SCHEMA_STATEMENTS:
            connection.execute(statement)
        for statement in INDEX_STATEMENTS:
            connection.execute(statement)
        connection.commit()


def clear_reference_tables(db_path: Path | str) -> None:
    """Remove reference-build data while preserving reviewed mapping history."""

    with connect(db_path) as connection:
        connection.execute("DELETE FROM lineage_cache")
        connection.execute("DELETE FROM taxon_names")
        connection.execute("DELETE FROM taxa")
        connection.execute("DELETE FROM metadata")
        connection.commit()


def insert_taxa_rows(rows: list[tuple[object, ...]], db_path: Path | str | None = None) -> None:
    """Bulk insert parsed taxa rows from `nodes.dmp`."""

    with connect(db_path or get_default_db_path()) as connection:
        connection.executemany(
            """
            INSERT INTO taxa(
                taxid,
                parent_taxid,
                rank,
                is_root,
                source_node_embl_code,
                division_id,
                inherited_div_flag,
                genetic_code_id,
                inherited_gc_flag,
                mitochondrial_genetic_code_id,
                inherited_mgc_flag,
                genbank_hidden_flag,
                hidden_subtree_root_flag,
                comments
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        connection.commit()


def insert_taxon_name_rows(
    rows: list[tuple[object, ...]], db_path: Path | str | None = None
) -> None:
    """Bulk insert parsed taxon name rows from `names.dmp`."""

    with connect(db_path or get_default_db_path()) as connection:
        connection.executemany(
            """
            INSERT INTO taxon_names(
                taxid,
                name_txt,
                unique_name,
                name_class,
                normalized_name
            ) VALUES (?, ?, ?, ?, ?)
            """,
            rows,
        )
        connection.commit()


def insert_lineage_rows(
    rows: list[tuple[object, ...]], db_path: Path | str | None = None
) -> None:
    """Bulk insert materialized lineage cache rows."""

    with connect(db_path or get_default_db_path()) as connection:
        connection.executemany(
            """
            INSERT INTO lineage_cache(
                taxid,
                lineage_json,
                superkingdom,
                phylum,
                class_name,
                order_name,
                family,
                genus,
                species
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        connection.commit()


def upsert_metadata(db_path: Path | str, items: dict[str, str]) -> None:
    """Persist build metadata used for reproducibility and cache reuse."""

    with connect(db_path) as connection:
        connection.executemany(
            """
            INSERT INTO metadata(key, value)
            VALUES(?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """,
            items.items(),
        )
        connection.commit()
