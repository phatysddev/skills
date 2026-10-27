# SPEC-014: Prototype fidelity and revision reconciliation

- Status: done
- Requirement: [Requirement](../requirement.md#current-capability-prototype-fidelity-and-revision-reconciliation)
- Context: [Context](../../CONTEXT.md#current-capability-prototype-fidelity-and-revision-reconciliation)

## Problem and outcome

The user reports production output diverging from an accepted prototype and
poor scope reconciliation when editing prototypes after task implementation
starts. Existing guidance strips most appearance as visual-only, excludes
pixel differences from review, and identifies revisions through overwritten
live paths. Preserve an executable visual agreement and coordinate revisions
through the complete existing plan.

## Contract

- Accepted prototypes default to faithful visual treatment in a spec UI
  contract, not behavior-only interpretation. Record stable UI IDs, observable
  visual ACs, exact baseline, acceptance basis, conditions and exceptions.
- Preserve recoverable HTML/CSS/JS/assets at an immutable Git revision or a
  separate self-contained baseline snapshot with file/hash inventory. Missing
  old content is a gap, never a guessed historical baseline.
- Tasks carry UI/AC/baseline references and rendered-comparison Todo work.
  Implementation translates the accepted design, and final review checks
  visual criteria with actual evidence under comparable conditions. Missing
  required visual evidence cannot be represented as passed.
- Editing a referenced prototype preserves the old accepted source and reports
  shared-dependency/downstream impact. Experiments do not change acceptance.
- Accepted replacements after tasks exist use change-scope as document owner,
  composing spec-with-prototype and to-tasks without recursive routing or
  stopping at a partial spec update. Visual-only deltas count. Preserve IDs and
  unaffected evidence, update open tasks, invalidate affected review readiness,
  and link missing delta work to done deliveries rather than rewriting history.
- Active batches re-preflight affected work; new members require authorization.
  Drift against an unchanged contract is an implementation defect.

No new skill identifier, global verification mode, automatic deployment,
universal pixel-difference threshold, automatic prototype acceptance or implied
business-rule approval. Existing parent/status/write/test/commit boundaries
remain in effect. This task changes reusable instructions, not a consumer app.

## Acceptance and verification

| ID | Observable behavior | Verification |
| --- | --- | --- |
| AC-01 | Accepted layout and visual treatment survive spec/task decomposition through stable UI/visual AC mapping and immutable assets. | Inspect spec/reference, task mapping, implementation and review handoff. |
| AC-02 | Visual drift is not excused by behavior passing; required missing render evidence remains unverified. | Walk through generic-restyle, allowed-accessibility and unavailable-render cases. |
| AC-03 | Editing shared CSS preserves older baselines and reports every affected consumer; experiments do not advance acceptance. | Revision/shared-file and lost-history scenarios. |
| AC-04 | Accepted replacement with todo/in_progress/in_review/done tasks reconciles contract and task coverage in one operation with correct historical/evidence treatment. | Mixed-status change scenario, repeat/idempotency and batch-scope walkthrough. |
| AC-05 | Router/docs and existing skill contracts remain coherent without recursive handoffs or new IDs. | Pack checker, frontmatter/link review and focused diff review. |

## Delivery

Owned by [TASK-027](../tasks/TASK-027-prototype-fidelity-and-reconciliation.md).
Source walkthroughs establish instruction coverage, not observed model fidelity
or a guarantee of production visual quality. No consumer application was supplied.
