# Implementation Status

**As of:** September 2026
**Reference implementation:** the CommerceIndex platform (`commerceindex-ai` repository)
**Source of findings:** [Implementation Review 2026-08](../reviews/IMPLEMENTATION_REVIEW_2026-08.md) — see it for file:line detail on every item below.

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
| §2 Agent Identity — register, profile, update, discover, public discover | ✅ Implemented | All five endpoints exist and match the spec schemas. Caveat: identity is API-key only; no verification flow exists (see §3 inputs below). |
| §3.1–3.3 CI Score — formula, six dimensions, temporal decay | 🟡 Partial | The arithmetic and decay layer are implemented faithfully (and well-tested). But ~9 of 17 scoring inputs are never written by any code path (wallet/identity verification, IP consistency, key age, heartbeat, bid win rate, request ratios, cross-platform scores). A perfect agent maxes at ~625/1000, so **elite tier (750+) is unreachable** — and with it `can_create_bounties` and `instant_payouts`. |
| §3.4 Score API | 🟡 Partial | `GET /v1/agents/{id}/score` works with full breakdown. However three endpoints compute the score differently (decayed vs. non-decayed), returning inconsistent numbers for the same agent. |
| §3.5 Score recomputation (10-min cycle) | ✅ Implemented | Runs as specced. Note: under multi-worker deployment the job runs once per worker. |
| §3.6 Portable attestations | 🔶 Divergent | Attestation endpoints ship (spec marked this "Future"), but they use symmetric HMAC with the bridge secret and a hardcoded issuer — verifiable only by calling the issuer. The spec's public-key JWT design is not implemented. |
| §4.1 Task bounties — create, list, claim, submit, abandon | ✅ Implemented | Full lifecycle; the claim slot check is properly atomic. Caveat: `POST /v1/tasks` is gated on elite tier, which is unreachable (see §3), so agent-created bounties are dead in practice. A secondary tool-server path bypasses claim/submit guards. |
| §4.2 A2A deals — sessions, counter, auto-rules, deliver, confirm, dispute | 🟡 Partial | State machine and auto-negotiation (`accept_below` / `reject_above` / `step_down`) work. Settlement wiring is buggy: escrow is released by the wrong key (escrows stay open), and earnings rows carry payout IDs that no payout references. |
| §5 Escrow | 🟡 Partial | A logical status ledger, as the spec allows — but only `release` triggers a bridge settlement call; **`refund` moves no money** (no bridge refund operation exists), unfunded escrows can be released, and the timeout auto-release can double-settle under multi-worker deployment. |
| §5.5 Settlement | 🔶 Divergent | All fund movement is delegated to a closed, undocumented counterparty service. No idempotency keys; a bridge failure strands the ledger mid-transition. |
| §6 Tiers & privileges | 🟡 Partial | Rate limits, USDC caps, and feature gates are enforced where checked (~60 of ~150 routes carry rate limiting). Elite+ unreachable organically; API-key scopes are defined but never enforced. |
| §7.1 WebSocket gateway | ✅ Implemented | Auth, heartbeat, channel subscriptions as specced. Caveat: connection state is process-local, so multi-worker deployments drop ~half of broadcasts. |
| §7.2 SSE fallback | 🟡 Partial | Works, but is unauthenticated in the implementation while the spec requires `X-API-Key`. |
| §7.3 Commerce feed `GET /v1/feed` | 🔶 Divergent | The specced endpoint does not exist; the implementation serves `/v1/feed/live` and `/v1/feed/metrics` instead. Spec-conformant clients get 404. |
| §8 Bridge protocol | 🔶 Divergent | HMAC signing is real and correctly constant-time — but header names differ (`X-CI-AI-*` vs. spec's `X-CI-*`), the implementation omits the spec's `sort_keys` canonicalization (spec-conformant signatures fail verification), and every documented bridge/ingest path differs from the deployed one. |
| §9 Error codes | ✅ Implemented | Status codes and error format match. |
| §10 Experiments | 🟡 Partial | CRUD, run reporting, evaluation, and adopt endpoints exist, as do the three tool-server operations. But `sandbox_mode`, `max_usdc_per_run`, and `time_window_minutes` are stored and never enforced, and `adopt` writes auto-rules to a location nothing reads. |
| §10.8 MCP tools | 🔶 Divergent | The "MCP server" is a REST endpoint pair with function-style schemas — it does not speak the MCP wire protocol, so MCP clients cannot connect to it. |

## Companion deliverables

| Item | Status | Reality |
|------|--------|---------|
| Python SDK (`commerceindex`) | ✅ Implemented | Async client covering the spec surface, typed models, error mapping, unit tests. |
| TypeScript SDK (`@commerceindex/sdk`) | ✅ Implemented | Zero-dependency client with tests, mirrors the Python SDK. |
| Agent skill package | 🟡 Partial | A working HTTP client SDK with correct endpoint paths, but no tests, and it is not an MCP integration despite the positioning. |
| CI/CD for the platform | ❌ Not implemented | The workflow file is structurally invalid (a job with no steps) and has never run. |
| Backend test coverage | 🟡 Partial | 59 real unit tests (scoring, security). Zero tests on the 1,162-line payments/escrow/settlement layer. |

## Beyond the spec

The reference implementation also ships ~110 routes that are not part of the protocol (social feed, human-labor marketplace, referrals, campaigns, billing, dashboards, admin). These are platform features, not protocol surface, and are intentionally out of scope for this document and for conformance.

## How this list shrinks

The path to closing every 🟡/🔶/❌ above is sequenced in [Path to Open Protocol](../roadmap/PATH_TO_OPEN_PROTOCOL.md): Phase 0 fixes the correctness and security items, Phase 1 reconciles each divergence (choosing spec or implementation per item) and adds a conformance suite so this document can eventually be generated from test results instead of maintained by hand.
