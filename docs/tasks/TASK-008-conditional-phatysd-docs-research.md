# TASK-008: Add conditional Phatysd Docs research to grill-with-phat

> Historical record: the external Phatysd Docs research behavior was removed
> on 2026-10-03. Research instructions and checks below no longer apply.
> The template-selection skill was also removed on 2026-10-03; project setup
> now hands off directly to prototype or specification.

- Status: done
- Spec: [SPEC-004](../specs/SPEC-004-phatysd-docs-research.md)

## Goal

`grill-with-phat` can conditionally research published Phatysd Docs when local
evidence is insufficient, record the evidence used, preserve project-specific
authority, and handle unavailable or inconclusive research without inventing
claims.

Read before implementation:

- [SPEC-004](../specs/SPEC-004-phatysd-docs-research.md)
- [Requirement](../requirement.md)
- [Repository context](../../CONTEXT.md)
- [Agent guidance](../../AGENTS.md)
- [Workflow](../workflow.md)

Relevant existing area:

- `.agents/skills/grill-with-phat/SKILL.md` owns the grilling workflow and
  currently contains an uncommitted research-related change to reconcile with
  SPEC-004.

## Blocked by

- None

## Todo

- [x] Reconcile `.agents/skills/grill-with-phat/SKILL.md` with SPEC-004: the
  conditional research trigger, `docs.phatysd.me` discovery locations,
  canonical/Markdown/JSON source guidance, source metadata fields, authority
  rules, freshness uncertainty, read-only boundary, and unavailable/empty-
  content fallback are explicit while the existing A–D question and
  downstream-handoff contracts remain intact (AC-01–AC-08).
- [x] Preserve the existing skill frontmatter, terminology, decision-state
  rules, repository-first inspection, and no-implementation/no-auto-handoff
  boundaries; unrelated `implement-task` changes and the untracked SPEC-004
  file were not modified or staged.
- [x] Verify the behavior with observable scenarios represented by the skill
  contract: skipped research, required research, source recording, conflicting
  authority, unavailable or empty docs, and missing machine-readable
  representations. Static assertions covered AC-01–AC-08; the live public
  index currently reports no published content, so the documented fallback is
  the observable result and no fabricated claim is added.
- [x] Run repository-supported static checks: frontmatter/source/fallback
  assertions passed, `git diff --check` passed, `/llms.txt`, `/docs`, and
  `/search` returned successfully, and `/llms.txt` contained `No published
  content yet.` No repository test or build command exists.
- [x] Created the required task-scoped commit `066e4c4`
  (`task(TASK-008): add conditional Phatysd docs research`) containing only
  TASK-008 changes; no push performed.
- [x] Resolved review finding P2 at
  `.agents/skills/grill-with-phat/SKILL.md:106-110` (AC-04): public/local
  conflicts are now kept visible in the grilling summary or decision record
  for resolution while the project-specific source remains authoritative.
- [x] Resolved review finding P2 at
  `.agents/skills/grill-with-phat/SKILL.md:92-96` (AC-06): a human page is
  usable only when it directly supports the claim; otherwise the claim stays
  **Research needed** or **Open question** when Markdown/JSON is unavailable.
- [x] Created follow-up task-scoped commit `1cdb275`
  (`task(TASK-008): resolve research review findings`) containing only the
  review corrections; the existing `066e4c4` implementation commit was
  preserved and no push was performed.
- [x] Review approved — commits `066e4c4` and `1cdb275` against their parents;
  AC-01–AC-08 verified; frontmatter, contract assertions, live endpoint checks,
  and `git diff --check` passed; no findings.
