# To Tasks reference: task templates and coverage

Read this reference when creating task files, writing task checklists, handling task-specific context or verification, using spikes, or running the final coverage checks.

## Contents

- [Task shape](#task-shape)
- [Goal](#goal)
- [Scope boundaries](#scope-boundaries)
- [Context for a new session](#context-for-a-new-session)
- [Implementation notes](#implementation-notes)
- [Verification](#verification)
- [Checklist ownership](#checklist-ownership)
- [Spikes](#spikes)
- [Coverage checks](#coverage-checks)

## Task shape

Use this structure by default:

```markdown
# TASK-###: <behavioral slice>

- Status: todo
- Spec: [relative link]

## Goal

Describe the behavioral result and include links to the authoritative spec,
requirement, context, or ADRs needed in a fresh session.

## Blocked by

List only real upstream task IDs that must be completed first. Use `- None`
when the task can start. If an external blocker appears, record the reason and
unblock condition here without inventing a new task.

## Todo

Use unchecked items for work that remains and checked items only after the work
is actually complete:

- [ ] Implement the task's behavioral slice.
- [ ] Verify the acceptance criteria and relevant failure paths.
- [ ] If repository policy or user instructions require a commit, commit only
      the task-scoped changes; otherwise leave the focused diff for review.
```

Adapt the headings when the repository already has an established task format.

## Goal

The goal should describe the result, not the activity.

Prefer:

```text
Customers can cancel an eligible upcoming booking.
```

Avoid:

```text
Implement cancellation code.
```

The goal should make it possible to tell whether the task succeeded without reading its implementation.

Keep the Goal concise but include the authoritative links or essential context
needed to start the task. Do not add a separate context section.

When visual behavior matters, link to the owning spec and any prototype IDs it
uses as supporting evidence. The spec, not the prototype, remains authoritative.

## Scope boundaries

Keep each task aligned with the source spec.

Represent scope boundaries through specific Todo items and links to the source
spec. Do not add `In scope`, `Out of scope`, or acceptance-criteria sections to
the task file.

A task may cover:

* one acceptance criterion;
* multiple closely related acceptance criteria;
* part of an acceptance criterion when multiple tasks are genuinely required to complete it.

Do not claim an acceptance criterion is fully covered when the task delivers only part of it.

When multiple tasks jointly satisfy an AC, make that relationship explicit.

Do not add behavior that exists only because it seems technically useful.

## Context for a new session

Assume `$implement-task` may run in a fresh conversation. Put the minimum
context and authoritative links in `Goal`, upstream task IDs in `Blocked by`,
and all implementation, acceptance, verification, and commit work in `Todo`.

Prefer:

```text
Read:
- docs/specs/SPEC-004-booking.md
- docs/adr/0002-authentication.md

Relevant existing area:
- current booking module
```

over copying entire requirements into the task. The task should be resumable
without becoming a duplicate source of truth.

## Implementation notes

Implementation notes belong in the Goal or in a specific Todo item; do not add
an `Implementation notes` section to a generated task file. They may contain:

* established architecture constraints;
* reusable existing components or modules;
* known integration boundaries;
* compatibility requirements;
* relevant patterns already used in the repository.

Do not turn implementation notes into generated code.

Do not over-design the solution before `$implement-task` inspects the current code.

Use phrases such as:

```text
Reuse the existing authorization boundary.
```

when supported by the repository.

Avoid speculative instructions such as:

```text
Create BookingManagerFactoryService in src/services/factories/.
```

unless that structure is already an agreed contract.

## Verification

Every task must have a concrete definition of done represented by Todo items.

Verification may include:

* unit tests;
* integration tests;
* end-to-end tests;
* type checking;
* linting;
* build verification;
* API contract checks;
* authorization checks;
* accessibility checks;
* responsive checks;
* manual observable verification when automation is not justified.

Use commands only when they are supported by repository evidence.

Do not invent commands because they are common for the framework.

For example:

```text
Verification:
- `pnpm test -- booking`
- `pnpm typecheck`
- Confirm an unavailable slot cannot be submitted through the booking UI.
```

If no known command exists, write an observable verification Todo item and
leave command discovery to implementation rather than fabricating one.

## Checklist ownership

Do not create an `Evidence` section in task files. A new task starts with all
Todo items unchecked. `$implement-task` checks items only after performing the
work and records command/result detail in the checklist item or its commit.

Implementation and review workflows own actual evidence such as:

* tests executed;
* commands and results;
* screenshots;
* relevant diff references;
* manual checks;
* review findings.

`$to-tasks` plans the checklist; it does not claim that any Todo item is done.

## Spikes

Use a spike only when a technical unknown prevents responsible task planning but does not require a new product decision.

Examples include:

* confirming whether an existing API supports a required operation;
* determining compatibility with an existing library version;
* validating an uncertain integration constraint.

A spike should be explicitly labeled:

```text
Type: spike
```

and define:

* question being answered;
* why the answer is needed;
* investigation boundary;
* concrete exit condition;
* downstream tasks it may unblock.

A spike does not satisfy a user-facing acceptance criterion merely because research was performed.

If the unknown is actually a product, domain, scope, or architecture decision, route to `$grill-workflow` instead.

## Coverage checks

Before finishing, verify all of the following.

### Acceptance coverage

Every source `AC-##` is mapped to one or more tasks.

No task claims an acceptance criterion that does not exist in the target spec.

No criterion is silently omitted.

### Task boundaries

Every task represents a coherent implementation slice.

Tasks are not divided mechanically by database/backend/frontend layers without justification.

No two tasks own the same implementation slice unnecessarily.

### Dependencies

Dependency IDs exist.

No dependency cycle exists.

Dependencies describe actual blocking relationships.

At least one task is runnable if implementation can begin.

### Context

Every task links to its source spec.

Each task contains enough context for a new implementation session.

Large project rationale is linked rather than duplicated.

### Verification

Every task contains a concrete verification approach.

Verification reflects the acceptance criteria the task claims to cover.

No fake evidence has been recorded.
