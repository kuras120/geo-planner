# Target Product Architecture

## Status

This document describes the accepted target boundaries for the replacement applications. It is not a claim that the Angular frontend or Kotlin backend already exists. Current runtime behavior remains documented in `map-build-flow.md`.

## System Boundary

Geo Planner evolves from the local Python/HTML prototype into a thin
Angular/OpenLayers client backed by one Kotlin/Spring Boot application:

```text
thin Angular/OpenLayers client
  -> same-origin Geo Planner API
       -> project and source-catalog services
       -> area-of-interest resolver
       -> acquisition job orchestrator
            -> ULDK adapter
            -> WMS/WMTS adapter
            -> planning/vector HTTP adapter
       -> snapshot validator and provenance writer
       -> persistence ports
            -> RuntimeStateStore
                 -> local PostgreSQL container
                 -> hosted managed PostgreSQL
            -> ArtifactStore
                 -> local filesystem
                 -> hosted GCS/S3-compatible object storage
  <- project/layer descriptors, job progress, validated artifacts
```

The frontend owns presentation, OpenLayers rendering, forms, and transient interaction state. The backend owns authoritative projects and overlays, trusted provider configuration, acquisition, validation, caching, provenance, and export assembly.

## Frontend Technology Decision

Angular was selected because it matches the owner's experience and provides a
coherent structure for an application expected to grow beyond one map page.
OpenLayers is used directly behind application-owned adapters because the
product needs WMS, multiple projections, raster and vector rendering, editing,
and explicit control of map behavior. An Angular wrapper would add another
compatibility boundary without owning those spatial requirements.

React remained viable but did not provide a benefit that justified defining
more application conventions locally. MapLibre GL JS becomes worth
re-evaluating if vector tiles replace WMS, mixed projections, and raster
evidence as the dominant workload. SvelteKit was not selected because its
smaller alignment with the owner's experience and established application
conventions outweighed its component brevity. The generated HTML application
remains migration evidence and a legacy runtime, not a target frontend.

Reassess this decision only if the dominant map delivery model changes, a
mobile-native client becomes a primary requirement, the application proves
permanently too small for Angular, or OpenLayers loses a required spatial
capability.

## Backend Technology Decision

The backend uses Kotlin, Spring Boot, Spring MVC, Gradle Kotlin DSL, and Kotest.
Spring MVC is the simplest model that satisfies the current HTTP contracts and
blocking provider and persistence integrations. Ktor remained viable but would
require more application conventions and integrations to be assembled locally.
WebFlux is not justified by the present workload; reassess it only when measured
concurrency or streaming behavior cannot be handled clearly and safely with the
current model.

The application is not currently organized or described as a modular
monolith. Keep capability boundaries clear in code, but introduce explicitly
enforced domain modules only when several distinct domains and their dependency
boundaries create a demonstrated need. Do not create empty modules in
anticipation of that growth.

Spring Security, PostGIS, a message broker, or other infrastructure enters the
architecture only with an accepted requirement, an operational owner, and a
verification strategy. The build and pinned toolchain own exact JDK, Kotlin,
Spring, Gradle, and test-library versions.

PostgreSQL state and filesystem/object artifact storage are adapters behind
deployment-neutral
`RuntimeStateStore` and `ArtifactStore` ports. Domain and application services
never branch on the provider or expose paths or bucket keys as product
identity. Local and self-hosted profiles use PostgreSQL plus filesystem
artifacts. A commercial deployment keeps PostgreSQL semantics and replaces only
the artifact adapter with object storage, without changing project,
acquisition, provenance, overlay, or frontend API contracts. Exact port
semantics and migration safety are defined in
[Local Artifact Data Root Contract](local-data-root.md).

Normal rendering may use validated backend artifacts or controlled live-layer URLs when a source's CORS, performance, licensing, and CRS behavior are known. Acquisition and reproducible export default to backend-owned snapshots. There is no generic remote-URL proxy.

## Shared Contract Model

The HTTP boundary is versioned through OpenAPI. Transport DTOs remain separate from both Kotlin domain models and Angular view/domain models.

The specification evolves with implemented vertical slices. It is published and regenerated repeatedly during development; it is not a one-time complete design prerequisite. A frontend feature depends only on the accepted contract for its current backend capability.

Contract discovery for a slice is frontend-led but jointly accepted. The
frontend implementation agent first describes user actions/states, exact data
needs, frontend domain/view models, and representative commands, responses, and
problems. The owner reviews that proposal and implements the accepted
Kotlin/OpenAPI contract. The frontend implementation agent then generates the
client and implements the Angular feature. UI needs inform the transport use
case but never become backend persistence models or authorize speculative
endpoints.

### Project

A project contains:

- stable ID, name, locale, and privacy classification;
- area-of-interest geometry and acquisition/display CRS;
- selected catalog layer IDs and typed overrides;
- references to immutable acquisition records;
- backend-owned overlay state.

It does not contain executable provider URLs, credentials, filesystem paths, or UI-specific branching.

An invalid or unresolved AOI blocks project creation. Once its AOI is valid, the
project remains usable when an individual source layer is unavailable. Layer
readiness is independent and distinguishes loading, ready, no coverage, failed,
and stale results; failures remain visible rather than appearing as blank
successful layers.

The initial MVP presentation shows ortho, subject parcels, EGiB, and planning
zones. Land classes, OUZ, addresses, and utility layers start hidden. Later
visibility choices are project/user preferences rather than a global template
constant.

### Area Of Interest

Supported target inputs are:

- one or more full parcel identifiers;
- a point resolved to a parcel;
- an uploaded or drawn polygon;
- an explicit bbox for expert use.

Resolution returns canonical geometry plus a buffered acquisition bbox. CRS and coordinate order are explicit at every boundary.

The visible default context buffer is 100 metres. A project may deliberately
set it from 0 to 500 metres and persists the selected value. Resolution shows
the resulting extent before acquisition. The selectable range is not an
override: hard subject and acquisition budgets may reject a buffered extent or
require a smaller value.

Before buffering or acquisition, the backend rejects a normalized AOI whose
envelope exceeds server-owned limits for width, height, area, parcel separation,
estimated pixels, bytes, or requests. These hard limits cannot be overridden by
user confirmation or expert bbox input. Distant parcel groups must become
separate projects rather than one nationwide-scale acquisition.

The initial local-MVP profile permits at most 2 kilometres of envelope width,
2 kilometres of envelope height, 4 square kilometres of envelope area, and 100
selected parcels. It is evaluated against both the normalized subject and the
buffered acquisition extent. A different deployment may raise the profile only
after explicit provider, load, and storage validation; it is never a
user-overridable project field.

### Source And Layer Descriptor

Each server-owned catalog entry declares:

- stable source/layer IDs and Polish display labels;
- protocol kind such as `wms`, `wmts`, `xyz`, `vector-http`, `local-vector`, or later `cog`;
- allowlisted endpoint and capability-discovery policy;
- candidate upstream layers/styles and required/optional status;
- attribution, licence note, purpose, and uncertainty warning;
- accepted MIME types, formats, CRS/axis rules, request limits, and delivery modes;
- isolated adapter-specific parsing behavior.

Projects select catalog IDs. User input never becomes an unrestricted fetch URL.

### Layer Presentation And Inspection

Every MVP layer exposes a compact provenance card containing:

- readiness state;
- provider and dataset/layer identity;
- acquisition time or source-document date;
- CRS and covered extent;
- attribution and the applicable uncertainty or preview warning.

Only queryable or normalized vector sources expose feature-level details such
as parcel number or planning-zone symbol. A rendered WMS pixel does not imply
identification of a building, land class, address, or utility feature. Exact
request parameters, artifact dimensions, resolution, checksum, and other
diagnostic metadata remain available through expandable technical details
rather than dominating the normal map interface.

### Sketch Geometry Interaction

Sketch creation begins with explicit point, line, or area intent. A line has at
least two vertices and may have more without becoming an area. An area has at
least three user vertices and closes only when drawing finishes. Open-line and
filled-area previews remain visually distinct throughout the interaction.

The frontend supports an explicit finish action plus Enter or double-click,
Escape to cancel the current draft, and point undo. Attempting to close a line
at its first vertex may offer an intentional conversion to an area, but vertex
count or visual closure never changes the geometry type silently.

### Overlay Identity And Concurrency

The backend assigns every overlay feature an immutable ID. A feature name,
label, or serialized geometry is content, not identity. Geometrically identical
features are legal because they may represent different user intent; the
application may warn about similarity but never silently merges them.

Overlay collection replacement carries an optimistic revision precondition.
When the authoritative revision has changed, the API rejects the stale write
and returns enough current-version context for an explicit reload or conflict
workflow instead of overwriting newer state.

Legacy overlay import is explicit and produces a preview and result report. It
preserves valid existing IDs, assigns stable import IDs when absent, and is
idempotent when the same source file is imported again. It never treats a
matching name or geometry as permission to replace another feature.

### Acquisition Job And Record

The target job state machine is:

`QUEUED -> RESOLVING -> DOWNLOADING -> VALIDATING -> READY`

Terminal states are `FAILED` and `CANCELLED`. Per-layer results distinguish required failures from optional warnings. Repeated normalized commands use backend-supported idempotency.

Acquisition failure for one source layer does not make an otherwise valid
project unusable. A completed job may expose usable artifacts together with
explicit per-layer warnings. Project creation is blocked by AOI/parcel
resolution failure, not by failure of an independently readable evidence
layer.

Every promoted artifact records:

- catalog version and capability fingerprint;
- sanitized upstream request identity;
- layer, style, protocol version, format, and response MIME type;
- bbox, CRS, dimensions, and resolution;
- acquisition time, checksum, byte size, and storage key;
- attribution/licence, warnings, job identity, and stale/superseded state.

The initial local-MVP raster profile defaults to 0.5 m/px. A descriptor may
offer 0.25 m/px only when the selected coverage supports it and the smaller AOI
fits the budget; 1 m/px is an explicit lower-cost choice. The planner uses
2048 × 2048 product tiles and permits at most 16 million pixels per layer, 64
planned tile requests, 64 MiB per upstream response, and 512 MiB of promoted
artifacts per acquisition. It never silently coarsens the accepted resolution.

Upstream response bodies are streamed to bounded temporary storage rather than
buffered in process memory. The job reports per-layer resolving, downloading,
validating, and ready/failure progress. Only validated complete artifacts are
atomically promoted. The frontend observes progress and consumes controlled
artifact or tile endpoints; it never downloads the whole acquisition into
memory or embeds it in the application document. The exact progress transport
and delivery endpoint shape are selected with the acquisition vertical slice.

## Proposed HTTP Surface

This surface is a contract proposal to be accepted incrementally by the frontend owner and backend implementer:

| Endpoint | Purpose |
| --- | --- |
| `GET /api/source-catalog` | Return approved layers, capability status, attribution, and warnings. |
| `POST /api/areas/resolve` | Resolve parcel, point, polygon, or bbox input into canonical AOI geometry. |
| `POST /api/projects` | Create a project from validated metadata and AOI. |
| `GET /api/projects/{projectId}` | Return project metadata and acquisition/layer references. |
| `POST /api/projects/{projectId}/acquisitions` | Start an idempotent acquisition job. |
| `GET /api/acquisitions/{jobId}` | Return progress, per-layer results, and terminal state. |
| `DELETE /api/acquisitions/{jobId}` | Request cancellation when supported. |
| `GET /api/artifacts/{artifactId}` | Stream an authorized validated artifact. |
| `GET/PUT /api/projects/{projectId}/overlays` | Read or atomically replace versioned overlay state. |

API evolution must preserve explicit errors, warnings, provenance, correlation identifiers, nullability, and compatibility rules.

## Generic Acquisition Flow

```text
validated AOI + selected catalog layer
  -> load allowlisted descriptor
  -> fetch/cache/parse capabilities
  -> select version, layer, style, format, and CRS
  -> normalize bbox and protocol-specific axis order
  -> split requests under provider limits
  -> stream chunks to bounded temporary storage
  -> validate status, MIME, signature, dimensions, and OGC errors
  -> mosaic/reproject only through an explicit spatial operation
  -> checksum and atomically promote
  -> persist acquisition record
  -> expose the artifact to the frontend
```

WMS version and axis order are protocol decisions, not one global flag. Large extents require deterministic chunking. Prefer a georeferenced format such as GeoTIFF/COG or explicit sidecar metadata over an anonymous image whose bbox lives elsewhere.

## Persistence Evolution

Delivery stage and deployment profile are separate. `MVP` identifies the basic
Geo Planner capabilities; the same slice can run locally and in a private cloud
development environment. A cloud deployment becomes SaaS only after accepted
identity, ownership, quotas, retention, cost, and operational boundaries.

### Local MVP

- Bind the backend to loopback during local development.
- Run PostgreSQL in Docker for projects, AOI state, jobs, manifests, overlays,
  revisions, imports, and storage-schema version.
- Store only artifact/export bytes and acquisition temporary files under the
  configurable ignored directory defined by
  [Local Artifact Data Root Contract](local-data-root.md).
- Use temporary files plus atomic promotion.
- Run acquisition through a bounded in-process executor.
- Persist restart-safe user state through versioned PostgreSQL migrations and
  transactions.
- Import the legacy ignored `manual-overlays.json` without making it tracked data.

By the first persisted project slice, durable state includes project/AOI input
and resolution, selected layers/preferences, acquisition/job/provenance
records, artifact references, overlay IDs/revisions, imports, and storage
schema version. Large raster/export bytes remain artifact files/objects rather
than database values.

The artifact port supports bounded streaming, abort, complete-only promotion,
metadata/stat, ranged reads, authorized delivery, and deletion by opaque key.
The state port preserves transactions or equivalent atomic revision semantics.
An adapter may implement promotion differently—atomic filesystem rename
locally versus temporary object plus manifest transition in object storage—but
callers observe the same complete-or-not-visible contract.

### Hosted Single-user Or Test Environment

- Serve frontend and backend through one origin.
- Store large artifacts in quota-controlled S3-compatible/object storage or an
  equivalent artifact service; do not accumulate multi-gigabyte user archives
  on the application server filesystem.
- Introduce a relational database when durable queryable state requires it.
- Deployment-level authentication may precede product accounts.

Browser OPFS/IndexedDB/Cache storage may later provide a bounded,
reconstructible offline or hot-tile cache. It is not authoritative project,
overlay, manifest, or acquisition-record storage because browser quota,
eviction, origin, and site-data-clearing behavior is outside backend control.

### Accounts And Multi-user Cloud

- Add Spring Security and explicit ownership.
- Use PostgreSQL for metadata and PostGIS only for justified server-side spatial queries.
- Add quotas, retention, audit events, and signed artifact access.
- Separate workers or introduce a broker only when in-process jobs no longer meet reliability or scaling needs.

## Security And Reliability

- Allowlist provider scheme, host, port, and path; revalidate redirects and reject private/link-local destinations.
- Bound timeouts, redirects, response bytes, raster dimensions, concurrency, and temporary storage.
- Never derive filesystem paths or upstream URLs directly from project input.
- Failed or partial refresh never replaces the last valid artifact.
- Mark artifacts stale after incompatible AOI or CRS changes.
- Reject ambiguous coordinate order rather than guessing.
- Redact secret-classified query parameters and never log overlay bodies.
- Keep source date, attribution, uncertainty, and preview-only status visible.
- Keep automated tests and normal builds independent of live services.

## Migration Boundaries

| Legacy area | Target |
| --- | --- |
| `project-config.json` | Versioned project/AOI/catalog and acquisition contracts. |
| `update_sources.py` | Behavioral reference, then Kotlin provider adapters. |
| `build_map.py` | Transition comparison/export tool, then legacy-only path. |
| inline HTML template | Feature-by-feature Angular/OpenLayers replacement. |
| `manual-overlays.json` | Explicit legacy import into backend-owned overlay storage. |
| `sources/`, `assets/` | Configurable ignored runtime data; only intentional fixtures remain tracked. |

The prototype stays available until contract, functional, privacy, overlay, and
spatial parity are accepted for representative locations and CRS/axis-order
combinations. Migration remains feature-by-feature; its reusable delivery rules
belong to the Angular engineering guide and each implementation increment gets
an owner-approved, feature-specific project plan.
