# PEP-001: Escrow Sentinel — release/hold risk review on automatic escrow releases

**Status:** Implemented (sandbox, flags off by default) · **Date:** October 2026 · **Reference implementation:** [`commerceindex-ai#7`](https://github.com/mithunkadur/commerceindex-ai/pull/7) (merged), hardened by the Phase 0 money-path fixes in [`commerceindex-ai#8`](https://github.com/mithunkadur/commerceindex-ai/pull/8) (merged)

## Motivation

Coinbase's "Owning Intelligence" series ([Part 1](https://www.coinbase.com/blog/part-one-how-coinbase-built-evaluated-and-post-trained-a-fraud-agent)) showed a production pattern for money-at-stake decisions: cheap rules first, then a prompted frontier-model reviewer emitting only a risk level (A/B: 30% fewer fraudulent transactions at ~3× ROI), a domain benchmark scored against verified outcomes, and only then a post-trained small model (Qwen3.5-9B beating Opus 4.5 on their fraud benchmark for <$100 of training). The durable asset is the labeled outcome stream and the eval loop, not the model.

CommerceIndex has the same decision shape at its escrow release points — fast call, money at stake, ground truth arrives later as dispute outcomes — and, uniquely, it **owns the label source**: every release decision is labeled free when the dispute window closes clean or a dispute resolves.

## The decision

**One label, one number to beat:** *release or hold* one pending automatic escrow release.

Protected release points (where no counterparty judgment exists today):
1. **Task auto-approve** — work previously paid out on the submitter's own `quality_confidence`.
2. **Escrow timeout auto-release** — funds previously paid out unconditionally after 72h.

(Agent-confirmed releases — A2A buyer confirmation, merchant review — already embed a counterparty decision and are out of scope for v1.)

## Specification

**Inputs (feature snapshot, logged with every decision):** reference id, release kind, amount, delivery summary (truncated), self-graded flag, payee {score, tasks completed, disputes 30d, abandonments, lifetime earnings}, payer {score, disputes 30d}, prior released transactions between the pair.

**Decision pipeline:** deterministic rules (free, always first) → optional LLM reviewer for amounts ≥ threshold, emitting **only** `RISK_LEVEL: N` (1–5) → final level = max(rules, LLM) → `hold` iff level ≥ hold threshold (default 4). A hold never moves money: it routes the release to review (auto-approve → `under_review`; timeout → one 24h deferral, then release). Disabled or erroring, the Sentinel **fails open** to current behavior.

**Labels:** dispute outcomes (`refund_buyer` / `split` = release was wrong; `release_to_seller` = hold was wrong) and `released_clean` after the label window passes without dispute.

**Dataset & benchmark (AgentEscrowBench):** the decision log + labels exported as a replayable benchmark — the platform's equivalent of Coinbase's 16,140-transaction replay set. Published openly once volume exists; frontier baselines re-run on every major model release.

**Baselines to beat:** (a) release-everything (current behavior), (b) rules-only — measured on precision, recall, and dollar-weighted recall of bad releases.

**Success numbers:** dollar-weighted recall of bad releases at ≤5% false-hold rate; reviewer inference cost ≤ ⅓ of fraud dollars prevented (Coinbase's ROI bar).

## Rollout order (Coinbase's order, deliberately)

1. Rules live in sandbox (ships with the reference implementation, flags off by default).
2. Prompted frontier reviewer behind `SENTINEL_LLM_ENABLED`, sandbox pilots generating labeled volume.
3. Publish AgentEscrowBench + frontier baselines.
4. Fine-tune a small open model on the labels; publish the numbers.
5. Sell the loop (decision point + label stream + benchmark + retraining), not the weights.

## Constraints

- Sandbox-only until an external security audit passes — a risk model on unsafe rails is a smarter lock on a broken door. *(The Phase 0 money-path fixes — double-settlement, dispute-split — landed October 2026 in `commerceindex-ai#8`; the audit remains outstanding.)*
- The Sentinel holds; humans (or merchant review) release. Graduated autonomy applies to the Sentinel itself: its authority can grow only as its benchmark record does.
- No real-funds holds before money-transmission counsel.
