# SPEC-007: Automated implementation verification agents

- Status: done
- Requirement: [docs/requirement.md](../requirement.md)
- Context: [CONTEXT.md](../../CONTEXT.md)
- ADRs: None

## Problem and outcome

`implement-task` currently relies on a main agent to implement a task and then
hands off to a separately invoked review skill. Projects also lack a durable
choice about which verification levels should run. This makes test coverage,
review timing, failure handling, and the ownership of sub-agent changes
inconsistent across tasks.

The outcome is a project-configured verification workflow in which
`setup-project` asks for four independent verification modes,
`implement-task` dispatches relevant installed test capabilities in a
controlled sequence, and one final `code-review` stage runs only after the
task reaches `in_review`. The main agent owns implementation fixes, test
verification, and task-scoped commit handling; `code-review` owns the final
`in_review` to `done` decision.

This spec captures the agreed automation behavior. The canonical review
identifier and final-review ownership decisions are recorded in the project
requirement and context.

## In scope

- Ask once during `setup-project` for a mode for unit, integration, end-to-end,
  and code-review verification.
- Persist the four confirmed modes as project context and use them as the
  default for later `implement-task` runs.
- Permit an explicit per-task override without silently changing the project
  policy.
- Select `unit-test`, `integration-test`, and `e2e-test` by task scope and
  acceptance criteria; record a reason when a non-off test level is not
  relevant and is skipped.
- Run selected test sub-agents sequentially before finalization.
- Move a task to `in_review` only after implementation, selected tests,
  required fixes, final checks, and the effective commit policy are complete.
- When the `code-review` mode permits automatic execution, dispatch exactly one
  final `code-review` sub-agent after the task is `in_review`; never run a
  second pre-review or duplicate review stage.
- Resolve only detected, installed capability skills and repository-supported
  runners; never install missing skills automatically.
- Keep test sub-agents limited to creating or updating task-owned test files.
- Keep the final review sub-agent from modifying implementation, test, project,
  or Git files; it may update only the selected task's review evidence and
  status when running in final mode.
- Treat required verification failures, unresolved review findings, and missing
  required skills or runners as blocking gates unless the user supplies an
  explicit per-task override.

## Out of scope

- Implementing product application behavior.
- Choosing a test framework, test runner, or language-specific library for a
  repository that has not selected one.
- Auto-installing skills, dependencies, browsers, services, or runners.
- Allowing sub-agents to modify production implementation files.
- Replacing the task/spec review contract with an engineering-only review.
- Changing the public skill identifier migration owned by
  [SPEC-006](SPEC-006-neutral-skill-identifiers.md). Implementations must use
  `code-review` as the canonical identifier; the completed SPEC-006 migration
  remains the source of that identifier and this spec does not own the
  migration itself.
- Creating compatibility aliases for renamed skills.
- Running test or review agents concurrently.
- Creating implementation tasks.

## User flow and behavior

### Primary setup flow

1. The user invokes `setup-project` with project context ready.
2. The setup flow asks for four independent modes:
   - unit tests;
   - integration tests;
   - end-to-end tests; and
   - code review.
3. The user confirms the modes, and setup persists them as project
   verification policy without inventing defaults or changing unrelated
   project decisions.
4. A later `implement-task` invocation reads the policy before selecting
   verification work.

### Primary implementation flow

1. The main agent implements exactly one ready task.
2. The main agent applies any explicit per-task verification override for the
   current task; otherwise the persisted project policy remains authoritative.
3. For each `auto` or `required` test level that is relevant to the task scope
   and acceptance criteria, `implement-task` dispatches the corresponding
   installed capability in this order: `unit-test`, `integration-test`, then
   `e2e-test`.
4. A test capability may create or update only test files owned by the current
   task. It reports the runner, scope, commands, results, and any findings.
5. The main agent integrates test reports, fixes implementation or task-owned
   test issues within the task scope, and reruns affected checks through fresh
   test sub-agents.
6. After final checks and the effective commit policy complete, the main agent
   moves the task to `in_review`.
7. If the effective `code-review` mode permits automatic execution, the main
   agent dispatches exactly one final review sub-agent. The final reviewer
   records the review result and owns the `in_review` to `done` transition.

### Alternate flows

- **Off capability:** Do not dispatch that capability. Preserve the `off`
  state in the reported verification summary. For `code-review: off`, leave a
  ready task in `in_review` and route the user to the manual `$code-review`
  stage when final approval is needed.
- **Auto but unavailable capability:** Skip it with an observable,
  non-blocking reason. A required unavailable capability remains blocking.
- **Auto/required but irrelevant test level:** Skip the test capability and
  record the task-scope/acceptance-criteria reason. This is not a failure.
- **Missing skill or runner:** Do not install or invent a replacement. Block
  the task and identify the missing capability until an explicit per-task
  override changes the gate.
- **Test failure:** Keep the task out of commit/`in_review`; the main agent
  investigates, fixes in-scope issues, and reruns the failed gate.
- **Review finding:** Keep the task in `in_review`; the reviewer records the
  finding and routes the task to `$implement-task`. The main agent owns the
  fix and rerun before the same final review stage is attempted again.
- **Explicit per-task override:** Report the override, its affected gate, and
  its rationale. Do not silently rewrite the persisted project policy.

## Business rules and constraints

- Project verification policy is established by explicit user choices during
  setup and is reused by downstream implementation tasks.
- A task override applies only to the current task and does not mutate the
  project policy.
- Relevance is determined from the task scope and observable acceptance
  criteria, not from the mere availability of a test capability.
- `code-review` is applicable to every implementation task when its mode is
  not `off`, but automatic review runs only after the task reaches `in_review`.
- Test capabilities run in a fixed sequential order before `in_review`; the
  final review stage occurs once after that transition.
- Only installed and detected skills/runners may be invoked. The workflow must
  not auto-install missing capabilities or dependencies.
- Test sub-agents own only task-scoped test-file changes. The main agent owns
  production implementation changes, integration of test reports, final
  checks, and the task-scoped commit. `code-review` owns the final task-status
  decision from `in_review`.
- A required verification gate that is applicable cannot be silently
  downgraded to advisory status.
- Project requirements, specifications, ADRs, and explicit user decisions
  remain authoritative over generic test or review guidance.

## Data and permissions

- The verification policy is project-owned context visible to downstream Phat
  skills.
- The main agent and test sub-agents may read the task, spec, repository
  context, implementation, and existing tests needed for the selected gate.
- Test sub-agents may write only task-owned test files.
- The final review sub-agent may read the relevant diff and evidence and may
  update only the selected task's review evidence and status. It may not write
  implementation files, test files, project source files, specifications,
  requirements, or Git state.
- The main agent is the only actor that may apply implementation fixes and
  create the task-scoped commit.
- No credentials, private repository content, or unrelated external service
  state is sent to an external skill or service by this workflow.

## Errors and edge cases

- A project has no persisted verification policy: stop and route to setup
  rather than inventing modes.
- A policy has missing or malformed mode values: report the unresolved
  policy and block implementation until setup or an explicit task override
  repairs the state.
- A task's acceptance criteria do not justify a non-off test level: skip it
  with a recorded reason rather than manufacturing a test target.
- Multiple installed skills claim the same capability role: treat the mapping
  as ambiguous and block until the user or project policy resolves it.
- A test sub-agent attempts to modify production files: reject the change,
  report the boundary violation, and keep the task blocked.
- A final review sub-agent attempts to change any file outside the selected
  task's review evidence/status boundary: reject the write and keep the task
  in review until a clean final review is completed.
- A test sub-agent times out, crashes, or returns an inconclusive result: treat
  the affected required gate as unresolved and block unless an explicit
  per-task override applies. A final review timeout or crash leaves the task
  in `in_review` with an unresolved review result.
- The identifier migration remains a separate concern owned by completed
  SPEC-006. Its earlier `review-with-phat` to `review-task` mapping is
  superseded by the confirmed `code-review` canonical identifier recorded in
  the requirement and context.

## Interfaces and observable test points

- Setup output shows the four verification modes and the confirmed project
  policy.
- Project context exposes the persisted policy and distinguishes it from a
  per-task override.
- An implementation report identifies each selected capability as `passed`,
  `skipped with reason`, `failed`, `blocked`, or `overridden`.
- The report shows the sequential test order, the `in_review` transition, and
  at most one final `code-review` stage.
- Test-agent changes are limited to task-owned test files, and final-review
  changes are limited to the selected task's review evidence/status.
- A failed, missing, ambiguous, or inconclusive required test gate prevents the
  task-scoped commit and `in_review` transition. A required final-review issue
  prevents the `done` transition.
- A successful run shows the main agent's final rerun and the evidence used
  before commit.
- `code-review` preserves the existing Phat review outputs: findings,
  acceptance-criteria assessment, check status, and task-status decision when
  invoked as the single final review workflow.

## Non-functional requirements

- **Safety:** no automatic dependency or skill installation and no hidden
  external writes.
- **Traceability:** every selected, skipped, failed, blocked, and overridden
  capability has an observable reason or result.
- **Isolation:** sub-agent write permissions are limited to their documented
  task-owned surfaces.
- **Determinism:** the same project policy and task evidence produce the same
  capability-selection order unless an explicit override is present.
- **Maintainability:** capability selection uses role-based discovery rather
  than hard-coded provider names.

## Acceptance criteria

- AC-01: Given a project entering `setup-project`, when the verification policy
  is configured, then the user is asked for independent unit, integration,
  end-to-end, and code-review modes, each with the value `auto`, `required`,
  or `off`, and the confirmed values are persisted as project context.
- AC-02: Given a persisted project policy, when `implement-task` starts a
  task, then it uses that policy by default and applies an explicit per-task
  override only to the current task.
- AC-03: Given `auto` or `required` test modes, when task scope and acceptance
  criteria are evaluated, then only relevant test capabilities run and every
  skipped non-off level includes an observable reason.
- AC-04: Given a non-off capability role, when the workflow resolves the
  implementation, then it uses only one detected installed skill/runner for
  that role and blocks on missing or ambiguous resolution without
  auto-installing a replacement.
- AC-05: Given relevant `auto` or `required` test capabilities, when
  implementation verification runs, then `unit-test`, `integration-test`, and
  `e2e-test` execute sequentially in that order before the task enters
  `in_review`, and automatic `code-review` runs at most once after that
  transition.
- AC-06: Given a test sub-agent is invoked, when it writes changes, then only
  task-owned test files are modified and its commands/results are reported.
- AC-07: Given `code-review` is not `off`, when an implementation task reaches
  `in_review`, then exactly one final review sub-agent inspects the resulting
  diff and may update only the selected task's review evidence/status; it does
  not modify implementation, test, project, or Git files.
- AC-08: Given a test failure, missing runner, missing skill, ambiguous skill
  resolution, timeout, or inconclusive required test result, when no explicit
  per-task override applies, then the task cannot be committed or moved to
  `in_review`. A required final-review failure prevents `done`.
- AC-09: Given the main agent receives test reports or a later review finding,
  when an actionable in-scope issue exists, then the main agent owns the fix
  and reruns affected test gates before the task enters or re-enters the final
  review stage.
- AC-10: Given a user supplies an explicit per-task override, when a non-off
  gate is changed for that task, then the report identifies the overridden
  gate and rationale without changing the persisted project policy.
- AC-11: Given a successful implementation and test verification run for a
  ready task, then the task-scoped commit contains only task-owned changes and
  the task enters `in_review`, where the single final review workflow may move
  it to `done`.
- AC-12: Given the canonical `code-review` identifier is used, when the single
  final review is invoked, then it preserves the established task/spec/evidence
  review behavior while operating under the new identifier.

## Verification plan

| AC | Verification |
| --- | --- |
| AC-01 | Run setup with representative `auto`, `required`, and `off` combinations and inspect the persisted project policy and confirmation output. |
| AC-02 | Run an implementation with no override and with a task-only override; compare the selected capabilities and confirm project policy is unchanged. |
| AC-03 | Use tasks with unit-only, integration-boundary, e2e-flow, and mixed acceptance criteria; verify relevant selections and explicit skip reasons. |
| AC-04 | Provide installed, missing, and duplicate capability-role mappings; verify detected-only behavior, blocking, and no auto-install. |
| AC-05 | Inspect timestamps/order and agent reports for a mixed task; verify tests finish, the task enters `in_review`, and the final review runs at most once afterward. |
| AC-06 | Review the test sub-agent diff and file list; verify production files remain unchanged and commands/results are recorded. |
| AC-07 | Run the final code review on an `in_review` task with a known finding; verify only task review evidence/status may change and the report is evidence-backed. |
| AC-08 | Simulate failed, unavailable, ambiguous, timeout, and inconclusive test gates plus a final-review failure; verify no commit/`in_review` transition for test failures and no `done` transition for review failures. |
| AC-09 | Seed an actionable test or review finding; verify the main agent applies the fix and reruns only affected test gates plus required final checks before the single final review. |
| AC-10 | Apply an explicit override and inspect both the task report and unchanged project policy. |
| AC-11 | Inspect the final staged diff, commit contents, task status, and unrelated working-tree changes. |
| AC-12 | Compare the renamed skill body and review output against SPEC-006's accepted pre-rename behavior; verify canonical references use `code-review` and no compatibility alias is introduced. |

## Open questions

- **Non-blocking:** The exact persisted Markdown/YAML representation of the
  four modes can be selected during task planning if it remains inspectable
  and idempotent.
- **Non-blocking:** The exact role-discovery metadata fields and framework
  detection commands can be selected during implementation without changing
  the observable behavior.
