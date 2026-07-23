# Privacy And Data Separation Audit

## Status

- Audit date: 2026-07-20
- Scope: tracked/ignored files, generated output, raster metadata, Git history, and configured remote.
- Limitation: repository exposure review, not a legal assessment or proof that raster pixels contain no identifying detail.

## Finding

The initial local, unpushed snapshot combined public spatial data with private person/property context. No exposure of the identified private case strings on the public remote branch was confirmed.

The sanitized repository boundary was implemented:

- public parcel/precinct identifiers, official geometry, coordinates, and approved raster previews may remain;
- person names, relationships, legal/property context, ownership/acquisition assertions, and private intentions are excluded;
- `manual-overlays.json` and generated HTML remain local and ignored;
- a missing overlay file initializes from a tracked empty example without replacing existing data;
- reusable files contain no personal examples or absolute home-directory paths.

No credentials, API tokens, private keys, PESEL/NIP-like identifiers, or telephone numbers were found during the audit. Inspected PNGs contained no EXIF/author metadata; their geographic pixels are still location-identifying.

## Durable Separation Model

```text
public application repository
  code + schemas + generic catalog + approved public/synthetic fixtures

local user workspace
  manual overlays + generated exports + private notes + future account data
```

| Class | Examples | Storage rule |
| --- | --- | --- |
| Public product | code, schemas, non-personal service definitions, docs | tracked |
| Approved public spatial sample | official identifiers, geometry, source snapshots, raster previews | tracked only after licence/attribution review |
| Private user data | names, relationships, legal context, sketches, generated exports | ignored/local or authenticated storage |
| Secrets | credentials and private endpoints | secret storage, never project JSON or Git |

## Publication Gate

- A clean clone contains no personal identifiers, private legal/property context, or local account paths.
- Generated output cannot reintroduce private content into tracked files.
- The public sample is synthetic or explicitly approved.
- Source licence, attribution, and snapshot-publication decisions are documented.
- History reachable from the branch intended for push contains none of the selected private paths or strings.
- Local overlays are never normalized, staged, replaced, logged, or exported without explicit user action.
