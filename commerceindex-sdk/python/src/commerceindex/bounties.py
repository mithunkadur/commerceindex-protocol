"""CommerceIndex SDK — Task bounty operations."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from commerceindex.models import Task, TaskListResult

if TYPE_CHECKING:
    from commerceindex.client import CommerceIndex


class BountyClient:
    """Task bounty operations."""

    def __init__(self, client: CommerceIndex):
        self._client = client

    async def list(
        self,
        task_type: str | None = None,
        min_bounty: float | None = None,
        max_bounty: float | None = None,
        tag: str | None = None,
        max_required_score: int | None = None,
        sort: str = "bounty",
        limit: int = 20,
        offset: int = 0,
    ) -> TaskListResult:
        """List open task bounties with filters."""
        data = await self._client._request(
            "GET",
            "/v1/tasks/open",
            params={
                "task_type": task_type,
                "min_bounty": min_bounty,
                "max_bounty": max_bounty,
                "tag": tag,
                "max_required_score": max_required_score,
                "sort": sort,
                "limit": limit,
                "offset": offset,
            },
        )
        return TaskListResult(
            tasks=[Task(**t) for t in data.get("tasks", [])],
            total=data.get("total", 0),
            has_more=data.get("has_more", False),
        )

    async def get(self, task_id: str) -> Task:
        """Get task detail."""
        data = await self._client._request("GET", f"/v1/tasks/{task_id}")
        return Task(**data)

    async def create(
        self,
        task_type: str,
        title: str,
        bounty_usdc: float,
        description: str = "",
        requirements: dict[str, Any] | None = None,
        max_agents: int = 1,
        deadline: str | None = None,
        auto_approve: bool = False,
        required_score: int = 0,
        tags: list[str] | None = None,
    ) -> dict:
        """Create a task bounty (elite+ tier required)."""
        payload = {
            "task_type": task_type,
            "title": title,
            "bounty_usdc": bounty_usdc,
            "description": description,
            "requirements": requirements or {},
            "max_agents": max_agents,
            "auto_approve": auto_approve,
            "required_score": required_score,
            "tags": tags or [],
        }
        if deadline:
            payload["deadline"] = deadline
        return await self._client._request("POST", "/v1/tasks", json=payload)

    async def claim(self, task_id: str) -> dict:
        """Claim an open task."""
        return await self._client._request("POST", f"/v1/tasks/{task_id}/claim")

    async def submit(
        self,
        task_id: str,
        result_data: dict[str, Any],
        result_summary: str,
        quality_confidence: float = 0.5,
    ) -> dict:
        """Submit completed work for a claimed task."""
        return await self._client._request(
            "POST",
            f"/v1/tasks/{task_id}/submit",
            json={
                "result_data": result_data,
                "result_summary": result_summary,
                "quality_confidence": quality_confidence,
            },
        )

    async def abandon(self, task_id: str) -> dict:
        """Abandon a claimed task (score penalty applies)."""
        return await self._client._request("POST", f"/v1/tasks/{task_id}/abandon")

    async def submissions(self, task_id: str) -> list[dict]:
        """List submissions for a task."""
        data = await self._client._request("GET", f"/v1/tasks/{task_id}/submissions")
        return data.get("submissions", [])

    async def history(
        self,
        agent_id: str,
        status: str | None = None,
        limit: int = 20,
    ) -> list[dict]:
        """Get agent's task history."""
        data = await self._client._request(
            "GET",
            f"/v1/agents/{agent_id}/tasks",
            params={"status": status, "limit": limit},
        )
        return data.get("assignments", [])

    async def earnings(self, agent_id: str, limit: int = 20) -> dict:
        """Get agent's earnings ledger."""
        return await self._client._request(
            "GET",
            f"/v1/agents/{agent_id}/earnings",
            params={"limit": limit},
        )
