# TASK-003: Generate safe code-derived repository context

- Status: done
- Spec: [SPEC-002](../specs/SPEC-002-code-to-context.md)

## Goal

An existing repository can invoke the standalone `code-to-context` skill to
inspect repository evidence safely and create or update the generated
`## Codebase Context` block in `CONTEXT.md` without exposing secrets,
overwriting human-authored context, or changing any other project files.

Read before implementation:

- [SPEC-002](../specs/SPEC-002-code-to-context.md)
- [Requirement](../requirement.md)
- [Repository context](../../CONTEXT.md)
- [Agent guidance](../../AGENTS.md)
- [Workflow](../workflow.md)

Relevant existing areas:

- `.agents/skills/` for the installable skill layout;
- `CONTEXT.md` for the existing human-authored context;
- the repository's current documentation and source-discovery conventions.

## Blocked by

- None

## Todo

- [x] Implement `.agents/skills/code-to-context/SKILL.md` with valid `name` and
  `description` frontmatter and the standalone workflow described by SPEC-002.
  Verified valid frontmatter and unique name across all 11 skills.
- [x] Implement repository discovery and the fixed generated Markdown schema,
  including source revision metadata, `Observed`/`Inferred`/`Unknown` labels,
  attributable evidence, completion summary, and explicit unknowns for
  unreadable or unavailable safe inputs (AC-01, AC-04, AC-09).
- [x] Implement missing-file creation and marked-block replacement while
  preserving human-authored context, authoritative sources, malformed or
  ambiguous content, and conflict records; repeated runs must not duplicate
  the generated block (AC-02, AC-03, AC-05, AC-08).
- [x] Implement exclusion and safety rules for generated output, dependencies,
  vendor files, build output, binaries, oversized/unreadable inputs, secrets,
  and sensitive command output; retain only safe structural information and
  use `[REDACTED]` where required (AC-06, AC-07).
- [x] Verify the skill with representative fixture repositories covering
  existing and missing `CONTEXT.md`, manual sections, prior generated blocks,
  malformed markers, conflicting authoritative content, dirty worktrees,
  excluded paths, fake secrets, and safe discovery command failures; confirm
  no secret appears in `CONTEXT.md` or the completion summary.
  Verified via scratch/verify_fixtures.sh (6 test scenarios passed).
- [x] Run repository-supported static checks and `git diff --check`; because
  this repository has no test runner, record observable fixture verification
  rather than inventing a test command.
  `git diff --check` passed cleanly with exit code 0.
- [x] If this is a Git repository, commit only the task-scoped changes; do not
  commit unrelated user changes or push automatically.
  Task-scoped commit 3e56d3f created on main.
- [x] Review approved — commit 3e56d3f against main (parent f66beea); AC-01–AC-09
  verified; frontmatter validation, fixture tests (6 scenarios), and
  `git diff --check` passed; no findings.
