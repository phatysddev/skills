# Setup reference: Git initialization and task commits

Inspect Git availability and repository/worktree membership before asking.
Use `git rev-parse --show-toplevel` from the project directory; an enclosing
repository or linked worktree already counts as Git. Do not rely on a local
`.git` directory check or create a nested repository automatically. Distinguish
missing Git, non-repository state and other command errors.

Reuse explicit session decisions and a valid confirmed `## Git Policy` in
`CONTEXT.md`; do not ask again. If sources conflict, resolve the conflicting
choice with the user before changing Git state or overwriting policy.

When no repository exists and no decision has been given, ask once:

> Initialize Git in this project and automatically create a task-scoped commit
> after successful verification in implement-task and auto-implement? This
> enables local commits only; it does not push.

- Yes: run `git init` at the confirmed project root, verify its actual root,
  and persist `initialization: initialized` and `task-commits: required`.
- No: leave Git uninitialized, persist `initialization: declined` and
  `task-commits: disabled`, unless the user explicitly chooses another policy.
- An explicit choice to initialize Git enables required task commits by default;
  explain that consequence in the question. Honor an explicit no-commit override.
- No answer: keep this choice pending; continue independent document work but
  do not claim setup complete or run initialization.

For an existing repository, do not initialize again. If no explicit commit
policy exists, ask whether implementation should automatically commit each
verified task: yes means `required`, no means `disabled`. Preserve an existing
explicit `required`, `allowed` or `disabled` policy rather than asking again.

Persist one section, for example:

```markdown
## Git Policy

Status: confirmed
Repository root: <resolved project/repository root, or none if declined>
Initialization: initialized
Task commits: required
Push: manual
```

`Initialization` is `initialized`, `existing` or `declined`; `Task commits` is
`required`, `allowed` or `disabled`. Record the actual applicable repository
root, especially when the project is inside an enclosing repository. These
fields represent decisions and observed results, not instructions to create a
new repository when implementation runs. Confirmed policy is valid only with
all fields, supported values, and no duplicate/conflicting entries.

If Git is unavailable or initialization fails, record the decision separately
from the failed result and report the remedy; never claim initialized/confirmed
readiness until the selected Git operation succeeds. Do not install Git,
invent identity settings or change global configuration automatically.

Setup creates no initial commit, stages no project files, configures no remote
and performs no push. Implementation owns later task commits. A first task
commit still includes only its owned changes, not the entire pre-existing
project. Check ignore rules and exclude secrets/generated files as usual.

On rerun preserve a confirmed decision, verify current repository membership,
and report drift. A declined project that later has Git needs reconciliation;
missing Git after prior initialization is a problem, not permission to re-init.

Command semantics: [git-init](https://git-scm.com/docs/git-init),
[git-rev-parse](https://git-scm.com/docs/git-rev-parse).
