# Engineering Guide

## Design

- Keep project-specific facts in `project-config.json` and visual preferences in `map-config.json`.
- Keep download orchestration separate from deterministic building and verification.
- Validate configuration and external formats at their boundaries with contextual errors.
- Derive filenames, local-storage keys, editor URLs, bbox serialization, titles, and source text from configuration rather than duplicating them.
- Preserve a clear distinction between source data, owner metadata, and manual sketches.
- Prefer standard-library Python and browser APIs unless a dependency solves a demonstrated reliability problem.

## Spatial Data

- Make CRS and coordinate order explicit at every format boundary.
- Do not infer raster coverage from image dimensions; coverage comes from project configuration and acquisition parameters.
- Preserve polygon rings and multi-geometries. Add a fixture before extending a parser for a new WKT/GML variant.
- Reject ambiguous configuration instead of silently using a location-specific fallback.
- Treat visual alignment as a required manual check after source, bbox, CRS, or parser changes.

## Persistence And Safety

- Treat the ignored `manual-overlays.json` as local user data and write it atomically. Never stage it or generated HTML that embeds it.
- Bind the editor to loopback and validate request origin, body size, collection shape, and geometry type.
- Never run network refresh inside tests, normal builds, or hot reload.
- Do not replace a usable optional snapshot when its remote service is temporarily unavailable.

## Testing

- Unit-test configuration invariants, bbox axis order, supported WKT/GML coordinate variants, and unsafe paths.
- Add a regression test for every parsing, persistence, source-selection, or output-naming bug.
- Keep fixtures small. Use checked-in source snapshots only for build smoke verification.
- Finish changes with `./scripts/verify.sh` and report any manual spatial validation still required.

## Specialized Guides

- `angular-engineering-guide.md` defines Angular, API-client, component-composition, state, OpenLayers, and frontend testing standards.
- `kotlin-backend-engineering-guide.md` defines Kotlin semantics, Spring boundaries, Gradle Kotlin DSL, Kotest, and backend thin-client standards.

## Review Standard

Prioritize spatial misalignment, data loss, cross-project leakage, wrong-source attribution, unsafe filesystem paths, parser regressions, unexpected network calls, and claims stronger than their evidence. Require documentation changes when configuration ownership, supported formats, layer meaning, or runtime flow changes.
