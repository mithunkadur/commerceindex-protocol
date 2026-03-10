"""CommerceIndex SDK — CI Score operations."""

from __future__ import annotations

from typing import TYPE_CHECKING

from commerceindex.models import CIScore

if TYPE_CHECKING:
    from commerceindex.client import CommerceIndex


class ScoreClient:
    """CI Score operations."""

    def __init__(self, client: CommerceIndex):
        self._client = client

    async def get(self, agent_id: str) -> CIScore:
        """Get full CI Agent Score breakdown for an agent."""
        data = await self._client._request("GET", f"/v1/agents/{agent_id}/score")
        return CIScore(**data)
