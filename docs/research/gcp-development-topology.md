# GCP Development Topology

## Status

Owner-requested deployment research recorded on 2026-07-28. The topology is a
recommendation awaiting an explicit database/infrastructure decision; it is not
an implemented environment.

Cost comparison and the recommended local-plus-on-demand operating model are
recorded in `gcp-cost-options.md`.

## Product Stage Versus Deployment

`MVP` describes the basic Geo Planner capabilities, not a restriction that the
application may run only on localhost. The same feature set may have:

- a required local development/self-hosted profile;
- an early private GCP development deployment;
- a later SaaS profile with authentication, tenant ownership, quotas,
  retention, cost controls, and production operations.

Deploying MVP code to GCP does not by itself make the product SaaS-ready.

## State Needed From The First Persisted Project

The first project-creation slice must retain:

- project identity, AOI input/resolved geometry, CRS, and buffer;
- selected catalog layers and presentation preferences;
- acquisition commands, job state, per-layer results, and provenance;
- artifact metadata and object keys;
- overlay feature IDs, collection revision, and metadata;
- import records and schema/storage version.

Raster/COG/tile bytes and large exports are objects, not database rows.

## Recommended Topology

```text
Angular
  -> Firebase Hosting
  -> Firebase Authentication token
  -> Spring Boot/Kotlin on Cloud Run
       -> PostgreSQL persistence port
            -> external scale-to-zero PostgreSQL for intermittent development
            -> Cloud SQL PostgreSQL when same-provider production operation
               is justified
       -> Cloud Storage: COGs, tiles, source snapshots, exports
       -> later CDN and durable job orchestration
```

Local development uses:

- the Node contract simulator for frontend-only journeys;
- Spring Boot plus PostgreSQL in Docker/Testcontainers for real backend slices;
- the local data-root filesystem adapter for artifacts;
- Firebase emulators when authentication or Cloud Storage behavior enters the
  accepted slice.

The persistence ports keep local filesystem/object storage and GCP Cloud Storage
adapters separate from the application/domain model.

## Database Assessment

### PostgreSQL — Recommended Data Model

Strengths:

- matches saved projects, ownership, optimistic revisions, jobs, and manifests;
- standard migrations, constraints, transactions, and Kotlin/Spring support;
- local and managed PostgreSQL share the same core database semantics;
- Cloud SQL, Neon, and Supabase support PostGIS when accepted spatial queries
  later justify it.

Costs:

- Cloud SQL development adds configuration and a standing cost;
- an external scale-to-zero provider reduces idle compute cost but adds
  cross-provider networking, latency, and another operational dependency;
- Cloud Run connection pools and maximum instance counts must be bounded;
- self-hosted/local delivery includes a PostgreSQL container. A future
  single-process package would require a separately accepted embedded database
  adapter rather than file-backed user state.

For intermittent private development, Neon is the leading managed candidate
pending a disposable proof of migrations, PostGIS, Cloud Run connectivity,
pooling, cold starts, latency, backup/restore, and cost reporting. Cloud SQL
remains the conservative hosted-production option when same-provider
networking and operations outweigh its baseline cost.

Supabase PostgreSQL is viable, but its broader Auth, Storage, and API platform
overlaps with the proposed Firebase services. Select it only if that overlap is
intentional rather than an accidental second platform.

### Firestore — Fast Prototype Alternative

Strengths:

- managed/serverless operation and useful Firebase emulator tooling;
- low setup for document-shaped metadata and early prototypes;
- integrates naturally with Firebase identity and client tooling.

Constraints:

- maximum document size is 1 MiB;
- collection/feature modeling, relational integrity, migrations, and complex
  reporting require deliberate document/index design;
- read/write-based cost and query shapes can leak into application design;
- no PostGIS path for later spatial predicates/aggregation;
- choosing it only for development creates a likely persistence migration.

Firestore may still suit small auxiliary documents, but using both databases
without a concrete boundary would add more complexity than value.

## Cloud Run And Artifact Safety

Cloud Run's normal writable container filesystem is in-memory and disappears
when an instance stops. It is temporary workspace only. Acquisition must stream
to bounded temporary space and promote to Cloud Storage; project truth cannot
depend on container files.

Large/long acquisitions may later require Cloud Run Jobs, Cloud Tasks, Pub/Sub,
or another accepted durable orchestration mechanism. This is not selected
before measured job duration and retry requirements exist.

## Recommended Adoption Order

1. Angular foundation and Node contract simulator, no database.
2. Accepted project/AOI slice with Spring Boot and local PostgreSQL
   persistence.
3. Acquisition slice with Cloud Storage artifact adapter and durable records.
4. Disposable external PostgreSQL connectivity/cost proof, with no real owner
   data.
5. Private GCP development deployment on Cloud Run, the accepted PostgreSQL
   provider, and Cloud Storage.
6. Firebase Authentication before the environment accepts public user writes.
7. SaaS tenancy, quotas, retention, billing/cost controls, and durable job
   orchestration as separately accepted slices.

## Open Decision

Choose the persisted-project database:

- PostgreSQL locally plus Cloud SQL in GCP (conservative same-provider option);
- PostgreSQL locally plus an external scale-to-zero managed PostgreSQL
  (leading intermittent-development candidate);
- Firestore/emulator with an accepted future migration risk;
- file/embedded local MVP followed by a later database migration.

Make this decision only with the workload/cost model from
`gcp-cost-options.md`; architecture fit alone is insufficient.

Primary references:

- `https://docs.cloud.google.com/run/docs/container-contract`
- `https://docs.cloud.google.com/sql/docs/postgres/connect-run`
- `https://docs.cloud.google.com/sql/docs/postgres/extensions`
- `https://firebase.google.com/docs/firestore/quotas`
- `https://firebase.google.com/docs/emulator-suite`
- `https://firebase.google.com/docs/auth/admin/verify-id-tokens`
- `https://docs.cloud.google.com/storage/docs/lifecycle`
