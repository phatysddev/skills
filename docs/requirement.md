# Requirement: publish and maintain the Phat skill pack

Status: active skill-pack contract

## Problem and outcome

The current Phat skills are stored locally but do not yet have a documented
repository-level setup for distribution. Users should be able to install the
collection from its GitLab repository with the `skills` CLI.

## Goal

Make the existing skill collection installable with:

```bash
npx skills@latest add https://gitlab.com/phatysd.dev/skills
```

The source GitLab repository is public.

## Current skill pack

The published collection contains 19 installable skills:

- Core workflow: `ask-workflow`, `grill-workflow`, `grill-design`, `setup-project`,
  `write-spec`, `to-tasks`, `implement-task`, `auto-implement`, and
  `code-review`.
- Brownfield support: `code-to-context`.
- Utility: `compact-context`, `ui-design`, `debug-task`.
- Optional prototype: `to-prototype`, `edit-prototype`, and
  `spec-with-prototype`.
- Verification capabilities: `unit-test`, `integration-test`, and `e2e-test`.

The skill pack keeps the `.agents/skills/<skill-name>/SKILL.md` source layout
and `agents/openai.yaml` interface metadata for every skill.

## Completed capability: `code-to-context`

The completed Phat capability is a standalone skill that reads an existing
repository and maintains code-derived context so downstream Phat skills can
continue without rediscovering the codebase.

The skill will:

- update only a generated `## Codebase Context` section in `CONTEXT.md`,
  creating `CONTEXT.md` when it does not exist;
- preserve human-authored context and authoritative requirements;
- use a fixed Markdown schema covering the project map, stack, commands,
  entrypoints, module boundaries, data and integrations, tests, deployment,
  risks, and unknowns;
- label claims as `Observed`, `Inferred`, or `Unknown`, and attach source paths,
  line references when useful, and generated date/commit metadata;
- record conflicts for later confirmation instead of resolving them silently;
- inspect source, manifests, configuration, tests, CI, and relevant docs while
  excluding generated output, dependencies, vendor files, build output, and
  secrets;
- use only safe read-only discovery commands and redact sensitive values;
- be recommended by `ask-workflow` for explicit refresh or a concrete repository
  knowledge gap that blocks the next scoped step and needs broad discovery;
  missing generated context or changed commits alone must not interrupt active tasks.

The skill must not modify code, configuration, `AGENTS.md`, README, specs, or
tasks, and must not create ADRs or implementation tasks from observations.

## Current capability: `compact-context`

`compact-context` is an inline utility for reducing verbose intermediate agent
handoffs. It may be composed by a parent workflow when the handoff is
materially repetitive, multilingual, or too long for the next step.

It must preserve decisions, facts, constraints, scope, exact identifiers,
paths, commands, acceptance criteria, references, unresolved questions, and
conflicts. It must not replace canonical documents, route the project, or be
inserted between a canonical spec/task and the workflow that consumes it.

## Current capability: diagnosis and behavior-focused testing

Adapt the relevant diagnosing-bugs and tdd guidance from mattpocock/skills into
Phat boundaries. Add `debug-task` for reproductions, evidence-driven hypotheses,
and bounded probes, with production fixes/status owned by implementation.
Improve existing testing capabilities with independent expected results,
regression seams that preserve the real trigger, and doubles that do not erase
the boundary under test. Optional red/green cycles run in the main implementation
agent; verification sub-agents still modify only authorized tests. Preserve
existing policy, runner/delegation requirements, review ownership, auto-implement
blocker rules, and correction budgets. Retain pinned upstream attribution and
license per adapted skill rather than installing the upstream workflow verbatim.

## Current capability: `auto-implement`

Support explicit automatic implementation of all existing tasks in an authorized
repository/spec/task batch. Whole-batch preflight must identify all user-action
blockers before implementation, explain each affected task's concrete remedy,
expected configuration location, and safe unblock check, and wait until all are
resolved. Internal task dependencies are automatic scheduling edges, not user
setup blockers. Secret values belong in the project's actual local environment
or secret store, never chat or task records. Execution composes `implement-task`
sequentially, preserves required tests/final review, stops for new blockers or
stalled corrections, and reports actual task states without auto-marking done or
changing policy. Batch authorization does not grant commit, push, deployment,
external provisioning, or additional product decisions.

## Current capability: `grill-design`

Provide optional custom-design discovery after `grill-workflow`. For UI work,
product grilling asks once whether the user wants design customization, then
explains `grill-design`, `to-prototype`, and `write-spec` with one recommended
next step, without invoking it. Design discovery records explicit scoped
constraints, preferences, delegated choices, references, and verification in
`docs/requirement.md` under `UI Design Requirements` (or an existing authoritative
location). New projects carry a summary through `setup-project` for persistence.
`ui-design` must read and follow applicable Agreed decisions. Customization must
not edit shared skill instructions, silently replace confirmed branding, invent
product behavior, or require design discovery for every UI task.

## Current capability: `ui-design`

Requested as a reusable supporting skill for reducing generic AI-generated UI.
It is composed inline when prototype or task-owned UI work needs meaningful
visual decisions, including by `to-prototype`, `edit-prototype`, and
`implement-task`. It grounds composition in content, users, existing design
systems and confirmed direction, then inspects rendered states and responsive
layouts when tools are available. It preserves the parent's scope, behavioral
sources, file boundaries, verification gates, and workflow ownership. Routine
UI edits with an already determined design need not invoke it. Missing support
is reported with a local-pattern fallback and never auto-installed.

## Maintainer consistency check

The repository provides `scripts/check_skill_pack.py` as a standard-library
static checker. It verifies that every skill directory has its required source
and interface metadata, each source name matches its directory, active skill
references point to current identifiers, workflow skills are covered by
`ask-workflow`, README catalog entries and documented counts match the source
catalog, and local Markdown links resolve. Run it with
`python3 scripts/check_skill_pack.py` before publishing repository changes.

## Agreed implementation verification policy

`setup-project` will ask once per project for four independent verification
modes: `unit-test`, `integration-test`, `e2e-test`, and `code-review`. Each mode
is one of `auto`, `required`, or `off`:

- `auto` runs when the capability is relevant and a repository-supported skill
  and runner are available; otherwise it records a non-blocking skip reason;
- `required` runs when relevant and blocks the task when the required skill or
  runner is missing, ambiguous, unavailable, or fails; and
- `off` does not invoke the capability and records the configured mode.

`implement-task` uses the persisted modes as defaults for each task and accepts
an explicit per-task override. The agreed orchestration is sequential:
`implement-task` dispatches one sub-agent per selected test capability, waits
for each terminal report, integrates fixes, completes final checks and commit
handling, and moves the task to `in_review`. It then dispatches exactly one
final `code-review` sub-agent when the review mode permits automatic execution.
The final reviewer owns the `in_review` to `done` decision, so the same task
does not receive a pre-review and a second final review.

The orchestration may dispatch only detected, installed testing and review
skills as dedicated sub-agents. It must not auto-install missing skills or run
a selected capability inline when delegation is unavailable. A missing
capability blocks a `required` mode and is a non-blocking skip for an `auto`
mode.

Test sub-agents may create or update only task-owned test files. A final review
sub-agent may update only the selected task's review evidence and status; it
may not modify implementation, tests, project documents, or Git state. The
main agent owns implementation fixes, test-result integration, final
verification, and task-scoped commit handling.

The skill pack includes three test capability skills: `unit-test`,
`integration-test`, and `e2e-test`. The canonical review capability is
`code-review`, preserving its task/spec/acceptance-review behavior, evidence
checks, and task-status decisions. Selection of verification modes per task is
relevance-based: `auto` and `required` test skills run only when the task scope
and acceptance criteria require them, `off` skills are skipped, every skip
records a reason, and non-off `code-review` is applicable to every
implementation task. `code-review` supports explicit standalone, final, and
delegated modes. Final mode is the single automated review stage after
`in_review`; delegated mode remains read-only for other parent handoffs.

Historical mapping in SPEC-006 and TASK-012: `review-with-phat` →
`review-task`. Current identifier: `code-review`, as recorded in the current
migration map and canonical skill. The historical names are not usable aliases.

The final `code-review` sub-agent may inspect the repository and report
findings, and may update only the selected task's review evidence and status.
It may not modify implementation files, test files, project documents,
requirements, specifications, or Git state. Approval moves `in_review` to
`done`; findings keep the task in `in_review` and route back to
`implement-task`.

Task commits are conditional: create a task-scoped commit only when an explicit
user or repository policy requires or authorizes agent commits. Otherwise leave
the verified focused diff ready for review, and never push automatically.


## In scope

- Preserve the `.agents/skills/<skill-name>/SKILL.md` layout.
- Keep each skill's required `name` and `description` frontmatter.
- Document discovery, installation, and Phat workflow navigation for all 19
  skills across workflow, brownfield, utility, prototype, and verification
  categories.
- Keep catalog and workflow updates idempotent; change skill instructions only
  through a reviewed, traceable specification/task scope.

## Out of scope for this setup

- Adding unrelated product application features.
- Implementing product features.
- Choosing installation policy without an explicit decision.

## Verification criteria

- `npx skills@latest add https://gitlab.com/phatysd.dev/skills --list` discovers
  the current 19 skills across the documented categories after publication.
- A selected skill can be installed by name.
- The complete collection can be installed with the CLI's all-skills option.
- The installed skill files retain valid frontmatter and their existing
  instructions.
