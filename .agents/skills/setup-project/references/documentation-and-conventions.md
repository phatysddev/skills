# Setup reference: durable documents and conventions

Use this reference when creating or updating `AGENTS.md`, `CONTEXT.md`,
`docs/requirement.md`, `docs/workflow.md`, ADRs, or repository command and
source-of-truth guidance.

## Contents

- [Minimum project structure](#minimum-project-structure)
- [AGENTS.md](#agentsmd)
- [Project context](#project-context)
- [CONTEXT.md](#contextmd)
- [docs/requirement.md](#docsrequirementmd)
- [Architecture decisions](#architecture-decisions)
- [docs/workflow.md](#docsworkflowmd)
- [Source-of-truth rules](#source-of-truth-rules)
- [Commands and repository conventions](#commands-and-repository-conventions)
- [Branch, commit, and review policy](#branch-commit-and-review-policy)
- [Small and medium project rule](#small-and-medium-project-rule)

## Minimum project structure

Use local Markdown as the default durable record store unless the repository already has an established documentation system.

Create or update only what is actually useful.

The default structure is:

```text
AGENTS.md
CONTEXT.md

docs/
├── requirement.md
└── workflow.md

docs/assets/prototype/  # only when a prototype exists or is being created
```

Additional artifacts use:

```text
docs/adr/NNNN-<decision>.md
docs/specs/SPEC-###-<feature>.md
docs/tasks/TASK-###-<slice>.md
```

Do not create `docs/adr/`, `docs/specs/`, or `docs/tasks/` simply because they may be useful someday.

Create those directories only when:

* an artifact of that type is being created now; or
* the repository already uses that structure.

Do not create empty placeholder documents.

Do not create documents solely to satisfy a template.

## AGENTS.md

Use `AGENTS.md` as the navigation and working-rules entry point for agents.

Record only durable repository guidance such as:

* important commands;
* package manager;
* test commands;
* lint/type-check commands;
* build commands;
* repository structure;
* coding conventions;
* documentation locations;
* workflow navigation;
* branch/review rules when known.

Prefer links to deeper documents instead of copying their content.

For example:

```markdown
## Project context

- Product requirements: `docs/requirement.md`
- Domain context: `CONTEXT.md`
- Workflow: `docs/workflow.md`
- Architecture decisions: `docs/adr/`
- Feature specs: `docs/specs/`
- Tasks: `docs/tasks/`
- Prototype assets: `docs/assets/prototype/` when present
```

Do not place product rationale, domain documentation, or feature requirements directly into `AGENTS.md` unless they are genuinely agent working rules.

## Project context

Prefer links to deeper documents instead of copying their content. A typical
navigation block is:

```markdown
## Project context

- Product requirements: `docs/requirement.md`
- Domain context: `CONTEXT.md`
- Workflow: `docs/workflow.md`
- Architecture decisions: `docs/adr/`
- Feature specs: `docs/specs/`
- Tasks: `docs/tasks/`
- Prototype assets: `docs/assets/prototype/` when present
```

Do not place product rationale, domain documentation, or feature requirements
directly into `AGENTS.md` unless they are genuinely agent working rules.

## CONTEXT.md

Use `CONTEXT.md` for durable domain understanding.

Include only established information such as:

* domain vocabulary;
* important entities;
* relationships;
* ownership;
* invariants;
* business rules;
* terminology that must remain consistent.

Keep unresolved domain questions explicitly marked.

Do not use `CONTEXT.md` as a feature backlog or architecture dump.

Do not duplicate detailed product requirements that already belong in `docs/requirement.md`.

## docs/requirement.md

Use `docs/requirement.md` as the project-level product source of truth.

When known, record:

* problem;
* target users;
* desired outcome;
* success indicators;
* project scope;
* out-of-scope boundaries;
* major constraints;
* relevant product-level requirements.

For unresolved information, use an explicit section such as:

```markdown
## Open questions

- Pending: ...
```

Do not invent details to make the document look complete.

Do not put feature-specific implementation plans here.

## Architecture decisions

Create an ADR only for a meaningful decision that benefits from durable rationale.

Examples may include:

* framework choice;
* database choice;
* authentication model;
* deployment architecture;
* multi-tenancy model;
* significant integration strategy.

Use:

```text
docs/adr/NNNN-<decision>.md
```

Do not create ADRs for trivial implementation details.

Do not create retrospective rationale for a decision unless the decision and rationale are actually known.

If the decision is unresolved, send it to `$grill-workflow` instead.

## docs/workflow.md

Create `docs/workflow.md` when workflow conventions are not already documented somewhere authoritative.

Record the shared Phat workflow contract:

```text
requirement
    ├─ optional prototype → edit-prototype* → spec reconciliation
    └─ spec
    ↓
task
    ↓
implementation
    ↓
review evidence
```

Use the following default states unless the repository already has an established equivalent:

```text
todo
    ↓
in_progress
    ↓
in_review
    ↓
done
```

Use:

```text
blocked
```

when work cannot continue.

A blocked task must record:

* blocker;
* reason;
* unblock condition.

Also record these rules:

* a spec with material blocking questions is not ready for implementation;
* scope changes must update the owning source of truth;
* do not rewrite requirements or specs merely to make them match existing code;
* start project context reading at `AGENTS.md`;
* follow links from `AGENTS.md` instead of reading every project document;
* tasks must contain enough context to continue in a new chat;
* agreed decisions must have one authoritative source of truth;
* link to decisions instead of duplicating rationale across documents.
* prototype files are visual artifacts; accepted behavior must be reconciled
  into the owning spec before task decomposition.

If the repository already has equivalent workflow documentation, preserve it rather than creating a competing `docs/workflow.md`.

## Source-of-truth rules

Prefer one authoritative location for each type of information.

Default ownership:

```text
Product intent
→ docs/requirement.md

Domain knowledge
→ CONTEXT.md

Architecture decisions
→ docs/adr/

Feature behavior
→ docs/specs/

Execution slices
→ docs/tasks/

Agent working rules and navigation
→ AGENTS.md
```

Link across documents instead of copying large sections.

When information belongs to multiple concerns, choose the most authoritative owner and reference it elsewhere.

Do not allow multiple files to silently become competing sources of truth.

## Commands and repository conventions

Record commands only when they are supported by repository evidence.

For example:

```text
pnpm test
pnpm lint
pnpm typecheck
pnpm build
```

Do not invent commands based solely on common ecosystem conventions.

If the repository contains no command for an important operation, record it as unknown rather than fabricating one.

Do not replace the user's existing package manager, framework, formatting rules, or testing setup without an agreed decision.

## Branch, commit, and review policy

Record what the repository actually requires.

If an existing policy exists, preserve it.

If no policy exists, use this conservative default:

* prepare reviewable changes;
* do not push automatically;
* do not commit automatically unless the user or repository policy asks for it;
* keep changes scoped to the current workflow;
* preserve unrelated user changes.

Do not introduce elaborate Git workflow rules to a small project without a requirement.

## Small and medium project rule

Optimize for the minimum durable context needed to work safely.

Do not introduce unnecessary process such as:

* large documentation hierarchies;
* enterprise governance documents;
* speculative ADRs;
* architecture catalogs;
* empty roadmap structures;
* unused task trees.

A landing page and a multi-user booking application do not need the same amount of project documentation.

Add structure only when project complexity creates a real need for it.
