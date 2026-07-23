---
name: maintain-docs
description: Create or update durable Geo Planner documentation so it matches implemented behavior. Use when behavior, configuration, architecture, data meaning, setup, verification, portability, research conclusions, or repository routing changes.
---

# Protocol C: Documentation

1. Read the implementation and existing docs; describe observed behavior, not intentions.
2. Put visitor-facing purpose and quick start in `README.md`; operational commands in `docs/guidelines/repository-guide.md`; invariants and terminology in `docs/domain/`; design flow in `docs/architecture/`; reusable investigations in `docs/research/`.
3. Keep `AGENTS.md` as a concise routing table. Do not duplicate detailed rules there.
4. Distinguish current support, known limitations, and proposals. Add dates and source links to time-sensitive research.
5. Update all affected links and commands. Keep generated HTML clearly marked as generated.
6. Run repository verification and check Markdown links/paths before closeout.
7. Remove an accepted temporary project file only after durable documentation contains its lasting decisions.
