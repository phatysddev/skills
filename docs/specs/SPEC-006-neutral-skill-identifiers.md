# SPEC-006: Neutral skill identifiers

- Status: done
- Requirement: [docs/requirement.md](../requirement.md)
- Context: [CONTEXT.md](../../CONTEXT.md)
- ADRs: None

## Problem and outcome

The published skill pack uses `phat` in five installable skill identifiers.
The identifiers expose an internal brand term rather than the responsibility
of each workflow skill, which makes the catalog less portable and less clear
when the skills are used outside the original project context.

The outcome is a breaking, traceable rename to responsibility-based skill
identifiers while preserving the Phat/Phatysd terminology in project
documentation and public knowledge-source references.

## Agreed decisions

The following decisions were explicitly confirmed during grilling:

| Current identifier | New identifier | Decision state |
| --- | --- | --- |
| `ask-phat` | `ask-workflow` | Agreed |
| `grill-with-phat` | `grill-workflow` | Agreed |
| `setup-phat-project` | `setup-project` | Agreed |
| `to-spec-with-phat` | `write-spec` | Agreed |
| `review-with-phat` | `code-review` | Agreed |

`to-tasks`, `implement-task`, `code-to-context`, `compact-context`,
`to-prototype`, `edit-prototype`, `spec-with-prototype`, and `setup-template`
retain their current identifiers.

## In scope

- Replace the five current identifiers with the agreed new identifiers in the
  published skill catalog.
- Make each renamed skill's public identity use the new identifier, including
  its discoverable source path and required `name` frontmatter.
- Update maintained workflow, catalog, installation, handoff, and interface
  references so they point to the new identifiers.
- Preserve the existing skill instructions, decision rules, research behavior,
  handoffs, and public content URLs unless a reference must change because of
  the identifier rename.
- Publish a migration map from every old identifier to its new identifier and
  state clearly that the rename is breaking.
- Keep the terms `Phat`, `Phat workflow`, and `Phatysd` in explanatory project
  and knowledge-site content where they describe the product, workflow, or
  source rather than an installable identifier.

## Out of scope

- Renaming the Phat/Phatysd product, workflow, repository, GitLab project, or
  `docs.phatysd.me` URLs.
- Changing the responsibilities, prompts, decision contracts, or behavior of
  any skill.
- Adding compatibility aliases, redirect skills, duplicate directories, or
  fallback installation names for the old identifiers.
- Renaming skill identifiers that do not contain `phat`.
- Changing the `skills` CLI, its external installation policy, or the public
  GitLab hosting location.
- Decomposing the rename into implementation tasks; that belongs to
  `$to-tasks` after this specification.

## User flow and behavior

### Primary flow: maintainer publishes the renamed catalog

1. A maintainer reads the migration map and the agreed identifier mapping.
2. The source repository exposes the five renamed skills under their new
   identifiers.
3. A user or agent discovers the catalog and sees the new identifiers rather
   than the old identifiers as installable choices.
4. The user installs or invokes a renamed skill using its new identifier.
5. The skill behaves according to its existing instructions; only the public
   identifier and references to that identifier have changed.

### Alternate flow: a user has an old reference

- The migration map identifies the replacement identifier and explicitly marks
  the old identifier as retired.
- The old identifier is not advertised as an alias and is not required to
  install or invoke a compatibility wrapper.
- Maintained repository references are updated so new workflow guidance does
  not continue sending users to the retired identifier.

### No-change flow

- A skill whose identifier does not contain `phat` remains discoverable under
  its existing identifier.
- Explanatory prose may continue to mention the Phat workflow or Phatysd docs
  when that terminology is describing the product or source, not a skill ID.

## Business rules and constraints

- The mapping is one-to-one: each retired identifier has exactly one new
  identifier, and no two current skills share a new identifier.
- The rename is breaking. The old identifiers are not compatibility aliases.
- Public identifier changes must be traceable through a migration map and
  consistent across the catalog, frontmatter, installation guidance, and
  workflow handoffs.
- Skill behavior is authoritative in each renamed skill's existing
  `SKILL.md`; identifier work must not silently rewrite that behavior.
- The complete catalog remains a 13-skill catalog after the rename.
- The source-of-truth boundaries in [AGENTS.md](../../AGENTS.md),
  [docs/requirement.md](../requirement.md), and [CONTEXT.md](../../CONTEXT.md)
  remain authoritative for repository vocabulary and distribution behavior.

## Data and permissions

- The change affects public repository files, installable identifiers, and
  documentation references only.
- No application user data, credentials, private project data, or external
  service state is read or changed.
- The public GitLab source and Phatysd knowledge site remain external links;
  this change does not publish to or authenticate against either service.

## Errors and edge cases

- A stale maintained reference to a retired identifier is a migration defect
  and must be corrected before the rename is considered complete.
- If a new identifier collides with an existing skill identifier, the catalog
  must not publish an ambiguous result; the conflict is blocking and must be
  resolved before implementation can be marked complete.
- Historical records may mention retired identifiers when they document the
  previous contract, but current installation and workflow guidance must point
  to the new identifiers.
- If the public skill listing cannot verify the new identifiers after
  publication, the result is incomplete even if local files look correct.
- A renamed skill with invalid or missing `name` frontmatter is not a valid
  published skill and must not be treated as successfully migrated.

## Interfaces and observable test points

- The source tree exposes the five agreed new skill identifiers.
- Each renamed `SKILL.md` declares its new identifier in YAML frontmatter.
- The public catalog and installation examples expose the new identifiers.
- Workflow handoff references use the new identifiers, including UI metadata
  and user-facing skill invocation examples.
- A migration map exposes the complete old-to-new mapping and the breaking
  compatibility rule.
- The eight unaffected skill identifiers remain unchanged.
- The renamed skills retain their prior instruction content and behavior aside
  from identifier/reference updates.

## Non-functional requirements

- **Traceability:** every retired identifier maps to one new identifier and the
  mapping is preserved in a public repository document.
- **Consistency:** source paths, frontmatter, catalog entries, handoffs, and
  installation guidance cannot disagree about a renamed identifier.
- **Idempotence:** repeating the catalog/reference update must not create
  duplicate skills, duplicate aliases, or repeated migration entries.
- **Compatibility clarity:** the published documentation must state that this
  is a breaking rename and must not imply that old identifiers still work.

## Acceptance criteria

- AC-01: Given the current 13-skill catalog, when the rename is applied, then
  the five identifiers are replaced one-to-one by `ask-workflow`,
  `grill-workflow`, `setup-project`, `write-spec`, and `code-review`, while the
  eight unaffected identifiers remain unchanged.
- AC-02: Given any renamed skill source, when its public identity is inspected,
  then its source path and required `name` frontmatter use the new identifier
  and the frontmatter remains valid.
- AC-03: Given maintained README, workflow, installation, handoff, and
  interface references, when they are inspected after the rename, then they
  point to the new identifiers and do not direct current users to retired
  identifiers.
- AC-04: Given the migration documentation, when a user looks up any retired
  identifier, then it finds exactly one replacement and an explicit breaking
  rename notice, with no compatibility alias promised.
- AC-05: Given the published skill listing, when a user discovers or selects a
  renamed skill, then the new identifier is listed and usable, while the old
  identifier is not advertised as an installable alias.
- AC-06: Given the renamed skill instructions, when they are compared with the
  pre-rename contract, then responsibilities, behavior, research rules,
  decision contracts, and workflow handoffs remain unchanged except for the
  identifier/reference updates required by this spec.
- AC-07: Given the repository still uses product or source terminology, when
  explanatory prose is inspected, then `Phat`, `Phat workflow`, `Phatysd`, and
  `docs.phatysd.me` remain available where they describe the product, workflow,
  or external source rather than an installable skill ID.
- AC-08: Given the repository and published listing are checked after the
  rename, when the complete catalog is counted, then exactly 13 discoverable
  skills exist and no duplicate new identifier or retired alias exists.

## Verification plan

| AC | Verification |
| --- | --- |
| AC-01 | Enumerate `.agents/skills/` and compare the identifiers with the agreed 13-skill mapping. |
| AC-02 | Parse every renamed `SKILL.md` frontmatter and verify `name`, path, and required fields. |
| AC-03 | Search maintained README, AGENTS, CONTEXT, workflow, specs, tasks, skill instructions, and `agents/openai.yaml` references; inspect remaining retired names and classify only migration/history mentions as allowed. |
| AC-04 | Inspect the migration map for all five retired identifiers, one replacement each, and the explicit breaking rule. |
| AC-05 | Run the published skill listing and selected-install checks against the GitLab source after publication; verify new IDs are discoverable and old IDs are not advertised. |
| AC-06 | Compare the renamed `SKILL.md` bodies and interface metadata against the pre-rename versions, excluding intentional identifier/reference substitutions. |
| AC-07 | Search explanatory prose and external URLs to verify brand/source terminology was preserved where required. |
| AC-08 | Count the published catalog and run duplicate/alias checks; verify `git diff --check` and the repository's available static validation. |

## Open questions

- **Non-blocking:** The migration map's exact filename and section location can
  be chosen during task planning as long as it is public, discoverable, and
  linked from the catalog guidance.
