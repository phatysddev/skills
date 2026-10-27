# TASK-027: Preserve prototype fidelity and reconcile revisions

- Status: done
- Spec: [SPEC-014](../specs/SPEC-014-prototype-fidelity-and-reconciliation.md)

## Goal

Fix the reusable prototype-to-production contract and the post-planning
revision path described in SPEC-014, preserving existing workflow ownership.

## Blocked by

None.

## Todo

- [x] Add immutable baseline, UI contract, visual AC and rendered-comparison guidance across spec, tasks, implementation and review (AC-01–AC-02).
- [x] Preserve referenced baseline assets before edits; report shared-file and downstream impact; distinguish experiments from accepted replacements (AC-03).
- [x] Coordinate replacement interpretation and task reconciliation within change-scope, with mixed-status evidence handling and batch boundaries (AC-04).
- [x] Update routing, supporting skills and authoritative/public docs while preserving 23 identifiers (AC-05).
- [x] Maintenance checks: python3 scripts/check_skill_pack.py passed for all 23 skills, frontmatter/name matching, source/interface files, catalog counts, active references/router coverage and local links. git diff --check passed. No runtime code or dependency changed; application/scanner tests are not applicable to this instruction-only change.
- [x] Manual source scenario: accepted booking-v3 desktop two-column/mobile stack plus type/color/component treatment maps through UI-01 and visual AC to task Goal/comparison Todo, implementation baseline inspection and canonical reviewer input. A generic restyle with matching fields is a visual AC defect; a listed semantic/accessibility adaptation is an allowed exception. Missing browser/render output remains unverified, not a visual pass (AC-01–AC-02).
- [x] Manual revision scenario: editing shared CSS used by two accepted pages requires preserving HTML plus dependency assets outside the live tree and reporting both consumers, even with one unchanged HTML. An experiment leaves the accepted baseline valid; accepting replacement triggers reconciliation. Missing old files are reported/recovered from actual history, never reconstructed as fact (AC-03).
- [x] Manual mixed-status scenario: for an accepted v4 replacement after tasks exist, change-scope owns the operation, composes spec-with-prototype interpretation, updates UI/AC baseline delta, then composes to-tasks. todo/in_progress work updates in place; affected in_review leaves readiness and gains unchecked re-verification; done delivery keeps history with only missing delta follow-up. Unaffected evidence stays valid. On repetition existing follow-ups are reused; new tasks are not silently added to an active batch (AC-04). These are instruction walkthroughs, not executed independent model evaluations.
- [x] Scoped self-review inspected spec reconciliation, edit revision preservation, task mapping, implementation/finalization/reviewer handoff, code-review criteria, change-scope composition and router/batch rules plus docs. Resolved the prior contradictory visual-only/pixel exclusion rules and clarified that accepting a rendered design can make previously delegated styling contractual. Existing four verification modes, task body shape, review/status ownership and commit policy remain. No consumer application/prototype was supplied or repaired, and no production visual-fidelity benchmark or independent agent result is claimed. Changes remain uncommitted.
