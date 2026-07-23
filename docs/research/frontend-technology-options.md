# Frontend Technology Options

## Decision Context

The current browser application is a single HTML template with inline CSS and JavaScript. It combines rendering, layer state, coordinate conversion, feature selection, drawing, persistence, and UI construction. That was effective for a prototype, but it makes changes hard to isolate and test.

The target application must support Polish public geospatial services, arbitrary project extents, custom coordinate reference systems, raster and vector layers, feature inspection, editable sketches, and an offline/export workflow. The owner has the most experience with Angular and some experience with React and TypeScript.

## Recommendation

Use **Angular with TypeScript and OpenLayers**, keeping OpenLayers behind a small application-owned adapter instead of adopting a framework-specific map wrapper.

- Angular standalone components, dependency injection, typed forms, router, test tooling, and signals provide a clear structure for a growing editor. Existing Angular experience lowers migration and maintenance cost.
- OpenLayers directly supports WMS/WMTS, capability documents, tiled and image services, vector formats, drawing/modification/snapping, feature inspection, custom projections through Proj4, and client-side raster reprojection.
- A thin adapter (`MapFacade` plus focused layer/editing services) contains the imperative OpenLayers object lifecycle. Angular components own panels and workflows; they do not manipulate map internals directly.
- Use signals for local synchronous UI state and RxJS for HTTP, events, cancellation, and acquisition progress. Do not introduce NgRx until cross-feature state complexity demonstrates a need.

Primary references: [Angular signals](https://angular.dev/guide/signals), [Angular standalone migration](https://angular.dev/reference/migrations/standalone), [OpenLayers examples](https://openlayers.org/en/latest/examples/), [OpenLayers raster reprojection](https://openlayers.org/doc/tutorials/raster-reprojection.html), and [OpenLayers Proj4 integration](https://openlayers.org/en/latest/apidoc/module-ol_proj_proj4.html).

## Options Compared

| Option | OGC/custom CRS fit | Application structure | Team fit | Assessment |
| --- | --- | --- | --- | --- |
| Angular + OpenLayers | Excellent | Strong conventions and built-in composition | Best current fit | **Recommended** |
| React + OpenLayers | Excellent | Flexible, but routing/data/state/testing choices must be assembled | Familiar enough | Good alternative if a React ecosystem or team becomes the priority |
| React/Angular + MapLibre GL JS | Moderate for the current sources; excellent for WebGL vector tiles | Good | Learnable | Prefer if the product moves to EPSG:3857 vector tiles, large WebGL datasets, or 3D |
| Leaflet | Good for simple maps; advanced CRS/OGC/editing often relies on plugins | Simple | Easy | Attractive for a small viewer, not the strongest base for this editor |
| Keep custom SVG/d3 template | Requires custom GIS behavior | Weak separation at current scale | Known code | Suitable only as a temporary migration source |

React is technically viable. Its official guidance supports build tools such as Vite when starting from scratch, while noting that routing, data fetching, and other production patterns must be selected and maintained by the team. Create React App is deprecated. That flexibility does not provide enough benefit here to offset the owner's stronger Angular experience. See [React: build from scratch](https://react.dev/learn/build-a-react-app-from-scratch) and [React installation](https://react.dev/learn/installation).

MapLibre GL JS is a strong TypeScript/WebGL renderer for vector-tile-centric products. Its WMS example exposes WMS as EPSG:3857 raster tiles, whereas this project needs first-class handling of varying WMS versions, capability negotiation, Polish projected CRSs, and editable vectors. See [MapLibre GL JS introduction](https://maplibre.org/maplibre-gl-js/docs/) and [WMS example](https://maplibre.org/maplibre-gl-js/docs/examples/add-a-wms-source/).

## Proposed Frontend Shape

```text
Angular UI
  project setup | layer catalog | inspector | sketch editor | export/status
       |
application services and typed domain models
  ProjectStore | LayerRegistry | SelectionService | OverlayRepository
       |
MapFacade (the only general OpenLayers boundary)
       |
OpenLayers map, sources, layers, interactions and projections
       |
remote services or local acquisition API + private project workspace
```

Suggested feature boundaries:

- `core/map`: map lifecycle, projection registration, viewport, layer ordering;
- `features/projects`: create/open/validate a project and choose an area;
- `features/layers`: catalog, capability-derived options, visibility, opacity, legends;
- `features/inspect`: GetFeatureInfo and local vector attributes;
- `features/sketch`: draw/modify/snap, typed overlay properties, undo/redo;
- `features/acquisition`: refresh status, provenance, errors, cancellation;
- `features/export`: reproducible offline snapshot and sanitized share export.

Keep the current Python code initially as an offline acquisition/build boundary. Convert it into a reusable package and CLI before deciding whether a local FastAPI service is necessary. A service becomes useful when the browser must initiate downloads, bypass third-party CORS limitations, keep credentials private, or stream long-running acquisition progress. It should not be introduced merely to serve static frontend assets.

## Migration Strategy

1. Freeze and characterize current behavior with domain and browser-level tests.
2. Extract TypeScript domain models and JSON Schema from the generic project/source contracts.
3. Build a read-only Angular/OpenLayers shell capable of loading the sanitized demo.
4. Add dynamic layers and projection handling from descriptors rather than hard-coded IDs.
5. Port feature inspection and sketch editing, including import of current overlay JSON.
6. Add acquisition status and offline/export workflows against the generic Python boundary.
7. Run old and new renderers side by side for representative control points, then retire the inline template.

The migration should not be a visual rewrite combined with a data-model rewrite in one release. Stabilizing the generic contracts first makes it possible to compare both renderers against the same project.

## Research Conclusion

Angular is not being selected solely because it is familiar. Angular plus OpenLayers matches both the maintenance problem and the GIS protocol requirements. React plus OpenLayers remains a sound fallback with near-identical map capabilities. MapLibre becomes preferable only after a deliberate backend/data-pipeline shift toward web-mercator vector tiles or 3D, which is a different architecture from the current public-service integration.

