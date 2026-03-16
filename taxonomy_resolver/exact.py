"""Deterministic lookup layer.

This module intentionally contains only placeholders in the first scaffold.
Phase 5 will implement query logic against scientific names, synonyms, and
normalized matches.
"""

from __future__ import annotations

from .schemas import ResolveRequest, ResolveResult


def resolve_exact(_request: ResolveRequest) -> ResolveResult | None:
    """Return a deterministic result if a single safe match exists."""

    return None
