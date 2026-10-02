# Review reference: findings and status

Read this reference when classifying review findings, writing the finding record, separating questions from defects, recording a review result, or deciding the task status.

## Contents

- [Severity](#severity)
- [Finding format](#finding-format)
- [Questions and suggestions](#questions-and-suggestions)
- [No findings](#no-findings)
- [Review record](#review-record)
- [Status transition](#status-transition)

## Severity

Use severity based on actual impact.

### P0 — Critical

Use for an issue that makes the change unsafe to ship under normal conditions.

Examples:

* serious security exposure;
* destructive data loss;
* catastrophic correctness failure;
* system-wide failure caused by the change.

Use P0 rarely.

### P1 — High

Use for important defects such as:

* core acceptance criterion failure;
* authorization bypass;
* significant security issue;
* incorrect critical business behavior;
* corruption or major state inconsistency.

The task cannot become `done`.

### P2 — Medium

Use for normal required defects such as:

* missing required edge behavior;
* incomplete error handling that affects users;
* meaningful regression;
* incorrect non-critical behavior;
* verification gap that prevents confidently approving an AC.

The task normally remains `in_review` until resolved.

### P3 — Low

Use for a real but low-impact issue worth correcting.

Examples:

* small maintainability defect;
* minor required behavior mismatch;
* localized robustness issue.

Do not use P3 merely for taste or stylistic preference.

## Finding format

Order findings by severity.

Use:

```markdown
### P1 — <concise title>

**Location:** `path/to/file.ts:120-138`

**Evidence**
Explain the exact observed behavior, code path, failing check, or mismatch.

**Impact**
Explain what breaks or what risk this creates.

**Spec / AC**
AC-## or engineering risk.

**Fix direction**
Describe the smallest useful direction for correction without implementing it.
```

Use the narrowest useful location.

Prefer exact lines when available.

When an issue spans several files, identify the primary location and mention supporting locations as needed.

Do not produce vague findings such as:

```text
The code could be cleaner.
```

## Questions and suggestions

Keep these separate from defects.

Use them only when useful.

### Question

Use when review cannot determine whether behavior is intended.

A question is not automatically a defect.

If answering it requires a product/domain/architecture decision:

```text
→ $grill-workflow
```

If it exposes an incomplete behavioral contract:

```text
→ $write-spec
```

### Optional suggestion

Use sparingly for improvements that are genuinely optional.

Do not let suggestions affect task status.

## No findings

If there are no actionable findings, state:

```text
No findings.
```

Then report:

* acceptance criteria verified;
* checks passed;
* checks not run;
* residual uncertainty, if any.

Do not invent low-severity issues merely to avoid returning a clean review.

## Review record

When the review is associated with a Phat task, update its `Status` and append
or update a concise review item in the existing `Todo` checklist. Keep the
task body limited to `Goal`, `Blocked by`, and `Todo`; do not create a `Review`
section.

Use a checked item for approval:

```markdown
- [x] Review approved — `<target>` against `<base>`; AC-01 and AC-02 verified;
  `<check>` passed; no findings.
```

Use an unchecked item when changes are required or an external blocker remains:

```markdown
- [ ] Review changes requested — P2 at `path/to/file.ts:120`; fix and re-run
  `<check>` before review.
```

Record only target, acceptance-criteria results, checks, findings, and
limitations that actually exist. Preserve implementation checklist items and
prior review history when practical. The final response may contain the full
finding details.

On re-review, mark a prior changes-requested item resolved only after verifying
its underlying required findings and affected checks. Preserve its original
finding and add the resolution evidence; do not leave an active unresolved
request alongside a new approval for the same findings.

## Status transition

Review owns the final transition from `in_review`.

### Approve

Set:

```text
Status: done
```

only when:

* the task's in-scope behavior is implemented;
* all claimed acceptance criteria are sufficiently verified;
* no P0, P1, or unresolved required defect remains;
* required relevant gates have passed or have a valid explicit task override /
  irrelevance result under the effective policy; a documented limitation alone
  cannot waive a required gate;
* the review result and concise evidence are recorded in the task's `Todo`;
* no known blocker remains.

A task does not need to be theoretically perfect to become `done`.

It must satisfy its documented contract to a reasonable engineering standard.

### Request changes

Keep:

```text
Status: in_review
```

when fixable findings remain.

Record the result in the existing task checklist:

```text
Status: in_review
- [ ] Review changes requested — <finding and fix direction>
```

Route to:

```text
$implement-task
```

for the same task.

Do not create a new task merely to repair the current task unless the original decomposition is itself wrong.

### Blocked

In standalone mode, use `Status: blocked` only for a concrete external or
decision blocker and record its reason and unblock condition in `Blocked by`.

In final mode, preserve `Status: in_review` and record the blocker and unblock
condition as an unchecked review Todo item. Return a blocked review result;
do not edit `Blocked by`, which is outside the final review write boundary.
Delegated mode returns the same blocker without writing any file.
