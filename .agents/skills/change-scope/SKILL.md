---
name: change-scope
description: "Assess and reconcile an agreed requirement change across an existing feature's requirement, spec, and task plan. Use when requested behavior changes after planning or implementation has started; not for ordinary implementation defects or a new unrelated feature."
---

# Change Scope

Keep an existing feature's authoritative contract and work plan consistent when
its intended behavior changes. Preserve completed work, evidence, and stable IDs.
Do not change production code, tests, runtime configuration, verification policy,
or the generated Codebase Context block.

## Establish the requested change

Read repository guidance, the user's requested change, the owning requirement
and full spec, linked tasks/dependencies, relevant ADRs and accepted design or
prototype decisions. Inspect current source/diff only to establish impact.
Use the repository's actual document paths and conventions.

Distinguish a changed agreement from a defect against an unchanged agreement.
A defect belongs to `$implement-task`, or `$debug-task` when its cause is unclear.
An unrelated feature belongs to `$write-spec` after its decisions are settled.
Do not edit the contract to make incorrect code pass review.

For an impact-only question, report the analysis without modifying documents.
When the user has instructed an unambiguous change, that instruction authorizes
its scoped document reconciliation; do not ask them to approve it again.
If material behavior is undecided, identify the exact decision and affected work.
Keep proposals separate from the accepted contract; recommend `$grill-workflow`
for product decisions or `$grill-design` for visual decisions. Do not repeatedly
return settled decisions to discovery.

## Map the impact before editing

Build a concise before/after map identifying:

- changed behavior and affected acceptance-criterion IDs;
- requirement/spec sections, task IDs, interfaces and dependencies affected;
- completed work and evidence that remain valid;
- work or evidence invalidated by the change;
- any actual migration, compatibility, or release implications.

Only include implications supported by the requested behavior and repository
facts. A missing optional document or old context SHA is not a scope blocker.

## Reconcile an agreed change

Update the authoritative requirement and its existing owning spec in place.
Keep unaffected criteria/IDs stable, allocate new IDs for new behavior, and note
superseded criteria without reusing their IDs for a different meaning. Preserve
traceability to the prior agreement and relevant accepted prototype/design.
An accepted prototype that still needs interpretation belongs to
`$spec-with-prototype`; do not invent its behavioral meaning here. A conflict
with an ADR needs an explicit superseding decision, not a silent ADR rewrite.

Use `$write-spec`'s quality contract when updating the spec. Keep it `draft`
while material decisions remain; use `ready` once the revised contract is
implementation-ready. A previously `done` spec with new work becomes `ready`,
not evidence that the new behavior has shipped.

Reconcile affected open tasks using `$to-tasks`'s task/coverage contract. Load
that skill when actual decomposition or dependency changes are needed, within
this authorized documentation scope; do not hand the user back to it for work
already completed here. Preserve task IDs, useful history, valid checked items,
and the `Goal` / `Blocked by` / `Todo` format. Create only missing work, with
acceptance coverage and an acyclic dependency graph. If the supporting skill is
unavailable, finish the contract/impact map and report the specific planning gap;
do not install it automatically or invent its rules.

Do not rewrite or reopen `done` tasks automatically. Preserve them as historical
deliveries and plan a linked follow-up for changed behavior. In open tasks,
annotate invalidated evidence and add unchecked re-verification work; do not
claim that old passes cover changed criteria. An affected `in_review` task must
leave review readiness (use `in_progress` for ready remaining work, or `blocked`
with a concrete unblock condition). Tasks whose entire goal is removed must not
remain runnable: use the repository's cancellation convention if one exists;
otherwise mark the open task `blocked` and record `Retired by scope change:` in
`Blocked by`, citing the accepted requirement/spec change and stating that no
work remains on this task. Remove obsolete scheduling edges from surviving
tasks. This is retirement evidence, not an unresolved external prerequisite.
Never mark removed work `done` as if tested.

## Handoff and validation

Verify every revised AC has task coverage or evidence still valid for that
exact behavior. Check links, dependency cycles, stale runnable work, task status,
and preservation of unrelated changes. The parent `change-scope` owns
invalidation of existing review readiness; composed `to-tasks` does not start
tasks or perform those transitions. No implementation/test/review runs occur
as part of this document reconciliation.

Report the applied change (or impact-only result), changed paths and IDs,
preserved deliveries, invalidated evidence, and any remaining decision.
Recommend at most one next action: the first ready `$implement-task`, a concrete
remaining planning/decision step, or no action if nothing remains. Use
`$auto-implement` only when the user explicitly requests a batch and identifies
its authorized scope. Newly created tasks are not added to an existing batch
without authorization. Stop after the report; do not start implementation.
