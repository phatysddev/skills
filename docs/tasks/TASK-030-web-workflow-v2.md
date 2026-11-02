# TASK-030 — Implement the v2 local web skill workflow

Status: done
Spec: [SPEC-017](../specs/SPEC-017-web-workflow-v2.md)

## Scope

Add start-workflow with bundled web runtime, durable queue and agent CLI;
adapt all 23 existing skill entrypoints; synchronize maintained catalogs and
workflow guidance. Preserve existing stage authority and chat compatibility.

## Acceptance and verification

- AC-01–02: server, request form and reference persistence.
- AC-03–04: four question types, named stage actions, shared adapters.
- AC-05: prototype workspace, pages, viewport and scoped edit requests.
- AC-06–07: durable events, idempotency, atomic ack and local/path boundaries.
- AC-08: installed-skill portability and honest active-agent instructions.

## Evidence

- Bridge/HTTP regressions: 14 passed, including durable replay/atomic ack, all answer types, uploads, stale input, host/origin/token checks and preview confinement.
- Browser checks (isolated temporary project on port 9910): request → /grill; input/select/checkbox/textarea answers received by CLI; /prototype Home/Details tabs; 390px viewport and reload; feedback received with UI-2; named acceptance action received as spec-with-prototype; 390×844 responsive tools stack; complete → new-workflow → second request; existing-tab draft submitted successfully after server restart with no reload. Main localhost:9909 workspace remains idle and free of QA requests.
- Pack consistency passed for 24 skills. Existing artifact tests: 22 passed; UI-helper tests: 28 passed. JS syntax and git diff whitespace checks passed. Bundled quick_validate.py could not run because this host lacks PyYAML; the repository pack checker independently verified frontmatter, metadata presence, names, catalogs, router coverage and Markdown references.
- Independent review found three issues (new workflow access, noncanonical preview paths, restart token refresh); all fixed and regression/browser checked. Final re-review also corrected the prototype-completion visibility edge.
- Commit policy: disabled for this change under repository instructions; no push.

## Final canonical code review

Mode: final. Approved TASK-030 task-owned working tree against HEAD, including
new start-workflow runtime/assets/protocol/tests, SPEC-017/TASK-030 and maintained
skill adapters, catalogs, workflow docs and generated static site files. No
remaining actionable findings in the reviewed scope. AC-01–08 are supported by
implementation inspection and the recorded bridge/HTTP/browser evidence. The
three original findings and the prototype-completion start-screen visibility
edge are resolved in source. Durable agent audit events and retained request
history preserve recovery evidence across new requests.

The reviewer independently reran 10 bridge tests, the 24-skill pack checker, JS
syntax and diff whitespace checks; all passed. Parent evidence supplies 14
combined bridge/HTTP tests, 22 artifact tests, 28 UI-helper tests and the isolated
browser interaction/restart/responsive checks. These establish the transport
and UI contract; they do not establish autonomous model availability after a
host ends its agent turn, production consumer acceptance, or external effects.
The documented active-agent requirement and local-HTML preview limits remain
explicit. PyYAML-dependent quick_validate was unavailable; the maintained pack
checker verified source names/frontmatter/metadata/catalog/link consistency.
Reviewer changed only this task's review evidence/status; no implementation,
other artifact or Git mutation.
