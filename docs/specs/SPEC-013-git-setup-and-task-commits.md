# SPEC-013: Git setup and automatic task commits

- Status: done
- Requirement: [Requirement](../requirement.md#current-capability-git-setup-and-automatic-task-commits)
- Context: [Context](../../CONTEXT.md#current-capability-git-setup-and-automatic-task-commits)

## Problem and outcome

The user requests a Git-init question during setup and automatic commits from
both single-task and batch implementation when initialization is accepted.
Persist the choice so later skills do not ask again or infer authorization
merely from a repository's existence.

## Scope

Ask once about initialization plus its automatic task-commit consequence.
Reuse prior decisions, recognize parent repositories and linked worktrees,
initialize only the selected project root, and persist one confirmed Git Policy
in CONTEXT.md. For existing Git without policy ask about commits separately.
Keep existing explicit policy and honor user overrides. Missing answers/failures
remain unresolved; declining does not initialize Git.

Confirmed required commits run after verification and before in_review through
the main implementation owner, one task per commit/correction cycle. Preserve
index boundaries, avoid empty/duplicate commits, and block unresolved required
commit failures. Review/status authority and test policy remain unchanged.
No automatic initial commit, identity configuration, branch/remote creation,
push, history rewrite or Git installation. Consumer policy is not silently
applied to this skill-pack repository itself.

## Acceptance and verification

| ID | Observable behavior | Verification |
| --- | --- | --- |
| AC-01 | Setup detects Git correctly, asks when needed, explains commit opt-in, persists confirmed policy and reuses it. | Source walkthrough for new/declined/existing/enclosing/worktree/rerun scenarios; isolated Git detection smoke check. |
| AC-02 | Single and batch implementation reuse required commit authorization without per-task questions, after gates and before review. | Inspect both entrypoints, Git reference and existing finalization/handoff contracts. |
| AC-03 | Missing Git/identity, failed commit or unsafe index isolation is reported accurately; no unrelated staged files, duplicate or empty commits, push or reviewer writes. | Source boundary scenarios and isolated staged-index smoke check. |
| AC-04 | Documentation, references and 23 identifiers stay coherent. | Pack checker and diff check. |

## Delivery

Owned by [TASK-026](../tasks/TASK-026-git-setup-and-task-commits.md).
Instruction-only change; application tests are not applicable. No commit of
the skill-pack changes is authorized by this behavior request.
