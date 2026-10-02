# TASK-011: Integrate setup-template into the workflow and catalog

- Status: done
- Spec: [SPEC-005](../specs/SPEC-005-setup-template.md)

## Goal

The completed `setup-template` skill is an installable, documented Phat
workflow capability with explicit entry routes from project setup and workflow
routing when a reusable visual direction is needed. Its final response
preserves the existing visual handoffs and read-only safety boundaries.

Read:

- [SPEC-005](../specs/SPEC-005-setup-template.md)
- [Requirement](../requirement.md)
- [Repository context](../../CONTEXT.md)
- [Workflow](../workflow.md)
- [TASK-010](TASK-010-persist-confirmed-design-direction.md)
- [Agent guidance](../../AGENTS.md)

Relevant existing area:

- `.agents/skills/setup-template/SKILL.md`
- `.agents/skills/setup-project/SKILL.md`
- `.agents/skills/ask-workflow/SKILL.md`
- `README.md`
- `AGENTS.md`
- `CONTEXT.md`
- `docs/requirement.md`
- `docs/workflow.md`

## Blocked by

- TASK-010

## Todo

- [x] Complete the final handoff behavior: recommend exactly `$to-prototype`
  when visual validation is requested or `$write-spec` otherwise, and
  never invoke the downstream skill automatically (AC-12). Verified: the
  confirmed-only handoff section covers both branches, unresolved states, and
  the no-auto-invocation rule.
- [x] Keep the skill explicitly read-only toward `docs.phatysd.me` and bounded
  to public content; require no credentials, transmit no private project data,
  and generate no production code or prototype (AC-13). Verified: the skill's
  research-boundary and static safety assertions pass.
- [x] Add `setup-template` to the repository's installable skill layout and
  update the public catalog, workflow navigation, and current-skill metadata
  consistently after implementation, without changing existing skill names or
  unrelated user files. Verified at implementation time: the then-current
  13-skill catalog, README layout, AGENTS.md, CONTEXT.md, requirement, and
  workflow metadata were consistent.
- [x] Verify frontmatter, source layout, catalog consistency, handoff branches,
  no-auto-invocation behavior, and the read-only safety boundary at the
  original implementation. Verified at that time: all 13 skill
  frontmatter/name checks, targeted handoff/safety assertions, and whitespace
  checks passed; no repository test/build/lint runner exists.
- [x] If repository policy or user instructions require a commit, create only
  a task-scoped commit; otherwise leave the focused diff for review. Created
  task-scoped commit `bc6533f`
  (`task(TASK-011): integrate setup-template workflow`); no push performed.
- [x] Route the optional reusable-direction decision from both
  `setup-project` and `ask-workflow` to `$setup-template` before prototype or
  spec work; preserve the direct route when no template direction is needed
  (AC-14). Verified: both routing instructions require explicit reusable
  direction intent, and visual validation alone still routes to
  `$to-prototype`.
- [x] Add and run the repository consistency checker against the current
  catalog. Verified: `python3 scripts/check_skill_pack.py` passed with 16
  skill directories, required files, frontmatter names, counts, active
  references, workflow routes, and local Markdown links.
- [x] Review approved — current working tree against `HEAD`; AC-12, AC-13, and
  AC-14 verified; `python3 scripts/check_skill_pack.py` and `git diff --check`
  passed; no findings. The earlier P2 reference to a stale 12-skill catalog at
  `docs/workflow.md:128` was no longer present in the current source; the
  current catalog consistently declares 16 skills.
