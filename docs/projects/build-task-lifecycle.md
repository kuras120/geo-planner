# Build Task Lifecycle

## Status

- Phase: IMPLEMENTED

## Problem And Outcome

The root `mise.toml` currently mixes environment setup, dependency installation,
verification, artifact assembly, and release naming:

- `build-local` installs npm dependencies and Chromium but also cleans and builds
  the backend;
- `verify` covers frontend, simulator, and legacy checks but invokes only the
  backend `test` task, bypassing other Gradle verification such as ktlint;
- `build-release` performs dependency installation and artifact assembly but does
  not publish or deploy a release;
- the GitHub workflow needs deterministic npm installation before running the
  shared verification gate.

The outcome is one task vocabulary shared by developers and CI, with installation,
verification, assembly, and release kept as distinct lifecycle concerns.

## Scope And Non-goals

In scope:

- reorganize root mise tasks for the backend, frontend, backend simulator, and
  legacy map checks;
- use mutable npm installation locally and frozen npm installation in CI;
- make one root `verify` task cover all repository quality gates;
- define artifact assembly separately from verification and deployment;
- simplify the GitHub workflow to invoke one CI orchestration task.

Non-goals:

- publishing a GitHub release, container image, frontend deployment, or backend
  deployment;
- changing application behavior or source acquisition;
- redesigning the npm scripts or Gradle lifecycle unless a missing verification
  edge is discovered during implementation;
- introducing another task runner.

## Decisions, Assumptions, And Open Questions

### Confirmed decisions

- The GitHub verification workflow will not retain build artifacts initially.
  Artifact assembly and upload will be added only when another job or a release
  process consumes the outputs.

### Proposed decisions

- `setup` is the developer-oriented dependency setup task. It uses `npm install`
  for both npm projects and installs Playwright Chromium.
- `setup-ci` is the clean, reproducible CI setup task. It uses `npm ci` for both
  npm projects and installs Chromium plus Linux browser dependencies.
- Neither setup task compiles, tests, or assembles the applications.
- The setup tasks do not run a separate backend dependency-installation step:
  Gradle has no required equivalent of `npm install`, and the Wrapper resolves
  the configurations needed by `check`, `bootRun`, or `bootJar` on demand.
- Component verification tasks are named `verify-backend`, `verify-frontend`,
  `verify-simulator`, and `verify-legacy`.
- `validate-tasks` runs mise's static task-definition validation and is included
  in root `verify`. It analyzes the task graph without executing the tasks it
  validates, so it does not recurse into `verify`.
- Root `verify` aggregates all component verification tasks and performs no
  explicit dependency-installation step. On a fresh machine, Gradle may still
  download the Wrapper distribution, plugins, and dependencies required by
  `:backend:check`.
- Backend verification invokes `./gradlew :backend:check`, not only
  `:backend:test`, so tests and attached static-analysis checks share one Gradle
  lifecycle gate.
- `assemble` creates the deployable backend and frontend outputs without cleaning,
  installing dependencies, publishing, or deploying.
- `ci` runs `setup-ci` and then `verify`. It may additionally assemble or upload
  artifacts only when the workflow has a consumer for them.
- The name `release` is reserved for a future versioning/publishing/deployment
  workflow. The current `build-release` task is replaced by `assemble`.
- Development server tasks (`frontend`, `backend`, `storybook`, and `simulator`)
  remain focused on running their respective processes.

### Assumptions

- Both npm projects continue to commit matching `package-lock.json` files.
- The frontend `npm run verify` remains the authoritative frontend quality gate,
  including its production build, Storybook build, and Playwright smoke test.
- A normal Gradle invocation may reuse incremental outputs and caches; routine
  `clean` is not required for correctness.
- The legacy verification remains offline and must never refresh external map
  sources.

### Open questions

- None.

## Task Contract

| Task | Responsibility | Expected commands |
| --- | --- | --- |
| `setup` | Mutable local dependency setup | `npm install` in frontend and simulator; Playwright Chromium install |
| `setup-ci` | Frozen clean CI dependency setup | `npm ci` in frontend and simulator; Playwright Chromium installation with Linux dependencies |
| `validate-tasks` | Static mise task-definition gate | `mise tasks validate` |
| `verify-backend` | Complete Kotlin/Spring quality gate | `./gradlew :backend:check` |
| `verify-frontend` | Complete Angular/UI quality gate | `npm --prefix frontend run verify` |
| `verify-simulator` | Complete contract-simulator quality gate | `npm --prefix backend-simulator run verify` |
| `verify-legacy` | Legacy Python/map offline gate | `./scripts/verify.sh` |
| `verify` | Aggregate all component gates | mise task dependencies on the four `verify-*` tasks |
| `assemble` | Produce deployable application artifacts | `./gradlew :backend:bootJar` and `npm --prefix frontend run build` |
| `ci` | Reproduce the pull-request quality gate | sequential `setup-ci`, then `verify` |
| `clean` | Explicitly discard generated build outputs | Gradle clean plus deliberate frontend/simulator output cleanup only if needed |

`clean` is an escape hatch, not a dependency of `verify`, `assemble`, or `ci`.

## Runtime Flow

Developer first setup:

```text
mise install -> mise run setup -> mise run verify
```

Developer iteration:

```text
source change -> mise run verify
```

Pull-request CI:

```text
checkout -> mise-action installs pinned tools -> mise run ci
         -> setup-ci -> validate-tasks
                     -> verify-backend
                     -> verify-frontend
                     -> verify-simulator
                     -> verify-legacy
```

Future artifact-producing workflow:

```text
checkout -> pinned tools -> setup-ci -> verify -> assemble -> upload/publish
```

Publishing or deployment remains outside `assemble` and requires an explicitly
designed release task.

## Failure Behavior And Migration Impact

- `setup-ci` fails when either lockfile is absent or inconsistent with its
  `package.json`; it must not repair or rewrite lockfiles.
- `verify` stops with a non-zero result when any component gate fails. Individual
  task reports remain attributable to their component.
- `assemble` assumes dependencies are already installed and fails clearly when
  they are missing.
- Playwright browser installation remains a networked setup operation; verification
  itself must not refresh government map sources. A first backend verification
  may access Gradle distribution, plugin, and dependency repositories unless the
  relevant Gradle caches are already populated.
- Existing users migrate from `mise run build-local` to `mise run setup`, and from
  `mise run build-release` to `mise run assemble`.
- README and repository guidance must be updated in the implementation so obsolete
  task names are not left behind.
- Existing uncommitted workflow and Gradle changes are owner work and must be
  preserved during implementation.
- Implementation inspection found that npm 10 requires the `npm exec --
  playwright ...` separator; without it, the former task displayed npm help
  instead of invoking Playwright. The setup tasks will use the corrected form.

## Implementation Plan

1. [done] Replace mixed root tasks with `setup`, `setup-ci`, component
   `verify-*` tasks, aggregate `verify`, `assemble`, and `ci`.
2. [done] Keep local installation mutable with `npm install`; make CI
   installation frozen with `npm ci` and install the required Playwright browser
   dependencies.
3. [done] Change backend verification from `:backend:test` to
   `:backend:check` and confirm ktlint remains attached exactly once.
4. [done] Update `.github/workflows/build.yml` to run `mise run ci` after
   checkout and mise tool setup.
5. [done] Update durable repository setup documentation and README command
   examples to the accepted task names.
6. [done] Run the individual tasks and the aggregate CI task, recording any
   unavoidable network-dependent setup separately from offline verification.
7. [done] Add static mise task-definition validation to the root verification
   graph without making the legacy quality gate depend on mise.

## Verification And Acceptance

- `mise tasks` presents task names and descriptions matching their responsibilities.
- `mise run validate-tasks` validates the task graph without recursively running
  `verify` or any component gate.
- `mise run setup` installs local npm dependencies and Chromium without compiling
  or testing either application.
- From clean npm worktrees, `mise run setup-ci` installs exactly the committed
  dependency graphs and leaves both lockfiles unchanged.
- `mise run verify-backend` runs backend tests and ktlint through Gradle `check`.
- `mise run verify-frontend`, `mise run verify-simulator`, and
  `mise run verify-legacy` each pass independently.
- `mise run verify` covers backend, frontend, simulator, and legacy checks without
  installing dependencies or refreshing external map sources.
- `mise run assemble` produces the backend Boot JAR and production frontend output
  without publishing or deploying them.
- `mise run ci` succeeds from a clean checkout after `mise install` and matches the
  GitHub pull-request gate.
- `git diff --exit-code -- frontend/package-lock.json backend-simulator/package-lock.json`
  succeeds after CI setup and verification.
- The GitHub workflow contains no empty steps and invokes only the root CI contract,
  not a second hand-maintained list of component commands.

## Result

- Implemented the accepted task vocabulary in root `mise.toml`, enabled the
  GitHub workflow through `mise run ci`, and updated README and repository
  guidance on 2026-08-08.
- Modeled `setup-ci` as the formal prerequisite of `ci` and `verify` as its
  native mise task step, preserving strict setup-before-verification ordering
  without nested shell invocations of `mise run`.
- Added `validate-tasks` to the root verification graph; it statically validates
  task definitions and does not execute the task graph being inspected.
- Corrected the Playwright invocation to use npm's required `exec --` separator;
  both `setup` and `setup-ci` completed successfully when allowed network/cache
  access, and neither npm lockfile changed.
- `mise tasks validate`, `verify-frontend`, `verify-simulator`,
  `verify-legacy`, and `assemble` passed. Frontend verification included 11 unit
  tests and one Chromium end-to-end test; simulator verification included two
  tests; legacy verification included 31 tests.
- `verify-backend`, aggregate `verify`, and therefore `ci` correctly fail on
  pre-existing ktlint violations in committed backend source and test files.
  Fixing those owner-maintained Kotlin files is outside this project's
  authorized implementation scope; no backend production code was changed.
- `npm ci` reports 15 existing frontend dependency audit findings (7 moderate,
  8 high). Dependency upgrades remain outside this project.
- No spatial data, sources, configuration, or manual overlays changed, so no
  manual spatial alignment check was required.
- Awaiting owner acceptance before project closeout.
