# Repository context

## Project identity

This repository contains reusable Agent Skills for the Phat workflow. The
completed setup objective was to make the collection discoverable and
installable from the GitLab repository through the `skills` CLI. The collection
now has 23 skills across workflow, brownfield support, utility, prototype,
verification, and optional assessment categories. `code-to-context` is complete under SPEC-002;
the latest completed feature specification is SPEC-009 for inline agent
security support. SPEC-008 covers scope changes and optional assessments.

## Vocabulary

- **Skill**: A reusable instruction set stored in a `SKILL.md` file.
- **Skill pack**: This repository's collection of skills.
- **Skill source**: `.agents/skills/<skill-name>/SKILL.md`.
- **Phat workflow**: The requirement → spec → task → implementation → review
  evidence lifecycle described in `docs/workflow.md`.
- **skills CLI**: The external CLI invoked with `npx skills@latest add` to
  discover and install skills.
- **Code-derived context**: Repository evidence maintained in the generated
  `## Codebase Context` section of `CONTEXT.md`, distinct from human-authored
  domain context and authoritative requirements.

## Established repository facts

- Skills are stored under `.agents/skills/`.
- The repository currently contains 23 skills: ten core workflow skills —
  `ask-workflow`, `grill-workflow`, `grill-design`, `setup-project`, `write-spec`,
  `to-tasks`, `implement-task`, `auto-implement`, `code-review`, and `change-scope`; one
  brownfield support skill, `code-to-context`; four utilities, `compact-context`,
  `ui-design`, `debug-task`, and `agent-security`;
  and three optional prototype skills — `to-prototype`, `edit-prototype`, and
  `spec-with-prototype`; and three verification capabilities — `unit-test`,
  `integration-test`, and `e2e-test`; and two optional assessments,
  `verify-feature` and `release-check`.
- Each current skill has a `SKILL.md` with `name` and `description` frontmatter.
- No product application code, package manifest, or repository-local build/test
  system is present.
- The canonical hosting target is the GitLab project identified by the
  configured remote `phatysd.dev/skills.git`, available at
  `https://gitlab.com/phatysd.dev/skills`.
- The source GitLab repository is intended to be public.
- The current `skills` CLI supports adding a repository through a full GitLab
  URL.
- The publication work described by SPEC-001 has completed TASK-001 and
  TASK-002; both tasks are `done`.
- SPEC-002 for `code-to-context` is complete. TASK-003 implements the
  standalone skill and TASK-004 integrates its `ask-workflow` route; both tasks are
  `done`.
- SPEC-003 for the `compact-context` utility and its conditional handoff
  integrations is complete. It is decomposed into TASK-005, TASK-006, and
  TASK-007, all `done`.
- SPEC-004 and TASK-008 record a historical research capability that was removed
  on 2026-10-03; grilling now uses project evidence and explicit user decisions.
- SPEC-006 for neutral skill identifiers is complete through TASK-012,
  TASK-013, and TASK-014, all `done`.
- SPEC-007 for automated implementation verification agents is complete
  through TASK-015, TASK-016, TASK-017, TASK-018, and TASK-019, all `done`.
- The agreed `code-to-context` behavior preserves human-authored context and
  writes only a marked generated section when implemented.

SPEC-009 and TASK-021 deliver the inline security utility and its parent/handoff
integrations; both are complete.

## Current capability: `agent-security`

`agent-security` is an inline utility for source research and host/workspace
operations. It separates retrieved evidence from authority, checks execution
scope and effects (including hooks), protects secrets, and preserves provenance
through compacted and delegated handoffs. Operational parent skills compose it;
when unavailable they retain the core boundary without automatic installation.
It adds no workflow stage, verification mode, or default confirmation for
understood authorized work. Unsafe dependent actions return concrete gaps while
unaffected work continues. It is behavioral guidance, not a sandbox guarantee.

## Current capability: `debug-task` and testing quality

`debug-task` supports standalone or inline evidence-based diagnosis without
owning production fixes or task status. Implementation uses symptom-specific
regressions and optional main-agent test-first cycles; verification capabilities
retain their selected runners and test-only writes. Test expectations must be
independent of production algorithms, and mocks must not erase the boundary
being verified. Adaptation source is Matt Pocock's diagnosing-bugs and tdd at
revision d81f3a183412e71a5b1e84ca21bc1a35eea03a60; per-skill references retain
source links and the upstream MIT notice.

## Current capability: `auto-implement`

`auto-implement` orchestrates an explicitly authorized batch of existing tasks.
It checks all task/spec prerequisites and user-action blockers before starting
any implementation, reports concrete remediation and safe unblock checks, then
composes `implement-task` inline one task at a time in dependency order.
Internal dependency edges are scheduled automatically; external blockers require
user resolution first. Verification/review and commit policy remain authoritative,
review alone owns done, and new blockers or stalled corrections stop the batch.

## Current capability: `grill-design`

`grill-design` is optional design discovery after product grilling. It records
scoped, user-confirmed UI decisions in the project's requirements under
`UI Design Requirements`, or reuses an existing authoritative design location.
New-project decisions remain a handoff summary until setup persists them.
`ui-design` consumes this agreement without modifying its reusable instructions.
`grill-workflow` asks about opting in when UI work is relevant and presents
specification, prototype, and custom-design continuations with one primary
recommendation. Confirmed design overrides must explicitly resolve conflicts
with existing direction; behavior and workflow ownership remain unchanged.

## Current capability: `ui-design`

`ui-design` is a supporting utility for content-led UI composition and rendered
inspection within an authorized parent scope. Prototype creation, targeted
prototype editing, and task implementation compose it inline when visual
choices are needed. It preserves confirmed direction and authoritative behavior;
the parent owns files, revisions, task status, required verification, and handoff.
It does not introduce a new workflow stage or require a separate agent.

## Agreed implementation verification policy

Project setup asks once for the implementation verification policy and
persists four independent modes for unit tests, integration tests, end-to-end
tests, and code review. Each mode is `auto`, `required`, or `off`.
`implement-task` uses those modes by default and accepts an explicit per-task
override. The agreed sequence is for `implement-task` to dispatch one
sub-agent per selected test capability first, wait for each terminal report,
then integrate fixes, complete final checks and commit handling, and move the
task to `in_review`. It dispatches exactly one final review sub-agent after
that transition when the review mode permits. `auto` runs a relevant
capability when its installed skill and runner are available;
`required` blocks when a relevant capability cannot be resolved or fails;
`off` skips it. Orchestration never auto-installs a missing capability.
Test sub-agents may modify only task-owned test files; final review may modify
only the selected task's review evidence and status. The main agent owns
implementation fixes, test-result integration, final verification, and commit
handling. Task commits are conditional on explicit user or repository
authorization; otherwise the verified diff remains uncommitted.
The test capability skills are `unit-test`, `integration-test`, and `e2e-test`.
The canonical review capability is `code-review`, preserving its
task/spec/acceptance-review behavior, evidence checks, and task-status
decisions. Final mode is the single automated review stage after `in_review`;
delegated mode remains read-only for other parent handoffs. Selection remains
relevance-based and records every skip reason.

Historical mapping in SPEC-006 and TASK-012: `review-with-phat` →
`review-task`. Current identifier: `code-review`, as recorded in the current
migration map and canonical skill. The historical names are not usable aliases.

The final `code-review` sub-agent may inspect the repository and report
findings, and may modify only the selected task's review evidence and status.
It may not modify implementation files, test files, project documents, or Git
state. Approval moves `in_review` to `done`; findings keep the task in
`in_review` and route back to `implement-task`.

## Verification Policy

- Status: confirmed
- Source: explicit setup confirmation
- Confirmed at: 2026-09-21

| Capability | Mode |
| --- | --- |
| `unit-test` | `required` |
| `integration-test` | `required` |
| `e2e-test` | `required` |
| `code-review` | `required` |

## Open questions

- Non-blocking: The preferred installation scope (project or global) has not
  been recorded.

## Codebase Context

<!-- phat:code-to-context:start -->

> Generated from safe repository inspection. This block describes observed implementation state and is not agreed product or architecture intent.

- Generated at: 2026-09-29T16:42:44Z
- Source revision: 096d7d917323cef359dae6565d8c8f1c861873c3 (working tree with uncommitted changes)

### Project map

- [Observed] This repository is a Phat Agent Skills pack with root guidance, workflow documentation, feature specifications, implementation tasks, individual skill sources, a static landing page, and the maintainer checker. — Source: `AGENTS.md`; `README.md`; `docs/`; `.agents/skills/`; `scripts/check_skill_pack.py`; `index.html`; `styles.css`; `script.js`
- [Observed] The source catalog has 16 skill directories; each has a `SKILL.md` and `agents/openai.yaml`, and every `SKILL.md` has `name` and `description` frontmatter. — Source: safe command `find .agents/skills -mindepth 1 -maxdepth 1 -type d`; `AGENTS.md`; `scripts/check_skill_pack.py`
- [Observed] The pack includes eight workflow skills, one brownfield skill, one utility, three prototype skills, and three verification capabilities. — Source: `AGENTS.md`; `docs/workflow.md`
- [Observed] The repository has 19 task documents and seven feature specifications; all task documents report `done`, and SPEC-005 reports `ready`. — Source: safe command `rg --files docs/tasks docs/specs` and `rg -n '^- Status:' docs/tasks docs/specs`
- [Observed] No ADR directory or ADR files were found. — Source: safe command `find docs/adr -type f -print`

### Stack and runtime

- [Observed] The landing page uses static HTML, CSS, and browser JavaScript. — Source: `index.html`; `styles.css`; `script.js`
- [Observed] No package manifest, framework, build, test-runner, lint, container, or CI configuration is documented. — Source: `AGENTS.md`; safe repository-topology inspection
- [Unknown] The browser targets, deployment runtime, and production asset pipeline are not defined. — Searched: root files, `docs/`, `.agents/skills/`, and configuration filenames

### Commands and workflows

- [Observed] The public installation source is `https://gitlab.com/phatysd.dev/skills`, installed with `npx skills@latest add`; discovery can be narrowed with `--list`, `--skill`, or `--agent`. — Source: `AGENTS.md`; `README.md`
- [Observed] The workflow supports optional custom-design discovery and prototype routes before specification, then task decomposition, implementation, verification, and review. — Source: `docs/workflow.md`; `README.md`
- [Observed] The repository consistency checker runs with `python3 scripts/check_skill_pack.py`; it checks required skill files, frontmatter names, catalog counts/listing, active skill references, router coverage, and local Markdown links. — Source: `AGENTS.md`; `docs/requirement.md`; `scripts/check_skill_pack.py`
- [Observed] Brownfield context refresh uses the `code-to-context` skill and its bundled updater, which owns only the marked generated block in `CONTEXT.md`. — Source: `.agents/skills/code-to-context/SKILL.md`; `.agents/skills/code-to-context/scripts/update_context.py`
- [Observed] Verification modes are `auto`, `required`, and `off`; task commits require explicit user or repository authorization. — Source: `docs/requirement.md`; `.agents/skills/setup-project/references/verification-policy.md`; `docs/workflow.md`
- [Observed] No repository-local build, test, lint, or deployment runner is documented; the consistency checker is the documented static maintenance check. — Source: `AGENTS.md`; `docs/requirement.md`

### Entrypoints

- [Observed] The static landing page entrypoint is `index.html`, with stylesheet and browser-script dependencies at `styles.css` and `script.js`. — Source: `index.html`
- [Observed] Each skill entrypoint is `.agents/skills/<skill-name>/SKILL.md`, with interface metadata in `agents/openai.yaml`. — Source: `AGENTS.md`; `docs/requirement.md`
- [Observed] The maintainer consistency-check entrypoint is `scripts/check_skill_pack.py`. — Source: `AGENTS.md`; `README.md`

### Module boundaries

- [Observed] Workflow behavior is separated by skill directory; requirements, context, workflow rules, specs, and task status live in root and `docs/` documents. — Source: `AGENTS.md`; `docs/workflow.md`; `.agents/skills/`
- [Inferred] Each skill is intended to be distributable independently with its `SKILL.md` and supporting resources kept under that skill directory. — Based on: `AGENTS.md`; current `.agents/skills/` topology
- [Observed] The configured verification policy requires `unit-test`, `integration-test`, `e2e-test`, and `code-review`. — Source: `CONTEXT.md` under `## Verification Policy`

### Data and integrations

- [Observed] The repository documents public GitLab skill installation and `https://docs.phatysd.me/` as Phat workflow documentation. — Source: `docs/requirement.md`; `README.md`; `index.html`
- [Observed] No application database, API server, queue, authentication service, or persistence layer is present in the inspected source/configuration. — Source: `index.html`; `script.js`; `styles.css`; repository-topology inspection
- [Unknown] Whether the hosted docs or package discovery service performs additional validation is not known from local files. — Searched: repository documentation and configuration; no external access performed

### Tests and verification

- [Observed] The pack includes `unit-test`, `integration-test`, `e2e-test`, and the canonical `code-review` skill. — Source: `.agents/skills/`; `CONTEXT.md`
- [Observed] The static checker validates the local skill catalog, metadata, active references, routing, and Markdown links. — Source: `scripts/check_skill_pack.py`; successful run in this work session
- [Observed] Verification policy uses `auto`, `required`, and `off`, with required relevant gates blocking completion when unresolved. — Source: `CONTEXT.md`; `.agents/skills/setup-project/references/verification-policy.md`
- [Unknown] No local automated test runner, browser E2E environment, CI job, or coverage configuration is defined. — Searched: package/build/test/lint/CI configuration files and repository topology

### Deployment and operations

- [Observed] The repository identifies a public GitLab installation source but contains no deployment manifest, hosting configuration, release workflow, or operations runbook for the static page. — Source: `AGENTS.md`; `docs/requirement.md`
- [Unknown] The hosting target, deployment trigger, cache strategy, and rollback process are not defined locally. — Searched: root, `docs/`, `.agents/skills/`, and deployment/CI configuration filenames

### Risks and unknowns

- [Unknown] The current published GitLab catalog and external package discovery were not re-verified in this work session. — Searched: local repository only
- [Observed] Historical migration records retain retired identifiers for audit traceability; current active routes use current identifiers and identify historical mappings where referenced. — Source: `docs/migrations/skill-identifier-migration.md`; active `.agents/skills/`; `CONTEXT.md`; `docs/requirement.md`
- [Unknown] The relationship between the static landing page and hosted docs/install source is informational only in the inspected files; no local release linkage was found. — Searched: `index.html`, `README.md`, `docs/`, and repository configuration
- [Observed] The working tree contains uncommitted skill, routing, documentation, and task-status changes. The updater must preserve human-authored context around this generated block. — Source: safe command `git status --porcelain`; `.agents/skills/code-to-context/scripts/update_context.py`

### Conflicts / Needs confirmation

- [Observed] The previous 13-versus-16 catalog conflict is resolved: current source directories, README entries, and canonical count statements all report 16 skills. — Source: `AGENTS.md`; `README.md`; `CONTEXT.md`; `docs/requirement.md`; successful `scripts/check_skill_pack.py` run
- [Observed] Historical skill identifiers remain only in migration/history references or explicit retired-identifier guidance; active invocations use current identifiers. — Source: `docs/migrations/skill-identifier-migration.md`; active skill sources; successful `scripts/check_skill_pack.py` run

<!-- phat:code-to-context:end -->
