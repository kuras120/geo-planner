# Repository Guide

## Environment

The repository requires Python 3, Bash, and `curl`. It has no third-party Python or Node.js dependencies. The generated browser interface imports `d3-geo` from a CDN, so displaying geometry currently requires internet access even when the HTML data itself is embedded.

## Commands

From the repository root:

```bash
./scripts/update_requirements_index.py  # refresh requirement dashboard statistics
./scripts/verify.sh                     # run the offline quality gate
```

The requirement-index updater reads all application-area requirement files and
atomically regenerates the area, delivery-stage, status, and grand-total tables
in `docs/requirements/index.md`. The quality gate rejects a stale requirement
index, runs unit tests, compiles Python modules, rebuilds generated HTML from
checked-in inputs, and rejects unresolved template markers. Neither command
accesses the network.

From `mapa/`:

```bash
./scripts/build-map.sh             # build from checked-in snapshots
./scripts/edit-map.sh              # build, serve, persist sketches, hot reload
./scripts/edit-map.sh --port 8877  # select another loopback port
./scripts/update-sources.sh        # explicitly replace downloaded snapshots
```

The editor URL uses `outputFile` from `project-config.json`.

The reference builder also accepts an explicit project-map directory:

```bash
python3 mapa/scripts/build_map.py --map-dir /path/to/complete-map-directory
python3 -m unittest tests.test_project_fixtures
```

Production-style map directories must include the shared template. Test
fixtures copy that template into a temporary directory so generated outputs and
runtime overlays never modify the tracked fixture.

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

- `project-config.json`: location, data, sources, identity, output, and raster
  paths including the KIEG land-use/classification snapshot;
- `map-config.json`: sizes, label visibility, styling values, and initial layer switches;
- `manual-overlays.example.json`: tracked neutral initializer for local sketches;
- `manual-overlays.json`: ignored local user sketches and their descriptive properties;
- `map-fragment.template.html`: shared interface behavior, supported standard layer controls, and styles.

## Generated Files

`map-fragment.html` and the configured standalone output are generated, local, and ignored by Git. Do not edit them manually. Their size is expected because raster bytes, current data, and private local overlays are embedded. Share an output only after reviewing its embedded content.

The future local-MVP backend stores runtime state below the ignored
`.geo-planner-data/` default or an explicitly configured external root. It must
not use tracked fixtures, `mapa/sources/`, or `mapa/assets/` as writable
runtime storage.

## Troubleshooting

- Missing parcel source: refresh sources or correct the parcel filename in project config.
- Missing land-class markings: confirm the county publishes `uzytki` and
  `kontury` through KIEG, then explicitly refresh sources.
- Shifted raster: verify CRS, bbox, WMS version, and `wms130AxisOrder`, then refresh all rasters.
- Shifted planning geometry: verify `plan.coordinateOrder` and the GML `srsName`.
- Sketches from another area: assign a unique `projectId`; browser storage is derived from it.
- Optional addresses unavailable: the updater warns and continues, preserving the last existing file when possible.
- Blank geometry offline: the current generated map loads `d3-geo` from a CDN; bundle it locally before field/offline use.
