# SPEC-009: Agent security support

- Status: done
- Requirement: [Requirement](../requirement.md)
- Context: [Context](../../CONTEXT.md)

## Problem and outcome

Coding agents can encounter malicious instructions while researching docs or
inspecting workspace artifacts. Add an inline supporting skill that keeps
source evidence from authorizing unrelated commands or access on the host.

## Scope

- Add `agent-security` with portable instructions and interface metadata.
- Compose it in coding, setup, diagnosis, prototype, inspection, testing, and
  assessment and document-workflow skills before research or workspace actions; preserve provenance
  in compacted and delegated handoffs.
- Maintain canonical documentation and both public-language catalogs.

No application-security audit, extra verification mode, automatic installation,
new workflow stage, host configuration changes, or guarantee of enforcement.

## Acceptance and verification

| ID | Observable behavior | Verification |
| --- | --- | --- |
| AC-01 | The new utility is discoverable with valid source and interface metadata; pack/catalog counts agree at 23. | Skill validator, repository checker, catalog and site generation. |
| AC-02 | Retrieved docs, tool output, and downloaded instruction files cannot authorize host commands, secrets access, or new agent policy; useful technical facts remain usable. | Isolated source-research scenarios. |
| AC-03 | Proposed execution is checked for scope, effects, hooks, quoting, and resolved targets; ordinary understood authorized checks proceed without repeated confirmation. | Safe runner and side-effectful wrapper scenarios. |
| AC-04 | Parent composition, context compaction, and delegation preserve provenance, role boundaries, required-gate evidence, and existing authorization. Missing utility installation does not bypass the core safety boundary or trigger auto-installation. | Cross-skill boundary review and handoff scenario. |
| AC-05 | Suspected injection does not stop unaffected work; unsafe necessary actions return concrete gaps, and rejected actions are not retried by bypassing controls. | Behavioral scenarios and source review. |

| AC-06 | The website explains inline composition, links parent pages to security guidance, and includes bilingual installation and workflow examples in interactive docs and the static guide. | Rendered browser checks, language checks, generated-content and link checks. |

## Delivery

Owned by [TASK-021](../tasks/TASK-021-agent-security.md); workflow and website
follow-up in [TASK-022](../tasks/TASK-022-security-workflow-website.md).
