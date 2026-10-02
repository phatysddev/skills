# Implement reference: verification capability selection

Use this reference before implementing a task when `implement-task` must select
test capabilities from project policy and task evidence.

## Selection inputs

Read these sources before selecting a capability:

1. the project-owned `CONTEXT.md` `## Verification Policy` section;
2. the current task's `Goal`, `Blocked by`, and `Todo` items;
3. the linked feature specification and the task's observable acceptance
   criteria; and
4. repository evidence needed to identify installed capability skills and
   supported test runners.

The persisted policy is valid only when it is a confirmed policy with exactly
one mode value (`auto`, `required`, or `off`) for each of these four roles:

```text
unit-test
integration-test
e2e-test
code-review
```

If the policy is missing or malformed, do not invent defaults, derive values
from available runners, or let a task override silently create a policy. Stop
with an unresolved policy result and route to `$setup-project`.

## Per-task override

An override is valid only when the current user or parent workflow explicitly
names a capability, chooses `auto`, `required`, or `off`, and supplies a
rationale.
An example shape is:

```text
Verification override for this task:
- capability: e2e-test
  value: off
  rationale: The acceptance criteria contain no user-visible journey.
```

Apply a valid override only to the in-memory effective policy for the current
task. Report the persisted value, override value, and rationale together. Do
not edit `CONTEXT.md`, the requirement, the specification, or another task to
record it. Unknown capability names, duplicate overrides, invalid values, and
missing rationales are unresolved; do not guess.

An override cannot repair a missing or malformed project policy. Setup owns
establishing the project policy; `implement-task` owns only the current task's
selection.

## Relevance rules

Evaluate the three test roles independently from the task's scope and
observable acceptance criteria, not from runner availability:

| Role | Relevant when the task includes | Skip reason when absent |
| --- | --- | --- |
| `unit-test` | isolated rules, calculations, validation, pure transformations, or state transitions | identify the acceptance criteria or scope showing no isolated behavior |
| `integration-test` | boundaries between modules, APIs, databases, queues, filesystems, or services | identify the acceptance criteria or scope showing no component boundary |
| `e2e-test` | critical user journeys, navigation, authorization flows, browser interaction, or cross-layer behavior | identify the acceptance criteria or scope showing no critical journey |

Use `skipped with reason` for an `auto` or `required` role that is not relevant;
the reason must point to the task or acceptance criteria. An `off` role is not
invoked and remains reported as off. For a relevant `auto` role, select it only
when its skill and runner are available; otherwise record a non-blocking skip
with the missing or ambiguous resolution. A relevant `required` role blocks
when its skill or runner cannot be resolved. If the task evidence is genuinely
ambiguous about relevance, report the unresolved ambiguity rather than
silently omitting a potentially required gate.

Keep the selected order deterministic:

```text
unit-test → integration-test → e2e-test
```

This task selects the roles; the later verification stage owns sequential
sub-agent dispatch, execution, terminal-report waiting, and gate handling.
Selection itself never runs a capability inline in the main agent.

## Role and runner resolution

For each relevant role whose effective mode is not `off`:

1. discover installed capability skills using exact role identity and matching
   `SKILL.md` metadata;
2. require exactly one capability skill for the role;
3. use that capability's documented runner-resolution contract to detect one
   repository-supported runner from `AGENTS.md`, `CONTEXT.md`, manifests,
   configuration, CI, or existing test guidance; and
4. record the skill path, runner identity/evidence, or an unresolved result.

No matching skill is `missing`. Multiple matching skills, aliases, or
conflicting role claims are `ambiguous`. No runner is `missing`. Multiple
plausible runners without authoritative repository evidence are `ambiguous`.
For `required`, all such results block the current task. For `auto`, record the
result as a non-blocking skip. Do not auto-install or substitute anything.

Do not execute tests, start services, modify test files, or invoke
`code-review` in this selection step. Pass the selection summary to the later
verification stage, which will invoke the selected capability under its own
write boundary and report contract.

## Selection report

Record one row for each test role and keep the project policy visible:

```text
Verification policy: CONTEXT.md#Verification Policy
Task override: <none or capability/value/rationale>

| Capability | Persisted | Override | Effective | Relevance | Selection / resolution |
| unit-test | auto/required/off | unchanged/auto/required/off | auto/required/off | relevant/irrelevant | selected, skipped with reason, or blocked with evidence |
| integration-test | auto/required/off | unchanged/auto/required/off | auto/required/off | relevant/irrelevant | selected, skipped with reason, or blocked with evidence |
| e2e-test | auto/required/off | unchanged/auto/required/off | auto/required/off | relevant/irrelevant | selected, skipped with reason, or blocked with evidence |
```

Also report `code-review`'s persisted value as deferred to the final review
handoff. Do not claim a test capability passed here: selection reports only
policy, relevance, resolution, skip reasons, and blockers.
