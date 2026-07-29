# Prototype Assumption Register

## Status

Discovery register updated on 2026-07-28. It separates accepted migration
behavior from implementation constraints and owner decisions. An observed
prototype behavior is not a target requirement merely because it works today.

## Classification

| Classification | Meaning |
| --- | --- |
| Intended | Already supported by an owner decision or durable target boundary. |
| Prototype constraint | Useful evidence for parity, but not a target product contract. |
| Decision required | Product behavior must be selected interactively before dependent requirements or contracts are accepted. |

## Project Area And Spatial Context

| Observed assumption | Classification | Migration treatment |
| --- | --- | --- |
| Focus and context parcels, bbox, raster dimensions, and CRS are independently edited configuration values. | Prototype constraint | The target derives a bounded acquisition extent from canonical subject geometry and visible context input. |
| One bbox is used for vector filtering and every raster footprint. | Prototype constraint | Keep subject geometry, display/acquisition extent, and per-artifact bbox distinct. |
| A project may contain one or several parcel subjects. | Intended | Preserve the exact selected subjects and their union; surrounding parcels remain context unless selected. |
| A dispersed selection may create a country-scale envelope. | Intended replacement, owner accepted 2026-07-28 | The local-MVP profile allows at most 2 km width, 2 km height, 4 km² envelope area, and 100 selected parcels. Apply it before and after buffering; exceeding it requires separate projects without confirmation override. A deployment may raise it only after explicit validation. |
| Surrounding context is an unexplained margin inside the configured bbox. | Intended replacement, owner accepted 2026-07-28 | Use a visible 100 metre default context buffer, adjustable from 0 to 500 metres and persisted with the project. Show the resulting extent before acquisition; hard AOI budgets may reject a large resulting extent. |
| The project carries one global WMS axis-order flag. | Prototype constraint | Axis order belongs to the versioned source/layer descriptor and exact request. |

## Layer Catalog And Presentation

| Observed assumption | Classification | Migration treatment |
| --- | --- | --- |
| MVP covers the current parcel, planning, ortho, EGiB, address and utility views. | Intended | Discover concise application-area requirements for reading, displaying, identifying, provenance, uncertainty, and degraded states. |
| The HTML template has a fixed set of raster IDs, controls, labels, and SVG groups. | Prototype constraint | A server-owned catalog supplies typed layer descriptors; the frontend maps supported descriptor kinds to renderers. |
| The current bottom-to-top layer order is fixed globally. | Prototype constraint | Do not treat the SVG order as a target contract; define typed presentation groups/order with the frontend slice that renders them. |
| Initial visibility is fixed globally. | Intended default, owner accepted 2026-07-28 | Start MVP projects with ortho, subject parcels, EGiB, and planning zones visible; start land classes, OUZ, addresses, and utility layers hidden. Persist later visibility choices as project/user preferences. |
| Missing required rasters render as blank while only the address control is explicitly optional. | Prototype constraint, replacement accepted 2026-07-28 | AOI/parcel-resolution failure blocks project creation. An individual source-layer failure does not block opening an otherwise valid project and must have a visible unavailable, no-coverage, failed, or stale state. |
| Layer details expose only the fields currently embedded in the template. | Intended replacement, owner accepted 2026-07-28 | Every MVP layer gets a compact provenance card with readiness, provider, dataset/layer, acquisition or document date, CRS, extent, attribution, and warning. Only queryable/vector data exposes feature details; raster pixels do not pretend to identify source features. Full request metadata remains available in expandable technical details. |

## Acquisition And Failure Handling

| Observed assumption | Classification | Migration treatment |
| --- | --- | --- |
| Source refresh is an explicit operator action and offline verification never refreshes data. | Intended | Keep network acquisition explicit, observable, and separate from deterministic tests/builds. |
| Successful downloads use temporary files and atomic promotion; a failed target keeps its previous snapshot. | Intended | Preserve last-known-good artifacts and record partial/per-layer outcomes. |
| Downloads are sequential, have no job progress, and stop at the first required failure. | Prototype constraint | Use the accepted acquisition job state model and structured per-layer results. |
| Every raster uses the same configured dimensions, even after bbox changes. | Prototype constraint | Derive dimensions from layer-specific ground resolution and tile under declared limits. |
| Raster acquisition has no product resource budget. | Intended replacement, owner accepted 2026-07-28 | Default to 0.5 m/px; allow validated 0.25 m/px and explicit 1 m/px. Use 2048² product tiles, at most 16M px/layer, 64 planned tile requests, 64 MiB/response, and 512 MiB promoted artifacts/acquisition. Never silently coarsen. |
| The prototype downloads each response as one subprocess result and later embeds raster bytes in HTML. | Intended replacement with deferred slice design, owner noted 2026-07-28 | The backend streams into bounded temporary storage, validates and atomically promotes, and reports per-layer stages/progress. The frontend never loads or embeds the whole acquisition; exact delivery endpoints and progress events are designed with the acquisition vertical slice. |
| Raster images have no embedded or sidecar georeferencing and are stretched over the bbox. | Prototype constraint | Persist exact bbox, CRS, resolution, dimensions, request identity, and checksum with every promoted artifact. |
| Only addresses are currently treated as optional. | Prototype constraint, replacement accepted 2026-07-28 | Every acquired MVP source layer has independent readiness. A usable project may open with explicit layer warnings; no failed layer is silently rendered as an empty success. |

## Sketch Interaction And Persistence

| Observed assumption | Classification | Migration treatment |
| --- | --- | --- |
| A LineString may have two or more vertices; Polygon is a separate closed geometry. | Intended geometry meaning | Preserve valid multi-vertex lines. Do not infer a polygon merely from vertex count or visual closure. |
| The user selects point/line/polygon mode before drawing and finishes lines and polygons explicitly. | Intended replacement, owner accepted 2026-07-28 | Select point, line, or area intent first. Lines accept two or more vertices and remain open; areas accept three or more vertices and close only on finish. Use distinct open/filled previews, explicit finish plus Enter/double-click, Escape to cancel, and point undo. Attempting to close a line may offer conversion but never silently changes its geometry type. |
| Local identity prefers explicit ID, then name/label, then serialized geometry; later local features replace matching embedded features and duplicate geometries collapse. | Intended replacement, owner accepted 2026-07-28 | The backend assigns immutable feature IDs; names and geometries are not identities. Geometric duplicates are legal and may produce a warning, but are never silently merged. Collection writes use optimistic version checks and reject conflicts instead of overwriting newer state. |
| Direct-file browser storage and loopback repository storage are merged with different deletion capabilities. | Intended replacement, owner accepted 2026-07-28 | Backend storage becomes authoritative. Legacy import has a preview and report, preserves valid IDs, assigns stable import IDs when absent, and is idempotent for the same source file. No automatic merge by name or geometry occurs. |
| The loopback editor sends and atomically replaces the whole FeatureCollection after each edit. | Migration evidence | Retain atomic, versioned collection replacement as the current parity baseline; incremental commands may be designed later if justified. |

## Browser Runtime

| Observed assumption | Classification | Migration treatment |
| --- | --- | --- |
| The generated HTML embeds all snapshots and private overlays. | Prototype constraint | The target frontend receives authorized descriptors/artifacts and never becomes the durable overlay store. |
| Geometry rendering depends on CDN-loaded `d3-geo`. | Prototype constraint | The Angular/OpenLayers application owns its bundled renderer dependencies. |
| Save/build changes cause a full-page hot reload and transient UI state loss. | Prototype constraint | Normal target mutations update explicit state without rebuilding the application document. |
| Invalid browser-local JSON and hot-reload polling failures are silent. | Prototype constraint | Surface actionable state and preserve the last usable view without claiming success. |

## Interactive Decision Order

Resolve one coherent cluster at a time:

1. [accepted 2026-07-28] layer defaults and independent layer readiness;
2. [accepted 2026-07-28] concise identify/provenance fields by MVP layer;
3. [accepted 2026-07-28] drawing interaction;
4. [accepted 2026-07-28] overlay identity, duplicates, import, and conflicts;
5. [accepted 2026-07-28] acquisition defaults and provider budgets, including
   deferred streaming/progress delivery design for the acquisition slice.

The accepted answer for each cluster must be recorded in its durable owner
before dependent requirements or shared contracts are accepted.
