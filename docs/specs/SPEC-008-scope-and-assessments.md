# SPEC-008: Scope changes and optional assessments

- Status: done
- Requirement: [Requirement](../requirement.md)
- Context: [Context](../../CONTEXT.md)

## Problem and outcome

An agreed behavior can change after tasks start, task-local checks can miss
feature-wide gaps, and review approval alone does not establish release readiness.
Add three optional skills with distinct ownership and evidence-based handoffs.

## Scope

- `change-scope`: assess or apply an agreed change to the existing requirement,
  owning spec, and affected work plan. Preserve completed deliveries and allocate
  follow-up work rather than rewriting history.
- `verify-feature`: report full-feature acceptance and cross-task evidence.
- `release-check`: report readiness of a candidate for an identified environment.
- Integrate routing, supporting skill handoffs, metadata, and public catalogs.

No automatic deployment, new verification modes, mandatory assessment stages,
context-refresh gates, or automatic expansion of an existing task batch.

## Acceptance and verification

| ID | Observable behavior | Verification |
| --- | --- | --- |
| AC-01 | Three independently discoverable skills have valid source and interface metadata. | Skill validators and catalog/source checks. |
| AC-02 | An instructed scope change updates its existing contract and affected plan, retains done-task history, and invalidates affected review readiness/evidence without implementation changes. Impact-only requests stay read-only. | Isolated change fixture and boundary review. |
| AC-03 | Feature assessment maps all ACs to attributable evidence, distinguishes missing cross-task behavior from passing unit checks, and does not change task/spec status. | Isolated feature fixture with disconnected producer/consumer behavior. |
| AC-04 | Release assessment binds its verdict to candidate/environment and reports failed or unknown prerequisites without executing deployment/migration hooks. | Isolated release fixture with a build hook that deploys. |
| AC-05 | Routes preserve existing task ownership, the four verification-policy modes, batch scope, and settled decisions; no automatic assessment chain or parent/child routing loop is introduced. | Cross-skill handoff review and fixture outcomes. |
| AC-06 | Canonical catalogs and rendered website list the same 22 skills and classify assessments separately from task test capabilities. | Repository checker, catalog comparison, site generation and inspection. |

## Delivery

Owned by [TASK-020](../tasks/TASK-020-scope-and-assessments.md).
