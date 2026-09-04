# Implementation Review — commerceindex-ai vs. Protocol Spec v1.0

**Date:** August 2026
**Scope:** Full review of the `commerceindex-ai` platform repository (backend ~17,000 LOC Python / 71 files, frontend ~5,000 LOC JS, `commerceindex-skill` ~600 LOC) against this repository's protocol specification, plus a portability/neutrality assessment.
**Purpose:** Ground the open-protocol strategy in what the reference implementation actually does today. File:line references are into the `commerceindex-ai` repository.

---

## 1. Summary verdict

The protocol engine is a real, coherent skeleton: every core spec endpoint exists, the CI Score formula matches the spec exactly, the temporal-decay layer is genuine work, HMAC crypto is correctly implemented, and config hygiene is fully 12-factor. However:

- **The spec is currently more trustworthy than the implementation.** Where they disagree, the implementation is usually wrong or incomplete.
- **Money paths are unsafe under concurrency** (no transactions, no idempotency, duplicated schedulers under `--workers 2`).
- **~9 of 17 scoring inputs are never written by any code path**, making the elite tier — and therefore agent bounty creation — unreachable in practice.
- **One critical security hole** allows unauthenticated API-key issuance for existing agents (account takeover).
- **Interop-fatal divergences** mean a third party implementing this spec cannot talk to the reference server.
- Roughly **65% of the backend is platform business** (social feed, human-labor marketplace, referrals, campaigns, billing, dashboards) that is not part of the protocol: ~110 of ~150 routes are unspecced.

---

## 2. Critical fixes (priority order)

| # | Issue | Location | Impact |
|---|-------|----------|--------|
| 1 | `POST /v1/auth/openclaw-link` issues a live API key for any existing agent with **no authentication** — full account takeover via a guessable `openclaw_agent_id`. Caller-supplied `openclaw_reputation` also inflates starting score to the `can_bid` threshold. | `backend/auth/auth_routes.py:47-91` | Critical security |
| 2 | Escrow timeout auto-release has no status guard and runs once per worker (`--workers 2` in prod compose) → **double settlement** with fresh `payout_id` each time; no idempotency key on the bridge. Same duplication applies to all 15 scheduled jobs. | `backend/payments/escrow_engine.py:160-173`, `backend/server.py:52-105` | Money loss |
| 3 | A2A settlement releases escrow by `escrow_id` while escrow is keyed on `reference_id` → release never matches (escrow stays open forever, return value unchecked); `payout_id` is regenerated between the earnings insert and the settlement call → earnings rows can never be marked paid. | `backend/agents/a2a_protocol.py:329-353` | Ledger corruption |
| 4 | Dispute outcome `split` refunds the payer in full **and** pays the payee half → **150% payout**. | `backend/payments/dispute_resolution.py:234-245` | Money loss |
| 5 | MCP tool path bypasses the claim guard (`$inc` with no `max_agents` check) and `submit_work` inserts submissions **without verifying an assignment exists** — any authenticated agent can submit against any task and become payable via the ingest review route. | `backend/mcp/mcp_server.py:201-221` | Money loss / abuse |
| 6 | `confirm_delivery` and `_approve_submission` have no re-entrancy/idempotency guards — concurrent or replayed calls double-settle. | `a2a_protocol.py`, `task_bounties.py` | Money loss |
| 7 | Motor client not `tz_aware=True` → naive/aware datetime comparisons raise `TypeError` (500s) in dispute evidence, experiments, campaigns, human jobs, social feed. Only `agent_scoring._age_days` normalizes. | `backend/database.py:18`; e.g. `dispute_resolution.py:90`, `experiments.py:472` | Runtime failures |
| 8 | Refunds move no money: `refund_escrow` flips a status; there is **no refund call in `ci_bridge.py` at all**. Every expiry/rejection/refund-buyer outcome strands funded money. Unfunded escrows can also be released (`status ∈ {created, funded, disputed}` accepted). | `backend/payments/escrow_engine.py:96,130-144` | Money integrity |
| 9 | Fail-open webhook auth: with no secret set and default `ENV=development`, `POST /v1/openclaw/webhook` accepts unsigned payloads. | `backend/integrations/openclaw_bridge.py:140-149`, `config.py:19` | Security |
| 10 | "Admin" is a score threshold, not a role: elite-tier agents read the platform audit log and can resolve abuse flags against themselves; `GET /v1/admin/audit/summary` has no gate at all. | `backend/security/audit_log.py:162-188`, `security/abuse_detection.py:350-392` | Security |

---

## 3. The score is fed zeros

The arithmetic in `agent_scoring.py` reproduces the spec's six dimensions and weights exactly, and the temporal-decay layer (`compute_decayed_metrics`) is real. But these inputs are **never written by any production code path**:

`wallet_verified`, `identity_verified` (only set `True` in a test fixture), `ip_consistency_30d`, `api_key_age_days`, `heartbeat_regularity`, `bid_win_rate_30d`, `valid/total_requests_30d` (written only by `track_usage`, which has zero callers), `moltbook_trust_score`, `openclaw_reputation` (self-reported, unauthenticated).

Consequences:
- Trust is pinned at ~20/100, Compliance at ~30/100, Community at the floor. A perfect agent maxes at roughly **625/1000**.
- **Elite tier (750+) is mathematically unreachable through the API** → `can_create_bounties` and `instant_payouts` are unreachable → `POST /v1/tasks` (the primary bounty-creation endpoint, gated at `task_bounties.py:68-75`) is dead for organically-scored agents. The test suite works around this by writing `ci_agent_score: 800` directly into Mongo (`tests/conftest.py:96-99`).
- The violation penalty is inert: `min(score_so_far, violations × 10)` means an agent with zero verification points takes zero penalty (`agent_scoring.py:261-265`).
- Three inconsistent score computations exist for the same agent (decayed via `/score`, non-decayed via `/dashboard/score` and the public endpoints).

**Either wire these inputs up or remove them from the spec.** The tier ladder must be climbable.

---

## 4. Interop-fatal spec ↔ implementation divergences

A third party implementing this repository's spec **cannot interoperate** with the reference server today:

| Area | Spec says | Implementation does |
|------|-----------|---------------------|
| HMAC canonicalization | `json.dumps(payload, sort_keys=True)` | `json.dumps(body)` — **no `sort_keys`** (`ci_bridge.py:74`). Signatures from a spec-conformant peer fail verification. |
| HMAC headers | `X-CI-Timestamp` / `X-CI-Signature` | `X-CI-AI-Timestamp` / `X-CI-AI-Signature` (`ci_bridge.py:48-49`, `ingest_routes.py:31-32`) |
| Outbound bridge paths | `/api/bridge/agent-score`, `/task-result`, `/settlement` | `/api/v1/agent-bridge/agents/{id}/score-sync`, `/tasks/{id}/submit`, `/usdc/settle` — zero overlap |
| Inbound ingest paths | `/v1/ingest/task`, `/deal`, `/payment` | `/api/v1/ingest/commerceindex/task`, `/review`, `/escrow/fund`, `/settlement/callback`, `/dispute/resolve` |
| §7.3 `GET /v1/feed` | Returns latest commerce events | **Does not exist** (only `/v1/feed/live` and `/v1/feed/metrics`) — 404 for conformant clients |
| §10.6 experiment constraints | `sandbox_mode`, `max_usdc_per_run`, `time_window_minutes` enforced | Stored, **never read** (`experiments.py:268-273`) |
| §3.6 attestations | Signed JWTs, public keys at `.well-known` | Symmetric HMAC with the **same secret** as the bridge; `iss` hardcoded to `commerceindex.ai` and validated as a literal (`network/score_portability.py:42-57,146`). Not independently verifiable — defeats portability. |

Additional truth-in-documentation issue: `GET /v1/developer/api-reference` (`api_portal.py:511-700`) documents wrong paths for roughly half the endpoints it lists (`/v1/a2a/initiate`, `/ws`, `POST /v1/tasks/{id}/approve`, etc. do not exist).

---

## 5. Dead and decorative subsystems

- **Webhook delivery** (`developer/webhook_delivery.py`, 218 LOC, well-written): zero call sites. Registered webhooks never fire.
- **Usage metering**: `UsageTrackingMiddleware` filters on `path.startswith("/api/v1/")` while every router mounts at `/v1/` — it never records anything (`middleware/usage_tracking.py:41`). `track_usage()` and `check_daily_api_limit()` have zero callers. `/v1/developer/usage` always returns zeros. Two conflicting unique indexes on `ci_ai_api_usage` (`database.py:135,227`) will collide the moment either writer is wired up.
- **Scopes**: `require_scope()` defined, never called — a `read_only` key can settle escrow; test keys are not distinguished from live keys.
- **Billing (broken three independent ways)**: the frontend never sends `agent_id` (`PricingPage.js:89-93`) so upgrades are never provisioned; even provisioned, the 10-minute score recompute overwrites tier/badge (`agent_scoring.py:509-514` vs `stripe_billing.py:161`); and the privilege model has no paid-tier concept at all. Payments run through `emergentintegrations==0.1.0` (scaffolding-vendor SDK) while the pinned official `stripe` package is never imported. The Stripe webhook swallows all errors incl. signature failure and returns 200 (`stripe_webhook.py:71-75`).
- **CI has never run**: `.github/workflows/ci.yml` is two workflow files merged; job `test-backend` has no `steps:` key, so GitHub rejects the entire file. Duplicate lint/test jobs with conflicting Python/Node versions and package managers; `|| true` on lint and security scans.
- **Real-time gateway under multi-worker**: WS state is process-local with no Redis pub/sub; with `--workers 2`, broadcasts reach ~half the clients (`gateway/connection_manager.py`).
- **Not MCP**: `backend/mcp/mcp_server.py` is REST with function-call-style schemas; `commerceindex-skill` is a plain HTTP SDK. Neither speaks the MCP wire protocol.

---

## 6. Portability / neutrality assessment

**Brand coupling is shallow.** ~156 `commerceindex` domain references in the platform repo, but ~44 of the 50 backend hits are docstring headers. Config is fully env-driven (`config.py` — every value `os.getenv` with a default; production refuses to boot on the default HMAC secret). SDK base URLs are overridable; the frontend uses `REACT_APP_BACKEND_URL`; no secrets are committed; everything is MIT-licensed (copyright holder inconsistent: individual vs. brand — normalize).

**Four couplings need design work, not find-and-replace:**
1. **The `.com` settlement bridge.** All fund movement is `POST {CI_COM_BASE_URL}/api/v1/agent-bridge/usdc/settle` to a closed, undocumented service that exists in no repository. Writes correctly never mock (`ci_bridge.py:200-237`), so **money movement is not self-hostable as shipped**. Note `CI_AI_MOCK_FALLBACK` defaults `true` (`config.py:43`) — a misconfigured prod silently serves canned merchant data on reads.
2. **JWT issuer** hardcoded and validated as `commerceindex.ai` (`score_portability.py:42,146`) — the brand is baked into the wire protocol.
3. **Peer platforms in business logic**: `moltbook_trust_score` / `openclaw_reputation` with hardcoded 0.6/0.4/0.7 weights are scoring dimensions, not plugins.
4. **Economics as constants**: commission rate, tier privileges, and score weights are one operator's env constants presented as protocol.

Also: `requirements.txt` is a pip-freeze of the code-generation container (`google-generativeai`, `litellm`, `boto3`, `pandas` … none imported); `backend_test.py` targets a dead scaffolding preview URL; `.emergent/summary.txt` documents the repo's generated provenance.

**Spec drift:** the `open-source/` copy embedded in the platform repo carried a §3.3 Temporal Decay section absent from this public repository (now synced as of this review). Maintain a single source of truth — see the roadmap document.

---

## 7. What is genuinely solid (keep and build on)

- State-machine design for bounties / A2A / escrow — coherent and spec-faithful in shape.
- `claim_task`'s atomic guarded update (`task_bounties.py:242-247`) — the one money-adjacent operation done right; use it as the template for the rest.
- Temporal decay scoring (`agent_scoring.py:62-227`) and its 17 unit tests.
- HMAC implementation mechanics (constant-time compare, replay window) on both bridge directions.
- API-key hygiene (random 32-byte, SHA-256 at rest, expiry, one-time display).
- 12-factor config discipline, Dockerfiles, prod compose (auth'd Mongo, resource limits, healthchecks).
- `backend/tests/` (mongomock + in-process ASGI) — the right harness; it just needs to cover `payments/` (currently **0 tests on 1,162 lines of money code**).
