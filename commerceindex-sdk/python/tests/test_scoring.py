"""Tests for CI Score operations."""

import pytest
from pytest_httpx import HTTPXMock

from commerceindex import CommerceIndex


@pytest.fixture
def ci():
    return CommerceIndex(api_key="ci_ai_test_abc", base_url="https://test.api")


@pytest.mark.asyncio
async def test_get_score(ci, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.api/v1/agents/agent_abc/score",
        json={
            "agent_id": "agent_abc",
            "ci_agent_score": 450,
            "tier": "established",
            "badge": "silver",
            "privileges": {
                "daily_usdc_cap": 5000,
                "can_bid": True,
                "can_a2a": True,
                "can_create_bounties": False,
            },
            "breakdown": {
                "trust": {
                    "score": 72.5,
                    "weight": 0.25,
                    "contribution": 181.3,
                    "factors": [
                        {"name": "wallet_verified", "points": 20, "status": "met"},
                    ],
                },
                "work_reputation": {
                    "score": 65.0,
                    "weight": 0.25,
                    "contribution": 162.5,
                    "factors": [],
                },
            },
            "improvements": [
                {
                    "dimension": "trust",
                    "action": "Complete identity verification",
                    "potential_gain": 50,
                }
            ],
            "history_30d": [50, 100, 200, 350, 450],
            "rank": 42,
            "percentile": 89.5,
            "computed_at": "2026-03-07T12:00:00Z",
        },
    )

    score = await ci.score.get("agent_abc")
    assert score.ci_agent_score == 450
    assert score.tier == "established"
    assert score.rank == 42
    assert score.percentile == 89.5
    assert len(score.improvements) == 1
    assert score.improvements[0].action == "Complete identity verification"
    assert score.breakdown.trust.score == 72.5
    assert score.breakdown.trust.weight == 0.25
    await ci.close()
