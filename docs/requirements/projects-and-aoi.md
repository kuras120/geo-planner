# Projects And AOI Requirements

## Application Area

Project identity, parcel subjects, surrounding context, and bounded spatial
extent. Source-layer acquisition and rendering belong to separate areas.

## Requirement Index

| ID | Delivery stage | Status | Priority | Capability |
| --- | --- | --- | --- | --- |
| `PROJECT-001` | `MVP` | `ACCEPTED` | `MUST` | Create a bounded project area from parcels |

## PROJECT-001 — Create a bounded project area from parcels

- Status: ACCEPTED
- Priority: MUST
- Delivery stage: MVP
- Source evidence: owner decisions from 2026-07-28;
  `docs/research/area-of-interest-and-raster-sizing.md`; sanitized
  single/multi-parcel fixtures.

### Outcome

A user selects one or several parcels and receives one reproducible project
subject plus visible surrounding context without calculating a bbox.

### Contract

- Input: 1–100 full parcel identifiers and a context buffer from 0–500 m,
  defaulting to 100 m.
- Sources: GUGiK ULDK `GetParcelByIdOrNr` through the approved parcel adapter.
- Output: resolved parcel geometries, their union, project CRS, chosen buffer,
  and acquisition extent.
- Degraded/failure behavior: identify unresolved parcels; reject ambiguous
  partial creation and any subject or buffered extent exceeding 2 km width,
  2 km height, or 4 km².

### Acceptance Criteria

- Single- and adjacent multi-parcel fixtures produce deterministic subjects and
  extents in their declared CRS.
- Selected parcels remain subjects; fetched neighbors remain context.
- The user previews the subject, buffer, and extent before acquisition.
- Distant or excessive selections are rejected without a confirmation override
  and direct the user to separate projects.
- Restart preserves the accepted identifiers, geometries, CRS, and buffer.

### Deferred Follow-up

- Expert polygon and bbox input require a separate later requirement covering
  CRS validation, authorization, and user-visible failure behavior. They do not
  expand this parcel-based MVP requirement.
