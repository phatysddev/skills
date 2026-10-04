# SPEC-005: Historical template-selection capability

- Status: done
- Requirement: [docs/requirement.md](../requirement.md)
- Context: [CONTEXT.md](../../CONTEXT.md)
- ADRs: None

## Retirement

The `setup-template` skill and its workflow stage were removed on 2026-10-03
at the user's request. This specification records historical implementation;
it does not define an active capability or authorize recreating the skill.

After `setup-project`, the workflow recommends `to-prototype` when visual
validation is requested, otherwise `write-spec` when the feature is ready.
Optional custom UI design discovery remains with `grill-design`.

## Historical implementation

[TASK-009](../tasks/TASK-009-setup-template-research.md),
[TASK-010](../tasks/TASK-010-persist-confirmed-design-direction.md), and
[TASK-011](../tasks/TASK-011-integrate-setup-template-workflow.md) record the
original implementation. Their template-selection instructions and checks
no longer apply. Existing project design and brand decisions remain evidence
for downstream UI work.
