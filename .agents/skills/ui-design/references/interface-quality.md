# Interface quality

Use the requested operation within the parent or explicit standalone scope.
Audit reports; authorized adaptation, hardening or fixes change implementation.
Neither is canonical code review, product security review, or a certification.

## Audit

Resolve the target, important user paths, supported devices/themes/languages,
and available evidence. Use existing tools and runners; do not install an audit
suite or enable remote debugging on a live session merely to perform a scan.
Choose checks relevant to actual requirements, not a universal scorecard.

Use authorized local/demo/test fixtures for state-changing interaction checks.
A read-only audit does not submit real transactions or change live records;
report paths that cannot be exercised within scope.

Inspect source and rendered interaction separately:

| Area | Evidence to inspect |
| --- | --- |
| Accessibility | Semantic controls and names; tab/focus order; focus return; error association; keyboard completion; actual contrast pairs; reduced motion; meaningful alternatives to color. |
| Responsive/input | Document vs intentional region overflow; text expansion/zoom; sticky overlap; control reachability; mouse, keyboard and touch paths actually exercised. A narrow viewport does not prove touch gestures. |
| Themes/system | Existing semantic tokens and shared patterns, selection/disabled/error states, supported theme contrast. Missing optional theming is not a defect. |
| Performance | Actual loading/reflow, expensive repeated paint/layout, interaction traces or timings when available. A large source file alone does not prove slowness. |
| Integrity | All required records/options/actions, valid HTML, accurate counts, honest mock behavior, no decorative controls presented as functioning features. |

Use repository-required accessibility targets when present. If invoking an
external standard, verify its current applicable criterion from an authoritative
source; do not invent a violation from a preferred control size. Automated
checks are partial coverage, never a claim of full accessibility compliance.

For each finding return location, evidence/method, user consequence, required
constraint or advisory status, and a concrete remedy. Separate observed,
source-suspected, unverified, and not-applicable results. Prioritize task
blockers/data loss, then significant usability/verification gaps, then polish.
Do not give a numerical beauty or compliance score based on unperformed checks.
Audit alone changes no source or status; audit-and-fix continues with scoped
corrections and rechecks without imposing another approval round.

## Local HTML check

Run the bundled standard-library helper only on scoped local HTML:

```text
python3 <skill-dir>/scripts/inspect_html.py <file.html-or-directory>
```

It reads files without executing HTML/JS, using network, or editing output.
JSON separates definite malformed-select/closing-tag/duplicate-ID findings from
advisory missing-name/alt/viewport observations. Use exit code 0 for no definite
defects (advisories may remain), 1 for definite defects, 2 for missing/unreadable
input or incomplete coverage. A fragment is not penalized for lacking viewport
metadata. Templates are explicitly excluded; dynamic DOM and framework source
need framework/rendered checks. Do not count ignored content as verified.

Review every candidate in context. A label may be supplied dynamically, but a
plain HTML parse cannot establish it. Follow the parent's gate policy; a
missing Python/tool is a reported gap, not automatic installation or a new gate.

## Adapt and harden

Inventory relevant states and content ranges: normal, first use, empty/filter
empty, loading, error/retry, disabled, success, permission-limited and large or
long content. Use only states supported by actual behavior; mock network or
permission scenarios honestly in a prototype instead of adding backend rules.

Preserve the primary task at narrow/intermediate/wide sizes. Decide what
wraps, reorders, scrolls within a region, or becomes a reachable disclosure.
Check full-page overflow separately from deliberate table/timeline scrolling.
When adding status, hints or actions to a bounded component, recheck the
existing text and controls too: let it grow or use deliberate whole-line
truncation with full content reachable, rather than clipping half a line.
Test the user's failing viewport and useful zoom/text expansion. For dense
work, count visible useful records and inspect legibility together; denser is
not automatically better. Dialogs and sticky actions must remain reachable.

Stress actual strings, missing values and supported scripts. Keep full required
content available when truncating. Thai combining marks, baseline and wraps
need real rendering; arbitrary Latin letter-spacing defaults can break them.
Use the existing localization pipeline, calendars/timezones and directionality
required by the product, rather than inventing a language or locale promise.

Exercise failures through supported local fixtures or safe test seams. Check
that errors name recovery, draft input survives rejection, duplicate submits
are handled by existing behavior, and focus moves sensibly. Do not invent
retry, undo, offline persistence, permissions or optimistic updates without a
behavioral contract. Reinspect corrected states and report untested devices.

## Copy and onboarding

Inventory action names, labels, hints, errors, empty states and confirmations.
Use the product's vocabulary and a clear information order: current state,
what it means, next useful action. Error copy identifies the specific problem
and recovery near its source without exposing secrets or raw internal errors.
Keep required labels visible; a tooltip is not a substitute for essential
instructions. Preserve factual claims, legal text, business rules and meaning.

Distinguish first-use empty, filter-no-results, unavailable data and completed
work. Each has a different next action. Onboarding should point to existing
work and be dismissible where the behavior permits; do not invent a tutorial,
account setup, product feature or permission flow merely to fill an empty view.
Use a before/after copy map for meaningful edits; verify long translations and
that each named action actually works. A prototype confirmation must not imply
a server save or persistence it does not provide.

## Optimize

Start with a reproducible symptom and representative path/device. Record an
actual baseline when measurement is available: asset loading, layout shift,
slow interaction, repeated rendering or expensive paint. If no profiler/runtime
exists, label source-level hypotheses and avoid invented speedup numbers.

Choose the smallest justified change: correct image dimensions/sources, defer
noncritical work, remove unused assets, bound expensive effects, or reuse the
existing component/render patterns. Do not blindly memoize, virtualize, lazy-load
the primary image, add a library, or rewrite the architecture. State/cache/API
changes belong to the implementation owner's behavioral scope.

Repeat the same measurement and functional path after changes. Record result,
conditions and tradeoffs; check that focus, layout, loading and visible content
did not regress. Report remaining hypotheses separately from measured gains.

Adaptation provenance and license: [upstream](upstream.md).
