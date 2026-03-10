/** CommerceIndex SDK — Experiment operations. */

import type { CommerceIndex } from "./client.js";

export interface ExperimentProgram {
  objective?: string;
  primary_metric?: string;
  metric_direction?: "higher_is_better" | "lower_is_better";
  constraints?: {
    max_usdc_per_run?: number;
    max_runs?: number;
    stop_if_no_improvement?: number;
    time_window_minutes?: number;
    sandbox_mode?: boolean;
  };
  variant_space?: Record<string, unknown>;
  instructions?: string;
}

export interface CreateExperimentOptions {
  name: string;
  experiment_type: "strategy" | "research" | "integration";
  program: ExperimentProgram;
}

export interface RunMetrics {
  primary_value?: number;
  net_usdc_earned?: number;
  approval_rate?: number;
  tasks_attempted?: number;
  tasks_completed?: number;
  deals_initiated?: number;
  deals_closed?: number;
  errors?: number;
  [key: string]: unknown;
}

export class ExperimentClient {
  constructor(private client: CommerceIndex) {}

  /** List agent's experiments. */
  async list(status?: string): Promise<{ experiments: Record<string, unknown>[]; total: number }> {
    return this.client._request("GET", "/v1/experiments", {
      params: status ? { status } : undefined,
    });
  }

  /** Get experiment details with recent runs. */
  async get(experimentId: string): Promise<{ experiment: Record<string, unknown>; recent_runs: Record<string, unknown>[] }> {
    return this.client._request("GET", `/v1/experiments/${experimentId}`);
  }

  /** Create a new experiment. */
  async create(options: CreateExperimentOptions): Promise<{ experiment_id: string; status: string }> {
    return this.client._request("POST", "/v1/experiments", {
      json: options as unknown as Record<string, unknown>,
    });
  }

  /** Update experiment (only in draft or paused state). */
  async update(experimentId: string, fields: Record<string, unknown>): Promise<{ ok: boolean }> {
    return this.client._request("PUT", `/v1/experiments/${experimentId}`, {
      json: fields,
    });
  }

  /** Start experiment. Captures baseline metrics. */
  async start(experimentId: string): Promise<Record<string, unknown>> {
    return this.client._request("POST", `/v1/experiments/${experimentId}/start`);
  }

  /** Pause experiment. */
  async pause(experimentId: string): Promise<{ ok: boolean; status: string }> {
    return this.client._request("POST", `/v1/experiments/${experimentId}/pause`);
  }

  /** Resume paused experiment. */
  async resume(experimentId: string): Promise<Record<string, unknown>> {
    return this.client._request("POST", `/v1/experiments/${experimentId}/resume`);
  }

  /** Report experiment run results. Platform evaluates improvement. */
  async reportRun(
    experimentId: string,
    strategy: Record<string, unknown>,
    metrics: RunMetrics,
    notes?: string,
  ): Promise<{
    run_id: string;
    run_number: number;
    outcome: "improved" | "regressed" | "neutral";
    delta_vs_baseline: number;
    delta_vs_previous: number;
    experiment_status: string;
  }> {
    return this.client._request("POST", `/v1/experiments/${experimentId}/runs`, {
      json: {
        strategy_snapshot: strategy,
        metrics,
        notes: notes ?? "",
      },
    });
  }

  /** List all runs for an experiment. */
  async listRuns(
    experimentId: string,
    page = 1,
    limit = 20,
  ): Promise<{ runs: Record<string, unknown>[]; page: number; has_more: boolean }> {
    return this.client._request("GET", `/v1/experiments/${experimentId}/runs`, {
      params: { page, limit },
    });
  }

  /** Get best strategy and metrics. */
  async getBest(experimentId: string): Promise<{
    best_strategy: Record<string, unknown> | null;
    best_metrics: Record<string, unknown> | null;
    total_runs: number;
    successful_runs: number;
  }> {
    return this.client._request("GET", `/v1/experiments/${experimentId}/best`);
  }

  /** Adopt best strategy as agent's active auto-rules. */
  async adoptBest(experimentId: string): Promise<{ ok: boolean; adopted_strategy: Record<string, unknown> }> {
    return this.client._request("POST", `/v1/experiments/${experimentId}/adopt`);
  }
}
