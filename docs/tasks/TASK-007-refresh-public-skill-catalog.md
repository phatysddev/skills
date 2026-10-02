# TASK-007: Refresh the public skill catalog

- Status: done
- Spec: [SPEC-003](../specs/SPEC-003-compact-context-utility.md)

## Goal

Repository documentation and workflow records describe the complete 12-skill
pack, close SPEC-002, point to SPEC-003, and apply repository/user Git policy
without requiring automatic commits.

Read before implementation:

- SPEC-003
- README.md
- AGENTS.md
- CONTEXT.md
- docs/requirement.md
- docs/workflow.md
- docs/specs/SPEC-002-code-to-context.md
- .agents/skills/implement-task/SKILL.md

## Blocked by

- TASK-005 (completed)
- TASK-006 (completed)

## Todo

- [x] Update README.md, AGENTS.md, CONTEXT.md, docs/requirement.md, and
  docs/workflow.md from the old 10-skill catalog to the 12-skill category model.
- [x] Preserve TASK-001 and TASK-002 as historical publication evidence while
  closing SPEC-002 and recording TASK-003/TASK-004 as done.
- [x] Update implement-task and its reference policy so commits follow repository
  policy or explicit user instructions, with a focused working-tree diff as the
  default handoff.
- [x] Create SPEC-003 and TASK-005 through TASK-007 with links, status, scope,
  acceptance criteria, and verification evidence.
- [x] Verify catalog/status links, file inventory, frontmatter, line counts,
  whitespace, and anchor integrity.
  Verified in the current worktree.
- [x] Review approved — catalog, requirement, workflow, current status, and
  conditional Git policy are synchronized; no repository-local test runner is
  available.
