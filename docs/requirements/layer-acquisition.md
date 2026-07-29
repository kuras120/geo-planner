# Layer Acquisition Requirements

## Application Area

Bounded retrieval, validation, provenance, progress, and promotion of source
evidence for an accepted project AOI.

## Requirement Index

| ID | Delivery stage | Status | Priority | Capability |
| --- | --- | --- | --- | --- |
| `ACQUIRE-001` | `MVP` | `ACCEPTED` | `MUST` | Acquire selected project layers safely |

## ACQUIRE-001 — Acquire selected project layers safely

- Status: ACCEPTED
- Priority: MUST
- Delivery stage: MVP
- Source evidence: exact public-integration inventory; AOI/raster research;
  owner acquisition-budget and streaming decisions from 2026-07-28.

### Outcome

A user prepares project evidence through an observable acquisition job without
loading a large acquisition into the browser or losing the last valid data.

### Contract

- Input: accepted AOI, selected catalog layers, and 0.5 m/px default,
  validated 0.25 m/px, or explicit 1 m/px resolution.
- Sources: ULDK, configured APP document, ORTO, KIEG, KINA, and KIUT adapters.
- Output: per-layer progress/results and validated immutable artifacts with
  request identity, bbox, CRS, resolution, dates, checksum, and warnings.
- Budgets: 2048² product tiles, 16M pixels/layer, 64 planned tile requests,
  64 MiB/response, and 512 MiB promoted artifacts/acquisition.
- Degraded/failure behavior: never silently coarsen; preserve last valid
  artifacts; expose independent warnings and partial job results.

### Acceptance Criteria

- Upstream bodies stream into bounded temporary storage and only complete,
  validated artifacts are atomically promoted.
- Provider dimension/format/axis rules come from the exact descriptor and
  capabilities evidence; unknown limits use a conservative product cap.
- OGC errors, wrong MIME/signature, timeout, cancellation, partial tile failure,
  and no coverage have distinct results.
- A retry or restart never exposes an incomplete mosaic as ready.
- The frontend observes stages and consumes controlled artifact/tile endpoints
  without buffering or embedding the full acquisition.

### Open Decisions

- Select polling, SSE, or another progress transport with the implementation
  slice.
- Select the exact artifact/tile delivery surface and retention policy.
