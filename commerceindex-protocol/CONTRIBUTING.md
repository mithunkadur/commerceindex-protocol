# Contributing to CommerceIndex Protocol

Thank you for your interest in improving the CommerceIndex Protocol.

## What This Repo Contains

This repository contains the **open protocol specification** for AI agent commerce. It defines the standards that any platform can implement to enable agents to register, build reputation, transact, and settle.

This is **not** the platform implementation — that lives in a separate private repository.

## Types of Contributions

### 1. Clarifications & Fixes
If you find an error, ambiguity, or missing detail in the specification, open a PR with the fix.

### 2. Feature Proposals
For new protocol features or changes to existing behavior:

1. Open an issue describing:
   - The problem or gap in the current protocol
   - Your proposed solution
   - Impact on existing implementations
   - Backwards compatibility considerations
2. Discuss with the community
3. Once consensus is reached, submit a PR with the spec changes

### 3. Protocol Enhancement Proposals (PEPs)
For significant additions (new protocol components, major scoring changes, new transaction types):

1. Create a new document in `docs/proposals/` following the template:
   - Title, author, status (draft/review/accepted/rejected)
   - Abstract, motivation, specification, backwards compatibility, security considerations
2. Submit as a PR for community review
3. PEPs require maintainer approval before merging

## Guidelines

- Keep specifications precise and unambiguous
- Include JSON schemas for all data structures
- Include state machine diagrams (Mermaid) for all lifecycle flows
- Document error codes and edge cases
- Consider backwards compatibility — breaking changes require a major version bump
- Security implications must be explicitly addressed

## Code of Conduct

Be respectful, constructive, and collaborative. We're building infrastructure for the agent economy — that requires trust between humans too.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
