# Layer Viewing Requirements

## Application Area

Map navigation, layer visibility/readiness, and safe inspection of current
parcel, planning, and raster evidence. Acquisition belongs to a separate area.

## Requirement Index

| ID | Delivery stage | Status | Priority | Capability |
| --- | --- | --- | --- | --- |
| `LAYER-001` | `MVP` | `ACCEPTED` | `MUST` | Open and control project evidence layers |
| `LAYER-002` | `MVP` | `ACCEPTED` | `MUST` | Inspect a parcel |
| `LAYER-003` | `MVP` | `ACCEPTED` | `MUST` | Inspect planning zones and OUZ |
| `LAYER-004` | `MVP` | `ACCEPTED` | `MUST` | Read raster evidence safely |

## LAYER-001 — Open and control project evidence layers

- Status: ACCEPTED
- Priority: MUST
- Delivery stage: MVP
- Source evidence: prototype layer/interaction inventory, characterization
  tests, owner layer-default and readiness decisions from 2026-07-28.

### Outcome

A user opens a project, navigates its map, and independently controls every
available evidence layer while seeing whether each layer is usable.

### Contract

- Input: a valid project and server-owned layer descriptors/results.
- Sources: project API, source catalog, and validated layer artifacts.
- Output: pan/zoom/reset map, layer controls, persisted visibility preferences,
  and compact readiness/provenance cards.
- Degraded/failure behavior: show loading, no coverage, failed, unavailable, or
  stale state without rendering a silent blank success.

### Acceptance Criteria

- Ortho, parcels, EGiB, and planning zones start visible; land classes, OUZ,
  addresses, and utilities start hidden.
- Later visibility choices persist for the project/user.
- Mouse and keyboard controls work at desktop and narrow widths.
- Failure of one evidence layer does not block an otherwise valid project.
- Each card shows provider, dataset/layer, acquisition/document date, CRS,
  extent, attribution, and warning; technical details are expandable.

### Open Decisions

- Whether opacity and user-controlled layer reordering belong to MVP.

## LAYER-002 — Inspect a parcel

- Status: ACCEPTED
- Priority: MUST
- Delivery stage: MVP
- Source evidence: ULDK parcel workflow; prototype map/list/label selection;
  keyboard characterization.

### Outcome

A user selects a subject or context parcel and sees its qualified identity and
source evidence without confusing configured notes with official attributes.

### Contract

- Input: click, keyboard activation, or list selection of a normalized parcel.
- Sources: GUGiK ULDK geometry/identity plus explicit project role.
- Output: selected geometry, parcel number, subject/context role, provider, and
  resolution/acquisition metadata.
- Degraded/failure behavior: missing optional attributes remain absent and are
  never inferred from owner notes or stale calculated percentages.

### Acceptance Criteria

- Geometry, label, and list select the same parcel with visible emphasis.
- Enter and Space activate focusable map/list targets.
- Source attributes, derived values, and user-authored metadata are visibly
  distinct.
- Selection survives ordinary layer toggling and map navigation.

### Open Decisions

- Whether geometry-derived parcel area is an MVP inspection field.

## LAYER-003 — Inspect planning zones and OUZ

- Status: ACCEPTED
- Priority: MUST
- Delivery stage: MVP
- Source evidence: configured APP GML workflow, XY/YX fixtures, prototype
  planning parser and layer inventory.

### Outcome

A user displays and selects planning zones or OUZ and can tell what the feature
means and which planning document supplied it.

### Contract

- Input: a project AOI and normalized APP `StrefaPlanistyczna` or
  `ObszarUzupelnieniaZabudowy` feature.
- Sources: exact configured APP GML document and adapter version.
- Output: geometry, type, symbol/designation when present, document identity,
  date/status, CRS, and warning.
- Degraded/failure behavior: distinguish no coverage, absent feature type,
  parse omission, unsupported geometry, and source failure.

### Acceptance Criteria

- Both sanitized axis-order fixtures render planning geometry in the expected
  location.
- Selection exposes feature and document provenance.
- Complex geometry rejected or simplified by an adapter produces an explicit
  warning rather than silent omission.
- The UI never presents planning preview as a building-right determination.

### Open Decisions

- Exact normalization of adopted, draft, and unknown APP document status.

## LAYER-004 — Read raster evidence safely

- Status: ACCEPTED
- Priority: MUST
- Delivery stage: MVP
- Source evidence: current ORTO, KIEG, KINA, and KIUT request inventory; owner
  provenance/readiness decisions; official capabilities checked 2026-07-28.

### Outcome

A user visually compares current raster evidence with parcels and planning data
while understanding its coverage, currency, and preview-only limitations.

### Contract

- Input: validated artifacts for ORTO `Raster`; KIEG
  `budynki,numery_dzialek` and `uzytki,kontury`; KINA
  `prg-adresy,prg-ulice,prg-place`; and KIUT power/water/sewer layers.
- Sources: allowlisted GUGiK WMS descriptors and exact acquisition records.
- Output: aligned map imagery plus compact per-layer provenance/readiness.
- Degraded/failure behavior: retain usable layers and distinguish no coverage,
  stale artifact, provider failure, and unsupported source.

### Acceptance Criteria

- Artifact bbox, CRS, dimensions, and resolution match its displayed extent.
- Representative control points align on both spatial fixtures.
- A raster pixel never pretends to identify a building, land class, address,
  or utility feature.
- Land-class rasters never produce authoritative area percentages.
- Utility and cadastral previews retain their uncertainty warnings.

### Open Decisions

- Which accepted legends or queryable/vector sources later supplement each
  raster preview.
