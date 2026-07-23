# Agent Briefing

Use this file to select repository context. Read every routed document for the touched area before planning, reviewing, or changing it. Keep detailed rules in `docs/**` and reusable work procedures in `.agents/skills/**`.

## Required Workflow

- For non-trivial work, use Protocol A (`$plan-work`) and follow `docs/guidelines/project-lifecycle.md`. An explicit request to plan and execute in one task counts as implementation authorization for that stated scope.
- Use Protocol B (`$implement-change`) for implementation, Protocol C (`$maintain-docs`) for durable documentation, Protocol D (`$triage-inbox`) for loose notes or `INBOX.md`, and `$review-kotlin-backend` for read-only principal-level backend review.
- Respect stream ownership: Codex implements the Angular frontend under owner review; the owner implements the Kotlin backend under Codex review. Do not modify backend production code unless explicitly requested for a named scope.
- Treat `AGENTS.md` as owner-controlled permanent policy. Do not add, remove, or change its content unless the owner explicitly asks for that exact AGENTS change or approves proposed wording. The default is to keep this file unchanged and put task-specific material in the appropriate documentation or temporary plan.
- When the owner changes a reusable way of working, persist the accepted rule in the appropriate durable documentation, reusable skill, or—only with explicit owner approval—`AGENTS.md`. Do not rely on conversational memory. Keep one-off scope and sequencing in temporary project plans.
- Keep active plans under `docs/projects/**`; remove completed plans only after accepted decisions are reflected in durable docs.
- Preserve existing user changes and do not refresh external map sources unless explicitly requested.
- Keep code and technical documentation in English. Preserve Polish user-facing map text and source terminology where it is part of the product or data.

## Repository Map

| Path | Responsibility |
| --- | --- |
| `README.md` | Project purpose, safety boundary, documentation links, and quick start. |
| `INBOX.md` | Unstructured owner input awaiting interactive classification. |
| `mapa/project-config.json` | Project identity, spatial extent, CRS, parcels, plan, services, raster files, and output name. |
| `mapa/map-config.json` | Presentation and initial layer visibility only. |
| `mapa/manual-overlays.example.json` | Tracked empty initializer for local sketches. |
| `mapa/manual-overlays.json` | Ignored local user sketches; treat as private user data. |
| `mapa/map-fragment.template.html` | Reusable browser interface and local sketch editor. |
| `mapa/map-fragment.html`, `mapa/*.html` | Generated outputs; do not edit manually. |
| `mapa/scripts/build_map.py` | Configuration validation, source parsing, data embedding, and HTML generation. |
| `mapa/scripts/update_sources.py` | Explicit network refresh of parcels, plan, and rasters. |
| `mapa/scripts/edit_map_server.py` | Loopback-only editor persistence, rebuilding, and hot reload. |
| `mapa/sources/**`, `mapa/assets/**` | Downloaded source data bound to the configured bbox and CRS. |
| `tests/**` | Configuration, geometry, and workflow regression tests. |
| `scripts/verify.sh` | Offline repository verification. |
| `docs/domain/**` | Spatial concepts, data contracts, invariants, and safety meaning. |
| `docs/guidelines/**` | Setup, engineering standards, lifecycle, and verification. |
| `docs/architecture/**` | Runtime and data-flow descriptions. |
| `docs/projects/**` | Temporary proposals and active implementation plans. |
| `docs/research/**` | Durable investigations, source evaluations, and candidate layers. |
| `.agents/skills/**` | Reusable planning, implementation, documentation, triage, and backend-review protocols. |

## Task Routing

| Task or touched area | Read before work |
| --- | --- |
| Any repository change | `docs/guidelines/repository-guide.md` and `docs/guidelines/engineering-guide.md` |
| Project config, parcels, CRS, bbox, plan, overlays, or spatial parsers | `docs/domain/map-domain.md` |
| Build, generated HTML, map template, browser editor, or local server | `docs/domain/map-domain.md` and `docs/architecture/map-build-flow.md` |
| Source URLs, downloads, WMS/ULDK/GML, or new layers | `docs/domain/map-domain.md` and relevant `docs/research/**` notes |
| Target runtime, shared API contracts, acquisition jobs, or persistence evolution | `docs/architecture/target-product-architecture.md` |
| Requirements discovery or writing | `docs/guidelines/requirements-guide.md`; create requirement files only after owner-authorized discovery |
| Angular feature, API call, component, state, OpenLayers adapter, or frontend test | `docs/guidelines/angular-engineering-guide.md`, `docs/architecture/target-product-architecture.md`, and a new feature-specific `docs/projects/**` plan |
| Planned Kotlin/Spring backend, provider adapters, or persistence | accepted functional requirements when available, `docs/guidelines/engineering-guide.md`, `docs/guidelines/kotlin-backend-engineering-guide.md`, `docs/architecture/target-product-architecture.md`, `docs/research/backend-technology-options.md`, and `docs/research/current-public-integrations.md` |
| Kotlin/Spring backend review | `$review-kotlin-backend` and its routed backend documents |
| Non-trivial planning and delivery | `docs/guidelines/project-lifecycle.md` and matching `docs/projects/**` file |
| Loose notes, links, ideas, or requirements | `INBOX.md`, `$triage-inbox`, and relevant requirement/domain/research docs |
| Documentation or repository routing | `$maintain-docs` plus implemented behavior and affected durable docs |

## Repository-Specific Instructions

- Treat ignored `manual-overlays.json` as private local user data. Never stage, clear, normalize, or replace it unless explicitly requested.
- A raster is valid only for the bbox and CRS used when it was downloaded; rebuild alone does not reproject it.
- Generated HTML is ignored because it embeds current source and local overlay data. Regenerate it after changing configuration, sources, templates, or overlays.
- Do not claim legal, cadastral, utility, or planning certainty from preview layers. Preserve source dates and uncertainty.
- Keep network refresh separate from offline verification so tests cannot silently replace checked-in evidence.
