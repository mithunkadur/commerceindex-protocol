# Path to a Real Open Protocol

**Date:** August 2026
**Companion to:** [Implementation Review 2026-08](../reviews/IMPLEMENTATION_REVIEW_2026-08.md)

This document answers two strategic questions and lays out the sequence to get from "a platform with a published spec" to "a protocol other people implement."

---

## 1. Would developers adopt this if the CommerceIndex references were removed?

**No — because the brand was never the barrier.** The portability review shows rebranding is mechanical: the domain references are mostly docstring headers, config is fully env-driven, SDK base URLs are overridable, and everything is MIT. A weekend of renaming makes it neutral.

What actually determines protocol adoption, in order:

1. **Trust.** The first thing a serious adopter does is audit the reference implementation. Today that audit finds an unauthenticated account-takeover endpoint, double-settlement races, and a dispute path that pays 150%. No amount of neutral naming survives that first look.
2. **Interoperability.** A protocol exists when two independent implementations talk to each other. Today a spec-conformant client cannot even verify a signature against the reference server (canonicalization mismatch), and `GET /v1/feed` 404s.
3. **Completeness.** The commerce in the commerce protocol — settlement — is a closed, undocumented private API. A protocol whose money layer is proprietary is a platform with documentation.
4. **Network effects.** Developers adopt protocols for who else is on them. That is earned through a beachhead niche, lighthouse users, and a second implementation — not through naming.

Also calibrate the goal: **"every developer" is not a realistic bar for any protocol** — HTTP-level ubiquity is an outcome of decades, not a launch target. The right target is: the default choice for one concrete job (portable agent reputation + escrowed task exchange), adopted by a handful of visible projects, growing from there.

## 2. Is stripping the protocol from the platform important?

**Yes — and it is now an engineering necessity, not an aesthetic preference:**

- **Drift is already happening.** The spec copy embedded in the platform repo gained a Temporal Decay section (§3.3) that the public spec repo lacked for months. Two sources of truth diverged almost immediately.
- **The platform is the de-facto spec today, and it's wrong.** Where the server and spec disagree (signing, headers, paths, endpoints), an implementer cannot know which to follow.
- **~65% of the backend is one company's business** — social feed, human-labor marketplace, referrals, campaigns, billing, dashboards. ~110 of ~150 routes are unspecced. Shipping that as "the implementation" makes the protocol unauditable.
- **The settlement boundary — the most important interface in the protocol — is private.** Until it is a documented, pluggable interface, no one else can run the economy.
- **Reputation portability is architecturally captive**: attestations are symmetric-HMAC tokens verifiable only by calling the issuer, with the brand hardcoded in the `iss` claim. Portable reputation requires asymmetric signing and issuer-agnostic verification.

Separation means: a normative spec repo (single source of truth, machine-readable), a public conformance suite, and a minimal neutral reference implementation with settlement as an adapter interface — with the hosted platform positioned as the first and best deployment, not the definition.

---

## 3. The sequence

### Phase 0 — Stop the bleeding (blocker for everything)

Nothing below matters while the reference implementation can lose money or leak accounts. In the platform repo:

- [ ] Remove/authenticate `POST /v1/auth/openclaw-link` key issuance (account takeover).
- [ ] Status-guarded `find_one_and_update` + idempotency keys on every money transition (escrow release/refund, settlement, approval, confirm). Use `claim_task`'s atomic pattern as the template.
- [ ] Fix the 150% dispute split; fix the A2A escrow-key / payout-id bugs; check return values of `release_escrow`/`refund_escrow`/`fund_escrow`.
- [ ] Single-instance schedulers (or a distributed lock) — jobs currently run once per worker.
- [ ] `tz_aware=True` on the Motor client.
- [ ] Fix the invalid CI workflow so lint + tests actually run; add tests for `payments/` (currently zero on 1,162 lines).

### Phase 1 — One source of truth + conformance

- [ ] This repo's spec becomes the **only** copy; delete the embedded `open-source/` duplicate from the platform repo (replace with a submodule or a link). (Temporal Decay §3.3 is now synced here.)
- [ ] Publish machine-readable artifacts: OpenAPI (FastAPI generates it — export and commit it here) + JSON Schemas for every message.
- [ ] Reconcile spec ↔ implementation, choosing one side per divergence: HMAC `sort_keys` canonicalization, header names (`X-CI-*` vs `X-CI-AI-*`), bridge/ingest paths, `GET /v1/feed`, experiment constraint enforcement (`sandbox_mode`, `max_usdc_per_run`, `time_window_minutes`).
- [ ] Ship `commerceindex-conformance`: a pytest/HTTP suite any implementation can run against any base URL. The hosted platform passes it publicly (badge in both READMEs).
- [ ] Either wire up the nine unwritten scoring inputs or remove them from the spec — **the tier ladder must be climbable**; elite (and therefore bounty creation) is currently unreachable.

### Phase 2 — Extract the reference implementation

- [ ] Carve the ~6k-LOC protocol engine (registry, scoring, tasks, A2A, escrow ledger, gateway) into a neutral, self-hostable server. Success bar: `docker compose up` → a working local agent economy with **sandbox money** in five minutes. That demo is the single highest-leverage adoption asset.
- [ ] Define **settlement as a protocol interface** with adapters: `mock/sandbox` (ships first), `stripe`, and a stablecoin rail (e.g. x402 / USDC on an L2) later. The private `.com` bridge becomes just one adapter behind the documented interface.
- [ ] Clean dependency manifest (the current `requirements.txt` is a scaffold-container freeze), real MCP server (the current one is REST, not MCP), and multi-worker-safe gateway (Redis pub/sub) — or documented single-worker mode.

### Phase 3 — Portable trust for real

- [ ] Cryptographic agent identity: agents hold keypairs and sign their actions; API keys become a transport detail. This is what makes reputation portable and sybils expensive — and it fixes the whitepaper's own critique ("scam today, new API key tomorrow").
- [ ] Attestations: Ed25519-signed JWTs, JWKS at `/.well-known/`, **configurable issuer** (remove the hardcoded brand from `iss`), separate keys from the bridge HMAC secret (one secret currently spans four trust domains).
- [ ] Evidence-based reputation: signed transaction receipts as the portable primitive; the CI Score becomes one open, reproducible scoring function over receipts that anyone can verify or compete with. This converts "trust our number" into "check our math."

### Phase 4 — Distribution: go where agents already are

- [ ] A real MCP server, published where agent developers look for tools.
- [ ] **Integrate, don't fight, the incumbent rails**: position against Google AP2, OpenAI/Stripe ACP, Coinbase x402, and ERC-8004 explicitly in the whitepaper. The defensible layer here is reputation + escrow + graduated autonomy — payments rails are being commoditized by much larger players. Concrete integration: a CI Score attestation consumable inside an AP2/ACP checkout flow; x402 as a settlement adapter.
- [ ] Publish the agent skill to the registries agents actually use; keep SDK quickstarts at "reputation in 10 lines."

### Phase 5 — Adoption mechanics

- [ ] Neutral governance: spec under a neutral namespace/org, a working proposal process (the `docs/proposals/` PEP directory is currently empty), and 2–3 named external design partners reviewing spec changes.
- [ ] A lighthouse use case with real volume — sandbox-first, one concrete vertical (e.g. data-enrichment bounties between agent frameworks) rather than "all agent commerce."
- [ ] The credibility milestone that makes it a *protocol*: **a second, independent implementation** passing the conformance suite.
- [ ] Real money only after an external security audit of the settlement path — and market "escrow-backed settlement" only once it is true.

---

## 4. Sequencing rationale

Each phase is the trust prerequisite for the next: a correct implementation (0) makes a single-source spec meaningful (1); a conformance suite makes extraction verifiable (2); a neutral engine makes portable trust credible (3); portable trust is the differentiated thing worth distributing (4); and distribution is what earns the second implementation that makes this a protocol instead of a product (5). Skipping ahead — e.g. marketing the protocol before Phase 0 — spends credibility that is very hard to buy back.
