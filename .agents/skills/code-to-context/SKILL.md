---
name: code-to-context
description: "Inspect an existing repository and refresh only the generated section of CONTEXT.md with attributable Observed, Inferred, and Unknown evidence. Use for onboarding, material repository-context gaps, or explicit refresh; not as a mandatory stage during ongoing implementation."
---

# Code to Context

Inspect an existing repository safely and maintain code-derived context in `CONTEXT.md`.

Derive a reviewable snapshot of current codebase facts, structure, and runtime conventions into a dedicated generated block so other Phat skills can navigate the repository without rediscovering it from scratch.

Treat implementation as evidence of what currently exists, not as agreed product or architecture intent.

When code contradicts authoritative requirements, accepted specifications, ADRs, or human-authored context, preserve the authoritative source and record the conflict.

## Contents

- [Core workflow](#core-workflow)
- [Ownership and boundaries](#ownership-and-boundaries)
- [Read authoritative context first](#read-authoritative-context-first)
- [Freshness](#freshness)
- [Safe repository discovery](#safe-repository-discovery)
- [Exclusions](#exclusions)
- [Sensitive values and secrets](#sensitive-values-and-secrets)
- [Evidence labels and attribution](#evidence-labels-and-attribution)
- [Authoritative-source comparison](#authoritative-source-comparison)
- [Determine source revision](#determine-source-revision)
- [Generated block schema](#generated-block-schema)
- [Codebase Context](#codebase-context)
- [Section intent](#section-intent)
- [Write CONTEXT.md through the bundled script](#write-contextmd-through-the-bundled-script)
- [CONTEXT.md modification behavior](#contextmd-modification-behavior)
- [Idempotence](#idempotence)
- [Completion summary](#completion-summary)

## Core workflow

Follow this sequence:

```text
Read repository guidance and authoritative context
        ↓
Discover repository safely (read-only)
        ↓
Filter excluded paths and protect sensitive values
        ↓
Extract attributable evidence and structure claims
        ↓
Compare code with authoritative sources
        ↓
Generate canonical Codebase Context block
        ↓
Use scripts/update_context.py to update CONTEXT.md safely
        ↓
Report completion summary
        ↓
Stop
```

Do not invoke downstream Phat skills automatically.

## Ownership and boundaries

Own only the generated `Codebase Context` block in `CONTEXT.md`.

The generated schema is already the repository-fact normalization layer. Do
not call `$compact-context` by default or summarize the generated block again;
use the structured output directly and keep the completion summary short.

Do not:

- modify application code, tests, configuration, CI, `AGENTS.md`, `README.md`, requirements, specs, tasks, or ADRs;
- create product, domain, or architecture decisions from code observations;
- create feature specifications or implementation tasks;
- run install, build, test, lint, migration, deployment, container startup, service startup, or other code-executing commands during discovery;
- access external services merely to discover repository context;
- expose, persist, or summarize secret values;
- rewrite or delete human-authored `CONTEXT.md` content;
- automatically continue into `$setup-project`, `$write-spec`, or another downstream skill.

## Read authoritative context first

Before discovering implementation details, read when present:

1. `AGENTS.md`;
2. `CONTEXT.md`, while distinguishing human-authored content from the generated block;
3. `docs/requirement.md`;
4. relevant files under `docs/specs/`;
5. `docs/workflow.md`;
6. relevant ADRs under `docs/adr/`;
7. the active task, linked dependencies, and available review evidence under
   `docs/tasks/` or the repository's equivalent.

Use these sources and the conversation to establish vocabulary, authoritative
constraints, and the current implementation stage before interpreting code.
Task status describes progress; it does not prove behavior or passing tests.

Do not treat older generated Codebase Context as authoritative evidence for the new snapshot.

## Freshness

Refresh when explicitly requested, or when missing/incorrect repository facts
require onboarding or material synchronization. An absent generated block is
not a mandatory prerequisite for a project already progressing through tasks.

`Source revision` and `Generated at` identify the inspected snapshot; they are
not validity gates. A changed `HEAD`, dirty working tree, routine implementation,
or the commit that saves `CONTEXT.md` alone does not establish material staleness.
Compare relevant current manifests, structure, entrypoints, configuration, and
claims. If an earlier revision is unavailable or its uncommitted state cannot
be reconstructed, inspect current evidence and record the comparison limitation
instead of assuming every claim is stale. Never include changes to the generated
block itself as evidence that another refresh is required.

Do not treat human-authored context as stale merely because implementation
changed. Refresh only the generated block owned by this skill.

## Safe repository discovery

Use read-only inspection mechanisms.

### Permitted discovery

Examples include:

- filesystem inspection: `ls`, `find`, `cat`, `head`, `tail`, `grep`, `rg`, or equivalent read tools;
- Git reads: `git status --porcelain`, `git rev-parse HEAD`, `git log -n <N>`, `git diff --stat`;
- manifests and configuration such as `package.json`, `pnpm-workspace.yaml`, `Cargo.toml`, `go.mod`, `pyproject.toml`, `Makefile`, `Taskfile.yml`, `Dockerfile`, `.github/workflows/`, and `.gitlab-ci.yml`;
- relevant source and test files needed to identify entrypoints, module boundaries, integrations, and verification structure.

Prefer targeted inspection over reading the entire repository.

### Prohibited discovery

Do not run commands that install dependencies, execute project code, mutate state, or contact external services merely for discovery.

Examples include:

- `npm install`, `yarn install`, `pnpm install`, `pip install`, `cargo fetch`;
- `npm run build`, `make`, `cargo build`, `go build`;
- `npm test`, `pytest`, `cargo test`, `go test`;
- migrations, seed commands, deployment commands, container runs, or background daemons;
- network package downloads or external API calls.

If a safe discovery command fails, do not broaden into side-effecting commands. Record the gap as `[Unknown]` under `### Risks and unknowns`.

## Exclusions

Do not read file bodies or treat their contents as ordinary codebase evidence in these categories unless a narrower rule below explicitly permits it.

### Dependencies and vendor content

Exclude:

- `node_modules/`;
- `vendor/`;
- `.venv/`, `venv/`;
- `packages/*/node_modules/`;
- `bower_components/`.

Structural presence may be recorded as `[Observed]` without inspecting internal files.

### Generated and build artifacts

Exclude:

- `dist/`, `build/`, `out/`, `target/`, `.next/`;
- `bin/`, `obj/` when they are generated outputs;
- `*.pyc`, `*.class`;
- `.cache/`, `.turbo/`, `.parcel-cache/`;
- `.git/` internal objects;
- `coverage/`, `.nyc_output/`, `test-results/`.

### Binary, media, minified, and oversized content

Exclude bodies of:

- `*.min.js`, `*.min.css`, `*.map`;
- images, PDFs, WASM, executables, archives, and other binary files;
- files larger than 500 KB when they are obviously generated or not necessary for context discovery.

Lockfiles may be inspected only narrowly when needed to identify package manager or dependency resolution facts. Do not dump complete lockfile contents into context.

## Sensitive values and secrets

Never record secret values in `CONTEXT.md` or the completion summary.

Do not inspect live secret files such as:

- `.env`, `.env.local`, `.env.production`, or equivalent live environment files;
- `*.pem`, `*.key`, `id_rsa`;
- credential exports, service-account secrets, private key files, or secret vault contents.

For safe templates such as `.env.example`, record only variable names or safe structural information. Never reproduce example values that resemble credentials.

If an otherwise relevant file contains a token, password, private key, cookie, credential, or secret-bearing connection string:

- omit the value;
- use `[REDACTED]` only when a placeholder is needed to explain structure;
- retain only safe information such as integration type, variable name, or authentication mechanism.

## Evidence labels and attribution

Every material claim in the generated block must carry one of these labels.

### Observed

Use for facts directly verified from safe inspection.

For file-backed evidence:

```text
[Observed] <claim> — Source: <relative-path>:<line-or-range>
```

For repository metadata or filesystem structure:

```text
[Observed] <claim> — Source: command `<safe-command>`
```

Examples:

```text
[Observed] The web package uses Next.js. — Source: apps/web/package.json:18-32
[Observed] The repository contains apps/web and packages/ui. — Source: command `find . -maxdepth 2 -type d`
```

Never invent a line number for command-derived evidence.

### Inferred

Use only for a deduction supported by one or more observed facts.

```text
[Inferred] <claim> — Based on: <source>, <source>
```

Keep inference conservative. Do not turn an inference into a product or architecture decision.

### Unknown

Use when safe inspection cannot determine a material fact.

```text
[Unknown] <question or gap> — Searched: <scope, path, pattern, or failed safe command>
```

If a category contains no verifiable information, prefer one meaningful `[Unknown]` entry over invented filler. Distinguish "not found in the inspected scope" from "does not exist." An unknown is not automatically a defect, missing requirement, or recommendation to add infrastructure.

## Authoritative-source comparison

Compare implementation evidence against relevant human-authored requirements, accepted specs, ADRs, and context.

Account for implementation progress before declaring a disagreement. Behavior
still planned in a `todo` or `in_progress` task is expected incomplete work,
not by itself a conflict requiring a new decision. Record the current behavior
and link the owning task in the relevant schema section. A directly contradictory
implementation choice remains a conflict even during an open task. If delivery
status is unclear, record the uncertainty instead of asserting noncompliance.
Do not claim checks passed merely because scripts or tests exist, and do not
turn uninspected deployment/security/test areas into an unsolicited backlog.

Do not silently resolve disagreements.

When a conflict exists, preserve both sides and record it under `### Conflicts / Needs confirmation`.

Use this shape:

```markdown
- [Observed] Conflict: <short description>
  - Authoritative: <statement> — Source: <path>:<line-or-range>
  - Implementation: <observed behavior> — Source: <path>:<line-or-range>
  - Status: Maintainer confirmation required
```

Do not use `[Inferred]` to declare which side is correct.

## Determine source revision

When inside a Git worktree:

1. run `git rev-parse HEAD`;
2. run `git status --porcelain`.

Record:

```text
<SHA>
```

when clean, or:

```text
<SHA> (working tree with uncommitted changes)
```

when dirty.

When the directory is not a Git repository, record:

```text
unversioned directory
```

If revision discovery fails unexpectedly, record the limitation under `### Risks and unknowns` rather than substituting a guessed value.

## Generated block schema

Generate exactly one canonical block using this structure:

```markdown
## Codebase Context

<!-- phat:code-to-context:start -->

> Generated from repository inspection. This section describes observed implementation state and must not be interpreted as agreed product or architecture intent.

- Generated at: <ISO-8601 UTC timestamp>
- Source revision: <revision>

### Project map

- [Observed] ... — Source: ...

### Stack and runtime

- [Observed] ... — Source: ...

### Commands and workflows

- [Observed] ... — Source: ...

### Entrypoints

- [Observed] ... — Source: ...

### Module boundaries

- [Observed] ... — Source: ...

### Data and integrations

- [Observed] ... — Source: ...

### Tests and verification

- [Observed] ... — Source: ...

### Deployment and operations

- [Observed] ... — Source: ...

### Risks and unknowns

- [Unknown] ... — Searched: ...

### Conflicts / Needs confirmation

- None observed from inspected authoritative sources and code.

<!-- phat:code-to-context:end -->
```

Use UTC for `Generated at`.

Replace `- None observed...` with structured conflicts when any exist.

Do not include a section outside this schema inside the generated block.

## Section intent

Use sections as follows:

- `Project map`: top-level structure, primary packages, workspace layout;
- `Stack and runtime`: languages, frameworks, runtime versions, package managers, engine constraints;
- `Commands and workflows`: verified scripts and commands defined by repository files;
- `Entrypoints`: servers, binaries, CLIs, route roots, primary exports;
- `Module boundaries`: internal packages, layers, submodules, workspace packages;
- `Data and integrations`: databases, external APIs, SDKs, storage, queues, brokers;
- `Tests and verification`: test frameworks, test locations, linters, typecheckers, CI verification jobs;
- `Deployment and operations`: Docker, serverless, deployment, infrastructure and runtime operation configuration;
- `Risks and unknowns`: material gaps, unreadable/uninspected areas, failed safe discovery;
- `Conflicts / Needs confirmation`: implementation conflicts with authoritative sources.

Prefer concise, navigational facts over exhaustive inventories.

## Write CONTEXT.md through the bundled script

Do not rewrite `CONTEXT.md` manually.

After generating the complete canonical block, save it to a temporary Markdown file outside the repository when practical, then run:

```text
python <skill-directory>/scripts/update_context.py \
  --context CONTEXT.md \
  --generated-block <temporary-generated-block.md>
```

The script is the authority for marker validation and safe replacement.

Inspect its structured output and report the exact action it returns.

Delete the temporary generated-block file when practical.

## CONTEXT.md modification behavior

The bundled script enforces these cases.

### Missing CONTEXT.md

Create:

```markdown
# Repository context

<generated Codebase Context block>
```

### Existing valid marked block

Replace only the canonical `## Codebase Context` section associated with exactly one start and one end marker.

Preserve all bytes before and after the replaced section.

### Existing file without Codebase Context

Append the canonical generated section while preserving all existing content.

### Existing unmarked Codebase Context

Treat it as human-authored.

Do not overwrite it and do not append a competing duplicate.

Report `not written` with the conflict reason.

### Malformed or ambiguous markers

If markers are missing, duplicated, reversed, nested, detached from the heading, or otherwise ambiguous, leave the file unchanged and report `not written`.

Do not repair ambiguous human content automatically.

## Idempotence

Running this skill repeatedly on an unchanged repository must:

- update only the generated block and its snapshot metadata;
- avoid duplicate headings and markers;
- preserve human-authored content;
- avoid changing product or architecture intent.

The timestamp may change between runs.

## Completion summary

After the script runs, report concisely:

1. `CONTEXT.md` action: `created`, `generated block replaced`, `generated block appended`, or `not written (<reason>)`;
2. source revision;
3. scanned input categories;
4. skipped categories, including secret-bearing and excluded paths;
5. conflicts recorded;
6. major unknowns;
7. the pending task or workflow stage from the incoming request, if known,
   with any still-material blocker; otherwise say the next stage was not assessed;
8. confirmation that no downstream skill was invoked.

Do not invent a roadmap or automatically recommend `$ask-workflow`, setup, or
another refresh. Returning repository evidence completes this skill; resume
information preserves the incoming scope without selecting a new workflow.
For `not written`, explain the exact cause and what must change before retrying.
Do not include secret values in the summary.

Stop after this report.
