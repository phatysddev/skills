# SPEC-001: Publish the Phat skill pack

- Status: done
- Requirement: [docs/requirement.md](../requirement.md)
- Context: [CONTEXT.md](../../CONTEXT.md)
- ADRs: None

## Problem and outcome

The Phat skills currently exist in a local repository but do not yet have a
complete, verifiable publication contract. A maintainer must be able to publish
the existing collection to the decided GitLab repository, and an installer
must be able to discover and install one or all skills with the `skills` CLI.

## In scope

- Make the ten existing skills — seven core workflow skills and three optional
  prototype skills — discoverable from the repository's
  `.agents/skills/<skill-name>/SKILL.md` locations.
- Preserve each skill's `name`, `description`, and existing instructions.
- Support discovery before installation with the `skills` CLI.
- Support installing one named skill and the complete collection for Codex.
- Document the repository layout and installation commands for users.

## Out of scope

- Adding or changing the behavior of any skill.
- Creating a package manifest or a separate runtime application.
- Adding new skills.
- Selecting installation policy without an explicit decision.
- Defining installation behavior for agents other than the supported CLI
  targets needed by this requirement.

## User flow and behavior

### Maintainer flow

1. The maintainer publishes the repository containing the existing skill
   directories to the decided GitLab source.
2. The maintainer can run the CLI discovery command and see all ten current
   skills by name, including the optional prototype skills.
3. The maintainer can document the resulting canonical installation command.

### Installer flow

1. An installer runs `npx skills@latest add https://gitlab.com/phatysd.dev/skills --list`.
2. The CLI discovers the skills whose `SKILL.md` files are in the supported
   repository locations and whose frontmatter is valid.
3. The installer selects one skill, or selects all skills, and targets Codex.
4. The selected skill files become available to Codex without changing their
   instructions.

### Alternate flows

- If the repository cannot be accessed, installation is not considered
  successful and the CLI's access error is surfaced to the installer.
- If a skill lacks required frontmatter, that skill is not considered a valid
  installable skill and the problem must be visible during discovery or
  validation.
- If the installer requests a skill name that does not exist, the CLI must not
  claim that the requested skill was installed.

## Business rules and constraints

- The existing ten skill names remain stable unless a later requirement
  explicitly changes them.
- Each installable skill must have a `SKILL.md` with valid `name` and
  `description` frontmatter.
- The repository layout remains the source of truth for skill content.
- Documentation must use the decided GitLab source URL.
- Setup and documentation changes must not silently alter skill instructions.

## Data and permissions

- The distributable data is the skill source: each `SKILL.md` and any future
  sibling files intentionally required by that skill.
- Installers need read access to the chosen public GitLab repository.
- The installed skills do not own application user data and do not introduce
  runtime authorization rules.

## Errors and edge cases

- The source repository is unavailable, private without configured access, or
  points to the wrong owner/repository.
- A `SKILL.md` has missing or invalid required frontmatter.
- Two skills expose the same installable name.
- The requested skill is not in the published source.
- The installer chooses project or global scope, or an agent target, that is
  not available in the current environment.

## Interfaces and observable test points

- Discovery command:

  ```bash
  npx skills@latest add https://gitlab.com/phatysd.dev/skills --list
  ```

- Single-skill Codex installation:

  ```bash
  npx skills@latest add https://gitlab.com/phatysd.dev/skills --skill ask-phat --agent codex --yes
  ```

- Complete Codex installation:

  ```bash
  npx skills@latest add https://gitlab.com/phatysd.dev/skills --skill '*' --agent codex --yes
  ```

- Source layout:

  ```text
  .agents/skills/<skill-name>/SKILL.md
  ```

- User documentation: `README.md` describes discovery and installation.

## Non-functional requirements

- The setup is repeatable without creating duplicate specs or changing
  established skill content.
- The published source must remain reviewable as plain text in GitLab.
- No unagreed numeric performance, availability, or telemetry target is added.

## Acceptance criteria

- AC-01: Given the repository is published at the decided GitLab source, when
  an installer runs the discovery command, then all ten current skill names
  are listed as discoverable.
- AC-02: Given the published source contains the current `ask-phat` skill, when
  an installer requests `ask-phat` for Codex, then that skill is installed and
  retains its existing `name`, `description`, and instructions.
- AC-03: Given the published source contains all ten current skills, when an
  installer requests all skills for Codex, then all ten are installed without
  changing their source instructions.
- AC-04: Given a fresh checkout of the repository, when the skill sources are
  statically inspected, then every current `SKILL.md` has valid `name` and
  `description` frontmatter, the ten skill names are unique, and each name
  matches its directory.
- AC-05: Given a user reads the repository documentation, when they look for
  installation guidance, then `README.md` explains the concrete GitLab source,
  discovery command, single-skill installation, and all-skills installation.
- AC-06: Given the repository setup is run again, when the existing project
  documents and skill sources are inspected, then no duplicate project
  documents are created and no skill instructions are changed.

## Verification plan

| AC | Verification |
| --- | --- |
| AC-01 | Run `npx skills@latest add https://gitlab.com/phatysd.dev/skills --list` against the published source and compare the names with the ten entries in `CONTEXT.md`. |
| AC-02 | Install `ask-phat` into a clean Codex target, then compare its frontmatter and instructions with the repository source. |
| AC-03 | Install `--skill '*'` into a clean Codex target and verify all ten skill directories are present. |
| AC-04 | Run a repository-local frontmatter, directory/name, and duplicate-name check over `.agents/skills/*/SKILL.md`. |
| AC-05 | Review `README.md` against the three documented CLI flows. |
| AC-06 | Rerun the setup/spec workflow and inspect the working tree for duplicate documents and unintended changes under `.agents/skills/`. |

## Open questions

- **Non-blocking:** Should the recommended default be project-scoped or global
  installation? Both are supported by the CLI and do not change the skill
  source contract.
