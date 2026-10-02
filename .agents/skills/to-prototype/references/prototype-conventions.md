# To Prototype reference: prototype conventions

Read this reference when creating or reviewing prototype files. It contains the location, mock boundaries, revision IDs, navigation metadata, visual conventions, responsive/accessibility expectations, and traceability rules.

## Contents

- [Prototype location](#prototype-location)
- [Prototype boundaries](#prototype-boundaries)
- [Page revision IDs](#page-revision-ids)
- [Navigation IDs](#navigation-ids)
- [Revision model](#revision-model)
- [Visual design](#visual-design)
- [Responsive behavior](#responsive-behavior)
- [Accessibility](#accessibility)
- [Existing prototype](#existing-prototype)
- [Requirement traceability](#requirement-traceability)

## Prototype location

Create prototype files under:

```text
docs/assets/prototype/
```

Use:

```text
docs/assets/prototype/
├── index.html
├── <page>.html
├── style.css
└── script.js
```

Use `index.html` for the primary/home page.

Examples:

```text
docs/assets/prototype/
├── index.html
├── about.html
├── contact.html
├── booking.html
├── style.css
└── script.js
```

Do not introduce a build system for the prototype.

Prefer plain:

* HTML;
* CSS;
* JavaScript.

The prototype should be viewable by opening `index.html` or using any simple static server.

## Prototype boundaries

Prototype enough behavior to communicate the intended experience.

Use mock or temporary client-side state for interactions such as:

* navigation;
* tabs;
* accordions;
* dropdowns;
* modal dialogs;
* form states;
* filters;
* mock search;
* fake submission confirmation;
* loading states;
* empty states;
* validation examples.

Do not connect to:

* production databases;
* real authentication;
* payment providers;
* external APIs;
* production services;

unless the user explicitly requests a separate integration prototype.

Mock these interactions instead.

## Page revision IDs

Every prototype page must have a stable page name and revision ID.

Use:

```text
<page>-v<number>
```

Examples:

```text
home-v1
about-v1
contact-v1
booking-v1
dashboard-v1
```

Add both attributes to the page root:

```html
<body
  data-prototype-page="home"
  data-prototype-id="home-v1"
>
```

Every page must visibly display its current prototype ID in a small prototype control bar at the top.

Example:

```text
PHAT PROTOTYPE
Page: Home
ID: home-v1
```

The control bar is prototype tooling, not production UI.

## Navigation IDs

When the prototype contains navigation, make page IDs visible so the user can refer to an exact page revision.

For example:

```text
Home
home-v1

About
about-v1

Contact
contact-v1
```

Also encode the target ID in markup:

```html
<a
  href="about.html"
  data-prototype-target="about-v1"
>
  About
  <small>about-v1</small>
</a>
```

This allows commands such as:

```text
$edit-prototype home-v1
```

without relying on filenames alone.

## Revision model

The revision ID identifies the current revision of one page.

Initial creation uses:

```text
home-v1
```

When `$edit-prototype` makes a meaningful requested change to that page:

```text
home-v1
→
home-v2
```

The HTML file may remain:

```text
index.html
```

The revision is represented by prototype metadata, not the filename.

Version control is the preferred historical record when available.

Do not create copied files such as:

```text
home-v1.html
home-v2.html
home-v3.html
```

unless the user explicitly requests archived visual alternatives.

## Visual design

Produce a polished but intentionally lightweight prototype.

Prefer:

* clear hierarchy;
* consistent spacing;
* readable typography;
* restrained color usage;
* reusable CSS variables;
* responsive layouts;
* meaningful empty states;
* visible interaction states;
* semantic HTML.

Avoid common AI-generated UI problems such as:

* excessive gradients;
* unnecessary glassmorphism;
* every section placed inside cards;
* random border radii;
* inconsistent spacing;
* giant headings without hierarchy;
* unnecessary visual decoration;
* excessive animation.

Follow existing brand guidance, confirmed Design Direction, and applicable
Agreed UI Design Requirements. The defaults above do not override explicit
user-confirmed styling. If no direction or custom preference exists, choose a
restrained provisional treatment appropriate to the content rather than
inventing elaborate branding.

## Responsive behavior

Prototype at least:

* mobile;
* desktop.

Account for tablet when the layout meaningfully changes.

Navigation, forms, tables, dialogs, and primary actions should remain understandable at small widths.

Do not attempt pixel-perfect responsiveness for every possible breakpoint.

## Accessibility

Use reasonable prototype-level accessibility:

* semantic elements;
* form labels;
* keyboard-operable controls where practical;
* meaningful button text;
* reasonable heading hierarchy;
* visible focus states;
* sufficient basic contrast.

The prototype is not a substitute for production accessibility verification.

## Existing prototype

If `docs/assets/prototype/` already exists, inspect it before creating anything.

Do not overwrite an existing prototype with a new design merely because `$to-prototype` was invoked again.

If the requested change targets existing prototype pages, prefer:

```text
$edit-prototype
```

Use `$to-prototype` to add a new coherent prototype surface only when appropriate.

## Requirement traceability

Prototype only behavior reasonably supported by:

* agreed requirements;
* agreed domain context;
* ADRs;
* an existing spec;
* explicit user direction.

Visual details may be proposed for usability.

Business behavior must not be invented.

When a prototype requires an unresolved choice, clearly distinguish:

```text
Requirement-backed
Prototype proposal
Open question
```

Do not silently promote a prototype proposal into an agreed requirement.
