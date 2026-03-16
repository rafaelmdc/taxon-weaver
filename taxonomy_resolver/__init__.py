"""Public package surface for the taxonomy resolver foundation."""

from .policy import MatchType, ResolutionStatus, WarningCode
from .schemas import (
    BatchResolveRequest,
    BatchResolveResult,
    CandidateMatch,
    DecisionAction,
    DecisionRecord,
    LineageEntry,
    ResolveRequest,
    ResolveResult,
)
from .service import TaxonomyResolverService

__all__ = [
    "BatchResolveRequest",
    "BatchResolveResult",
    "CandidateMatch",
    "DecisionAction",
    "DecisionRecord",
    "LineageEntry",
    "MatchType",
    "ResolveRequest",
    "ResolveResult",
    "ResolutionStatus",
    "TaxonomyResolverService",
    "WarningCode",
]
