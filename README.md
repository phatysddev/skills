# Phat Skills

**A lightweight product-to-code workflow for AI coding agents.**

Phat is a connected workflow, not a loose prompt collection:

```text
Decide before spec.
Spec before tasks.
Tasks before code.
Evidence before done.

Prototype only when seeing the UI helps.
```

The skills are designed to work with Codex and other agents that support the
Agent Skills format. They keep product decisions, project context, behavioral
specifications, implementation tasks, and review evidence connected.

## Workflow

The default path is:

```text
Idea
  ↓
ask-workflow
  ↓
grill-workflow
  ↓
optional grill-design (when custom UI direction is requested)
  ↓
setup-project
  ↓
optional setup-template (when a reusable direction is requested)
  ↓
write-spec (or to-prototype first when visual validation is requested)
  ↓
to-tasks
  ↓
implement-task
  ↓
unit-test / integration-test / e2e-test (when relevant and selected)
  ↓
code-review
```

For an existing repository with meaningful code, `ask-workflow` gives the
brownfield path priority:

```text
ask-workflow
  ↓
code-to-context
  ↓
setup-project
  ↓
write-spec
```

When visual validation will materially improve the decision, use the optional
prototype path between project setup and the final specification:

```text
setup-project
  ↓
setup-template (only when a reusable visual direction is needed)
  ↓
to-prototype
  ↓
edit-prototype ↺
  ↓
spec-with-prototype
  ↓
to-tasks
```

When a reusable published direction is not requested, continue directly from
`setup-project` to `to-prototype` or `write-spec`. Visual validation alone does
not trigger template research.

After product grilling, choose `grill-design` to customize the visual direction,
`to-prototype` to validate the UI, or `write-spec` to define behavior (initialize
project context first when needed). Design discovery is optional. Its confirmed
scoped decisions live in `UI Design Requirements` within the project's
requirements and guide `ui-design`; it does not rewrite the shared skill.

For automatic batch work, invoke `$auto-implement` after tasks exist. It scans
all scoped tasks before coding and explains every user-action blocker (such as
missing credentials, permissions, or required verification infrastructure).
Resolve those prerequisites first; it then runs `implement-task` in dependency
order under the existing verification/review policy. Normal single-task work
continues to use `implement-task`. Automatic implementation does not authorize
push/deployment or skip review.

Review findings normally return to `implement-task`. If the review exposes a
decomposition or specification problem, route back through `to-tasks` or the
owning specification workflow instead of silently expanding the implementation
task.

Utility skills are not workflow stages. A parent workflow may compose
`compact-context` inline for a temporary handoff when the context is verbose;
the utility does not advance project state, replace canonical documents, or
choose the next workflow skill. `ui-design` supports visual decisions inside
`to-prototype`, `edit-prototype`, or `implement-task` when needed; the parent
retains scope and verification ownership. Routine UI changes with an established
design may skip it. Install it alongside those skills if using a selected subset.

## Skill catalog

The collection contains 20 skills grouped by responsibility.

### Core Workflow — 10

| Skill | Responsibility |
| --- | --- |
| `ask-workflow` | Recommend the single next workflow step. |
| `grill-workflow` | Clarify requirements, domain rules, scope, and decisions. |
| `grill-design` | Optionally agree on custom UI design requirements for downstream UI work. |
| `setup-project` | Establish durable project context and workflow navigation. |
| `setup-template` | Research and persist one confirmed visual direction from published templates. |
| `write-spec` | Turn agreed decisions into an implementation-ready behavioral spec. |
| `to-tasks` | Break a ready spec into implementation-ready vertical slices. |
| `implement-task` | Implement and verify exactly one ready task. |
| `auto-implement` | Preflight all blockers, then implement an authorized task batch sequentially. |
| `code-review` | Review implementation against the spec and engineering standards. |

### Brownfield Support — 1

| Skill | Responsibility |
| --- | --- |
| `code-to-context` | Build a safe, attributable generated codebase context for an existing repository. |

### Utility — 3

| Skill | Responsibility |
| --- | --- |
| `compact-context` | Compress temporary agent handoffs without replacing canonical sources. |
| `ui-design` | Compose and refine content-led UI within prototype or implementation scope. |
| `debug-task` | Diagnose bugs and regressions with symptom-specific evidence before fixes. |

### Optional Prototype — 3

| Skill | Responsibility |
| --- | --- |
| `to-prototype` | Create a lightweight multi-page HTML/CSS/JavaScript UI prototype. |
| `edit-prototype` | Make targeted changes to a prototype page by revision ID. |
| `spec-with-prototype` | Reconcile an accepted prototype into the owning feature spec. |

The prototype skills are optional: use them when validating navigation, page
structure, states, content hierarchy, or interaction flow will reduce product
uncertainty.

### Verification Capabilities — 3

| Skill | Responsibility |
| --- | --- |
| `unit-test` | Verify isolated task behavior with a repository-detected runner. |
| `integration-test` | Verify task-owned component and service boundaries. |
| `e2e-test` | Verify task-owned critical user journeys. |

`implement-task` selects these capabilities from the project policy and task
scope. They run only when relevant and available under the configured mode;
they run before the task enters `in_review` and do not replace the single final
`code-review` stage. When automatic review is enabled, `implement-task`
dispatches that final reviewer once after `in_review`; otherwise the user can
invoke `$code-review` manually.

Diagnosis and testing guidance adapts Matt Pocock's
[diagnosing-bugs](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/skills/engineering/diagnosing-bugs/SKILL.md)
and [tdd](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/skills/engineering/tdd/SKILL.md).
`debug-task` returns evidence to the owning implementation workflow; optional
red/green development stays with the main agent and does not replace required
verification. Source links and the upstream MIT notice ship in each adapted
skill's `references/upstream.md`.

## Maintainer check

Run the repository consistency checker before publishing skill-pack changes:

```bash
python3 scripts/check_skill_pack.py
```

It checks skill source and interface files, frontmatter names, the README
catalog and documented counts, active skill references, router coverage, and
local Markdown links.

The breaking identifier migration is documented in the
[skill identifier migration map](docs/migrations/skill-identifier-migration.md).

## Installation

The canonical public source is:

```text
https://gitlab.com/phatysd.dev/skills
```

The examples below use the `skills` CLI and target Codex.

Discover the available skills before installing:

```bash
npx skills@latest add https://gitlab.com/phatysd.dev/skills --list
```

Install one skill:

```bash
npx skills@latest add https://gitlab.com/phatysd.dev/skills --skill ask-workflow --agent codex --yes
```

Install the complete current collection, including brownfield, utility,
prototype, and verification skills:

```bash
npx skills@latest add https://gitlab.com/phatysd.dev/skills --skill '*' --agent codex --yes
```

Install one skill globally instead of in the current project:

```bash
npx skills@latest add https://gitlab.com/phatysd.dev/skills --skill ask-workflow --agent codex --global --yes
```

## Repository layout

The canonical source layout for this repository is:

```text
.
├── README.md
├── LICENSE
├── AGENTS.md
├── CONTEXT.md
├── docs/
└── .agents/
    └── skills/
        ├── ask-workflow/SKILL.md
        ├── grill-workflow/SKILL.md
        ├── grill-design/SKILL.md
        ├── setup-project/SKILL.md
        ├── setup-template/SKILL.md
        ├── write-spec/SKILL.md
        ├── to-tasks/SKILL.md
        ├── implement-task/SKILL.md
        ├── auto-implement/SKILL.md
        ├── code-review/SKILL.md
        ├── code-to-context/SKILL.md
        ├── compact-context/SKILL.md
        ├── ui-design/SKILL.md
        ├── debug-task/SKILL.md
        ├── to-prototype/SKILL.md
        ├── edit-prototype/SKILL.md
        ├── spec-with-prototype/SKILL.md
        ├── unit-test/SKILL.md
        ├── integration-test/SKILL.md
        └── e2e-test/SKILL.md
```

Every installable skill has a `SKILL.md` with canonical `name` and
`description` frontmatter. Skill names and directory names use the same
lowercase kebab-case identifier.

This repository keeps `.agents/skills/<skill-name>/SKILL.md` as its source and
`skills` CLI installation contract. GitLab's native project-level convention
uses `skills/<skill-name>/SKILL.md`; adopting that path or adding a second copy
is a separate migration decision. The canonical files intentionally avoid
platform-specific frontmatter such as GitLab slash-command metadata so their
core instructions remain portable across compatible agents.

For GitLab's current Agent Skills behavior, see the [GitLab Agent Skills
documentation](https://docs.gitlab.com/user/duo_agent_platform/customize/agent_skills/).

## License

Phat Skills is released under the [MIT License](LICENSE). You may use,
modify, extend, and redistribute it, including in commercial projects, subject
to the license terms.
