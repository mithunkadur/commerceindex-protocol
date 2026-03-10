"""CommerceIndex SDK — The commerce layer for AI agents."""

from commerceindex.client import CommerceIndex
from commerceindex.models import (
    Agent,
    CIScore,
    ScoreBreakdown,
    Task,
    TaskAssignment,
    TaskSubmission,
    A2ASession,
    Escrow,
    Earning,
    CommerceEvent,
)
from commerceindex.exceptions import (
    CommerceIndexError,
    AuthenticationError,
    InsufficientTierError,
    InsufficientScoreError,
    NotFoundError,
    ConflictError,
    RateLimitError,
    InvalidStateError,
)

__version__ = "0.1.0"

__all__ = [
    "CommerceIndex",
    "Agent",
    "CIScore",
    "ScoreBreakdown",
    "Task",
    "TaskAssignment",
    "TaskSubmission",
    "A2ASession",
    "Escrow",
    "Earning",
    "CommerceEvent",
    "CommerceIndexError",
    "AuthenticationError",
    "InsufficientTierError",
    "InsufficientScoreError",
    "NotFoundError",
    "ConflictError",
    "RateLimitError",
    "InvalidStateError",
]
