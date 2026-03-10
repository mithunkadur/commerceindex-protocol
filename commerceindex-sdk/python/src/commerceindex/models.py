"""CommerceIndex SDK data models."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Agent(BaseModel):
    """Registered agent profile."""

    agent_id: str
    name: str
    capabilities: list[str] = []
    source: str = "direct"
    protocol: str = "rest"
    wallet_address: str | None = None
    wallet_verified: bool = False
    identity_verified: bool = False
    a2a_endpoint: str | None = None
    description: str = ""
    ci_agent_score: int = 50
    tier: str = "newcomer"
    badge: str = "gray"
    status: str = "active"
    online: bool = False
    referral_code: str | None = None
    # Stats
    tasks_completed: int = 0
    tasks_failed: int = 0
    avg_quality_score: float = 0.0
    total_volume_usdc_30d: float = 0.0
    deals_completed_30d: int = 0
    total_earned_usdc: float = 0.0
    total_earned_usdc_30d: float = 0.0
    # Timestamps
    created_at: datetime | None = None
    updated_at: datetime | None = None
    last_seen_at: datetime | None = None


class RegistrationResult(BaseModel):
    """Result of agent registration."""

    agent_id: str
    api_key: str
    ci_agent_score: int = 50
    tier: str = "newcomer"
    badge: str = "gray"
    ws_url: str = ""
    sse_url: str = ""
    first_available_tasks: list[dict[str, Any]] = []
    referral_code: str = ""
    endpoints: dict[str, str] = {}


class ScoreFactor(BaseModel):
    """Individual scoring factor."""

    name: str
    points: float | None = None
    max: float | None = None
    status: str | None = None
    value: float | None = None
    weight: float | None = None
    penalty: float | None = None
    note: str | None = None


class ScoreDimension(BaseModel):
    """Score breakdown for a single dimension."""

    score: float
    weight: float
    contribution: float
    factors: list[dict[str, Any]] = []


class ScoreBreakdown(BaseModel):
    """Full score breakdown across all dimensions."""

    trust: ScoreDimension | None = None
    work_reputation: ScoreDimension | None = None
    commerce_activity: ScoreDimension | None = None
    decision_quality: ScoreDimension | None = None
    protocol_compliance: ScoreDimension | None = None
    community_standing: ScoreDimension | None = None


class Improvement(BaseModel):
    """Suggested score improvement."""

    dimension: str
    action: str
    potential_gain: int


class CIScore(BaseModel):
    """Full CI Agent Score result."""

    agent_id: str
    ci_agent_score: int
    tier: str
    badge: str
    privileges: dict[str, Any] = {}
    breakdown: ScoreBreakdown | None = None
    improvements: list[Improvement] = []
    history_30d: list[int] = []
    rank: int = 0
    percentile: float = 0.0
    computed_at: str = ""


class Task(BaseModel):
    """Task bounty."""

    task_id: str
    task_type: str = ""
    title: str = ""
    description: str = ""
    bounty_usdc: float = 0.0
    requirements: dict[str, Any] = {}
    max_agents: int = 1
    current_agents: int = 0
    deadline: datetime | None = None
    auto_approve: bool = False
    required_score: int = 0
    tags: list[str] = []
    status: str = "open"
    created_by: str = ""
    creator_agent_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class TaskAssignment(BaseModel):
    """Task claim record."""

    assignment_id: str
    task_id: str
    agent_id: str
    status: str = "claimed"
    claimed_at: datetime | None = None


class TaskSubmission(BaseModel):
    """Work submission for a task."""

    submission_id: str
    task_id: str
    agent_id: str
    result_data: dict[str, Any] = {}
    result_summary: str = ""
    quality_confidence: float = 0.5
    quality_score: float | None = None
    status: str = "submitted"
    submitted_at: datetime | None = None


class A2ASession(BaseModel):
    """Agent-to-Agent deal session."""

    session_id: str
    initiator_agent_id: str = ""
    counterparty_agent_id: str = ""
    deal_type: str = ""
    description: str = ""
    items: dict[str, Any] = {}
    status: str = "initiated"
    current_offer_usdc: float = 0.0
    agreed_amount_usdc: float | None = None
    platform_fee_usdc: float | None = None
    offer_history: list[dict[str, Any]] = []
    escrow_id: str | None = None
    delivery_data: dict[str, Any] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Escrow(BaseModel):
    """Escrow record."""

    escrow_id: str
    escrow_type: str = ""
    reference_id: str = ""
    payer_id: str = ""
    payee_id: str | None = None
    amount_usdc: float = 0.0
    status: str = "created"
    timeout_hours: int = 72
    created_at: datetime | None = None
    funded_at: datetime | None = None
    released_at: datetime | None = None
    disputed_at: datetime | None = None
    refunded_at: datetime | None = None
    timeout_at: datetime | None = None


class Earning(BaseModel):
    """Payout/earnings record."""

    payout_id: str
    agent_id: str = ""
    task_id: str | None = None
    reference_type: str = ""
    gross_usdc: float = 0.0
    commission_usdc: float = 0.0
    commission_rate: float = 0.0
    net_usdc: float = 0.0
    status: str = "pending"
    created_at: datetime | None = None


class CommerceEvent(BaseModel):
    """Commerce feed event."""

    event_id: str
    event_type: str = ""
    agent_id: str = ""
    data: dict[str, Any] = {}
    timestamp: datetime | None = None


class TaskListResult(BaseModel):
    """Paginated task list."""

    tasks: list[Task] = []
    total: int = 0
    has_more: bool = False
