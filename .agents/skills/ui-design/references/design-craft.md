# Design craft

Use this reference to turn a visual thesis into decisions in the authorized UI.
The user's brief and established system take precedence over these defaults.
Choose what fits the surface; do not mechanically apply every technique.

## Typography and language

Assign roles before choosing sizes: display, heading, body, control, metadata,
and data where needed. Adjacent roles must differ visibly through weight,
size, placement, or spacing. Enlarging every heading destroys hierarchy.
Let expressive display type carry a campaign's voice when appropriate; keep
frequently used tools spatially stable. A familiar family is valid when tuned
deliberately; changing fonts alone does not create a distinctive design.

Reuse existing families. When a new face is justified and permitted, choose it
for the subject, glyph coverage, weights, and rendering, with usable fallbacks.
Avoid collecting fonts without a clear role. Check actual text after loading
and fallback; do not judge a font from a Latin sample alone.

For Thai or mixed Thai/English, inspect combining marks, stacked vowels and
tone marks, line breaking, baseline balance, and clipped text in compact
controls. Latin uppercase tracking and tight display leading are not universal
defaults. Do not force letter spacing or manual breaks across scripts.

For ordinary prose, roughly 45–75 characters per line is a useful starting
point, not a limit for tables or Thai text. Tune leading and measure together.
Keep body text readable at default zoom; ordinary web body text often starts
near 1rem. Use the project's scale for dense labels rather than shrinking all
text to fit. Check actual heading wraps at narrow and intermediate widths;
avoid hard breaks that look right at only one viewport. Preserve user zoom.
Use tabular numerals for comparable numeric columns when supported.

## Layout, rhythm, and density

Choose a reading path and focal element before boxes. Use proximity and
alignment to establish groups; add a container only when its boundary explains
ownership, independent interaction, or a real object. Repeated cards are useful
for equivalent independent items, not a substitute for page structure.

Create clear spacing relationships: related labels and values sit closer than
separate groups; sections have more separation than their internal elements.
Use the existing spacing scale. If none exists, a small consistent scale with
fine steps for controls and larger steps for sections is enough. Equal padding
everywhere makes all relationships look equally important.

On narrative pages, vary density, text/image proportions, and emphasis as the
content changes while retaining common alignment and type rules. Do not force
alternating layouts into equivalent records. On operational pages, repetition
supports comparison: align columns, stabilize row actions and status placement,
and keep useful information visible without surrounding each value with chrome.

Use whitespace to establish hierarchy, not to inflate a short page. A sparse
UI may need a stronger focal point or better use of content, not more padding.
Fix structure before micro-adjusting radii, borders, and shadows.

## Color, surfaces, and detail

Give the palette roles: canvas, surface, foreground, secondary foreground,
border, action/accent, and semantic status. Start from existing tokens and
extend only missing roles. A brand accent should lead attention somewhere;
using it on everything removes that guidance. Status colors retain stable
meanings, with words or symbols that work without color.

Choose neutral temperature and secondary colors to belong with the brand.
On tinted or dark surfaces, inspect the actual foreground/background pair;
do not assume a lighter opacity is readable. Verify contrast with available
tools rather than by impression. Gradients, glass, saturated colors, and shadows
can fit a brief; avoid using them to disguise weak grouping or missing imagery.

Match radius to object role and system conventions. Not every field, table,
button, panel, and image needs the same large rounding. Use elevation for real
layering such as a menu above content; a border or spacing may explain a flat
region better. Keep icon family, stroke weight, size, and optical alignment
coherent. An icon above every heading rarely contributes information.

When blandness is the problem, strengthen the focal point, image selection,
typographic contrast, or a purposeful brand accent. When noise is the problem,
remove competing emphasis and redundant containers. Neither request means
making every interface beige or replacing its identity.

## Imagery and product-specific character

Let relevant material do real work: an actual product view, object photograph,
artifact, map, editorial image, or useful diagram can communicate what abstract
decoration cannot. One well-composed asset may contribute more than numerous
generic icons. For a tool, precise data presentation can be the visual identity;
it does not need a stock photo.

Reuse authorized local assets first. When sourcing or generation is authorized
and available, choose material for the subject and desired crop; confirm that
it loads, has appropriate usage rights, and fits the composition. Preserve
provenance as the project requires. Do not install a media tool automatically,
invent customer logos, fabricate testimonials, or present placeholder metrics
as facts. An unavailable asset is a specific limitation; preserve a useful,
honest layout instead of pretending to have sourced it.

Set a deliberate image ratio, focal point, and crop for each relevant size;
reserve dimensions to prevent layout shift. Keep meaningful content accessible
with appropriate alternative text. A small image trapped inside a large
decorative frame often signals the wrong hierarchy.

## Responsive composition and interaction

Define what reflows, wraps, becomes a disclosure, or scrolls when space runs
out. Choose breakpoints from content pressure. Narrow screens need a hierarchy
of their own: preserve the primary task and useful context, adjust image crop
and type, and make navigation reachable. Do not merely shrink desktop or hide
required information. For tables, explicitly choose safe horizontal scrolling,
priority columns, or a legible record layout appropriate to comparison needs.

Use content extremes: long names, localized labels, zero results, validation,
loading, and delayed assets where relevant. Prefer minimum dimensions and
content-driven growth over fixed heights that clip translated text. Avoid
visual reordering that makes keyboard or reading order confusing.

Controls communicate their action and current state. Keep focus visible,
targets practical for touch, errors near inputs, and typed work intact during
recovery. Improve vague labels using known product vocabulary without altering
factual claims or business behavior. A visibly interactive affordance must do
what it promises within the prototype's honest mock boundary or the real app.

Motion should explain a change or reinforce a specific moment. Prefer a
coherent transition over identical scroll entrances on every section. Keep
content available without animation, respect reduced motion, and avoid blocking
work while decorative effects finish. Preserve native focus and scrolling
affordances unless the project has an accessible replacement.

Adaptation details and license: [upstream](upstream.md).
