# TASK-006: Integrate compact and brownfield handoffs

- Status: done
- Spec: [SPEC-003](../specs/SPEC-003-compact-context-utility.md)

## Goal

The Phat workflow composes compact-context only as a conditional temporary
utility, routes brownfield repositories through code-to-context before setup,
and reuses fresh generated Codebase Context without broad rediscovery.

Read before implementation:

- SPEC-003
- docs/workflow.md
- .agents/skills/ask-phat/SKILL.md
- .agents/skills/setup-phat-project/SKILL.md
- .agents/skills/grill-with-phat/SKILL.md
- .agents/skills/code-to-context/SKILL.md
- .agents/skills/to-tasks/SKILL.md
- .agents/skills/implement-task/SKILL.md
- .agents/skills/review-with-phat/SKILL.md

## Blocked by

- TASK-005 (completed)

## Todo

- [x] Make ask-phat route meaningful code/config with missing or stale
  Codebase Context to code-to-context before setup-phat-project.
- [x] Make setup-phat-project stop and recommend code-to-context for missing or
  stale generated context, and reuse fresh context as its primary fact index.
- [x] Add the conditional grill-with-phat compact handoff and keep
  compact-context out of primary routing.
- [x] State that canonical specs and tasks are read in full by to-tasks,
  implement-task, and review-with-phat.
- [x] State that code-to-context does not call compact-context by default.
- [x] Verify routing and composition rules by static inspection and link checks.
  Verified in the current worktree.
- [x] Review approved — ask/setup precedence, conditional grill handoff,
  canonical full-read rule, and no-default code-to-context compaction pass
  static inspection.
