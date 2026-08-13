# Project Lifecycle

## Purpose

Files under `docs/projects/**` are temporary records for bounded, non-trivial
changes. A project makes its outcome, decisions, implementation state, risks,
and acceptance evidence reviewable while work is active. It is not a permanent
roadmap, reusable procedure, or durable architecture owner.

The execution procedures for planning, implementation, documentation, inbox
triage, and specialized review live in their repository skills. This guide owns
only the lifecycle and required shape of a project record.

## Single Active Project

Only one project may be in progress. Complete and close it before creating
another unless the owner explicitly suspends or abandons the active project.

A question discovered during delivery may produce bounded research or a
durable decision referenced by the project. It does not authorize another
project or replace the next unresolved gate. After recording the supporting
material, return to the active project.

Each project represents one bounded outcome. A later substantial feature gets
a new project written from scratch even when it follows the same delivery
cadence or builds on the same foundation.

## Project Link Boundary

A project may link outward to durable requirements, domain, architecture,
research, and guideline documents. README, AGENTS, skills, durable
documentation, and other projects must not link to a specific project file.
This one-way dependency keeps completed project records removable.

## Interactive Decision Gates

Whenever work reaches a choice reserved for the owner:

1. present one coherent decision cluster rather than unrelated choices;
2. state the evidence, exact decision, viable alternatives, material tradeoffs,
   and recommendation when justified;
3. ask the smallest question that resolves the gate and wait for the answer;
4. record the accepted decision in the project and its durable owner before
   implementing dependent work;
5. continue to the next cluster only after the current one is resolved.

This applies to scope, requirements, architecture, data contracts, source
selection, risk acceptance, migration and cutover behavior, and other
owner-controlled choices. Ordinary reversible implementation details inside an
already authorized scope do not become additional approval gates.

## Pre-implementation Review

Before implementation begins, a non-trivial project must make the applicable
decision surfaces reviewable:

1. **Scope and assumptions** — intended outcome, in-scope behavior, boundaries,
   and unresolved product assumptions.
2. **Architecture** — component responsibilities, dependencies, state ownership,
   and data/runtime flow. Include a proportionate composition diagram when
   relationships between three or more components materially affect the design.
   Keep project diagrams small and decision-focused; use a table, tree, or fenced
   plain-text diagram according to the relationship being explained. Project plans
   favor these quick, directly readable views; durable architecture documentation
   uses the Mermaid convention defined by the engineering guide.
3. **UI** — for user-facing changes, low-fidelity mockups of primary screens,
   components, and relevant responsive breakpoints. Include PNG previews for
   material UI changes. Present mobile screens in portrait and desktop screens in
   landscape at representative viewport dimensions so each layout can be assessed
   in its intended form factor.
4. **UX** — navigation and interaction flows plus applicable content, empty,
   loading, offline, unavailable, validation, and failure states.
5. **Delivery** — implementation stages, migration and safety behavior,
   verification, and acceptance evidence.

Small copy, styling, or isolated maintenance changes may combine or omit
surfaces that are not materially affected. State why they do not apply instead
of producing decorative diagrams or irrelevant mockups.

The owner approves the plan as a whole by moving it to `APPROVED FOR
IMPLEMENTATION`; individual surfaces do not require separate fields or repeated
confirmation. Discussion, review, project edits, and documentation requests do
not change the phase.

An explicit request to plan and execute a named scope lets the project move
directly to `APPROVED FOR IMPLEMENTATION`. Ordinary reversible decisions within
it belong to the implementer. If planning or delivery exposes a new material
decision reserved for the owner, pause only the dependent work until that
decision is accepted; unrelated approved work may continue safely.

## Lifecycle States

### `PROPOSED`

The project defines the problem, outcome, scope, non-goals, decisions,
assumptions, open questions, affected flow, failure and migration behavior,
implementation stages, tests, manual checks, and acceptance criteria.
Dependent implementation has not started.

Keep non-goals short. Include only adjacent capabilities that a reader could
reasonably mistake as part of the outcome and whose exclusion affects the
design. Do not inventory unrelated future work.

### `APPROVED FOR IMPLEMENTATION`

The owner has approved the plan and explicitly authorized its named scope. Keep
progress markers, material deviations, new risks, and newly accepted decisions
current while implementing. Preserve user data and external evidence, and keep
destructive or network operations explicit.

### `IMPLEMENTED`

The requested behavior exists. Record actual verification results, manual
checks, known limitations, migration or operational impact, and follow-ups.
For owner-reviewed work, wait for implementation acceptance before durable
documentation cleanup.

### `APPROVED FOR DOCUMENTATION`

The owner has accepted the implementation result. Transfer lasting behavior,
decisions, rejected-alternative rationale, configuration, and safety boundaries
to their durable owners. Remove temporary delivery narration that has no
continuing value.

### `DONE`

Acceptance and durable documentation are complete. Delete the project file only
after confirming that:

- lasting behavior, decisions, limitations, and safety boundaries are recorded
  in their durable domain, architecture, requirements, research, or guideline
  owners;
- repository verification passes, or remaining failures are recorded accurately;
- no durable document links to the temporary project;
- temporary narration has been removed or replaced by durable facts.

## Project Template

```markdown
# <Change Name>

## Status

- Phase: PROPOSED | APPROVED FOR IMPLEMENTATION | IMPLEMENTED | APPROVED FOR DOCUMENTATION | DONE

## Problem And Outcome

## Scope And Non-goals

## Decisions, Assumptions, And Open Questions

## Architecture And Component Composition

## UI And UX Proposal

## Data Or Runtime Flow

## Failure Behavior, Safety, And Migration

## Implementation Plan

1. [pending] <step>

## Verification And Acceptance

- `<command>`
- <required manual check>

## Result

- <temporary implementation summary>
```

Use `[pending]`, `[in-progress]`, and `[done]` so interrupted work can resume
safely. Omit or briefly mark sections that are genuinely unaffected instead of
creating decorative content.
