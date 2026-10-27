# Motion and variants

## Motion

Use when animation, a useful delightful detail, or an ambitious effect is
requested. Preserve the established visual world and operating task. A small
well-timed acknowledgement can fit a tool; a creative showcase may deserve an
authored sequence. No surface needs motion on every element.

Identify the job first: explain a state change, preserve spatial continuity,
acknowledge an action, or express a product-specific focal moment. Name what
starts, ends and interrupts it. If removing an effect loses no useful meaning
or requested character, reconsider adding it.

Reuse the project's motion language and runtime. CSS is enough for simple
transitions; use existing animation tools for stateful sequencing when needed.
Do not install a library, create video assets, or replace a renderer merely to
demonstrate motion. For ambitious canvas/shader/3D work, use appropriate existing
tools only when within scope and feasible; keep a functioning fallback and
report unavailable capability instead of a static imitation claimed as working.

Tune duration to distance and consequence: immediate feedback should feel
immediate, routine overlays brief, and a focal sequence rare. Repeated use must
not make people wait. Prefer coherent deceleration over reflex bounce. Limit
stagger duration; a long list should not postpone the last useful control.

Keep content available before scripts/animation initialize. Avoid focus or
pointer traps during transitions. Test rapid toggles, Escape/cancel, reverse
direction and repeated activation; delayed callbacks must not restore stale
states. Prefer bounded compositing work and measure costly layout/filter/paint
effects on the target device rather than assuming transforms guarantee speed.

Provide reduced-motion behavior that reduces nonessential travel while keeping
state feedback understandable. Loops should pause when hidden where supported;
respect sound/autoplay settings. Check keyboard, narrow screens and final resting
states, not just a recording of the entrance. Report whether input and motion
were actually exercised, emulated, or only inferred from source.

For delight, choose a specific useful detail such as a clear completion
acknowledgement or considerate empty state. Do not invent rewards, progress,
achievement claims, sound or confetti disconnected from product behavior.

## Variants

Use when alternatives or comparison are requested, not as mandatory overhead
for every screen. Resolve the named target, fixed content/behavior/identity,
comparison question and requested number. Choose a small proportional set
when count is unspecified; a precise request for three means three.

Vary a consequential axis: reading path, task density, type hierarchy, asset
emphasis, or interaction presentation. Color-only alternatives are valid when
color is explicitly the question. Each candidate should be coherent rather
than one attractive sample against deliberate strawmen.

Keep the baseline safe and each alternative isolated using the parent's actual
prototype/artifact conventions. If no convention exists, use separate local
preview artifacts within the permitted output scope. Do not create Git branches,
replace shared tokens globally, or overwrite the current design just to compare.
Preserve the same data, path, state and viewport when capturing candidates.

Label changed axes and practical tradeoffs; use screenshots at readable detail
and working previews when possible. Scope DOM queries to the requested behavior,
not an assumed topology: an unassigned queue beside or below a timeline can both
be valid. Keep aesthetic observations distinct from functional defects and
measurement. For independent experiments, record prompts, snapshots and any
corrections; do not cherry-pick outputs to make one candidate win.

Return comparisons and a recommendation when useful. A request for alternatives
alone does not select or persist a winner. If selection or implementation is
explicitly delegated, choose and apply the preferred candidate within scope;
do not ask again for an already authorized choice. Use existing browser tools
when available, but do not claim a live editing panel or upstream plugin exists.

Adaptation provenance and license: [upstream](upstream.md).
