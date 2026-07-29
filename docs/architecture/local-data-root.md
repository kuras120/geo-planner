# Local Data Root Contract

## Status

Accepted migration boundary for the future local-MVP backend. This describes
storage ownership and safety; it does not claim that the Kotlin persistence
adapter exists.

## Configuration

The backend owns one configurable local data root:

- logical setting: `geo-planner.storage.root`;
- environment binding: `GEO_PLANNER_DATA_ROOT`;
- local development default: `<workspace>/.geo-planner-data`;
- the resolved root must be writable and is always ignored by Git.

Production deployment must set an explicit persistent path. Project input,
provider responses, filenames, and HTTP parameters never select or alter the
root.

In the local MVP the backend runs on the user's machine, so this root is
physically client-local and does not consume centralized server storage.

## Layout

```text
.geo-planner-data/
  storage-version.json
  projects/
    <project-id>/
      project.json
      overlays.json
      acquisitions/
        <job-id>.json
  artifacts/
    <artifact-id>/
      manifest.json
      content
  imports/
    <import-id>.json
  tmp/
    <job-id>/
```

The logical layout may evolve behind the persistence ports, but these ownership
rules remain:

- project metadata, overlay revisions, jobs, manifests, imports, and artifacts
  are runtime data;
- temporary downloads and their final artifact are created on the same
  filesystem so successful validation can use atomic promotion;
- manifests refer to opaque storage keys, never arbitrary absolute paths;
- project, job, import, and artifact IDs are validated before path resolution;
- every resolved descendant must remain under the canonical data root;
- incomplete temporary content is never exposed as a ready artifact.

## Privacy And Repository Boundary

The local data root may contain private sketches, property context, generated
exports, provider snapshots, and location-identifying pixels. It must never be
staged, logged as content, embedded into frontend source, or copied into test
fixtures.

Tracked spatial material is limited to explicitly reviewed public samples and
fully synthetic fixtures under `tests/fixtures/`. The legacy
`mapa/sources/`, `mapa/assets/`, and ignored `mapa/manual-overlays.json` remain
reference inputs until cutover; they are not silently migrated or moved by
normal startup.

Legacy import is an explicit user action. It reads the selected source,
previews and reports the result, writes new backend-owned state under the data
root, and never modifies or deletes the source file.

## Startup And Failure Behavior

- Startup creates the configured root and required subdirectories when
  permitted.
- Startup fails with a contextual configuration error when the root cannot be
  resolved, created, or written.
- The adapter writes metadata through temporary files plus atomic replacement.
- Restart recovery inspects manifests and marks interrupted jobs without
  promoting partial content.
- Quotas are evaluated before and during writes; exceeding one preserves the
  last valid state and reports the limiting budget.
- Cleanup targets only validated descendants of `tmp/` and never follows an
  unresolved user-controlled path.

Backup, retention, encryption-at-rest, and migration between local filesystem
and object/database storage are deployment decisions for later plans.
