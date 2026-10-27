# SPEC-001: Navigation pages
- Status: ready
- Agreement: b2
- Requirement: [Pages](../requirement.md)
## UI contract
Baseline: b2
Acceptance: synthetic case input accepts b2 (not a production user approval).
Source: ../assets/prototype-baselines/pages/b2/
Inventory: [hashes](../assets/prototype-baselines/pages/b2/inventory.json)
Fidelity: faithful
| UI ID | Page/state | Required appearance | AC | Compare conditions | Allowed differences |
| --- | --- | --- | --- | --- | --- |
| UI-01 | page1-v2/default | two-column at desktop, stack on mobile; purple secondary summary; shared type/color | AC-01 | 1280x900 and 390x844, Tuesday 10:00 | no prototype control bar |
| UI-02 | page2-v2/default | two-column at desktop, stack on mobile; purple secondary summary; shared type/color | AC-02 | 1280x900 and 390x844, Tuesday 10:00 | no prototype control bar |
| UI-03 | page3-v2/default | two-column at desktop, stack on mobile; purple secondary summary; shared type/color | AC-03 | 1280x900 and 390x844, Tuesday 10:00 | no prototype control bar |
| UI-04 | page4-v2/default | two-column at desktop, stack on mobile; purple secondary summary; shared type/color | AC-04 | 1280x900 and 390x844, Tuesday 10:00 | no prototype control bar |
## Acceptance criteria
AC-01: page1 retains the UI-01 composition and type/color treatment and working four-page navigation. Verify with rendered comparison plus link inspection.
AC-02: page2 retains the UI-02 composition and type/color treatment and working four-page navigation. Verify with rendered comparison plus link inspection.
AC-03: page3 retains the UI-03 composition and type/color treatment and working four-page navigation. Verify with rendered comparison plus link inspection.
AC-04: page4 retains the UI-04 composition and type/color treatment and working four-page navigation. Verify with rendered comparison plus link inspection.

## Change record CHG-001
Synthetic acceptance selects b2, replacing b1. Shared style.css changed text
and summary colors on all four page consumers (UI-01–UI-04, AC-01–AC-04).
No behavior change or migration. TASK-001 todo and TASK-002 in_progress update
in place. TASK-003 leaves in_review for in_progress and its historical b1 visual
evidence is superseded. TASK-004 stays done as history; TASK-005 owns only the
missing b2 delta for page4. Old snapshots and deliveries remain preserved.
Synchronization: complete for documents; implementation and visual review pending.
