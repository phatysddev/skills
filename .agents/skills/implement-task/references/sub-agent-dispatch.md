# Implement reference: verification sub-agent dispatch

Use this reference when `implement-task` dispatches verification work after
implementation. The parent `implement-task` agent owns orchestration; each
selected test capability and the single final review run in their own
sub-agent.

## Dispatch rule

Do not execute a selected test capability or final `code-review` inline in the
main agent. Use the host's available sub-agent/delegation mechanism to dispatch
one sub-agent per selected capability, passing the exact installed skill
identity and the capability's report contract.

If the host exposes no delegation mechanism, treat a relevant `required`
capability as `blocked` and a relevant `auto` capability as a non-blocking
`skipped with reason`. Never silently run the capability inline as a fallback.

Sub-agents must not dispatch other sub-agents. They perform only the delegated
capability and return one terminal report to the parent.

## Selection and ordering

Use the selection result already recorded by `implement-task`:

1. dispatch `unit-test` when its effective mode and relevance select it;
2. wait for its terminal report;
3. dispatch `integration-test` when selected, then wait for its terminal report;
4. dispatch `e2e-test` when selected, then wait for its terminal report; and
5. after every selected test report is terminal, integrate findings, run final
   checks, apply commit policy, and move the task to `in_review`;
6. dispatch exactly one final `code-review` sub-agent after `in_review` when its
   effective mode permits execution.

Never dispatch test capabilities concurrently, and never dispatch final review
before `in_review` or more than once per implementation cycle. `off`,
irrelevant, and unavailable `auto` roles are not dispatched; preserve their
reason in the parent report.

Each dispatch is a fresh sub-agent run. After a main-agent fix, do not reuse a
previous report as evidence: dispatch a fresh run for every affected gate,
preserving the same order, and dispatch one fresh final review after the task
re-enters `in_review`.

## Test sub-agent prompt contract

The parent prompt must include:

- `Mode: delegated verification`;
- the exact role and skill path (`unit-test`, `integration-test`, or
  `e2e-test`);
- the selected task, linked spec, relevant project context, acceptance
  criteria, implementation diff, and task-owned test scope;
- the effective mode, relevance decision, resolved repository runner, and
  runner evidence;
- the write boundary: only the explicitly task-owned test files may change;
- the prohibition on production, configuration, unrelated-test, project
  document, task metadata, and Git-state writes; and
- the required terminal report fields: result, runner/command, scope,
  findings, limitations, and changed files.

The sub-agent must stop after returning that report. It must not update task
status, edit production code, install or provision infrastructure, commit, or
invoke another capability.

## Final code-review sub-agent prompt contract

Dispatch exactly one canonical `code-review` sub-agent using its resolved installed path
after the task is `in_review` when the effective review mode permits execution.
Its prompt must include:

- `Mode: final`;
- the exact task, complete linked spec, requirements, `AGENTS.md`,
  `CONTEXT.md`, relevant ADRs, final implementation/test diff, and every
  terminal test-stage report;
- the instruction to inspect the supplied evidence against the task and
  acceptance criteria; and
- the write boundary: only the selected task's existing review evidence and
  `Status` metadata may change; no implementation, test, project-document,
  specification, requirement, or Git-state writes.

The reviewer returns one terminal report with findings, acceptance-criteria
assessment, checks and limitations, and a status recommendation. In final mode
the reviewer records supported review evidence and moves `in_review` to `done`
only when the findings/status contract permits it. Findings keep the task in
`in_review` and route it to `$implement-task`.

## Parent integration boundary

After every test sub-agent returns, the parent inspects the changed-file set
before continuing. A write outside the task-owned test scope is a blocking
boundary violation. After the final review sub-agent returns, only writes to
the selected task's existing review evidence/status boundary are accepted; any
other write attempt is a blocking boundary violation.

The parent classifies test results, preserves reports, fixes only in-scope
issues, performs final checks, and applies the effective commit policy. The
final review sub-agent owns the final `in_review` to `done` status decision;
test sub-agents do not own any orchestration or task-state action.
