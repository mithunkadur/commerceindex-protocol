"""Tests for bounty operations."""

import pytest
from pytest_httpx import HTTPXMock

from commerceindex import CommerceIndex


@pytest.fixture
def ci():
    return CommerceIndex(api_key="ci_ai_test_abc", base_url="https://test.api")


@pytest.mark.asyncio
async def test_list_bounties(ci, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={
            "tasks": [
                {
                    "task_id": "task_001",
                    "title": "Research pricing",
                    "bounty_usdc": 50.0,
                    "task_type": "research",
                    "status": "open",
                    "required_score": 200,
                    "tags": ["research"],
                },
                {
                    "task_id": "task_002",
                    "title": "Monitor prices",
                    "bounty_usdc": 25.0,
                    "task_type": "price_watch",
                    "status": "open",
                    "required_score": 0,
                    "tags": [],
                },
            ],
            "total": 2,
            "has_more": False,
        },
    )

    result = await ci.bounties.list(min_bounty=10.0)
    assert len(result.tasks) == 2
    assert result.tasks[0].task_id == "task_001"
    assert result.tasks[0].bounty_usdc == 50.0
    assert result.total == 2
    assert result.has_more is False
    await ci.close()


@pytest.mark.asyncio
async def test_claim_bounty(ci, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.api/v1/tasks/task_001/claim",
        method="POST",
        json={"ok": True, "assignment_id": "assign_abc", "status": "claimed"},
    )

    result = await ci.bounties.claim("task_001")
    assert result["ok"] is True
    assert result["assignment_id"] == "assign_abc"
    await ci.close()


@pytest.mark.asyncio
async def test_submit_work(ci, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.api/v1/tasks/task_001/submit",
        method="POST",
        json={"ok": True, "submission_id": "sub_abc", "status": "under_review"},
    )

    result = await ci.bounties.submit(
        "task_001",
        result_data={"findings": ["price dropped 15%"]},
        result_summary="Found significant price drop",
        quality_confidence=0.9,
    )
    assert result["ok"] is True
    assert result["submission_id"] == "sub_abc"
    await ci.close()


@pytest.mark.asyncio
async def test_create_bounty(ci, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.api/v1/tasks",
        method="POST",
        json={"ok": True, "task_id": "task_new", "status": "open"},
    )

    result = await ci.bounties.create(
        task_type="research",
        title="Analyze competitor pricing",
        bounty_usdc=100.0,
        tags=["research", "pricing"],
    )
    assert result["ok"] is True
    assert result["task_id"] == "task_new"
    await ci.close()


@pytest.mark.asyncio
async def test_earnings(ci, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={
            "earnings": [
                {
                    "payout_id": "pay_abc",
                    "agent_id": "agent_abc",
                    "task_id": "task_001",
                    "net_usdc": 45.0,
                    "status": "completed",
                }
            ],
            "total_earned_usdc": 45.0,
        },
    )

    result = await ci.bounties.earnings("agent_abc")
    assert result["total_earned_usdc"] == 45.0
    assert len(result["earnings"]) == 1
    await ci.close()
