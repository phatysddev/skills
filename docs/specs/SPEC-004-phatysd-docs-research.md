# SPEC-004: Conditional Phatysd Docs research during grilling

- Status: done
- Requirement: [docs/requirement.md](../requirement.md)
- Context: [CONTEXT.md](../../CONTEXT.md)
- ADRs: None

## Problem and outcome

`grill-workflow` can resolve ambiguity from repository evidence and explicit
user decisions, but some Phat-specific conventions or current workflow
guidance may not be present in the repository. The skill needs a bounded way to
consult the public Phatysd knowledge site when that evidence is insufficient,
while preserving project-specific sources of truth.

The outcome is a grilling flow that researches current, published Phatysd
guidance only when needed, records the evidence used, and keeps unresolved or
unavailable research explicit instead of inventing an answer.

## In scope

- Extend `grill-workflow` with a conditional research decision after local
  project context has been read.
- Use `https://docs.phatysd.me/` as the public Phatysd knowledge source.
- Discover published material through `/llms.txt`, `/search`, and `/docs`.
- Prefer a canonical human page for context and a Markdown or JSON
  representation for precise details when those representations are available.
- Record the source URL, title or identifier, access date, and supported claim
  in the grilling summary or a relevant decision record.
- Classify externally supported claims without changing the existing Fact,
  Proposal, Agreed, and Open question decision states.
- Preserve explicit fallback behavior when the site is unavailable or has no
  relevant published content.

## Out of scope

- Researching external docs for every grilling session when local evidence and
  user decisions are sufficient.
- Treating public docs as a replacement for project requirements, context,
  specifications, ADRs, or explicit user decisions.
- Publishing, editing, or authenticating against the Phatysd knowledge site.
- Building a crawler, cache, synchronization job, or new runtime integration.
- Automatically invoking a downstream Phat skill after research.
- Defining the question contract for `grill-workflow`; that behavior is owned
  by the grilling workflow rather than this research capability.

## User flow and behavior

### Primary flow

1. The user invokes `grill-workflow` for an ambiguous project or feature.
2. The skill reads `AGENTS.md` and relevant local project context before
   deciding whether external research is necessary.
3. If local evidence and explicit user decisions are sufficient, the skill
   skips external research and continues grilling.
4. If a missing Phat-specific fact, current guidance, skill capability, or
   platform behavior materially affects the decision, the skill checks the
   public Phatysd knowledge site.
5. The skill starts with `/llms.txt`, then uses `/search` or `/docs` to locate
   relevant published material. It uses the canonical page and available
   machine-readable representation to understand the claim.
6. The skill records the source metadata and uses only claims directly
   supported by published material.
7. The skill continues the normal grilling flow, asking the next small,
   highest-impact decision set using the question format appropriate to the
   decision, and preserving the existing decision-state rules.

### Alternate flows

- If the site is unavailable, times out, or cannot be read, the skill reports
  that research was inconclusive and marks the affected point as **Research
  needed** or **Open question**. It does not fabricate a Phat-specific answer.
- If the site is reachable but contains no relevant published material, the
  skill reports the same research gap and does not treat the absence of content
  as evidence for a decision.
- If public guidance conflicts with project-specific requirements, accepted
  specifications, ADRs, `AGENTS.md`, or an explicit user decision, the
  project-specific source remains authoritative and the conflict stays
  visible for resolution.
- If a Markdown or JSON representation is unavailable, the skill may use the
  canonical human page when it directly supports the claim; otherwise the
  claim remains unresolved.

## Business rules and constraints

- External research is conditional, not a mandatory step for every session.
- Explicit user decisions and project-specific repository documents are
  authoritative for project behavior.
- Public Phatysd docs may confirm general Phat conventions, but must not
  silently override project-specific sources.
- A published source that directly supports a claim may establish it as
  **Fact**; an unsupported or indirect claim remains **Proposal** or **Open
  question**.
- Research evidence must remain attributable through a URL, title or
  identifier, access date, and claim summary.
- The skill remains responsible for grilling only; research must not bypass
  specification, task, implementation, or review handoffs.

## Data and permissions

- The skill reads public Phatysd pages and their published representations.
- The skill does not require or collect credentials and does not write to the
  external site.
- Research metadata is retained only in the grilling summary or a relevant
  decision record unless a later workflow explicitly persists it elsewhere.
- No application user data, private project data, or external service state is
  changed by this capability.

## Errors and edge cases

- The public site is unavailable, returns an access error, or exposes no
  published content relevant to the question.
- The index, search results, canonical page, and machine-readable
  representation disagree or are incomplete.
- A page describes a general convention but does not directly support the
  project-specific decision being considered.
- Local requirements and public docs conflict; the conflict must not be
  silently resolved by the research result.
- A current/freshness claim cannot be established from the published source;
  the skill must retain the uncertainty rather than infer recency.

## Interfaces and observable test points

- `grill-workflow/SKILL.md` identifies the public source and the conditional
  research trigger.
- The research path identifies these discovery locations:

  ```text
  https://docs.phatysd.me/
  https://docs.phatysd.me/llms.txt
  https://docs.phatysd.me/search
  https://docs.phatysd.me/docs
  ```

- A research-backed grilling summary exposes the source URL, title or
  identifier, access date, and supported claim.
- An unavailable or inconclusive research attempt exposes **Research needed**
  or **Open question** and contains no invented external claim.
- The normal focused question-set/direct-question format and explicit
  downstream handoff remain observable after the research step; research does
  not change the grilling question contract.

## Non-functional requirements

- **Traceability:** Each material external claim used in grilling is tied to a
  published source and access date.
- **Safety:** The skill must not expose credentials, collect private access, or
  make writes to the external knowledge site.
- **Authority preservation:** External research cannot silently replace local
  project sources of truth.
- **Minimal side effects:** The research step changes only the evidence used in
  the grilling summary or explicitly requested decision record.

## Acceptance criteria

- AC-01: Given local project context and explicit user decisions fully answer
  the relevant Phat-specific question, when `grill-workflow` runs, then it
  skips external research and continues its normal questioning flow.
- AC-02: Given a missing Phat-specific fact, current guidance, skill capability,
  or platform behavior materially affects a decision, when `grill-workflow`
  runs, then it researches `https://docs.phatysd.me/` through the documented
  discovery path before relying on an external claim.
- AC-03: Given published material directly supports a claim, when the claim is
  used in grilling, then the summary or relevant decision record includes its
  source URL, title or identifier, access date, and claim summary.
- AC-04: Given a public Phatysd claim conflicts with an explicit user decision
  or project-specific requirement, accepted specification, ADR, or
  `AGENTS.md`, when the conflict is encountered, then the project-specific
  source remains authoritative and the conflict is not resolved silently.
- AC-05: Given the public site is unavailable or has no relevant published
  content, when research is attempted, then the skill marks the gap as
  **Research needed** or **Open question** and does not invent a Phat-specific
  answer.
- AC-06: Given a canonical page has no Markdown or JSON representation, when it
  directly supports the claim, then the skill may use the human page; otherwise
  the claim remains unresolved rather than being inferred as fact.
- AC-07: Given any research outcome, when `grill-workflow` continues, then it
  still asks one small, highest-impact decision set per round, uses 2–4
  concrete options only when meaningful alternatives exist, uses a direct
  question for boolean/factual/user-defined answers, and does not invoke a
  downstream skill automatically.
- AC-08: Given the research step is reviewed statically, when the skill source
  is inspected, then the conditional trigger, authority rules, source-recording
  fields, fallback behavior, and public discovery locations are all explicit.

## Verification plan

| AC | Verification |
| --- | --- |
| AC-01 | Run a scenario where the repository and user statement already define the Phat-specific decision; inspect that no external lookup is required and the normal question format remains intact. |
| AC-02 | Run a scenario with a missing/current Phat-specific rule; inspect the research path and confirm it checks the public index and relevant docs/search locations before using the claim. |
| AC-03 | Inspect a research-backed grilling summary and verify the URL, title or identifier, access date, and claim are all present. |
| AC-04 | Provide conflicting local and public guidance; verify the local authoritative source remains selected and the conflict is reported. |
| AC-05 | Simulate an unavailable site and an empty relevant result; verify the output contains `Research needed` or `Open question` and no fabricated external conclusion. |
| AC-06 | Use a canonical-page-only scenario and a scenario without direct support; verify the former may be cited and the latter remains unresolved. |
| AC-07 | Inspect representative outputs after skipped, successful, and failed research; verify the appropriate focused question format is used and no downstream skill is invoked. |
| AC-08 | Review `.agents/skills/grill-workflow/SKILL.md` against the documented trigger, source paths, authority, evidence, fallback, and question-format boundaries; run `git diff --check`. |

## Open questions

- **Non-blocking:** The public knowledge site currently has no published
  content, so the first live research attempts may remain inconclusive until
  relevant Docs are published.
- **Non-blocking:** The exact machine-readable URL pattern for individual
  published items can be adopted from the canonical page when such items are
  available; the behavior remains valid with the human page alone when it
  directly supports a claim.
