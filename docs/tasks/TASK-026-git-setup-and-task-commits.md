# TASK-026: Git setup and automatic task commits

- Status: done
- Spec: [SPEC-013](../specs/SPEC-013-git-setup-and-task-commits.md)

## Goal

Ask about Git initialization during setup and persist standing task-commit
authorization for single and batch implementation as specified in SPEC-013.

## Blocked by

None.

## Todo

- [x] Add setup Git detection, bundled initialization/commit choice, schema, reuse and failure rules (AC-01).
- [x] Connect implement-task and auto-implement to required task commits with preserved gates/index/reviewer boundaries (AC-02–AC-03).
- [x] Update public workflow/README and authoritative requirement/context (AC-04).
- [x] Pack consistency checker passed (23 skills, source/interface files, catalog counts, frontmatter/names, references, routing and local links); git diff --check passed. Supplementary quick_validate.py is unavailable on this host because PyYAML is missing as observed in TASK-025; source frontmatter/interfaces were unchanged.
- [x] Isolated standard-library subprocess smoke check passed for non-repository detection, successful git init/root resolution, enclosing repository detection without nested .git, task-only initial commit preserving an unrelated untracked file, detection of unrelated staged work via the full cached diff, and linked-worktree detection where .git is a file. Only a temporary repository was initialized/committed; the actual skill-pack repository Git state was preserved.
- [x] Manual instruction walkthrough (not an independent model execution): new yes produces initialized/required; no produces declined/disabled; pending answers do not authorize init; existing/enclosing/worktree projects skip init and reuse explicit policy or ask only for missing commit choice; reruns preserve choices; required commit failures block readiness; disabled/legacy policy does not infer permission; resumes avoid empty/duplicate commits; reviewer status writes remain outside implementation commits. AC-01–AC-03 clauses are present in the owning entrypoints/references.
- [x] Scoped self-review checked setup/reference/schema, both implementation entrypoints, Git details, existing gate/finalization/review contracts and documentation (AC-01–AC-04). Prior TASK-025/Ponytail changes were preserved, not attributed to this task. No application/runtime code changed, so application unit/integration/E2E tests are not applicable. Model adherence to these instructions remains to be observed in real usage; no independent agent evaluation or canonical review dispatch is claimed. No current-project initialization, commit, push or global Git configuration change performed.
