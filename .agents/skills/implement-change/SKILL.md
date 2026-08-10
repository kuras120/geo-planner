---
name: implement-change
description: Implement an approved or explicitly requested repository change with controlled scope and proportionate verification. Use when changing application behavior, configuration, integrations, tests, scripts, or other repository-owned behavior.
---

# Protocol B: Implementation

1. Read `AGENTS.md` and every document it routes for the affected area, including the active approved project file when one exists.
2. Confirm the requested scope and inspect existing user changes before editing.
3. Implement in small vertical slices. Follow repository-owned boundaries for configuration, code, generated artifacts, and user data instead of inventing new ownership rules in the skill.
4. Validate external input at boundaries. Preserve user data and external evidence; never overwrite either as an incidental fallback.
5. Add regression coverage for changed behavior, especially configuration, parsing, persistence, integration, and public-interface defects.
6. Run the repository verification entry point defined by `AGENTS.md` or its routed repository guide. Keep network refresh, destructive regeneration, and live external calls outside verification unless explicitly authorized.
7. Update the active project file with deviations and results. Report changed behavior, verification, manual checks, limitations, and follow-ups.
