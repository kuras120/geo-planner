---
name: audit-docs
description: Audit and compact Geo Planner documentation while preserving durable decisions and evidence. Use when the owner requests a documentation review or cleanup, after several documentation-heavy changes, before a milestone, or when README/AGENTS/docs/skills appear duplicated, stale, overgrown, misrouted, or hard to maintain.
---

# Documentation Audit

Reduce documentation entropy. Prefer one authoritative home for each fact or rule and delete repetition after preserving unique evidence.

## Guardrails

- Read `AGENTS.md`, `docs/guidelines/project-lifecycle.md`, and `.agents/skills/maintain-docs/SKILL.md`.
- Do not modify `AGENTS.md` without explicit owner authorization for the exact change.
- Preserve user edits and sourced evidence. Do not delete an active project merely to reduce file count.
- Never add a durable inbound link to a specific `docs/projects/**` file.
- Treat line count as a signal, not a target. Clarity and ownership matter more than arbitrary brevity.

## Audit

1. Inventory README, AGENTS, every `docs/**` file, and every repository skill. Record line counts, headings, links, status/date, and likely owner category.
2. Assign one responsibility:
   - README: purpose, safety, quick start, essential entry points;
   - AGENTS: owner-approved permanent agent policy and routing;
   - domain: current terminology, contracts, invariants, and meaning;
   - architecture: current or target runtime/data flow and boundaries;
   - guidelines: reusable ways of working and engineering standards;
   - research: dated evidence, comparison, conclusion, uncertainty, and sources;
   - requirements: evidence-backed functional value after authorized discovery;
   - projects: temporary bounded delivery state;
   - skills: concise reusable procedures.
3. Flag:
   - the same rule or decision in multiple owners;
   - proposals presented as current behavior;
   - plans or implementation sequences inside research/guidelines;
   - one-off tasks inside AGENTS;
   - detailed research/project links in root README;
   - stale open questions, completed remediation history, orphan files/links;
   - specific project links outside their own plan;
   - long prose that repeats a table or conclusion.
4. For each flag choose `keep`, `move`, `merge`, `compress`, `delete`, or `leave temporary`.

## Cleanup Order

1. Preserve unique facts, decisions, dates, sources, warnings, and accepted constraints in their authoritative owner.
2. Replace duplicate prose with a link only when both documents are durable and the dependency is stable.
3. Remove plan/checklist language from research after its conclusion is durable.
4. Compress old audits to the current finding, lasting boundary, and reusable gate; drop superseded operational narration.
5. Keep project plans until implementation and owner acceptance. Then move lasting decisions and delete the plan.
6. Do not create an audit report document unless the owner requests one; summarize findings in the task result.

## Verification

- Search for removed filenames, duplicate key phrases, specific `docs/projects/*.md` inbound links, unresolved TODOs, and broken relative Markdown targets.
- Compare pre/post line counts and explain material deletions.
- Run `git diff --check`, validate changed skills, and run `./scripts/verify.sh`.
- Report each document as retained, compressed, merged, deleted, or temporary, plus any remaining ambiguity requiring owner judgment.
