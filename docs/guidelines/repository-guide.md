# Repository Guide

## Environment

The repository requires Python 3, Bash, and `curl`. It has no third-party Python or Node.js dependencies. The generated browser interface imports `d3-geo` from a CDN, so displaying geometry currently requires internet access even when the HTML data itself is embedded.

## Commands

From the repository root:

```bash
./scripts/verify.sh
```

The quality gate runs unit tests, compiles Python modules, rebuilds generated HTML from checked-in inputs, and rejects unresolved template markers. It does not access the network.

From `mapa/`:

```bash
./scripts/build-map.sh             # build from checked-in snapshots
./scripts/edit-map.sh              # build, serve, persist sketches, hot reload
./scripts/edit-map.sh --port 8877  # select another loopback port
./scripts/update-sources.sh        # explicitly replace downloaded snapshots
```

The editor URL uses `outputFile` from `project-config.json`.

## Configure Another Area

1. Copy the map directory or start from a clean branch.
2. Set a new `projectId`, title, output filename, CRS, bbox, axis order, raster size, precinct, plan, and parcel list in `project-config.json`.
3. Remove location-specific parcel metadata that does not belong to the new project and use a distinct `projectId`.
4. Confirm the correct PL-2000 zone/CRS and both GML/WMS coordinate orders from the source metadata.
5. Run `./scripts/update-sources.sh`; this requires network access and replaces snapshots.
6. Run `./scripts/verify.sh` from the root.
7. Compare parcel boundaries, planning vectors, and each raster at recognizable control points before relying on the result.

Changing only the bbox is insufficient: raster snapshots, parcel sources, the plan snapshot, and project identity must remain coherent.

## Configuration Ownership

- `project-config.json`: location, data, sources, identity, and output;
- `map-config.json`: sizes, label visibility, styling values, and initial layer switches;
- `manual-overlays.example.json`: tracked neutral initializer for local sketches;
- `manual-overlays.json`: ignored local user sketches and their descriptive properties;
- `map-fragment.template.html`: shared interface behavior, supported standard layer controls, and styles.

## Generated Files

`map-fragment.html` and the configured standalone output are generated, local, and ignored by Git. Do not edit them manually. Their size is expected because raster bytes, current data, and private local overlays are embedded. Share an output only after reviewing its embedded content.

## Troubleshooting

- Missing parcel source: refresh sources or correct the parcel filename in project config.
- Shifted raster: verify CRS, bbox, WMS version, and `wms130AxisOrder`, then refresh all rasters.
- Shifted planning geometry: verify `plan.coordinateOrder` and the GML `srsName`.
- Sketches from another area: assign a unique `projectId`; browser storage is derived from it.
- Optional addresses unavailable: the updater warns and continues, preserving the last existing file when possible.
- Blank geometry offline: the current generated map loads `d3-geo` from a CDN; bundle it locally before field/offline use.
