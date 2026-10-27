# TASK-028: Synchronize agreements and verify portable workflow contracts

- Status: done
- Spec: [SPEC-015](../specs/SPEC-015-agreement-synchronization.md)

## Goal

Close agreement-update bypasses, align setup, support scoped runner sets and
portable Git boundaries, and add executable artifact/regression evidence.

## Blocked by

None for source changes. Production visual fidelity is unverified where rendering
is unavailable; this fixture does not establish general model reliability.

## Todo

- [x] Add pending-agreement guards and idempotent reconciliation identity (AC-01).
- [x] Remove conflicting context routing and duplicate clear-answer confirmation (AC-02).
- [x] Support package-scoped ordered runner sets and per-entry results (AC-03).
- [x] Disclose host capabilities before policy selection, preserving delegated verification (AC-04).
- [x] Separate portable Git identity/boundary from observed checkout path (AC-05).
- [x] Add read-only artifact checker and executable negative/positive tests (AC-06).
- [x] Record [executed behavioral fixture evidence](../evidence/workflow-regression-2026-10-27.md): mixed-status/shared CSS reconciliation, repeat without duplicate writes, resume blockers and two scope-specific runner commands. Direct Chrome probe failed; subsequent app-browser inspection observed matching b1 Home desktop only. Mobile/b2/final visual review remain unverified.
- [x] Artifact regression suite: 15 tests passed; existing HTML checker: 28 tests passed; pack checker passed; git diff --check passed. Fixture artifact index, navigation and baseline commands passed. Temporary clone/worktree [probe](../evidence/git-relocation-probe.json) established relocation evidence without changing this repository's Git state.
- [x] Scoped source review checked discovery/setup guards, parent runner selection and interface prompts, policy reuse and relocation links, checker failure modes and evidence limits. No commit or push. Self-review does not substitute for a canonical final reviewer.
- [x] Final canonical code-review approved — TASK-028 working tree (tracked diff against HEAD plus task-owned untracked checker/tests/spec/evidence); AC-01–AC-06 sufficiently verified by scoped source review, executed fixture, temporary Git probe and checks. No findings. Reviewer independently reran 15 artifact regressions, pack checker and git diff --check; all passed. Parent supplied terminal dedicated verification reports: required unit passed (15 tests), required integration passed (same 15 filesystem/hash/path/read-only tests plus real fixture CLI, not 30 distinct tests); required e2e was irrelevant because this change is maintenance instructions/local CLI, with no production application journey. Existing HTML suite's 28 passes and fixture navigation/baseline runs were previously recorded and credible. Reviewed saved b1 Home desktop comparison; mobile/other pages/b2 production/final consumer visual review and general model reliability remain unverified and are outside this bounded maintenance delivery. Reviewer authored the fixture earlier; final source review is a distinct delegated review of the parent's implementation, not an independent visual benchmark. No commit/push or implementation write by reviewer.
