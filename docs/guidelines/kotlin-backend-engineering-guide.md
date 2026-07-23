# Kotlin Backend Engineering Guide

## Purpose

These rules govern the owner-written Kotlin/Spring Boot backend. They complement the repository-wide design, spatial-data, safety, and testing rules in `engineering-guide.md`.

Codex reviews backend work through `$review-kotlin-backend` and does not modify backend production code unless the owner explicitly requests implementation for a named scope.

## Requirements-driven Delivery

- Start backend work from one coherent set of accepted IDs in `docs/requirements/**`, not from a permanent backend roadmap.
- Create a new bounded project plan for that slice. State the user outcome, domain invariants, API input/output/errors, external integration, tests, and definition of done.
- The owner implements the Kotlin slice and requests review. Codex remains read-only unless explicitly asked to implement a named fix.
- Publish OpenAPI only for implemented or currently accepted behavior. After backend review, it can unlock a separately planned frontend slice.
- Finish backend, contract, fixture, and operational acceptance for the selected requirements before starting another substantial slice.
- Update requirement status only from evidence: `ACCEPTED` to `IMPLEMENTED`, then `VERIFIED` after all acceptance checks pass.

Suggested learning progression is deliberately incremental:

1. reproducible Gradle Kotlin DSL/Kotest/configuration foundation;
2. one framework-free domain model and typed error set;
3. one task-oriented HTTP endpoint and OpenAPI contract;
4. one bounded provider adapter using recorded fixtures;
5. one restart-safe job/persistence flow;
6. repeated vertical slices driven by accepted product requirements.

## Language And Domain Modeling

- Write Kotlin-first code. Do not reproduce Java bean, builder, `Optional`, static utility, or exception-heavy patterns when Kotlin has a clearer language construct.
- Follow the official Kotlin coding conventions and enforce them in the Gradle `check` lifecycle.
- Prefer immutable state: use `val`, read-only collection interfaces, constructor parameters, and transformations that return new values. Confine necessary mutation to explicit aggregate, job, and storage boundaries.
- Use nullability to model genuine absence. Avoid platform types at application boundaries, never use `!!`, and validate external nullability before values enter the domain.
- Use data classes for immutable values, commands, events, and transport records. Do not use them automatically for mutable entities whose equality or identity has different semantics.
- Use sealed interfaces/classes for closed state machines and result variants, with exhaustive `when` expressions.
- Consider value classes for identifiers and validated scalar concepts when Jackson, Spring binding, and persistence interoperability are covered by tests.
- Prefer named/default parameters and small factory functions over builders. Use extension functions only when the receiver is the natural semantic owner; keep visibility narrow and avoid catch-all extension/utility files.
- Use scope functions and collection chains only when they make ownership and control flow clearer. Prefer a simple loop or named function over a clever expression with hidden allocation or non-local returns.
- Keep public/member return types explicit where they form an API. Add KDoc for public contracts whose constraints are not clear from names and types.

## Spring And Concurrency

- Use constructor injection only. Keep configuration in validated, immutable `@ConfigurationProperties` data classes.
- Keep framework annotations and transport DTOs at the API/adapter boundary; domain types must be testable without starting Spring.
- Start with Spring MVC controllers and `WebClient` for outbound streaming HTTP. Do not expose Reactor `Mono`/`Flux` from domain or application services.
- Use coroutines only for real asynchronous/concurrent work and preserve structured concurrency. Never use `GlobalScope`; make cancellation and dispatcher choice explicit at blocking boundaries.
- Represent expected domain failures as typed results or sealed errors. Reserve exceptions for unexpected faults and translate them once at the HTTP boundary.
- Keep the application a modular monolith until a measured scaling, deployment, or ownership boundary justifies a service split.

## Build And Dependencies

- Use the Gradle Wrapper and Kotlin DSL exclusively. Keep `settings.gradle.kts` and `build.gradle.kts` readable; move repeated non-trivial build logic into convention plugins rather than ad-hoc scripts.
- Centralize plugin/dependency versions and use the Spring/Kotlin BOMs where applicable. Commit dependency locking or verification metadata when the backend supply-chain policy is established.
- The first backend increment includes Kotest on the JUnit Platform. Use Kotest assertions/specs for domain behavior and property testing for parsers, bbox/CRS invariants, and idempotency.
- Use focused Spring integration tests only for HTTP serialization, configuration, security, and wiring. Keep most tests framework-free and fast.
- Add PostgreSQL/Testcontainers when relational persistence becomes a real feature. Add Spring Security with the first identity/authorization requirement. Add RabbitMQ only when durable cross-process asynchronous delivery is required.
- Every new dependency must solve a documented problem and include an ownership, testing, and removal/upgrade story.

## Suggested Modular Structure

```text
backend/
  api/             controllers, transport DTOs, exception mapping
  application/     project and acquisition use cases
  domain/          AOI, source, layer, job, artifact, provenance
  adapters/http/   ULDK, WMS/WMTS, planning/vector clients
  adapters/store/  local manifests and artifact storage
  config/          validated catalog and HTTP/job policies
```

Package names may evolve with implemented capabilities. Preserve dependency direction and cohesive domain ownership rather than creating every empty package up front.

## Thin-client Contract

- The backend owns project state, trusted source configuration, ULDK/WMS/GML protocol behavior, acquisition jobs, cache/provenance decisions, overlays, and export assembly.
- The Angular client owns presentation, OpenLayers rendering, form state, and transient interaction state. It must not contain provider endpoints, credentials, WMS layer names, axis-order rules, or authoritative persistence logic.
- Generate or validate frontend DTOs from OpenAPI. Do not share backend domain classes directly as the wire contract.
- Never implement a generic remote-URL proxy. Provider access is selected through server-owned, validated catalog identifiers.

## Backend Review Checklist

- Does the model use Kotlin nullability, immutability, sealed variants, and value semantics deliberately?
- Are domain/application types independent of Spring and transport DTOs?
- Are blocking, Reactor, and coroutine boundaries explicit, cancellable, and tested?
- Does the API preserve the accepted thin-client, provenance, idempotency, and error contracts?
- Are external providers bounded, allowlisted, recorded in fixtures, and excluded from normal tests?
- Does `./gradlew check` cover formatting/static analysis, unit tests, architecture rules, and focused integration tests?
- Is each dependency and infrastructure choice justified by a current requirement?
- Is the change traceable to accepted requirement IDs with evidence sufficient to advance their lifecycle?

## Primary References

- [Kotlin coding conventions](https://kotlinlang.org/docs/coding-conventions.html)
- [Spring Framework Kotlin support](https://docs.spring.io/spring-framework/reference/languages/kotlin.html)
- [Spring Boot Kotlin support](https://docs.spring.io/spring-boot/reference/features/kotlin.html)
- [Gradle Kotlin DSL](https://docs.gradle.org/current/userguide/kotlin_dsl.html)
- [Kotest quick start](https://kotest.io/docs/quickstart/)
