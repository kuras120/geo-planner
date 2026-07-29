# Sketches Requirements

## Application Area

Creation, inspection, editing, safe persistence, import, and export of private
user-authored map geometries.

## Requirement Index

| ID | Delivery stage | Status | Priority | Capability |
| --- | --- | --- | --- | --- |
| `SKETCH-001` | `STAGE-2` | `ACCEPTED` | `MUST` | Create and edit a sketch |
| `SKETCH-002` | `STAGE-2` | `ACCEPTED` | `MUST` | Persist and manage sketches safely |
| `SKETCH-003` | `STAGE-2` | `ACCEPTED` | `MUST` | Import and export legacy sketches |

## SKETCH-001 — Create and edit a sketch

- Status: ACCEPTED
- Priority: MUST
- Delivery stage: STAGE-2
- Source evidence: prototype drawing lifecycle and geometry characterization;
  owner drawing decision from 2026-07-28.

### Outcome

A user records and revises an indicative point, path, or area with unambiguous
geometry intent.

### Contract

- Input: point, line, or area mode; map vertices; name and supported metadata.
- Sources: user interaction in the explicit project CRS.
- Output: valid Point, LineString with at least two vertices, or Polygon with
  at least three user vertices and a closed stored ring.
- Degraded/failure behavior: invalid or unfinished input remains a draft until
  fixed or cancelled and never replaces an accepted feature.

### Acceptance Criteria

- Open-line and filled-area previews remain visually distinct.
- Finish button, Enter, and double-click complete supported drafts; Escape
  cancels and point undo removes only the last draft vertex.
- A multi-vertex line remains a line.
- Closing a line may offer conversion but never silently creates a polygon.
- Editing preserves immutable feature identity and reports invalid geometry.

### Open Decisions

- Snapping and advanced vertex-edit gestures belong to the feature-specific
  implementation plan.

## SKETCH-002 — Persist and manage sketches safely

- Status: ACCEPTED
- Priority: MUST
- Delivery stage: STAGE-2
- Source evidence: loopback save/atomic-failure baseline; owner overlay identity
  and concurrency decision from 2026-07-28.

### Outcome

A user can select, rename, edit, delete, or clear private sketches without
silent deduplication or lost concurrent changes.

### Contract

- Input: mutation against an immutable feature ID and current collection
  revision.
- Sources: authoritative backend overlay storage under the configured data
  root.
- Output: a new collection revision and updated feature set.
- Degraded/failure behavior: stale revision rejects the write; storage failure
  preserves the last accepted revision; geometrically identical features remain
  distinct.

### Acceptance Criteria

- Names and geometries never act as identity or automatic replacement keys.
- Restart preserves accepted features, IDs, metadata, CRS, and revision.
- A stale client cannot overwrite a newer edit.
- Delete and clear require explicit confirmation and affect only the intended
  authoritative revision.
- Private feature bodies are not logged or placed in tracked/generated source.

### Open Decisions

- Exact user-facing conflict comparison and merge interaction.

## SKETCH-003 — Import and export legacy sketches

- Status: ACCEPTED
- Priority: MUST
- Delivery stage: STAGE-2
- Source evidence: prototype GeoJSON export and ignored
  `manual-overlays.json`; owner import decision from 2026-07-28.

### Outcome

A user previews and imports legacy sketches into backend storage, and exports a
portable, CRS-qualified collection without modifying the source.

### Contract

- Input: reviewed legacy `manual-overlays.json` or supported exported
  collection.
- Sources: explicit user-selected file; never automatic repository scanning.
- Output: preview, import report, immutable/stable IDs, provenance, and
  CRS-qualified export.
- Degraded/failure behavior: reject unsupported/ambiguous geometry or CRS
  without partial silent import; preserve source and accepted backend state.

### Acceptance Criteria

- Valid existing IDs are preserved; missing IDs receive stable import IDs.
- Importing the same source twice is idempotent.
- Matching name or geometry never silently merges distinct records.
- Reported accepted, skipped, warning, and rejected counts reconcile with the
  preview.
- Export re-import preserves geometry, identity, metadata, and CRS.

### Open Decisions

- Select the fallback workflow for legacy files whose CRS cannot be proven.
