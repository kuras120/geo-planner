# Requirements Guide

## Purpose

Product requirements capture concrete functional value that must be preserved or introduced. They explain what a user can accomplish, which real business/data integration enables it, and how the result is accepted end to end.

Requirements are not a substitute for engineering guidelines, architecture, research, or a project plan.

## Authorization And Timing

- Only the repository owner can approve a project for implementation or requirements discovery.
- Do not infer approval from a request to edit, review, expand, or discuss a plan.
- Do not create migration requirements before the approved discovery work has inspected the implemented behavior, external integrations, data, errors, and user workflows.
- For prototype migration, requirements are produced near the end of discovery, after the inventory, characterization evidence, and integration analysis are available.
- Requirements created without that evidence must be discarded rather than promoted as a speculative backlog.
- Creating or accepting a requirement does not authorize implementation. A selected coherent feature still receives its own temporary project plan.

## What Belongs In Requirements

A functional requirement belongs in `docs/requirements/<business-domain>.md` when it identifies:

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
6. Group retained behavior by business domain.
7. Write concrete functional stories only from accepted evidence.
8. Review the stories interactively with the owner; the agent must not change their status to accepted on its own.

## Requirement Template

```markdown
## <DOMAIN-ID> — <Concrete capability>

- Status: DRAFT | ACCEPTED | IMPLEMENTED | VERIFIED | DEFERRED | REJECTED
- Priority: MUST | SHOULD | COULD
- Source evidence: <legacy files, behavior, provider documentation, owner decision>

### User Story

As a <real actor>, I want <concrete action>, so that <business/analytical value>.

### Current Or Intended Flow

1. <user/system step>

### Integration

- System/dataset: <exact provider or none>
- Operation/layer/document: <exact operation>
- Inputs: <realistic inputs and example>
- Outputs: <observable output and example>

### Acceptance Criteria

- Given <specific state>, when <specific action>, then <observable result>.
- <empty/degraded/failure behavior>

### Open Questions

- <decision required from owner or research>
```

## Quality Gate

A requirement is not ready for owner acceptance when:

- it could apply unchanged to almost any backend;
- its value is primarily a framework/tooling concern;
- it does not name the migrated workflow or integration;
- inputs, outputs, and failure behavior are unknown;
- acceptance can be satisfied by scaffolding or a unit test without demonstrating user value;
- it was written before the discovery evidence existed.
