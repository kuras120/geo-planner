# Geo Planner

Geo Planner is being rebuilt as an Angular client backed by a Kotlin/Spring
Boot application. The current repository contains the application foundation;
the target product will organize map evidence, projects, acquisition, sketches,
and spatial analysis while preserving provenance and uncertainty.

Government, cadastral, planning, utility, and derived layers are informative
unless an authoritative source and validation process explicitly establish
otherwise. Sketches are not surveying or legal evidence.

The Python/HTML implementation under `mapa/**` remains available as the legacy
application and as migration evidence until its capabilities are replaced.
Its operating instructions live in `mapa/README.md`.

## Quick Start

```bash
mise install
mise run setup
mise run backend
mise run frontend
```

Run `mise run simulator` instead of the backend for frontend work against
accepted deterministic contract scenarios. Run the UI workshop with
`mise run storybook`.

The repository-wide verification entry point is:

```bash
mise run verify
```

Use `mise run assemble` to produce backend and frontend application artifacts.

## Documentation

- [Repository setup and commands](docs/guidelines/repository-guide.md)
- [Engineering standards](docs/guidelines/engineering-guide.md)
- [Target product architecture](docs/architecture/target-product-architecture.md)
- [Map domain and safety contracts](docs/domain/map-domain.md)
- [Requirements portfolio](docs/requirements/index.md)
- [Project lifecycle and work protocols](docs/guidelines/project-lifecycle.md)
- [Legacy map operation](mapa/README.md)
