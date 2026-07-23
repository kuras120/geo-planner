# Documentation System Audit

## Status

- Phase: IMPLEMENTED — AWAITING OWNER ACCEPTANCE
- Created: 2026-07-24
- Authorization: the owner explicitly requested the audit, cleanup, AGENTS policy update, and reusable audit skill in one task.

## Outcome

Make repository documentation concise, non-overlapping, correctly routed, and removable where temporary. Preserve durable decisions and sourced research while removing repeated plans, policies, and obsolete operational history.

## Scope

- audit README, AGENTS, all `docs/**`, and repository skills;
- assign one responsibility to every durable document category;
- compress overlapping research and remove plan/guideline content from it;
- verify active project files remain temporary and have no durable inbound links;
- create and validate a reusable documentation-audit skill;
- verify links and repository tests.

## Plan

1. [done] Inventory files, headings, line counts, links, status, and ownership.
2. [done] Add the owner-approved permanent-memory policy to AGENTS.
3. [done] Compress and de-duplicate research and architecture boundaries.
4. [done] Create and validate `$audit-docs`.
5. [done] Re-run structural scans, skill validation, and `./scripts/verify.sh`.
6. [done] Record the result and await owner acceptance before deleting this plan.

## Acceptance

- README stays visitor-focused and lean.
- AGENTS contains only permanent policy and routing.
- Domain, architecture, guideline, research, requirement, and project responsibilities do not overlap materially.
- Research retains source/date/decision evidence without embedding delivery plans.
- Every active project is bounded, temporary, and unreferenced by durable docs.
- Documentation line count decreases without losing unique durable decisions.
- The audit skill validates and repository verification passes.

## Result

- README remains a visitor-focused quick start with five durable entry points.
- AGENTS contains permanent workflow, ownership, safety, and routing rules only.
- Research retains decisions, dates, uncertainty, and sources; delivery sequences
  were removed or moved to their existing authoritative guides.
- Architecture owns target boundaries without duplicating the Angular migration
  procedure.
- The two migration/foundation plans remain proposed and temporary. This audit
  plan is also temporary and can be deleted after owner acceptance.
- Documentation and skill sources decreased from 1,974 to 1,740 lines despite
  adding this plan and the audit skill.
- All relative Markdown targets, the audit skill, repository tests, and offline
  map generation pass.
