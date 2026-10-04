# TASK-020: Add scope changes and optional assessments

- Status: done
- Spec: [SPEC-008](../specs/SPEC-008-scope-and-assessments.md)

## Goal

Add three optional skills with explicit ownership and compatible Phat handoffs.

## Blocked by

- None

## Todo

- [x] Implement sources and interface metadata for all three skills (AC-01–04); Ruby YAML parsing verified names, descriptions, prompts and default automatic discovery.
- [x] Integrate router, planning, implementation, batch, and review handoffs without new mandatory gates (AC-05); preserve active/retired criteria, task history, status ownership and explicit batch scope.
- [x] Update canonical documentation and public catalogs (AC-06); all 22 source/catalog/homepage/guide entries agree and generated Codebase Context is byte-identical to HEAD.
- [x] Verify isolated behavioral scenarios: changed cutoff plus notification content preserved done work and planned a follow-up; impact-only request changed no files; removed notification obligation retired its open task and produced an empty executable queue.
- [x] Feature fixture: 2 unit tests passed while independent public-entrypoint inspection exposed missing cancellation-to-notification integration; returned not verified without source/status writes.
- [x] Release fixture: reported blocked, identified required review and configuration/recovery evidence gaps, and did not execute a build hook that called deployment; deployment sentinel absent.
- [x] Router fixtures: active implementation without generated context, explicit feature assessment, explicit scope change, explicit staging assessment, genuinely complete scope, and contradictory done metadata produced the appropriate bounded routes without a refresh/assessment loop.
- [x] Final checks: python3 scripts/check_skill_pack.py passed for 22 skills; JS syntax checks passed for catalog, translations, script and site builder; site generation passed and was idempotent; git diff --check passed.
- [x] Validation limitation: skill-creator quick_validate.py could not run because PyYAML is absent; real YAML parsing with Ruby plus repository frontmatter/catalog/reference checks passed instead. No dependencies installed.
- [x] Test-capability relevance: no application behavior was added; instruction behavior was forward-tested in isolated fixtures, catalog/site generation checked directly. Existing unit/integration/e2e/review policy was not modified.
- [x] Standalone review approved — working-tree scope against HEAD plus new skill/spec/task files; AC-01–06 verified from source contracts, isolated fixture evidence and final checks; no unresolved actionable findings. Delegated preliminary review also reported no substantive findings; its final report was interrupted, so approval is based on the completed standalone review.
- [x] Commit policy: disabled; no commit or push requested.
