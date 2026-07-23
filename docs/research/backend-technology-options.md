# Backend Technology Options

## Status

Decision research for a future owner-implemented backend. This document selects
a direction; it is not an implementation plan.

## Recommendation

Use Kotlin, Spring Boot, Spring MVC, Gradle Kotlin DSL, and Kotest for the first
backend slice.

This choice combines the desired Kotlin learning path with mature HTTP,
validation, security, observability, and persistence integrations. It leaves
room for PostgreSQL or asynchronous messaging only when a concrete requirement
creates that need.

Durable coding rules belong to
`docs/guidelines/kotlin-backend-engineering-guide.md`; system boundaries and
contracts belong to `docs/architecture/target-product-architecture.md`.

## Framework Comparison

| Option | Strengths | Main trade-off | Assessment |
| --- | --- | --- | --- |
| Spring Boot + Spring MVC | Mature ecosystem, explicit request model, strong Security/Data support, common commercial stack | Framework surface is large | Recommended |
| Ktor | Kotlin-first, small and explicit, coroutine-friendly | More application conventions and integrations must be assembled | Good alternative for a deliberately small service |
| Spring WebFlux | Reactive streams and non-blocking stack | Higher semantic and testing complexity | Introduce only for measured concurrency or streaming needs |

## Infrastructure Adoption Triggers

| Technology | Introduce when |
| --- | --- |
| PostgreSQL | Durable shared state, user accounts, saved projects, audit history, or spatial querying becomes a requirement |
| Spring Security | Authentication, authorization, tenant isolation, or protected write operations enter scope |
| RabbitMQ or another broker | Work must survive request boundaries, be retried independently, or fan out to consumers |
| PostGIS | Server-side spatial predicates, indexing, transformations, or aggregation are justified |
| Object storage | Rasters, exports, or large source artifacts must be shared or retained outside one process |

Do not add these technologies merely to demonstrate them. Each addition needs
an accepted requirement, an operational owner, and a verification strategy.

## Open Decisions for the First Backend Feature

Resolve these in the feature-specific plan:

- supported JDK and compatible Spring Boot/Kotlin versions;
- package and module boundaries implied by the first business capability;
- exact OpenAPI ownership and generation direction;
- upstream timeout, retry, cache, and error-normalization policy;
- whether the first slice has durable state;
- the smallest security boundary required by exposed operations.

## Primary References

- [Kotlin documentation](https://kotlinlang.org/docs/home.html)
- [Spring Boot documentation](https://docs.spring.io/spring-boot/)
- [Spring Framework reference](https://docs.spring.io/spring-framework/reference/)
- [Gradle Kotlin DSL primer](https://docs.gradle.org/current/userguide/kotlin_dsl.html)
- [Kotest documentation](https://kotest.io/docs/)
