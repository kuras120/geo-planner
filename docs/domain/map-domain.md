# Map Domain

## Purpose And Safety Boundary

Geo Planner combines selected parcel geometries, planning data, raster previews, and owner-authored sketches in one local interactive map. It supports exploration and communication. It does not replace an extract from the land register, a planning decision, a utility survey, a boundary survey, or legal due diligence.

Every displayed statement has one of three evidence classes:

- source data: downloaded from a named external service on a known date;
- project metadata: an owner-supplied classification or note in `project-config.json`;
- manual overlay: an indicative geometry drawn or imported by the user.

The interface must not blur these classes. Unverified ownership, access, utility, or development claims remain qualified in their status or description.

## Project Contract

`mapa/project-config.json` is the single source of project-specific build and acquisition settings:

- `projectId` is a stable lowercase identifier and namespaces browser storage;
- `title`, `description`, `locale`, and `sourceNote` define project-facing text;
- `outputFile` names the standalone generated map;
- `crs`, `bbox`, `wms130AxisOrder`, and `rasterSize` define the spatial frame;
- `precinctId` and `parcels` define ULDK requests and parcel metadata;
- `plan` identifies the GML file, schema namespace, source date, and coordinate order;
- `services` and `rasters` define acquisition endpoints and local raster paths.

`mapa/map-config.json` owns presentation only. It must not contain the bbox, CRS, parcel identity, source URLs, or facts about a property.

## Spatial Invariants

- Coordinates embedded in the current map, source parcel files, manual overlays, and raster footprint must use the configured CRS.
- `bbox` uses `[minX, minY, maxX, maxY]` regardless of WMS axis order.
- `wms130AxisOrder` controls request serialization, not the internal coordinate model.
- `plan.coordinateOrder` describes pairs in `gml:posList`; the builder normalizes them to `[x, y]`.
- Raster files do not carry georeferencing in the HTML. Each is stretched over the configured bbox and must be refreshed after bbox or CRS changes.
- Parcel numbers and source filenames are unique inside one project.
- A new `projectId` must be used for a spatially distinct project to prevent browser sketch leakage.

## Data Lifecycles

`sources/` and `assets/` are snapshots. `update-sources.sh` replaces them through explicit network calls. `build-map.sh` reads snapshots but never downloads data.

`manual-overlays.json` is persistent local user data and is ignored by Git. If it is missing, the build creates it from the tracked empty `manual-overlays.example.json`; initialization never replaces an existing file. The localhost editor writes the local file atomically after validating a GeoJSON-like `FeatureCollection`. When a generated file is opened directly, new sketches stay in browser storage under a project-specific key until exported.

Generated HTML embeds configuration, parsed vectors, rasters, and local overlays at build time. It is ignored by Git because it may contain private user notes, and it must be rebuilt whenever one of those inputs changes.

## Supported Geometry

The parcel parser accepts WKT `POLYGON` and `MULTIPOLYGON`, including multiple rings. The browser renderer supports Point, LineString, Polygon, and their Multi variants for display; interactive drawing creates the three single-geometry variants.

The planning parser currently targets the configured APP schema namespace and extracts `StrefaPlanistyczna` and `ObszarUzupelnieniaZabudowy`. Its handling of complex GML surfaces remains conservative: confirm holes and multi-surface semantics visually against the authoritative source.

## Layer Semantics

- parcels: selected or contextual cadastral geometry from ULDK;
- zones and OUZ: planning proposal geometry from the configured GML snapshot;
- ortho: aerial imagery preview;
- EGiB: building and parcel-number raster preview;
- addresses: optional street/address raster preview;
- power, water, sewer: indicative utility raster previews;
- manual: user-authored points, lines, and areas with optional status and description.

Candidate layers and their evidence/sourcing risks are evaluated in `docs/research/additional-map-layers.md`.
