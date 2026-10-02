# TASK-009: Research and recommend a published template

- Status: done
- Spec: [SPEC-005](../specs/SPEC-005-setup-template.md)

## Goal

`setup-template` can read prepared project context, research only published
Phatysd templates, and present exactly one evidence-backed recommendation as a
`Proposal`, or report an explicit unresolved research result without inventing
a direction.

Read:

- [SPEC-005](../specs/SPEC-005-setup-template.md)
- [Requirement](../requirement.md)
- [Repository context](../../CONTEXT.md)
- [Workflow](../workflow.md)
- [Grill Workflow](../../.agents/skills/grill-workflow/SKILL.md)

Relevant existing area:

- `.agents/skills/setup-template/SKILL.md` (new skill source)
- `.agents/skills/setup-phat-project/SKILL.md`
- `.agents/skills/to-prototype/SKILL.md`
- `.agents/skills/to-spec-with-phat/SKILL.md`

## Blocked by

- None

## Todo

- [x] Create the `setup-template` skill with valid frontmatter and the
  repository-first invocation boundary described by SPEC-005 (AC-01).
  Verified: `.agents/skills/setup-template/SKILL.md` has the required
  `name`/`description` frontmatter and prepared-context precondition.
- [x] Implement bounded discovery from the published Phatysd path, accepting
  only `type: template` and `status: published` records and using canonical,
  Markdown, or JSON representations without inferring semantics from CSS
  (AC-02, AC-11). Verified: discovery routes, published filtering,
  representation comparison, and no-CSS-inference rules are explicit; live
  `llms.txt` and template JSON checks passed.
- [x] Implement evidence-based matching against project applicability, scope,
  user flows, constraints, and visual profile, then expose exactly one
  candidate with identity, revision, freshness, profile, tokens, examples,
  and matching rationale as `Proposal` (AC-03, AC-04). Verified: matching
  signals and the single-candidate `Proposal` response shape are explicit.
- [x] Implement no-match, unavailable-site, incomplete-representation, and
  representation-mismatch outcomes as `Research needed` or `Open question`
  without changing existing project context (AC-09, AC-11). Verified: each
  fallback is documented with unchanged-context and no-invention boundaries.
- [x] Verify successful, filtered, unsupported, unavailable, and conflicting
  representation scenarios with static/manual checks; no repository test
  runner is known, so do not invent a test command. Verified: frontmatter and
  contract assertions passed, live public template checks passed, and both
  tracked/new-file `git diff --check` validations passed.
- [x] If repository policy or user instructions require a commit, create only
  a task-scoped commit; otherwise leave the focused diff for review. Created
  task-scoped commit `24c3dc4`
  (`task(TASK-009): add template research skill`); no push performed.
- [x] Review approved — commit `24c3dc4` against `24c3dc4^`; AC-01–AC-04,
  AC-09, and AC-11 verified; frontmatter, static contract assertions, live
  public template checks, and `git diff --check` passed; no findings.
