# Spec With Prototype reference: reconciliation rules

Read this reference when translating accepted prototype evidence into a behavioral specification. It contains classification, state, acceptance, visual-fidelity, reconciliation, and verification rules.

## Contents

- [Classify prototype information](#classify-prototype-information)
- [What belongs in the spec](#what-belongs-in-the-spec)
- [Prototype references in the spec](#prototype-references-in-the-spec)
- [UI states](#ui-states)
- [Acceptance criteria](#acceptance-criteria)
- [Visual fidelity](#visual-fidelity)
- [Existing spec reconciliation](#existing-spec-reconciliation)
- [Verification plan](#verification-plan)

## Classify prototype information

For each meaningful prototype behavior or state, classify it as one of:

### Requirement-backed

Directly supported by an agreed requirement, domain rule, or ADR.

Safe to reflect in the spec.

### Prototype-confirmed

A UI/UX behavior explicitly accepted by the user during prototype review.

Becomes part of the applicable behavioral or visual UI contract.

### Visual-only

Examples:

* spacing;
* decorative color;
* border radius;
* non-contractual typography;
* decorative imagery.

For an accepted prototype these belong in the scoped UI contract by baseline
reference, with observable visual ACs; do not discard its appearance merely
because business behavior is unchanged. See [UI contract](ui-contract.md).
If an exact visual choice is an
Agreed constraint in UI Design Requirements, preserve it by reference and map
it to appropriate verification as `$write-spec` does. Do not discard a required
visual constraint merely because the prototype represents it as color or spacing.
Preferences and proposals outside the accepted surface remain non-mandatory.
Once the user selects a rendered design, that accepted appearance is captured
as a contract even if its individual choices were originally delegated.

### Prototype proposal

A speculative idea shown for exploration but not explicitly agreed.

Do not place it into the spec as required behavior.

### Conflict

Prototype behavior conflicts with an authoritative requirement, domain rule, ADR, or existing agreed behavior.

Do not silently resolve the conflict.

Route to:

```text
$grill-workflow
```

or `$write-spec` as appropriate.

## What belongs in the spec

Translate prototype evidence into implementation-relevant behavior such as:

* page/view existence;
* navigation behavior;
* primary user flow;
* required content states;
* form behavior;
* validation states;
* empty states;
* loading states;
* error states;
* confirmation states;
* role-dependent UI;
* enabled/disabled states;
* responsive behavioral requirements when material;
* interaction rules;
* observable transitions.

Do not specify visual implementation detail unless it is genuinely required.

For example, prefer:

```text
On mobile, primary navigation must remain accessible without
overflowing the viewport.
```

over:

```text
Use a 24px hamburger button positioned 18px from the right edge.
```

unless that exact design is explicitly required.

## Prototype references in the spec

Add a section such as:

```markdown
## Prototype references

- `home-v3` — `docs/assets/prototype/index.html`
- `booking-v2` — `docs/assets/prototype/booking.html`
```

Prototype IDs alone are insufficient: link the immutable baseline inventory
and UI contract with visual ACs as described in [UI contract](ui-contract.md).

## UI states

When important UI states exist in the prototype, make them explicit.

Example:

```markdown
## UI states

### Booking form

- default
- validation error
- unavailable slot
- submitting
- success
```

Only include states that matter to behavior or verification.

## Acceptance criteria

Acceptance criteria cover observable functional behavior and accepted visual
fidelity. Give each kind a concrete verification method.

Use the prototype to make ACs more concrete.

Example:

```text
AC-04:
Given a selected time slot becomes unavailable before submission,
when the customer submits the booking,
then the booking is not created and the booking view presents
an unavailable-slot state without losing the customer's entered details.
```

Do not create ACs such as:

```text
AC-05: Match prototype exactly.
```

or:

```text
AC-06: Use the same CSS as booking-v2.
```

The prototype is evidence, not the acceptance criterion itself.

## Visual fidelity

Unless explicitly stated otherwise, implementation should preserve:

* information hierarchy;
* primary interaction flow;
* important UI states;
* navigation structure;
* meaningful control placement.

Faithful appearance is the default for an accepted prototype: retain its
layout, typography roles, spacing, color and component treatment via the UI
contract. This does not require universal pixel-perfect reproduction, but it
also does not allow an unrelated redesign merely because behavior matches.

Production implementation may adapt details, with recorded reasons while
preserving the agreed design, to:

* framework conventions;
* accessibility;
* responsive behavior;
* real data;
* technical constraints.

Material deviations from agreed behavior must return to the spec rather than being decided silently during implementation.

## Existing spec reconciliation

When updating an existing spec, compare:

```text
existing behavioral contract
vs
accepted prototype
```

Do not blindly rewrite the spec to match the prototype.

For each difference determine:

```text
prototype clarifies existing requirement
→ update spec

prototype adds explicitly confirmed behavior
→ update spec

prototype changes accepted appearance only
→ update UI contract/visual ACs; reconcile existing tasks through change-scope

prototype proposal is not confirmed
→ leave out

prototype conflicts with agreed behavior
→ resolve before continuing
```

Preserve existing AC IDs when their meaning has not changed.

Add new AC IDs only when new agreed behavior requires them.

Do not renumber existing acceptance criteria merely for neatness.

## Verification plan

Map behavioral UI criteria to suitable verification such as:

* interaction test;
* component/integration test;
* end-to-end test;
* responsive check;
* accessibility check;
* manual visual review where appropriate.

Do not use:

```text
Looks like prototype
```

as the only verification for functional behavior.
