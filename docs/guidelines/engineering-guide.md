# Engineering Guide

## Design

- Keep product facts and environment-specific values in explicit configuration;
  keep reusable behavior in code.
- Separate external acquisition and mutable setup from deterministic build,
  test, and verification paths.
- Validate configuration, external input, and serialized formats at their
  boundaries with contextual errors.
- Derive repeated identifiers, paths, URLs, and labels from one authoritative
  source instead of duplicating them.
- Keep domain, transport, persistence, and presentation models distinct where
  they have different invariants or ownership.
- Introduce dependencies and abstractions only for demonstrated needs.

## State And Safety

- Treat ignored or external user-owned files as data, not disposable build
  output. Preserve them unless the user explicitly authorizes replacement.
- Use atomic writes or transactional state changes for durable mutations.
- Validate paths, origins, authorization, request size, and payload shape at
  trust boundaries.
- Never run network refresh, destructive migration, or live integration calls
  as a hidden part of tests, normal builds, hot reload, or verification.
- Preserve the last usable optional artifact when a refresh fails unless the
  product contract explicitly requires removal.
- Keep generated artifacts distinguishable from source and regenerate them
  through their owning task rather than editing them manually.

## Testing And Verification

- Test domain invariants, boundary validation, failure behavior, and unsafe
  inputs at the narrowest useful layer.
- Add regression coverage for every correctness, parsing, persistence,
  integration, or public-contract bug.
- Keep fixtures small, deterministic, and free of secrets or private data.
- Add focused integration and end-to-end checks only where unit tests cannot
  prove the boundary.
- Finish changes with the repository verification entry point routed by
  `AGENTS.md`; report any manual checks or unavailable gates separately.

## Technical Documentation

- Present evidence and current facts before conclusions or proposals.
- Describe an accepted model positively: state what the system does and which
  boundary it adopts. Do not define it by listing rejected mechanisms.
- Put considered but unselected approaches under **Alternatives Considered**. Give
  each one an explicit status such as **Rejected**, **Rejected for now**, or
  **Deferred**, followed by the reason and, when useful, the condition for revisiting
  it.
- Keep open decisions separate from findings, accepted decisions, and alternatives.
- Use the order **Findings**, **Decision** or **Accepted Model**, **Alternatives
  Considered**, and **Open Decisions** when all four are present.
- Use Mermaid for durable architecture, data-flow, state, or interaction
  diagrams when the relationships are materially clearer visually than in
  prose or a compact table. Keep diagrams focused, label boundaries and
  direction explicitly, and update them with the model they document.

## Specialized Guides

- `angular-engineering-guide.md` defines transferable Angular, API-client,
  component-composition, state, and frontend testing standards.
- `kotlin-backend-engineering-guide.md` defines transferable Kotlin, Spring,
  Gradle Kotlin DSL, Kotest, and backend standards.
- Repository-specific architecture and domain documents decide which of those
  patterns apply to the current system.

## Review Standard

Prioritize correctness, data loss, privacy, authorization, unsafe filesystem or
network access, concurrency, contract regressions, unexpected external calls,
and claims stronger than their evidence. Require documentation changes when
configuration ownership, supported behavior, data meaning, or runtime flow
changes.
