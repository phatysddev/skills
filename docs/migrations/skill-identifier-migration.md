# Skill identifier migration

- Status: breaking rename
- Source: [SPEC-006](../specs/SPEC-006-neutral-skill-identifiers.md)

## Mapping

| Retired identifier | Replacement |
| --- | --- |
| `ask-phat` | `ask-workflow` |
| `grill-with-phat` | `grill-workflow` |
| `setup-phat-project` | `setup-project` |
| `to-spec-with-phat` | `write-spec` |
| `review-with-phat` | `code-review` |

## Compatibility

This is a breaking migration. Retired identifiers are not aliases, redirects,
duplicate source directories, or install names. Users must update their skill
references and installation commands to use the replacement identifiers.

## Preserved terminology

`Phat`, `Phat workflow`, `Phatysd`, and `https://docs.phatysd.me/` remain
product, workflow, and source terms. They are not skill identifiers being
removed by this migration.
