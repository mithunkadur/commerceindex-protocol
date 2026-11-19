# Collateral

| File | Audience | Use |
|------|----------|-----|
| `CommerceIndex_Partner_Briefing.pptx` | Platform partners, SIs, enterprises, VCs (13 slides, speaker notes included) | Meetings; tailor per the notes on slides 10-12 |
| `CommerceIndex_OnePager.pdf` | Leave-behind for any audience; email attachment | Summarizes protocol, honest status, developer playbook, partnership architecture |

Both documents state implementation status honestly (sandbox-only money, audit-before-production commitment). Keep them consistent with [Implementation Status](../protocol/IMPLEMENTATION_STATUS.md) when updating. Positioning and sequencing live in [Landscape & GTM](../strategy/LANDSCAPE_AND_GTM.md).

## Known inaccuracies — fix before sending (November 2026)

**`CommerceIndex_OnePager.pdf` is out of date and should not be sent as is.** Three statements in it are not true today:

- "`pip install commerceindex · npm i @commerceindex/sdk`" — neither package is published. Install is from this repository (see the SDK READMEs).
- "Open spec + conformance suite: anyone can implement and verify" — the conformance suite does not exist yet; it is roadmap work.
- "published audit" — what is published is our own review of the implementation, not an external audit.

The PDF has to be regenerated to fix these; publishing the SDKs would make the first one true.

The deck's wording was corrected in November 2026 ("commissioned … audit" became "our own review"; the governance seat is offered "as it forms"). It is still dated September 2026 and its status slide predates the November review — check slide 7 against the status matrix before presenting.
