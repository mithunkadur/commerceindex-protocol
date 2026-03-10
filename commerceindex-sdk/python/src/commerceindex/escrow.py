"""CommerceIndex SDK — Escrow operations."""

from __future__ import annotations

from typing import TYPE_CHECKING

from commerceindex.models import Escrow

if TYPE_CHECKING:
    from commerceindex.client import CommerceIndex


class EscrowClient:
    """Escrow operations."""

    def __init__(self, client: CommerceIndex):
        self._client = client

    async def get(self, escrow_id: str) -> Escrow:
        """Get escrow status."""
        data = await self._client._request("GET", f"/v1/escrow/{escrow_id}")
        return Escrow(**data)

    async def dispute(self, escrow_id: str) -> dict:
        """Dispute an escrow (freeze funds). Must be a party."""
        return await self._client._request("POST", f"/v1/escrow/{escrow_id}/dispute")
