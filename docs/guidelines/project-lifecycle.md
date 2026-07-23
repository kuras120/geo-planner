# Project Lifecycle And Protocols

Use this workflow for changes that affect behavior, data meaning, architecture, portability, external sources, or multiple repository areas. The reusable procedures are project skills under `.agents/skills/`.

## Protocol A: Planning (`$plan-work`)

Create one proposal in `docs/projects/` with status `PROPOSED`. Include:

- problem, outcome, scope, and non-goals;
- confirmed decisions, assumptions, and open questions;
- affected components and data/runtime flow;
- failure behavior, data-safety concerns, and migration impact;
- staged implementation plan;
- automated tests, manual spatial checks, and acceptance criteria.

A project file represents one bounded change, not a permanent roadmap or reusable execution loop. Close it after that outcome is accepted. A later substantial feature receives a new plan written from scratch, even when it follows the same delivery cadence or builds on the same foundation.

Project files may link outward to durable documentation. Do not create inbound links to a specific project file from `README.md`, `AGENTS.md`, skills, durable documentation, or another project plan. This keeps temporary plans removable after their decisions and implemented behavior have durable homes.

Implementation starts only after the owner explicitly approves it or explicitly requests planning and execution together for a named scope. The agent must not change a plan to `APPROVED FOR IMPLEMENTATION` based on discussion, review, plan edits, documentation requests, or inferred intent.

## Protocol B: Implementation (`$implement-change`)

Implement only the authorized scope, preserve user data, and keep the proposal current. Record material deviations and new risks. Finish with offline verification and identify any network refresh or visual alignment check that remains manual.

Set the project to `IMPLEMENTED` and report changed behavior, test results, manual checks, known limitations, and follow-ups. For owner-reviewed work, wait for implementation acceptance before final documentation cleanup.

## Protocol C: Documentation (`$maintain-docs`)

After implementation is accepted, update durable domain, guideline, architecture, and research documents to match behavior. Update visitor-facing README content when purpose, setup, or maturity changed. Remove the temporary proposal only after lasting decisions have a durable home.

## Protocol D: Inbox Triage (`$triage-inbox`)

`INBOX.md` accepts intentionally loose material. Triage it interactively into one primary destination:

| Class | Destination and expected shape |
| --- | --- |
| Requirement | After authorized discovery, a `docs/requirements/` domain file following `docs/guidelines/requirements-guide.md`. |
| Backlog | Project proposal candidate with value, rough scope, dependencies, and priority rationale. |
| Research | `docs/research/` question with provenance, evidence needed, and decision it informs. |
| Decision | Durable domain/guideline statement with rationale and date when time-sensitive. |
| Risk | Relevant project/domain doc with likelihood, impact, signals, and mitigation. |
| Archive | Marked duplicate, obsolete, or rejected note with a short reason. |

An inbox note is not verified fact or implementation authorization. Preserve original wording and provenance until classification is accepted. Process one coherent cluster at a time, ask the smallest useful question, write the destination, link it, and only then remove the inbox entry.

## Backend Principal Review (`$review-kotlin-backend`)

The owner implements the Kotlin backend. Codex reviews designs and changes without editing production code by default. Reviews lead with severity-ranked evidence and cover correctness, thin-client contracts, Kotlin semantics, Spring, Gradle Kotlin DSL, Kotest, security, persistence, and failure behavior.

Changing from review to implementation requires an explicit owner request naming the scope and then follows Protocol B.

## Project Template

```markdown
# <Change Name>

## Status
- Phase: PROPOSED | APPROVED FOR IMPLEMENTATION | IMPLEMENTED | APPROVED FOR DOCUMENTATION | DONE

## Problem And Outcome

## Scope And Non-goals

## Decisions, Assumptions, And Open Questions

## Data Or Runtime Flow

## Implementation Plan
1. [pending] <step>

## Verification And Acceptance
- `<command>`
- <manual spatial check>

## Result
- <temporary implementation summary>
```

Use `[pending]`, `[in-progress]`, and `[done]` so interrupted work can resume safely.
