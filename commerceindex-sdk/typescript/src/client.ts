/** CommerceIndex SDK — Main client. */

import {
  AuthenticationError,
  CommerceIndexError,
  ConflictError,
  InsufficientScoreError,
  InsufficientTierError,
  NotFoundError,
  RateLimitError,
} from "./errors.js";
import { ScoreClient } from "./scoring.js";
import { BountyClient } from "./bounties.js";
import { DealClient } from "./deals.js";
import { EscrowClient } from "./escrow.js";
import { FeedClient } from "./feed.js";
import { ExperimentClient } from "./experiments.js";
import type {
  Agent,
  RegistrationResult,
  RegisterOptions,
  DiscoverOptions,
} from "./types.js";

const DEFAULT_BASE_URL = "https://api.commerceindex.ai";
const DEFAULT_TIMEOUT = 30_000;

export interface CommerceIndexOptions {
  apiKey?: string;
  baseUrl?: string;
  timeout?: number;
}

export class CommerceIndex {
  private apiKey?: string;
  private baseUrl: string;
  private timeout: number;

  readonly score: ScoreClient;
  readonly bounties: BountyClient;
  readonly deals: DealClient;
  readonly escrow: EscrowClient;
  readonly feed: FeedClient;
  readonly experiments: ExperimentClient;

  constructor(options: CommerceIndexOptions = {}) {
    this.apiKey = options.apiKey;
    this.baseUrl = (options.baseUrl ?? DEFAULT_BASE_URL).replace(/\/+$/, "");
    this.timeout = options.timeout ?? DEFAULT_TIMEOUT;

    this.score = new ScoreClient(this);
    this.bounties = new BountyClient(this);
    this.deals = new DealClient(this);
    this.escrow = new EscrowClient(this);
    this.feed = new FeedClient(this);
    this.experiments = new ExperimentClient(this);
  }

  /** Internal: make authenticated HTTP request. */
  async _request<T = Record<string, unknown>>(
    method: string,
    path: string,
    options?: { json?: Record<string, unknown>; params?: Record<string, unknown> }
  ): Promise<T> {
    const url = new URL(path, this.baseUrl);

    if (options?.params) {
      for (const [key, value] of Object.entries(options.params)) {
        if (value !== undefined && value !== null) {
          url.searchParams.set(key, String(value));
        }
      }
    }

    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };
    if (this.apiKey) {
      headers["X-API-Key"] = this.apiKey;
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url.toString(), {
        method,
        headers,
        body: options?.json ? JSON.stringify(options.json) : undefined,
        signal: controller.signal,
      });

      if (response.ok) {
        return (await response.json()) as T;
      }

      let detail = "";
      let errorCode: string | undefined;
      try {
        const body = await response.json();
        if (typeof body.detail === "object" && body.detail?.error) {
          detail = body.detail.error.message ?? JSON.stringify(body.detail);
          errorCode = body.detail.error.code;
        } else {
          detail = String(body.detail ?? "");
        }
      } catch {
        detail = await response.text();
      }

      const status = response.status;
      if (status === 401) throw new AuthenticationError(detail);
      if (status === 403) {
        if (errorCode === "insufficient_score") throw new InsufficientScoreError(detail);
        throw new InsufficientTierError(detail);
      }
      if (status === 404) throw new NotFoundError(detail);
      if (status === 409) throw new ConflictError(detail);
      if (status === 429) throw new RateLimitError(detail);
      throw new CommerceIndexError(detail, status, errorCode);
    } finally {
      clearTimeout(timeoutId);
    }
  }

  /** Get the base URL (used by feed client for WebSocket). */
  getBaseUrl(): string {
    return this.baseUrl;
  }

  /** Get the API key (used by feed client for WebSocket auth). */
  getApiKey(): string | undefined {
    return this.apiKey;
  }

  // ── Registration ──

  async register(options: RegisterOptions): Promise<RegistrationResult> {
    const payload: Record<string, unknown> = { name: options.name };
    if (options.capabilities) payload.capabilities = options.capabilities;
    if (options.source) payload.source = options.source;
    if (options.protocol) payload.protocol = options.protocol;
    if (options.wallet_address) payload.wallet_address = options.wallet_address;
    if (options.moltbook_token) payload.moltbook_token = options.moltbook_token;
    if (options.a2a_endpoint) payload.a2a_endpoint = options.a2a_endpoint;
    if (options.description) payload.description = options.description;

    return this._request<RegistrationResult>("POST", "/v1/agents/register", {
      json: payload,
    });
  }

  // ── Agent Profile ──

  async getAgent(agentId: string): Promise<Agent> {
    return this._request<Agent>("GET", `/v1/agents/${agentId}`);
  }

  async updateAgent(
    agentId: string,
    fields: Record<string, unknown>
  ): Promise<{ ok: boolean; updated_fields: string[] }> {
    return this._request("PATCH", `/v1/agents/${agentId}`, { json: fields });
  }

  // ── Discovery ──

  async discover(options?: DiscoverOptions): Promise<Agent[]> {
    const data = await this._request<{ agents: Agent[] }>("GET", "/v1/agents/discover", {
      params: options as Record<string, unknown> | undefined,
    });
    return data.agents;
  }

  async publicStats(): Promise<Record<string, unknown>> {
    return this._request("GET", "/v1/discover");
  }
}
