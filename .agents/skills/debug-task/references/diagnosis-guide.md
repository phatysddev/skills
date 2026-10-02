# Symptom-specific diagnostic loop

## Build the signal

Prefer an existing focused failing test, then an authorized local API/CLI/browser
reproduction or a small temporary harness. Use the smallest available check
that reaches the actual bug pattern. Assert the precise wrong result, not only
that the process exits successfully. Record command, input, environment facts,
expected output, and actual verdict; redact secrets and private data.

Do not install a new browser/framework or silently run stress tests against live
services. Replay only authorized sanitized artifacts locally. A harness cannot
satisfy a required unit/integration/e2e gate in place of its capability/runner.

Separate a real red result from import, syntax, missing fixture, auth, or service
setup errors. The latter may prevent reproduction but do not prove the bug.
Control time, randomness, and mutable fixtures when relevant and supported.
For intermittent failures, report attempts/failures, seed/timing conditions and
limits; retain failing inputs. Never equate zero failures in a short run with proof.

## Minimize and test hypotheses

Reduce one input, caller, or configuration dimension at a time, rerunning after
each change. Keep the original reproduction and any shared-state/concurrency
interaction that carries the failure. Do not simplify a multi-caller bug into
one caller just to obtain a convenient unit test.

Rank plausible explanations and state a discriminating prediction for each.
Use a debugger or targeted boundary observations when available. Keep probes
local, reversible and within the parent's write authority. Tag new diagnostic
instrumentation so it can be removed without touching unrelated diagnostics.
An unexpected result changes the hypothesis, not the expected product behavior.

For performance regressions, measure comparable baselines with the same data,
configuration, warmup, and workload before claiming improvement. Prefer profiling
or query evidence to indiscriminate logging. Do not invent a performance target.
Git/history comparison is read-only by default; any execution in older revisions
must be isolated and authorized, never reset/stash the user's checkout.

## Evidence for the fix

Identify a test seam that retains the real trigger. The owning implementation
agent turns it into a regression test when appropriate, observes the intended
failure, applies the smallest fix, and verifies both the minimized and original
reproduction. Selected test capabilities still run under policy afterwards.
When no suitable seam or environment exists, explain the missing proof and
unblock condition instead of declaring the bug fixed from source inspection.

Stop probes when they repeat without new evidence, need unauthorized effects,
or encounter a product/external blocker. Respect the parent's correction budget;
loading this skill does not reset auto-implement's retry limit.
