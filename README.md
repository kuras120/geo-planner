# Geo Planner

Geo Planner builds a self-contained, layered HTML map for parcel analysis and local sketching. A project configuration defines the area, coordinate system, parcels, planning data, raster services, and output name; the same map engine can therefore be reused for another fragment of Poland without editing source code.

The checked-in example covers parcels in Ciężkowice. Government layers are informative and may be incomplete or out of date. Manual overlays are sketches, not surveying or legal evidence.

Manual overlays and generated HTML are local artifacts ignored by Git. On the first build, an empty `mapa/manual-overlays.json` is created automatically from the tracked neutral example.

## Quick Start

```bash
cd mapa
./scripts/build-map.sh
./scripts/edit-map.sh
```

Open the local URL printed by the editor, normally `http://127.0.0.1:8765/mapa-ciezkowice.html`. Use `./scripts/update-sources.sh` only when government sources should be downloaded again.

To configure another area, copy `mapa/project-config.json`, change its project identity, bbox, CRS, precinct, parcels, plan, and output file, then refresh sources and build. Appearance-only settings remain in `mapa/map-config.json`.

## Documentation

- [Repository guide](docs/guidelines/repository-guide.md)
- [Map domain and data contracts](docs/domain/map-domain.md)
- [Engineering guide](docs/guidelines/engineering-guide.md)
- [Project lifecycle and work protocols](docs/guidelines/project-lifecycle.md)
- [Map build flow](docs/architecture/map-build-flow.md)
- [Candidate map layers](docs/research/additional-map-layers.md)
- [Privacy and data-separation audit](docs/research/privacy-and-data-separation-audit.md)
- [Frontend technology options](docs/research/frontend-technology-options.md)
- [Productization and generic map workflow proposal](docs/projects/productization-and-generic-map-workflow.md)
- [Map interface details](mapa/README.md)

Run `./scripts/verify.sh` for the complete local quality gate. It uses checked-in data and does not access the network.
