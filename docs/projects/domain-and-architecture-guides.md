# Domain And Architecture Guides

## Status

- Phase: IMPLEMENTED

## Problem And Outcome

Domain and architecture documents have repository routing but no concise rules
for what each category owns. Add two agent-facing guides and align the current
documents so product meaning stays in domain while runtime structure and flow
stay in architecture.

## Scope And Non-goals

In scope:

- add one domain guide and one architecture guide;
- route domain and architecture work to them from `AGENTS.md`;
- align the six existing domain and architecture documents without changing
  accepted behavior;
- keep README links focused on project documentation, not agent procedures.

Non-goals:

- creating a guide for every documentation category;
- inventing bounded contexts, modules, APIs, or runtime decisions;
- rewriting research, requirements, or application code;
- changing legacy behavior or refreshing external evidence.

## Decisions, Assumptions, And Open Questions

- A guide is justified only when it defines a durable category boundary and
  review standard used across multiple documents.
- Domain owns terminology, meaning, invariants, and domain state; architecture
  owns component responsibilities, runtime/data flow, persistence, failure,
  deployment, and implementation state.
- Guides are agent-facing and are routed centrally by `AGENTS.md`, not README
  or repeated skill-specific guide lists.
- Skills name only their direct procedural guide dependencies. `AGENTS.md`
  decides which repository and category context applies to the touched area.
- Skills consume routed context without referring back to `AGENTS.md`; the root
  policy remains the sole owner of routing and its loading mechanism.
- Existing documents should be compacted or moved only where ownership is
  clearly wrong. No open owner decision remains.

## Architecture And Component Composition

Not applicable: documentation ownership changes only.

## UI And UX Proposal

Not applicable: no user-facing behavior changes.

## Data Or Runtime Flow

No runtime flow changes. Documentation routing changes from the generic
engineering guide to the new category-specific guides.

## Failure Behavior, Safety, And Migration

Preserve all accepted facts, legacy safety boundaries, source uncertainty, and
current-versus-target distinctions. Do not move evidence into guidelines or
turn proposals into current behavior.

## Implementation Plan

1. [done] Define concise domain and architecture category guides.
2. [done] Route agent documentation work to the new guides.
3. [done] Align current domain and architecture documents.
4. [done] Audit ownership, links, formatting, and repository verification.

## Verification And Acceptance

- review every file under `docs/domain/**` and `docs/architecture/**` against
  its category guide;
- verify README links no guide except the repository guide;
- validate relative Markdown links and project inbound-link boundaries;
- `git diff --check`;
- `mise run verify`.

## Result

- Added concise domain and architecture guides with ownership tables, document
  shape, evolution rules, and review checklists.
- Routed category work centrally through `AGENTS.md` while keeping the guides
  out of README and removing duplicated category routing from general skills.
- Removed explicit `AGENTS.md` references from every skill so procedures consume
  routed context without duplicating how it is supplied.
- Standardized all current domain and architecture documents on a clear
  `Status And Scope` section.
- Kept legacy identity, spatial meaning, evidence classes, geometry semantics,
  and safety in domain; moved build, parser, generated-output, persistence, and
  reload mechanics to the current legacy architecture flow.
- Retained the other domain and architecture documents because they already
  satisfy the new ownership and current-versus-target rules.
- Relative links, category routing, README guide boundaries, project inbound
  links, and `git diff --check` passed. `mise run verify` passed; existing
  non-blocking Storybook/Compodoc warnings remain unchanged.
