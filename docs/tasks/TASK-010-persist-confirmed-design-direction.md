# TASK-010: Persist a confirmed design direction

- Status: done
- Spec: [SPEC-005](../specs/SPEC-005-setup-template.md)

## Goal

After the user confirms the `setup-template` proposal, the skill persists one
traceable `## Design Direction` record in `CONTEXT.md`, while preserving
existing decisions, exposing conflicts, and remaining idempotent.

Read:

- [SPEC-005](../specs/SPEC-005-setup-template.md)
- [Requirement](../requirement.md)
- [Repository context](../../CONTEXT.md)
- [Workflow](../workflow.md)
- [TASK-009](TASK-009-setup-template-research.md)

Relevant existing area:

- `.agents/skills/setup-template/SKILL.md`
- `.agents/skills/code-to-context/SKILL.md` for context-preservation boundaries
- `.agents/skills/setup-phat-project/SKILL.md` for source-of-truth ownership

## Blocked by

- TASK-009

## Todo

- [x] Add the explicit confirmation boundary so a proposal, rejection, or
  missing confirmation cannot be persisted as `Agreed` (AC-05, AC-10).
  Verified: the skill requires explicit confirmation and keeps rejected,
  ambiguous, or missing responses on the no-write path.
- [x] Persist one `## Design Direction` section with agreed status, template
  identity and revision, published profile, tokens, examples, source metadata,
  access date, and matching rationale while preserving unrelated context
  (AC-06). Verified: the stable Markdown record shape and preservation boundary
  are explicit in `Confirm and persist`.
- [x] Handle an existing conflicting direction by showing the conflict and
  requiring explicit replacement confirmation; preserve the old direction
  until then (AC-07). Verified: different template/revision conflicts require
  replacement confirmation before the owned section is updated.
- [x] Make same-template, same-revision reruns idempotent without duplicate
  sections or unrelated changes (AC-08). Verified: the rerun rule compares the
  owned record and leaves matching context unchanged.
- [x] Verify proposal-only, confirmed, rejected, conflicting, replacement,
  repeated-run, and malformed-context scenarios against the observable
  persisted record and diff. Verified: frontmatter, persistence-contract,
  no-write, conflict, idempotency, malformed-context-guard, live source, and
  whitespace assertions passed; no repository test runner is available.
- [x] If repository policy or user instructions require a commit, create only
  a task-scoped commit; otherwise leave the focused diff for review. Created
  task-scoped commit `538b000`
  (`task(TASK-010): persist confirmed design direction`); no push performed.
- [x] Review approved — commit `538b000` against `538b000^`; AC-05–AC-08 and
  AC-10 verified; frontmatter, persistence-contract, no-write, conflict,
  idempotency, malformed-context, live-source, and whitespace checks passed;
  no findings. No repository test runner is available.
