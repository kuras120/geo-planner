# Target Product Architecture

## Status

This document describes the accepted target boundaries for the replacement applications. It is not a claim that the Angular frontend or Kotlin backend already exists. Current runtime behavior remains documented in `map-build-flow.md`.

## System Boundary

Geo Planner evolves from the local Python/HTML prototype into a thin Angular/OpenLayers client backed by a Kotlin/Spring Boot modular monolith:

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
            -> MVP local data directory
            -> later database and object storage
  <- project/layer descriptors, job progress, validated artifacts
```

The frontend owns presentation, OpenLayers rendering, forms, and transient interaction state. The backend owns authoritative projects and overlays, trusted provider configuration, acquisition, validation, caching, provenance, and export assembly.

Normal rendering may use validated backend artifacts or controlled live-layer URLs when a source's CORS, performance, licensing, and CRS behavior are known. Acquisition and reproducible export default to backend-owned snapshots. There is no generic remote-URL proxy.

## Shared Contract Model

The HTTP boundary is versioned through OpenAPI. Transport DTOs remain separate from both Kotlin domain models and Angular view/domain models.

The specification evolves with implemented vertical slices. It is published and regenerated repeatedly during development; it is not a one-time complete design prerequisite. A frontend feature depends only on the accepted contract for its current backend capability.

### Project

A project contains:

- stable ID, name, locale, and privacy classification;
- area-of-interest geometry and acquisition/display CRS;
- selected catalog layer IDs and typed overrides;
- references to immutable acquisition records;
- backend-owned overlay state.

It does not contain executable provider URLs, credentials, filesystem paths, or UI-specific branching.

### Area Of Interest

Supported target inputs are:

- one or more full parcel identifiers;
- a point resolved to a parcel;
- an uploaded or drawn polygon;
- an explicit bbox for expert use.

Resolution returns canonical geometry plus a buffered acquisition bbox. CRS and coordinate order are explicit at every boundary.

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

### Acquisition Job And Record

The target job state machine is:

`QUEUED -> RESOLVING -> DOWNLOADING -> VALIDATING -> READY`

Terminal states are `FAILED` and `CANCELLED`. Per-layer results distinguish required failures from optional warnings. Repeated normalized commands use backend-supported idempotency.

Every promoted artifact records:

- catalog version and capability fingerprint;
- sanitized upstream request identity;
- layer, style, protocol version, format, and response MIME type;
- bbox, CRS, dimensions, and resolution;
- acquisition time, checksum, byte size, and storage key;
- attribution/licence, warnings, job identity, and stale/superseded state.

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

### Local MVP

- Bind the backend to loopback during local development.
- Store projects, jobs, manifests, overlays, and artifacts under one configurable ignored data directory.
- Use temporary files plus atomic promotion.
- Run acquisition through a bounded in-process executor.
- Persist restart-safe state through manifests or a deliberately selected embedded store.
- Import the legacy ignored `manual-overlays.json` without making it tracked data.

### Hosted Single-user Or Test Environment

- Serve frontend and backend through one origin.
- Store large artifacts on a persistent volume or S3-compatible storage.
- Introduce a relational database when durable queryable state requires it.
- Deployment-level authentication may precede product accounts.

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
