"""Supervised fuzzy suggestion layer placeholder.

Phase 6 will add candidate generation and scoring without altering the
deterministic-first resolution order.
"""

from __future__ import annotations

from .schemas import CandidateMatch, ResolveRequest


def suggest_fuzzy_candidates(_request: ResolveRequest) -> list[CandidateMatch]:
    """Return review-only fuzzy candidates when implemented."""

    return []
