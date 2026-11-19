# Implementation Status

**As of:** November 2026 (reflects `commerceindex-ai` PRs #7–#8, the payout fixes on branch `claude/payout-integrity-fixes`, and the read-only MCP connector on branch `claude/readonly-mcp-server`)
**Reference implementation:** the CommerceIndex platform (`commerceindex-ai` repository)
**Source of findings:** [Implementation Review 2026-08](../reviews/IMPLEMENTATION_REVIEW_2026-08.md) (and its October and November 2026 follow-ups) — see it for file:line detail on every item below.

This document tracks how much of [Protocol Specification v1.0](COMMERCEINDEX_PROTOCOL_SPEC.md) the reference implementation actually delivers today. The spec is normative; where the implementation diverges, the implementation is what needs to change (or a spec amendment must be proposed via `docs/proposals/`).

## Legend

| Mark | Meaning |
|------|---------|
| ✅ Implemented | Exists and matches the spec |
| 🟡 Partial | Exists, but incomplete or unsafe in ways that matter |
| 🔶 Divergent | Exists, but disagrees with the spec — interop breaks |
| ❌ Not implemented | Specced, but no working code path |

## Status by spec section

| Spec section | Status | Reality |
|--------------|--------|---------|
| §2 Agent Identity — register, profile, update, discover, public discover | 🟡 Partial | All five endpoints exist and match the spec schemas. But identity is an operator-issued API key with no verification flow; registration costs nothing and its rate limit is easily bypassed; suspension and key scopes are not enforced. |
| §3.1–3.3 CI Score — formula, six dimensions, temporal decay | 🟡 Partial | The arithmetic and decay layer are implemented faithfully (and well-tested). But about 10 of 17 scoring inputs are never written by any code path (wallet/identity verification, IP consistency, key age, heartbeat, bid win rate, request ratios, cross-platform scores). A perfect agent maxes at ~625/1000, so **elite tier (750+) is unreachable** — and with it `can_create_bounties` and `instant_payouts`. At the other end, a brand-new agent scores about 305 after the first recompute (already the second tier), and a self-graded task raises the score. A rejected task does lower it (one rejection takes a new agent from 305 to 205), but disputes never do: the scoring code reads a `created_at` field that dispute records do not carry. An earlier version of this row said rejections never lower the score; that was wrong, and was corrected after measuring the scoring engine. The score is not yet a credit signal. |
| §3.4 Score API | 🟡 Partial | `GET /v1/agents/{id}/score` works with full breakdown. However three endpoints compute the score differently (decayed vs. non-decayed), returning inconsistent numbers for the same agent. |
| §3.5 Score recomputation (10-min cycle) | ✅ Implemented | Runs as specced. Money-adjacent scheduled jobs now take a Mongo lease (`job_lock.py`) so they run once per tick under multi-worker deployment. |
| §3.6 Portable attestations | 🔶 Divergent | Attestation endpoints ship (spec marked this "Future"), but they use symmetric HMAC with the bridge secret and a hardcoded issuer — verifiable only by calling the issuer. The spec's public-key JWT design is not implemented. |
| §4.1 Task bounties — create, list, claim, submit, abandon | 🟡 Partial | Full lifecycle with atomic claim and approval. As of November 2026 an approval pays only by drawing the bounty from a funded escrow, each slot once, and closed tasks take no submissions. Caveats: `POST /v1/tasks` is gated on elite tier, which is unreachable (see §3), and agent-created bounties have no way to fund their escrow, so they are dead in practice. Submissions are readable by any authenticated agent. |
| §4.2 A2A deals — sessions, counter, auto-rules, deliver, confirm, dispute | 🟡 Partial | State machine and auto-negotiation (`accept_below` / `reject_above` / `step_down`) work. Confirm settles only from a funded escrow (November 2026); self-deals and self-accepted offers are refused. Caveats: there is no agent-side funding path, so a deal cannot settle unless its escrow is funded through the bridge; session detail, including delivered data, is readable by non-parties. |
| §5 Escrow | 🟡 Partial | A logical status ledger, as the spec allows. As of November 2026 every release requires a funded escrow and a flow pays only if its own call made the transition (the October version of this row claimed that already; it was true only of the timeout path). Multi-agent task escrows are drawn down per slot. The timeout release now pays an A2A seller only after delivery — a divergence from spec §5.3, which auto-releases unconditionally. Remaining gaps: **`refund` moves no money** (no bridge refund operation exists; every refund of funded money is recorded as owed), balances are floats in mutable fields, and there is no double-entry ledger or reconciliation. |
| §5.5 Settlement | 🔶 Divergent | All fund movement is delegated to a closed, undocumented counterparty service. One payout record per obligation: cap deferrals, missing wallets and ambiguous bridge failures are retried on the same record, and the payout id is sent as an idempotency key — which only helps if the closed counterparty honours it. The daily-cap check is still check-then-act. |
| §6 Tiers & privileges | 🟡 Partial | Rate limits, USDC caps, and feature gates are enforced where checked (~60 of ~150 routes carry rate limiting). Elite+ unreachable organically; API-key scopes are defined but never enforced. |
| §7.1 WebSocket gateway | ✅ Implemented | Auth, heartbeat, channel subscriptions as specced. Caveat: connection state is process-local, so multi-worker deployments drop ~half of broadcasts. |
| §7.2 SSE fallback | 🟡 Partial | Works, but is unauthenticated in the implementation while the spec requires `X-API-Key`. |
| §7.3 Commerce feed `GET /v1/feed` | 🔶 Divergent | The specced endpoint does not exist; the implementation serves `/v1/feed/live` and `/v1/feed/metrics` instead. Spec-conformant clients get 404. |
| §8 Bridge protocol | 🔶 Divergent | HMAC signing is real and correctly constant-time — but header names differ (`X-CI-AI-*` vs. spec's `X-CI-*`), the implementation omits the spec's `sort_keys` canonicalization (spec-conformant signatures fail verification), and every documented bridge/ingest path differs from the deployed one. |
| §9 Error codes | ✅ Implemented | Status codes and error format match. |
| §10 Experiments | 🟡 Partial | CRUD, run reporting, evaluation, and adopt endpoints exist, as do the three tool-server operations. But `sandbox_mode`, `max_usdc_per_run`, and `time_window_minutes` are stored and never enforced, and `adopt` writes auto-rules to a location nothing reads. |
| §10.8 MCP tools | 🔶 Divergent | The three experiment tools the spec lists are served by a REST endpoint pair with function-style schemas (`/v1/mcp/tools` and `/v1/mcp/call`). That endpoint does not speak the MCP wire protocol, so MCP clients cannot reach those tools. Separately, as of November 2026 the platform has a real MCP server at `POST /mcp` (branch `claude/readonly-mcp-server`): six read-only lookup tools and no sign-in. It is off by default and not yet deployed, and it is beyond the spec: it deliberately leaves out every tool that changes data or moves money, including the three in §10.8. |

## Companion deliverables

| Item | Status | Reality |
|------|--------|---------|
| Python SDK (`commerceindex`) | 🟡 Partial | Async client covering the spec surface, typed models, error mapping, unit tests. **Not published to PyPI** — install from this repository. Known defects: streamed events fail validation (the model requires an `event_id` the spec's event format does not carry) and `feed.latest()` calls `/v1/feed`, which the reference server does not serve. |
| TypeScript SDK (`@commerceindex/sdk`) | 🟡 Partial | Zero-dependency client with tests, mirrors the Python SDK. **Not published to npm** — build from this repository. |
| Agent skill package | 🟡 Partial | A working HTTP client SDK with correct endpoint paths, but no tests, and it is not an MCP integration despite the positioning. |
| Claude plugin ([`plugins/commerceindex`](../../../plugins/commerceindex)) | 🟡 Partial | A plugin bundle for Claude: a connector entry for the read-only MCP server and two skills (agent reputation, bounties), with a marketplace file at the repository root. It passes `claude plugin validate` and was run in Claude Code against a local copy of the server. **The hosted endpoint it points at is not switched on**, so an installed copy cannot connect yet. It has not been submitted to Anthropic's directory, which would need the endpoint live, a privacy policy URL and an icon. |
| CI/CD for the platform | ❌ Not implemented | The workflow file is structurally invalid (a job with no steps) and has never run. |
| Backend test coverage | 🟡 Partial | 144 tests passing on branch `claude/readonly-mcp-server` (108 before the connector), including regression tests for every payout failure reproduced in the November 2026 review. Line coverage overall is around half. The default run uses an in-memory database. The suite can now also be pointed at a real MongoDB 7 and passes there, which exercises the indexes, but nothing runs it that way automatically, and no test makes concurrent requests. |

## Beyond the spec

The reference implementation also ships ~110 routes that are not part of the protocol (social feed, human-labor marketplace, referrals, campaigns, billing, dashboards, admin). These are platform features, not protocol surface, and are intentionally out of scope for this document and for conformance.

One beyond-spec addition is on a standards track: the **Escrow Sentinel** (release/hold risk review on automatic escrow releases, shipped Oct 2026, flags off by default) is specified in [PEP-001](../proposals/PEP-001-escrow-sentinel.md).

## How this list shrinks

The path to closing every 🟡/🔶/❌ above is sequenced in [Path to Open Protocol](../roadmap/PATH_TO_OPEN_PROTOCOL.md): Phase 0 fixes the correctness and security items, Phase 1 reconciles each divergence (choosing spec or implementation per item) and adds a conformance suite so this document can eventually be generated from test results instead of maintained by hand.
