# Repository Guide

## Environment

The legacy map workflow requires Python 3, Bash, and `curl`. The replacement
frontend, Kotlin backend, and contract simulator use the exact Node.js and JDK
versions pinned in root-level `mise.toml`; the JDK runs the backend and OpenAPI
Generator. The npm dependencies are locked independently under `frontend/` and
`backend-simulator/`. Gradle resolves backend plugins and dependencies on demand
for the requested backend task.

The generated legacy browser interface imports `d3-geo` from a CDN, so
displaying its geometry currently requires internet access even when the HTML
data itself is embedded.

## Commands

From the repository root:

```bash
mise install                       # install the pinned Node.js and JDK
mise run setup                     # mutable local npm installs plus Chromium
mise run setup-ci                  # frozen CI npm installs plus Linux browser dependencies
mise run frontend                  # Angular development server
mise run backend                   # Spring Boot development server
mise run storybook                 # shared UI workshop
mise run simulator                 # Node contract simulator on loopback
mise run validate-tasks            # validate the mise task graph and definitions
mise run verify                    # task definitions plus all application quality gates
mise run assemble                  # backend Boot JAR plus production frontend
mise run ci                        # setup-ci followed by verify
mise run clean                     # remove generated application/test outputs
./scripts/update_requirements_index.py  # refresh requirement dashboard statistics
./scripts/verify.sh                     # run the legacy/Python offline quality gate
```

The requirement-index updater reads all application-area requirement files and
atomically regenerates the area, delivery-stage, status, and grand-total tables
in `docs/requirements/index.md`. The quality gate rejects a stale requirement
index, runs unit tests, compiles Python modules, rebuilds generated HTML from
checked-in inputs, and rejects unresolved template markers. Neither command
accesses the network.

`mise install`, `mise run setup`, and `mise run setup-ci` access tool, package,
or Playwright download services. On a fresh machine, backend verification may
also download the Gradle Wrapper, plugins, and dependencies. Quality commands
never refresh government map sources.

`setup` and `setup-ci` do not compile, test, or assemble applications. Gradle
does not require a separate backend installation task: `verify-backend`,
`backend`, and `assemble` resolve the configurations they need. `verify` first
includes static validation of the mise task definitions and aggregates the four
application component gates; it does not run npm installation.
`assemble` assumes setup has already completed and produces artifacts without
publishing or deploying them.

From `frontend/`:

```bash
npm start                 # Angular development server
npm run storybook         # Storybook 10 shared UI workshop
npm run lint
npm run test:unit
npm run build
npm run storybook:build
npm run e2e               # Chromium smoke test
npm run verify            # complete frontend gate
npm run api:generate -- /path/to/openapi.yaml
```

From `backend-simulator/`:

```bash
npm run build
npm start                 # 127.0.0.1:4300
npm run verify
```

The simulator foundation exposes only `GET /_simulator/health`. Product routes,
fixtures, and named scenarios enter with their accepted contract slices.

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
