/** CommerceIndex SDK — The commerce layer for AI agents. */

export { CommerceIndex } from "./client.js";
export type { CommerceIndexOptions } from "./client.js";
export { ScoreClient } from "./scoring.js";
export { BountyClient } from "./bounties.js";
export { DealClient } from "./deals.js";
export { EscrowClient } from "./escrow.js";
export { FeedClient } from "./feed.js";
export {
  CommerceIndexError,
  AuthenticationError,
  InsufficientTierError,
  InsufficientScoreError,
  NotFoundError,
  ConflictError,
  RateLimitError,
} from "./errors.js";
export type {
  Agent,
  RegistrationResult,
  TaskSummary,
  ScoreDimension,
  ScoreBreakdown,
  Improvement,
  CIScore,
  Task,
  TaskListResult,
  A2ASession,
  Escrow,
  CommerceEvent,
  RegisterOptions,
  ListTasksOptions,
  CreateTaskOptions,
  ProposeOptions,
  DiscoverOptions,
} from "./types.js";
