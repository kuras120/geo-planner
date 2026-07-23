# Current Public Integrations

## Status

Evidence record reconstructed from the prototype on 2026-07-19. Endpoints and
capabilities can change; verify them before implementing a new adapter.

## Integrations Used by the Prototype

| Capability | Public system | Protocol or format | Current prototype use |
| --- | --- | --- | --- |
| Parcel lookup | GUGiK ULDK | HTTP query returning WKT | Resolve parcel geometry from cadastral identifiers |
| Orthophoto | GUGiK national geoportal | WMS `GetMap` | Download a raster for the configured bbox and CRS |
| Terrain relief | GUGiK national geoportal | WMS `GetMap` | Download shaded-relief raster |
| Local planning data | Municipal public map service | WMS plus linked GML/XML | Download plan image and extract selected plan geometry |
| Background map | OpenStreetMap | Public tile service | Browser-only visual context |

The checked-in prototype does not require an account or application token for
these reads. Public accessibility does not remove licensing, attribution,
availability, fair-use, or rate-limit obligations.

## Evidence in the Repository

- `mapa/scripts/update_sources.py` contains ULDK and WMS request construction.
- `mapa/project-config.json` records services, layers, CRS, bbox, and sources.
- `mapa/scripts/build_map.py` parses artifacts and embeds normalized results.
- `mapa/map-fragment.template.html` initializes the OpenStreetMap background.

## Adapter Families Needed in a Generic Product

| Adapter family | Responsibility |
| --- | --- |
| Cadastral parcel resolver | Convert jurisdiction-specific parcel identifiers into normalized geometry and source metadata |
| OGC map-image client | Discover capabilities and request WMS images with explicit layer, style, CRS, bbox, dimensions, and format |
| Planning-data adapter | Normalize municipality-specific WMS/GML/XML structures into product concepts |
| Basemap configuration | Select permitted background maps and preserve attribution |
| Source evidence recorder | Retain request parameters, retrieval time, service identity, and uncertainty |

## Portability Gap

WMS is reusable, but layer names, coordinate systems, styles, formats, response
limits, and municipal planning schemas vary. A generic implementation therefore
needs capability discovery and provider adapters rather than a universal
hard-coded URL builder.

## Candidates Requiring Separate Validation

- official address and building services;
- elevation point or terrain models suitable for quantitative analysis;
- environmental and flood-risk services;
- utility-network data with lawful public access;
- planning-data services outside the prototype municipality.

For each candidate, verify official ownership, terms, coverage, update cadence,
identifiers, CRS support, failure behavior, and redistribution rights.

## Official References

- [GUGiK ULDK documentation](https://uldk.gugik.gov.pl/)
- [Polish national geoportal](https://www.geoportal.gov.pl/)
- [OGC Web Map Service standard](https://www.ogc.org/standard/wms/)
- [OpenStreetMap tile usage policy](https://operations.osmfoundation.org/policies/tiles/)
