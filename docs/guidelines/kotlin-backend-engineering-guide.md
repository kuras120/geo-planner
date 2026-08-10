# Kotlin Backend Engineering Guide

## Purpose

Use these rules for Kotlin and Spring Boot backend work. Repository architecture
decides product boundaries, module names, persistence, external integrations,
API ownership, and deployment topology.

## Requirements-driven Delivery

- Start a substantial increment from accepted behavior or requirements, not a
  permanent technology roadmap.
- Define the intended contract, domain invariants, failures, operational needs,
  and acceptance evidence before selecting infrastructure.
- Publish API descriptions only for implemented or explicitly accepted behavior.
- Reuse accepted contract examples as HTTP and integration fixtures.
- Deliver bounded vertical slices through domain, application, adapter, API,
  tests, and operations rather than completing horizontal infrastructure layers.
- Update requirement status only from implementation and acceptance evidence.

## Language And Domain Modeling

- Write Kotlin-first code. Avoid Java bean, builder, `Optional`, static utility,
  and exception-heavy patterns when Kotlin has a clearer construct.
- Follow the official Kotlin coding conventions and enforce them in Gradle's
  `check` lifecycle.
- Prefer immutable state with `val`, read-only collection interfaces, constructor
  parameters, and transformations that return new values.
- Use nullability for genuine absence, avoid platform types at application
  boundaries, and do not use `!!` in production code.
- Use data classes for immutable values, commands, events, and transport records,
  not automatically for mutable identity-based entities.
- Use sealed types for closed state machines and result variants with exhaustive
  `when` expressions.
- Consider value classes for validated identifiers and scalar concepts when
  serialization, binding, and persistence interoperability are tested.
- Prefer named and default parameters and small factory functions over builders.
- Keep extension functions narrowly visible and owned by a natural receiver.
- Prefer clear loops or named functions over clever chains with hidden
  allocation, non-local returns, or unclear error flow.
- Keep public return types explicit where they form an API; document constraints
  that names and types cannot express.

## Spring And Concurrency

- Use constructor injection and validated immutable `@ConfigurationProperties`.
- Keep framework annotations and transport DTOs at adapter boundaries; domain
  types must be testable without starting Spring.
- Choose MVC, WebFlux, or coroutine APIs from measured concurrency and streaming
  needs; do not mix models accidentally across layers.
- Preserve structured concurrency. Never use `GlobalScope`; make cancellation,
  deadlines, and dispatcher choice explicit at blocking boundaries.
- Represent expected domain failures as typed results or sealed errors. Reserve
  exceptions for unexpected faults and translate them once at the delivery edge.
- Bound transactions around consistency rules rather than controllers or whole
  workflows, and keep remote calls outside database transactions where possible.
- Start with the simplest deployable topology that satisfies current reliability,
  scale, and ownership constraints.

## Build And Dependencies

- Use the Gradle Wrapper and Kotlin DSL. Keep build files readable and move
  repeated non-trivial logic into convention plugins.
- Centralize versions and use compatible platform or BOM alignment where useful.
- Adopt dependency locking or verification according to repository supply-chain policy.
- Every dependency must solve a documented problem and have testing, ownership,
  upgrade, and removal considerations.
- Add databases, brokers, reactive stacks, and distributed services only when a
  current requirement and operational model justify them.
- Make the repository's aggregate verification task depend on Gradle `check` or
  an equivalent complete backend quality gate.

## Architecture Boundaries

A typical dependency direction is:

```text
delivery adapters -> application -> domain
infrastructure adapters -> application ports
configuration -> adapter wiring
```

- Organize packages by cohesive capabilities; do not create empty layers or
  generic dumping grounds in advance.
- Keep persistence and provider SDK types outside domain and application APIs.
- Define storage and integration ports by required semantics, not by vendor names.
- Keep environment choices in composition and configuration, not `if local` or
  `if vendor` branches inside application services.
- Run contract tests against materially different adapter implementations.
- Generate or validate client DTOs from the published transport contract; do not
  expose backend domain classes as the wire model.
- Do not implement an unrestricted remote URL proxy. Select integrations through
  server-owned validated identifiers and allowlists.

## Testing

- Use Kotest on the JUnit Platform when it is the repository standard; use
  behavior tests for domain rules and property tests for broad invariant spaces.
- Keep most domain and application tests framework-free and fast.
- Use focused Spring tests for serialization, configuration, security, database
  integration, transactions, and wiring.
- Record deterministic external fixtures and keep normal verification offline.
- Cover success, invalid input, absence, timeout, cancellation, retry,
  concurrency, partial failure, and restart or persistence behavior as relevant.
- Ensure `./gradlew check` covers the repository's formatting, static analysis,
  unit, architecture, and focused integration gates.

## Backend Review Checklist

- Does the model use Kotlin nullability, immutability, sealed variants, and value
  semantics deliberately?
- Are domain and application types independent of Spring and transport DTOs?
- Are blocking, reactive, and coroutine boundaries explicit and tested?
- Does the API preserve accepted idempotency, compatibility, error, and
  authorization contracts?
- Are external integrations bounded, allowlisted, observable, and excluded from
  normal offline tests?
- Are transactions, retries, and state transitions safe under concurrency and
  partial failure?
- Is each dependency and infrastructure choice justified by a current need?

## Primary References

- [Kotlin coding conventions](https://kotlinlang.org/docs/coding-conventions.html)
- [Spring Framework Kotlin support](https://docs.spring.io/spring-framework/reference/languages/kotlin.html)
- [Spring Boot Kotlin support](https://docs.spring.io/spring-boot/reference/features/kotlin.html)
- [Gradle Kotlin DSL](https://docs.gradle.org/current/userguide/kotlin_dsl.html)
- [Kotest quick start](https://kotest.io/docs/quickstart/)
