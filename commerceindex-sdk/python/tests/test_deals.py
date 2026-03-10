"""Tests for A2A deal operations."""

import pytest
from pytest_httpx import HTTPXMock

from commerceindex import CommerceIndex


@pytest.fixture
def ci():
    return CommerceIndex(api_key="ci_ai_test_abc", base_url="https://test.api")


@pytest.mark.asyncio
async def test_propose_deal(ci, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.api/v1/a2a/sessions",
        method="POST",
        json={"ok": True, "session_id": "a2a_abc", "status": "initiated"},
    )

    result = await ci.deals.propose(
        to_agent="agent_xyz",
        deal_type="task_delegation",
        offer_usdc=25.0,
        description="Analyze 500 product listings",
    )
    assert result["ok"] is True
    assert result["session_id"] == "a2a_abc"
    await ci.close()


@pytest.mark.asyncio
async def test_counter_offer(ci, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.api/v1/a2a/sessions/a2a_abc/counter",
        method="POST",
        json={"ok": True, "status": "negotiating", "round": 2},
    )

    result = await ci.deals.counter("a2a_abc", offer_usdc=20.0, message="Can you do less?")
    assert result["ok"] is True
    assert result["round"] == 2
    await ci.close()


@pytest.mark.asyncio
async def test_accept_deal(ci, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.api/v1/a2a/sessions/a2a_abc/counter",
        method="POST",
        json={
            "ok": True,
            "status": "escrowed",
            "agreed_amount_usdc": 22.5,
            "fee_usdc": 0.11,
        },
    )

    result = await ci.deals.accept("a2a_abc")
    assert result["status"] == "escrowed"
    assert result["agreed_amount_usdc"] == 22.5
    await ci.close()


@pytest.mark.asyncio
async def test_deliver_and_confirm(ci, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.api/v1/a2a/sessions/a2a_abc/deliver",
        method="POST",
        json={"ok": True, "status": "delivered"},
    )

    result = await ci.deals.deliver(
        "a2a_abc",
        delivery_data={"report_url": "https://example.com/report"},
        delivery_summary="Analysis complete",
    )
    assert result["status"] == "delivered"

    httpx_mock.add_response(
        url="https://test.api/v1/a2a/sessions/a2a_abc/confirm",
        method="POST",
        json={"ok": True, "status": "settled", "payout_usdc": 22.39},
    )

    result = await ci.deals.confirm("a2a_abc")
    assert result["status"] == "settled"
    assert result["payout_usdc"] == 22.39
    await ci.close()


@pytest.mark.asyncio
async def test_get_session(ci, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.api/v1/a2a/sessions/a2a_abc",
        json={
            "session_id": "a2a_abc",
            "initiator_agent_id": "agent_abc",
            "counterparty_agent_id": "agent_xyz",
            "deal_type": "task_delegation",
            "status": "negotiating",
            "current_offer_usdc": 20.0,
            "offer_history": [
                {"round": 1, "action": "initial_offer", "offer_usdc": 25.0},
                {"round": 2, "action": "counter", "offer_usdc": 20.0},
            ],
        },
    )

    session = await ci.deals.get("a2a_abc")
    assert session.session_id == "a2a_abc"
    assert session.status == "negotiating"
    assert session.current_offer_usdc == 20.0
    assert len(session.offer_history) == 2
    await ci.close()
