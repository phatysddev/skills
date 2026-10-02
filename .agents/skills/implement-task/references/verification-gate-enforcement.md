# Implement reference: verification gate enforcement

Use this reference after capability selection when `implement-task` dispatches
test sub-agents, integrates their reports, and decides whether a task may be
committed and moved to `in_review`. The final `code-review` stage starts only
after that transition. Follow
[the sub-agent dispatch contract](sub-agent-dispatch.md) for the prompt,
waiting, and ownership rules.

## Execution plan and ordering

Create one plan from the current task, effective policy, selection summary,
task-owned test scope, and repository-supported runner evidence. Do not infer
new capabilities or runners during execution.

Dispatch selected relevant test capabilities as separate sub-agents one at a
time in this order, waiting for a terminal report before starting the next
role:

```text
unit-test → integration-test → e2e-test
```

After all selected test roles report, the main agent integrates findings,
applies in-scope fixes, runs final checks, applies commit policy, and moves the
task to `in_review`. Do not dispatch `code-review` before that transition.
`off`, irrelevant, and unavailable `auto` test roles are not dispatched, but
remain in the report with the effective mode and observable reason.

## Gate result classification

Record one terminal result for every selected role and report non-invoked
`off`/irrelevant roles with their reason:

| Result | Gate behavior |
| --- | --- |
| `passed` | gate is satisfied for this run |
| `skipped with reason` | non-blocking for `off`, an irrelevant role with a task/AC reason, or an unavailable `auto` role |
| `overridden` | policy metadata only; evaluate the gate under the explicit effective mode and record its actual run/skip result |
| `failed` | blocking; main agent fixes and reruns the affected gate |
| `blocked` | blocking; identify the missing/ambiguous/unavailable dependency and unblock condition |
| `inconclusive` | blocking; rerun or resolve the timeout, crash, or incomplete report |

Missing or ambiguous skills, runners, environments, or role mappings are
blocking for a `required` role unless a valid task-only override changes the
affected gate. For an `auto` role, the same resolution result is a non-blocking
skip with evidence. Never install, substitute, weaken, or silently omit a
required capability.

An override changes selection, not evidence. If its effective mode still selects
a relevant gate, that gate must actually pass. An override cannot relabel a failed,
blocked, or inconclusive run as passed, waive an ownership violation, or grant
review approval. Report the old and effective modes and rationale separately
from the gate's observed result.

The final `code-review` stage has its own post-`in_review` contract. A required
reviewer that is unavailable or returns unresolved findings prevents `done`.
An unavailable `auto` reviewer is a non-blocking skip that leaves the task in
`in_review`; a review that does run must resolve its findings before approval.

## Test-agent write boundary

Before dispatching a test sub-agent, identify the test files owned by the
current task from the task and specification. If no task-owned test path is
authorized, the capability may read existing tests but must not create an
arbitrary file; report the unresolved write scope when a useful test change is
required.

After each test sub-agent returns, inspect the changed-file set. Accept only
changes to the authorized task-owned test files. Reject and report writes to
production code, configuration, fixtures owned elsewhere, unrelated tests,
requirements, context, specifications, task metadata, or Git state. A
boundary violation is a blocking result and cannot be converted into a pass
by ignoring the file.

## Final-review write boundary

The final canonical `code-review` sub-agent may read the task, spec,
requirements, context, ADRs, implementation and test diff, and all test-stage
reports. It may update only the selected task's review evidence/status in its
existing `Todo` and `Status` metadata. It must not write implementation files,
test files, project documents, specifications, requirements, or Git state. Any
other write is a blocking boundary violation.

The main agent owns implementation fixes, task-owned test fixes, test-report
integration, final verification, and a task-scoped commit when commit policy
requires or authorizes one. `code-review` owns the final `in_review` to `done`
decision.

## Main-agent integration and reruns

After reports arrive, the main agent must:

1. preserve every capability status, command, runner, scope, result, finding,
   limitation, and changed-file report;
2. classify failures as task-caused, pre-existing, environmental, or
   unresolved without hiding them;
3. apply only in-scope implementation or authorized task-owned test fixes;
4. dispatch fresh sub-agents to rerun the affected gate(s) using the same
   repository-supported capability and runner, preserving required order when
   multiple gates are affected; and
5. run required final checks and record the evidence before finalization.

Do not mark a gate passed from a static assumption, a missing report, or a
command that was not run. Do not dispatch the final review before test-stage
reports are terminal and the task is `in_review`. Do not finalize while any
required test gate or ownership check remains unresolved.

## Finalization and status gate

Before moving the task to `in_review`:

- all required relevant test gates have passed, or have a valid explicit
  override/irrelevance result; auto-mode skips are recorded with evidence;
- no required test finding, missing/ambiguous resolution, timeout, crash,
  inconclusive result, or write-boundary violation remains;
- final checks and the report are recorded in the task `Todo`; and
- task metadata accurately records the final verification result while
  unrelated working-tree changes remain untouched.

If the effective repository/user commit policy requires or explicitly
authorizes a task-scoped commit, stage only task-owned paths and verify the
staged file list before creating it. Otherwise leave the verified focused diff
uncommitted and report that state.

If any condition fails, keep the task in `in_progress` or `blocked` as
appropriate, do not finalize the task, and record the exact reason and unblock
condition in `Blocked by`.

## Post-`in_review` final review

After the task enters `in_review`, dispatch exactly one fresh canonical
`code-review` sub-agent with `Mode: final` when the effective mode is
`required` or `auto` and the skill is available. Do not dispatch a second
review for the same implementation cycle. If the mode is `off`, or an
`auto` reviewer is unavailable, leave the task in `in_review` with the reason
and route to manual `$code-review` when approval is needed. The final reviewer
may update only the selected task's review evidence/status: approval moves the
task to `done`, while findings keep it in `in_review` and route back to
`$implement-task`.
