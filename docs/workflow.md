# Phat workflow

The shared lifecycle is:

```text
requirement
    ├─ optional prototype → edit-prototype* → spec reconciliation
    └─ spec
    ↓
task
    ↓
implementation
    ↓
review evidence
```

Default task states are:

```text
todo → in_progress → in_review → done
```

Use `blocked` when work cannot continue. A blocked task records the blocker,
the reason, and the condition that will unblock it.

A spec with material blocking questions is not ready for implementation. Scope
changes must update the owning source of truth, and accepted prototype
behavior must be reconciled into the owning spec before task decomposition.

## Skill categories

The pack distinguishes five kinds of capability:

- **Workflow skills:** `ask-workflow`, `grill-workflow`,
  `grill-design` (optional), `setup-project`, `write-spec`, `to-tasks`,
  `implement-task`, `auto-implement`, and `code-review`. They own project-state transitions
  and handoffs.
- **Brownfield support:** `code-to-context` derives a safe generated context
  snapshot before setup or specification work in an existing codebase.
- **Utility skills:** `compact-context` reduces a temporary handoff;
  `debug-task` supports evidence-driven diagnosis without production fixes;
  `ui-design` supports content-led UI composition and rendered inspection when
  visual decisions are needed. All three may be composed inline by a parent without
  advancing project state, replacing canonical documents, or choosing the next
  workflow skill. `ui-design` works only within the parent's authorized UI files.
- **Optional prototype skills:** `to-prototype`, `edit-prototype`, and
  `spec-with-prototype` support visual validation before specification without
  replacing the requirement or behavioral spec as source of truth.
- **Verification capabilities:** `unit-test`, `integration-test`, and
  `e2e-test` verify task-owned behavior under the project policy. They may write
  only task-owned test files. `implement-task` dispatches one sub-agent per
  selected test capability in sequence, moves the task to `in_review` after
  finalization, then dispatches one final `code-review` sub-agent when its mode
  permits automatic review.

Workflow skills do not silently continue into unrelated workflow stages.
An explicitly invoked `auto-implement` batch is the bounded exception: after
whole-batch blocker preflight, it composes `implement-task` sequentially and
continues in-scope corrections. It does not authorize other product stages,
policy changes, push, deployment, or external provisioning.
`implement-task` explicitly dispatches its configured verification capabilities
and, after entering `in_review`, its single final `code-review` stage. Utility
skills may be used internally within the parent's scope; the parent remains
responsible for authoritative documents, verification, and the next explicit handoff.

### Verification and finalization policy

`setup-project` records one mode for each verification capability in
`CONTEXT.md`: `auto`, `required`, or `off`. `implement-task` applies the mode
to the current task's observable scope. `auto` runs when the relevant skill and
runner are available, `required` blocks when they cannot be resolved or fail,
and `off` skips the capability. Test capabilities run sequentially before
finalization and `in_review`; one final `code-review` stage runs after
`in_review` when its mode permits automatic review. Test agents may write only
task-owned test files, while final review may write only the selected task's
review evidence and status.

Move a task to `in_review` only after required test gates are resolved and the
implementation is ready for final review. `code-review` owns the final
`in_review` to `done` transition. Create a task-scoped commit only when an
explicit user or repository policy requires or authorizes it; otherwise leave
the verified focused diff uncommitted. Never push automatically.

## Skill handoffs

- `$grill-workflow`: resolve unsettled product, scope, domain, or architecture
  decisions.
- `$grill-design`: optionally clarify and record scoped, confirmed UI design
  requirements after product grilling; `ui-design` consumes that agreement.
- `$setup-project`: establish repository context and workflow navigation.
- `$code-to-context`: derive read-only repository evidence into the marked
  generated context section when existing code context is missing or stale.
- `$compact-context`: reduce a verbose temporary handoff when a parent workflow
  explicitly needs a smaller agent-facing summary; never use it as a substitute
  for reading a canonical requirement, spec, task, or review target.
- `$debug-task`: diagnose reported symptoms standalone or inline; return
  reproduction/cause evidence to implementation without replacing test gates.
- `$ui-design`: support visual decisions within prototype creation, targeted
  edits, or task-owned UI implementation; skip routine UI work whose design is
  already determined. It does not replace required tests/review or add a stage.
- `$write-spec`: turn an agreed requirement into an implementation-ready
  feature specification.
- `$to-tasks`: decompose a ready specification into implementation tasks.
- `$implement-task`: implement one ready task and record evidence.
- `$auto-implement`: scan an authorized existing task batch for all user-action
  blockers, provide remedies and wait for their resolution, then compose
  `implement-task` sequentially in dependency order. New blockers stop the batch;
  internal dependency edges alone do not require user intervention.
- `$code-review`: review implementation evidence and decide whether the
  task is ready for `done`.
- `$ask-workflow`: route the next step when the project state is unclear.
- `$to-prototype`: create a lightweight prototype when visual validation is
  useful before finalizing a specification.
- `$edit-prototype`: make targeted changes to an existing prototype revision.
- `$spec-with-prototype`: reconcile an accepted prototype into the owning
  implementation-ready specification.

For UI work, `grill-workflow` asks once whether custom-design discovery is
wanted, explains `grill-design`, `to-prototype`, and `write-spec`, and recommends
one primary next step without invoking it. An opt-in routes to `grill-design`;
otherwise setup readiness and visual-validation intent determine the next step.
Design discovery records Agreed constraints, preferences, delegated choices,
references, and verification in `docs/requirement.md` under
`UI Design Requirements`, or the existing authoritative design location.
New-project summaries are persisted by setup. Explicit scoped overrides resolve
conflicts with base Design Direction; proposals never silently override it.

```text
grill-workflow → optional grill-design → setup-project when needed
                                      → to-prototype or write-spec
```

The optional prototype path is:

```text
setup-project → to-prototype → edit-prototype* → spec-with-prototype → to-tasks
```

Use it only when seeing the UI helps resolve navigation, hierarchy, state, or
interaction uncertainty. It does not replace the owning requirement or spec.

The brownfield path is:

```text
ask-workflow → code-to-context → setup-project → specification
```

When meaningful implementation exists, missing or stale generated Codebase
Context takes precedence over setup. Setup reuses a fresh generated context
and inspects source only to resolve gaps or verify facts required for setup.

The compact utility may sit beside, not inside, the canonical workflow:

```text
grill-workflow ──┐
                 └─ optional compact-context → setup-project
```

Do not insert it between a spec and `to-tasks`, a task and `implement-task`, or
a spec and `code-review`; those consumers read the canonical artifact in
full.

## Source of truth

- Product/setup requirement: `docs/requirement.md`
- Repository and domain context: `CONTEXT.md`
- Agent navigation and working rules: `AGENTS.md`
- Feature specifications: `docs/specs/`
- Implementation tasks: `docs/tasks/`

The publication feature is complete and documented in
[`SPEC-001`](specs/SPEC-001-publish-phat-skill-pack.md). Its implementation
tasks — [`TASK-001`](tasks/TASK-001-source-and-installation-contract.md) and
[`TASK-002`](tasks/TASK-002-verify-public-gitlab-installation.md) — are both
`done`.

[`SPEC-002`](specs/SPEC-002-code-to-context.md) is complete. Its implementation
tasks — [`TASK-003`](tasks/TASK-003-code-to-context-skill.md) and
[`TASK-004`](tasks/TASK-004-route-code-to-context-from-ask-phat.md) — are both
`done`.

[`SPEC-003`](specs/SPEC-003-compact-context-utility.md) is complete. It covers
the compact utility and conditional handoffs. Its
implementation tasks — [`TASK-005`](tasks/TASK-005-compact-context-skill.md),
[`TASK-006`](tasks/TASK-006-integrate-compact-handoffs.md), and
[`TASK-007`](tasks/TASK-007-refresh-public-skill-catalog.md) — are all `done`.

[`SPEC-005`](specs/SPEC-005-setup-template.md) and TASK-009 through TASK-011
are historical records of a removed template-selection stage. Project setup
now hands off directly to prototype or specification, with optional custom
design discovery through `grill-design`.

[`SPEC-004`](specs/SPEC-004-phatysd-docs-research.md) and
[`TASK-008`](tasks/TASK-008-conditional-phatysd-docs-research.md) are historical.
The Phatysd Docs research step was removed on 2026-10-03.

[`SPEC-006`](specs/SPEC-006-neutral-skill-identifiers.md) is complete through
[`TASK-012`](tasks/TASK-012-rename-skill-source-identifiers.md),
[`TASK-013`](tasks/TASK-013-update-skill-references-and-migration.md), and
[`TASK-014`](tasks/TASK-014-verify-neutral-skill-catalog.md), all `done`.

[`SPEC-007`](specs/SPEC-007-automated-verification-agents.md) is complete
through [`TASK-015`](tasks/TASK-015-configure-verification-policy.md),
[`TASK-016`](tasks/TASK-016-add-test-capability-skills.md),
[`TASK-017`](tasks/TASK-017-select-verification-capabilities.md),
[`TASK-018`](tasks/TASK-018-enforce-verification-gates.md), and
[`TASK-019`](tasks/TASK-019-integrate-canonical-code-review.md), all `done`.

Specification lifecycle: `write-spec` establishes a spec as `ready` for task
decomposition. A maintainer or owning workflow changes it to `done` only after
every linked implementation task is `done` and no open question or blocker
remains. A spec stays `ready` while any linked task is `todo`, `in_progress`,
`in_review`, or `blocked`.
