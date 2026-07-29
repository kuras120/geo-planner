# Spatial Analysis Requirements

## Application Area

Measurements and comparisons derived from accepted source layers and
user-authored geometries. Layer viewing, source acquisition, and sketch
lifecycle belong to separate application areas.

## Requirement Index

| ID | Delivery stage | Status | Priority | Capability |
| --- | --- | --- | --- | --- |
| `ANALYSIS-001` | `STAGE-3` | `ACCEPTED` | `MUST` | Calculate sketch overlap with planning zones and land classes |

## ANALYSIS-001 — Calculate sketch overlap with planning zones and land classes

- Status: ACCEPTED
- Priority: MUST
- Delivery stage: STAGE-3
- Source evidence: owner request from 2026-07-25; manual-overlay selection in
  `mapa/map-fragment.template.html`; APP parsing in
  `mapa/scripts/build_map.py`; configured parcel percentages in
  `mapa/project-config.json`; KIEG `uzytki,kontury` display snapshot from
  2026-07-24.

### Outcome

A property owner selects a polygon sketch and receives source-qualified area
and percentage overlaps with planning zones, OUZ, and available vector EGiB
land classes.

### Contract

- Input: valid sketch Polygon and covering source geometry in one explicit CRS.
- Sources: APP `StrefaPlanistyczna`, APP `ObszarUzupelnieniaZabudowy`, and an
  authoritative vector EGiB land-use/classification dataset.
- Output: sketch area; area and percentage per category; uncovered area; source
  identity, date, and legal/draft status.
- KIEG `uzytki,kontury` raster may support display but not authoritative
  intersection calculations.

Example:

```text
Sketch area: 1,240 m²
General-plan draft 2026-06-17: 108SJ — 82.7%; 39SO — 17.3%
OUZ: 65.6%
EGiB snapshot: RIIIb — 220 m² (17.7%); RIVb — 1,020 m² (82.3%)
```

### Acceptance Criteria

- Calculated category areas reconcile with covered sketch area within an
  accepted tolerance; values never come from configured parcel percentages.
- Partial coverage is reported as uncovered, not zero or an inferred category.
- Results identify source snapshots and distinguish draft from adopted planning
  data.
- Invalid geometry or calculation failure preserves the sketch and clears stale
  results.
- Raster-only land classes never produce authoritative percentages.
- Planning, cadastral, and manual evidence remain visibly distinct; no result
  claims building rights or resolves agricultural-land obligations.

### Open Decisions

- Select a lawful vector EGiB source with required attributes and currency.
- Set numeric tolerance and minimum sliver area.
- Decide whether point/line analysis belongs in this requirement.
