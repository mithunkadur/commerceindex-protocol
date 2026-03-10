"""Tests for escrow operations."""

import pytest
from pytest_httpx import HTTPXMock

from commerceindex import CommerceIndex


@pytest.fixture
def ci():
    return CommerceIndex(api_key="ci_ai_test_abc", base_url="https://test.api")


@pytest.mark.asyncio
async def test_get_escrow(ci, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.api/v1/escrow/esc_abc",
        json={
            "escrow_id": "esc_abc",
            "escrow_type": "task",
            "reference_id": "task_001",
            "payer_id": "agent_abc",
            "payee_id": "agent_xyz",
            "amount_usdc": 50.0,
            "status": "funded",
            "timeout_hours": 72,
        },
    )

    escrow = await ci.escrow.get("esc_abc")
    assert escrow.escrow_id == "esc_abc"
    assert escrow.amount_usdc == 50.0
    assert escrow.status == "funded"
    assert escrow.payer_id == "agent_abc"
    await ci.close()


@pytest.mark.asyncio
async def test_dispute_escrow(ci, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://test.api/v1/escrow/esc_abc/dispute",
        method="POST",
        json={"ok": True, "status": "disputed"},
    )

    result = await ci.escrow.dispute("esc_abc")
    assert result["ok"] is True
    assert result["status"] == "disputed"
    await ci.close()
