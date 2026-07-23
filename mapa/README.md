# Map Interface And Local Editor

The current project generates `mapa-ciezkowice.html` and `map-fragment.html`. Both are local, Git-ignored build outputs and must not be edited manually. The reusable interface lives in `map-fragment.template.html`.

## Build And Edit

From this directory:

```bash
./scripts/build-map.sh
./scripts/edit-map.sh
```

The editor prints the URL derived from `project-config.json`, normally `http://127.0.0.1:8765/mapa-ciezkowice.html`. Use `--port 8877` to select another port. Stop it with `Ctrl+C`.

The loopback editor watches the project/configuration JSON files, template, source data, rasters, and manual overlays. It rebuilds and reloads the browser after a change. Completed sketches and deletions are written atomically to the local, Git-ignored `manual-overlays.json`.

If `manual-overlays.json` does not exist, the first build creates it from the tracked empty `manual-overlays.example.json`. An existing local file is never replaced by initialization. To reset it, delete the local file deliberately and run the build again.

When opening generated HTML through `file://`, repository writes are unavailable. Sketches remain in browser `localStorage`, namespaced by `projectId`, and can be exported as GeoJSON.

## Interaction

- Mouse wheel: zoom.
- Middle-button drag: pan.
- Left click: select a parcel/sketch or add a drawing point.
- Right click: browser context menu.
- Drawing modes: point, line, or polygon; finish explicitly except for points.
- Deletion: select the sketch first, then confirm removal.

The selected object receives a stronger outline and its metadata appears in the side panel. Manual `category`, `status`, and `description` fields remain optional and are never inferred by the editor.

## Configuration

`project-config.json` contains location and data concerns: identity, output name, CRS, bbox, WMS axis order, raster dimensions, precinct, parcel list and metadata, plan source/schema, services, raster paths, and source note.

`map-config.json` contains presentation only:

- parcel/manual label size and visibility;
- label halo width;
- manual overlay stroke/fill values;
- desktop/mobile map height and sidebar width;
- workspace layout and initial layer visibility.

Changing the bbox, CRS, or project location requires refreshing every bound source and raster, not only rebuilding HTML.

## Source Refresh

```bash
./scripts/update-sources.sh
./scripts/build-map.sh
```

Refresh uses ULDK, the configured planning GML URL, and configured WMS services. It is intentionally separate from build and tests because it accesses the network and replaces snapshots. The address layer is optional; other failures stop the refresh.

Government data and utility rasters are informative previews. The planning file may be a draft. Manual roads, pipes, areas, and property notes are indicative sketches. Use authoritative current documents and professional surveys for legal, planning, design, and construction decisions.

See the root [repository guide](../docs/guidelines/repository-guide.md) for moving the engine to another area and [map domain](../docs/domain/map-domain.md) for spatial invariants.
