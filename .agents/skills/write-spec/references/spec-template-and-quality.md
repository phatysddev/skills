# To Spec reference: template and quality

Read this reference when creating or updating a specification. It contains the full spec template, acceptance-criteria rules, verification mapping, traceability, and status gate.

## Contents

- [Required spec content](#required-spec-content)
- [Acceptance criteria](#acceptance-criteria)
- [Verification plan](#verification-plan)
- [Open questions](#open-questions)
- [Traceability](#traceability)
- [Status](#status)

## Required spec content

Use this structure as the default.

Adapt headings only when the repository already has an established spec format.

```markdown
# SPEC-###: <feature>

- Status: draft | ready
- Requirement: [relative link]
- Context: [relative link]
- ADRs: [relative links or None]

## Problem and outcome

Describe the specific problem this feature addresses and the observable outcome it must create.

Do not restate the entire project background.

## In scope

List behavior this spec owns.

## Out of scope

Explicitly identify nearby behavior that this spec does not own when ambiguity is likely.

## User flow and behavior

Describe the primary flow and meaningful alternate flows from the user's or calling system's perspective.

## Business rules and constraints

Record feature-specific rules and constraints.

Link to project-level sources instead of duplicating global rules.

## Data and permissions

Describe relevant domain data, ownership, visibility, authorization, and state transitions.

Do not design implementation-specific schemas unless the schema itself is part of an agreed contract.

## Errors and edge cases

Describe important failure behavior, invalid states, conflicts, retries, unavailable dependencies, and edge conditions.

Include only cases that materially affect the contract.

## Interfaces and observable test points

Describe externally or behaviorally meaningful contracts such as:

- UI states;
- API routes;
- request/response behavior;
- events;
- public functions;
- callbacks;
- redirects;
- notifications;
- state transitions.

Do not enumerate internal functions merely to make the section look complete.

## Non-functional requirements

Include only requirements relevant to this feature.

Possible areas include:

- accessibility;
- performance;
- security;
- privacy;
- reliability;
- SEO;
- observability;
- operational constraints.

Do not manufacture numeric targets that have not been agreed.

## Acceptance criteria

- AC-01: Given ..., when ..., then ...
- AC-02: Given ..., when ..., then ...

## Verification plan

| AC | Verification |
| --- | --- |
| AC-01 | <test or observable verification approach> |
| AC-02 | <test or observable verification approach> |

## Open questions

List unresolved questions.

Mark whether each question is blocking or non-blocking.
```

## Acceptance criteria

Acceptance criteria define observable completion.

Each acceptance criterion must:

* have a unique `AC-##` ID;
* describe one independently referenceable behavior or outcome;
* be testable or otherwise objectively verifiable;
* avoid implementation-task language;
* include relevant failure or authorization behavior;
* be specific enough that `$to-tasks` can reference it later.

Prefer Given / When / Then when it improves precision.

For example:

```text
AC-01: Given an available appointment slot,
when a customer confirms a valid booking,
then the booking is created and the slot is no longer available
to another customer.
```

Avoid criteria such as:

```text
AC-01: Build the booking API.
```

That is an implementation task, not an acceptance criterion.

Also avoid vague criteria such as:

```text
AC-02: Booking should work correctly.
```

## Verification plan

Every acceptance criterion must map to at least one reasonable verification approach.

Verification may include:

* unit tests;
* integration tests;
* end-to-end tests;
* API contract tests;
* authorization tests;
* UI interaction tests;
* responsive checks;
* accessibility checks;
* manual verification when automation is not justified.

Describe the verification target, not detailed test implementation.

A spec cannot be `ready` if a material acceptance criterion has no credible verification approach.

## Traceability

Maintain traceability in both directions:

```text
requirement / context / ADR
            ↓
           spec
            ↓
      acceptance criteria
            ↓
      verification points
            ↓
          to-tasks
```

Each important behavior in the spec should be supported by an agreed requirement, domain rule, or architecture decision.

Do not add hidden scope merely because it appears technically useful.

If the spec introduces behavior that cannot be traced to an agreed source, either:

1. remove it; or
2. mark it as an open question and route it to `$grill-workflow`.

## Status

Use only:

```text
draft
ready
done
```

### `draft`

Use `draft` when any material product, domain, architecture, or acceptance decision remains unresolved.

A draft spec may still contain useful completed sections.

Clearly identify blocking open questions.

Do not route a draft spec to `$to-tasks` as if implementation can safely begin.

### `ready`

Mark a spec `ready` only when:

* scope is sufficiently stable;
* material behavior is defined;
* relevant business rules are defined;
* permissions and failure behavior are defined where applicable;
* every acceptance criterion is observable and independently referenceable;
* every acceptance criterion has a verification approach;
* all blocking questions are resolved;
* remaining open questions are explicitly non-blocking;
* no hidden implementation assumptions are required to understand the intended behavior.

`ready` means ready for task decomposition, not approved implementation.

An existing `ready` spec may still enter the optional prototype flow when the
user requests visual validation. After the prototype is accepted, use
`$spec-with-prototype` to update the same owning spec before returning to
`$to-tasks`.

### `done`

Use `done` when the feature's accepted behavior has been implemented, reviewed,
and the linked implementation tasks are complete. Keep the specification as a
historical source of truth; later changes create or update the owning spec
through the normal workflow rather than rewriting delivery evidence.
