---
name: plan-work
description: Plan non-trivial Geo Planner changes before implementation. Use when a request changes behavior, data contracts, architecture, source acquisition, portability, or spans multiple repository areas and needs an explicit proposal with decisions, risks, stages, verification, and acceptance criteria.
---

# Protocol A: Planning

1. Read `AGENTS.md` and every document routed for the affected area.
2. Inspect implemented behavior and current worktree state. Separate facts, assumptions, and open decisions.
3. Create one cohesive proposal under `docs/projects/` using `docs/guidelines/project-lifecycle.md`.
4. Include the problem, outcome, scope, non-goals, data/runtime flow, failure behavior, migration impact, stages, tests, acceptance criteria, and unresolved choices.
5. Prefer reversible stages and preserve current project data. Flag any network call or data regeneration separately.
6. Do not implement while the proposal is only `PROPOSED`, unless the owner explicitly requested planning and execution together.
7. Keep progress markers current during extended work. After acceptance and closeout, transfer durable decisions to domain/guideline docs and remove the temporary proposal.
