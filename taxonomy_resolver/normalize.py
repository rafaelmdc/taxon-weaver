"""String normalization helpers for deterministic lookup preparation."""

from __future__ import annotations

import re

WHITESPACE_RE = re.compile(r"\s+")
VAGUE_LABEL_TOKENS = {
    "sp.",
    "spp.",
    "uncultured",
    "unclassified",
    "group",
    "cluster",
}


def normalize_name(name: str) -> str:
    """Normalize a user-entered taxon string for lookup.

    This intentionally stays conservative for the deterministic layer.
    It normalizes casing and spacing without attempting typo correction,
    abbreviation expansion, or taxonomy-aware rewriting.
    """

    normalized = name.strip().lower().replace("_", " ")
    return WHITESPACE_RE.sub(" ", normalized)


def looks_vague(name: str) -> bool:
    """Flag labels that should generally route to manual review."""

    normalized = normalize_name(name)
    return any(token in normalized.split() or token in normalized for token in VAGUE_LABEL_TOKENS)
