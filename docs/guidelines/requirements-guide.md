# Requirements Guide

## Purpose

Product requirements capture concrete functional value that must be preserved or introduced. They explain what a user can accomplish, which real business/data integration enables it, and how the result is accepted end to end.

Requirements are not a substitute for engineering guidelines, architecture, research, or a project plan.

## Organization And Indexing

`docs/requirements/index.md` is the portfolio index. Requirements are grouped
by application area: a cohesive product module or user-facing responsibility,
not a business-domain model and not one file per requirement. Each area has one
`docs/requirements/<application-area>.md` file with:

- a short area purpose and boundary;
- an area index listing every requirement ID, delivery stage, status,
  priority, and title;
- the full requirement records below the index.

The portfolio index links the application-area files and aggregates:

- total requirements and `VERIFIED` requirements per application area;
- totals by delivery stage;
- totals by status;
- one grand total across all areas.

Update the area index in the same change as any requirement addition,
removal, status change, stage change, split, or merge, then run:

```bash
./scripts/update_requirements_index.py
```

The script validates required metadata and unique IDs, then atomically
regenerates the portfolio tables. `./scripts/verify.sh` runs its read-only
`--check` mode and rejects stale statistics. Stable requirement IDs are never
reused.

Only `VERIFIED` counts as completed. `IMPLEMENTED` means the behavior exists but
has not yet passed end-to-end acceptance. `REJECTED` and `DEFERRED` remain
visible in status statistics but do not count as completed.

## Delivery Stages

Every requirement has one owner-approved delivery stage:

| Stage | Migration intent |
| --- | --- |
| `MVP` | Read, display, identify, and safely interpret the basic source layers already available in the prototype, including provenance and degraded availability. |
| `STAGE-2` | Create, import, edit, persist, select, and export manual sketches after layer reading is stable. |
| `STAGE-3` | Calculate spatial intersections, measurements, comparisons, and other derived analysis using accepted source and sketch contracts. |
| `LATER` | A valuable capability intentionally outside the first three stages. |

Stages describe product delivery order, not requirement status or technical
implementation sequence. A requirement moves between stages only through an
owner decision. Dependencies that are necessary to deliver an earlier stage
must be visible in that requirement rather than hidden in a later-stage story.

## Authorization And Timing

- Only the repository owner can approve a project for implementation or requirements discovery.
- Do not infer approval from a request to edit, review, expand, or discuss a plan.
- Do not create migration requirements before the approved discovery work has inspected the implemented behavior, external integrations, data, errors, and user workflows.
- For prototype migration, requirements are produced near the end of discovery, after the inventory, characterization evidence, and integration analysis are available.
- Requirements created without that evidence must be discarded rather than promoted as a speculative backlog.
- Creating or accepting a requirement does not authorize implementation. A selected coherent feature still receives its own temporary project plan.

## What Belongs In Requirements

A functional requirement belongs in its application-area file when it identifies:

- a real actor and concrete goal;
- observable business or analytical value;
- the existing prototype behavior to preserve or an explicitly requested new behavior;
- a named external system, dataset, document, or user workflow when integration is involved;
- realistic inputs and outputs, including representative examples;
- success, empty, degraded, and failure behavior visible to the user;
- acceptance criteria that can be demonstrated end to end;
- provenance showing where the requirement came from.

Examples of appropriate requirement subjects:

- resolve a Polish parcel through a specific ULDK operation and return geometry usable for a project;
- acquire the ORTO `Raster` layer for the selected AOI and display its source date and attribution;
- preserve optional KINA failure as a visible warning while retaining other usable layers;
- import a concrete legacy overlay file without duplicating features.

## What Does Not Belong

Keep these elsewhere:

- Gradle reproducibility, linting, Kotest conventions, module layout, and Kotlin style → engineering guidelines;
- SSRF policy, persistence strategy, API layering, and runtime topology → architecture/security guidelines;
- whether PostgreSQL, RabbitMQ, or WebFlux is justified → technology research and architecture decisions;
- implementation steps, sequencing, ownership, and temporary risks → a project plan;
- unverified ideas or raw notes → `INBOX.md`;
- source evaluation and licence uncertainty → research.

Non-functional behavior may appear as an acceptance constraint of a functional story when it is necessary to deliver its value, but it must not be disguised as a standalone product story such as “As a developer, I want a reproducible build.”

## Discovery Workflow

1. Inspect the actual legacy workflow and record what the user does, sees, saves, and exports.
2. Trace the code and configuration that implement it.
3. Identify every external source and exact operation, layer, document, request input, and response form.
4. Capture success, no-data, optional failure, hard failure, stale data, and privacy behavior.
5. Decide with the owner which behavior is intentional, accidental, obsolete, or missing.
6. Group retained behavior by cohesive application area.
7. Write concrete functional stories only from accepted evidence.
8. Review stories one application area at a time, following the interactive
   decision gates in `project-lifecycle.md`. Present a compact area index, then
   each requirement's outcome, contract, acceptance, and unresolved decisions.
   Never infer acceptance, deferral, rejection, split/merge, priority, or
   delivery-stage decisions.

## Requirement Template

```markdown
## <AREA-ID> — <Short verb-object capability>

- Status: DRAFT | ACCEPTED | IMPLEMENTED | VERIFIED | DEFERRED | REJECTED
- Priority: MUST | SHOULD | COULD
- Delivery stage: MVP | STAGE-2 | STAGE-3 | LATER
- Source evidence: <legacy files, behavior, provider documentation, owner decision>

### Outcome

<Actor, concrete result, and value in one short paragraph.>

### Contract

- Input: <realistic input>
- Sources: <exact system, dataset, operation, layer, or none>
- Output: <observable result>
- Degraded/failure behavior: <what the user sees and what is preserved>

### Acceptance Criteria

- Given <specific state>, when <specific action>, then <observable result>.
- <empty/degraded/failure behavior>

### Open Decisions

- <decision required from owner or research>
```

Keep each record short and unambiguous. Use a verb-object title, state each fact
once, prefer compact bullets over narrative flow, and link to research instead
of copying its full evidence. A requirement is still incomplete if brevity
removes its user value, concrete contract, degraded/failure behavior, acceptance
criteria, or provenance.

## Quality Gate

A requirement is not ready for owner acceptance when:

- it could apply unchanged to almost any backend;
- its value is primarily a framework/tooling concern;
- it does not name the migrated workflow or integration;
- inputs, outputs, and failure behavior are unknown;
- acceptance can be satisfied by scaffolding or a unit test without demonstrating user value;
- it was written before the discovery evidence existed.
