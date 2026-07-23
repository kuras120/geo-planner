# Frontend Technology Options

## Status

Decision research for the future thin client. Revisit only when product
constraints or the selected mapping engine materially change.

## Recommendation

Use Angular with TypeScript and OpenLayers.

Angular fits the owner's experience and provides a coherent application
framework for a frontend expected to grow beyond a single map page. OpenLayers
matches the existing spatial workload: WMS, multiple projections, vector
features, raster overlays, editing, and explicit control over map behavior.

Durable implementation rules belong to
`docs/guidelines/angular-engineering-guide.md`; target system boundaries belong
to `docs/architecture/target-product-architecture.md`.

## Options Compared

| Option | Strengths | Main trade-off | Assessment |
| --- | --- | --- | --- |
| Angular + OpenLayers | Strong application structure, typed DI, mature routing/forms, broad GIS support | More framework ceremony than a small component library | Recommended |
| React + OpenLayers | Flexible composition, broad ecosystem, good TypeScript support | More architectural decisions must be standardized locally | Viable alternative |
| React + MapLibre GL JS | Excellent vector-tile rendering and modern styling | Existing WMS/raster/projection workflows need more adaptation | Reconsider for a vector-tile-first product |
| SvelteKit + OpenLayers | Compact components and good developer experience | Smaller team familiarity and fewer established enterprise conventions | Attractive, but not the best learning/product fit |
| Keep the generated HTML application | No migration cost | Increasing maintenance cost and weak application boundaries | Prototype only |

## Why OpenLayers Directly

An Angular wrapper would shorten a few templates but introduces another
compatibility and abstraction layer. Direct OpenLayers use behind
application-owned services and adapters keeps upgrades and advanced GIS
behavior under project control.

## Re-evaluation Triggers

Reassess the choice if:

- the primary delivery format becomes vector tiles;
- mobile-native delivery becomes a primary requirement;
- the application remains permanently small enough that a full framework is
  unjustified;
- OpenLayers drops a required projection, service, or editing capability.

## Primary References

- [Angular documentation](https://angular.dev/)
- [Angular update guide](https://angular.dev/update-guide)
- [OpenLayers documentation](https://openlayers.org/)
- [MapLibre GL JS documentation](https://maplibre.org/maplibre-gl-js/docs/)
- [React documentation](https://react.dev/)
- [Svelte documentation](https://svelte.dev/docs)
