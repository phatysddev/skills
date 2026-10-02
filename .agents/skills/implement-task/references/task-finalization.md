# Implement reference: task finalization

Read this reference after implementation when updating the task checklist,
deciding whether it is ready for review, or reporting the result.

## Task record

Task files keep only `Goal`, `Blocked by`, and `Todo` body sections, plus their
existing `Status` and `Spec` metadata. Record implementation, verification, and
commit progress in `Todo`; do not add `Evidence`, `Review`, `In scope`, `Out of
scope`, or other sections. Mark an item checked only after its result is
observed, and include command/result detail when it is not otherwise visible.

If work cannot safely continue, set `Status: blocked` and record the reason,
impact, and unblock condition in `Blocked by`. Use `blocked` only for a
concrete inability to continue, and continue the same task when the blocker is
resolved.

## Review readiness

Set `Status: in_review` only when:

- in-scope behavior is implemented and claimed acceptance criteria are
  addressed;
- useful task-owned tests are added or updated;
- required relevant verification gates passed or have a valid explicit override /
  irrelevance result; recording a limitation alone does not satisfy a required gate;
- required implementation, verification, and commit Todo items are checked and
  reflect current implementation; review-approval items remain reviewer-owned;
- required or explicitly authorized commit handling is complete, or the
  focused uncommitted diff is ready for review;
- no known blocker prevents meaningful review; and
- the diff is focused enough to review.

`in_review` is not `done`. Only `$code-review` owns the final transition.
For a correction cycle, record the fix and current verification beside prior
review findings while preserving their history. An unchecked request awaiting
re-review does not itself prevent returning to `in_review` once the underlying
defect is fixed; never check an approval item on the reviewer's behalf.

## Final quality gate

Before reporting, confirm:

- exactly one task was implemented and dependencies were complete;
- unrelated changes were preserved and no hidden scope was added;
- acceptance criteria remain traceable to behavior and evidence;
- verification policy, overrides, selected roles, skips, and blockers are
  accurately recorded;
- selected test capabilities ran sequentially under task-owned write limits;
- all required gates and relevant reruns are resolved before `in_review`;
- final review dispatch follows the configured policy and happens after
  `in_review`;
- no requirement, spec, or ADR was silently rewritten; and
- Git handling follows the effective policy.

See [verification gate enforcement](verification-gate-enforcement.md) for
gate, ordering, ownership, and commit decisions, and
[implementation details](implementation-details.md) for task evidence and
repository conflict handling.

## Finish report

Report:

1. task ID and resulting status;
2. acceptance criteria addressed;
3. changed files;
4. tests added or updated;
5. checks run and results, plus checks not run;
6. limitations, blockers, and relevant unrelated issues;
7. verification selection, overrides, and gate outcomes;
8. final `$code-review` result and its evidence/status write boundary; and
9. next skill.

Use `$code-review` when approval is still pending, `$to-tasks` when task
decomposition is wrong, `$write-spec` for a specification problem, and
`$grill-workflow` when a product, domain, scope, or architecture decision is
required. If the final reviewer already approved the task, report `done` without
requesting redundant review. Do not mark the task `done` yourself or push.
Standalone invocation stops after this task; when composed by an authorized
`$auto-implement` batch, return the result to that parent for its next task.
