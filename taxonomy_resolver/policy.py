"""Shared status and warning definitions for resolver workflows.

Keeping workflow vocabulary in one place prevents CLI, services, and later
Django integration from drifting into incompatible string literals.
"""

from __future__ import annotations

from enum import StrEnum


class ResolutionStatus(StrEnum):
    """High-level machine and review statuses used across the project."""

    RESOLVED_EXACT_SCIENTIFIC = "resolved_exact_scientific"
    RESOLVED_EXACT_SYNONYM = "resolved_exact_synonym"
    RESOLVED_NORMALIZED = "resolved_normalized"
    SUGGESTED_FUZZY_UNIQUE = "suggested_fuzzy_unique"
    AMBIGUOUS_FUZZY_MULTIPLE = "ambiguous_fuzzy_multiple"
    UNRESOLVED_VAGUE_LABEL = "unresolved_vague_label"
    UNRESOLVED_NO_MATCH = "unresolved_no_match"
    MANUAL_REVIEW_REQUIRED = "manual_review_required"
    CONFIRMED_BY_USER = "confirmed_by_user"
    REJECTED_BY_USER = "rejected_by_user"
    LEVEL_CONFLICT = "level_conflict"


class MatchType(StrEnum):
    """How a candidate or resolved taxon was reached."""

    EXACT_SCIENTIFIC = "exact_scientific"
    EXACT_SYNONYM = "exact_synonym"
    NORMALIZED = "normalized"
    FUZZY = "fuzzy"
    CACHED = "cached"
    USER_CONFIRMED = "user_confirmed"
    USER_SELECTED = "user_selected"
    NONE = "none"


class WarningCode(StrEnum):
    """Non-terminal annotations that downstream consumers should surface."""

    PROVIDED_LEVEL_CONFLICT = "provided_level_conflict"
    MULTIPLE_EXACT_CANDIDATES = "multiple_exact_candidates"
    MULTIPLE_FUZZY_CANDIDATES = "multiple_fuzzy_candidates"
    SYNONYM_MATCHED = "synonym_matched"
    NORMALIZED_MATCHED = "normalized_matched"
    VAGUE_LABEL_DETECTED = "vague_label_detected"
    PLACEHOLDER_LABEL_DETECTED = "placeholder_label_detected"
    CACHED_DECISION_REUSED = "cached_decision_reused"
    NOT_IMPLEMENTED = "not_implemented"
