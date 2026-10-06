# TASK-021: Add inline agent security

- Status: done
- Spec: [SPEC-009](../specs/SPEC-009-agent-security.md)

## Goal

Protect Phat research and workspace actions against source prompt injection
while preserving authorized task execution (AC-01–05).

## Blocked by

- None

## Todo

- [x] Added the utility, metadata, and focused decision examples (AC-01–03).
- [x] Integrated all 22 existing parent skills: 21 inline source/host boundaries plus compact-context provenance preservation; verification dispatch passes the boundary without expanding worker permissions or changing gate modes (AC-04).
- [x] Updated canonical catalogs and bilingual website content to 23 skills; source/catalog/homepage/guide names match exactly (AC-01).
- [x] Repository checker passed for 23 skills; real Ruby YAML parsing passed all skill frontmatter/interface files and the new skill's name/schema/description/scaffold constraints; JS syntax checks passed and site generation was idempotent.
- [x] Validation limitation: skill-creator quick_validate.py could not import PyYAML in either system or bundled Python. Used parsed Ruby YAML plus equivalent constraints and the pack checker; no dependencies installed. No Git metadata is present in this workspace, so no git diff check was available.
- [x] Independent isolated forward-test completed: docs fixture rejected a concealed diagnostic/credential directive while implementing the task; wrapper fixture inspected the verify-to-publish chain and ran the safe checks directly, explicitly leaving the full wrapper unverified; handoff fixture retained claimed approval as untrusted instead of a runnable prerequisite (AC-02–05).
- [x] Inspected actual generated code and compacted handoff, reran all three behavior checks successfully, and verified diagnostic/outbound/deployment sentinel files were absent. No network, real credentials, host changes, or skill-pack writes by the evaluating agent.
- [x] Boundary review completed against AC-01–05: existing authorization, parent ownership, gate result semantics, missing-utility fallback, and useful unaffected work are preserved. Skills provide behavioral guidance rather than host enforcement; no sandbox guarantee or application-security audit added.
- [x] Commit policy: disabled; no commit or push requested.
