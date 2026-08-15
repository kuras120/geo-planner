---
name: maintain-docs
description: Create or update durable repository documentation so it matches implemented behavior. Use when behavior, configuration, architecture, data meaning, setup, verification, portability, research conclusions, or repository routing changes.
---

# Protocol C: Documentation

## Primary Guide

- `docs/guidelines/engineering-guide.md` defines the structure and quality
  rules for technical documentation.

1. Read the implementation and every document routed for the affected area; describe observed behavior, not intentions.
2. Keep the root README lean: purpose, safety boundary, quick start, and essential durable entry points. Do not make temporary project files permanent navigation.
3. Follow repository-defined document ownership. When the repository uses the conventional `docs/` layout, keep commands in its repository guide, functional requirements in `requirements/`, invariants and terminology in `domain/`, design flow in `architecture/`, reusable evidence in `research/`, and temporary delivery state in `projects/`.
4. Distinguish current support, known limitations, and proposals. Add dates and source links to time-sensitive research.
5. Update all affected links and commands. Mark generated artifacts clearly and do not edit them as source.
6. Run the repository-defined verification entry point and check Markdown links and paths before closeout.
7. Remove an accepted temporary project file only after durable documentation contains its lasting decisions.
8. Treat `docs/projects/**` as temporary and one-way: plans may reference durable docs, but root guidance, skills, durable docs, and other plans must not link to a specific project file.
