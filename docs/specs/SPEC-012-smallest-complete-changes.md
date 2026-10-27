# SPEC-012: Smallest complete changes

- Status: done
- Requirement: [Requirement](../requirement.md#current-capability-smallest-complete-changes)
- Context: [Context](../../CONTEXT.md#current-capability-smallest-complete-changes)

## Problem and outcome

Bring the useful core of DietrichGebert/ponytail into Phat's existing
implementation and review skills. Reduce unnecessary code and dependencies
while completing the agreed task and retaining its verification contract.

## Scope

Adapt the core `ponytail` skill into `implement-task` and `code-review`.
Trace consumers before changing shared seams; reuse existing project code,
platform features and installed dependencies before introducing new machinery.
Preserve readability, validation, failure handling, security, accessibility,
compatibility and agreed behavior. Smaller behavior proposals use scope change.

Keep all 23 identifiers and existing verification/review authority. Do not
import upstream session persistence, persona/levels, fixed response suffix,
test mandates, install hooks or the other audit/debt/gain skills. Retain pinned
provenance and the MIT notice in each adapted installable skill.

## Acceptance and verification

| ID | Observable behavior | Verification |
| --- | --- | --- |
| AC-01 | Implementation traces affected consumers and selects a complete readable change using existing seams before new dependencies. | Source inspection and shared-interface scenario. |
| AC-02 | Required behavior and protections survive simplification; proposed scope reductions do not silently change the contract or verification policy. | Scope and shortcut scenarios. |
| AC-03 | Review reports concrete completeness/maintenance risks without line-count or style gates, production fixes or extra audits. | Review-boundary scenario. |
| AC-04 | Both installable skills retain pinned attribution/license; docs and 23-skill catalog stay coherent. | Pack checker, skill validation and diff review. |

## Delivery

Owned by [TASK-025](../tasks/TASK-025-smallest-complete-changes.md).
This is an instruction/documentation change; no runtime or dependency added.
Commit policy: disabled unless explicitly authorized.
