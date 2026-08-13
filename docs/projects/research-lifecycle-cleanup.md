# Research Lifecycle Cleanup

## Status

- Phase: IMPLEMENTED
- Authorization: owner requested the audit, durable-rule update, and
  decision-gated cleanup on 2026-08-12.

## Problem And Outcome

`docs/research/**` mixes active investigations, durable evidence, completed
decision records, migration ledgers, and historical audits. The repository
needs a visible lifecycle for research and should retain a research file only
while its evidence or unresolved questions will be used again.

The outcome is a smaller research set in which every retained investigation
states the decision it informs, its progress, its durable outputs, and its
remaining return conditions. Completed research is removed only after unique
evidence and accepted/rejected-option rationale have an authoritative durable
home.

## Scope And Non-goals

In scope:

- classify every Markdown file under `docs/research/`;
- review one deletion/retention recommendation at a time with the owner;
- add a reusable research-lifecycle rule to durable guidance;
- move or compact unique conclusions before deleting completed research;
- repair references and verify the documentation and repository.

Out of scope:

- refreshing live external sources or prices;
- changing product requirements, architecture, or implementation decisions;
- modifying the legacy application or private local data;
- deleting migration evidence before its dependent parity/cutover gate closes.

## Decisions, Assumptions, And Open Questions

- Confirmed: owner decisions are taken one research file at a time.
- Confirmed: deletion requires a durable home for the selected path and the
  material rationale for rejected alternatives.
- Confirmed: research that will be revisited remains, with links showing what
  is complete and what question or trigger remains.
- Accepted 2026-08-12: close `frontend-technology-options.md` after preserving
  the selected Angular/OpenLayers path, rejected-alternative rationale, and
  re-evaluation triggers in target architecture.
- Accepted 2026-08-12: close `backend-technology-options.md` after preserving
  the Kotlin/Spring MVC decision, rejected-alternative rationale, and
  infrastructure triggers in target architecture. The owner explicitly did
  not select a modular monolith; enforced domain modules remain conditional on
  demonstrated multi-domain boundaries.
- Accepted 2026-08-12: close `PORTABILITY-AUDIT.md` after preserving the
  verified synthetic-fixture result and the boundary between portable legacy
  assembly and specialized acquisition in `mapa/README.md`.
- Accepted 2026-08-13: delete `privacy-and-data-separation-audit.md` without
  creating broader storage restrictions. Its completed scope was removing
  private material from tracked repository content. Authorized PostgreSQL and
  artifact storage may retain user analyses and user-selected names under the
  product's access controls.
- Accepted 2026-08-13: delete `prototype-assumption-register.md` without
  copying its resolved decision clusters. Their accepted outcomes already live
  in architecture and requirements; ongoing migration progress remains owned
  by the parity ledger.
- Accepted 2026-08-13: retain and compact
  `area-of-interest-and-raster-sizing.md` to dated provider evidence,
  calculations, validation cases, completed-output links, open questions, and
  explicit return triggers.
- Accepted 2026-08-13: retain and compact
  `artifact-storage-and-client-cache.md` to hosted delivery alternatives,
  browser-cache evidence, conservative reuse assumptions, completed-output
  links, and explicit return triggers.
- Accepted 2026-08-13: retain and compact
  `current-public-integrations.md` while preserving its exact legacy request
  inventory and KIEG evidence; replace generic architecture and candidate-layer
  prose with durable-owner links and explicit adapter return triggers.
- Accepted 2026-08-13: retain and compact `gcp-development-topology.md`; keep
  its GCP connection diagram explicitly candidate-only, deployment-stage
  distinctions, unresolved provider boundaries, and return trigger. Remove
  duplicated database comparison and historical adoption sequencing.
- Accepted 2026-08-13: retain and compact `gcp-cost-options.md`; keep operating
  profiles, managed-provider alternatives, workload equations, disposable
  proof, cost controls, durable-owner links, and return triggers. Remove stale
  numeric allowances, repeated architecture, and premature provider preference.
- Accepted 2026-08-13: split documentation responsibilities. Project lifecycle
  owns only temporary project records and approval/closeout states; the new
  research guide owns research traceability and cleanup; repository guide owns
  PR closeout; skills remain the sole procedural owners for planning,
  implementation, documentation, inbox triage, and specialized review. Keep
  technical-writing rules in the engineering guide and route research through
  the owner-approved AGENTS update.
- Accepted 2026-08-13: retain `MARKET-OPPORTUNITY.md` as active product
  hypothesis research, rename it to `market-opportunity.md`, and add decision
  trace, missing evidence, durable product boundary, and explicit return
  triggers without presenting the direction as accepted strategy.
- Accepted 2026-08-13: make repository skills deterministic by naming their one
  or two primary guides directly while retaining AGENTS routing for complete
  touched-area context. Do not duplicate guide content inside skills.
- Accepted 2026-08-13: merge `SIMILAR-APPS-RESEARCH.md` into active
  `market-opportunity.md`. Preserve the comparator table, method limitation,
  positioning evidence, sources, and revalidation trigger; remove duplicated
  implications and the standalone file.
- Accepted 2026-08-13: retain `additional-map-layers.md` with its candidate and
  source evidence; clarify that the order guides evaluation rather than an
  accepted roadmap, link its durable domain output, and add the selection and
  revalidation return gate.
- Accepted 2026-08-13: retain `prototype-migration-parity-ledger.md` as the
  migration/cutover evidence tracker. Add status, durable-output links,
  evidence-backed advancement rules, requirement links, and explicit return
  triggers; clarify that repository separation does not prohibit authorized
  user data in PostgreSQL or artifact storage.
- Accepted 2026-08-13: retain the detailed
  `prototype-behavior-inventory.md` as the observable legacy baseline. Add
  durable-output links and return triggers, remove procedural discovery
  instructions, and update stale pre-decision narration without deleting
  capability, layer, persistence, failure, or characterization evidence.
- Assumption: filename casing and naming cleanup is considered only when a file
  is retained and the value outweighs link churn.
- Open: none; all 15 original research files have an accepted disposition.

## Data Or Runtime Flow

This is documentation-only work. It does not change runtime data, external
integrations, generated artifacts, or private files.

## Implementation Plan

1. [done] Inventory research files, headings, status language, line counts,
   inbound links, and candidate durable owners.
2. [done] Present one recommendation at a time and record each owner
   decision.
3. [done] Add the accepted research lifecycle and traceability rule.
4. [done] Preserve unique conclusions/rationale, then compact, retain, or
   delete each accepted file and repair links.
5. [done] Verify references, Markdown paths, skill structure, diff quality,
   and the aggregate repository gate.
6. [pending] Summarize dispositions, move durable results, and remove this
   temporary plan after owner acceptance.

## Verification And Acceptance

- `rg` searches find no references to deleted files and no stale research
  TODO/status text.
- Relative Markdown links resolve.
- Changed repository skills, if any, retain valid front matter and structure.
- `git diff --check`
- `mise run verify`
- The owner has accepted every delete/retain recommendation individually.

## Result

- All 15 original research files received an explicit owner decision.
- Six standalone research files were removed; one of them was merged into the
  retained market research. Nine research files remain with decision trace and
  return conditions appropriate to their current use.
- Research content fell from 1,585 lines across 15 files to the final audited
  set reported at closeout, while preserving legacy evidence, provider details,
  market hypotheses, cloud alternatives, and cutover tracking.
- Project lifecycle, research lifecycle, PR closeout, technical-documentation
  guidance, and skill routing now have distinct owners.
- Relative Markdown links, removed-name searches, durable project-link rules,
  skill front matter, `git diff --check`, and `mise run verify` passed.
- The case-only market research rename required `git mv` on macOS and is the
  only staged change; all other task changes remain unstaged.
