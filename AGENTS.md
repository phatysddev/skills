# Repository guidance

This repository is a small collection of Agent Skills for the Phat workflow.

## Project navigation

- Project goal: [`docs/requirement.md`](docs/requirement.md)
- Domain and repository context: [`CONTEXT.md`](CONTEXT.md)
- Workflow contract: [`docs/workflow.md`](docs/workflow.md)
- Feature specifications: [`docs/specs/`](docs/specs/)
- Implementation tasks: [`docs/tasks/`](docs/tasks/)
- Individual skills: [`.agents/skills/`](.agents/skills/)
- Latest completed specification: [`SPEC-009`](docs/specs/SPEC-009-agent-security.md)

## Repository structure

Each installable skill lives at `.agents/skills/<skill-name>/SKILL.md`.
Every `SKILL.md` must keep YAML frontmatter with `name` and `description`.

The current pack contains 23 skills:

- Core workflow: `ask-workflow`, `grill-workflow`, `grill-design`, `setup-project`,
  `write-spec`, `to-tasks`, `implement-task`, `auto-implement`,
  `code-review`, `change-scope`.
- Optional assessments: `verify-feature`, `release-check`.
- Brownfield support: `code-to-context`.
- Utility: `compact-context`, `ui-design`, `debug-task`, `agent-security`.
- Optional prototype: `to-prototype`, `edit-prototype`,
  `spec-with-prototype`.
- Verification capabilities: `unit-test`, `integration-test`, `e2e-test`.

## Commands and verification

No package manifest, build configuration, test runner, or lint configuration is
currently present, so no repository-local build, test, or lint commands are
known. The repository provides a standard-library consistency checker:

```bash
python3 scripts/check_skill_pack.py
```

Run it after changing skill sources, metadata, routing, or catalog documents.

The target installation command, supplied as the project requirement, is:

```bash
npx skills@latest add https://gitlab.com/phatysd.dev/skills
```

Use `--list` to verify discovery before installing, and use `--skill` or
`--agent` to narrow the installation when needed.

## Working rules

- Preserve the existing skill names and directory layout unless an explicit
  requirement changes them.
- Keep skill-specific instructions inside the corresponding `SKILL.md`.
- Treat `docs/requirement.md` as the product/setup requirement source of truth.
- Treat `CONTEXT.md` as the source of repository and domain vocabulary.
- Follow [`docs/workflow.md`](docs/workflow.md) for Phat workflow states and
  handoffs.
- Treat feature specifications as the source of behavioral contracts and tasks
  as the source of implementation status; do not infer intended decisions from
  implementation behavior alone.
- The agreed `code-to-context` capability may update only its generated section
  in `CONTEXT.md`; it must preserve human-authored context and must not modify
  `AGENTS.md`, README, specs, tasks, or ADRs.
- Do not commit or push automatically unless explicitly requested.
- When implementation needs a commit decision, classify it as `required`,
  `allowed`, or `disabled`; absent an explicit user or repository requirement,
  leave the verified focused diff uncommitted.
