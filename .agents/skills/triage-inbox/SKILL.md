---
name: triage-inbox
description: Interactively turn loose Geo Planner notes from INBOX.md or pasted material into requirements, backlog items, research questions, decisions, risks, or discarded duplicates. Use when the owner provides unstructured ideas, observations, links, map-layer requests, property notes, or uncertain facts that must be classified without prematurely implementing them.
---

# Protocol D: Inbox Triage

1. Read `INBOX.md`, relevant durable docs, and active `docs/projects/` files. Do not treat an inbox statement as verified fact or implementation approval.
2. Process one coherent cluster at a time. Restate it briefly and ask only the decision needed to classify it when intent is ambiguous.
3. Assign each item to exactly one primary destination:
   - requirement: user-visible need with acceptance evidence;
   - backlog: actionable work not yet selected;
   - research: question requiring evidence or comparison;
   - decision: accepted constraint or choice with rationale;
   - risk: uncertainty with impact and mitigation;
   - archive: duplicate, obsolete, or intentionally rejected note.
4. Preserve provenance: original wording, date, links/files, confidence, and owner decision.
5. Move clarified content into the relevant domain doc, research note, or `docs/projects/` proposal. Use a short stable ID for requirements and backlog items.
6. Remove an inbox entry only after its destination is written and linked. Keep unresolved items in `INBOX.md` with the next question.
7. End each session with counts by category, unresolved questions, and the next smallest useful triage batch. Never implement backlog items without separate authorization.
