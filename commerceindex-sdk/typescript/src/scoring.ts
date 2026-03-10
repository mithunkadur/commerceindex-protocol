/** CommerceIndex SDK — CI Score operations. */

import type { CommerceIndex } from "./client.js";
import type { CIScore } from "./types.js";

export class ScoreClient {
  constructor(private client: CommerceIndex) {}

  /** Get full CI Agent Score breakdown. */
  async get(agentId: string): Promise<CIScore> {
    return this.client._request<CIScore>("GET", `/v1/agents/${agentId}/score`);
  }
}
