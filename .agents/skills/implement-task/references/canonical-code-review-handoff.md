# Implement reference: canonical code-review handoff

Use this reference when `implement-task` dispatches the single final review
sub-agent after the task has entered `in_review`.

## Canonical identity

Resolve exactly one installed capability with both of these properties:

```text
role: code-review
skill: <resolved installed code-review skill path>
frontmatter name: code-review
```

The source pack stores it at `.agents/skills/code-review/SKILL.md`; an installed
copy may live in a host-specific project or global skill directory. Resolve the
host's active installed path rather than requiring the source-pack layout in
every consumer repository. The canonical identifier is `code-review`. `review-task` and
`review-with-phat` are retired identifiers, not aliases or fallback skills.
If the canonical skill is missing or multiple skills claim the role, a
`required` mode is blocked while an `auto` mode records a non-blocking skip;
do not install, alias, or substitute one.

## Ordering and policy

The selected test stage must report completion before finalization, and the
task must enter `in_review` before `code-review` starts.
The handoff is sequential:

```text
selected unit-test → integration-test → e2e-test stages
        ↓
main-agent final checks and in_review
        ↓
one final canonical code-review
```

The exact test-stage selection and order are owned by the verification
selection and gate-enforcement contracts. This handoff must not start review
before `in_review`, run a second review for the same implementation cycle, or
run test and review capabilities concurrently.

When effective `code-review` is `required`, review is applicable to every
implementation task and an unavailable reviewer leaves the task in `in_review`
with a blocking review result. When it is `auto`, dispatch it when the
canonical skill is available; an unavailable reviewer is a non-blocking skip
that leaves the task in `in_review`. When it is `off` or explicitly overridden
to `off`, do not dispatch it; report the effective mode, override, and rationale
without mutating the persisted project policy and route to manual review when
needed.

## Final mode

The parent must dispatch exactly one fresh sub-agent using the canonical skill
and identify the handoff as `Mode: final`. The task is already `in_review`.
Do not execute review inline in the parent, and do not dispatch it concurrently
with a test sub-agent or a second reviewer. The final reviewer may update only
the selected task's review evidence in its existing `Todo` and `Status`
metadata; it may not modify implementation, test, project, specification,
requirement, or Git files.

The parent waits for the final review sub-agent's terminal report before
reporting the task outcome. Approval moves `in_review` to `done`; findings keep
the task in `in_review` and route to `$implement-task`. If a later fix changes
the implementation or task-owned tests, that is a new implementation cycle:
the task returns through test gates and receives one fresh final review.

## Review input contract

Pass the reviewer enough context to preserve the existing Phat review:

1. the selected task and its implementation evidence;
2. the complete linked feature specification and claimed acceptance criteria;
3. `AGENTS.md`, `CONTEXT.md`, requirements, and relevant ADRs;
4. the final implementation diff and any task-owned test diff; and
5. every selected test-stage report, including skipped, blocked, overridden,
   failed, or passed results.

Do not reduce the handoff to a generic code-quality prompt or discard test
evidence before review.

## Review output contract

Forward the canonical review result without changing its meaning. It must
retain:

- actionable findings with severity, locations, evidence, impact, and fix
  direction;
- acceptance-criteria verification and any unverified criteria;
- checks run, checks not run, and residual limitations or uncertainty; and
- the task-status decision and next workflow route.

The final reviewer records the result in the selected task's existing `Todo`
checklist and updates `Status` according to the findings/status contract.
Review output does not grant permission to alter implementation or Git state.

## Read-only ownership boundary

The final review capability may read the repository, task, spec, context, diff,
tests, and reports. It may write only the selected task's review evidence and
status metadata. It may not write implementation files, task-owned test files,
project requirements, specifications, ADRs, or Git state.

The main agent owns all implementation integration work: applying in-scope
fixes, rerunning affected tests and checks, and creating a task-scoped commit
only when commit policy requires or authorizes one. A final-review write outside
the task evidence/status boundary is a violation and keeps the task in review
until a clean final review is completed.
