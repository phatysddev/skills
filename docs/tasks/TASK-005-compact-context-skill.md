# TASK-005: Compact context utility

- Status: done
- Spec: [SPEC-003](../specs/SPEC-003-compact-context-utility.md)

## Goal

The compact-context utility provides a short, loss-aware inline handoff format
for verbose intermediate context without replacing canonical project documents,
changing decisions, or routing the workflow.

Read before implementation:

- SPEC-003
- .agents/skills/compact-context/SKILL.md
- docs/workflow.md
- AGENTS.md

## Blocked by

- None

## Todo

- [x] Reduce compact-context/SKILL.md to a focused utility guide under 180
  lines, with purpose, trigger conditions, preserve/remove rules, normalization,
  output shape, loss check, and calling contract.
- [x] Preserve exact identifiers, paths, commands, acceptance criteria,
  references, open questions, conflicts, and decision states.
- [x] State that canonical requirements, specs, tasks, and review targets must
  remain available in full; do not use the utility as a default code-to-context
  step.
- [x] Verify frontmatter, line count, TOC anchors, and reference links.
  Verified in the current worktree.
- [x] Review approved — compact-context is 163 lines; frontmatter, preserve /
  remove rules, canonical-source guardrails, and utility calling contract pass
  static inspection.
