"""CLI entry point for resolving one organism string."""

from __future__ import annotations

import argparse
import json

from taxonomy_resolver.schemas import ResolveRequest
from taxonomy_resolver.service import TaxonomyResolverService


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for single-name resolution."""

    parser = argparse.ArgumentParser(description="Resolve one organism name.")
    parser.add_argument("name", help="Organism name to resolve")
    parser.add_argument("--db", required=True, help="Path to taxonomy SQLite database")
    parser.add_argument("--level", help="Optional curator-provided taxonomic level")
    return parser.parse_args()


def main() -> None:
    """Resolve one name and print the structured result as JSON."""

    args = parse_args()
    service = TaxonomyResolverService(taxonomy_db_path=args.db)
    result = service.resolve_name(
        ResolveRequest(original_name=args.name, provided_level=args.level)
    )
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
