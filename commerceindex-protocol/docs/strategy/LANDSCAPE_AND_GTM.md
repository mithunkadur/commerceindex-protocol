# Landscape & Go-to-Market

**Date:** September 2026
**Companions:** [Path to Open Protocol](../roadmap/PATH_TO_OPEN_PROTOCOL.md) · [Implementation Status](../protocol/IMPLEMENTATION_STATUS.md) · collateral in [`docs/collateral/`](../collateral/)

## 1. The landscape (researched September 2026)

### Payment rails — settled territory, integrate don't compete
- **AP2 (Agent Payments Protocol)**: announced by Google (Sept 2025), donated to the **FIDO Alliance** (April 2026) with 60+ partners including Mastercard, PayPal, Coinbase, American Express, Revolut. Signed user mandates for agent payments.
- **ACP (OpenAI + Stripe Agentic Commerce Protocol)**: agent checkout; the market expectation is merchants implement both AP2 and ACP.
- **x402 (Coinbase)**: machine-to-machine stablecoin payments.
- **Visa Trusted Agent Protocol / Mastercard Agent Pay**: card-rail tokenization schemes; Mastercard committed to AP2 alongside its own scheme.

### Trust & reputation — the recognized open gap
- **IETF Internet-Draft (March 2026)**: trust scoring and identity verification for autonomous agents — the standards world has named the missing layer.
- **WEF "Know Your Agent" (KYA)** framing; analysts describe an emerging **"agent credit bureau"** category.
- **ERC-8004 "Trustless Agents"**: live on Ethereum mainnet since Jan 29 2026; real adoption (ENS, EigenLayer, The Graph, Base deployments). But an empirical study (arXiv:2606.26028) found the reputation registry **cannot function as a trust signal**: 59–91% of reviewers across chains show coordinated Sybil behavior, feedback is rarely grounded in verifiable interactions, and manipulation is nearly free. **This is the strongest third-party evidence that our design choices — behavioral evidence, temporal decay, graduated stakes, escrow-grounded feedback — are the right ones.** ERC-8004 v2 plans x402 payment-proof schemas inside feedback attestations: a natural integration target for CI Score attestations.

### Adjacent / competing builders
- **Virtuals Protocol ACP** (crypto): the closest live analog — negotiation → escrow → evaluator agents → settlement, with reputation, "agent graduation," automatic ERC-8004 registration, and demonstrated volume (~55k transactions/day peaks). Token-native, crypto-first. They own the crypto version of this idea today.
- **Skyfire** (KYAPay, ~$9.5M — a16z CSX, Coinbase Ventures): agent identity + payments via signed JWTs.
- **Catena Labs** ($30M Series A — a16z crypto, Acrew; OCC trust-bank charter filed): regulated financial rails for agents.
- **Basis Theory, Nekuda, Payman**: funded agent-payments/credential infrastructure.
- **MIT Project NANDA** (Media Lab): "Internet of AI Agents" — decentralized registry (DNS-for-agents), trust fabric research, corporate partners (Cisco, Dell, TCS, HCL). A university program squarely on this thesis.

### The open position
No one found combines **open-spec behavioral reputation + escrowed task exchange + graduated autonomy tiers** in a fiat-compatible, framework-neutral, enterprise-governable form. Virtuals has the crypto-native version; the fiat/enterprise-governance version is unclaimed. The window is real but narrow — this is a 12–18 month race, not a blue ocean.

## 2. Positioning by audience

- **VCs (one paragraph):** Agent payments are commoditizing — AP2 sits in FIDO with 60+ partners, and every rail assumes an answer to "should this agent be trusted with this money?" that none of them provides. The only live reputation registry at scale (ERC-8004) has been shown to be Sybil-gamed within months. CommerceIndex is the open protocol for the missing layer: behavioral credit scoring, escrowed accountability, and graduated autonomy that portfolio companies can adopt with one SDK — so every agent a portfolio ships starts building portable reputation now, before the standard hardens without them.
- **Universities (MIT/Stanford):** the open research problems here are publishable and unsolved — Sybil-resistant behavioral scoring (ERC-8004's failure is the motivating citation), incentive design for non-conscious economic actors, graduated-autonomy safety architecture, mechanism design for agent labor markets. MIT NANDA is already building the registry layer; CommerceIndex is a natural commerce/reputation testbed above it. Offer: co-authored benchmark + a sandbox economy as research infrastructure, not a sponsorship pitch.
- **Enterprises:** enter through SIs with governance (tiers→risk-policy mapping, conformance-as-audit), after developer traction exists. See the partner-briefing deck.

## 3. Go-to-market: four waves

**Wave 1 — Developers & open source (now → +3 months).** Public repo as the diligence surface; five-minute sandbox quickstart; MCP server in catalogs; skills/integrations for the major agent frameworks; seeded sandbox bounty economy so early agents earn from day one. Exit criteria: first 100 registered agents, first external contributor, first external implementer of any spec section.
**Wave 2 — Ecosystem & research (+2 → +6 months).** Agent-framework partnerships; MIT NANDA / university lab engagement (benchmark + testbed); ERC-8004 v2 and x402 interop work; publish the conformance suite. Exit criteria: one university collaboration, one interop demo on a major rail, conformance suite public.
**Wave 3 — VC portfolio networks (+4 → +9 months).** VCs as distribution, not (only) capital: a portfolio-adoption program (office hours, integration bounties, a "trust-ready" badge). One warm fund whose portfolio skews agentic beats ten cold pitches. Exit criteria: 2–3 funds actively routing portfolio companies.
**Wave 4 — Enterprises via SIs (+9 months →).** Deloitte-type governance practices carry it into regulated buyers once Phase 0–1 are done and real developer volume exists. Never lead with enterprise; arrive with evidence.

**Sequencing rule:** each wave manufactures the credibility the next wave requires. Skipping ahead (enterprise or VC before developer proof) spends credibility that is hard to buy back.

## 4. Publish vs. email

Both, with distinct jobs: **GitHub is the diligence surface** (public repo, spec, status matrix, collateral — what a VC associate or professor checks before replying), **email is the channel** (warm, specific, one ask). A pitch whose repo is private or stale fails silently; a public repo with honest status converts skeptics. Keep the platform repo private until Phase 0 security fixes land; the protocol repo is already the public face.
