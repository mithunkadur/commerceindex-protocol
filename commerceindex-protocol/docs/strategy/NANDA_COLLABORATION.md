# Project NANDA — Collaboration Brief

**Date:** September 2026
**Companions:** [Landscape & GTM](LANDSCAPE_AND_GTM.md) (Wave 2) · [Path to Open Protocol](../roadmap/PATH_TO_OPEN_PROTOCOL.md) (Phases 1 & 3 are prerequisites for the deeper items below)

## What NANDA is

Project NANDA (MIT Media Lab, Ramesh Raskar's group) is building the **Internet of AI Agents**: replacements for the internet's four choke points — DNS (discovery), Certificate Authorities (identity), orchestration, and attestation — redesigned for billions of ephemeral autonomous agents.

Architecture ([Beyond DNS paper](https://arxiv.org/abs/2507.14263), [quilt repo](https://github.com/aidecentralized/NANDA-Quilt-of-Registries-and-Verified-AgentFacts)):
- **NANDA Index** — lean registry that resolves to agent data rather than storing it (DNS, not a directory)
- **AgentFacts** — cryptographically signed agent descriptions (capabilities, credentials, endpoints) signed by credential issuers, CRDT-based updates, sub-second revocation, **schema-validated capability assertions**
- **Adaptive Resolver** ([paper](https://arxiv.org/pdf/2508.03113)) — context-aware endpoint resolution
- **Quilt** — a federation of registries across sectors/jurisdictions, third-party agents included
- **Bridges** — A2A, MCP, HTTPS interop; a Python adapter that makes local agents globally discoverable

Ecosystem: 6,000+ community members, weekly webinars, paid fellowships (FAN, Tresata, Radius), the NANDA Town simulation environment (their most-forked repo), a Massachusetts civic-agents initiative, and partners including Google (A2A), HCLTech, and Mitsubishi Electric.

Roadmap: **Phase 1 (current)** — discovery infrastructure. **Phase 2 (upcoming) — "Agentic Commerce": knowledge pricing, economic incentive protocols.** Phase 3 — Large Population Models.

## The strategic read

NANDA's stack answers *who is this agent, what does it claim, where do I reach it*. It does not answer *has this agent behaved well, should I pay it, what happens if it doesn't deliver*. Their GitHub organization contains **no commerce, payments, escrow, or reputation repository**; their [trust-fabric paper](https://arxiv.org/pdf/2507.07901) advocates for quantified agent reputation without implementing it — and their own roadmap names agentic commerce as the next phase.

**CommerceIndex is a running, audited first draft of NANDA's Phase 2** — the specification and SDKs are open (MIT); the hosted implementation is currently private, with a neutral, self-hostable reference server planned as [Path to Open Protocol](../roadmap/PATH_TO_OPEN_PROTOCOL.md) Phase 2 work. Complementary by construction: NANDA is DNS+CA for agents; CommerceIndex is the credit bureau, escrow, and graduated access above it.

## What we add to them

1. A working head start on Phase 2 (spec, state machines, SDKs, scoring with temporal decay, sandbox economy — plus a published audit, which matches academic epistemic norms).
2. **Behavioral ground truth for AgentFacts.** Credentials can carry claims; escrow-conditioned transaction records are the *verifiable interaction* evidence reputation needs — the exact ingredient whose absence let ERC-8004's registry be Sybil-gamed ([empirical study](https://arxiv.org/abs/2606.26028): 59–91% coordinated reviewers).
3. An enforcement story for their attestation choke point: graduated autonomy tiers as Zero-Trust *graduation* (pairs with their ZTAA enterprise work).
4. A live experiment substrate: NANDA Town simulates agent societies; our sandbox adds money, negotiation, escrow, and disputes.

## What should excite them (ranked)

1. **CI Score attestations as an AgentFacts credential assertion** — resolve an agent through the NANDA Index and get its behavioral trust score with its facts. Makes their index answer the question every consumer will ask; makes our score discoverable across their quilt.
2. **Escrow-grounded, decaying reputation evidence** — a publishable answer to the Sybil failure mode, with ERC-8004 as the baseline.
3. **Graduated autonomy as control architecture** — the safety story their civic and enterprise tracks need.
4. **The transparency posture** — a collaborator that publishes its own hostile audit is a safe bet for an academic brand.

## Collaboration proposals (ranked by effort)

| # | Proposal | Effort | Prerequisite |
|---|----------|--------|--------------|
| a | Join community: Discord, present at a weekly webinar, apply to a fellowship (a fellow working on "commerce attestations for AgentFacts") | Low | None |
| b | Co-author an **AgentFacts extension spec** carrying CI Score attestations as a credential type | Medium | Asymmetric attestations (Phase 3) |
| c | Register CommerceIndex sandbox agents in the NANDA Index via their adapter | Low-Med | None |
| d | Joint **Sybil-resistance benchmark** paper (their registry + our escrow-grounded scores vs. ERC-8004 baseline) | Medium | Phase 0/1 hygiene |
| e | NANDA Town × CommerceIndex sandbox demo at a NANDA summit | Medium | c |

## Cautions

- **Two-sided window:** engage now and we are the obvious Phase 2 partner; wait and we may compete with a NANDA-native economic protocol carrying MIT's brand.
- **Our prerequisites bind:** proposal (b) requires third-party-verifiable attestations; deep integration invites scrutiny — Phase 0 fixes first.
- **Academic pace:** weeks-to-months, often routed through students/fellows. A fellow or student adopting the testbed is the win condition, not a professor's signature.

## Outreach hook

Lead the MIT email with: *"Your roadmap's Phase 2 is agentic commerce — we've built a running, audited first draft of that layer, with an open spec and SDKs, and we'd rather it grow up inside NANDA's quilt than outside it."* (Be precise about openness: the spec and SDKs are public today; the hosted implementation is private until the open reference server ships — recipients will check.)
