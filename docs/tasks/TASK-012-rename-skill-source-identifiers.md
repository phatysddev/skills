# TASK-012: Rename skill source identifiers

- Status: done
- Spec: [SPEC-006](../specs/SPEC-006-neutral-skill-identifiers.md)

## Goal

The five agreed workflow skills are exposed under their new responsibility-based
identifiers with valid source paths, frontmatter, and interface metadata, while
their instructions and behavior remain unchanged.

Read:

- [SPEC-006](../specs/SPEC-006-neutral-skill-identifiers.md)
- [Requirement](../requirement.md)
- [Repository context](../../CONTEXT.md)
- [Agent guidance](../../AGENTS.md)

Relevant existing area:

- `.agents/skills/ask-phat/`
- `.agents/skills/grill-with-phat/`
- `.agents/skills/setup-phat-project/`
- `.agents/skills/to-spec-with-phat/`
- `.agents/skills/review-with-phat/`
- each renamed skill's `agents/openai.yaml`

## Blocked by

- None

## Todo

- [x] Rename exactly these five source directories and no others: `ask-phat` →
  `ask-workflow`, `grill-with-phat` → `grill-workflow`, `setup-phat-project` →
  `setup-project`, `to-spec-with-phat` → `write-spec`, and `review-with-phat` →
  `review-task` (AC-01). Verified: the five old directories were renamed and
  no other source directory was renamed.
- [x] Update each renamed `SKILL.md` frontmatter `name` and its own public
  interface metadata to the new identifier, keeping required frontmatter valid
  and avoiding duplicate directories or compatibility aliases (AC-02, AC-08).
  Verified: all five frontmatter names, descriptions, and self-referencing
  interface prompts are valid and aligned with their new paths.
- [x] Preserve each renamed skill's description, instruction body, research
  rules, decision contract, workflow behavior, and handoff semantics; limit
  changes in this task to the identity substitutions required by the rename
  (AC-06). Verified: nested reference files and non-identity content match the
  pre-rename source; the pre-existing A–D question-set changes in the grill
  skill were preserved and not expanded by this task.
- [x] Verify that all five new source paths exist, all five frontmatter names
  match their directories, the eight unaffected skill identifiers remain
  unchanged, and no retired source directory remains (AC-01, AC-02, AC-08).
  Verified: the catalog has 13 source directories, all five retired paths are
  absent, and all eight unaffected paths remain present.
- [x] If repository policy or user instructions require a commit, create only
  a task-scoped commit; otherwise leave the focused diff for review. Created
  task-scoped commit `3d073b0`
  (`task(TASK-012): rename skill source identifiers`); no push performed.
- [x] Review approved — commit `3d073b0` against `3d073b0^`; AC-01, AC-02,
  AC-06, and AC-08 verified; catalog, frontmatter, interface metadata, and
  `git diff --check` passed; no findings. Public catalog and maintained
  cross-reference checks remain in TASK-013/TASK-014 scope, and no repository
  test/build/lint runner is documented.
