# TASK-022: Explain security support across the workflow and website

- Status: done
- Spec: [SPEC-009](../specs/SPEC-009-agent-security.md)

## Goal

Make agent-security composition clear in parent skills, the workflow contract,
and the public website, with linked bilingual usage and installation guidance
(AC-04, AC-06).

## Blocked by

- None

## Todo

- [x] Kept each parent purpose first, placed inline security support before its operational sections, and added relevant contents links. The workflow contract maps all 22 existing skills to their security role (AC-04).
- [x] Added a dedicated security guide, specialized agent-security detail page, links from parent skill pages and workflow paths, subset installation guidance, parent invocation examples, and matching Thai/English copy in interactive docs and the generated static guide (AC-06).
- [x] Browser verification passed: security detail page in Thai and English; security → implement-task → security navigation; homepage search returned exactly agent-security; no browser console errors observed. Saved the Thai preview at /private/tmp/phat-security-workflow-preview.jpg.
- [x] Static checks passed: catalog/source agreement at 23 skills, all 22 parent roles listed, new security prose translations present, static-guide security/parent links present with unique IDs, JS syntax, idempotent site generation, and python3 scripts/check_skill_pack.py.
- [x] Boundary review: parent ownership, verification modes, write boundaries, and missing-utility fallback remain intact. No skill installation, host policy changes, publishing, or workflow stage was introduced.
- [x] Commit policy: disabled; no commit or push requested. Website files are updated locally; no hosting/release action is part of this task.
