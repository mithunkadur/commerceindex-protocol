"""CommerceIndex SDK — Experiment operations."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from commerceindex.client import CommerceIndex


class ExperimentClient:
    """Autonomous experiment loop operations.

    Usage:
        ci = CommerceIndex(api_key="ci_ai_live_...")

        # Create an experiment
        exp = await ci.experiments.create(
            name="Optimize negotiation thresholds",
            experiment_type="strategy",
            program={
                "objective": "Maximize net earnings",
                "primary_metric": "net_usdc_earned",
                "metric_direction": "higher_is_better",
                "constraints": {"max_runs": 50, "stop_if_no_improvement": 10},
                "variant_space": {"accept_below_range": {"min": 10, "max": 500}},
                "instructions": "Try lowering accept_below each run...",
            },
        )

        # Start the experiment
        result = await ci.experiments.start(exp["experiment_id"])

        # Report a run
        outcome = await ci.experiments.report_run(
            experiment_id=exp["experiment_id"],
            strategy={"accept_below": 50, "step_down": 2.5},
            metrics={"primary_value": 125.50, "approval_rate": 0.85},
            notes="Lowered accept_below from 75 to 50",
        )

        # Adopt best strategy
        await ci.experiments.adopt_best(exp["experiment_id"])
    """

    def __init__(self, client: CommerceIndex):
        self._client = client

    async def list(self, status: str | None = None) -> dict:
        """List agent's experiments."""
        params = {}
        if status:
            params["status"] = status
        return await self._client._request("GET", "/v1/experiments", params=params)

    async def get(self, experiment_id: str) -> dict:
        """Get experiment details with recent runs."""
        return await self._client._request("GET", f"/v1/experiments/{experiment_id}")

    async def create(
        self,
        name: str,
        experiment_type: str,
        program: dict,
    ) -> dict:
        """Create a new experiment.

        Args:
            name: Experiment name.
            experiment_type: "strategy" | "research" | "integration"
            program: Experiment program with objective, primary_metric,
                     metric_direction, constraints, variant_space, instructions.
        """
        return await self._client._request(
            "POST",
            "/v1/experiments",
            json={"name": name, "experiment_type": experiment_type, "program": program},
        )

    async def update(self, experiment_id: str, **fields) -> dict:
        """Update experiment (only in draft or paused state)."""
        return await self._client._request(
            "PUT", f"/v1/experiments/{experiment_id}", json=fields,
        )

    async def start(self, experiment_id: str) -> dict:
        """Start experiment. Captures baseline metrics."""
        return await self._client._request(
            "POST", f"/v1/experiments/{experiment_id}/start",
        )

    async def pause(self, experiment_id: str) -> dict:
        """Pause experiment."""
        return await self._client._request(
            "POST", f"/v1/experiments/{experiment_id}/pause",
        )

    async def resume(self, experiment_id: str) -> dict:
        """Resume paused experiment."""
        return await self._client._request(
            "POST", f"/v1/experiments/{experiment_id}/resume",
        )

    async def report_run(
        self,
        experiment_id: str,
        strategy: dict,
        metrics: dict,
        notes: str = "",
    ) -> dict:
        """Report experiment run results. Platform evaluates improvement.

        Args:
            experiment_id: Experiment to report for.
            strategy: Strategy config used for this run.
            metrics: Measured outcomes (must include primary_value).
            notes: Hypothesis or observation.
        """
        return await self._client._request(
            "POST",
            f"/v1/experiments/{experiment_id}/runs",
            json={
                "strategy_snapshot": strategy,
                "metrics": metrics,
                "notes": notes,
            },
        )

    async def list_runs(
        self, experiment_id: str, page: int = 1, limit: int = 20,
    ) -> dict:
        """List all runs for an experiment."""
        return await self._client._request(
            "GET",
            f"/v1/experiments/{experiment_id}/runs",
            params={"page": page, "limit": limit},
        )

    async def get_best(self, experiment_id: str) -> dict:
        """Get best strategy and metrics."""
        return await self._client._request(
            "GET", f"/v1/experiments/{experiment_id}/best",
        )

    async def adopt_best(self, experiment_id: str) -> dict:
        """Adopt best strategy as agent's active auto-rules."""
        return await self._client._request(
            "POST", f"/v1/experiments/{experiment_id}/adopt",
        )
