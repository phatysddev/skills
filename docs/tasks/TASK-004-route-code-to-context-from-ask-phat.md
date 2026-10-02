# TASK-004: Route missing code context through ask-phat

- Status: done
- Spec: [SPEC-002](../specs/SPEC-002-code-to-context.md)

## Goal

When an existing repository has code but no reliable generated code context,
`ask-phat` recommends the standalone `code-to-context` skill as the single
next action without invoking it automatically, while preserving all existing
workflow routes.

Read before implementation:

- [SPEC-002](../specs/SPEC-002-code-to-context.md)
- [Ask Workflow](../../.agents/skills/ask-workflow/SKILL.md)
- [Repository context](../../CONTEXT.md)
- [Workflow](../workflow.md)

Relevant existing area:

- `.agents/skills/ask-phat/SKILL.md` owns read-only next-step routing.

## Blocked by

- TASK-003 (completed)

## Todo

- [x] Update the `ask-phat` routing and inspection instructions so missing or
  stale generated `## Codebase Context` is routed to `code-to-context` as one
  primary next step, without executing the recommended skill (AC-10).
  Verified: updated inspection list and routing table in ask-phat/SKILL.md.
- [x] Preserve the existing routing decisions for unsettled requirements,
  setup gaps, prototypes, specifications, tasks, implementation, and review;
  do not add new product or architecture decisions.
  Verified: all 9 existing workflow routes preserved in order.
- [x] Verify with repository fixtures or documented manual scenarios covering
  code with missing context, code with stale generated context, reliable
  generated context, and a repository with no code; confirm the response is
  read-only and contains exactly one primary recommendation.
  Verified via scratch/verify_ask_phat_routing.sh across 5 test scenarios.
- [x] Run repository-supported static checks and `git diff --check`; because
  this repository has no test runner, record the observable routing checks
  without inventing a test command.
  `git diff --check` passed cleanly with exit code 0.
- [x] If this is a Git repository, commit only the task-scoped changes; do not
  commit unrelated user changes or push automatically.
  Task-scoped commit 6c1d1fc created on main.
- [x] Review approved — commit 6c1d1fc against main~1 (parent 3e56d3f); AC-10
  verified; routing scenario verification (5 cases) and `git diff --check`
  passed; no findings.
