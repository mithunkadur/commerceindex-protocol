"""CommerceIndex SDK exceptions."""


class CommerceIndexError(Exception):
    """Base exception for all CommerceIndex errors."""

    def __init__(self, message: str, status_code: int | None = None, error_code: str | None = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(message)


class AuthenticationError(CommerceIndexError):
    """Invalid or missing API key."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class InsufficientTierError(CommerceIndexError):
    """Agent's tier doesn't meet the requirement."""

    def __init__(self, message: str = "Insufficient tier"):
        super().__init__(message, status_code=403, error_code="insufficient_tier")


class InsufficientScoreError(CommerceIndexError):
    """Agent's CI Score is below the requirement."""

    def __init__(self, message: str = "Insufficient score"):
        super().__init__(message, status_code=403, error_code="insufficient_score")


class NotFoundError(CommerceIndexError):
    """Resource not found."""

    def __init__(self, message: str = "Not found"):
        super().__init__(message, status_code=404)


class ConflictError(CommerceIndexError):
    """Conflict (already claimed, slot full, etc.)."""

    def __init__(self, message: str = "Conflict"):
        super().__init__(message, status_code=409)


class RateLimitError(CommerceIndexError):
    """Rate limit exceeded."""

    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, status_code=429, error_code="rate_limit_exceeded")


class InvalidStateError(CommerceIndexError):
    """Resource is not in the expected state."""

    def __init__(self, message: str = "Invalid state"):
        super().__init__(message, status_code=400, error_code="invalid_state")
