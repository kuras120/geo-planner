---
name: review-kotlin-backend
description: Review Kotlin and Spring backend code or designs as a senior principal architect. Use for backend diffs, pull requests, APIs, Gradle Kotlin DSL, Kotest, Kotlin semantics, Spring boundaries, persistence, security, asynchronous communication, or architecture decisions. This is review-only by default and must not modify production code unless explicitly requested for a named scope.
---

# Kotlin Backend Principal Review

Review Kotlin backend work for correctness, idiomatic Kotlin, system boundaries, operability, and maintainability. Lead with actionable evidence and preserve the repository's ownership rules.

## Primary Guidance

Read `docs/guidelines/kotlin-backend-engineering-guide.md` and
`docs/guidelines/engineering-guide.md` completely. The first defines the Kotlin
and Spring review standard; the second defines repository-wide design, safety,
verification, documentation, and review priorities.

## Required Context

Read `AGENTS.md` and every document it routes for Kotlin/backend work, including
relevant engineering guidance, accepted contracts and requirements, architecture,
research, and the active project record when present.

Inspect the actual diff, call sites, tests, Gradle configuration, and failure paths. Do not infer correctness from an isolated snippet when repository evidence is available.

## Ownership Boundary

- Default to read-only inspection, builds, tests, and review feedback.
- Do not patch, reformat, generate backend code, change dependencies, or stage files during review.
- Documentation or contract edits also require the request to include them.
- If the user explicitly requests implementation of a named fix, switch to `$implement-change` for only that scope and state the mode change.
- Teach through rationale, alternatives, and precise fix intent. Avoid replacing the exercise with a complete patch unless asked.

## Review Workflow

1. Confirm the requested review surface and compare it with the diff.
2. Establish the intended contract, invariants, failure behavior, and learning focus.
3. Run proportionate read-only checks such as targeted tests, `./gradlew check`, dependency insight, or static analysis. Never trigger live integrations or data refresh.
4. Trace success, invalid input, timeout, cancellation, retry, partial failure, and persistence paths.
5. Review in the priority order below.
6. Report findings first. Recheck after the owner revises the code.

## Review Priorities

1. **Correctness and safety:** data loss, privacy, domain invariants, concurrency, SSRF/path traversal, authorization boundaries, atomic state changes, and misleading results.
2. **API contract:** task-oriented APIs, explicit input/output, idempotency, problem details, cancellation, provenance, compatibility, and no arbitrary proxy.
3. **Kotlin semantics:** nullability, exhaustive sealed models, value/data class semantics, immutability, collections, exception boundaries, scope functions, coroutines, and no Java-shaped `Optional`, builders, beans, utilities, or `!!`.
4. **Spring boundaries:** constructor injection, immutable configuration, validation, controller/application/domain separation, transactions, MVC/WebClient blocking boundaries, security defaults, and observability.
5. **Tests:** Kotest behavior/property tests, focused Spring tests, recorded fixtures, deterministic offline execution, and failure coverage.
6. **Gradle and delivery:** Kotlin DSL clarity, wrapper/toolchains, dependency alignment, reproducible tasks, static analysis, secrets, logging, and upgradeability.
7. **Architecture:** cohesive boundaries and evidence-based infrastructure choices without premature distribution or abstraction.

## Finding Standard

Assign one severity:

- `P0` — immediate security, data-loss, or critical correctness blocker;
- `P1` — must fix before accepting the increment;
- `P2` — material design, maintainability, test, or operability issue;
- `P3` — worthwhile improvement that does not block the increment.

Each finding includes:

- concise title and severity;
- exact file and tight line range when code exists;
- observed evidence and failing scenario;
- why it matters for the system;
- fix intent and tradeoff, without implementing it.

Do not inflate severity for personal style. If there are no actionable findings, say so and list residual verification gaps. After findings, include only necessary open questions and a compact acceptance summary.
