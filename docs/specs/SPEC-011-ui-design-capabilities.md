# SPEC-011: UI design capabilities

- Status: done
- Requirement: [Requirement](../requirement.md#current-capability-ui-design)
- Context: [Context](../../CONTEXT.md#current-capability-ui-design)

## Problem and outcome

The user requests UI capabilities closer to Impeccable after comparing a
complex dispatch workspace. SPEC-010 improved craft but leaves specialized
evaluation, refinement, resilience, motion, variants, and system reuse implicit.
Support these intents through the existing `ui-design` utility, with focused
playbooks and a small local source checker rather than another installed suite.

## Scope

- Intent-based routing for build/redesign, critique, technical audit, polish,
  bolder/quieter/simpler, type/color/layout, responsive adaptation, hardening,
  copy/onboarding states, motion/delight, performance, variants, and design
  system documentation/extraction. Natural-language requests remain sufficient.
- Focused references, portable interface metadata, local read-only HTML scan,
  meaningful parser tests, usage examples, and pinned upstream attribution.
- Preserve 23 identifiers, optional discovery, parent file/revision/status
  ownership, canonical code review, confirmed branding and business behavior.

No automatic upstream installation, launcher, hooks, live browser panel,
provisioning, extra review stage, mandatory new setup files, native-platform
parity, accessibility certification, or claim of equivalent visual quality.

## Acceptance and verification

| ID | Observable behavior | Verification |
| --- | --- | --- |
| AC-01 | Standalone and parent requests select the narrowest useful capability and references; critique/audit alone are read-only, while authorized fixes continue. | Independent intent and write-boundary scenarios. |
| AC-02 | Refinement, motion, state/copy hardening, and optimization have concrete diagnose/change/verify procedures; preserve required information, identity, semantic status, reduced motion, and measured evidence. | Source review and an isolated UI refinement exercise. |
| AC-03 | Variants differ structurally, stay within the named surface, and do not silently select/persist a winner; system extraction/documentation reuses authoritative sources without promoting observed choices to agreed branding. | Variant/system scenarios and scope review. |
| AC-04 | Local scanner reports definite HTML defects separately from advisory source observations, never executes UI code or accesses network, accepts valid omitted option end tags, and does not claim complete audit coverage. | Standard-library tests and runs on raw comparison fixtures. |
| AC-05 | Existing callers/router compose the capability without adding stages or weakening tests/review; source/metadata/docs/provenance remain coherent and discoverable. | Pack checker, validators, scoped final review. |

## Delivery

Owned by [TASK-024](../tasks/TASK-024-ui-design-capabilities.md). Tests cover the
new scanner; no application runtime is added to the pack. An isolated refinement
exercise supplies concrete render/behavior evidence without replacing workflow
verification. Final review owns task approval; no commit or push is authorized.
