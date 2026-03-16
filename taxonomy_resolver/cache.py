"""Reviewed mapping cache interface.

The first scaffold defines the boundary only. Phase 9 will implement reuse
rules and storage-backed lookup/write behavior.
"""

from __future__ import annotations

from .schemas import DecisionRecord, ResolveRequest


def lookup_reviewed_mapping(_request: ResolveRequest) -> DecisionRecord | None:
    """Return a reusable reviewed mapping if one is available."""

    return None


def record_reviewed_mapping(_decision: DecisionRecord) -> None:
    """Persist a reviewed mapping decision when implemented."""

    return None
