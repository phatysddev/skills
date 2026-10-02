# TASK-017: Select verification capabilities for each implementation task

- Status: done
- Spec: [SPEC-007](../specs/SPEC-007-automated-verification-agents.md)

## Goal

`implement-task` reads the persisted project verification policy, applies an
explicit override only to the current task, selects relevant installed test
capabilities from task scope and acceptance criteria, and reports skips or
unresolved role mappings without silently changing project policy.

Read:

- [SPEC-007](../specs/SPEC-007-automated-verification-agents.md)
- [Requirement](../requirement.md)
- [Repository context](../../CONTEXT.md)
- [Implement task skill](../../.agents/skills/implement-task/SKILL.md)
- [TASK-015](TASK-015-configure-verification-policy.md)
- [TASK-016](TASK-016-add-test-capability-skills.md)
- [Agent guidance](../../AGENTS.md)

Relevant existing area:

- `.agents/skills/implement-task/SKILL.md`
- `.agents/skills/implement-task/references/`
- project verification policy written by TASK-015
- capability role contracts written by TASK-016

## Blocked by

- TASK-015
- TASK-016

## Todo

- [x] Read the project policy by default and apply an explicit per-task
  override only to the current task without mutating persisted context
  (AC-02, AC-10). Implemented with a validated `## Verification Policy`
  input, in-memory override shape, rationale requirement, and setup routing
  for missing or malformed policy.
- [x] Determine relevance from task scope and observable acceptance criteria,
  select only relevant non-off test capabilities, and record an observable
  reason for every skipped capability (AC-03). Added
  independent role rules for unit, integration, and e2e selection plus the
  deterministic `unit-test` → `integration-test` → `e2e-test` order.
- [x] Resolve at most one detected installed skill/runner for each selected
  capability role, and block with an explicit reason for missing or ambiguous
  resolution without auto-installing a replacement (AC-04). Added exact role
  identity, single-skill/single-runner resolution, and missing/ambiguous block
  rules without substitution or installation.
- [x] Verify default-policy, override, relevance, skip-reason, missing-role,
  and ambiguous-role scenarios while preserving unrelated project policy and
  working-tree changes (AC-02, AC-03, AC-04, AC-10). Static contract
  assertions covered the policy, override, selection, resolution, report, and
  mutation boundaries; no-trailing-whitespace and `git diff --check` passed.
  No repository-local test runner is documented.
- [x] If repository policy or user instructions require a commit, create only
  a task-scoped commit; otherwise leave the focused diff for review. Verified:
  commit `4561006` (`task(TASK-017): select verification capabilities`).
- [x] Review approved — `4561006` against `4561006^`; AC-02, AC-03, AC-04,
  and AC-10 verified; independent contract assertions, `git diff --check`,
  and task-scoped path checks passed; no findings. No repository-local
  build/test/lint runner is documented.
