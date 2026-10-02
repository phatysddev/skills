---
name: setup-template
description: "Read prepared Phat project context, research published Phatysd templates, and recommend exactly one evidence-backed design direction without persisting a proposal. Use after setup-project when a reusable visual direction is needed."
---

# Setup Template

Research the published Phatysd template library and recommend one design
direction that fits the prepared project context.

This skill owns the research, confirmation, and persistence boundary. A
recommendation is always a `Proposal` until the user explicitly confirms it.
Do not write a design direction while it is only a proposal. Do not generate
production code, create a prototype, or invoke a downstream skill.

## Contents

- [Workflow](#workflow)
- [Read before researching](#read-before-researching)
- [Preconditions](#preconditions)
- [Discover published templates](#discover-published-templates)
- [Validate representations](#validate-representations)
- [Match project evidence](#match-project-evidence)
- [Recommendation output](#recommendation-output)
- [Confirm and persist](#confirm-and-persist)
- [Final handoff](#final-handoff)
- [Fallback behavior](#fallback-behavior)
- [Research boundaries](#research-boundaries)

## Workflow

Follow this sequence:

```text
Read prepared project context
        ↓
Discover published template candidates
        ↓
Validate identity and representations
        ↓
Match candidates against project evidence
        ↓
Recommend exactly one candidate as Proposal
        ↓
Wait for explicit confirmation
        ↓
Persist only the confirmed direction
```

After confirmation, persist only the selected direction according to
[Confirm and persist](#confirm-and-persist). Do not invoke another Phat skill
from this workflow.

## Read before researching

Read `AGENTS.md` first if it exists.

Then read only the project sources relevant to the design decision:

- `docs/requirement.md` for product goal, users, scope, constraints, and
  visual-validation intent, and applicable Agreed UI Design Requirements;
- `CONTEXT.md` for domain vocabulary, existing project facts, and any existing
  `## Design Direction` section;
- accepted specifications that describe the product surfaces or user flows;
- relevant ADRs when they constrain the project direction; and
- `docs/workflow.md` when the final workflow intent must be identified.

Treat local requirements, accepted specifications, ADRs, `AGENTS.md`, and
explicit user decisions as authoritative. Existing project behavior is
evidence, not permission to silently choose a design direction.

## Preconditions

Run after `$setup-project` has prepared the project context.

If `CONTEXT.md` is missing, the project context is not initialized, or a
required source is materially unresolved, stop and recommend
`$setup-project`. If the existing `## Design Direction` structure is
ambiguous or malformed enough that its owned boundaries cannot be identified
safely, stop and report `Open question` rather than rewriting the file. Do not
create unrelated context merely to continue research.

If an existing `## Design Direction` is present, read it and keep it visible.
This research phase may report a possible conflict, but it must not replace,
rewrite, or duplicate the existing direction.

## Discover published templates

Use the public Phatysd knowledge site only as read-only research input:

```text
https://docs.phatysd.me/
https://docs.phatysd.me/llms.txt
https://docs.phatysd.me/templates
https://docs.phatysd.me/search
https://docs.phatysd.me/docs
```

Start with `https://docs.phatysd.me/llms.txt` to discover canonical published
URLs. Narrow the set through the Templates collection, search, hierarchy, or
topic/tag pages only as needed. Do not crawl unrelated content or assume that
URL order means relevance or freshness.

For each promising canonical item, retrieve the available representations:

```text
Human page: https://docs.phatysd.me/content/:slug
Markdown:   https://docs.phatysd.me/content/:slug/markdown
JSON:       https://docs.phatysd.me/content/:slug/json
```

Prefer JSON for structured identity, revision, profile, token, and example
fields. Prefer Markdown for authored guidance and text-first context. Use the
human page for hierarchy and readable context, but do not scrape visual CSS to
invent template semantics.

Only consider an item when its published identity directly establishes:

- `type: template`;
- `status: published`;
- title, slug, and canonical URL;
- revision and available published/updated timestamps; and
- enough of `templateProfile`, `templateTokens`, and `templateExamples` to
  support the recommendation output.

Draft, archived, missing, or incomplete items are not candidates. Do not use a
known direct URL to bypass the published status or discovery contract.

## Validate representations

Treat the canonical page, Markdown, and JSON as representations of one
published item. Before using a candidate:

1. Compare title, slug, canonical URL, type, status, and revision when those
   fields appear in more than one representation.
2. Retain the explicit revision and timestamp values; never infer freshness
   from list position or page layout.
3. Treat a disagreement affecting identity, status, revision, or structured
   fields as unresolved and report the mismatch.
4. If Markdown or JSON is unavailable, use the human page only when it directly
   supports the claim being made. Otherwise report `Research needed` or
   `Open question`.
5. Ignore fields that the published contract does not expose. Do not infer
   `templateProfile`, `templateTokens`, or `templateExamples` from arbitrary
   CSS or visual resemblance.

Record the source URL, source title or identifier, access date, and the claim
supported by each material external fact used in the recommendation.

## Match project evidence

Evaluate candidates against evidence already present in the project. Keep the
matching rationale separate from published facts.

Use these signals in order of importance:

1. Applicability and use cases against the product goal, target users, and
   agreed scope.
2. Component set against known user flows, product surfaces, and information
   hierarchy.
3. Constraints against agreed accessibility, responsive, content, or
   operational requirements.
4. Mood, tone, visual style, typography, and animation principles against any
   explicit visual direction.
5. Topics, tags, hierarchy, tokens, and examples as supporting evidence or
   tie-breakers, never as the sole proof of domain fit.

Do not invent project goals, users, constraints, or visual preferences. If the
available project evidence cannot distinguish a best fit, report
`Research needed` or `Open question` rather than manufacturing a ranking.

## Recommendation output

When one candidate is sufficiently supported, present exactly one
recommendation using this shape:

```text
Template recommendation
- State: Proposal
- Title: <published title>
- Type: template
- Slug: <published slug>
- Canonical URL: <published canonical URL>
- Revision: <published revision>
- Published/updated: <published timestamps when available>
- Profile: <relevant published profile fields>
- Tokens: <published templateTokens>
- Examples: <published templateExamples>
- Why it fits: <project evidence mapped to template evidence>
- Research evidence: <source title/identifier, URL, access date, claim>

Confirmation required: confirm or reject this proposal.
```

Label externally supported statements as `Fact` when the published source
directly supports them. Label the candidate match as `Proposal`; it is not an
agreed project decision. Do not present a second candidate as an automatic
fallback in the same recommendation.

The response must not create or update `## Design Direction` while the result
is only a proposal. After explicit confirmation, use
[Confirm and persist](#confirm-and-persist). A rejection or missing
confirmation leaves existing context unchanged.

## Confirm and persist

Persist only after the user explicitly confirms the current proposal.

Before confirmation, compare the candidate with applicable Agreed UI Design
Requirements, including scoped overrides from `$grill-design`. Expose any
material conflict. Confirming a template alone does not revoke those decisions.
Require an explicit resolution; if it changes the authoritative design brief,
recommend `$grill-design` to record that change before proceeding. This skill
still owns only Design Direction and must not rewrite the requirements. Keep
published template values faithful and distinguish them from project overrides.

1. Treat an explicit confirmation of the displayed proposal as permission to
   persist that template. A rejection, ambiguous response, or missing response
   is not confirmation and must not change `CONTEXT.md`.
2. If an existing `## Design Direction` names a different template or
   revision, show the existing and proposed identities and the material
   differences. Require explicit replacement confirmation after exposing that
   conflict; the first proposal response must not silently replace the old
   direction.
3. If no `## Design Direction` exists, append exactly one dedicated section to
   `CONTEXT.md`. If one exists and replacement is confirmed, update only that
   section. Preserve every other human-authored section, the generated
   `## Codebase Context` section, requirements, specifications, ADR references,
   and unrelated formatting.
   If multiple or malformed design-direction boundaries make the owned section
   ambiguous, stop without writing and report `Open question`.
4. Persist the confirmed direction using this stable, inspectable shape:

   ```markdown
   ## Design Direction

   - Status: Agreed
   - Title: <published title>
   - Type: template
   - Slug: <published slug>
   - Canonical URL: <published canonical URL>
   - Revision: <published revision>
   - Published: <published timestamp when available>
   - Updated: <published timestamp when available>

   ### Profile

   - Applicability: <published value when available>
   - Mood and tone: <published value when available>
   - Color palette: <published value when available>
   - Typography: <published value when available>
   - Visual style: <published value when available>
   - Animation principles: <published value when available>
   - UI / component set: <published value when available>
   - Constraints: <published value when available>

   ### Tokens

   <published templateTokens, kept inspectable and faithful>

   ### Examples

   <published templateExamples, kept inspectable and faithful>

   ### Research evidence

   - Source title or identifier: <published source title or identifier>
   - Source URL: <canonical source URL>
   - Accessed: <access date>
   - Claim: <claim directly supported by the source>
   - Matching rationale: <project evidence mapped to template evidence>
   ```

   Preserve published token and example values without silently changing their
   meaning. Include only profile fields the source provides; do not fill gaps
   from CSS or visual guesses.
5. For a rerun with the same template slug and revision, compare the existing
   direction and leave it unchanged when it already represents the same
   confirmed record. Do not add a duplicate section or rewrite unrelated
   context. A newer revision may update the owned section only after the user
   confirms the current proposal.
6. Report the persisted state as `Agreed`, including the template identity,
   revision, source metadata, and the fact that the project direction was
   updated. Do not invoke `$to-prototype`, `$write-spec`, or another
   downstream skill from this skill.

## Final handoff

Only after the confirmed direction has been persisted and reported as `Agreed`,
recommend exactly one next workflow skill based on the existing visual-
validation intent:

- When visual validation was explicitly requested, report `Next: $to-prototype`.
- Otherwise, report `Next: $write-spec`.

Read the visual-validation intent from the authoritative local project sources
already required by this skill and from explicit user decisions. Do not infer
it from the selected template, and do not silently choose a branch when the
authoritative sources conflict; report the unresolved `Open question` instead.

For a `Proposal`, rejection, missing confirmation, `Research needed`,
`Open question`, unresolved replacement conflict, or failed persistence, report
the current state without recommending a downstream skill as though the
direction were confirmed. Never invoke the recommended skill automatically.

## Fallback behavior

Use the following outcomes without inventing a conclusion:

- **No suitable candidate:** report that no published template has enough
  evidence to be the single best fit; use `Research needed` or `Open question`.
- **Site unavailable or access error:** report an inconclusive research result
  as `Research needed` and identify the unavailable discovery or content route.
- **No relevant published content:** report the research gap; absence of a
  template is not evidence for a generic style.
- **Representation mismatch:** report the conflicting identity, status,
  revision, or structured field and leave the candidate unresolved.
- **Missing structured fields:** use a canonical human page only for claims it
  directly supports; otherwise keep the affected claim unresolved.
- **Existing direction conflict:** show the proposed difference and preserve
  the existing direction. Do not overwrite or create a duplicate section.
- **Malformed context:** if the design-direction boundary is ambiguous or
  duplicated, report `Open question` and leave `CONTEXT.md` unchanged.

In every research fallback, do not write `CONTEXT.md`, do not call another
skill, and do not claim that a template was selected. A rejected or
unconfirmed proposal follows the same no-write boundary.

## Research boundaries

- Public Phatysd content is read-only. Do not publish, edit, authenticate, or
  send credentials to `docs.phatysd.me`.
- Do not transmit private repository content, application data, or secrets to
  the external site. Use only the minimum public research needed to compare
  candidates.
- Do not generate production code, create a prototype, or change application
  files as a result of this skill.
- Do not invoke `$to-prototype`, `$write-spec`, or any other downstream
  skill automatically.
- Do not persist a proposal. Persist only an explicitly confirmed direction
  through [Confirm and persist](#confirm-and-persist), and never invoke a
  downstream skill automatically.
