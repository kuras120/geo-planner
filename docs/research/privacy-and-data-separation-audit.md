# Privacy And Data Separation Audit

## Status And Scope

- Audit date: 2026-07-20
- Scope: working tree, ignored IDE files, generated outputs, raster metadata, Git history, commit metadata, and configured GitHub remote.
- Method: filename and content inspection, targeted searches for identifiers and secrets, image metadata inspection, and Git object/history review.
- Limitation: this is a repository exposure review, not a legal assessment or proof that every image contains no visually identifying detail.

## Executive Finding

The local commit created from the initial project snapshot was not anonymized: it combined public spatial data with private person/property context. The GitHub repository is public, but the private commit is one commit ahead of `origin/master` and was not pushed. A content scan of `origin/master` found none of the private case strings identified by this audit.

The required containment action is therefore to avoid pushing the old local commit, stage the sanitized tree, and amend that local commit before publication. No remote history rewrite is required for the private case data under the confirmed branch state.

## Findings

| Severity | Location | Finding | Consequence |
| --- | --- | --- | --- |
| High | Local Git commit | The unpushed commit at the time of audit contains private person/property metadata and overlay content. | Pushing it would publish the data; amending it locally prevents that commit from entering the branch history. |
| Verified clean for identified case strings | `origin/master` content | The public remote branch contains only the earlier initial commit, and the targeted content scan found none of the audited private case strings. | No public exposure of the private case data was confirmed. |
| High | Initial `mapa/project-config.json` | Private legal/property status and a planned action linked to a named third party appeared beside exact public spatial identifiers. | Connected identifiable people and private intentions to exact land. |
| High | Initial `mapa/manual-overlays.json` | Personal identifiers, private legal/property notes, access arrangements, and private drainage/utility sketches were tracked. | Revealed relationships, negotiations, infrastructure, and intended use of specific land. |
| High | `mapa/map-fragment.html`, `mapa/mapa-ciezkowice.html` | Generated standalone files duplicate configuration, vectors, overlay descriptions, coordinates, and embedded raster imagery. | A single shared HTML file discloses most of the project without requiring source files. |
| Medium | `mapa/sources/**`, `mapa/assets/**` | Exact parcel geometry, TERYT/parcel identifiers, coordinates, orthophoto and infrastructure rasters for the selected area. No private-person attributes were found in the official GML snapshot. | Exact location can remain identifiable even after names are removed. Raster pixels may expose buildings and infrastructure. |
| Medium | Git commit metadata | The public initial commit contains personal author identity/contact metadata. | This is a separate public-identity choice; removing it would require rewriting the already-pushed root commit. |
| Low | Local unpushed reusable files | A local account path and a person-specific UI example existed in the unpushed commit. | They are removed by amending the local commit before push. |

No credentials, API tokens, private keys, PESEL/NIP-like identifiers, or telephone numbers were found. The inspected PNG files did not contain EXIF or author metadata; this does not make their geographic content anonymous.

## Current-Tree Remediation

The approved MVP boundary was implemented on 2026-07-20: public spatial data remains, private project metadata was neutralized, local overlays and generated HTML were removed from the Git index and ignored, a tracked empty initializer was added, and reusable personal/local-environment references were removed. The local overlay file was preserved unchanged. The sanitized snapshot must replace the unpushed local commit through `git commit --amend` before push.

## Required Separation Model

The reusable product and a real analysis project should have different storage and publication boundaries:

```text
public application repository
  app code + schemas + generic source catalog + synthetic/demo project

local user workspace (ignored or external)
  manual overlays + generated exports + private notes
```

Classification should be explicit:

- **Public product data:** code, schemas, non-personal service definitions, documentation, and synthetic fixtures.
- **Public official data by MVP policy:** parcel/precinct identifiers, official geometry and source snapshots, coordinates, and raster previews, subject to attribution and licence review.
- **Private user data:** person names, relationships, legal context, ownership/acquisition assertions, manual sketches, generated exports, and loose notes.
- **Secrets:** credentials and private endpoints; these belong outside both Git and project JSON.

## Containment And Sanitization Plan

1. Do not push the unsanitized local commit or share generated HTML containing local overlays.
2. Amend the single unpushed local commit with the verified sanitized snapshot.
3. Keep `manual-overlays.json` local and ignored, initialized from a tracked empty example without replacing an existing user file.
4. Keep the approved public spatial example while removing personal identifiers, relationships, private legal context, and ownership/acquisition assertions.
5. Ensure generated exports and IDE state are ignored by default. Commit official source snapshots only under the documented MVP policy.
6. Remove personal examples and absolute home-directory paths from reusable files.
7. Rescan the amended branch relative to `origin/master`, then push only the sanitized commit.
8. Use non-personal metadata for the amended commit if desired and add automated secret/PII heuristics.

Amending the confirmed unpushed commit changes only local history and does not require a force-push. The superseded object may remain temporarily in the local reflog/object database, so it must not be restored or pushed. Rewriting the already-pushed root commit is a separate operation needed only if the owner also wants to replace its public author metadata.

## Publication Gate

The local change is ready to be pushed only when all of the following are true:

- a clean clone contains no person identifiers, private legal/property context, or local account paths;
- generated output cannot reintroduce private project content into tracked files;
- the public demo is synthetic or explicitly approved for publication;
- the branch reachable from `HEAD` contains none of the selected private paths or strings;
- source licences, attribution, and snapshot-publication decisions are documented;
- `HEAD` is exactly one sanitized commit ahead of `origin/master`.
