import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { CommerceIndex } from "../src/client.js";
import {
  AuthenticationError,
  InsufficientTierError,
  NotFoundError,
  ConflictError,
  RateLimitError,
} from "../src/errors.js";

// Mock fetch globally
const mockFetch = vi.fn();
vi.stubGlobal("fetch", mockFetch);

function mockResponse(body: unknown, status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
    text: async () => JSON.stringify(body),
  };
}

describe("CommerceIndex", () => {
  let ci: CommerceIndex;

  beforeEach(() => {
    ci = new CommerceIndex({ apiKey: "ci_ai_test_abc", baseUrl: "https://test.api" });
    mockFetch.mockReset();
  });

  describe("register", () => {
    it("should register a new agent", async () => {
      mockFetch.mockResolvedValueOnce(
        mockResponse({
          agent_id: "agent_abc",
          api_key: "ci_ai_live_xyz",
          ci_agent_score: 50,
          tier: "newcomer",
          badge: "gray",
          ws_url: "wss://test.api/v1/gateway/ws",
          sse_url: "https://test.api/v1/gateway/events",
          first_available_tasks: [],
          referral_code: "ref_abc",
          endpoints: {},
        })
      );

      const result = await ci.register({
        name: "test-agent",
        capabilities: ["research"],
      });

      expect(result.agent_id).toBe("agent_abc");
      expect(result.api_key).toBe("ci_ai_live_xyz");
      expect(result.tier).toBe("newcomer");
    });
  });

  describe("getAgent", () => {
    it("should get agent profile", async () => {
      mockFetch.mockResolvedValueOnce(
        mockResponse({
          agent_id: "agent_abc",
          name: "Test Agent",
          capabilities: ["research"],
          ci_agent_score: 450,
          tier: "established",
        })
      );

      const agent = await ci.getAgent("agent_abc");
      expect(agent.agent_id).toBe("agent_abc");
      expect(agent.ci_agent_score).toBe(450);
    });
  });

  describe("error handling", () => {
    it("should throw AuthenticationError on 401", async () => {
      mockFetch.mockResolvedValueOnce(
        mockResponse({ detail: "Invalid API key" }, 401)
      );

      await expect(ci.getAgent("agent_abc")).rejects.toThrow(AuthenticationError);
    });

    it("should throw InsufficientTierError on 403", async () => {
      mockFetch.mockResolvedValueOnce(
        mockResponse(
          {
            detail: {
              error: {
                code: "insufficient_tier",
                message: "A2A requires established+ tier",
              },
            },
          },
          403
        )
      );

      await expect(
        ci.deals.propose({
          to_agent: "agent_xyz",
          deal_type: "task_delegation",
          offer_usdc: 25.0,
        })
      ).rejects.toThrow(InsufficientTierError);
    });

    it("should throw NotFoundError on 404", async () => {
      mockFetch.mockResolvedValueOnce(
        mockResponse({ detail: "Agent not found" }, 404)
      );

      await expect(ci.score.get("agent_none")).rejects.toThrow(NotFoundError);
    });

    it("should throw ConflictError on 409", async () => {
      mockFetch.mockResolvedValueOnce(
        mockResponse({ detail: "Already claimed" }, 409)
      );

      await expect(ci.bounties.claim("task_abc")).rejects.toThrow(ConflictError);
    });

    it("should throw RateLimitError on 429", async () => {
      mockFetch.mockResolvedValueOnce(
        mockResponse({ detail: "Rate limit exceeded" }, 429)
      );

      await expect(ci.getAgent("agent_abc")).rejects.toThrow(RateLimitError);
    });
  });

  describe("score", () => {
    it("should get CI score", async () => {
      mockFetch.mockResolvedValueOnce(
        mockResponse({
          agent_id: "agent_abc",
          ci_agent_score: 450,
          tier: "established",
          badge: "silver",
          privileges: { can_a2a: true },
          breakdown: {
            trust: { score: 72.5, weight: 0.25, contribution: 181.3, factors: [] },
          },
          improvements: [{ dimension: "trust", action: "Verify wallet", potential_gain: 50 }],
          history_30d: [50, 200, 450],
          rank: 42,
          percentile: 89.5,
          computed_at: "2026-03-07T12:00:00Z",
        })
      );

      const score = await ci.score.get("agent_abc");
      expect(score.ci_agent_score).toBe(450);
      expect(score.tier).toBe("established");
      expect(score.rank).toBe(42);
    });
  });

  describe("bounties", () => {
    it("should list open bounties", async () => {
      mockFetch.mockResolvedValueOnce(
        mockResponse({
          tasks: [
            { task_id: "task_001", title: "Research", bounty_usdc: 50, status: "open" },
          ],
          total: 1,
          has_more: false,
        })
      );

      const result = await ci.bounties.list({ min_bounty: 10 });
      expect(result.tasks).toHaveLength(1);
      expect(result.tasks[0].bounty_usdc).toBe(50);
    });

    it("should claim a bounty", async () => {
      mockFetch.mockResolvedValueOnce(
        mockResponse({ ok: true, assignment_id: "assign_abc", status: "claimed" })
      );

      const result = await ci.bounties.claim("task_001");
      expect(result.ok).toBe(true);
    });
  });

  describe("deals", () => {
    it("should propose a deal", async () => {
      mockFetch.mockResolvedValueOnce(
        mockResponse({ ok: true, session_id: "a2a_abc", status: "initiated" })
      );

      const result = await ci.deals.propose({
        to_agent: "agent_xyz",
        deal_type: "task_delegation",
        offer_usdc: 25.0,
      });
      expect(result.ok).toBe(true);
      expect(result.session_id).toBe("a2a_abc");
    });

    it("should accept a deal", async () => {
      mockFetch.mockResolvedValueOnce(
        mockResponse({ ok: true, status: "escrowed", agreed_amount_usdc: 25.0 })
      );

      const result = await ci.deals.accept("a2a_abc");
      expect(result.status).toBe("escrowed");
    });
  });

  describe("escrow", () => {
    it("should get escrow status", async () => {
      mockFetch.mockResolvedValueOnce(
        mockResponse({
          escrow_id: "esc_abc",
          escrow_type: "task",
          amount_usdc: 50.0,
          status: "funded",
        })
      );

      const escrow = await ci.escrow.get("esc_abc");
      expect(escrow.escrow_id).toBe("esc_abc");
      expect(escrow.status).toBe("funded");
    });
  });
});
