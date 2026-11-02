# SPEC-017 — Web-first workflow v2

Status: done

## Problem and outcome

The skill pack currently interacts through chat-only handoffs. Users want a
local web workspace with an active coding agent awaiting browser events.
Preserve existing workflow decisions, artifact ownership and verification while
making the web the main surface across all stages.

## Agreed behavior

- AC-01: A new installable `start-workflow` starts a self-contained, dependency-free
  local runtime on localhost:9909 for the selected consumer project. It resumes
  durable state; another project's occupied port is a conflict.
- AC-02: `/` provides a request textarea, multiple reference attachments and
  submit. Files are stored under docs/ref/ with unique names. Submission durably
  queues grill-workflow input and navigates to /grill.
- AC-03: The active parent agent publishes relevant checkbox, select, input and
  textarea question sets. Required/type/choice checks and question-set/revision
  checks reject invalid and stale answers. No canned model responses.
- AC-04: All existing skills use the shared web event adapter during web sessions.
  Parent progress, results and explicit next-skill actions are visible on the
  web. Clicked actions authorize their named stage; existing document, scope,
  testing, review, commit and deployment boundaries remain authoritative.
- AC-05: `/prototype` provides left 70% workspace and right 30% tools. Left
  vertical layout is 10% page tabs, 60% preview and provisional 30% activity.
  Tools select viewport, reload preview, request page-scoped edits and accept
  via named next actions. Responsive layouts stack tools below.
- AC-06: Events survive process restart and are acknowledged atomically with
  agent state updates. At-least-once delivery requires the agent to reconcile
  already-written artifacts on resume. Duplicate browser keys do not enqueue
  duplicate work. One parent consumes events; no competing delegated consumers.
- AC-07: Bind loopback only, reject foreign hosts/origins, require per-server
  mutation tokens, confine uploads/preview paths, and isolate prototype scripts
  in a sandbox. Browser payloads cannot execute shell commands or publish agent
  state. Persisted state and canonical artifacts remain separate.
- AC-08: Installation includes the runtime assets/protocol. Documentation explains
  that an active agent is necessary; a running server does not imply an active
  model. Interrupted agent turns resume with start-workflow.

## Architecture

`start-workflow/{scripts,assets,references}` travels with the installed skill.
Python 3.10+ HTTP server and SQLite use only the standard library. Browser
mutations enqueue events; a local CLI supplies bounded wait/state/publish.
Polling refreshes browser state without rebuilding the current question form.
The current coding agent runs skills with existing tools and permissions.
There is no provider-specific SDK, API credential handling or browser command
runner. A future always-on worker is separate scope.

## Verification and limits

Task: [TASK-030](../tasks/TASK-030-web-workflow-v2.md). Bridge unit/integration
regressions cover persistence, replay, atomic ack, stale answers, upload and
path constraints. Browser checks cover the request, all form types, prototype
navigation, tools and responsive layout. Model decisions and consumer artifact
semantics still require the owning agent; transport tests cannot prove them.
No push/deployment. Prototype previews support local HTML and relative assets,
not arbitrary backend-dependent applications.
