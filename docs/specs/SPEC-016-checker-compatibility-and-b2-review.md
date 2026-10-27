# SPEC-016: Checker compatibility and completed b2 fixture review

- Status: ready
- Requirement: [Follow-up](../requirement.md#current-capability-checker-compatibility-and-b2-fixture-review)

## Contract

Fix the reported validator interoperability defects without changing agreement
ownership. Continue the existing controlled consumer fixture through b2
implementation and visual comparison. The user's current request authorizes
TASK-005's missing delta as well as the previously planned tasks; this is a new
explicit scope authorization, not silent expansion of the prior batch.

## Acceptance criteria

- AC-01: write-spec's default `- AC-01:` declaration, plain declarations and table rows validate; regression demonstrates pre-fix failure and post-fix pass.
- AC-02: every task has one source Spec link targeting its indexed owning spec; mismatched targets/explicit IDs, missing/duplicate links and remote targets fail. A generic label or local fragment may be valid.
- AC-03: the bounded static app implements accepted b2 shared colors across all four existing pages, preserving navigation/content/layout and b1 snapshots and historical TASK-004.
- AC-04: baseline and application are rendered and compared for all four default states at 1280×900 and 390×844 with Tuesday 10:00; capture evidence and a final consumer review assess UI-01–04 / fixture AC-01–04, without claiming untested behavior or general stability.

## Verification

Run artifact regression tests, fixture index/navigation/baseline commands, pack
and whitespace checks. Use actual browser viewport overrides and saved captures;
no simulated mobile CSS or source-only visual pass. Independent delegated final
review must inspect images and contract. Seeded acceptance/history and the static
nature of this app remain explicit limits.

## Delivery

[TASK-029](../tasks/TASK-029-checker-compatibility-and-b2-review.md).
