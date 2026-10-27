# Controlled agent workflow execution — 2026-10-27

This is one agent-executed controlled fixture, not a measured success rate or a
production visual-fidelity benchmark. The fixture driver supplies synthetic
acceptance and historical task statuses; no production user approved this UI.
The agent read the current prototype, change-scope, decomposition and batch
contracts and produced actual consumer files, inspected impact, reconciled them
and ran the checks below. Reconciliation was performed as a document operation;
the pack does not contain an automated reconciliation implementation.

## Reviewable artifacts

The [fixture](workflow-regression-fixture/AGENTS.md) contains the final consumer
project, [initial plan](workflow-regression-fixture/stages/01-planned/docs/specs/SPEC-001-pages.md),
[experiment stage](workflow-regression-fixture/stages/02-experiment/docs/specs/SPEC-001-pages.md),
[reconciled stage](workflow-regression-fixture/stages/03-reconciled/docs/specs/SPEC-001-pages.md),
[batch decision report](workflow-regression-fixture/batch-report.json),
[index](workflow-regression-fixture/artifact-index.json), prototype snapshots and
initial production translation under `app/`. Intermediate stages precede audit
metadata normalization and are historical fixtures, not separate active plans.

## Observed execution

1. Created four navigable prototype pages with one shared stylesheet and
   self-contained b1 snapshot/hash inventory. Derived one spec with four stable
   UI/AC pairs and mixed-status tasks: todo, in_progress, in_review, done.
2. Translated the accepted b1 pages into a bounded static consumer `app/`.
   Relative navigation targets exist. The translation establishes a concrete
   implementation input for comparison; source equality is not visual review.
3. Before editing shared CSS, retained b1 outside the live tree. Changed text
   and summary colors to purple in b2, bumped all four visibly affected page
   IDs, retained both inventories and found all four stylesheet consumers.
   During the experiment stage, the contract remained b1 and tasks were untouched.
4. Applied the synthetic explicit replacement selection through change-scope:
   updated requirement/spec to b2, kept UI/AC IDs, updated TASK-001/002 in place,
   changed TASK-003 from in_review to in_progress, labeled its b1 visual evidence
   superseded and added unchecked b2 verification. Preserved done TASK-004 and
   created exactly one missing visual delta TASK-005 linked to that delivery.
5. Re-read reconciliation record, task coverage and existing follow-up. A
   second pass required no writes. Compared document SHA-256 maps before/after:
   identical; task count stayed five. TASK-004 was byte-identical to its seeded
   initial delivery at this point. Later artifact-index preparation added only
   `Agreement: b1` metadata to that task; its historical body/status stayed intact.
6. Recorded interruption of original batch TASK-001–004 when b2 was accepted
   before task synchronization. Resume preflight read current b2 work, retained
   TASK-004 done and excluded TASK-005 from batch membership pending explicit
   authorization. The required visual/review gap stops implementation on resume;
   no b2 production change or review completion was asserted.

## Executed verification

From the skill-pack root:

```text
python3 .agents/skills/to-tasks/scripts/check_project_artifacts.py docs/evidence/workflow-regression-fixture/artifact-index.json --root docs/evidence/workflow-regression-fixture
Artifact index checks passed; semantic coverage and rendered fidelity require review.

python3 docs/evidence/workflow-regression-fixture/checks/check_navigation.py
navigation: 4 pages x 4 targets passed

python3 docs/evidence/workflow-regression-fixture/checks/check_baselines.py
baseline inventory: b1 and b2 passed
```

The two ordered commands have distinct necessary scopes: navigation and retained
baseline dependencies. Both exited 0; neither result substitutes for the other
or for visual verification. Their repository evidence is the fixture RUNNERS.md.
This exercises a runner set as two concrete commands but does not benchmark
frontend/backend framework discovery or a delegated test capability invocation.

A real local renderer probe attempted Google Chrome's installed executable with
`--headless --disable-gpu --no-first-run`, an isolated temporary user-data-dir,
`--screenshot`, `--window-size=1280,900`, and the b1 application file URL. It
exited 134 and produced no screenshot. No browser/rendering dependency was
installed or permission bypass attempted. The initial headless desktop/mobile comparison attempt was **unverified**; see
the subsequent app-browser observation below. A final visual pass or done status
for changed work is not claimed. A working approved renderer with captures of baseline/application
at both recorded viewports is the concrete unblock condition.

The unavailable-delegation case is a controlled input profile recorded in the
batch report, not a claim that this actual host lacks delegation. Under required
review it returns blocked with no inline fallback. This run itself was delegated
by the parent agent and did not dispatch a final production reviewer. Required
verification and rendering gaps therefore remain visible instead of becoming
successful evidence.

## Limits

This demonstrates real artifact-producing reconciliation and repeat/resume
behavior for one controlled case. It does not prove complete model adherence,
visual quality, completed post-change implementation, or the full
prototype-to-final-visual-review success path. Rendering failed; that path remains
incomplete and must be rerun with working renderer/reviewer infrastructure.

## Subsequent parent browser observation

The parent served only this synthetic fixture on 127.0.0.1 and used the app's
browser after the direct Chrome probe failed. The b1 Home application and b1
baseline rendered at the same 1280×720 viewport. Inspection found matching
navigation, two-column content/summary placement, type, colors and spacing in
this one state. Saved evidence: [application](app-b1-desktop.jpg) and
[baseline](baseline-b1-desktop.jpg). This is a narrow observed desktop comparison;
mobile, the other pages, b2 implementation and final delegated visual review
remain unverified. The unavailable-render case above remains a real failed
probe, but does not imply every renderer on this host is unavailable.
