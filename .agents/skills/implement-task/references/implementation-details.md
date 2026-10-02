# Implement reference: verification and task boundaries

Read this reference when mapping acceptance criteria, selecting tests or verification, handling failures or source conflicts, classifying scope discoveries, or preparing the task-scoped commit.

## Contents

- [Acceptance-criteria traceability](#acceptance-criteria-traceability)
- [Tests](#tests)
- [Verification strategy](#verification-strategy)
- [Verification failures](#verification-failures)
- [Repository conflicts](#repository-conflicts)
- [Scope discoveries](#scope-discoveries)
- [Git policy](#git-policy)

## Acceptance-criteria traceability

Keep the task's claimed acceptance criteria visible during implementation.

For each claimed `AC-##`, map the implementation behavior and verification to
one or more Todo items. Do not add an acceptance-criteria or evidence section
to the task file.

Use a working model such as:

```text
AC-01
→ implemented behavior
→ checked Todo item after verification

AC-02
→ implemented behavior
→ checked Todo item after verification
```

Do not mark an AC covered merely because related code changed.

If implementation reveals that the task cannot actually satisfy an AC within its documented scope, do not expand the task silently.

Return the decomposition issue to `$to-tasks`.

## Tests

Add or update tests when they materially prove behavior, protect business rules, or reduce regression risk.

Prefer behavior-focused tests.

Choose the test level from the task's verification plan and the behavior being
changed:

* unit tests for isolated domain rules, calculations, validation, or state transitions;
* integration tests for boundaries between modules, APIs, databases, queues, or external services;
* end-to-end tests for critical user-visible journeys, navigation, authorization flows, or cross-layer behavior.

Use more than one level when an acceptance criterion spans multiple boundaries.
Do not require both unit and end-to-end tests for every task, and do not add a
test level merely to increase coverage. Observable/manual verification can
supplement the evidence, but cannot replace a relevant required capability or
a selected gate that failed. Apply the effective verification policy and gate
enforcement first; record unavailable auto-mode skips or valid explicit
current-task overrides with their reasons.

Test:

* important success behavior;
* relevant failure behavior;
* authorization or permission boundaries;
* important edge cases;
* business rules;
* regressions addressed by the task.

Do not add tests that merely mirror internal implementation details.

Do not force test-driven development for trivial changes where it adds ceremony without useful confidence.

Use TDD when it helps clarify business logic or safely drive behavior.
For a bug fix with a suitable seam, establish a regression that fails for the
reported symptom before fixing it. For explicit test-first work, the main agent
uses one observable behavior → red → smallest green implementation per cycle;
do not write a speculative suite for all imagined future behaviors first.
Record the seam from the task/spec and existing interfaces. Ask the user only
if selecting it requires an unresolved contract decision, not for routine test
placement. A test that fails to import is not evidence of the intended red.

The main agent owns both sides of this test-first loop. Later verification
sub-agents independently run their selected scopes with test-only write limits;
expected red during development never counts as a terminal passed gate. Keep
local refactors proportional and verified; reviewers remain reviewers and do
not acquire production-write authority from TDD.

Choose independent expected results from the spec, a known example, or a
trusted reference; do not recompute them with the algorithm under test. Prefer
caller-visible results and stable interfaces over private methods, internal
call order, or implementation-shaped snapshots. Mock external boundaries or
uncontrollable time/randomness when useful, but do not mock the boundary whose
real communication the chosen test level must verify.

Adaptation details and license: [upstream](upstream.md).

## Verification strategy

Run the narrowest relevant checks first.

Examples:

```text
targeted test
        ↓
related test suite
        ↓
typecheck / lint
        ↓
build or broader required checks
```

Use repository-supported commands only.

Do not invent commands from ecosystem convention.

Prioritize checks required by:

* the task;
* the linked spec;
* `AGENTS.md`;
* repository policy;
* CI configuration.

When practical, run broader required checks after focused verification.

Do not rerun expensive checks repeatedly without a reason.

## Verification failures

When a check fails, determine whether the failure is:

* caused by this task;
* pre-existing;
* environmental;
* unrelated;
* blocked by unavailable infrastructure.

Do not weaken, delete, skip, or rewrite a valid test merely to make the task pass.

Do not suppress type, lint, security, or validation errors without understanding them.

Fix failures caused by the task when they remain in scope. When the cause is
unclear or a fix does not resolve the symptom, compose `$debug-task` inline if
available. Preserve the original failure signal, test one evidence-backed cause
at a time, and use its regression seam for the in-scope fix. Without the support
skill, apply the same reproduce/probe discipline locally; do not auto-install it.
Diagnostic checks supplement and never replace selected verification gates.

For an unrelated pre-existing failure:

* record it;
* distinguish it from task regressions;
* continue when the task can still be responsibly verified.

If a required check cannot be run, record exactly why and what remains unverified.

## Repository conflicts

If implementation facts conflict with the source spec, do not silently choose the code over the spec or the spec over reality.

Determine the impact.

Examples:

* required API does not exist;
* existing domain model contradicts the documented rule;
* task assumes a capability the architecture does not support;
* implementation reveals an impossible acceptance criterion.

Continue independent work that remains valid when practical.

For a behavioral/specification problem:

```text
→ $write-spec
```

For a new product/domain/architecture decision:

```text
→ $grill-workflow
```

Do not rewrite the authoritative source merely to make implementation appear complete.

## Scope discoveries

Implementation often reveals nearby issues.

Classify them.

### Required for this task

Fix them when necessary to satisfy the task safely.

### Useful but not required

Do not implement them.

Record them briefly as follow-up information if worth preserving.

### Changes the feature contract

Stop the affected part and return to the owning workflow.

Avoid "while I'm here" development.


## Git policy

Resolve the effective repository/user commit policy before finalization:

* `required` — an explicit user or repository policy requires a task-scoped
  commit before `in_review`;
* `allowed` — a commit is permitted, but no commit is required; create one only
  when the user explicitly authorizes it for the current work; and
* `disabled` — do not create a commit.

When a commit is required or explicitly authorized:

1. Inspect `git status` and the diff.
2. Stage only files owned by the selected task; never use `git add .`,
   `git add -A`, or a broad path that could include unrelated work.
3. Create one task-scoped commit, for example:
   `task(TASK-###): <short goal>`.
4. Verify the commit succeeded and record its hash in the existing commit Todo item.

When a commit is not required or authorized, leave the verified focused diff
uncommitted and report that state. Do not push, rewrite history, discard
unrelated changes, or create a branch automatically. If an authorized commit
cannot be isolated safely, keep the task out of `in_review`, set it to
`blocked`, and record the reason and unblock condition in `Blocked by`.
