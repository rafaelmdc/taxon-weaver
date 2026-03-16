"""CLI entry point for building the taxonomy reference database."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import urllib.request

from taxonomy_resolver.build import build_taxonomy_database

DEFAULT_TAXDUMP_URL = "https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz"


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for the database bootstrap command."""

    parser = argparse.ArgumentParser(
        description="Build the taxonomy SQLite database from an NCBI taxdump archive."
    )
    parser.add_argument("--dump", required=True, help="Path to NCBI taxdump.tar.gz")
    parser.add_argument("--db", required=True, help="Output SQLite database path")
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download the NCBI taxdump archive to --dump before building the database",
    )
    parser.add_argument(
        "--download-url",
        default=DEFAULT_TAXDUMP_URL,
        help="Source URL used when --download is enabled",
    )
    parser.add_argument(
        "--report-json",
        help="Optional path for writing the build summary as JSON",
    )
    return parser.parse_args()


def download_taxdump(url: str, destination: Path) -> None:
    """Download the NCBI taxdump archive to a local path.

    The builder still operates on a local archive file. This helper simply adds
    an optional one-step fetch phase before the normal local build path.
    """

    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as response, destination.open("wb") as handle:
        shutil.copyfileobj(response, handle)


def main() -> None:
    """Run the CLI bootstrap command."""

    args = parse_args()
    dump_path = Path(args.dump)
    if args.download:
        print(f"Downloading NCBI taxdump to {dump_path}")
        download_taxdump(args.download_url, dump_path)

    summary = build_taxonomy_database(dump_path, Path(args.db))

    if args.report_json:
        report_path = Path(args.report_json)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(summary.to_dict(), indent=2), encoding="utf-8")

    print(f"Built taxonomy database at {summary.db_path}")
    print(f"Taxonomy build version: {summary.taxonomy_build_version}")
    print(f"Taxa: {summary.taxa_count}")
    print(f"Names: {summary.name_count}")
    print(f"Scientific names: {summary.scientific_name_count}")
    print(f"Synonyms/non-scientific names: {summary.synonym_count}")
    print(f"Lineage cache rows: {summary.lineage_cache_count}")
    print(f"Validation checks: {json.dumps(summary.validation_checks, sort_keys=True)}")


if __name__ == "__main__":
    main()
