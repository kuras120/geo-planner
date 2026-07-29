# Angular Frontend Foundation

## Status

- Phase: IMPLEMENTED
- Created: 2026-07-23
- Updated: 2026-07-29
- Implementation owner: frontend implementation agent.
- Reviewer and acceptance owner: repository owner.
- Authorization: implementation approved by the repository owner on 2026-07-29.

## Problem And Outcome

Before any legacy feature can be migrated, Geo Planner needs a maintainable Angular workspace with explicit architecture boundaries and repeatable quality gates.

The outcome of this project is only a migration-ready frontend foundation under `frontend/`. It does not migrate a map, project, layer, acquisition, inspection, overlay, or export feature.

This plan is single-use. After the foundation is accepted and documented, it is completed and eventually removed under the normal project lifecycle. It must not become the running plan for later frontend work.

## Scope

- scaffold the Angular application with exact tool versions and a lockfile;
- pin the repository Node.js toolchain through root-level mise configuration;
- enable strict TypeScript, standalone components, zoneless change detection, and routing;
- use the Angular CLI workspace convention: the root application under
  `frontend/src/` and reusable Angular libraries under `frontend/projects/`;
- scaffold `ui` and `geo-planner-api` as the initial library boundaries;
- add an accessible empty application shell and placeholder route, without product behavior;
- configure Storybook for shared UI development;
- configure formatting, lint/static analysis, Vitest, production build, and one
  minimal Playwright real-browser smoke test;
- establish runtime configuration and top-level error-reporting boundaries;
- select and configure the OpenAPI generator command, generated-source location, and application-owned API facade boundary;
- make the generation command accept a backend specification when one becomes available, without inventing or generating a complete future API;
- create the separate root-level `backend-simulator/` Node application and its
  non-product readiness boundary without inventing future API endpoints or
  contract fixtures;
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
- Use the newest Node.js LTS available at implementation start and pin its exact
  resolved version in root-level `mise.toml`.
- Use npm with committed package lockfiles for both Node workspaces.
- The workspace uses standalone, zoneless, signal-ready Angular and the CLI's supported Vitest integration.
- The frontend lives under `frontend/` in this repository for the foundation increment.
- The root Angular application follows the CLI convention under `frontend/src/`.
  Angular libraries follow the CLI convention under `frontend/projects/`.
- The initial Angular libraries are `ui` for genuinely shared presentation and
  `geo-planner-api` for generated transport, mapping, and application-owned API
  facade boundaries.
- Feature code starts under `frontend/src/app/features/`. It becomes another
  Angular library only when an independently reusable or enforceable domain
  boundary justifies the packaging cost.
- Use the newest stable Storybook compatible with the selected Angular version.
  Keep its shared configuration under `frontend/.storybook/`.
- Use Playwright with Chromium for the minimal application E2E smoke test.
- Keep the Node contract simulator in root-level `backend-simulator/`, outside
  the Angular CLI workspace and with its own package lockfile.
- The implemented baseline resolves to Node.js `24.18.1`, npm `11.16.0`,
  Temurin JDK `25.0.3+9`, Angular CLI `22.0.9`, Angular `22.0.8`,
  Storybook `10.5.5`, Playwright `1.62.0`, and OpenAPI Generator CLI wrapper
  `2.40.1` with generator `7.24.0`.
- Generated transport code has a dedicated boundary and is never hand-edited.
- OpenAPI generation is prepared now but first produces meaningful code only when the owner-written backend publishes the first accepted endpoint.
- Every later frontend feature receives a new, separately named plan under `docs/projects/`, written from scratch for that feature's behavior, API contract, migration evidence, risks, tests, and acceptance.
- Later feature plans may reference this foundation and durable guidelines; they must not append their implementation steps or progress markers to this file.

## Implementation Plan

1. [done] Record the supported Node.js/package-manager/browser baseline
   and exact Angular/tool versions.
2. [done] Scaffold `frontend/` with standalone routing, zoneless operation, strict TypeScript, lockfile, and reproducible scripts.
3. [done] Generate the `ui` and `geo-planner-api` Angular libraries using the
   native `projects/` convention.
4. [done] Configure Storybook, formatting, lint/static analysis, Vitest,
   production build, bundle budget, and minimal Playwright smoke testing.
5. [done] Create the accessible empty shell, placeholder route, runtime configuration boundary, and top-level error boundary.
6. [done] Establish feature-first directories and enforce the intended dependency direction without introducing speculative feature abstractions.
7. [done] Configure a reproducible OpenAPI generation entry point and generated/API-facade locations without requiring a complete backend specification.
8. [done] Create the backend simulator foundation without product endpoints
   or speculative contract data.
9. [done] Document setup and run all frontend and repository quality gates.

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

- Whether generated transport sources are committed or reproduced in build/CI
  remains deferred until the first accepted backend contract. The generator
  entry point must remain reproducible in either case.

## Verification And Acceptance

- A clean install uses the lockfile and documented tool versions.
- Formatting, lint/static analysis, strict type checking, Vitest, production build, and browser smoke test pass.
- The application starts and exposes only an accessible empty shell/placeholder route.
- The repository contains no migrated feature, speculative endpoint, handwritten transport DTO, provider URL, or OpenLayers behavior in the foundation.
- The OpenAPI generation command is documented and ready to receive a future backend specification.
- `./scripts/verify.sh` remains offline and passes.
- Owner acceptance closes this plan; the next frontend capability starts with a new project document.

## Result

- Added the mise-pinned Node/JDK toolchain and repository tasks for install,
  development, Storybook, simulator, and complete verification.
- Added the Angular workspace, `ui` and `geo-planner-api` libraries, accessible
  lazy-loaded placeholder shell, runtime configuration validation, global error
  handling, Storybook, ESLint, Prettier, Vitest, Playwright, bundle budgets,
  and reproducible OpenAPI generation boundary.
- Added the separate loopback-only Node simulator. Its only implemented route
  is `GET /_simulator/health`; all unaccepted product routes return Problem
  Details `404`.
- Disabled the Angular persistent disk cache because the transitive
  LMDB/message-pack native acceleration crashes under the pinned Node 24 build
  on macOS ARM. Builds remain correct; only cache performance is unavailable.
- Follow-up review made TypeScript and Angular template strictness explicit and
  validates the configured API path with the platform URL parser so
  backslash-based inputs cannot escape the same-origin boundary.
- `mise run verify` passes: simulator formatting/typecheck/build and 2 tests;
  frontend formatting/lint/typecheck, 11 Vitest tests, production build,
  Storybook build, and 1 Chromium E2E test; and the existing 31-test offline
  repository gate.
- The production Angular initial bundle is 196.94 kB raw and approximately
  55.60 kB transferred, within the configured budget.
- Manual simulator smoke returned HTTP `200` with the expected readiness JSON
  on `127.0.0.1:4300`.
- `npm audit` was not run because it exports dependency metadata to the npm
  registry and that external disclosure was not separately authorized.
