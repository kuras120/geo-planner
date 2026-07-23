# Prototype Migration Preparation

## Status

- Phase: PROPOSED
- Created: 2026-07-23
- Updated: 2026-07-24
- Owner: Codex implements; repository owner reviews and accepts.
- Authorization: planning only. Discovery, characterization, requirement creation, behavior changes, and source refresh require explicit owner approval to start.

## Problem And Outcome

The Python and inline HTML application is useful migration evidence, but provider rules, location-bound snapshots, generated UI, and persistence remain interleaved. Rewriting directly from it would copy accidental structure into both new applications.

The outcome is a stable, sanitized baseline: observable behavior is inventoried, contracts and fixtures are explicit, runtime/private data is separated, and old/new implementations can be compared without continuing to productize the inline HTML.

After the prototype and integrations have been analyzed, the final discovery output includes concrete functional requirements describing exactly which user value and external integrations must be migrated.

## Scope And Non-goals

In scope:

- characterize workflows, layer behavior, spatial rules, and failures;
- define versioned neutral contracts before either rewrite depends on them;
- at the end of discovery, extract evidence-backed functional stories with stable IDs, concrete business value, exact integrations, realistic inputs/outputs, and end-to-end acceptance criteria;
- isolate hard-coded project, provider, and presentation assumptions;
- prepare small sanitized parity fixtures and offline verification;
- define cutover and legacy-deletion criteria.

Non-goals:

- redesign the legacy UI or add product features to it;
- refresh external sources implicitly;
- implement the Kotlin backend for the owner;
- delete legacy code before spatial and behavioral parity.

## Decisions

- The legacy runtime is a reference and fallback, not the target architecture.
- Only characterization, contract, privacy, and deterministic-comparison changes belong in it.
- Public sample identifiers/snapshots may remain; private overlays and generated HTML remain ignored.
- Backend-neutral OpenAPI/JSON examples are shared integration artifacts.
- Contract decisions require owner acceptance because they constrain both applications.
- Contract preparation is incremental. This stream supplies the examples and legacy evidence required for the next vertical slice, not a complete speculative API for the whole product.
- Do not create requirements before the workflow, code, data, and integrations have been inventoried and characterized.
- Requirements contain functional migration value. Engineering quality, build setup, framework conventions, and infrastructure-selection rules remain in guidelines, architecture, or research.
- Only the owner may approve this plan or accept requirements. Discussion, editing, or expansion of the plan is not approval.

## Implementation Plan

1. [pending] Inventory actual screens, controls, map interactions, keyboard behavior, persistence, export, refresh, warnings, and user-visible failure behavior.
2. [pending] Trace each capability through current code, configuration, source data, generated output, and local/private state.
3. [pending] Inventory each exact external integration: provider, operation/layer/document, request inputs, response form, optionality, provenance, and current limitation.
4. [pending] Add characterization tests for configuration, descriptors, overlays, layer ordering, selection, sketch round-trip, and failure preservation.
5. [pending] Create two compact sanitized spatial fixtures covering different locations and CRS/axis-order behavior.
6. [pending] Identify hard-coded provider/project assumptions and separate intended behavior from prototype accidents with owner decisions.
7. [pending] Put runtime-only artifact assumptions behind an explicit local data-root contract while preserving intentional fixtures.
8. [pending] Establish a side-by-side parity inventory and feature cutover ledger based on observed behavior.
9. [pending] Only after steps 1–8, create `docs/requirements/<domain>.md` containing concrete functional migration stories according to `docs/guidelines/requirements-guide.md`.
10. [pending] Review the generated stories with the owner; only the owner may accept, defer, reject, split, merge, or reprioritize them.
11. [pending] Freeze legacy features after discovery is accepted; permit only correctness, privacy, and comparison fixes.

## Verification And Acceptance

- `./scripts/verify.sh` stays offline and deterministic.
- Fixtures contain no names, private legal context, sketches, or generated exports.
- Every spatial fixture records bbox, CRS, coordinate order, source, and provenance.
- Two locations exercise the reference build without source-code edits.
- Each migrated feature has observable evidence, not remembered appearance.
- Every retained capability is represented by a concrete functional requirement traceable to observed legacy behavior, an exact integration, or an explicit owner decision.
- Requirements state realistic inputs, outputs, business value, degraded/failure behavior, and end-to-end acceptance; generic engineering tasks are excluded.
- The owner can determine exactly what backend integration to implement without reverse-engineering the prototype again.
- Legacy deletion requires frontend parity, backend integration, overlay migration, spatial checks, and owner acceptance.

## Dependencies

If approved and executed, this project supplies functional requirements, contract examples, parity evidence, and adapter fixtures for later owner-written backend and feature-specific frontend work. Target system boundaries are defined in `docs/architecture/target-product-architecture.md`.
