# TASK-013: Reconcile canonical review identifier and update references

- Status: done
- Spec: [SPEC-006](../specs/SPEC-006-neutral-skill-identifiers.md)

## Goal

The current catalog, installation guidance, workflow handoffs, and interface
references direct users to the five final identifiers — including canonical
`code-review` — while a public migration map explains the breaking rename and
preserves the Phat/Phatysd product and source terminology.

Read:

- [SPEC-006](../specs/SPEC-006-neutral-skill-identifiers.md)
- [Requirement](../requirement.md)
- [Repository context](../../CONTEXT.md)
- [Workflow](../workflow.md)
- [Agent guidance](../../AGENTS.md)

Relevant existing area:

- `README.md`
- `AGENTS.md`
- `CONTEXT.md`
- `docs/requirement.md`
- `docs/workflow.md`
- maintained `SKILL.md` and interface-reference content under `.agents/skills/`
- the intermediate `.agents/skills/review-task/` source created by TASK-012
- historical specs and tasks, which may retain retired identifiers as evidence

## Blocked by

- None

## Todo

- [x] Reconcile the intermediate `review-task` source from TASK-012 to the
  canonical `code-review` source identity, including its path, frontmatter,
  and public interface metadata, while preserving its review behavior and
  without adding an alias (AC-01, AC-02, AC-06, AC-08). Verified: only
  `.agents/skills/code-review/` exists, its frontmatter and `$code-review`
  interface prompt match the canonical identity, and no compatibility alias
  or `review-task` source directory remains.
- [x] Update current README, catalog, installation, repository-layout,
  requirement, context, workflow, and user-facing handoff references to use
  `ask-workflow`, `grill-workflow`, `setup-project`, `write-spec`, and
  `code-review`, without renaming unaffected skills (AC-03). Verified in
  `README.md`, `AGENTS.md`, `CONTEXT.md`, `docs/requirement.md`, and
  `docs/workflow.md`.
- [x] Update maintained cross-skill references in current skill instructions
  and interface guidance where they direct users to a retired identifier;
  preserve historical task/spec evidence when it documents the previous
  contract, and do not change skill behavior beyond identifier substitutions
  (AC-03, AC-06). Verified: current `.agents/skills/` references use the five
  replacement IDs; remaining retired-ID hits are migration/history mentions or
  Markdown anchors only.
- [x] Create a public `docs/migrations/skill-identifier-migration.md` map
  linked from the catalog guidance, containing exactly one replacement for
  each retired identifier and an explicit breaking-rename/no-alias notice
  (AC-04). Verified: all five mapping rows occur exactly once and README links
  the map.
- [x] Preserve `Phat`, `Phat workflow`, `Phatysd`, and `docs.phatysd.me` when
  they describe the product, workflow, or external source rather than an
  installable skill identifier (AC-07). Verified in the migration map and
  maintained project documentation.
- [x] Search maintained references for retired identifiers, classify allowed
  migration/history mentions, verify links and catalog counts remain coherent,
  and run the repository-supported whitespace check (AC-03, AC-04, AC-07).
  Verified: 13 source directories match their frontmatter names, no retired
  source directory remains, `git diff --check` passes, and allowed hits are
  limited to historical task/spec evidence or Markdown anchors.
- [x] If repository policy or user instructions require a commit, create only
  a task-scoped commit; otherwise leave the focused diff for review. Verified:
  commit `f3fb818` (`task(TASK-013): reconcile canonical review identifier`).
- [x] Review approved — `f3fb818` against `3d073b0`; AC-01, AC-02, AC-03,
  AC-04, AC-06, AC-07, and AC-08 verified; `git diff --check` passed; no
  Standards or Spec findings. AC-05 published listing/install verification
  remains external follow-up for TASK-014 and was not run in this local review.
