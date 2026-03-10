/** CommerceIndex SDK — A2A deal operations. */

import type { CommerceIndex } from "./client.js";
import type { A2ASession, ProposeOptions } from "./types.js";

export class DealClient {
  constructor(private client: CommerceIndex) {}

  /** Initiate an A2A deal (established+ tier). */
  async propose(options: ProposeOptions): Promise<{ ok: boolean; session_id: string; status: string }> {
    const payload: Record<string, unknown> = {
      counterparty_agent_id: options.to_agent,
      deal_type: options.deal_type,
      initial_offer_usdc: options.offer_usdc,
      description: options.description ?? "",
      items: options.items ?? {},
    };
    if (options.auto_rules) payload.auto_rules = options.auto_rules;

    return this.client._request("POST", "/v1/a2a/sessions", { json: payload });
  }

  /** Get A2A session details. */
  async get(sessionId: string): Promise<A2ASession> {
    return this.client._request<A2ASession>("GET", `/v1/a2a/sessions/${sessionId}`);
  }

  /** Send a counter-offer. */
  async counter(
    sessionId: string,
    offerUsdc: number,
    message?: string
  ): Promise<{ ok: boolean; status: string; round: number }> {
    const payload: Record<string, unknown> = { action: "counter", offer_usdc: offerUsdc };
    if (message) payload.message = message;
    return this.client._request("POST", `/v1/a2a/sessions/${sessionId}/counter`, {
      json: payload,
    });
  }

  /** Accept the current offer. */
  async accept(sessionId: string): Promise<{ ok: boolean; status: string; agreed_amount_usdc: number }> {
    return this.client._request("POST", `/v1/a2a/sessions/${sessionId}/counter`, {
      json: { action: "accept" },
    });
  }

  /** Reject the deal. */
  async reject(
    sessionId: string,
    message?: string
  ): Promise<{ ok: boolean; status: string }> {
    const payload: Record<string, unknown> = { action: "reject" };
    if (message) payload.message = message;
    return this.client._request("POST", `/v1/a2a/sessions/${sessionId}/counter`, {
      json: payload,
    });
  }

  /** Deliver goods/data/service (seller only). */
  async deliver(
    sessionId: string,
    deliveryData: Record<string, unknown>,
    deliverySummary = ""
  ): Promise<{ ok: boolean; status: string }> {
    return this.client._request("POST", `/v1/a2a/sessions/${sessionId}/deliver`, {
      json: { delivery_data: deliveryData, delivery_summary: deliverySummary },
    });
  }

  /** Confirm delivery, release escrow (buyer only). */
  async confirm(sessionId: string): Promise<{ ok: boolean; status: string; payout_usdc: number }> {
    return this.client._request("POST", `/v1/a2a/sessions/${sessionId}/confirm`);
  }

  /** Dispute the deal, freeze escrow. */
  async dispute(sessionId: string): Promise<{ ok: boolean; status: string }> {
    return this.client._request("POST", `/v1/a2a/sessions/${sessionId}/dispute`);
  }

  /** Get agent's A2A deal history. */
  async history(
    agentId: string,
    options?: { status?: string; limit?: number }
  ): Promise<A2ASession[]> {
    const data = await this.client._request<{ sessions: A2ASession[] }>(
      "GET",
      `/v1/agents/${agentId}/a2a`,
      { params: options as Record<string, unknown> | undefined }
    );
    return data.sessions;
  }
}
