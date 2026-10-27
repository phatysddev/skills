# TASK-029: Fix checker compatibility and complete b2 fixture review

- Status: done
- Spec: [SPEC-016](../specs/SPEC-016-checker-compatibility-and-b2-review.md)

## Goal

Fix bullet AC parsing and task/source Spec identity validation, then finish the
bounded b2 app and desktop/mobile consumer review. Preserve historical evidence.

## Blocked by

None. App-browser viewport control is available for rendered comparisons.

## Todo

- [x] Reproduce both checker defects before fixing; tests also reject mismatched label/target and missing/duplicate/remote Spec metadata (AC-01–02).
- [x] Implement fixes and run 22 passing checker tests (AC-01–02).
- [x] Apply b2 shared CSS across the fixture app and preserve b1/history (AC-03).
- [x] Capture all four pages at desktop/mobile sizes and verify navigation/rendered layout (AC-04).
- [x] Required unit passed (22 tests); required integration passed (22 shared tests plus fixture index/navigation/baseline/saved-observation checks). Required e2e passed via independent app-browser run: all 4 destinations × 2 viewports, actual viewport/colors/layout/no-overflow assertions. No verification sub-agent writes.
- [x] [Render evidence](../evidence/b2-review/README.md): 16 captures, 8 identical metric/pixel pairs, parent 32 navigation transitions; preserved-input hashes prove b1/b2 snapshots and historical TASK-004 unchanged. Seeded history/acceptance and static-default-state limits remain explicit.
- [x] Final canonical consumer/code review approved — TASK-029 working tree against HEAD (tracked task-owned diff plus new SPEC-016/task/b2-review artifacts); no findings. AC-01–02 verified by parser/link diff inspection and independently rerun 22 passing regressions. AC-03 verified by focused shared-color diff, retained before-app snapshot and preserved-input hashes. AC-04 / consumer UI-01–04 and AC-01–04 passed scoped final visual review: inspected all four baseline/application desktop and mobile pairs in comparison sheets plus full-size Booking desktop and Account mobile captures; content hierarchy, two-column desktop / stacked mobile, shared purple treatment, typography/spacing and navigation presentation match the accepted b2 contract. Independently reran pack checker, fixture artifact index, saved-observation integrity checker and git diff --check; all passed. Supplied terminal required unit/integration/e2e reports are credible: 22 shared rule/filesystem tests, fixture checks, independent eight-destination browser replay and parent 32-transition matrix. Original pre-fix red run and HTML 28-test result are previously recorded evidence, not rerun here. Limits remain one controlled static default-state fixture, two viewports and one browser/host with seeded acceptance/history; no claim for real frontend/backend runner discovery, genuine unavailable-delegation host, booking-button behavior, production acceptance or general workflow reliability. Reviewer changed only this task evidence/status; consumer task metadata remains separately review-owned. No commit/push.
- [x] Leave focused diff uncommitted under AGENTS.md; do not push.
