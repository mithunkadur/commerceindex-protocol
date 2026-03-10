/** CommerceIndex SDK — Escrow operations. */

import type { CommerceIndex } from "./client.js";
import type { Escrow } from "./types.js";

export class EscrowClient {
  constructor(private client: CommerceIndex) {}

  /** Get escrow status. */
  async get(escrowId: string): Promise<Escrow> {
    return this.client._request<Escrow>("GET", `/v1/escrow/${escrowId}`);
  }

  /** Dispute an escrow (freeze funds). Must be a party. */
  async dispute(escrowId: string): Promise<{ ok: boolean; status: string }> {
    return this.client._request("POST", `/v1/escrow/${escrowId}/dispute`);
  }
}
