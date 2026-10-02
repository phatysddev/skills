---
title: "Research: Next.js 16 for Agents"
source: "https://docs.phatysd.me/content/nextjs-16-agent-first-guide"
machine_source: "https://docs.phatysd.me/content/nextjs-16-agent-first-guide/markdown"
structured_source: "https://docs.phatysd.me/content/nextjs-16-agent-first-guide/json"
accessed: "2026-09-21"
---

# Research: Next.js 16 for Agents

## Question

What does the Phatysd guide recommend an agent do before and during work in a
Next.js 16 App Router repository?

## Short answer

Treat the repository and installed framework version as the starting point,
make the smallest boundary-aware change, and report only behavior that was
actually verified. The guide is explicitly an agent workflow rather than a
syntax cheat sheet. [Canonical page](https://docs.phatysd.me/content/nextjs-16-agent-first-guide)

## Key findings

### 1. Establish repository and version context first

Before editing, read repository instructions, `package.json`, the lockfile,
Next config, the `app/` tree, and the files touched by the task. Confirm the
installed Next.js version instead of inferring APIs from an older tutorial.
The guide's snapshot observes `next@16.3.5` in its `web-blog` target.
[Markdown source](https://docs.phatysd.me/content/nextjs-16-agent-first-guide/markdown)

### 2. Classify the runtime boundary before changing code

An agent should identify whether the change belongs to a route, Server
Component, Client Component, Server Action, Route Handler, data-access layer,
or `proxy.ts`. Keep components on the server until they need browser APIs,
state, effects, event handlers, or an interactive library; put `'use client'`
on the smallest interactive leaf.
[Markdown source](https://docs.phatysd.me/content/nextjs-16-agent-first-guide/markdown)

### 3. Make the data lifecycle explicit

Before adding a query or fetch, decide whether data is request-time,
prerendered, cached, revalidated, or client-refetched. When Cache Components
are enabled, the guide recommends intentional use of `'use cache'`,
`cacheLife()`, and `cacheTag()`. `updateTag()` is the fit for a Server Action
that needs immediate read-your-writes behavior, while `revalidateTag()` is for
stale-while-revalidate semantics.
[Markdown source](https://docs.phatysd.me/content/nextjs-16-agent-first-guide/markdown)

### 4. Keep authorization at the mutation/data boundary

`proxy.ts` is described as request interception, not the complete authorization
layer. A cookie check may support a coarse redirect, but real session,
ownership, role, input validation, and abuse protection belong in the Server
Action or data-access boundary.
[Markdown source](https://docs.phatysd.me/content/nextjs-16-agent-first-guide/markdown)

### 5. Treat public representations as contracts

For public content, separate the human HTML page from discovery metadata and
machine-readable endpoints. The guide recommends stable canonical URLs,
complete JSON bodies with identity/status/timestamps, parseable Markdown
metadata, real 404s for missing resources, and backward-compatible additions.
[Markdown source](https://docs.phatysd.me/content/nextjs-16-agent-first-guide/markdown)

### 6. Verification must cover behavior, not only build success

`next build` alone is not enough. The guide calls for typecheck, lint, build,
and focused smoke checks covering public pages, protected redirects, invalid
input, missing-resource 404s, mutation/read-after-write behavior, dynamic
route params, and public endpoint exposure. It also separates `Observed`,
`Inferred`, and `Unknown` evidence in the final report.
[Markdown source](https://docs.phatysd.me/content/nextjs-16-agent-first-guide/markdown)

## Agent-ready workflow extracted from the doc

```text
Read AGENTS.md and repository sources of truth
  → confirm installed Next.js version
  → classify the runtime boundary
  → state the data/cache lifecycle
  → enforce auth and validation at the server boundary
  → make the smallest scoped change
  → run static checks and behavior smoke tests
  → report Observed / Inferred / Unknown evidence
```

## Source metadata verified from JSON

The machine-readable representation reports:

- `id`: 23
- `type`: `docs`
- `status`: `published`
- `revision`: 3
- `updatedAt`: `2026-09-19T16:05:12.560Z`
- hierarchy: `Next.js > App Router > Agent-first development`
- topics: Next.js, Next.js 16, App Router, AI agents, TypeScript, Production

[JSON source](https://docs.phatysd.me/content/nextjs-16-agent-first-guide/json)

## Limits and follow-up

- This is a dated research snapshot from 2026-09-19, so framework behavior
  should be checked against the installed repository version and the official
  Next.js documentation before implementation.
- The listed commands and deployment details near the end of the guide are
  specific to its `web-blog` repository target; they should not be copied into
  another repository without checking its `package.json` and deployment setup.
- The guide links to official Next.js documentation for the framework facts;
  those links are the next verification step when implementing a specific API
  or migration.
