# TASK-015: Configure the project verification policy

- Status: done
- Spec: [SPEC-007](../specs/SPEC-007-automated-verification-agents.md)

## Goal

`setup-project` asks once for four independent verification modes
(`auto`, `required`, or `off`) and persists the confirmed unit-test,
integration-test, e2e-test, and code-review policy as inspectable project
context without inventing defaults or overwriting an existing confirmed policy.

Read:

- [SPEC-007](../specs/SPEC-007-automated-verification-agents.md)
- [Requirement](../requirement.md)
- [Repository context](../../CONTEXT.md)
- [Setup project skill](../../.agents/skills/setup-project/SKILL.md)
- [Agent guidance](../../AGENTS.md)

Relevant existing area:

- `.agents/skills/setup-project/SKILL.md`
- `.agents/skills/setup-project/references/`

## Blocked by

- None

## Todo

- [x] Implement the one-time setup flow for the four independent verification
  modes and persist their confirmed values as project context (AC-01).
  Implemented in `setup-project` with the canonical policy schema in
  `references/verification-policy.md`.
- [x] Preserve existing confirmed values on rerun, keep each mode
  independently inspectable, and avoid inventing defaults or changing
  unrelated project decisions (AC-01). The skill now reuses valid policy,
  blocks malformed policy, and requires complete explicit confirmation before
  first persistence or repair.
- [x] Verify representative `auto`/`required`/`off` combinations, idempotent reruns,
  and the persisted policy shape through supported static or manual checks;
  do not invent a repository test command (AC-01). Inline static assertions
  covered all-off, mixed, and all-on combinations plus the first-run, rerun,
  malformed-policy, and per-task-separation branches; `git diff --check`
  passed. No repository-local test runner is documented.
- [x] If repository policy or user instructions require a commit, create only
  a task-scoped commit; otherwise leave the focused diff for review. Verified:
  commit `ed80871` (`task(TASK-015): configure verification policy`).
- [x] Review approved — `ed80871` against `4256e6b`; AC-01 verified; policy
  contract assertions, `git diff --check`, and task-scoped path checks passed;
  no findings. No repository-local test/build/lint runner is documented.
