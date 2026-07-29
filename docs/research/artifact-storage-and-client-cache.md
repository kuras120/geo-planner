# Artifact Storage And Client Cache

## Status

Deployment concern recorded on 2026-07-28. The owner correctly identified that
several acquisitions per user can reach multiple gigabytes. Exact browser-cache
and hosted-retention design is deferred to the acquisition/deployment slices.

## Physical Versus Logical Location

The local MVP backend runs on the user's machine. Its
`.geo-planner-data/` root is therefore physically client-local even though the
backend remains the logical authority for manifests, overlays, and artifacts.
This avoids central storage cost without making browser state authoritative.

For a hosted deployment, large artifacts belong in quota-controlled object
storage or an equivalent persistent artifact service. The application server
filesystem is temporary execution space, not a multi-gigabyte per-user archive.

## Browser Storage

OPFS, IndexedDB, and Cache API can support a recoverable offline/hot-tile cache,
but not the sole authoritative copy:

- quotas and persistence policy differ by browser and device;
- writes can fail with `QuotaExceededError`;
- non-persistent origins may be evicted under storage pressure;
- clearing site data also clears origin-private data;
- private browsing has different, usually temporary behavior;
- origin-scoped storage complicates backup, migration, and access from another
  device or deployment origin.

Any future browser cache must:

- check estimated usage/quota and request persistence when appropriate;
- enforce its own per-project/global limits and least-recently-used cleanup;
- store only reconstructible artifacts or explicit offline packages;
- never be the only copy of overlays, project manifests, or accepted
  acquisition records;
- show offline availability and eviction/download state to the user.

## SaaS Delivery Candidate

The browser should retrieve only the resolution and spatial fragments needed
for the current viewport, not a complete acquired raster:

```text
validated source artifact
  -> tiled raster with reduced-resolution overviews
  -> object storage
  -> CDN/range or tile endpoint
  -> OpenLayers requests visible zoom/viewport fragments
  -> bounded reconstructible browser cache
```

Two candidates require implementation-slice evaluation:

- Cloud Optimized GeoTIFF with internal/external overviews and HTTP Range;
- a derived XYZ/WMTS-style tile pyramid, normally 256² or 512² display tiles.

COG preserves one georeferenced artifact and lets a capable client request byte
ranges for only the needed tiles/overview. A tile pyramid makes CDN/browser
caching and authorization straightforward but creates derived objects and
requires a defined tile matrix. The selected layer may use either delivery
shape behind the same frontend layer descriptor.

Cross-user deduplication is an optional optimization, not the SaaS cost model.
Two users choosing the same parcel or exact AOI may be uncommon. Reuse is more
plausible when public raster content is stored in a stable provider-aligned
tile grid keyed by source, layer/style, source version, CRS, resolution/zoom,
and tile coordinate. Overlapping or nearby AOIs can then reference some of the
same immutable tiles without knowing anything about each other's projects.

The hit rate depends on geographic clustering, upstream determinism, update
cadence, licence, and chosen grid. AOI-specific COGs may have little or no reuse
beyond exact content-addressed duplicates. Capacity planning must therefore
assume no cross-user reuse and rely on quotas, retention, cold cleanup, and
explicit offline/export behavior. Deduplication or CDN hits only improve that
baseline.

Large vector sources should similarly use bounded AOI responses or vector tiles
rather than one nationwide GeoJSON response.

Docker images contain application code and a default catalog, not acquired user
rasters. Local/self-hosted delivery mounts a data volume for
`.geo-planner-data/` or configures compatible object storage.

## Deferred Hosted Decisions

- per-user/project quotas and pricing boundary;
- retention and automatic cleanup;
- measured value of provider-grid or content-addressed deduplication;
- whether cold artifacts are regenerated, archived, or deleted;
- offline-package format and explicit user export/import;
- exact tile/range endpoint and browser-cache policy.

Primary browser-storage references:

- `https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria`
- `https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system`
- `https://web.dev/articles/origin-private-file-system`

Primary raster-delivery references:

- `https://docs.ogc.org/is/21-026/21-026.html`
- `https://openlayers.org/en/latest/examples/cog-overviews.html`
- `https://openlayers.org/en/latest/apidoc/module-ol_source_TileWMS-TileWMS.html`
- `https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/RangeGETs.html`
