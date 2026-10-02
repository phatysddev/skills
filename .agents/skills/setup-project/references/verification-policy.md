# Setup reference: project verification policy

Use this reference when `setup-project` asks for, validates, or persists the
project's implementation verification policy.

## Owned location

The policy belongs in the project-owned `CONTEXT.md` under exactly one heading:

```markdown
## Verification Policy
```

Do not create a second policy document or duplicate the section in another
project source. Do not put per-task overrides in this section.

## Canonical shape

After explicit confirmation of all four choices, persist this Markdown shape,
replacing the date and mode values with the confirmed values:

```markdown
## Verification Policy

- Status: confirmed
- Source: explicit setup confirmation
- Confirmed at: YYYY-MM-DD

| Capability | Mode |
| --- | --- |
| `unit-test` | `auto` |
| `integration-test` | `off` |
| `e2e-test` | `off` |
| `code-review` | `required` |
```

The four capability rows are independent. The modes mean:

* `auto` — run when the capability is relevant and its installed skill and
  repository-supported runner are available; otherwise record a non-blocking
  skip reason;
* `required` — run when relevant and block the task when the capability or
  runner cannot be resolved, is unavailable, or fails; and
* `off` — do not automatically invoke the capability and record the
  configured mode. For `code-review`, an explicit user-invoked `$code-review`
  remains available as the manual final review stage.

A policy is valid only when it has `Status: confirmed`, an explicit source,
one row for each of the four capability identifiers, and exactly one mode from
`auto`, `required`, or `off` for each row. A missing, duplicated, or invalid row
is unresolved.

## First run and rerun behavior

On first setup, ask for all four values before writing the section. Repeat the
complete set for confirmation and write the section only after the user
confirms it. Never fill an unanswered choice with a default.

On a later setup run, a valid confirmed section is authoritative and is reused
without asking again or changing its values. Setup may report the reused policy
but must preserve unrelated `CONTEXT.md` content.

If the section is present but malformed, do not interpret missing values as
`off` and do not silently repair it. Keep the unresolved content visible,
ask the user to confirm all four values, and replace the section only after
that complete confirmation.
