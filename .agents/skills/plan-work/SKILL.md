---
name: plan-work
description: Plan non-trivial repository changes before implementation. Use when a request changes behavior, data contracts, architecture, integrations, portability, or multiple repository areas and needs an explicit proposal with decisions, risks, stages, verification, and acceptance criteria.
---

# Protocol A: Planning

## Primary Guidance

Read `docs/guidelines/project-lifecycle.md` completely. It is the authoritative
contract for project scope, decision gates, approval, status, progress, and
closeout. Use `docs/guidelines/research-guide.md` as the second primary guide
when the project creates or depends on bounded research.

1. Read `AGENTS.md` and every document it routes for the affected area.
2. Inspect implemented behavior and current worktree state. Separate facts, assumptions, and open decisions.
3. Create one cohesive proposal under `docs/projects/` using `docs/guidelines/project-lifecycle.md`.
   The plan may reference durable docs, but do not link another project plan and do not add inbound links from durable docs, README, AGENTS, or skills.
4. Include the problem, outcome, scope, non-goals, data/runtime flow, failure behavior, migration impact, stages, tests, acceptance criteria, and unresolved choices when applicable.
5. Prefer reversible stages and preserve user data and external evidence. Flag network calls, destructive operations, and data regeneration separately.
6. Keep the project `PROPOSED` until the owner approves it for implementation or explicitly requests planning and execution together for a named scope. The combined request lets it enter `APPROVED FOR IMPLEMENTATION`; ordinary reversible decisions stay inside that scope, but a newly discovered material owner decision still blocks dependent work until accepted. Editing, reviewing, or expanding a plan does not change its phase.
7. Keep progress markers current during extended work. After acceptance and closeout, transfer lasting decisions, limitations, and safety boundaries to their durable domain, architecture, requirements, research, or guideline owners and remove the temporary proposal.
