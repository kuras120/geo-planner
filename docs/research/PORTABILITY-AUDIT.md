# Portability Audit

Updated: 28 July 2026.

## Result

The main location-specific values now live in `project-config.json`: project identity, title, output file, CRS, bbox, WMS axis order, raster size, precinct, planning source/schema, parcels and their metadata, service URLs, raster paths, and source attribution.

The builder, downloader, browser storage, standalone title, source note, local editor, and generated output name all consume that configuration. WKT parcel parsing supports both Polygon and MultiPolygon. Offline tests cover configuration safety, duplicate parcels, WMS axis order, polygon rings, multipolygons, and GML coordinate order.

The builder also accepts an explicit project-map directory. Two fully synthetic
test projects exercise the same build path with no source-code changes: a
single-parcel EPSG:2180/XY project and an adjacent multi-parcel
EPSG:2178/YX project. Each fixture records its bbox, CRS, axis rules, source,
provenance, and absence of private data.

For another Polish area using compatible ULDK, WMS, and APP planning inputs,
the reference builder now needs project-directory data rather than source-code
edits. Acquisition remains less portable than assembly because provider
adapters and the renderer layer catalog are still fixed.

## Remaining Constraints

- The template still has a fixed catalog of standard raster layer IDs (`ortho`,
  `egib`, `landClasses`, `addresses`, `power`, `water`, `sewer`). Adding a new
  layer still requires interface/config work.
- Planning parsing targets the configured APP namespace but does not fully model every GML surface/holes variant or validate each feature's `srsName`.
- Raster files are unreferenced images stretched over the bbox; alignment requires a visual control-point check after refresh.
- `manual-overlays.json` uses the project CRS although GeoJSON interoperability normally assumes WGS84 unless a separate CRS contract is supplied.
- The standalone HTML embeds data but loads `d3-geo` from a CDN, so it is not fully offline.
- Source availability and coverage differ by authority and region.

## Implication

Further portability depends on separating acquisition adapters from normalized
layer data and making the raster catalog configuration-driven. Implementation
still requires an owner-approved feature plan.
