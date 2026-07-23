# Productization And Generic Map Workflow

## Status

- Phase: PROPOSED
- Created: 2026-07-20
- Authorization: planning and research only; no private-data deletion, history rewrite, source refresh, or frontend implementation is included.

## Problem And Outcome

The repository mixes reusable map code, one real property case, downloaded evidence, generated exports, and assumptions about a fixed set of Polish WMS layers. Configuration exists, but changing a bbox is not enough to create a safe and correct new project. The inline HTML application also couples UI, GIS logic, and persistence.

The outcome is a reusable Geo Planner product in which a user can create a private project for another area, select an area by parcel/point/polygon, discover and acquire compatible layers, validate provenance and alignment, edit sketches, and export a reproducible view without changing application code.

## Scope And Non-goals

In scope:

- separate public product code from private project workspaces and generated artifacts;
- define generic project, area, source, layer, snapshot, and overlay contracts;
- make raster/vector acquisition descriptor-driven and capability-aware;
- support arbitrary Polish areas and appropriate CRS selection/reprojection;
- migrate the browser UI incrementally to Angular + TypeScript + OpenLayers;
- preserve an explicit offline workflow, provenance, uncertainty, and spatial verification;
- provide a sanitized synthetic demo and migration tools for existing projects.

Non-goals for the first implementation:

- legal, cadastral, planning, or utility certainty;
- nationwide mirroring of public datasets;
- collaborative cloud accounts or multi-user synchronization;
- changing official source data or silently refreshing checked-in evidence;
- immediate replacement of every Python component with a web backend.

## Confirmed Decisions

- The reusable application and real analysis data have separate publication boundaries.
- Source refresh remains explicit and is never part of offline verification.
- `manual-overlays.json` is user data and will not be modified or migrated without explicit owner authorization.
- The frontend target is Angular + TypeScript + OpenLayers; OpenLayers is accessed through an application-owned adapter.
- Existing Python acquisition logic is retained initially, then split into reusable domain/source adapters and CLI orchestration.
- Layer UI is generated from data descriptors; standard layer IDs such as `ortho` or `water` are catalog defaults, not validator requirements.
- Every downloaded snapshot records provenance and the bbox/CRS for which it is valid.
- The MVP may keep public parcel/precinct identifiers, official geometry, coordinates, and raster previews. Personal/legal context and manual overlays stay outside tracked files.

## Assumptions And Open Questions

Assumptions:

- Poland is the initial geographic scope, so EPSG:2180 is a useful nationwide acquisition/storage default where a service supports it; frontend display CRS remains configurable.
- A project may be private even if all upstream services are public.
- Live services and reproducible offline snapshots are both valuable and should use the same layer descriptor.

Open decisions before implementation:

1. Should private projects live in an ignored `workspace/` directory or in a separate external directory by default?
2. Is live WMS viewing required in the first Angular release, or is snapshot-only parity sufficient?
3. Which sources and derived snapshots may legally be redistributed, and with what attribution?
4. Is a local HTTP acquisition service required, or should the first version expose only CLI commands?

## Target Contracts

### Project

A project contains identity, privacy classification, area-of-interest geometry, preferred display/storage CRS, selected layer descriptors, private annotations, and references to immutable acquisition records. It does not contain hard-coded knowledge of particular UI controls.

### Area Of Interest

An area can be supplied as:

- one or more full parcel identifiers;
- a point used to resolve a parcel through ULDK;
- an uploaded/drawn polygon;
- an explicit bbox for expert use.

The resolver returns canonical geometry plus a buffered acquisition bbox. ULDK supports lookup by parcel identifier, name, or point and can return geometry in a requested SRID; see the [official ULDK API description](https://uldk.gugik.gov.pl/opis.html).

### Source And Layer Descriptor

Each catalog entry declares:

- stable catalog ID and human label;
- kind: `wms`, `wmts`, `xyz`, `vector-http`, `local-vector`, or later `cog`;
- endpoint and capability-discovery policy;
- candidate layer names/styles and required/optional status;
- supported purpose, attribution, licence note, and uncertainty warning;
- preferred formats, CRS rules, request limits, and axis-order behavior;
- live, snapshot, or both acquisition modes;
- adapter-specific parsing rules, never UI-specific branching.

Project configuration selects catalog entries and may supply typed overrides. It does not duplicate service implementation details unless needed for reproducibility.

### Acquisition Record

Every snapshot records source/catalog version, resolved URL excluding secrets, selected layer/style, WMS/WMTS version, request bbox, CRS, dimensions/resolution, acquisition time, response MIME type, checksum, local file, attribution/licence, and capability-document fingerprint. This record is the authority for whether a raster still matches a changed project.

## Generic Raster Acquisition Flow

```text
area input
  -> resolve geometry and buffered bbox
  -> choose project/acquisition CRS
  -> load source descriptor
  -> fetch and parse GetCapabilities
  -> match layer, style, format and supported CRS
  -> tile/chunk request when service limits require it
  -> validate HTTP, MIME type and OGC exception response
  -> persist georeferenced snapshot + acquisition record
  -> verify extent/resolution/checksum
  -> expose layer dynamically in the frontend
```

The adapter must account for WMS version and coordinate-axis rules rather than relying on a single global `wms130AxisOrder` flag. `GetCapabilities`, `GetMap`, and optional `GetFeatureInfo` are standard WMS operations; see the [OGC WMS standard](https://www.ogc.org/standards/wms/). Capability results should be cached with expiry and fingerprinting, because layer names and supported formats can change.

Snapshot validation must reject HTML/XML error documents saved as images, OGC `ServiceException` responses, empty or uniform unexpected tiles, incompatible CRS, and dimensions outside service limits. Large extents should use tiled requests with deterministic mosaicking. Prefer GeoTIFF/COG or an image plus explicit georeferencing metadata over an anonymous PNG whose bbox exists only in unrelated configuration.

## Affected Components And Migration

| Current area | Required change |
| --- | --- |
| `project-config.json` | Versioned schema; privacy and AOI model; references to catalog entries and acquisition records. |
| `update_sources.py` | Split into source adapters, capability parser, request planner, validator, storage, and CLI. Remove required fixed layer IDs. |
| `build_map.py` | Consume generic layer arrays and manifests; later become an export path rather than the primary UI builder. |
| HTML template | Keep only during parity migration; replace with Angular/OpenLayers features. |
| manual overlays | Introduce versioned overlay schema and explicit import; preserve original user file until accepted. |
| `sources/` and `assets/` | Move under private project workspace; store provenance beside each snapshot. |
| tests | Add schema, adapter, capabilities, CRS/axis-order, error-response, migration, and visual-control fixtures. |
| repository | Track only code, schemas, safe fixtures, and synthetic demo; ignore private workspaces and exports. |

Compatibility should be implemented as an explicit importer from the current configuration/overlay format. The application should never guess whether a legacy file is safe to publish.

## Implementation Plan

1. [pending] **Contain exposure.** Amend the confirmed unpushed local commit with the sanitized snapshot, verify its diff from `origin/master`, and avoid tracking local overlays/exports.
2. [pending] **Create the product/data boundary.** Add ignored project-workspace conventions, a synthetic demo, safe export rules, and repository checks that reject real-project/generated content in public paths.
3. [pending] **Specify versioned contracts.** Add JSON Schemas and typed examples for project, AOI, source catalog, layer selection, acquisition record, and overlays. Document migrations and privacy classification.
4. [pending] **Extract a Python core.** Separate configuration/domain validation from CLI commands and from individual ULDK, WMS, WMTS, GML, and file adapters.
5. [pending] **Implement capability-aware acquisition.** Parse/cache capabilities, negotiate version/CRS/format/style, plan tiled downloads, validate responses, store georeferencing and provenance, and make optional-layer failure non-destructive.
6. [pending] **Generalize vectors and AOI creation.** Resolve parcels/points/polygons, normalize geometry, support declared vector parsers, and eliminate hard-coded plan feature-type assumptions where schema descriptors suffice.
7. [pending] **Build Angular/OpenLayers read-only parity.** Load the generic demo, register projections, render catalog-driven raster/vector layers, and implement layer ordering, opacity, legends, selection, and warnings.
8. [pending] **Port editing and persistence.** Add typed sketch tools, snap/modify/undo, project-scoped persistence, legacy overlay import, and clear private/share export modes.
9. [pending] **Integrate acquisition workflow.** Start with CLI status/manifests; add a loopback API only if browser-triggered refresh/CORS/progress requirements are approved.
10. [pending] **Spatial parity and cutover.** Compare old/new output at known control points across multiple CRSs and source variants, migrate the private project, retire the inline HTML runtime, and update durable docs.
11. [pending] **Verify publication history.** Confirm the sanitized commit is the only branch commit ahead of `origin/master`; rewrite pushed history only if a separate audit finds private case data there.

## Failure And Safety Behavior

- Failed acquisition never replaces the last valid snapshot.
- A changed AOI or CRS marks incompatible snapshots stale and hides them by default.
- Missing optional layers produce visible warnings; missing required layers block a reproducible export.
- Capability drift requires a new acquisition record and operator-visible diff.
- Geometry parsing never silently swaps coordinate order; ambiguous input is rejected.
- Public export excludes private annotations and source files unless the user selects an explicit reviewed profile.
- The UI preserves source date, attribution, uncertainty, and preview-only status.
- Offline verification uses fixtures and must not contact or mutate external sources.

## Verification And Acceptance

Automated gates:

- JSON Schema validation and migrations for legacy/current fixtures;
- unit tests for bbox, buffering, CRS negotiation, axis order, URL creation, chunking, mosaicking, and checksums;
- recorded capability/exception fixtures for representative WMS 1.1.1, WMS 1.3.0, WMTS, ULDK, and plan GML paths;
- integration test proving that a failed refresh preserves the prior snapshot;
- frontend component/service tests plus browser tests for layer, inspection, and sketch workflows;
- repository privacy gate scanning tracked files and generated manifests from a clean clone;
- `./scripts/verify.sh` remains offline and deterministic throughout migration.

Manual spatial checks:

- at least two geographically separate projects and two CRS/axis-order combinations;
- parcel, orthophoto, EGiB, planning, and utility alignment at recognizable control points;
- GetFeatureInfo/selection correspondence with visible features;
- imported overlays retain geometry and properties exactly;
- offline export reproduces the accepted viewport without network access;
- clean public demo contains no real names, private legal context, or local paths.

Acceptance criteria:

- a new area can be configured and acquired without editing Python, TypeScript, or HTML;
- adding a compatible source requires a descriptor or isolated adapter, not changes across UI/build validation;
- every raster can prove its bbox, CRS, source, timestamp, and checksum;
- private project data and generated exports are excluded from the public repository by default;
- the Angular application provides functional parity before the old runtime is removed;
- a reviewed clean clone passes both technical and privacy gates.

## Result

- Research and implementation proposal prepared; implementation has not started.
- Privacy details are recorded in `docs/research/privacy-and-data-separation-audit.md`.
- Frontend evidence and recommendation are recorded in `docs/research/frontend-technology-options.md`.
