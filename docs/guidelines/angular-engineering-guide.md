# Angular Engineering Guide

## Purpose And Ownership

This guide governs the replacement Geo Planner frontend. Codex implements the frontend; the owner reviews and accepts it. The frontend is a thin client: it owns presentation, browser interaction, transient UI state, and OpenLayers rendering, while the backend owns trusted provider integration, authoritative project state, acquisition, validation, and persistence.

Backend code is outside the frontend implementation mandate. Contract questions are resolved in OpenAPI and project decisions rather than by silently changing either side.

Frontend delivery is incremental. First complete and close one bounded frontend-foundation project. Then create a new plan from scratch for each end-to-end feature as the owner-written backend exposes accepted capabilities. Do not turn the foundation into a rolling backlog, batch the rewrite, or run the frontend several speculative features ahead.

## Version And Preview Policy

- Start each implementation increment on the newest Angular stable major and active patch available that day. Record exact Angular, TypeScript, Node.js, package-manager, and OpenLayers versions in the workspace and lockfile.
- The `next` or release-candidate channel is allowed when the owner accepts the concrete benefit and upgrade risk.
- A Developer Preview or experimental API requires a short ADR or project decision naming the benefit, stability label, containment boundary, fallback, and removal/upgrade trigger.
- Keep preview APIs behind a feature-local adapter. Do not let an unstable forms, state, rendering, or build API become a repository-wide convention.
- Upgrade one concern at a time and run the full quality gate. Do not combine a framework-major upgrade with a large feature migration.

As of 2026-07-23, Angular 22 is the current stable major. New CLI applications use Vitest, zoneless change detection is the default from Angular 21, and `httpResource` is stable in Angular 22. Signal Forms suit new signal-based applications, but Angular still recommends Reactive Forms when production stability guarantees are required. Therefore Reactive Forms are the default until a feature-scoped Signal Forms decision is accepted.

## Application Shape

Use a single Angular application organized by product feature, with small platform boundaries:

```text
frontend/src/app/
  core/                 bootstrap, error reporting, runtime config
  api/
    generated/          generated transport code; never hand-edit
    geo-planner-api.ts  application-owned API facade
    mappers/            transport DTO <-> domain mappings
  map/                  OpenLayers adapter, projection and interaction ports
  features/             projects, layers, inspect, sketch, acquisition, export
  shared/ui/            genuinely reusable presentation primitives
```

- Use standalone components and functional providers. Do not introduce NgModules for application features.
- Lazy-load route-level features. Keep route configuration close to the feature and use stable URLs as user-visible state.
- A feature may depend on `core`, `api`, `map`, and `shared`; reusable platform areas must not depend on features.
- Do not create generic `utils`, `common`, or `services` dumping grounds. Name modules after domain capabilities.
- Keep files focused and colocate a component's TypeScript, template, styles, and tests.

## Component Composition

- Route/page components orchestrate use cases and convert feature state into explicit child inputs.
- Presentation components receive data through signal `input()` and report intent through `output()`. Outputs describe domain actions such as `layerVisibilityChanged`, not DOM mechanics such as `buttonClicked`.
- Use `model()` only for a natural two-way control value. Do not use it to hide a workflow or mutate parent-owned domain state.
- Prefer composition, content projection, directives, and small typed configuration objects over component inheritance.
- Reusable UI must not inject feature stores, HTTP clients, the router, or OpenLayers objects.
- Keep lifecycle hooks small and delegate to behavior-named methods. Use lifecycle interfaces when hooks are needed.
- Prefer built-in template control flow and direct `class`/`style` bindings. Move non-trivial computation to `computed()` or pure functions.
- Preserve accessibility: native elements first, visible focus, keyboard access, labelled controls, announced async/error state, and no color-only meaning.

## State And Reactivity

- Use signals for synchronous local and feature state, `computed()` for derived values, and `effect()` only for actual external side effects.
- Keep writable signals private; expose readonly state and intention-revealing commands.
- Use RxJS for event streams, cancellation, debouncing, WebSocket/SSE streams, and orchestration where time is part of the model. Convert at deliberate boundaries.
- Do not introduce NgRx or another global store until multiple features need coordinated history, effects, or debugging that feature-scoped signals cannot provide.
- Run zoneless. Notify Angular through signals, template listeners, `AsyncPipe`, or explicit framework APIs; do not depend on ZoneJS side effects.
- Model loading, empty, ready, partial, stale, and failure states explicitly instead of combining unrelated booleans.

## API Input And Output

The published OpenAPI document is the transport contract.

```text
component -> feature facade/store -> application API facade
          -> generated OpenAPI client -> same-origin backend
```

- Generate transport clients and DTOs; never hand-edit generated files or import them directly into reusable components.
- Treat OpenAPI generation as a repeatable development loop. Regenerate after every accepted backend contract change and review the generated diff before adapting application code.
- Generate only from the backend's current published contract. Do not invent placeholder future endpoints to produce a complete client early.
- Keep the generator configuration and command stable from the first real endpoint onward. Decide once whether generated sources are committed or CI-produced, then enforce reproducibility.
- Map transport DTOs to frontend domain/view models at the API boundary.
- Keep queries and commands distinct. A command contains the smallest explicit intent, not a serialized screen or giant mutable project.
- Use stable identifiers, ISO-8601 timestamps, explicit CRS/coordinate order, discriminated unions for closed variants, and defined absent-versus-null semantics.
- Treat server output as untrusted. Check status, content type, invariants, and spatial metadata; use runtime validation where generated typing cannot prove validity.
- Use `httpResource` for suitable idempotent reads. Use injectable HttpClient services for mutations, uploads, downloads, cancellation, and deliberately controlled workflows.
- HTTP calls do not belong in components. Centralize base URL, correlation headers, timeouts, and error translation.
- Do not retry mutations automatically. Retry safe reads only under a bounded visible policy; use backend idempotency for acquisition commands.
- Preserve problem details, field errors, warnings, provenance, and correlation IDs in typed results. Translate them to Polish UI at the presentation boundary.
- The browser never receives arbitrary provider URLs, secrets, WMS axis-order rules, or filesystem paths.

## Incremental Migration Discipline

- Keep at most one substantial frontend migration slice in progress.
- Give every substantial feature its own `docs/projects/**` plan with feature-specific scope, contract, legacy evidence, risks, verification, and acceptance criteria.
- Close the foundation plan after scaffolding; never append feature steps or progress to it.
- Each slice starts with current legacy evidence and one accepted backend contract, and ends with an owner-reviewed working browser capability.
- Prefer a thin end-to-end slice over completing all API infrastructure, all map infrastructure, or all components in isolation.
- Keep the legacy path operational for capabilities not yet migrated.
- Do not combine Angular/framework upgrades, broad visual redesign, OpenAPI-wide refactoring, and feature migration in one slice.
- A generated-client compilation break is contract feedback and is resolved in the current slice, not hidden behind `any`, duplicate DTOs, or permanent adapters for draft shapes.
- Mark a legacy capability as migrated only after backend, generated client, Angular behavior, error handling, and relevant spatial/browser checks pass together.

## OpenLayers Boundary

- `MapFacade` is the general imperative boundary. Components express intent and observe typed events; they do not retain OpenLayers map, layer, source, feature, or interaction instances.
- Use focused adapters for projections, layer materialization, selection, sketch interactions, and export rather than one unbounded facade class.
- Keep domain-ID to OpenLayers-object mappings inside the adapter.
- Register projections explicitly and preserve CRS, axis order, extent, resolution, attribution, and provenance.
- Clean up targets, listeners, interactions, object URLs, and subscriptions deterministically.
- Test domain-to-map descriptors without a browser, then cover rendering and interaction in real-browser tests.

## Forms

- Use strictly typed Reactive Forms by default for project/AOI and overlay editing.
- Keep form models separate from API commands; normalize and validate before mapping a submission.
- Surface backend field errors without replacing client validation.
- Signal Forms may be piloted only after a preview-policy decision. Their removal must not change API or domain models.

## Testing And Quality Gates

- Use Angular CLI's default Vitest integration for unit and component tests.
- Test through public inputs, outputs, DOM, and feature facades rather than private details.
- Use `provideHttpClientTesting` and contract fixtures derived from OpenAPI examples.
- Add real-browser tests for map rendering, projections, pointer/keyboard interaction, sketching, resize, cleanup, and downloads.
- Prefer `whenStable()` and visible assertions in zoneless tests; avoid indiscriminate `detectChanges()`.
- Gate on formatting, lint/static analysis, type checking, unit tests, production build, bundle budgets, and selected browser tests.
- Include accessibility plus reduced-motion, narrow viewport, slow request, cancellation, partial failure, and stale-artifact cases.

## Review Checklist

- Is the thin-client boundary preserved?
- Are API DTOs isolated and mapped?
- Is state valid by construction and narrowly owned?
- Are components composed through typed inputs/outputs without hidden coupling?
- Is OpenLayers imperative behavior behind the map boundary?
- Are preview APIs documented, isolated, and replaceable?
- Are warnings, provenance, accessibility, cleanup, and proportionate tests covered?

## Primary References

- [Angular releases](https://angular.dev/reference/releases)
- [Angular style guide](https://angular.dev/style-guide)
- [Angular components](https://angular.dev/guide/components)
- [Angular HTTP](https://angular.dev/guide/http)
- [Angular `httpResource`](https://angular.dev/api/common/http/httpResource)
- [Angular resources](https://angular.dev/guide/signals/resource)
- [Angular zoneless](https://angular.dev/guide/zoneless)
- [Angular testing](https://angular.dev/guide/testing)
- [Angular Signal Forms](https://angular.dev/guide/forms/signals/overview)
