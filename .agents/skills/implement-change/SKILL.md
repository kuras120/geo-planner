---
name: implement-change
description: Implement an approved or explicitly requested Geo Planner change with controlled scope and proportionate verification. Use when modifying map generation, configuration, source downloads, the browser editor, spatial parsers, tests, scripts, or other repository behavior.
---

# Protocol B: Implementation

1. Read `AGENTS.md`, the repository and engineering guides, relevant domain docs, and the approved project file when one exists.
2. Confirm the requested scope and inspect existing user changes before editing.
3. Implement in small vertical slices. Keep location-specific values in `mapa/project-config.json`, presentation settings in `mapa/map-config.json`, and reusable behavior in scripts/templates.
4. Validate external input at boundaries. Never overwrite manual overlays or source data as an incidental fallback.
5. Add regression coverage for parsing, configuration, persistence, and public-interface changes.
6. Run `./scripts/verify.sh`. Do not download fresh government data during verification; use checked-in fixtures unless regeneration was explicitly requested.
7. Update the active project file with deviations and results. Report changed behavior, verification, manual checks, limitations, and follow-ups.
