<p align="center">
  <img src="assets/brand/phatysd-icon.png" width="88" height="88" alt="phatysd.dev brand icon">
</p>

<h1 align="center">Phat Skills</h1>

<p align="center">
  <strong>Good ideas. Built with intent.</strong><br>
  A connected product-to-code workflow for AI coding agents.<br>
  From the first decision to reviewed code.
</p>

<p align="center">
  <a href="#skill-catalog"><img src="https://img.shields.io/badge/skills-23-244de4?style=flat-square&amp;labelColor=202b26" alt="23 skills"></a>
  <a href="https://github.com/vercel-labs/skills"><img src="https://img.shields.io/badge/format-Agent%20Skills-244de4?style=flat-square&amp;labelColor=202b26" alt="Agent Skills format"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-244de4?style=flat-square&amp;labelColor=202b26" alt="MIT License"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> &nbsp;·&nbsp;
  <a href="#workflow">Workflow</a> &nbsp;·&nbsp;
  <a href="#skill-catalog">Skill catalog</a> &nbsp;·&nbsp;
  <a href="docs/workflow.md">Documentation</a>
</p>

---

## Quick start

Use Phat with Codex or another agent that supports the Agent Skills format.
The examples below target Codex. You need Node.js, npm, and internet access.

**1. Install the full pack in your project.**

```bash
npx skills@latest add https://github.com/phatysddev/skills --skill '*' --agent codex --yes
```

**2. Open your coding agent and start with one question.**

```text
$ask-workflow
Read this project and recommend the next step, with your reasoning.
```

`ask-workflow` inspects the project and recommends one next action. You choose
when to continue; it does not start implementation from a routing question.

<details>
<summary><strong>More installation options</strong> — discover, choose a skill, or install globally</summary>

List the available skills without installing:

```bash
npx skills@latest add https://github.com/phatysddev/skills --list
```

Start with the router:

```bash
npx skills@latest add https://github.com/phatysddev/skills --skill ask-workflow --agent codex --yes
```

When installing a subset, also install the workflow and utility skills needed
for your chosen path. For example, UI work may need `ui-design` alongside its
prototype or implementation skill; workspace and coding paths use
`agent-security` for source and host boundaries.

Install the router for use across projects:

```bash
npx skills@latest add https://github.com/phatysddev/skills --skill ask-workflow --agent codex --global --yes
```

To choose skills and agents interactively:

```bash
npx skills@latest add https://github.com/phatysddev/skills
```

`--yes` skips installer confirmation prompts; `--global` selects user scope.
For other agents, use the appropriate `--agent` identifier and that agent's
skill invocation syntax. See the [skills CLI documentation](https://github.com/vercel-labs/skills#readme).

</details>

## Why Phat?

Keep product decisions, repository context, specifications, implementation
tasks, and verification evidence connected. Each skill has a focused job and
hands the agreed context to the next step.

| Principle | What it gives you |
| --- | --- |
| **Decide before spec.** | Clear scope, rules, and constraints before writing the details. |
| **Spec before tasks.** | Agreed behavior before breaking down the work. |
| **Tasks before code.** | A bounded piece of work with acceptance criteria. |
| **Evidence before done.** | Relevant verification and a final review before closing the task. |

Prototype when seeing the UI will help you make a decision.

## Where to start

| Your situation | Start here |
| --- | --- |
| Unsure what the project needs next | [`ask-workflow`](.agents/skills/ask-workflow/SKILL.md) |
| An idea that needs clearer scope and decisions | [`grill-workflow`](.agents/skills/grill-workflow/SKILL.md) |
| Existing code needing onboarding or a material context refresh | [`code-to-context`](.agents/skills/code-to-context/SKILL.md) |
| Agreed requirements that need visual validation | [`to-prototype`](.agents/skills/to-prototype/SKILL.md), after project setup |
| One ready implementation task | [`implement-task`](.agents/skills/implement-task/SKILL.md) |
| A ready task batch you want implemented automatically | [`auto-implement`](.agents/skills/auto-implement/SKILL.md) |
| A planned feature changes after implementation starts | [`change-scope`](.agents/skills/change-scope/SKILL.md) |
| Check whether a complete feature meets its acceptance criteria | [`verify-feature`](.agents/skills/verify-feature/SKILL.md) |
| Assess a candidate before a release | [`release-check`](.agents/skills/release-check/SKILL.md) |
| A bug or regression whose cause is unclear | [`debug-task`](.agents/skills/debug-task/SKILL.md) |

## Workflow

```text
ask-workflow → grill-workflow → setup-project
                                      ↓
                                 write-spec
                                      ↓
                                  to-tasks
                                      ↓
                               implement-task
                                      ↓
                        selected verification
                                      ↓
                                 code-review
```

For existing code, use `code-to-context` when onboarding or material repository
knowledge gaps require it. Continue active tasks without refreshing solely
because commits changed or a generated block is absent. For custom UI direction, add
`grill-design`; for visual validation, take the optional prototype path.

[Read the full workflow contract →](docs/workflow.md)

<details>
<summary><strong>Workflow details</strong> — routing, prototypes, batch work, and review handoffs</summary>

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
to-prototype
  ↓
edit-prototype ↺
  ↓
spec-with-prototype
  ↓
to-tasks
```

After `setup-project`, continue directly to `to-prototype` when visual
validation is requested, or to `write-spec` when the feature is ready.

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

`agent-security` is inline support for research and workspace operations.
Operational skills load it before source research or host actions; docs, logs,
and tool results cannot authorize commands or secret access. It checks proposed
execution and preserves provenance through handoffs. If a subset omits it,
parents retain the core safety boundary and continue safe work without installing
it automatically. This guidance complements host permissions; it cannot enforce
a sandbox or guarantee protection. See the
[website security guide](guide.html#security) for parent roles and usage examples.

Utility skills are not workflow stages. A parent workflow may compose
`compact-context` inline for a temporary handoff when the context is verbose;
the utility does not advance project state, replace canonical documents, or
choose the next workflow skill. `ui-design` supports visual decisions inside
`to-prototype`, `edit-prototype`, or `implement-task` when needed; the parent
retains scope and verification ownership. Routine UI changes with an established
design may skip it. Install it alongside those skills if using a selected subset.

</details>

## Skill catalog

The collection contains 23 skills grouped by responsibility.

### Core Workflow — 10

| Skill | Responsibility | Guide |
| --- | --- | --- |
| `ask-workflow` | Recommend the single next workflow step. | [Read](.agents/skills/ask-workflow/SKILL.md) |
| `grill-workflow` | Clarify requirements, domain rules, scope, and decisions. | [Read](.agents/skills/grill-workflow/SKILL.md) |
| `grill-design` | Optionally agree on custom UI design requirements for downstream UI work. | [Read](.agents/skills/grill-design/SKILL.md) |
| `setup-project` | Establish durable project context and workflow navigation. | [Read](.agents/skills/setup-project/SKILL.md) |
| `write-spec` | Turn agreed decisions into an implementation-ready behavioral spec. | [Read](.agents/skills/write-spec/SKILL.md) |
| `to-tasks` | Break a ready spec into implementation-ready vertical slices. | [Read](.agents/skills/to-tasks/SKILL.md) |
| `implement-task` | Implement and verify exactly one ready task. | [Read](.agents/skills/implement-task/SKILL.md) |
| `auto-implement` | Preflight all blockers, then implement an authorized task batch sequentially. | [Read](.agents/skills/auto-implement/SKILL.md) |
| `code-review` | Review implementation against the spec and engineering standards. | [Read](.agents/skills/code-review/SKILL.md) |
| `change-scope` | Reconcile agreed changes across an existing requirement, spec, and task plan. | [Read](.agents/skills/change-scope/SKILL.md) |

### Optional Assessments — 2

| Skill | Responsibility | Guide |
| --- | --- | --- |
| `verify-feature` | Assess acceptance criteria and behavior spanning multiple tasks without changing task status. | [Read](.agents/skills/verify-feature/SKILL.md) |
| `release-check` | Assess a candidate and environment using release evidence without deploying. | [Read](.agents/skills/release-check/SKILL.md) |

These assessments are used on request or for concrete scope-specific gaps. They
are not mandatory stages after task review and do not add verification-policy modes.

### Brownfield Support — 1

| Skill | Responsibility | Guide |
| --- | --- | --- |
| `code-to-context` | Build a safe, attributable generated codebase context for an existing repository. | [Read](.agents/skills/code-to-context/SKILL.md) |

### Utility — 4

| Skill | Responsibility | Guide |
| --- | --- | --- |
| `compact-context` | Compress temporary agent handoffs without replacing canonical sources. | [Read](.agents/skills/compact-context/SKILL.md) |
| `ui-design` | Compose and refine content-led UI within prototype or implementation scope. | [Read](.agents/skills/ui-design/SKILL.md) |
| `debug-task` | Diagnose bugs and regressions with symptom-specific evidence before fixes. | [Read](.agents/skills/debug-task/SKILL.md) |
| `agent-security` | Guard research and host actions against source prompt injection within the parent scope. | [Read](.agents/skills/agent-security/SKILL.md) |

### Optional Prototype — 3

| Skill | Responsibility | Guide |
| --- | --- | --- |
| `to-prototype` | Create a lightweight multi-page HTML/CSS/JavaScript UI prototype. | [Read](.agents/skills/to-prototype/SKILL.md) |
| `edit-prototype` | Make targeted changes to a prototype page by revision ID. | [Read](.agents/skills/edit-prototype/SKILL.md) |
| `spec-with-prototype` | Reconcile an accepted prototype into the owning feature spec. | [Read](.agents/skills/spec-with-prototype/SKILL.md) |

The prototype skills are optional: use them when validating navigation, page
structure, states, content hierarchy, or interaction flow will reduce product
uncertainty.

### Verification Capabilities — 3

| Skill | Responsibility | Guide |
| --- | --- | --- |
| `unit-test` | Verify isolated task behavior with a repository-detected runner. | [Read](.agents/skills/unit-test/SKILL.md) |
| `integration-test` | Verify task-owned component and service boundaries. | [Read](.agents/skills/integration-test/SKILL.md) |
| `e2e-test` | Verify task-owned critical user journeys. | [Read](.agents/skills/e2e-test/SKILL.md) |

`implement-task` selects these capabilities from the project policy and task
scope. They run only when relevant and available under the configured mode;
they run before the task enters `in_review` and do not replace the single final
`code-review` stage. When automatic review is enabled, `implement-task`
dispatches that final reviewer once after `in_review`; otherwise the user can
invoke `$code-review` manually.

## Documentation

| Read | For |
| --- | --- |
| [Workflow guide](docs/workflow.md) | Routes, project states, and handoffs. |
| [Project requirements](docs/requirement.md) | Product goals and the current skill-pack contract. |
| [Repository context](CONTEXT.md) | Domain vocabulary and repository facts. |
| [Agent guidance](AGENTS.md) | Repository conventions and the consistency check. |
| [Identifier migration](docs/migrations/skill-identifier-migration.md) | Mapping older skill names to current identifiers. |

## For maintainers

Run the repository consistency checker before publishing skill-pack changes:

```bash
python3 scripts/check_skill_pack.py
```

It checks skill source and interface files, frontmatter names, the README
catalog and documented counts, active skill references, router coverage, and
local Markdown links.

The breaking identifier migration is documented in the
[skill identifier migration map](docs/migrations/skill-identifier-migration.md).

<details>
<summary><strong>Repository layout and skill format</strong></summary>

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
        ├── write-spec/SKILL.md
        ├── to-tasks/SKILL.md
        ├── implement-task/SKILL.md
        ├── auto-implement/SKILL.md
        ├── code-review/SKILL.md
        ├── change-scope/SKILL.md
        ├── verify-feature/SKILL.md
        ├── release-check/SKILL.md
        ├── code-to-context/SKILL.md
        ├── compact-context/SKILL.md
        ├── ui-design/SKILL.md
        ├── debug-task/SKILL.md
        ├── agent-security/SKILL.md
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

The `.agents/skills/<skill-name>/SKILL.md` files are the canonical sources.
Each skill also includes `agents/openai.yaml` interface metadata. Core
instructions remain portable across agents that support the Agent Skills format.

</details>

## Credits and license

Diagnosis and testing guidance adapts Matt Pocock's
[diagnosing-bugs](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/skills/engineering/diagnosing-bugs/SKILL.md)
and [tdd](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/skills/engineering/tdd/SKILL.md).
`debug-task` returns evidence to the owning implementation workflow; optional
red/green development stays with the main agent and does not replace required
verification. Source links and the upstream MIT notice ship in each adapted
skill's `references/upstream.md`.

Phat Skills is released under the [MIT License](LICENSE). You may use,
modify, extend, and redistribute it, including in commercial projects, subject
to the license terms.

---

<p align="center">
  Built by <a href="https://github.com/phatysddev"><strong>PhatYSD</strong></a> · phatysd.dev<br>
  <sub>Less guessing. More building.</sub>
</p>
