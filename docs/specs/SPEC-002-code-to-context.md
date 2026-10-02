# SPEC-002: Generate code-derived repository context

- Status: done
- Requirement: [docs/requirement.md](../requirement.md)
- Context: [CONTEXT.md](../../CONTEXT.md)
- ADRs: None

## Problem and outcome

An existing repository can contain enough code and configuration to continue
work, while its Phat project context is missing, incomplete, or stale. The
standalone `code-to-context` skill reads the repository as evidence and
maintains a durable, reviewable code-derived context in `CONTEXT.md` so other
Phat skills can understand the codebase without rediscovering it from scratch.

The generated context describes the current repository without pretending that
current implementation behavior is an agreed product or architecture decision.

## In scope

- Provide a standalone `code-to-context` skill for an existing repository.
- Inspect relevant source, manifests, configuration, tests, CI, and project
  documentation using safe read-only discovery.
- Create `CONTEXT.md` when it does not exist.
- Maintain one generated `## Codebase Context` section in `CONTEXT.md` using a
  fixed Markdown schema.
- Label material claims as `Observed`, `Inferred`, or `Unknown` and attach
  source paths, line references when useful, and generated date/revision
  metadata.
- Preserve human-authored context and authoritative requirements.
- Record conflicts for later confirmation instead of resolving them silently.
- Redact secrets and sensitive values from generated output.
- Allow `ask-phat` to recommend this skill when repository context is missing
  or stale.

## Out of scope

- Modifying application code, tests, configuration, CI, `AGENTS.md`, README,
  requirements, specs, tasks, or ADRs.
- Creating product decisions, architecture decisions, specifications, or
  implementation tasks from repository observations.
- Running installation, build, test, lint, migration, deployment, or service
  startup commands as part of context discovery.
- Reading or reproducing secret values, private keys, credentials, tokens,
  cookies, or connection-string secrets.
- Invoking downstream Phat skills automatically after context generation.
- Replacing the full `CONTEXT.md` file or rewriting human-authored sections.

## User flow and behavior

### Primary flow

1. The user invokes `code-to-context` for an existing repository.
2. The skill reads repository guidance and relevant project sources before
   making changes.
3. The skill inspects source, manifests, configuration, tests, CI, and relevant
   documentation while excluding generated output, dependencies, vendor files,
   build output, and sensitive values.
4. The skill records repository evidence in the fixed generated schema.
5. The skill creates or replaces only its generated context block in
   `CONTEXT.md` and preserves human-authored sections.
6. The skill reports what it scanned, what it skipped, generated metadata,
   unknowns, and conflicts that need confirmation.

The skill stops after updating context. It does not invoke another skill. The
result is available for `ask-phat` and the downstream Phat workflow.

### Alternate flows

- If `CONTEXT.md` does not exist, create it with a `# Repository context`
  heading and the generated `## Codebase Context` section.
- If a generated block from a prior run exists, replace that block rather than
  appending a duplicate.
- If an unmarked human-authored `## Codebase Context` section already exists,
  preserve it, report a conflict, and do not overwrite or create a duplicate
  section.
- If a source, manifest, or configuration area cannot be inspected, continue
  with the remaining safe inputs and record the gap as `Unknown` with its path
  and reason.
- If the repository has uncommitted changes, record the source revision as a
  working tree rather than presenting a clean commit as the source.

## Business rules and constraints

- Existing implementation is evidence of current behavior, not automatically
  the intended product or architecture contract.
- Requirement documents, accepted specs, and ADRs remain authoritative for
  intended behavior and decisions.
- When code conflicts with an authoritative source, preserve the source and
  record the mismatch under `Conflicts / Needs confirmation`.
- An `Inferred` claim must remain explicitly labeled and be supported by one or
  more `Observed` facts.
- An `Unknown` claim must identify what could not be established and, when
  possible, the evidence that was searched.
- The skill must use only read-only discovery commands and must not use network
  access or project commands with installation, build, migration, deployment,
  or service-start side effects.
- The generated context is a maintainer-readable document, not a replacement
  for requirements, specifications, ADRs, or task checklists.

## Data and permissions

- The skill needs read access to the repository and write access only to
  `CONTEXT.md`, including creating that file when it is absent.
- The skill may read existing `CONTEXT.md` to preserve human-authored content
  and identify conflicts.
- The skill may inspect environment templates and configuration structure, but
  must omit secret values and redact sensitive literals as `[REDACTED]`.
- Generated claims must not expose credentials, tokens, private keys, cookies,
  passwords, or complete secret-bearing connection strings.
- No application user data or external service state is changed.

## Errors and edge cases

- The repository is empty or contains no recognizable source: write the
  generated metadata and explicit `Unknown` entries rather than inventing a
  project description.
- A file is binary, generated, oversized, unreadable, or excluded by scope:
  skip its contents and record the skipped path and reason when it affects
  confidence.
- A source file contains a value that resembles a secret: omit the value,
  redact any output, and retain only safe structural information such as the
  key name or integration type.
- A generated block has malformed or missing boundary markers: do not overwrite
  ambiguous content; report a conflict and leave the existing content intact.
- A command needed for safe discovery fails: continue where possible and
  record the command and failure as an `Unknown`; do not retry with a command
  that has broader side effects.
- The same repository state is analyzed repeatedly: no duplicate generated
  section may be created and human-authored content must remain unchanged.

## Interfaces and observable test points

### Generated context block

The generated block is a Markdown section in `CONTEXT.md` with stable boundary
markers and these headings:

```markdown
## Codebase Context
<!-- phat:code-to-context:start -->

- Generated at: <ISO-8601 timestamp>
- Source revision: <commit SHA or working tree>

### Project map
### Stack and runtime
### Commands and workflows
### Entrypoints
### Module boundaries
### Data and integrations
### Tests and verification
### Deployment and operations
### Risks and unknowns
### Conflicts / Needs confirmation

<!-- phat:code-to-context:end -->
```

Material claims inside these headings use one of the explicit labels:

```text
[Observed] <claim> — Source: path/to/file:line
[Inferred] <claim> — Based on: path/to/file:line, path/to/other-file:line
[Unknown] <question or gap> — Searched: <scope or path>
```

The exact number of bullets is determined by repository evidence. Empty
headings may be retained when the category is relevant but no reliable fact is
available; the limitation must be represented as `Unknown` rather than filled
with speculation.

### Completion summary

After the write, the skill reports an observable summary containing:

- the `CONTEXT.md` action: created, generated block replaced, or not written;
- source revision metadata;
- scanned and skipped input categories;
- conflicts and unknowns;
- confirmation that no downstream skill was invoked.

### Routing point

When `ask-phat` inspects a repository with code but no reliable generated code
context, it may recommend `code-to-context` as the single next workflow step.
That recommendation does not authorize automatic execution.

## Non-functional requirements

- **Safety:** Sensitive values must not appear in `CONTEXT.md`, terminal
  summaries, or generated evidence.
- **Traceability:** Material claims must be attributable to repository paths and
  line references when useful.
- **Idempotence:** Repeated runs must not duplicate the generated block or
  change human-authored sections; freshness metadata may be refreshed.
- **Portability:** The generated artifact must be plain Markdown usable by the
  existing Phat skills and compatible AI agents.
- **Minimal side effects:** The only repository write is the generated portion
  of `CONTEXT.md`.

## Acceptance criteria

- AC-01: Given an existing repository with source, configuration, tests, or
  documentation, when the user invokes `code-to-context`, then the skill
  produces a generated `## Codebase Context` block in `CONTEXT.md` with the
  required headings and source revision metadata.
- AC-02: Given a repository without `CONTEXT.md`, when the user invokes the
  skill, then it creates `CONTEXT.md` with the repository context heading and
  one generated code-context block.
- AC-03: Given an existing `CONTEXT.md` containing human-authored sections,
  when the skill runs, then those sections remain unchanged and only the
  marked generated block is created or replaced.
- AC-04: Given material claims in the generated block, when the output is
  inspected, then each claim is labeled `Observed`, `Inferred`, or `Unknown`
  and has attributable source evidence or an explicit search gap.
- AC-05: Given code behavior conflicts with an authoritative requirement,
  accepted spec, ADR, or human-authored context, when the skill runs, then it
  preserves the authoritative content and records the mismatch under
  `Conflicts / Needs confirmation` without resolving it silently.
- AC-06: Given files or command output contain secrets or sensitive values,
  when the skill generates context and its completion summary, then the values
  are absent or replaced with `[REDACTED]` and only safe structural information
  is retained.
- AC-07: Given the repository contains excluded generated, dependency, vendor,
  build-output, or sensitive inputs, when the skill runs, then it does not use
  their contents as ordinary evidence and records material skipped areas as
  `Unknown` or skipped input information.
- AC-08: Given the same repository state is analyzed more than once, when the
  skill reruns, then it does not append duplicate generated blocks or modify
  human-authored context sections.
- AC-09: Given safe discovery commands are available or unavailable, when the
  skill runs, then it uses only read-only discovery and records command failures
  as unknowns without installing, building, migrating, deploying, or starting
  services.
- AC-10: Given a repository has code but missing or stale generated context,
  when `ask-phat` evaluates the repository, then it can recommend
  `code-to-context` as the next skill without invoking it automatically.

## Verification plan

| AC | Verification |
| --- | --- |
| AC-01 | Run the skill against a fixture repository with representative source, manifest, config, tests, CI, and docs; inspect the generated block headings, labels, and revision metadata. |
| AC-02 | Run against a fixture with no `CONTEXT.md`; verify the file and exactly one generated block are created. |
| AC-03 | Seed `CONTEXT.md` with manual sections and a prior generated block; rerun and compare manual sections before and after. |
| AC-04 | Inspect every material generated claim in the fixture output and verify its label and path/line evidence or explicit unknown reason. |
| AC-05 | Create a fixture conflict between code behavior and an authoritative context/spec statement; verify the authoritative text remains and the conflict is recorded without a chosen resolution. |
| AC-06 | Include fake token/password/private-key/connection-string values in fixture inputs; verify exact values do not occur in `CONTEXT.md`, logs, or the completion summary. |
| AC-07 | Include representative generated, dependency, vendor, build, and sensitive paths; verify they are skipped or represented as limited/unknown evidence. |
| AC-08 | Run twice against the same fixture state; verify no duplicate generated block and no manual-section diff, allowing only freshness metadata changes. |
| AC-09 | Provide safe discovery commands plus failing/side-effecting command candidates; verify only safe commands run and failures become recorded unknowns. |
| AC-10 | Evaluate `ask-phat` against a fixture with code and missing/stale context; verify it recommends `code-to-context` and does not invoke it. |

## Open questions

- **Non-blocking:** The exact heuristic for deciding that an existing generated
  context is stale can be refined during implementation using source revision,
  generated metadata, and changed-file evidence.
- **Non-blocking:** Large-repository prioritization and maximum context size can
  be tuned after observing real repositories; the first implementation must
  preserve the safety and traceability rules above.

## Delivery

Implemented and reviewed by [`TASK-003`](../tasks/TASK-003-code-to-context-skill.md)
and [`TASK-004`](../tasks/TASK-004-route-code-to-context-from-ask-phat.md), both
`done`. The standalone skill and `ask-phat` routing are now part of the
published 12-skill collection.
