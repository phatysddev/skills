# SPEC-015: Agreement synchronization and portable verification

- Status: ready
- Requirement: [Current capability](../requirement.md#current-capability-agreement-synchronization-and-portable-verification)

## Contract and acceptance

| ID | Observable behavior | Verification |
| --- | --- | --- |
| AC-01 | Discovery/setup preserve active agreements when specs exist and hand pending confirmed changes to change-scope; reconciliation is resumable and idempotent across mixed task states. | Executed fixture and source review. |
| AC-02 | Setup routes discovery only for material knowledge gaps and accepts explicit policy answers once. | Focused source review. |
| AC-03 | Distinct package runners execute as an ordered set with individual evidence; unresolved alternatives remain ambiguous. | Fixture commands and contract review. |
| AC-04 | Host capabilities and required unavailable gates are disclosed before policy choice; no inline fallback appears. | Fixture unavailable-render result and contract review. |
| AC-05 | Checkout relocation preserves commit permission only after project identity and relative boundary verification. | Git fixture evidence and source review. |
| AC-06 | Read-only artifact checking detects coverage gaps, cycles, missing/stale agreements, source-index drift and baseline tampering. | Standard-library regression suite. |

The checker uses an optional derived index with documented formatting limits;
it cannot establish semantic coverage or rendered fidelity. Behavioral evidence
is a bounded fixture run, not a measured production success rate.

## Delivery

[TASK-028](../tasks/TASK-028-agreement-synchronization.md). Historical SPEC-014
and TASK-027 remain unchanged; their original walkthrough evidence is not
retroactively upgraded to a behavioral evaluation.
