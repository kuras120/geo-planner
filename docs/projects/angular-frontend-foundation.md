# Angular Frontend Foundation

## Status

- Phase: PROPOSED
- Created: 2026-07-23
- Updated: 2026-07-24
- Implementation owner: Codex.
- Reviewer and acceptance owner: repository owner.
- Authorization: planning only. Implementation starts after approval of this foundation scope.

## Problem And Outcome

Before any legacy feature can be migrated, Geo Planner needs a maintainable Angular workspace with explicit architecture boundaries and repeatable quality gates.

The outcome of this project is only a migration-ready frontend foundation under `frontend/`. It does not migrate a map, project, layer, acquisition, inspection, overlay, or export feature.

This plan is single-use. After the foundation is accepted and documented, it is completed and eventually removed under the normal project lifecycle. It must not become the running plan for later frontend work.

## Scope

- scaffold the Angular application with exact tool versions and a lockfile;
- enable strict TypeScript, standalone components, zoneless change detection, and routing;
- establish the feature-first source boundaries from `docs/guidelines/angular-engineering-guide.md`;
- add an accessible empty application shell and placeholder route, without product behavior;
- configure formatting, lint/static analysis, Vitest, production build, and one minimal real-browser smoke test;
- establish runtime configuration and top-level error-reporting boundaries;
- select and configure the OpenAPI generator command, generated-source location, and application-owned API facade boundary;
- make the generation command accept a backend specification when one becomes available, without inventing or generating a complete future API;
- document local development and quality-gate commands.

## Non-goals

- migrating any existing product feature;
- implementing OpenLayers map behavior, projections, layers, or interactions;
- implementing project, AOI, acquisition, inspection, sketch, persistence, import, or export UI;
- defining future backend endpoints;
- creating mock APIs for features that the backend does not expose;
- generating the complete frontend transport client in advance;
- choosing feature-specific state, forms, visual-system, or component abstractions before a concrete feature needs them;
- removing or changing the legacy application.

## Decisions

- Use the newest stable Angular major and active patch available when scaffolding begins; preview dependencies still require the Angular guide's decision gate.
- The workspace uses standalone, zoneless, signal-ready Angular and the CLI's supported Vitest integration.
- The frontend lives under `frontend/` in this repository for the foundation increment.
- Generated transport code has a dedicated boundary and is never hand-edited.
- OpenAPI generation is prepared now but first produces meaningful code only when the owner-written backend publishes the first accepted endpoint.
- Every later frontend feature receives a new, separately named plan under `docs/projects/`, written from scratch for that feature's behavior, API contract, migration evidence, risks, tests, and acceptance.
- Later feature plans may reference this foundation and durable guidelines; they must not append their implementation steps or progress markers to this file.

## Implementation Plan

1. [pending] Confirm the supported Node.js/package-manager/browser baseline and exact Angular/tool versions.
2. [pending] Scaffold `frontend/` with standalone routing, zoneless operation, strict TypeScript, lockfile, and reproducible scripts.
3. [pending] Configure formatting, lint/static analysis, Vitest, production build, bundle budget, and minimal real-browser smoke testing.
4. [pending] Create the accessible empty shell, placeholder route, runtime configuration boundary, and top-level error boundary.
5. [pending] Establish feature-first directories and enforce the intended dependency direction without introducing speculative feature abstractions.
6. [pending] Configure a reproducible OpenAPI generation entry point and generated/API-facade locations without requiring a complete backend specification.
7. [pending] Document setup and run all frontend and repository quality gates.

## Failure And Safety

- Scaffolding must not refresh public data sources or modify legacy snapshots and local overlays.
- Dependency installation must produce a committed lockfile and reproducible clean install.
- A preview package must not enter the baseline without an explicit recorded rationale and fallback.
- OpenAPI preparation must not create handwritten placeholder DTOs that later compete with generated contracts.
- The legacy application remains the only functional UI after this project; the empty Angular shell must not be presented as migrated functionality.

## Review Gates

The owner reviews:

- exact framework/tool versions and any preview status;
- workspace scripts and dependency choices;
- source boundaries and empty shell;
- testing/build commands;
- OpenAPI generator choice and boundary;
- final clean-clone developer experience.

## Open Decisions

1. Which Node.js LTS and package manager/version are selected with the current Angular release?
2. Which browser baseline is required for the initial smoke test?
3. Which OpenAPI generator best fits the accepted Angular/TypeScript toolchain?
4. Are generated transport sources committed or reproduced in build/CI? This may be deferred until the first real backend contract if the generator setup remains reproducible.

## Verification And Acceptance

- A clean install uses the lockfile and documented tool versions.
- Formatting, lint/static analysis, strict type checking, Vitest, production build, and browser smoke test pass.
- The application starts and exposes only an accessible empty shell/placeholder route.
- The repository contains no migrated feature, speculative endpoint, handwritten transport DTO, provider URL, or OpenLayers behavior in the foundation.
- The OpenAPI generation command is documented and ready to receive a future backend specification.
- `./scripts/verify.sh` remains offline and passes.
- Owner acceptance closes this plan; the next frontend capability starts with a new project document.
