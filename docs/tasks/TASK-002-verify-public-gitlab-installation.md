# TASK-002: Public GitLab discovery and Codex installation work

- Status: done
- Spec: [SPEC-001](../specs/SPEC-001-publish-phat-skill-pack.md)

## Goal

An installer can discover the ten skills — seven core workflow skills and
three optional prototype skills — from the public GitLab source and install
either `ask-phat` or the complete skill pack for Codex without source changes.
Read [SPEC-001](../specs/SPEC-001-publish-phat-skill-pack.md), [the requirement](../requirement.md), and [repository context](../../CONTEXT.md) for the authoritative contract. The public source is `https://gitlab.com/phatysd.dev/skills`.

## Blocked by

- None — TASK-001 is complete, the public source is reachable, and the earlier
  stale-public-revision blocker is resolved.

## Todo

- [x] AC-01 — Run
  `NPM_CONFIG_YES=true npx skills@latest add https://gitlab.com/phatysd.dev/skills --list`;
  the public discovery command exited 0 and listed all 10 expected skill
  names.
- [x] AC-02 — Run
  `NPM_CONFIG_YES=true npx skills@latest add https://gitlab.com/phatysd.dev/skills --skill ask-phat --agent codex --yes`
  in `/tmp/phat-skills-single.JHOovj`; the command exited 0, installed only
  `ask-phat`, and the installed `SKILL.md` matched the local source.
- [x] AC-03 — Run
  `NPM_CONFIG_YES=true npx skills@latest add https://gitlab.com/phatysd.dev/skills --skill '*' --agent codex --yes`
  in `/tmp/phat-skills-all.mZCFCG`; the command exited 0, installed all 10
  expected skill directories, and every installed `SKILL.md` matched the
  local source.
- [x] Confirm installation checks did not modify the source skill
  instructions. The earlier stale-public-revision observation at `3cefed6`
  is superseded by the current public-source checks.
- [x] Review approved — working tree evidence against SPEC-001 and `HEAD`;
  AC-01–AC-03 verified; public discovery, single/full installation parity,
  metadata checks, checklist-contract checks, and `git diff --check` passed;
  no findings.
- [x] Task-scoped commit check — not applicable: TASK-002 is verification-only
  and introduced no task-scoped implementation changes. Unrelated `README.md`
  and `LICENSE` changes were preserved and not attributed to this task; no push
  was performed.
