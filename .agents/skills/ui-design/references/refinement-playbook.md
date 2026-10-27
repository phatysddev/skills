# Refinement playbook

Use only the operation needed by the request. Preserve incumbent identity,
required content, behavior, and all surfaces outside scope. The visual brief
wins over aesthetic defaults. Read the relevant [craft](design-craft.md)
section for implementation detail; use [critique](visual-critique.md) to verify.

## Polish

Inspect the whole requested path, its tokens, components, states, and actual
render before editing. Classify each problem: wrong composition, missing state,
existing-token drift, shared-component drift, or local detail. Fix the cause at
the narrowest level rather than adding overrides to conceal it.

Prioritize blocked/misleading actions, clipped content and recovery paths,
then hierarchy and responsive structure, then type/spacing/color consistency,
then optical alignment and motion. Check all parts of the path rather than
perfecting one corner. A conceptual mismatch may need an explicitly scoped
redesign; a polish request alone does not replace the design world.

Batch corrections from a rendered inspection. Recheck the same states and
widths after material changes, including neighbors affected by shared styles.
Keep a compact before/finding/correction/evidence record. Avoid an unbounded
search for cosmetic differences after the requested weaknesses are resolved.

## Emphasis and simplification

First locate the competing emphasis: color, weight, scale, imagery, containers,
motion, or repeated information. Name the element that should lead and the
parts that should support it. Change relationships rather than every token.

| Request | Useful intervention | Preserve / verify |
| --- | --- | --- |
| Bolder | Strengthen one focal element through scale contrast, crop, voice, composition, or an established accent; remove competition. | Recognizable identity, surrounding layout and working actions; not an automatic new font or effects stack. |
| Quieter | Reduce repeated fills, heavy borders, redundant icon tiles, and competing emphasis; keep a deliberate primary anchor. | Readable contrast, status distinctions and usable controls; not uniformly tiny or faint text. |
| Simpler | Consolidate duplicate explanations, flatten unnecessary nesting, clarify grouping and action priority. | Required data/actions remain findable. New disclosure must retain a clear access path and appropriate keyboard behavior. |

On operational screens, calmer does not necessarily mean more padding. Compare
records visible, scroll distance, label readability and reachable actions. On
marketing or creative surfaces, stronger character can come from a decisive
artifact and composition rather than more badges. Do not substitute your taste
for requested gradients, eras, palettes or materials.

Record what moved, receded or was removed and why. Removing required fields,
workflow steps, or product functions needs product authorization; a visual
simplification does not grant it. Do not hide essential information merely to
increase the visible-row count or improve a screenshot.

## Type-color-layout

Diagnose each requested axis before choosing values:

- **Type:** identify current families and roles; compare adjacent hierarchy,
  measure, wrapping, weight and actual language. Change roles consistently,
  loading only needed assets when authorized. Check long Thai/English strings,
  fallback and user text scaling; do not replace identity for a font-tuning task.
- **Color:** map action, selection, status, foreground and surface meanings.
  Reuse semantic tokens and measure actual state/background pairs. Introduce
  brand expression where it directs attention, not on every region. Check
  supported themes; do not require dark mode when it is outside the product.
- **Layout:** name reading/task order, related groups, primary/secondary areas,
  density and narrow-screen changes. Improve proximity and rhythm before
  adding containers. Compare full-day overview against readable event detail,
  or simultaneous queue context against a wider workspace; choose for the task,
  not a universal ban on sidebars, cards, or scrolling regions.

Use a few role tokens rather than one-off values for each element. Optical
corrections follow rendering. Verify the relevant axis plus side effects:
larger type may break controls, quieter borders may hide selection, and a
denser table may remove useful context. Do not interpret a raw pixel count as
proof of beauty or usability.

Adaptation provenance and license: [upstream](upstream.md).
