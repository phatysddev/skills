# TASK-019: Integrate the canonical code-review capability

- Status: done
- Spec: [SPEC-007](../specs/SPEC-007-automated-verification-agents.md)

## Goal

The automated verification workflow resolves the canonical `code-review`
capability as the single final review stage after the task enters `in_review`
and preserves the established Phat review outputs — findings,
acceptance-criteria assessment, evidence checks, and task-status decision.
Final review may update only the selected task's review evidence/status; the
task does not create a compatibility alias or own the separate public
identifier migration.

Read:

- [SPEC-007](../specs/SPEC-007-automated-verification-agents.md)
- [SPEC-006](../specs/SPEC-006-neutral-skill-identifiers.md)
- [Requirement](../requirement.md)
- [Repository context](../../CONTEXT.md)
- [Implement task skill](../../.agents/skills/implement-task/SKILL.md)
- [Code review skill](../../.agents/skills/code-review/SKILL.md)
- [TASK-013](TASK-013-update-skill-references-and-migration.md)
- [TASK-014](TASK-014-verify-neutral-skill-catalog.md)
- [Agent guidance](../../AGENTS.md)

Relevant existing area:

- `.agents/skills/code-review/`
- `.agents/skills/implement-task/`
- maintained skill and workflow references using the canonical identifier

## Blocked by

- TASK-013
- TASK-014
- TASK-017

## Todo

- [x] Reconcile the review capability handoff with the confirmed canonical
  `code-review` identifier after TASK-013 and TASK-014 are updated to that
  decision; do not restore `review-task` as the canonical mapping or add an
  alias (AC-12). Updated `implement-task` and this task's maintained links to
  `.agents/skills/code-review/SKILL.md`; no alias or retired skill path is
  used for resolution.
- [x] Dispatch the canonical review capability exactly once after the task
  enters `in_review`, preserving findings, acceptance-criteria assessment,
  evidence checks, and task-status decision (AC-05, AC-07, AC-12). Added the
  final-mode handoff, complete input/output report contract, and boundary that
  permits writes only to the selected task's review evidence/status.
- [x] Verify the canonical review output against the accepted pre-rename
  behavior in SPEC-006, confirm maintained references use `code-review`, and
  confirm no compatibility alias is advertised (AC-12). Static assertions
  covered canonical identity, ordering, report preservation, final-review
  ownership, policy visibility, and retired-path exclusion; `git diff --check`
  passed. No repository-local test runner is documented.
- [x] If repository policy or user instructions require a commit, create only
  a task-scoped commit; otherwise leave the focused diff for review. Verified:
  commit `5fde81f` (`task(TASK-019): integrate canonical code-review`).
- [x] Review approved — `5fde81f` against `5fde81f^`; AC-05, AC-07, and AC-12
  verified; independent handoff assertions, `git diff --check`, and
  task-scoped path checks passed; no findings. No repository-local
  build/test/lint runner is documented.
