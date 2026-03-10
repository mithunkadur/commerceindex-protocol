/** CommerceIndex SDK errors. */

export class CommerceIndexError extends Error {
  statusCode?: number;
  errorCode?: string;

  constructor(message: string, statusCode?: number, errorCode?: string) {
    super(message);
    this.name = "CommerceIndexError";
    this.statusCode = statusCode;
    this.errorCode = errorCode;
  }
}

export class AuthenticationError extends CommerceIndexError {
  constructor(message = "Authentication failed") {
    super(message, 401);
    this.name = "AuthenticationError";
  }
}

export class InsufficientTierError extends CommerceIndexError {
  constructor(message = "Insufficient tier") {
    super(message, 403, "insufficient_tier");
    this.name = "InsufficientTierError";
  }
}

export class InsufficientScoreError extends CommerceIndexError {
  constructor(message = "Insufficient score") {
    super(message, 403, "insufficient_score");
    this.name = "InsufficientScoreError";
  }
}

export class NotFoundError extends CommerceIndexError {
  constructor(message = "Not found") {
    super(message, 404);
    this.name = "NotFoundError";
  }
}

export class ConflictError extends CommerceIndexError {
  constructor(message = "Conflict") {
    super(message, 409);
    this.name = "ConflictError";
  }
}

export class RateLimitError extends CommerceIndexError {
  constructor(message = "Rate limit exceeded") {
    super(message, 429, "rate_limit_exceeded");
    this.name = "RateLimitError";
  }
}
