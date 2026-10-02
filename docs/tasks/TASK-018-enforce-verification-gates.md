# TASK-018: Enforce sequential verification gates and ownership

- Status: done
- Spec: [SPEC-007](../specs/SPEC-007-automated-verification-agents.md)

## Goal

`implement-task` runs the selected test capabilities sequentially before the
task enters `in_review`, enforces sub-agent write boundaries and blocking
failures, and leaves the main agent responsible for integrating test reports,
fixing issues, rerunning checks, and creating the final task-scoped commit.

Read:

- [SPEC-007](../specs/SPEC-007-automated-verification-agents.md)
- [Requirement](../requirement.md)
- [Repository context](../../CONTEXT.md)
- [Implement task skill](../../.agents/skills/implement-task/SKILL.md)
- [TASK-017](TASK-017-select-verification-capabilities.md)
- [Agent guidance](../../AGENTS.md)

Relevant existing area:

- `.agents/skills/implement-task/SKILL.md`
- `.agents/skills/implement-task/references/`
- task status and checklist conventions under `docs/tasks/`

## Blocked by

- None

## Todo

- [x] Execute relevant non-off test capabilities in the fixed order
  `unit-test`, `integration-test`, then `e2e-test`, and leave the final review
  stage until after the task enters `in_review` (AC-05). Added the execution
  plan, one-at-a-time terminal-report requirement, and test-before-finalization
  ordering; this docs-only task has no relevant repository test boundary, so
  unit, integration, and e2e are each skipped with task-scope reasons.
- [x] Restrict test sub-agents to task-owned test files and reject/report
  production-file writes; keep the final review sub-agent limited to the
  selected task's review evidence/status (AC-06, AC-07). Added observable
  changed-file ownership checks and blocking write-violation rules for test and
  final-review capabilities.
- [x] Treat failed, unresolved, missing, ambiguous, timed-out, crashed, or
  inconclusive required gates as blocking, preventing commit and `in_review`
  unless an explicit per-task override applies (AC-08). Added terminal result
  classification, required-gate blocking, and no-downgrade rules.
- [x] Make the main agent integrate reports, apply in-scope fixes, rerun
  affected gates and required final checks, and record the final report before
  commit (AC-09). Added report preservation, failure classification, affected
  rerun, final-check, and main-agent ownership requirements.
- [x] Verify that a successful task-scoped commit contains only owned changes,
  preserves unrelated working-tree changes, and is followed by the existing
  `in_review` preparation behavior (AC-11). Added explicit-path staging,
  task-scoped commit, and status-gate requirements; static contract
  assertions and `git diff --check` passed. No repository-local test runner is
  documented.
- [x] If repository policy or user instructions require a commit, create only
  a task-scoped commit; otherwise leave the focused diff for review. Verified:
  commit `2216827` (`task(TASK-018): enforce verification gates`).
- [x] Review approved — `2216827` against `2216827^`; AC-05, AC-06, AC-07,
  AC-08, AC-09, and AC-11 verified; independent gate assertions,
  `git diff --check`, and task-scoped path checks passed; no findings. No
  repository-local build/test/lint runner is documented.
