---
name: integration-test
description: "Verify task-owned boundaries between modules, APIs, data stores, queues, or services with one repository-detected integration runner. Use when implement-task selects integration-test verification."
---

# Integration Test

Verify boundary behavior for the current implementation task using only a
runner and environment that the repository already documents or exposes. This
skill is a test capability dispatched by `implement-task` as a dedicated
sub-agent; it does not choose project policy, modify production code, or
install missing infrastructure.

## Contents

- [Role boundary](#role-boundary)
- [Workflow](#workflow)
- [Determine relevance](#determine-relevance)
- [Resolve one runner](#resolve-one-runner)
- [Test-file ownership](#test-file-ownership)
- [Test quality](#test-quality)
- [Execution and outcomes](#execution-and-outcomes)
- [Report contract](#report-contract)
- [Finish](#finish)

## Role boundary

This capability covers observable boundaries between modules, APIs, databases,
queues, filesystems, external services, or other runtime components. It
verifies that the participating components communicate and handle boundary
success or failure behavior correctly.

Do not dispatch another capability or sub-agent from this capability. Do not
use it for isolated rules that do not cross a boundary or for a complete user
journey. Do not select a test framework, install a dependency, manually
provision infrastructure, or invent a runner command. A repository-owned test
command may start its configured service, container, database, or temporary
dependency as part of normal execution. The task, specification, repository
context, and explicit project policy remain authoritative.

## Workflow

Follow this sequence:

```text
Read task and project context
        ↓
Determine whether integration verification is relevant
        ↓
Resolve exactly one existing repository runner and available environment
        ↓
Run the task-relevant boundary scope, or report an unresolved gate
        ↓
Report commands, results, findings, and file ownership
```

Read `AGENTS.md`, `CONTEXT.md`, the selected task, its linked specification,
and the relevant implementation before selecting a scope. Read existing
integration tests, fixtures, service configuration, and repository test
guidance when present; do not scan unrelated code.

## Determine relevance

Run integration verification only when the task scope or observable
acceptance criteria includes a component boundary. Identify the exact modules,
interfaces, data stores, queues, or services that justify the selection.

If the integration mode is `off`, a task-only override sets it to `off`, or the
task contains no boundary behavior, return `skipped with reason` and do not run
a command. The reason must identify the mode or task-scope evidence;
availability of an integration runner is not itself a reason to run it.

## Resolve one runner

Inspect only repository-supported evidence, such as:

* commands and test conventions in `AGENTS.md`, `CONTEXT.md`, and repository
  documentation;
* package-manager scripts and integration configuration when those files exist;
* language manifests, Makefiles, task runners, and CI workflows;
* existing integration-test files, fixtures, service definitions, and nearby
  configuration; and
* documented local or CI prerequisites that are already available.

Prefer an explicitly documented integration command. If documentation is
absent, use a runner command only when repository configuration identifies one
unambiguously. Record the evidence path and exact command, plus any already
available environment required to run it.

If no usable runner or required existing environment is detected, return
`blocked` with `runner: missing` and execute nothing. If more than one runner
or command is a plausible match and repository evidence does not select one,
return `blocked` with `runner: ambiguous` and list the candidates. Never
install or upgrade a skill, dependency, browser, service, database, or
replacement runner to resolve the result.

## Test-file ownership

The current task and its specification define the task-owned test-file scope.
The capability may create or update only those test files, and only when the
task explicitly owns test changes or the main agent has assigned that scope.

It may read existing tests, fixtures, and configuration needed for selection
and execution. It must not modify production files, runtime configuration,
fixtures owned by another task, unrelated tests, `CONTEXT.md`, requirements,
specifications, task metadata, or Git state. If a useful test change has no
clear task-owned path, report the boundary as an unresolved finding instead
of creating an arbitrary file.

## Test quality

Choose a stable observable interface that reaches the task's actual failure
pattern. Derive expected results independently from requirements or known
examples; do not repeat the production algorithm inside assertions. Prefer
behavior/results over private methods or incidental internal call counts.
A red result must represent the intended symptom, not missing setup/imports.
When reporting a regression, distinguish a failure observed before the fix from
a test only run on fixed code; do not invent prior red evidence.

Exercise the actual communication between participating components. Do not
mock away the tested boundary; a test with both sides replaced cannot prove
integration. Use supported test environments and documented fixtures, with
doubles only for external boundaries outside the contract under test. Database
inspection is legitimate when persistence itself is the observable contract;
prefer public retrieval when the requirement concerns retrievable behavior.

Use the narrowest meaningful scope. Avoid speculative extra test levels or
mandatory user approval for seams already established by task/spec. The main
agent owns red/green production fixes; this capability remains test-only and
returns failures for that agent to resolve.

Adaptation details and license: [upstream](references/upstream.md).

## Execution and outcomes

Run the smallest relevant integration scope first and use the exact detected
command. Do not hide failures, weaken assertions, delete tests, or reinterpret
a runner or service error as a pass.

Use these statuses:

* `passed` — the selected integration scope ran and passed;
* `failed` — the runner executed and reported a failure;
* `blocked` — required runner, environment, or scope resolution is missing,
  ambiguous, unavailable, or inconclusive;
* `skipped with reason` — policy, task scope, or an explicit override makes
  this capability inapplicable; and
* `overridden` — policy-selection metadata with its rationale, never a
  substitute for the observed run or skip result. Also report the actual outcome
  under the effective mode; a selected relevant gate still must pass.

A failed, blocked, or inconclusive selected and relevant integration gate
remains a required result for the main agent to resolve. The capability
reports the result; the main agent owns implementation fixes, reruns, and
finalization.

## Report contract

Return an observable report containing every field below:

```text
Capability: integration-test
Status: passed | failed | blocked | skipped with reason | overridden
Relevance: relevant | irrelevant — <task-scope reason>
Runner: <one detected runner and evidence path>, or missing/ambiguous
Scope: <task-owned boundary behavior and test files considered>
Commands: <exact commands executed, or none>
Results: <exit/result summary and relevant output>
Changed test files: <paths, or none>
Findings: <failures, unresolved risks, or none>
Write boundary: <confirmation that only task-owned test files changed>
Limitations: <missing environment or uncertainty, or none>
```

For `blocked`, include why resolution could not continue and the unblock
condition. For `skipped with reason` or `overridden`, include the policy value
or explicit user rationale. Do not claim `passed` without an observed result.

## Finish

Stop after returning the report. Do not invoke another capability, change
production implementation, alter task status, commit, push, or install
anything.
