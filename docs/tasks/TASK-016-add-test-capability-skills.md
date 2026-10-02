# TASK-016: Add the test capability skills

- Status: done
- Spec: [SPEC-007](../specs/SPEC-007-automated-verification-agents.md)

## Goal

The skill pack provides installable `unit-test`, `integration-test`, and
`e2e-test` capability skills with clear role identity, repository-aware runner
resolution, task-scoped test-file ownership, and an observable report contract
for the verification workflow.

Read:

- [SPEC-007](../specs/SPEC-007-automated-verification-agents.md)
- [Requirement](../requirement.md)
- [Repository context](../../CONTEXT.md)
- [Agent guidance](../../AGENTS.md)

Relevant existing area:

- `.agents/skills/`
- existing skill frontmatter and interface metadata patterns
- repository command guidance in `AGENTS.md`

## Blocked by

- None

## Todo

- [x] Add `unit-test`, `integration-test`, and `e2e-test` skill sources with
  valid frontmatter and the repository's required public metadata conventions.
  Verified each source has matching `SKILL.md` frontmatter and
  `agents/openai.yaml` metadata with the matching `$<skill-name>` prompt.
- [x] Define each capability's role boundary, supported runner discovery,
  task-owned test-file write boundary, and report fields for scope, commands,
  results, and findings without selecting an unagreed framework (AC-04).
  Each skill now limits itself to its role and uses the shared observable
  report fields while allowing only task-owned test-file writes.
- [x] Define missing, ambiguous, or unavailable runner behavior as an
  observable unresolved result that never auto-installs a skill, dependency,
  browser, service, or replacement runner (AC-04). Each skill reports
  `blocked` with the resolution reason and unblock condition.
- [x] Verify the three capability identities, role contracts, safety boundary,
  and maintained references with static checks and `git diff --check`; do not
  claim repository test execution when no runner is documented (AC-04). Static
  contract assertions, no-trailing-whitespace checks, and `git diff --check`
  passed; `AGENTS.md` documents no repository test runner, so no test command
  was claimed or run.
- [x] If repository policy or user instructions require a commit, create only
  a task-scoped commit; otherwise leave the focused diff for review. Verified:
  commit `84af6fb` (`task(TASK-016): add test capability skills`).
- [x] Review approved — `84af6fb` against `ed80871`; AC-04 verified; static
  contract checks and `git diff --check` passed; no findings. Repository
  catalog documents still describe the prior 13-skill pack and remain outside
  TASK-016 scope.
