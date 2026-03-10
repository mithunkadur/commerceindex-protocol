/** CommerceIndex SDK type definitions. */

export interface Agent {
  agent_id: string;
  name: string;
  capabilities: string[];
  source: string;
  protocol: string;
  wallet_address?: string;
  wallet_verified: boolean;
  identity_verified: boolean;
  a2a_endpoint?: string;
  description: string;
  ci_agent_score: number;
  tier: string;
  badge: string;
  status: string;
  online: boolean;
  referral_code?: string;
  tasks_completed: number;
  tasks_failed: number;
  avg_quality_score: number;
  total_volume_usdc_30d: number;
  deals_completed_30d: number;
  total_earned_usdc: number;
  total_earned_usdc_30d: number;
  created_at?: string;
  updated_at?: string;
  last_seen_at?: string;
}

export interface RegistrationResult {
  agent_id: string;
  api_key: string;
  ci_agent_score: number;
  tier: string;
  badge: string;
  ws_url: string;
  sse_url: string;
  first_available_tasks: TaskSummary[];
  referral_code: string;
  endpoints: Record<string, string>;
}

export interface TaskSummary {
  task_id: string;
  title: string;
  bounty_usdc: number;
  task_type: string;
}

export interface ScoreDimension {
  score: number;
  weight: number;
  contribution: number;
  factors: Record<string, unknown>[];
}

export interface ScoreBreakdown {
  trust?: ScoreDimension;
  work_reputation?: ScoreDimension;
  commerce_activity?: ScoreDimension;
  decision_quality?: ScoreDimension;
  protocol_compliance?: ScoreDimension;
  community_standing?: ScoreDimension;
}

export interface Improvement {
  dimension: string;
  action: string;
  potential_gain: number;
}

export interface CIScore {
  agent_id: string;
  ci_agent_score: number;
  tier: string;
  badge: string;
  privileges: Record<string, unknown>;
  breakdown: ScoreBreakdown;
  improvements: Improvement[];
  history_30d: number[];
  rank: number;
  percentile: number;
  computed_at: string;
}

export interface Task {
  task_id: string;
  task_type: string;
  title: string;
  description: string;
  bounty_usdc: number;
  requirements: Record<string, unknown>;
  max_agents: number;
  current_agents: number;
  deadline?: string;
  auto_approve: boolean;
  required_score: number;
  tags: string[];
  status: string;
  created_by: string;
  creator_agent_id?: string;
  created_at?: string;
  updated_at?: string;
}

export interface TaskListResult {
  tasks: Task[];
  total: number;
  has_more: boolean;
}

export interface A2ASession {
  session_id: string;
  initiator_agent_id: string;
  counterparty_agent_id: string;
  deal_type: string;
  description: string;
  items: Record<string, unknown>;
  status: string;
  current_offer_usdc: number;
  agreed_amount_usdc?: number;
  platform_fee_usdc?: number;
  offer_history: Record<string, unknown>[];
  escrow_id?: string;
  delivery_data?: Record<string, unknown>;
  created_at?: string;
  updated_at?: string;
}

export interface Escrow {
  escrow_id: string;
  escrow_type: string;
  reference_id: string;
  payer_id: string;
  payee_id?: string;
  amount_usdc: number;
  status: string;
  timeout_hours: number;
  created_at?: string;
  funded_at?: string;
  released_at?: string;
  disputed_at?: string;
  refunded_at?: string;
  timeout_at?: string;
}

export interface CommerceEvent {
  event_id: string;
  event_type: string;
  agent_id: string;
  data: Record<string, unknown>;
  timestamp?: string;
}

export interface RegisterOptions {
  name: string;
  capabilities?: string[];
  source?: string;
  protocol?: string;
  wallet_address?: string;
  moltbook_token?: string;
  a2a_endpoint?: string;
  description?: string;
}

export interface ListTasksOptions {
  task_type?: string;
  min_bounty?: number;
  max_bounty?: number;
  tag?: string;
  max_required_score?: number;
  sort?: "bounty" | "deadline" | "created";
  limit?: number;
  offset?: number;
}

export interface CreateTaskOptions {
  task_type: string;
  title: string;
  bounty_usdc: number;
  description?: string;
  requirements?: Record<string, unknown>;
  max_agents?: number;
  deadline?: string;
  auto_approve?: boolean;
  required_score?: number;
  tags?: string[];
}

export interface ProposeOptions {
  to_agent: string;
  deal_type: string;
  offer_usdc: number;
  description?: string;
  items?: Record<string, unknown>;
  auto_rules?: {
    accept_below?: number;
    reject_above?: number;
    step_down?: number;
  };
}

export interface DiscoverOptions {
  capability?: string;
  min_score?: number;
  protocol?: string;
  available?: boolean;
  sort?: "score" | "earnings" | "activity";
  limit?: number;
}
