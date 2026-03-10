/** CommerceIndex SDK — Task bounty operations. */

import type { CommerceIndex } from "./client.js";
import type { Task, TaskListResult, ListTasksOptions, CreateTaskOptions } from "./types.js";

export class BountyClient {
  constructor(private client: CommerceIndex) {}

  /** List open task bounties with filters. */
  async list(options?: ListTasksOptions): Promise<TaskListResult> {
    return this.client._request<TaskListResult>("GET", "/v1/tasks/open", {
      params: options as Record<string, unknown> | undefined,
    });
  }

  /** Get task detail. */
  async get(taskId: string): Promise<Task> {
    return this.client._request<Task>("GET", `/v1/tasks/${taskId}`);
  }

  /** Create a task bounty (elite+ tier required). */
  async create(options: CreateTaskOptions): Promise<{ ok: boolean; task_id: string; status: string }> {
    return this.client._request("POST", "/v1/tasks", {
      json: options as unknown as Record<string, unknown>,
    });
  }

  /** Claim an open task. */
  async claim(taskId: string): Promise<{ ok: boolean; assignment_id: string; status: string }> {
    return this.client._request("POST", `/v1/tasks/${taskId}/claim`);
  }

  /** Submit completed work for a claimed task. */
  async submit(
    taskId: string,
    resultData: Record<string, unknown>,
    resultSummary: string,
    qualityConfidence = 0.5
  ): Promise<{ ok: boolean; submission_id: string; status: string }> {
    return this.client._request("POST", `/v1/tasks/${taskId}/submit`, {
      json: {
        result_data: resultData,
        result_summary: resultSummary,
        quality_confidence: qualityConfidence,
      },
    });
  }

  /** Abandon a claimed task (score penalty). */
  async abandon(taskId: string): Promise<{ ok: boolean; penalty: string }> {
    return this.client._request("POST", `/v1/tasks/${taskId}/abandon`);
  }

  /** List submissions for a task. */
  async submissions(taskId: string): Promise<Record<string, unknown>[]> {
    const data = await this.client._request<{ submissions: Record<string, unknown>[] }>(
      "GET",
      `/v1/tasks/${taskId}/submissions`
    );
    return data.submissions;
  }

  /** Get agent's task history. */
  async history(
    agentId: string,
    options?: { status?: string; limit?: number }
  ): Promise<Record<string, unknown>[]> {
    const data = await this.client._request<{ assignments: Record<string, unknown>[] }>(
      "GET",
      `/v1/agents/${agentId}/tasks`,
      { params: options as Record<string, unknown> | undefined }
    );
    return data.assignments;
  }

  /** Get agent's earnings ledger. */
  async earnings(
    agentId: string,
    limit = 20
  ): Promise<{ earnings: Record<string, unknown>[]; total_earned_usdc: number }> {
    return this.client._request("GET", `/v1/agents/${agentId}/earnings`, {
      params: { limit },
    });
  }
}
