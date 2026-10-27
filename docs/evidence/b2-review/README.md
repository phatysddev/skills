# b2 consumer follow-up — 2026-10-27

This run follows the user's request to fix two checker defects and finish the
controlled fixture's b2 implementation through desktop/mobile consumer review.
It is a static four-page translation with real artifact and browser operations;
acceptance and historical statuses were seeded in the earlier evaluation.

## Checker defects and regression

Before the source fix, the expanded suite ran 22 tests and recorded eight failed
assertions: three bullet variants plus wrong Spec target, wrong ID, both wrong,
missing/duplicate metadata and remote link cases. The existing parser accepted
the wrong Spec links and rejected the default write-spec bullet format. After
the fix all 22 tests pass. The source now resolves the task's single Spec link
relative to the task and compares it with the indexed owner; a matching label
cannot hide a different target. Local fragments/generic labels remain valid.

## Implementation and current authorization

Changed only the existing app's shared colors from b1 green to accepted b2
purple. Navigation, layout, text and the historical page prototype markers stay
unchanged. The app HTML is a simple static consumer, not a framework migration.
The current request authorizes the missing TASK-005 delta as well as TASK-001–003;
it does not retroactively add that task to the original batch.

[Preserved hashes](preserved-input-hashes.json) cover both immutable baseline
trees and historical done TASK-004. [Before app](before-app-b1/page1.html) retains
the earlier implementation, making the actual b1→b2 delta reviewable. Historical
batch-report.json and original regression report remain evidence of the prior
blocked run; this follow-up does not overwrite those results.

## Actual render and navigation evidence

The parent used the app-browser's documented viewport override, not an iframe
or simulated media query, and captured all four baseline/application pairs at
1280×900 and 390×844 with Tuesday 10:00. Sixteen original captures and
[DOM-backed layout observations](render-observations.json) are retained here.
Temporary viewport overrides were reset and the created tab was closed.

[Desktop comparison](desktop-comparison.jpg) and
[mobile comparison](mobile-comparison.jpg) arrange baseline above application,
page 1–4 left to right. Desktop thumbnails are reduced to 640×450 for the sheet;
original captures retain the full specified dimensions. Mobile originals are
390×844. The eight pairs have equal rendered geometry/type/colors and equal
decoded pixels for these exact captured states. This equality supplements
human/agent visual inspection; it does not prove behavior outside those states.

Observed: desktop keeps content and summary in two columns; mobile stacks the
summary below content; navigation and text fit with no horizontal overflow;
purple summary and text colors match baseline throughout. The parent's actual
browser clicks covered all 4×4 source/target combinations at both viewports:
[32 transitions](navigation-observations.json). All expected URL/heading checks
passed. The placeholder Continue button has no specified journey and is not
claimed as a working booking operation.

Replay the saved-observation integrity checks from the skill-pack root:

```text
python3 docs/evidence/b2-review/check_observations.py
```

The script is read-only and verifies eight exact metric pairs, capture hashes,
viewport/layout/color assertions, navigation observation completeness and
preserved-input hashes. [Results](comparison-results.json) and
[decoded-pixel comparison](pixel-comparisons.json) are supplementary evidence.
Image sheets/pixel comparison used bundled Pillow with no dependency install.

## Verification and final review

Required delegated unit verification: passed, 22 tests. Required delegated
integration verification: passed, same 22 tests plus actual artifact index,
static navigation/baseline checks and saved-observation integrity checks. These
are shared assertions, not 44 distinct unit tests. Independent required browser journey verification also passed: a separate agent
clicked all four destinations at both viewports (8 checks), asserting current
URL/h1, exact viewport, purple summary, no horizontal overflow, desktop columns
and mobile stacking. This is an independent subset of the parent’s 32 checks.
Final canonical TASK-029 review approved after inspecting all four desktop/mobile
pairs and full-size samples. No findings; both checker fixes and the scoped b2
consumer visual contract passed. Separate final consumer reviews approved TASK-001, TASK-002, TASK-003 and
TASK-005; each reviewer viewed its original desktop/mobile baseline/app captures
and recorded actual b2 review evidence before marking that task done. No findings.
Historical TASK-004 remains unchanged as the b1 delivery. These reviews inspect
saved captures/source/observations; the independent fresh browser replay is the
e2e result above, not a claimed additional replay by every reviewer.

## Limits

One controlled case, four static pages/default states, two viewports, one host
and one browser. It does not establish frontend/backend framework runner
resolution, genuine no-delegation-host behavior, arbitrary app or interactive
state fidelity, production acceptance, or a general workflow success rate.
The previous Chrome headless exit 134 remains historical evidence; this run
used the working app-browser instead.

Final state: TASK-001/002/003/005 done for current b2; TASK-004 done as preserved
b1 history. The derived artifact index was synchronized to the actual source
statuses after review. Temporary browser viewports were reset, temporary tabs
closed and the fixture-only localhost server stopped. No commit or push.
