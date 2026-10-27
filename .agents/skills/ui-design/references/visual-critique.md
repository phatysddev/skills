# Visual critique and refinement

Use after building or for a requested critique, polish, or targeted improvement.
Critique-only work reports findings without editing. Refinement preserves
identity and behavior; only an explicitly scoped redesign replaces them.

## Establish evidence

Read the requested change, applicable design agreement, and incumbent system.
With rendering available, inspect the actual target at its important wide and
narrow widths and an intermediate width when layout changes there. Include
the user's failing viewport when known. Test the primary path and relevant
states; a resting screenshot cannot establish keyboard usability or recovery.

Wait for fonts and assets, settle animation, and confirm each capture shows the
correct route, state, and viewport. Use a full composition view plus readable
details. A broken or half-loaded capture is a reason to recapture, not redesign.
Inspect the same viewport/state after material corrections for useful comparison.

If the app cannot run, inspect available screenshots only after checking their
target and freshness against source. Label conclusions from stale or partial
evidence. Without rendering, inspect structure and styles and explicitly leave
visual hierarchy, responsive appearance, and interaction results unverified.

## Diagnose before polishing

Consider these questions in order, using observations rather than a numerical
beauty score:

1. **Purpose and first glance:** What leads when details are blurred? Is the
   subject, current task, or primary action clear? On a work screen, can the
   user locate the relevant record or next step without scanning decorations?
2. **Structure:** Does reading order match priority? Are groups obvious through
   alignment and spacing? Do containers help, or does every section receive
   the same card regardless of its role? Is density right for frequency of use?
3. **Character:** Which visible choices belong to this product and its brief?
   Could the same composition serve unrelated products after renaming it?
   Improve real content, artifact emphasis, or type/layout choices before
   adding novelty. Familiar operational patterns can be exactly right.
4. **Craft:** Do type roles, line breaks, spacing rhythm, color hierarchy,
   image crops, and icon weights cohere? Are small details compensating for a
   structural flaw? Check actual text, including supported scripts and zoom.
5. **Use and adaptation:** Is the action reachable with mouse, keyboard, and
   touch where applicable? Do loading, empty, error, focus, overlays, and long
   content keep the task clear at the inspected sizes?

For each material issue, record a location, visible symptom, user consequence,
and concrete correction. For example: “At the narrow viewport the save button
falls behind the sticky footer; add space for the footer and verify focus can
reach Save.” “Looks generic” alone is not actionable evidence.

Distinguish a required constraint violation, an observed usability defect, a
visual improvement within scope, and an optional alternative. Do not turn a
font preference or aesthetic default into a failed acceptance criterion.

## Correct at the right level

When editing is authorized, prioritize blocked or misleading interactions,
then composition and responsive failures, then typography and spacing, then
surface details. Batch related fixes from one inspection. A token mismatch
may need the existing token; a wrong reading order needs structure, not a
shadow. Change a shared primitive only when the scope supports its effects,
and inspect affected neighbors when doing so.

For “bolder,” increase one useful source of emphasis and reduce competing
ones. For “quieter,” reduce noise while retaining the primary hierarchy and
recognizable character. For “simpler,” remove redundant containers or steps
only within authorized behavior. Do not remove required data or actions.

Reinspect after material fixes. Finish when the requested problem is resolved
and applicable checks support the result; avoid endless cosmetic searching.
Stop a stalled pass and name the unresolved issue or required asset/decision.
Follow the parent's correction budget and required verification gates. This
pass does not add another review agent or substitute for canonical code review.

## Report proportionately

Return the target, key decisions or findings, corrections made when authorized,
viewports/states actually inspected, and specific remaining gaps. Attach useful
capture paths when available. Distinguish observed results from source-only
checks and recommendations. Never claim accessibility compliance, responsive
success, or better visual results solely because a build or linter passed.

Adaptation details and license: [upstream](upstream.md).
