# Design system reuse

Use for an explicit request to document an incumbent visual system, extract
tokens/components, or reconcile local drift. These operations do not authorize
site-wide migration, product changes, or creation of a new brand.

## Discover and distinguish

Find existing tokens, shared UI, component examples, design documentation and
the requested consumers. Read representative actual implementations and all
supported states/themes relevant to the request. A missing DESIGN.md does not
erase a coherent system. Confirmed rules remain authoritative; code-derived
values are observations, not automatically user-approved brand decisions.

Separate a missing semantic token, an implementation using the wrong token, a
one-off component, and a genuinely different behavior. Similar colors alone
do not mean two components should be merged. Reuse existing roles and primitives
before creating new ones; preserve deliberate exceptions with their evidence.

## Document

For a documentation request, use the named destination or existing maintained
design-system record. If neither is specified, use the established project docs
location and link it; do not impose upstream PRODUCT.md, DESIGN.md or sidecars.
When a destination decision materially affects ownership, ask that one question
while continuing source inspection. Do not edit UI during a document-only task.

Capture only reusable facts with source locations: semantic color roles and
observed values; typography roles/families/weights and script coverage; spacing,
containers and breakpoints; radius/elevation; control variants and meaningful
states; interaction/motion rules. Include exact values when observed, not from
mood words or invented ramps. Mark unresolved/proposed direction distinctly.
Avoid a copied CSS dump, duplicated token definitions, invented components, or
turning one route's layout into a system-wide prohibition.

Update the existing record idempotently, preserving human decisions and unrelated
sections. Record the scoped evidence and limits. Do not claim a screenshot
provides exact tokens or behavior when source/render evidence is unavailable.

## Extract

Confirm the authorized components, paths and consumers. Identify repeated uses
with the same intent, semantics and state behavior; extraction needs concrete
reuse value, not a fixed occurrence count. If no shared location exists, choose
a small location consistent with the repository rather than installing a system.

Define the smallest useful API and semantic roles before moving code. Keep
accessible names, focus, error wiring, disabled/loading states, supported themes
and responsiveness intact. Preserve source order and meaning. Avoid a universal
component with unrelated variants or tokens for every local exception.

Migrate only authorized consumers and remove obsolete local styles in that
scope. A shared primitive change with effects beyond it needs the parent to
resolve the write boundary before applying; return the affected consumers,
not a silent whole-site migration. Documentation and demos follow the project's
existing convention, without introducing Storybook or another dependency.

Verify visual and behavioral parity on affected consumers, states and widths.
For intended visual changes, compare against the requested outcome instead of
pretending they are parity. Report what was shared, which consumers migrated,
exceptions retained, actual checks and outstanding drift outside scope.

Adaptation provenance and license: [upstream](upstream.md).
