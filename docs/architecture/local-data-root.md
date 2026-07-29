# Local Data Root Contract

## Status

Accepted migration boundary for the future local-MVP and self-hosted backend.
The data root is one storage-adapter implementation, not the product's
commercial deployment contract. This describes storage ownership and safety;
it does not claim that the Kotlin persistence adapters exist.

## Deployment-neutral Storage Ports

Application and domain services must not depend on filesystem paths, Cloud
Storage, S3, or another provider SDK. They depend on two capability-oriented
ports:

- `RuntimeStateStore`: projects, AOI state, jobs, manifests, overlays,
  optimistic revisions, imports, and storage-schema version;
- `ArtifactStore`: bounded streaming write, abort, validated promotion,
  metadata/stat, ranged read, authorized delivery, and deletion by opaque key.

The first adapters are:

| Deployment | Runtime state | Large artifacts |
| --- | --- | --- |
| Local development / self-hosted | Files and manifests below the local data root | Files below the local data root |
| Hosted / commercial | PostgreSQL or another accepted durable state adapter | GCS/S3-compatible object storage adapter |

The ports own storage semantics, not vendor-shaped DTOs. In particular:

- services pass opaque IDs, streams, checksums, sizes, media types, and spatial
  metadata, never absolute paths, bucket URLs, or provider request objects;
- a successful promotion means a complete validated artifact becomes visible
  exactly once, even when an object store implements it through temporary keys
  and manifest state rather than filesystem rename;
- incomplete writes remain undiscoverable and can be cleaned up idempotently;
- ranged reads are supported when required by COG or tile delivery;
- quotas, authorization, retention, and encryption policy are applied at or
  above the port boundary and cannot be bypassed by selecting an adapter;
- provider-specific signed URLs are optional delivery results behind the
  adapter and never become durable domain identity.

Adapter selection is deployment configuration. Switching from filesystem to
object storage must not change project, acquisition, provenance, overlay, or
frontend API contracts. A migration command copies through the two ports,
verifies byte count and checksum, writes the destination manifest, and leaves
the source untouched until the operator separately accepts cleanup.

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

Backup duration, retention values, encryption keys, and the selected hosted
providers remain deployment decisions for later plans. The storage ports and
filesystem/object-store interchangeability are required architecture from the
first persisted slice.
