# Blocker readiness and remediation

Read during whole-batch preflight and whenever a new blocker stops execution.

## Establish the blocker

Use task/spec requirements, project setup docs, safe configuration templates,
existing runner evidence, and explicit user statements. Give each distinct
blocker a short working ID and list all affected tasks; deduplicate shared
prerequisites. Do not require every unfinished dependency to be completed by
the user. The batch implements its own authorized dependency graph.

For each blocker, report:

| Blocker | Affected tasks | Evidence / why needed | User action | Expected location | Unblock check |
| --- | --- | --- | --- | --- | --- |
| <ID and reason> | <task IDs> | <source path and prerequisite> | <concrete steps> | <file, service, or decision record> | <safe observable condition> |

Avoid vague instructions such as "fix environment". Distinguish an absent
credential, missing permission, unavailable service, missing required runner,
ambiguous spec, and an unauthorized dependency: each has a different remedy.
Use project-detected names and commands; do not invent an environment-variable
name, setup URL, callback URI, tool, or framework convention.

If provider-specific setup is needed, fetch relevant current official docs
through the host's documentation tools before giving precise steps. Cite the
source and identify what could not be verified. A missing external account or
permission must be explained to the user rather than provisioned automatically.

## Credentials and private configuration

Prefer `.env.example`, configuration schemas, safe docs, and variable-name
references to discover required keys and the file/runtime that loads them.
Ask the user to place real values directly in the intended local environment
or secret store. Never ask them to paste credentials into chat or a task file.
Do not display, copy into notes, commit, or echo live secret values.

If checking private configuration is necessary and authorized, use a narrowly
scoped local check that reports only required-key presence/non-emptiness and
known-placeholder detection. Do not dump the file, log values, execute/sourcing
the env file as shell code, or send values to an external service merely to
verify setup. Presence is not proof that a credential is valid or permitted;
record that distinction. Use a documented authorized check when one exists,
otherwise retain the unavailable validation as a limitation or blocker according
to whether it is needed for the required task verification.

An example report, only if repository evidence establishes these names:

```text
B-01 — OAuth configuration missing (TASK-004, TASK-007).
Evidence: .env.example and the auth setup guide require GOOGLE_CLIENT_ID and
GOOGLE_CLIENT_SECRET in .env.local.
Action: obtain the OAuth client values for your application's provider project
following the linked current official setup guide, then set both keys locally
in .env.local. Use the callback configuration specified by this repository.
Do not send the values in chat.
Unblock: the expected keys are nonempty/non-placeholder and the documented
local auth verification can run; credential validity is checked only through
that authorized flow.
```

This is a conditional illustration, not a universal Google setup procedure.
Some projects use `.env`, a deployment secret store, or different key names.
Do not request production credentials when the task needs only a test environment.

## Other common remedies

- Permission/account access: identify the specific capability and account scope
  from evidence, the action the user/admin must take, and an authorized check.
- Required testing infrastructure: list the installed skill/runner/environment
  that is absent and the project's supported setup procedure; do not auto-install
  replacements or silently change required to auto/off.
- Product/spec ambiguity: identify the exact unresolved decision and route to
  `$grill-workflow`, `$write-spec`, `$grill-design`, or `$to-tasks` as appropriate.
- Dependency outside scope: name its task ID; ask whether to include it or have
  it completed first. Missing IDs/cycles require task-graph correction.
- Manual review barrier: identify the in_review prerequisite and effective mode;
  request the owning review/policy action without treating it as done.

Recheck the specific unblock condition after the user acts. Keep unresolved
items visible, report only safe evidence, and do not start implementation until
all whole-batch user-action blockers are resolved.
