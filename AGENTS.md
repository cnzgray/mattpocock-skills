# AGENTS.md

## Composing skills: inline, don't call

A skill must be self-sufficient. Inline shared text through the template mechanism, never as a hand copy: add a template at `dev/templates/<plugin-relative-path>.tmpl` — the mirror of the rendered file's path under `plugin/`, not a sibling of it — pull the protocol in with a standalone `{{include:dev/source/<path>}}` line, run `scripts/generate-skills.py`, and commit the rendered file under `plugin/`. One `{{include}}` per need keeps a single source of truth (e.g. `improve-codebase-architecture` inlines the grilling protocol via `{{include:dev/source/grilling/grilling-protocol.md}}` instead of reaching for a skill call).
Do NOT write "Call the Skill tool with …" inside a skill body. Chaining skills like method calls turns the agent's on-demand judgement into a hard-coded step, nests the target's full text inside this skill's run, and breaks the flow whenever the target gets shelved or folded. A skill is consumed exactly two ways: a human invokes it by name, or the agent fires it on its own judgement, driven by the skill's `description` trigger words — never because another skill's body commanded it. This repo has zero such calls. Everything a skill needs every run is inlined through the template mechanism; reference shared across skills lives in `dev/source/` with one rendered copy per consuming skill.

## Issue tracker, triage labels and domain docs

### Issue tracker

Issues and specs live as local markdown files under `.scratch/<feature-slug>/` (`spec.md` plus `issues/<NN>-<slug>.md`). See `docs/agents/issue-tracker.md`.

### Triage labels

Default canonical vocabulary: state roles `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`; category roles `bug`, `enhancement`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `GLOSSARY.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.