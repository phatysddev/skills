# TASK-025: Adapt Ponytail core guidance

- Status: done
- Spec: [SPEC-012](../specs/SPEC-012-smallest-complete-changes.md)

## Goal

Integrate smallest-complete-change guidance into existing implementation and
review skills with Phat scope, protection and verification boundaries intact.

## Blocked by

None.

## Todo

- [x] Inspect pinned Ponytail core source and MIT license; adapt implementation and review criteria (AC-01–AC-03).
- [x] Keep 23 identifiers and add self-contained source/license notices to both adapted skills; update requirement, context, workflow and README (AC-04).
- [x] Pack checker passed for 23 skills including frontmatter/name, catalog, routing and local links; git diff --check passed. quick_validate.py could not run because host Python lacks PyYAML; no dependency was installed. No frontmatter/interface changes were made.
- [x] Manual instruction walkthrough (not an executed model benchmark): a shared-signature change must trace/update consumers; deleting trust-boundary validation is forbidden; a smaller feature that drops an AC stays a scope proposal; a justified larger adapter is allowed; reviewer cannot fix production code or report line count alone as a defect. Source clauses support AC-01–AC-03 without overriding existing test policy.
- [x] Focused self-review against pre-change HEAD inspected all changed skill guidance, both MIT notices, docs and this spec/task (AC-04); no conflicting scope/status/verification instruction found. Not an independent agent evaluation or canonical final-review dispatch. No executable code changed, so application unit/integration/E2E runs are not applicable. Runtime adherence remains unproven until real use. No commit or push performed.
