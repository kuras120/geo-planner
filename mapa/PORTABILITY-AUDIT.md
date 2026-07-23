# Portability Audit

Updated: 20 July 2026.

## Result

The main location-specific values now live in `project-config.json`: project identity, title, output file, CRS, bbox, WMS axis order, raster size, precinct, planning source/schema, parcels and their metadata, service URLs, raster paths, and source attribution.

The builder, downloader, browser storage, standalone title, source note, local editor, and generated output name all consume that configuration. WKT parcel parsing supports both Polygon and MultiPolygon. Offline tests cover configuration safety, duplicate parcels, WMS axis order, polygon rings, multipolygons, and GML coordinate order.

For another Polish area using compatible ULDK, WMS, and APP planning inputs, portability is now approximately **8/10**: moving the engine should require project-data configuration and source refresh rather than source-code edits.

## Remaining Constraints

- The template still has a fixed catalog of standard raster layer IDs (`ortho`, `egib`, `addresses`, `power`, `water`, `sewer`). Adding a new layer still requires interface/config work.
- Planning parsing targets the configured APP namespace but does not fully model every GML surface/holes variant or validate each feature's `srsName`.
- Raster files are unreferenced images stretched over the bbox; alignment requires a visual control-point check after refresh.
- `manual-overlays.json` uses the project CRS although GeoJSON interoperability normally assumes WGS84 unless a separate CRS contract is supplied.
- The standalone HTML embeds data but loads `d3-geo` from a CDN, so it is not fully offline.
- Source availability and coverage differ by authority and region.

## Next Portability Increment

Implement a generic raster catalog in `project-config.json` with labels, WMS parameters, ordering, optionality, opacity, acquisition timestamps, and source notes. Generate layer controls dynamically. NMT hillshade and SOPO are good first test layers because they are valuable around hilly terrain and exercise services beyond the current GUGiK integrations.

See [additional map layers](../docs/research/additional-map-layers.md) and the [repository guide](../docs/guidelines/repository-guide.md).
