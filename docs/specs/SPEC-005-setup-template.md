# SPEC-005: Set up a project design direction from published templates

- Status: ready
- Requirement: [docs/requirement.md](../requirement.md)
- Context: [CONTEXT.md](../../CONTEXT.md)
- ADRs: None

## Problem and outcome

`setup-project` establishes project context, but the workflow has no
bounded capability for selecting a reusable visual direction from the published
Phatysd template library. Agents may otherwise choose a style without direct
evidence, persist a design decision before the user agrees, or make downstream
prototype and specification work rediscover the same template.

The outcome is a `setup-template` workflow skill that reads prepared project
context, researches published templates, recommends one evidence-backed design
direction, waits for explicit confirmation, and persists the confirmed
direction for downstream Phat skills.

## In scope

- Run after `setup-project` has prepared project context when the project
  explicitly needs a reusable published visual direction.
- Discover published template candidates through the Phatysd public discovery
  path and retrieve their canonical, Markdown, or JSON representations.
- Match candidates against project evidence and recommend exactly one template
  with traceable supporting evidence.
- Keep the recommendation in a proposal state until the user explicitly
  confirms it.
- Persist a confirmed template direction in a dedicated `## Design Direction`
  section in `CONTEXT.md`.
- Preserve an existing design direction and expose conflicts before any
  replacement.
- Represent unavailable, incomplete, or inconclusive research as `Research
  needed` or `Open question` without inventing a direction.
- Recommend the existing next workflow skill based on visual-validation intent.

## Out of scope

- Generating or editing production code.
- Creating or editing a prototype automatically.
- Replacing `to-prototype`, `edit-prototype`, `spec-with-prototype`, or
  `write-spec`.
- Publishing, editing, or authenticating against `docs.phatysd.me`.
- Reading drafts or archived external content.
- Building a crawler, cache, synchronization job, or external runtime service.
- Automatically invoking a downstream skill in the same turn.
- Creating implementation tasks.

## User flow and behavior

### Primary flow

1. The user invokes `setup-template` after project context is prepared.
2. The skill reads `AGENTS.md`, `docs/requirement.md`, `CONTEXT.md`, relevant
   accepted specifications, and relevant ADRs when present. It treats local
   project sources and explicit user decisions as authoritative.
3. The skill checks the published Phatysd discovery path, starting with
   `https://docs.phatysd.me/llms.txt`, and narrows candidates through the
   published Templates collection, search, hierarchy, or docs pages as needed.
4. The skill accepts only candidates identified as `type: template` with
   `status: published` and retrieves a canonical page plus the available
   Markdown or JSON representation. JSON is preferred for structured template
   fields; Markdown is preferred for text-first authored guidance.
5. The skill evaluates candidate fit using evidence from the project and the
   published template:
   - applicability and use cases against the project's goal, users, and scope;
   - component set against known user flows and product surfaces;
   - constraints against accessibility, responsiveness, and other agreed
     product constraints;
   - mood, tone, visual style, typography, and animation principles against
     the requested visual direction; and
   - topics, tags, hierarchy, tokens, and examples as supporting evidence or
     tie-breakers, never as the sole proof of domain fit.
6. The skill recommends exactly one best-fit candidate and shows its title,
   slug, canonical URL, revision, freshness fields, relevant profile fields,
   tokens, examples, and the evidence used for the match. The recommendation
   is a `Proposal` until the user confirms it.
7. The skill asks the user to confirm or reject the recommendation. It does
   not update `CONTEXT.md` while the recommendation is only a proposal.
8. After explicit confirmation, the skill creates or updates the dedicated
   `## Design Direction` section in `CONTEXT.md` using the persisted contract
   described in [Persisted direction](#persisted-direction). It records the
   direction as `Agreed` and retains the published source metadata.
9. The skill reports exactly one next workflow recommendation based on the
   existing visual-validation intent: `$to-prototype` when visual validation
  is requested, otherwise `$write-spec`. It does not invoke that skill
   automatically.

### Alternate flows

- **No suitable candidate:** The skill reports that no published template is a
  sufficiently supported match, leaves any existing direction unchanged, and
  records the result as `Research needed` or `Open question`. It does not
  substitute a generic or unpublished style.
- **External research unavailable:** If discovery, retrieval, or the required
  representation fails, the skill reports an inconclusive research result and
  leaves `CONTEXT.md` unchanged unless the user explicitly asks to record the
  unresolved state.
- **User rejects the recommendation:** The skill does not persist the rejected
  template or treat it as agreed. It may present the next evidence-backed
  candidate or end with no selected direction, but it must not silently choose
  another template.
- **Existing direction conflicts:** If a different direction already exists,
  the skill shows the conflict and preserves the existing direction until the
  user explicitly confirms replacement. A same-template, same-revision rerun
  is idempotent and must not create duplicate sections.
- **Representation mismatch:** If the index, canonical page, Markdown, and
  JSON representations disagree on identity, status, or revision, the skill
  treats the candidate as unresolved until the inconsistency is reported or a
  directly supporting representation is available.
- **Missing machine-readable representation:** The skill may use the canonical
  human page only when it directly supports the claim. Otherwise it reports
  `Research needed` or `Open question` instead of inferring structured fields.

## Business rules and constraints

- Explicit user decisions, project requirements, accepted specifications,
  ADRs, and `AGENTS.md` remain authoritative over public template guidance.
- Only published public templates may be recommended. Draft and archived
  content is not a candidate even if a direct URL is known.
- A template's canonical identity is its published slug and canonical URL;
  revision and `updatedAt`/`updated_at` are freshness evidence. The skill must
  not infer the latest revision from list order or page position.
- `templateProfile`, `templateTokens`, and `templateExamples` are structured
  published fields. The skill must not infer template semantics from arbitrary
  CSS or from visual similarity alone.
- A recommendation is a `Proposal`; only explicit user confirmation promotes
  it to `Agreed` and permits persistence.
- Existing human-authored context, the generated `## Codebase Context`
  section, requirements, specs, and ADRs must be preserved. The skill owns only
  its dedicated `## Design Direction` section.
- The external docs site is read-only for this skill. No credentials or private
  project data may be sent to it.
- Research is bounded to the relevant public discovery and content routes. The
  skill does not crawl unrelated pages or maintain an external cache.

### Persisted direction

After confirmation, `CONTEXT.md` must contain one dedicated `## Design
Direction` section with an observable record containing, at minimum:

- status: `Agreed`, `Research needed`, or `Open question`;
- template identity: title, type, slug, canonical URL, revision, published
  timestamp, and updated timestamp when published;
- template profile: the published applicability, mood/tone, color palette,
  typography, visual style, animation principles, component set, and
  constraints when provided;
- template tokens: the published token object without silently changing its
  values;
- template examples: the published examples or a faithful structured
  representation that downstream agents can inspect; and
- research evidence: source URL, source title or identifier, access date, and
  the claim or matching rationale supported by the source.

The section must be updated idempotently for the same template revision. A
replacement must retain the conflict and confirmation boundary described above.

## Data and permissions

- `CONTEXT.md` is the project-owned destination for the confirmed design
  direction. The project owner and explicit user confirmation control whether
  a proposed direction becomes agreed.
- Public Phatysd content is read-only research input. The skill may retain
  source metadata in `CONTEXT.md` after confirmation but must not modify the
  external site.
- No application user data, private repository content, credentials, or
  external account state is sent to the Phatysd site.
- A proposal is not an active project direction until the confirmation state
  is observable in the response and persisted record.

## Errors and edge cases

- `llms.txt`, search, hierarchy, canonical, Markdown, or JSON retrieval is
  unavailable, times out, or returns an access error.
- A discovered item is not `type: template`, is not `status: published`, or
  exposes incomplete identity or freshness metadata.
- The public representations disagree or a canonical page has no direct
  support for the structured claim being made.
- No candidate has enough evidence to be recommended as the single best fit.
- A project already has a design direction and the new recommendation would
  replace or contradict it.
- The user rejects the recommendation or does not confirm it.
- `CONTEXT.md` is missing or the project has not completed the required setup;
  the skill must stop and route the project to `$setup-project` rather
  than creating unrelated project context itself.

## Interfaces and observable test points

- **Invocation boundary:** The skill is explicitly invoked after project setup
  when a reusable published visual direction is requested; it does not run as
  a hidden sub-step of another skill.
- **Research result:** The response identifies the selected candidate, its
  published identity and revision, the evidence used, and the state
  `Proposal`, `Research needed`, or `Open question`.
- **Confirmation boundary:** The response makes clear whether the user has
  confirmed the recommendation. A proposal-only response leaves the existing
  `CONTEXT.md` direction unchanged.
- **Persisted record:** A confirmed result is visible under exactly one
  `## Design Direction` section with the fields in [Persisted direction](#persisted-direction).
- **Conflict state:** A conflicting existing direction remains visible and is
  not overwritten until explicit replacement confirmation.
- **Handoff:** The response recommends exactly one of `$to-prototype` or
  `$write-spec` based on the existing visual-validation intent and does
  not invoke it automatically.

## Non-functional requirements

- **Traceability:** Every persisted external claim has a canonical source URL,
  title or identifier, access date, and matching rationale.
- **Authority preservation:** Public template guidance cannot silently override
  project requirements, context, ADRs, accepted specifications, or explicit
  user decisions.
- **Idempotency:** Repeating the skill for the same template revision does not
  duplicate the design-direction section or alter unrelated context.
- **Safety and privacy:** The skill uses public read-only content, does not
  require credentials, and does not transmit private project data externally.
- **Freshness awareness:** Persisted identity retains revision and timestamp
  fields so downstream agents can recognize stale template evidence.

## Research basis

The following published sources were checked on 2026-09-21:

- [Phatysd `llms.txt`](https://docs.phatysd.me/llms.txt) — published template
  discovery index and canonical template URLs.
- [Public Content Contract v1](https://docs.phatysd.me/content/public-content-contract-v1)
  — published-only lifecycle, stable human/Markdown/JSON routes, identity and
  revision fields, and the validated template profile/token/example fields.
- [Quiet SaaS Dashboard human page](https://docs.phatysd.me/content/quiet-saas-dashboard)
  and [JSON representation](https://docs.phatysd.me/content/quiet-saas-dashboard/json)
  — concrete published template profile, token, example, revision, and
  freshness shape.

## Acceptance criteria

- AC-01: Given a project with prepared context after `setup-project`, when
  `setup-template` is invoked, then it reads the relevant local project sources
  and does not create unrelated project context.
- AC-02: Given the public Phatysd site is available, when the skill researches
  candidates, then it starts from the published discovery path and considers
  only items identified as `type: template` and `status: published`.
- AC-03: Given one or more published candidates, when the skill evaluates fit,
  then its recommendation is supported by applicability/use cases, project
  scope or user flows, constraints, and visual profile evidence rather than
  by arbitrary CSS or list order alone.
- AC-04: Given a sufficiently supported candidate, when the research phase
  completes, then the skill recommends exactly one template and exposes its
  title, slug, canonical URL, revision, freshness metadata, relevant profile,
  tokens, examples, and matching rationale as `Proposal`.
- AC-05: Given a recommendation in `Proposal` state, when the user has not
  explicitly confirmed it, then the skill does not create or replace the
  `## Design Direction` section in `CONTEXT.md`.
- AC-06: Given the user explicitly confirms the recommendation, when the skill
  persists the result, then `CONTEXT.md` contains one `## Design Direction`
  section with `Agreed` status, template identity and revision, published
  profile/tokens/examples, and source URL, title or identifier, access date,
  and matching rationale.
- AC-07: Given `CONTEXT.md` already contains a different design direction,
  when a new recommendation conflicts with it, then the existing direction is
  preserved and replacement requires explicit confirmation with the conflict
  exposed.
- AC-08: Given the same confirmed template revision is processed again, when
  the skill updates project context, then it is idempotent and does not create
  duplicate design-direction sections or alter unrelated context.
- AC-09: Given the discovery site is unavailable, no suitable published
  candidate exists, or representations cannot directly support the claim,
  when research ends, then the skill reports `Research needed` or `Open
  question`, does not invent a template decision, and leaves existing context
  unchanged.
- AC-10: Given the user rejects or does not confirm the recommendation, when
  the skill finishes, then the rejected template is not persisted as `Agreed`
  and no replacement is selected silently.
- AC-11: Given a canonical page and machine-readable representation disagree,
  when the inconsistency affects identity, status, revision, or structured
  fields, then the candidate remains unresolved and the inconsistency is
  reported.
- AC-12: Given the confirmed result and the project's visual-validation intent,
  when the skill finishes, then it recommends `$to-prototype` if visual
  validation is requested or `$write-spec` otherwise, without invoking
  the downstream skill automatically.
- AC-13: Given any research or persistence outcome, when the skill operates,
  then it does not write to `docs.phatysd.me`, require credentials, transmit
  private project data, generate production code, or create a prototype.
- AC-14: Given project setup is complete and a reusable published visual
  direction is explicitly requested, when the next workflow route is chosen,
  then `$setup-project` or `$ask-workflow` recommends `$setup-template` if no
  agreed direction exists or an explicit replacement was requested; otherwise
  it preserves the existing prototype/specification route. A visual-validation
  request alone does not trigger template research.

## Verification plan

| AC | Verification |
| --- | --- |
| AC-01 | Run a prepared-project scenario and inspect the read set and resulting diff; verify no unrelated context or project files are created. |
| AC-02 | Use a fixture or live read of `llms.txt` and template content; verify discovery, `type`, and `status` filtering. |
| AC-03 | Review representative matches with distinct applicability, component, constraint, and visual-profile evidence; verify CSS or list order is not the sole rationale. |
| AC-04 | Inspect a successful research response for exactly one candidate and all required identity, profile, token, example, freshness, and rationale fields. |
| AC-05 | Stop before confirmation and inspect `CONTEXT.md`; verify no proposal is persisted. |
| AC-06 | Confirm a candidate and inspect `CONTEXT.md`; verify the single design-direction section and source metadata. |
| AC-07 | Seed an existing conflicting direction, run the skill, and verify the old direction remains until replacement is explicitly confirmed. |
| AC-08 | Run the same confirmed template revision twice and compare the second diff; verify no duplicate section or unrelated changes. |
| AC-09 | Simulate unavailable endpoints, empty matches, and unsupported representations; verify the explicit fallback state and unchanged context. |
| AC-10 | Reject or omit confirmation and inspect the persisted state; verify no rejected candidate becomes agreed and no silent fallback occurs. |
| AC-11 | Provide conflicting identity/status/revision fields across representations; verify the candidate is reported unresolved. |
| AC-12 | Exercise both visual-validation branches and inspect the final recommendation; verify no downstream skill is invoked automatically. |
| AC-13 | Static-review the skill boundary and run a read-only scenario; verify no external write, credential request, private-data transmission, code generation, or prototype creation. |
| AC-14 | Inspect the post-setup routing in `$setup-project` and `$ask-workflow` with/without an explicit template request and with an existing agreed direction; verify visual-validation requests alone still route directly to `$to-prototype`. |

## Open questions

- Non-blocking: The exact scoring or ordering method used internally when
  several candidates have comparable evidence can be chosen during task
  planning, provided the single-recommendation and evidence rules remain true.
- Non-blocking: The precise Markdown formatting for nested token and example
  values can be chosen during implementation, provided the persisted fields
  remain inspectable and faithful to the published representation.
