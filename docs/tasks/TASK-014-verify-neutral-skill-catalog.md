# TASK-014: Verify the renamed public skill catalog

- Status: done
- Spec: [SPEC-006](../specs/SPEC-006-neutral-skill-identifiers.md)

## Goal

The final local and published skill catalogs expose exactly 13 discoverable
skills, make the five new identifiers usable, preserve the eight unaffected
identifiers, and do not advertise retired identifiers or aliases.

Read:

- [SPEC-006](../specs/SPEC-006-neutral-skill-identifiers.md)
- [Requirement](../requirement.md)
- [Repository context](../../CONTEXT.md)
- [Agent guidance](../../AGENTS.md)
- [TASK-012](TASK-012-rename-skill-source-identifiers.md)
- [TASK-013](TASK-013-update-skill-references-and-migration.md)

Relevant existing area:

- `.agents/skills/`
- `README.md`
- `.agents/skills/<skill-name>/agents/openai.yaml`
- the public GitLab source at `https://gitlab.com/phatysd.dev/skills`

## Blocked by

- TASK-012
- TASK-013

## Todo

- [x] Enumerate the local source catalog and verify exactly 13 skill
  directories: the five agreed new identifiers plus the eight unchanged
  identifiers, with no retired directory, duplicate identifier, or alias
  (AC-01, AC-08). Verified with a local catalog script: exactly 13 expected
  directories, no retired directories, and no duplicate names.
- [x] Parse or otherwise statically inspect every renamed `SKILL.md` and
  interface metadata file to verify valid frontmatter, matching source paths,
  and consistent public names (AC-02). Verified: every local `SKILL.md` has
  matching `name`/directory and description frontmatter; all five renamed
  skills have `agents/openai.yaml` with the matching `$<skill-name>` prompt.
- [x] Verify the renamed skill bodies and maintained references contain only
  the intentional identifier substitutions, while required Phat/Phatysd source
  terminology and the migration map remain present (AC-06, AC-07). Verified:
  maintained references use the replacement identifiers, the migration map has
  all five mappings, and required Phat/Phatysd/docs.phatysd.me terminology is
  present.
- [x] Run `git diff --check` and the repository-supported static checks; do not
  invent a test, build, or lint command because no repository-local runner is
  documented. Verified: `git diff --check` passed; AGENTS.md documents no
  repository-local test, build, or lint runner.
- [x] After the updated source is available through the public GitLab
  repository, run the documented `skills` CLI discovery and selected-install
  checks for the new identifiers, and verify the old identifiers are not
  advertised as installable aliases (AC-05). Verified with
  `NPM_CONFIG_YES=true npx skills@latest add https://gitlab.com/phatysd.dev/skills
  --list`: public discovery found 13 skills and listed all five new IDs; a
  selected install of the five new IDs completed successfully in a temporary
  workspace with no retired installed names.
- [x] Verify the public listing reports exactly 13 discoverable skills and that
  the complete collection remains installable through the documented CLI
  workflow; if the public source is not yet updated, record that external
  verification is pending rather than claiming success (AC-05, AC-08).
  Verified: selected install installed 5 requested IDs and full install with
  `--skill '*'` installed exactly 13 expected IDs in a temporary workspace;
  no retired identifier directory was present.
- [x] If repository policy or user instructions require a commit, create only
  a task-scoped commit; otherwise leave the focused diff for review. Verified:
  commit `4256e6b` (`task(TASK-014): verify neutral skill catalog`).
- [x] Review approved: commit `4256e6b` against `41fed45` satisfies SPEC-006
  AC-01 through AC-08; public discovery, selected install, full install,
  local catalog checks, and `git diff --check` passed with no findings.
