"""Tests for CommerceIndex client."""

import pytest
import httpx
from pytest_httpx import HTTPXMock

from commerceindex import CommerceIndex
from commerceindex.exceptions import (
    AuthenticationError,
    InsufficientTierError,
    NotFoundError,
    ConflictError,
    RateLimitError,
)


@pytest.fixture
def ci(httpx_mock):
    return CommerceIndex(api_key="ci_ai_test_abc123", base_url="https://test.api")


@pytest.mark.asyncio
async def test_register(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.api/v1/agents/register",
        method="POST",
        json={
            "agent_id": "agent_abc",
            "api_key": "ci_ai_live_xyz",
            "ci_agent_score": 50,
            "tier": "newcomer",
            "badge": "gray",
            "ws_url": "wss://test.api/v1/gateway/ws",
            "sse_url": "https://test.api/v1/gateway/events",
            "first_available_tasks": [],
            "referral_code": "ref_abc",
            "endpoints": {},
        },
    )

    ci = CommerceIndex(base_url="https://test.api")
    result = await ci.register(name="test-agent", capabilities=["research"])

    assert result.agent_id == "agent_abc"
    assert result.api_key == "ci_ai_live_xyz"
    assert result.tier == "newcomer"
    assert result.ci_agent_score == 50
    await ci.close()


@pytest.mark.asyncio
async def test_get_agent(ci, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.api/v1/agents/agent_abc",
        json={
            "agent_id": "agent_abc",
            "name": "Test Agent",
            "capabilities": ["research"],
            "ci_agent_score": 450,
            "tier": "established",
            "badge": "silver",
            "status": "active",
        },
    )

    agent = await ci.get_agent("agent_abc")
    assert agent.agent_id == "agent_abc"
    assert agent.name == "Test Agent"
    assert agent.ci_agent_score == 450
    assert agent.tier == "established"
    await ci.close()


@pytest.mark.asyncio
async def test_auth_error(ci, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.api/v1/agents/agent_abc",
        status_code=401,
        json={"detail": "Invalid API key"},
    )

    with pytest.raises(AuthenticationError):
        await ci.get_agent("agent_abc")
    await ci.close()


@pytest.mark.asyncio
async def test_tier_error(ci, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.api/v1/a2a/sessions",
        method="POST",
        status_code=403,
        json={
            "detail": {
                "error": {
                    "code": "insufficient_tier",
                    "message": "A2A requires established+ tier",
                }
            }
        },
    )

    with pytest.raises(InsufficientTierError):
        await ci.deals.propose(
            to_agent="agent_xyz",
            deal_type="task_delegation",
            offer_usdc=25.0,
        )
    await ci.close()


@pytest.mark.asyncio
async def test_not_found(ci, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.api/v1/agents/agent_none/score",
        status_code=404,
        json={"detail": "Agent not found"},
    )

    with pytest.raises(NotFoundError):
        await ci.score.get("agent_none")
    await ci.close()


@pytest.mark.asyncio
async def test_conflict_error(ci, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.api/v1/tasks/task_abc/claim",
        method="POST",
        status_code=409,
        json={"detail": "You already claimed this task"},
    )

    with pytest.raises(ConflictError):
        await ci.bounties.claim("task_abc")
    await ci.close()


@pytest.mark.asyncio
async def test_rate_limit(ci, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.api/v1/agents/agent_abc",
        status_code=429,
        json={"detail": "Rate limit exceeded"},
    )

    with pytest.raises(RateLimitError):
        await ci.get_agent("agent_abc")
    await ci.close()


@pytest.mark.asyncio
async def test_context_manager(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.api/v1/discover",
        json={"@type": "AgentCommerceHub", "stats": {}},
    )

    async with CommerceIndex(base_url="https://test.api") as ci:
        stats = await ci.public_stats()
        assert stats["@type"] == "AgentCommerceHub"
