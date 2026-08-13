# Target Architecture Document Split

## Status

- Phase: IMPLEMENTED
- Authorization: the owner explicitly requested the split on 2026-08-13.

## Problem And Outcome

`target-product-architecture.md` mixes system composition, product concepts,
acquisition flow, user interaction, proposed endpoints, persistence, and
migration. Split it into durable owners without changing accepted behavior.

## Scope And Non-goals

In scope:

- retain system composition and technology/deployment decisions in the target
  architecture overview;
- move domain concepts and invariants into a named domain document;
- move provider acquisition, validation, and artifact flow into a focused
  architecture document;
- replace duplicated behavioral detail with links to accepted requirements;
- remove the speculative endpoint table because contracts are accepted per
  vertical slice.

Out of scope:

- changing requirements, runtime behavior, module structure, API contracts, or
  deployment choices;
- declaring separate bounded contexts before implementation evidence supports
  them;
- modifying `AGENTS.md` policy.

## Decisions, Assumptions, And Open Questions

- `target-product-architecture.md` remains the stable architecture entry point.
- `spatial-evidence.md` names the problem domain and owns its target terminology
  and invariants without claiming multiple bounded contexts or modules.
- `acquisition-and-artifact-flow.md` owns integration orchestration and its
  storage handoff.
- Requirements remain authoritative for exact user-visible behavior and
  accepted numeric limits.
- No owner decision remains open for this documentation-only split.

## Data Or Runtime Flow

No runtime or persisted data changes. Documentation references change from one
large owner to three focused durable owners.

## Implementation Plan

1. [done] Create the Spatial Evidence domain and acquisition architecture owners.
2. [done] Compact the target architecture overview and remove duplication.
3. [done] Repair durable links and verify ownership boundaries.
4. [done] Run documentation checks and `mise run verify`.

## Verification And Acceptance

- `git diff --check`
- relative Markdown link validation
- search for stale ownership statements and speculative endpoints
- `mise run verify`
- Acceptance: each document has one clear responsibility, accepted facts remain
  discoverable, and no runtime or product contract changes.

## Result

- Reduced the architecture entry point from 439 to 208 lines and retained only
  system composition, technology, contract, deployment, security, and migration
  boundaries.
- Added a focused Spatial Evidence domain owner and a 115-line acquisition
  architecture owner, with Mermaid diagrams for component and runtime
  relationships.
- Removed the speculative endpoint table; API shapes remain governed by
  accepted vertical slices and OpenAPI.
- Kept exact AOI and acquisition limits in requirements instead of duplicating
  them across durable owners.
- Updated README, legacy-domain, and research links to the new owners.
- Relative-link validation, ownership searches, `git diff --check`, and
  `mise run verify` passed. Existing non-blocking Storybook/Compodoc warnings
  remain unchanged.
