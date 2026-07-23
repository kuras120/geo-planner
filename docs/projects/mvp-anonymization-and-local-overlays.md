# MVP Anonymization And Local Overlays

## Status

- Phase: IMPLEMENTED
- Created: 2026-07-20
- Authorization: the owner explicitly approved this privacy boundary and requested implementation.

## Problem And Outcome

The current public project combines reusable code and public spatial data with private person/property context. Manual overlays and generated HTML can reproduce private notes in tracked files.

For the MVP, parcel identifiers, precinct identifiers, official source files, coordinates, and raster previews may remain public. Names, personal relationships, legal-purpose context, ownership/acquisition assertions, and private notes must not be part of the tracked current version.

## Scope And Non-goals

In scope:

- replace private parcel metadata and reusable UI examples with neutral analysis terminology;
- keep `manual-overlays.json` as local user data ignored by Git;
- create a missing local overlay file automatically from a tracked empty example;
- ignore generated HTML because it embeds local overlays;
- document the lifecycle and add regression tests.

Non-goals:

- removing public cadastral identifiers, geometry, rasters, or official planning data;
- rewriting the already-pushed root commit or changing remote visibility;
- introducing accounts, cloud persistence, or a database;
- refreshing external map sources.

## Decisions And Data Flow

`manual-overlays.example.json` is a tracked, neutral, empty `FeatureCollection`. On build, an existing `manual-overlays.json` is loaded unchanged. If it is missing, the builder creates it exclusively from the example, then embeds it into local generated HTML. The loopback editor continues to save it atomically.

```text
tracked empty example
  -> first build creates ignored manual-overlays.json
  -> editor updates ignored local file
  -> build embeds it in ignored generated HTML
```

The existing local overlay file is preserved. Removing it from the Git index is not permission to delete or reset its contents.

## Implementation Plan

1. [done] Sanitize current project metadata and reusable UI text.
2. [done] Add the tracked empty overlay example and first-run initialization.
3. [done] Ignore and untrack local overlays and generated HTML while retaining working files.
4. [done] Update domain, architecture, setup, and agent-routing documentation.
5. [done] Run tests, offline build verification, tracked-current-tree privacy scan, and ignore checks.

## Failure And Safety Behavior

- A present local overlay file is never replaced during initialization.
- Invalid existing JSON fails visibly instead of being reset.
- Concurrent first builds tolerate another process creating the local file first.
- Generated HTML remains shareable only by an explicit user action and is not staged by default.
- The confirmed unpushed commit may be amended; rewriting pushed history remains a separate operation.

## Verification And Acceptance

- first build creates a missing overlay file with an empty feature list;
- a pre-existing overlay survives build byte-for-byte in meaning;
- Git ignores the local overlay and generated HTML files;
- current tracked content contains no person names or private legal-purpose terminology identified by the audit;
- `./scripts/verify.sh` passes without network access.

## Result

- Parcel, precinct, source, coordinate, and raster data remain in the public MVP scope.
- Current project metadata uses neutral `focus`/`context` classification and contains none of the private strings identified by the audit.
- `manual-overlays.json` and generated HTML were removed from the Git index and are ignored; the pre-existing local overlay retained its SHA-256 checksum during migration and verification.
- A missing overlay is initialized from `manual-overlays.example.json`; regression tests cover creation and preservation.
- `./scripts/verify.sh` passes with 11 tests and no network access.
- Known private identifiers do not occur in the current non-ignored tree. The unsanitized commit was confirmed as local-only and is replaced by amending it before push.
