"""CommerceIndex SDK — Agent-to-Agent deal operations."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from commerceindex.models import A2ASession

if TYPE_CHECKING:
    from commerceindex.client import CommerceIndex


class DealClient:
    """A2A deal operations."""

    def __init__(self, client: CommerceIndex):
        self._client = client

    async def propose(
        self,
        to_agent: str,
        deal_type: str,
        offer_usdc: float,
        description: str = "",
        items: dict[str, Any] | None = None,
        auto_rules: dict[str, float] | None = None,
    ) -> dict:
        """Initiate an A2A deal with another agent (established+ tier)."""
        payload = {
            "counterparty_agent_id": to_agent,
            "deal_type": deal_type,
            "initial_offer_usdc": offer_usdc,
            "description": description,
            "items": items or {},
        }
        if auto_rules:
            payload["auto_rules"] = auto_rules
        return await self._client._request("POST", "/v1/a2a/sessions", json=payload)

    async def get(self, session_id: str) -> A2ASession:
        """Get A2A session details."""
        data = await self._client._request("GET", f"/v1/a2a/sessions/{session_id}")
        return A2ASession(**data)

    async def counter(
        self,
        session_id: str,
        offer_usdc: float,
        message: str | None = None,
    ) -> dict:
        """Send a counter-offer."""
        payload: dict[str, Any] = {"action": "counter", "offer_usdc": offer_usdc}
        if message:
            payload["message"] = message
        return await self._client._request(
            "POST", f"/v1/a2a/sessions/{session_id}/counter", json=payload
        )

    async def accept(self, session_id: str) -> dict:
        """Accept the current offer."""
        return await self._client._request(
            "POST",
            f"/v1/a2a/sessions/{session_id}/counter",
            json={"action": "accept"},
        )

    async def reject(self, session_id: str, message: str | None = None) -> dict:
        """Reject the deal."""
        payload: dict[str, Any] = {"action": "reject"}
        if message:
            payload["message"] = message
        return await self._client._request(
            "POST", f"/v1/a2a/sessions/{session_id}/counter", json=payload
        )

    async def deliver(
        self,
        session_id: str,
        delivery_data: dict[str, Any],
        delivery_summary: str = "",
    ) -> dict:
        """Deliver goods/data/service (seller only)."""
        return await self._client._request(
            "POST",
            f"/v1/a2a/sessions/{session_id}/deliver",
            json={
                "delivery_data": delivery_data,
                "delivery_summary": delivery_summary,
            },
        )

    async def confirm(self, session_id: str) -> dict:
        """Confirm delivery, release escrow (buyer only)."""
        return await self._client._request(
            "POST", f"/v1/a2a/sessions/{session_id}/confirm"
        )

    async def dispute(self, session_id: str) -> dict:
        """Dispute the deal, freeze escrow."""
        return await self._client._request(
            "POST", f"/v1/a2a/sessions/{session_id}/dispute"
        )

    async def history(
        self,
        agent_id: str,
        status: str | None = None,
        limit: int = 20,
    ) -> list[A2ASession]:
        """Get agent's A2A deal history."""
        data = await self._client._request(
            "GET",
            f"/v1/agents/{agent_id}/a2a",
            params={"status": status, "limit": limit},
        )
        return [A2ASession(**s) for s in data.get("sessions", [])]
