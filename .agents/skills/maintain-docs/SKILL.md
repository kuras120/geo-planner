---
name: maintain-docs
description: Create or update durable repository documentation so it matches implemented behavior. Use when behavior, configuration, architecture, data meaning, setup, verification, portability, research conclusions, or repository routing changes.
---

# Protocol C: Documentation

## Primary Guide

- `docs/guidelines/engineering-guide.md` defines the structure and quality
  rules for technical documentation.

1. Read `AGENTS.md`, the implementation, and every document it routes for the affected area; describe observed behavior, not intentions.
2. Keep the root README lean: purpose, safety boundary, quick start, and essential durable entry points. Do not make temporary project files permanent navigation.
3. Follow repository-defined document ownership. When the repository uses the conventional `docs/` layout, keep commands in its repository guide, functional requirements in `requirements/`, invariants and terminology in `domain/`, design flow in `architecture/`, reusable evidence in `research/`, and temporary delivery state in `projects/`.
4. Treat `AGENTS.md` as owner-controlled permanent policy. Never modify it unless the owner explicitly requests that exact change or approves proposed wording. Keep task-specific or temporary instructions elsewhere.
5. Distinguish current support, known limitations, and proposals. Add dates and source links to time-sensitive research.
6. Update all affected links and commands. Mark generated artifacts clearly and do not edit them as source.
7. Run the repository-defined verification entry point and check Markdown links and paths before closeout.
8. Remove an accepted temporary project file only after durable documentation contains its lasting decisions.
9. Treat `docs/projects/**` as temporary and one-way: plans may reference durable docs, but README, AGENTS, skills, durable docs, and other plans must not link to a specific project file.
