# Code review criteria

Read this reference when mapping acceptance criteria, evaluating engineering
risk or verification, or deciding whether an observation meets the finding
threshold.

## Specification behavior

Map every acceptance criterion claimed by the task to implementation behavior
and evidence. A useful working map is:

```text
AC-01 → implementation location → test or observable evidence → result
```

Check that required behavior exists; business rules, permissions, failures,
edge cases, interfaces, and visible states match the spec; and no out-of-scope
behavior was added. Do not approve an AC merely because related code exists;
the behavior must be credibly verifiable.

When the spec cites a prototype, compare accepted behavior such as states,
hierarchy, navigation, and interaction flow. Pixel differences and
prototype-only proposals are not findings. Independently check applicable
Agreed UI Design Requirements cited by the contract; required visual constraints
are not mere taste. Preferences and delegated choices must not become mandatory
findings. The prototype never overrides the requirement, domain context, ADR,
or spec.

## Engineering risk

Review for issues that materially affect correctness or maintainability. Where
relevant, consider data integrity, authorization, security, privacy,
concurrency, failure handling, idempotency, compatibility, state consistency,
resource cleanup, error propagation, regression risk, accessibility,
performance, and repository conventions.

Judge complexity relative to the project. Do not penalize a small project for
lacking infrastructure its requirements do not need. Flag unnecessary service
layers, abstractions, queues, caches, event systems, dependencies, distributed
architecture, or duplicate state only when they create meaningful maintenance
or correctness risk. Do not manufacture findings from generic best practices;
identify a concrete risk in the implementation.

## Verification quality

Inspect existing tests and relevant checks when available and appropriate.
Prefer the narrowest useful repository-supported check. Use the spec's
verification plan to judge whether the check level can prove the acceptance
criteria. Do not demand both unit and end-to-end tests for every task; request a
missing test only when existing tests or observable verification do not
credibly prove material behavior.

Possible checks include targeted unit, integration, end-to-end, authorization,
type, lint, build, repository-specific, or observable manual checks. Do not
invent commands from framework convention. Report each check distinctly as
`Passed`, `Failed`, `Not run`, `Unable to run`, or `Previously recorded only`;
never call an unrun check passed.

Check whether tests exercise the relevant acceptance criteria, business rules,
failure paths, authorization boundaries, and regressions. Flag false confidence
only when tests materially fail to prove required behavior. Do not demand tests
for trivial implementation details merely to increase coverage.

For regression fixes, assess whether the test reaches the original failure
pattern and whether expected results are independent of implementation. Flag
false confidence from mocked-away boundaries or tautological assertions when
it leaves material behavior unverified. Distinguish observed red/green evidence
from plausible coverage, check temporary diagnostics were cleaned up, and do
not demand TDD retroactively for every change. The reviewer does not perform
production refactoring or implement a fix.

Adaptation details and license: [upstream](upstream.md).

## Finding threshold

Report actionable findings supported by credible evidence of incorrect or
missing required behavior, security or data risk, a broken acceptance
criterion, regression, invalid assumption, significant maintainability
problem, or important verification gap.

Do not report personal style preferences, speculative improvements, optional
refactors, unrelated pre-existing problems, or differences allowed by
repository conventions. If intent is uncertain, record a question or unverified
risk rather than a confirmed defect.
