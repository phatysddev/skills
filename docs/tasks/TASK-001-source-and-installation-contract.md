# TASK-001: Skill source and installation contract are complete

- Status: done
- Spec: [SPEC-001](../specs/SPEC-001-publish-phat-skill-pack.md)
- Depends on: None

## Goal

The ten-skill repository — seven core workflow skills and three optional
prototype skills — has verified source metadata and clear installation
documentation for the public GitLab source.

## In scope

- Verify every current `.agents/skills/<skill-name>/SKILL.md` has valid `name`
  and `description` frontmatter, with no duplicate skill names.
- Keep the ten existing skill names, directory layout, and instructions
  unchanged.
- Keep `README.md`, `AGENTS.md`, and the project documents aligned on the
  canonical GitLab source and discovery, single-skill, and all-skills commands.
- Verify that rerunning the setup/spec workflow does not create duplicate
  project documents or modify skill instructions.

## Out of scope

- Running the published-source discovery or installation commands.
- Adding a package manifest, runtime application, or new validation framework.
- Changing the behavior or instructions of any individual skill.
- Choosing a default project/global installation policy.

## Acceptance criteria covered

- AC-04
- AC-05
- AC-06

## Context for a new session

Read:

- [SPEC-001](../specs/SPEC-001-publish-phat-skill-pack.md)
- [Requirement](../requirement.md)
- [Repository context](../../CONTEXT.md)
- [Workflow](../workflow.md)
- [Agent guidance](../../AGENTS.md)

The canonical public source is `https://gitlab.com/phatysd.dev/skills`.
The repository contains ten skills under `.agents/skills/` and has no package
manifest, test runner, or lint configuration.

## Implementation notes and constraints

- Preserve the existing Markdown document style and source-of-truth links.
- If a required frontmatter delimiter is malformed, normalize only that
  delimiter; preserve each skill's name, description, and instruction body.
- Do not add implementation-specific tooling merely to satisfy the static
  metadata check.
- Treat `.agents/skills/*/SKILL.md` as the authoritative skill source and do
  not rewrite it during documentation or setup work.

## Verification and definition of done

- Inspect all ten `SKILL.md` files and confirm each has non-empty `name` and
  `description` frontmatter; confirm the names are unique.
- Review `README.md` against the discovery, single-skill, and all-skills flows
  in SPEC-001 and confirm it names the concrete GitLab source.
- Re-run the relevant setup/spec inspection and confirm no duplicate project
  documents are created and any `.agents/skills` diff is limited to required
  frontmatter delimiter normalization with instruction bodies unchanged.
- Run `git diff --check`.

## Evidence

### Changes

- `.agents/skills/{grill-with-phat,implement-task,review-with-phat,setup-phat-project,to-spec-with-phat,to-tasks}/SKILL.md` — normalized the malformed closing frontmatter delimiter to `---`.
- The ten skill names, descriptions, and instruction bodies remain unchanged.
- Existing aligned documentation changes in `AGENTS.md`, `README.md`,
  `CONTEXT.md`, `docs/requirement.md`, `docs/workflow.md`, and SPEC-001 were
  preserved; no additional documentation scope was added during this task.

### Acceptance criteria

- AC-04 — all ten `SKILL.md` files have valid frontmatter with non-empty
  `name` and `description` fields, and the names are unique.
- AC-05 — `README.md` contains the concrete GitLab source plus discovery,
  single-skill Codex, and all-skills Codex installation flows.
- AC-06 — the project document inventory has one SPEC-001 and one each of
  TASK-001 and TASK-002; skill instruction bodies match `HEAD` and no duplicate
  project documents were created.

### Checks

- Focused shell verification of frontmatter, names, README commands, document
  IDs, and instruction-body preservation — passed.
- `git diff --check` — passed.

### Not verified

- Published-source discovery and Codex installation are intentionally reserved
  for TASK-002.
- No repository test, lint, typecheck, or build command exists in this
  repository.

## Review

- Result: approved
- Reviewed target: working tree, including unstaged and untracked changes
- Base: `HEAD`
- Review scope: TASK-001-owned frontmatter repairs; pre-existing documentation
  changes were preserved and not attributed as new implementation work.

### Acceptance criteria

- AC-04 — verified independently: all ten skill files have valid frontmatter,
  required metadata, unique names, and instruction bodies matching `HEAD`.
- AC-05 — verified independently: README contains the concrete GitLab source,
  discovery, single-skill Codex, and all-skills Codex commands.
- AC-06 — verified independently: no duplicate SPEC-001/TASK-001/TASK-002
  documents exist, and no instruction-body changes were introduced.

### Checks

- Independent frontmatter, uniqueness, README-flow, document-inventory, and
  instruction-body checks — passed.
- `git diff --check` — passed.

### Findings

- None.

### Not verified

- Published-source discovery and Codex installation remain reserved for
  TASK-002.
- No repository test, lint, typecheck, or build command exists.
