# Repository Guide

## Environment

Root-level `mise.toml` pins the JDK and Node.js versions used by the Kotlin
backend, Angular frontend, OpenAPI Generator, and Node contract simulator.
Gradle uses the committed wrapper. The frontend and simulator have independent
npm lockfiles. Python 3, Bash, and `curl` support the retained legacy
application and requirements-index helper; they are not runtimes of the new
application.

Install tools and local dependencies from the repository root:

```bash
mise install
mise run setup
```

`setup` performs mutable local npm installation and installs Playwright
Chromium. `setup-ci` uses frozen npm installation plus Linux browser
dependencies. Both access external download services.

## Root Tasks

```bash
mise run frontend          # Angular development server
mise run backend           # Spring Boot development server
mise run storybook         # shared UI workshop
mise run simulator         # loopback contract simulator
mise run validate-tasks    # validate mise task definitions
mise run verify            # aggregate repository quality gate
mise run assemble          # backend Boot JAR plus production frontend
mise run ci                # setup-ci followed by verify
mise run clean             # generated application and test outputs
```

`mise run verify`, backed by `[tasks.verify]`, is the only aggregate
verification entry point. It validates the mise graph, checks the requirements
index, and runs the backend, frontend, simulator, and legacy gates. The legacy
gate builds from checked-in snapshots but does not refresh external sources.

`verify-legacy` is available for a focused legacy check. Its implementation,
`scripts/verify.sh`, is an internal task detail and should not be used as a
second aggregate entry point.

`mise run assemble` assumes setup has completed and creates artifacts without
publishing or deploying them. On a fresh machine Gradle and npm verification
may resolve dependencies from the network; application tests must not call live
product integrations.

## Components

### Backend

`backend/` is the Kotlin/Spring Boot application. Use the root `backend` and
`verify-backend` tasks or, for a focused local check, the Gradle wrapper:

```bash
./gradlew :backend:check
./gradlew :backend:bootRun --console=plain
```

### Frontend

`frontend/` is the Angular CLI workspace. The root application uses `src/`;
reusable presentation code lives in `projects/ui/`; generated transport,
mapping, and application API boundaries live in `projects/geo-planner-api/`.

```bash
npm --prefix frontend start
npm --prefix frontend run storybook
npm --prefix frontend run test:unit
npm --prefix frontend run e2e
npm --prefix frontend run verify
npm --prefix frontend run api:generate -- /path/to/openapi.yaml
```

OpenAPI generation owns
`frontend/projects/geo-planner-api/src/lib/generated/`; never hand-edit its
output. Transport DTOs are mapped under `mappers/` and wrapped by the
application-facing `facade/` only when an accepted capability requires them.
Runtime deployment configuration is read from
`frontend/public/runtime-config.json`; `apiBaseUrl` must remain a same-origin
absolute path.

The Angular persistent disk cache is disabled because the current transitive
native cache acceleration is unstable with the pinned Node.js build on macOS
ARM. This affects build speed only and can be revisited after the dependency is
corrected.

### Contract Simulator

`backend-simulator/` is a loopback-only Node adapter for frontend development.
It currently exposes `GET /_simulator/health`. Product routes, payloads,
fixtures, and named scenarios enter only with accepted contract slices; the
simulator never defines the contract.

```bash
npm --prefix backend-simulator run verify
mise run simulator
```

### HTTP Examples

`http-client/` contains developer HTTP requests for exercising implemented
backend endpoints. Keep examples free of secrets and aligned with published
contracts.

## Requirements Index

After changing a requirement, its status, priority, or delivery stage, update
the area index and regenerate the portfolio tables:

```bash
./scripts/update_requirements_index.py
```

The `verify-requirements` mise task runs the read-only check and rejects stale
statistics.

## Generated And Local Files

Build output, test reports, browser artifacts, local runtime state, and generated
clients follow their owning tool's ignore rules. Do not edit generated output
as source or commit private runtime data.

The `mapa/**` tree remains a runnable legacy application and migration reference.
Use `mapa/README.md` for its build, editor, interaction, configuration, source
refresh, and safety instructions. New application work must not change legacy
code, configuration, templates, or tracked data incidentally. Source refresh
always requires an explicit request because it replaces checked-in evidence.

## Troubleshooting

- Missing tools: run `mise install`, then confirm `mise current`.
- Missing npm dependencies or browser: run `mise run setup`.
- Backend dependency resolution failure: retry the focused Gradle task after
  confirming network and repository availability.
- Stale requirement totals: run the requirement-index updater, then
  `mise run verify-requirements`.
- Frontend API generation failure: confirm the supplied OpenAPI file exists and
  represents the backend's accepted published contract.
