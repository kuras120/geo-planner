# Geo Planner

Geo Planner currently builds a self-contained, layered HTML map for parcel
analysis and local sketching. A migration-ready Angular workspace and
loopback-only backend contract simulator now provide the foundation for its
incremental replacement, but the legacy map remains the functional interface.

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
- [Engineering guide](docs/guidelines/engineering-guide.md)
- [Map domain and data contracts](docs/domain/map-domain.md)
- [Project lifecycle and work protocols](docs/guidelines/project-lifecycle.md)
- [Map interface details](mapa/README.md)

Run `./scripts/verify.sh` for the legacy/Python offline quality gate. It uses
checked-in data and does not access the network.

For replacement-application development, install the pinned toolchain and
dependencies with `mise install` and `mise run build-local`. Run the complete
frontend, simulator, backend and legacy gates with `mise run verify`.
