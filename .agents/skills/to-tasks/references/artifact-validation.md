# Project artifact validation

Run the bundled read-only checker after decomposition or scope reconciliation
when an artifact index is maintained. Resolve script paths from the installed
skill directory; do not assume the consumer project has the pack's scripts.

```text
python3 <to-tasks>/scripts/check_project_artifacts.py <index.json> --root <project-root>
```

Use the existing source Markdown as authority. The index is a derived audit
input, never a second source of decisions. Create/update it from inspected
sources within the authorized planning scope; do not modify agreements merely
to satisfy validation. If no index exists and producing it is outside scope,
report validation as manual/unverified, never an automated pass.

Version 1 shape (paths relative to root, SHA-256 of exact bytes):

```json
{
  "version": 1,
  "specs": [{"id": "SPEC-001", "path": "docs/specs/SPEC-001.md", "sha256": "<64 hex>", "agreement": "revision-2", "acs": ["AC-01"], "baselines": ["ui-2"]}],
  "tasks": [{"id": "TASK-001", "path": "docs/tasks/TASK-001.md", "spec": "SPEC-001", "status": "todo", "agreement": "revision-2", "acs": ["AC-01"], "dependencies": []}],
  "baselines": [{"id": "ui-2", "files": {"docs/assets/prototype-baselines/ui-2/index.html": "<64 hex>", "docs/assets/prototype-baselines/ui-2/style.css": "<64 hex>"}}]
}
```

Add `Agreement: revision-2` metadata to indexed source specs/tasks. Record the
actual agreement revision; do not relabel old evidence. A historical done task
may reference an older agreement but needs current task coverage for its changed
ACs. For explicitly assessed unchanged evidence, an indexed task may carry
`"valid_for": ["revision-2"]` and a nonempty `"evidence_basis"` linking the
reconciliation assessment. This preserves historical delivery without creating
unnecessary delta work. The reviewer must inspect that assessment; the utility
cannot prove its meaning. `retired: true` requires blocked status. This optional metadata preserves
Goal / Blocked by / Todo bodies and existing status ownership.

The checker checks source AC declarations (`| AC-01 |` table rows, `AC-01:`
lines or bullet declarations such as the write-spec template’s `- AC-01:`),
the task’s single `- Spec:` Markdown metadata link against its
indexed owning spec (resolved target and any SPEC ID in the label), task status, agreement markers, AC mentions, dependency IDs in Blocked
by, cycles/missing dependencies, current coverage, spec fingerprints and baseline
hashes. Include all tasks/dependencies and all baseline files including shared
CSS/JS/assets. Unsupported AC formats fail with a manual-review message.
Exit 0 means indexed structural checks passed; 1 means findings; 2 means invalid
input. It cannot prove index completeness, semantic AC coverage, immutable Git
history, correct impact classification or visual fidelity. Review source/index
completeness and render evidence separately. Never treat a hash pass as a visual
pass or mutate task status based on this utility.
