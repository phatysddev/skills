# SPEC-003: Compact context utility and skill-pack composition

- Status: done
- Requirement: [docs/requirement.md](../requirement.md)
- Context: [CONTEXT.md](../../CONTEXT.md)
- Workflow: [docs/workflow.md](../workflow.md)
- ADRs: None

## Problem and outcome

Intermediate handoffs can contain repetitive conversation, multilingual
discussion, and duplicated rationale. The compact-context utility reduces that
temporary context without weakening the canonical requirements, specs, tasks, or
repository evidence that downstream skills must read.

The skill pack also needs explicit composition rules so brownfield discovery,
setup, workflow handoffs, and public documentation do not duplicate work or
treat a utility as a project-state transition.

## In scope

- Keep compact-context as a short, model-invoked utility skill for temporary
  agent-facing handoffs.
- Preserve decisions, facts, constraints, scope, exact identifiers, references,
  acceptance criteria, open questions, conflicts, and status/dependency facts.
- Remove only semantic redundancy and normalize intermediate prose to concise
  English when safe.
- Let grill-with-phat use compact-context conditionally before reporting
  setup-phat-project.
- Route existing repositories with missing or stale generated Codebase Context
  to code-to-context before setup-phat-project.
- Reuse a fresh generated Codebase Context during setup and inspect source only
  for gaps or verification.
- Keep compact-context out of the ask-phat primary route and out of canonical
  spec/task/review handoffs.
- Document workflow, catalog, current feature status, and Git commit policy for
  the complete 12-skill collection.

## Out of scope

- Replacing or rewriting canonical project documents with compacted output.
- Automatically invoking another workflow stage from compact-context.
- Summarizing a canonical spec before task decomposition or review.
- Adding product application behavior.
- Changing the existing code-to-context generated schema.

## User flow and behavior

### Conditional grill handoff

When confirmed decisions are materially verbose or multilingual:

1. grill-with-phat prepares the confirmed-decision summary.
2. compact-context produces a temporary loss-aware handoff.
3. grill-with-phat reports setup-phat-project as the next explicit workflow
   skill without invoking it.

If the summary is already concise, the utility is skipped.

### Brownfield precedence

For a repository with meaningful code or configuration:

1. ask-phat checks the generated Codebase Context.
2. Missing or stale context routes to code-to-context.
3. Fresh context is reused by setup-phat-project.
4. Setup inspects source, manifests, and commands only for required gaps.

### Canonical artifact rule

to-tasks, implement-task, and review-with-phat read their canonical spec/task
inputs in full. compact-context may reduce temporary notes only after those
sources remain available.

## Business rules and constraints

- Utility output is ephemeral unless a parent explicitly requests a separate
  non-canonical summary.
- A proposal remains a proposal; compaction never resolves decisions or
  conflicts.
- Exact paths, IDs, commands, URLs, interfaces, status values, and AC meanings
  remain unchanged.
- User-facing copy, legal text, and exact quotes are not compacted by default.
- Code-to-context does not call compact-context by default because its generated
  schema already normalizes repository facts.
- Implement-task creates a commit only when repository policy or explicit user
  instructions require it; otherwise a focused working-tree diff is reviewable.
- The public catalog and repository docs describe all 12 skills by category.

## Acceptance criteria

- AC-01: compact-context has valid frontmatter, remains model-invoked, and its
  SKILL.md is no longer than 180 lines.
- AC-02: The utility preserves the goal, confirmed decisions, facts,
  constraints, scope, exact identifiers, references, acceptance criteria,
  open questions, conflicts, and status/dependency facts.
- AC-03: The utility removes only semantic redundancy, uses concise English when
  safe, and leaves user-facing copy and exact technical identifiers unchanged.
- AC-04: The utility never replaces canonical documents, routes the project, or
  substitutes for full canonical reads.
- AC-05: grill-with-phat conditionally points to compact-context only for a
  materially verbose or multilingual temporary handoff.
- AC-06: ask-phat gives code-to-context precedence over setup for meaningful code
  with missing or stale generated context.
- AC-07: setup-phat-project reuses fresh generated Codebase Context and routes
  missing/stale context back to code-to-context before broad discovery.
- AC-08: code-to-context does not call compact-context by default.
- AC-09: implement-task follows repository/user Git policy instead of requiring
  an automatic commit in every Git worktree.
- AC-10: README, AGENTS.md, CONTEXT.md, docs/requirement.md, and docs/workflow.md
  describe the current 12-skill categories and completed SPEC-002 state.
- AC-11: SPEC-003 and TASK-005 through TASK-007 record the compact utility,
  integrations, catalog, and verification evidence.

## Verification plan

| AC | Verification |
| --- | --- |
| AC-01 | Validate frontmatter and count compact-context SKILL.md lines. |
| AC-02–AC-04 | Inspect the utility rules and confirm preserve/remove/canonical-source boundaries are explicit. |
| AC-05–AC-08 | Inspect grill, ask, setup, workflow, and code-to-context instructions for the stated conditional routing and no-duplication rules. |
| AC-09 | Search implement-task and its implementation reference for conditional commit language and run repository policy checks. |
| AC-10–AC-11 | Search all catalog/status docs, verify links, task/spec inventory, and run git diff --check. |

## Delivery

Implemented in the current worktree by TASK-005, TASK-006, and TASK-007.
No repository-local test runner exists; static validation, link checks, line
counts, frontmatter checks, and git diff --check provide the available evidence.
