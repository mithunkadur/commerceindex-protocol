# Sentinel Validation & Distribution Plan

**Date:** October 2026 · **Companions:** [PEP-001](../proposals/PEP-001-escrow-sentinel.md) · [Landscape & GTM](LANDSCAPE_AND_GTM.md)

## 1. The 10-people validation (Mom-Test rules)

**Goal:** find 10 named people with a *past* incident — an AI agent spent money or did a job for them and it went wrong — before investing further. Ask about behavior, never pitch.

**The script (3 questions, no pitch):**
1. "Tell me about the last time an agent or automation spent money or did a task for you. What happened?"
2. "Has one ever gone wrong — wrong purchase, bad delivery, double payment, junk output you'd paid for? What did it cost, and what did you do about it?"
3. "What do you do today before letting an agent act with real money or real stakes?"

**Scoring:** a *hit* = specific past incident + real cost (money or hours) + they took action afterward. 10 hits → build with those 10 as pilot partners. 3–9 hits → niche exists, narrow to where the hits cluster. <3 hits → the pain is future-tense; stay in benchmark/instrument mode and re-run quarterly.

**Where to hunt:** builders shipping on agent frameworks (Discords/forums of the major agent stacks), teams running browser/procurement agents in production, ops leads at companies piloting agentic checkout, Coinbase-thread repliers describing incidents, NANDA community, r/AI_Agents war-story threads. Log every interview (who, incident, cost, workaround) — that log *is* the seed of the incident dataset and the fundraising evidence.

## 2. The poll (reply to Brian Armstrong's thread)

Reply text (≤280 chars):
> "Fraud labels arrive late" is the whole game. We're building the escrow layer for agent-to-agent commerce — the release/hold call is the same shape as your fraud agent, but nobody has the labels yet. Question for everyone shipping agents: 👇

Poll question: **"Has an AI agent ever cost you real money or hours (bad purchase, junk delivery, double payment)?"**
- `Yes — real money lost`
- `Yes — hours, not money`
- `Close call / caught it`
- `Never happened yet`

**Why this wording:** it's retrospective (Mom-Test-compatible — counts incidents, not worries), every option is informative (even "never yet" sizes the timing risk honestly), and "close call" captures the leading indicator. Follow-up post ready for repliers: "If you picked 1 or 2, I'm collecting these — DM me the story. First 10 get early access to the escrow sandbox." **The poll's real product is the DM list, not the vote count.**

## 3. Taking it to developers

- **The hook is the benchmark, not the platform.** "Can your model tell a bad agent payout from a good one?" travels; "join our marketplace" doesn't. Publish AgentEscrowBench with frontier baselines as soon as labeled volume exists; post the Show HN / technical write-up on the benchmark.
- **Five-minute path stays the spine:** SDK install → one registration call → sandbox bounty → watch the score move; the Sentinel adds the demo moment — *watch a risky payout get held in real time*.
- **Seed the label mine:** sandbox bounties that pay (simulated) for red-teaming the Sentinel — "get a bad payout past the reviewer" — generating hard adversarial examples while onboarding developers. Red-teamers show up for sport; their attacks are the dataset.
- **Ship where agent devs already are:** MCP catalogs, agent-framework integrations, the incident-story thread on the repo (a pinned "agent-gone-wrong" issue template feeding the interview log).

## 4. Taking it to platforms

- **Rails (AP2/ACP/x402 ecosystems):** position the Sentinel verdict + CI Score attestation as the risk signal their checkout consumes — "we answer the question your mandate format assumes someone answers." Integration demo > pitch deck.
- **Agent frameworks & marketplaces:** offer the release/hold decision as an API they call before paying out — the Visa-fraud-score model: embedded, white-label, their UX.
- **NANDA (Wave 2):** AgentEscrowBench is exactly the escrow-grounded evidence their trust fabric lacks; fold into the existing collaboration plan.
- **Consultancies/enterprises:** unchanged from Landscape & GTM Wave 4 — arrive with benchmark + pilot evidence, through SIs, never first.

## 5. Sequencing (now → 90 days)

| When | Milestone |
|------|-----------|
| Now | Merge Sentinel (flags off), PEP-001 public; post the poll; start interviews |
| +2 wks | 10 interviews logged; sandbox pilots with every "hit"; red-team bounty live |
| +6 wks | First labeled hundreds of decisions; frontier baseline run; publish v0 benchmark note |
| +90 days | AgentEscrowBench public with baselines; Show HN; go/no-go on fine-tuning from label volume; re-run validation scorecard |

**Honesty rail (unchanged):** sandbox money only until Phase 0 fixes + external audit; every public claim checkable against the repo.
