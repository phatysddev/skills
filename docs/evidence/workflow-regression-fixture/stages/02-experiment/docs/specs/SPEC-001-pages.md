# SPEC-001: Navigation pages
- Status: ready
- Requirement: [Pages](../requirement.md)
## UI contract
Baseline: b1
Acceptance: synthetic case input accepts b1 (not a production user approval).
Source: ../assets/prototype-baselines/pages/b1/
Inventory: [hashes](../assets/prototype-baselines/pages/b1/inventory.json)
Fidelity: faithful
| UI ID | Page/state | Required appearance | AC | Compare conditions | Allowed differences |
| --- | --- | --- | --- | --- | --- |
| UI-01 | page1-v1/default | two-column at desktop, stack on mobile; green secondary summary; shared type/color | AC-01 | 1280x900 and 390x844, Tuesday 10:00 | no prototype control bar |
| UI-02 | page2-v1/default | two-column at desktop, stack on mobile; green secondary summary; shared type/color | AC-02 | 1280x900 and 390x844, Tuesday 10:00 | no prototype control bar |
| UI-03 | page3-v1/default | two-column at desktop, stack on mobile; green secondary summary; shared type/color | AC-03 | 1280x900 and 390x844, Tuesday 10:00 | no prototype control bar |
| UI-04 | page4-v1/default | two-column at desktop, stack on mobile; green secondary summary; shared type/color | AC-04 | 1280x900 and 390x844, Tuesday 10:00 | no prototype control bar |
## Acceptance criteria
- AC-01: page1 retains the UI-01 composition and type/color treatment and working four-page navigation. Verify with rendered comparison plus link inspection.
- AC-02: page2 retains the UI-02 composition and type/color treatment and working four-page navigation. Verify with rendered comparison plus link inspection.
- AC-03: page3 retains the UI-03 composition and type/color treatment and working four-page navigation. Verify with rendered comparison plus link inspection.
- AC-04: page4 retains the UI-04 composition and type/color treatment and working four-page navigation. Verify with rendered comparison plus link inspection.
