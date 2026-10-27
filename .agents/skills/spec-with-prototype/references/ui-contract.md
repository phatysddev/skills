# Accepted prototype: UI contract and revision reconciliation

Read this for every prototype-backed spec. The spec owns the contract; its
accepted baseline supplies the concrete visual reference. Prototype existence
or an exploratory edit alone is not acceptance. Explicit instructions such as
"use this version", "implement this prototype" or "replace the old design
with this revision" are acceptance of that named surface; do not ask again.
Acceptance of appearance does not confirm unrelated speculative business rules.

## Preserve a reproducible baseline

Before marking the spec ready, bind each accepted page to recoverable content,
not just a revision ID plus a mutable live path. Use either an immutable Git
commit with all required files recoverable at that commit, or a self-contained
snapshot under `docs/assets/prototype-baselines/<feature>/<baseline-id>/`.
Prefer a snapshot when the accepted content is uncommitted or no Git exists.
Include the relevant HTML, shared CSS/JS, fonts/images and required local assets
with working relative references; record external asset URLs/versions and
unavailable resources. A screenshot alone cannot reproduce interaction states.
Do not create a commit solely to establish this reference without authorization.

Record an inventory with file paths and content hashes (for example SHA-256),
page revision IDs, acceptance basis, and capture conditions. Existing project
design artifact conventions may serve the same purpose. Keep snapshots outside
the live prototype tree; do not recursively copy baseline archives. Capture
the complete shared dependency set so a later CSS change cannot alter an older
baseline. Never overwrite an accepted baseline; create a new baseline ID.
If old content was already lost, report it as unavailable, recover from actual
history when possible, or obtain an explicitly selected replacement. Do not
label the latest live files as an older accepted revision.

## Spec UI contract

Add one scoped `UI contract` section to the owning spec, for example:

```markdown
## UI contract

Baseline: booking-ui-02
Acceptance: user selected booking-v3 in the current request
Source: docs/assets/prototype-baselines/booking/booking-ui-02/
Inventory: <relative link to file/hash inventory>
Fidelity: faithful (default for an accepted prototype)

| UI ID | Page/state | Baseline reference | Required appearance/interaction | AC | Compare conditions | Allowed differences |
| --- | --- | --- | --- | --- | --- | --- |
| UI-01 | booking-v3/default | booking.html + style.css | two-column form/summary at desktop, stacked on mobile; summary is secondary; same type/color/component treatment | AC-07 | 1440x900 and 390x844, same sample booking | prototype control bar omitted; real input semantics |
```

Use stable UI IDs within the spec. Record observable composition, content
hierarchy/density, control placement, typography roles, spacing rhythm, color
and component treatment, imagery and responsive layout represented by the
accepted surface. Link concrete tokens/assets instead of transcribing every
CSS property. Include important empty/loading/error/selected/expanded states
and interactions. State the expected viewport, route, sample data and state;
do not invent unobserved mobile layouts or prototype states as accepted facts.
Specify required missing states through the normal requirements process.

Faithful means the implementation is recognizably the accepted design under
comparable conditions, including visual treatment, not merely the same fields
and buttons. Framework choice is not permission to replace it with generic
components. Allow changes for real data, accessibility and responsive behavior
only while retaining the agreed design; record material exceptions and their
basis. User-requested exact dimensions/tokens remain required. A behavior-only
or deliberately loose interpretation must be explicitly chosen, not inferred.
Do not demand universal pixel identity or a screenshot-difference percentage.

Create observable visual ACs linked to UI IDs, e.g. "At the recorded desktop
and mobile widths, booking preserves the baseline's form/summary arrangement,
content hierarchy and type/color treatment, except listed differences."
Keep functional ACs separate. Do not use "match prototype exactly" as the
entire criterion. Visual acceptance must survive task decomposition.

## Existing plan or implementation

Before updating a baseline/contract, inspect linked tasks and current delivery.
With no tasks, reconcile directly here and hand off to `to-tasks`. Once tasks
exist, an accepted visual-only change is also a contract change: use
`change-scope` as document owner to reconcile baseline, UI/AC IDs, affected task
checklists, dependencies and evidence together. Do not update only the spec
and leave the task plan apparently current. When invoked by `change-scope`,
perform this interpretation/snapshot/spec work and return the delta to it;
do not route back recursively or create tasks from this skill.

The delta records old/new baseline and page IDs, changed shared dependencies,
affected UI/AC IDs and tasks, preserved behavior, invalidated visual/functional
evidence, and any actual unresolved choice. Distinguish redesign from drift:
production that violates an unchanged accepted UI contract needs an
implementation fix, not a scope change that blesses the mismatch.

## Verification evidence

For each UI AC, plan a rendered comparison of baseline and implementation at
the same viewport, representative content and interaction state. Record actual
captures/paths, inspected conditions, differences and allowed exceptions in
the task Todo evidence. Compare structure and visual treatment before details;
check responsive changes and affected shared components across pages. Source
inspection alone cannot establish visual fidelity; functional tests cannot
establish appearance. If rendering is unavailable, say unverified and record
the concrete unblock condition for a required visual AC. Do not mark it passed
or silently turn visual verification off. This is acceptance evidence under
existing verification policy, not a new global capability or review stage.
