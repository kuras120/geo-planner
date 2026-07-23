---
name: maintain-docs
description: Create or update durable Geo Planner documentation so it matches implemented behavior. Use when behavior, configuration, architecture, data meaning, setup, verification, portability, research conclusions, or repository routing changes.
---

# Protocol C: Documentation

1. Read the implementation and existing docs; describe observed behavior, not intentions.
2. Keep the root `README.md` lean: purpose, safety boundary, quick start, and only essential documentation entry points. Do not add links to individual project, research, or requirement files.
3. Put operational commands in `docs/guidelines/repository-guide.md`; evidence-backed functional stories in `docs/requirements/` only after owner-authorized discovery and according to `docs/guidelines/requirements-guide.md`; invariants and terminology in `docs/domain/`; design flow in `docs/architecture/`; reusable investigations in `docs/research/`.
4. Treat `AGENTS.md` as owner-controlled permanent policy. Never modify it unless the owner explicitly requests that exact change or approves proposed wording. Keep task-specific or temporary instructions elsewhere.
5. Distinguish current support, known limitations, and proposals. Add dates and source links to time-sensitive research.
6. Update all affected links and commands. Keep generated HTML clearly marked as generated.
7. Run repository verification and check Markdown links/paths before closeout.
8. Remove an accepted temporary project file only after durable documentation contains its lasting decisions.
9. Treat `docs/projects/**` as temporary and one-way: plans may reference durable docs, but README, AGENTS, skills, durable docs, and other plans must not link to a specific project file.
