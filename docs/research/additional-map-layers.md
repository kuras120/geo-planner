# Candidate Map Layers

Status checked: 20 July 2026. Service capabilities and legal meaning must be rechecked before implementation.

## Recommended Priority

| Priority | Layer | Value | Integration shape | Main caution |
| --- | --- | --- | --- | --- |
| 1 | Terrain shading, elevation, and derived slope | Reveals access gradients, drainage direction, earthworks, and construction difficulty. | NMT shaded-relief WMS first; later derive contours/slope from downloaded NMT. | A visual hillshade is not a geotechnical survey; vertical datum and acquisition date matter. |
| 1 | Landslides and mass-movement risk | Particularly important around Ciężkowice and other hilly areas. | Public SOPO WMS as an indicative overlay; link to source record when available. | Coverage, scale, and registry status vary; absence is not proof of stability. |
| 1 | Flood hazard and surface water | Supports early screening of buildability, access, drainage, and insurance risk. | Wody Polskie flood-hazard/river layers; start as raster preview. | Distinguish statutory flood scenarios, watercourses, and owner-drawn drainage hypotheses. |
| 1 | Binding and emerging planning acts | Complements the current general-plan snapshot with MPZP and other acts. | Prefer the Rejestr Urbanistyczny services; retain source date and act status. | A draft, adopted act, and in-force act must never share one undifferentiated style. |
| 2 | Nature protection and Natura 2000 | Screens protected areas and environmental constraints. | GDOŚ WMS/WFS, ideally as queryable vectors with form/type metadata. | Protection boundaries do not alone state every applicable restriction. Sensitive species data needs special handling. |
| 2 | Soil/agricultural suitability | Useful for farming, land conversion screening, and parcel comparison. | Geoportal soil-agricultural WMS, optionally GML where available. | Coverage and currency differ by region; historical classifications need qualified wording. |
| 2 | Topographic roads, paths, buildings, land cover | Improves real-world context and access analysis beyond the cadastral preview. | BDOT10k/KIBDOT or suitable Geoportal viewing service. | Cartographic presence does not establish ownership or legal access rights. |
| 3 | Heritage monuments and archaeological protection | Early warning for development and due diligence. | NID portal WMS/WFS after confirming current capabilities and license. | Registry layers may be incomplete for local conservation zones; confirm with competent authority. |
| 3 | Administrative/source-service coverage | Helps discover which local authority publishes planning or environmental services. | EZiUDP WMS and registry metadata, mostly as diagnostics rather than a default visible layer. | This describes datasets/services, not the underlying legal situation on the parcel. |

## Official Sources

- GUGiK lists current national WMS/WMTS services, including cadastral integration, utilities, planning, transport, thematic, and topographic data: [Geoportal viewing services](https://www.geoportal.gov.pl/pl/usluga/uslugi-przegladania-wms-i-wmts/).
- GUGiK documents NMT availability, 1 m/5 m grids, downloads, and the shaded-relief WMS: [Numeryczny model terenu](https://www.geoportal.gov.pl/pl/dane/numeryczny-model-terenu-nmt/).
- PIG-PIB exposes public SOPO viewing data; the open-data registry identifies the public landslide WMS: [SOPO WMS dataset](https://dane.gov.pl/pl/dataset/1297/resource/35123/table).
- Wody Polskie publishes flood hazard and risk map context and points to the map portal: [flood hazard and risk maps](https://www.gov.pl/web/wody-polskie/mapy-zagrozenia-powodziowego-i-mapy-ryzyka-powodziowego).
- GDOŚ documents official nature-protection WMS and WFS access: [geospatial data access](https://www.gov.pl/web/gdos/dostep-do-danych-geoprzestrzennych.).
- GUGiK documents the soil-agricultural map, its regional coverage, GML availability, and WMS/WMTS endpoints: [Geoportal thematic maps](https://www.geoportal.gov.pl/pl/dane/mapy/).
- On 6 July 2026 GUGiK announced Rejestr Urbanistyczny services for general plans, MPZP, landscape resolutions, regional plans, and landscape audits, with older GUGiK planning services entering a transition period: [Rejestr Urbanistyczny announcement](https://www.gov.pl/web/gugik/nowe-uslugi-w-geoportalu--rejestr-urbanistyczny).
- GUGiK provides EZiUDP registry coverage through WMS for locating available public spatial datasets and services: [EZiUDP WMS](https://www.gov.pl/web/gugik/ewidencja-zbiorow-i-uslug-danych-przestrzennych-dostepna-z-poziomu-geoportalu-w-postaci-uslugi-wms).

## Suggested Delivery Order

1. Add a generic raster-layer schema to project config (`id`, label, service, version, layer names, format, optionality, opacity, source note) so new WMS layers do not require template edits.
2. Implement NMT hillshade and SOPO as the first portability test: they exercise generic rasters and have high local value.
3. Add flood and nature-protection layers with explicit evidence/status legends.
4. Add queryable vector adapters only when property inspection is needed; avoid prematurely building one parser per provider.
5. Add per-layer acquisition timestamps, GetCapabilities snapshots, and a stale-data indicator before the layer catalog becomes large.

The current implementation centralizes the six established raster paths but the interface still knows their standard IDs. A generic raster catalog is therefore the next architectural increment, not part of the current portability baseline.
