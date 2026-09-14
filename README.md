# mattpocock-skills for Claude Code

[Matt Pocock's agent skills](https://github.com/mattpocock/skills), the "Skills for Real Engineers" set, packaged as a **native Claude Code plugin**.

This repo is an unofficial personal fork of that project, narrowed to the small set of skills I actually use: exactly 7 skills are enabled, whitelisted in `.claude-plugin/plugin.json`. The other 18 upstream skills are not deleted; they are parked out of the manifest under `skills/_shelved/` (see [Shelved](#shelved)). Skills install as namespaced slash commands, `/mattpocock-skills:<name>`.

What is not here: the Codex agent metadata, the docs site, the repo authoring notes, the scripts, and the release tooling that only ever mattered inside the upstream repo. If you want those, go upstream.

## Install

```bash
claude plugin marketplace add cnzgray/mattpocock-skills
claude plugin install mattpocock-skills@mattpocock
```

Or from inside a session:

```
/plugin marketplace add cnzgray/mattpocock-skills
/plugin install mattpocock-skills@mattpocock
```

This fork is not in Anthropic's official marketplace, so you have to add the marketplace first. That `add` step is not optional here: without it, the install step has nothing to resolve `mattpocock-skills@mattpocock` against.

`.claude-plugin/marketplace.json` is what makes this repo its own single-plugin marketplace. It is the supported way to install this repo, or your own fork of it, straight from git. Point `marketplace add` at a clone on disk to try local edits before pushing them.

While editing the skills themselves, skip the install step entirely:

```bash
claude --plugin-dir .
```

## Run `/mattpocock-skills:mattpocock-skills-setup` once per repo

In your Claude Code session, run [mattpocock-skills-setup](./skills/engineering/mattpocock-skills-setup/SKILL.md) as `/mattpocock-skills:mattpocock-skills-setup`, once in every repo where you want the engineering flows. Plugin skills are always namespaced, so every command in this README is `/mattpocock-skills:<skill>`. It asks you:

- which issue tracker you want (`to-spec` and `to-tickets` read it back)
- which label vocabulary `to-tickets` applies to issues
- where the docs the skills create should live, including the domain doc layout

## The flows

The main flow is **idea to ship**:

```
grilling → to-spec → to-tickets → implement (tdd + code-review) → commit
```

- **[grilling](./skills/productivity/grilling/SKILL.md)**: a relentless interview that sharpens the plan, the design, or the idea. As it goes, the interview decides whether the conversation has earned a paper trail, and writes `GLOSSARY.md` entries and ADRs only when something actually got settled.
- **[to-spec](./skills/engineering/to-spec/SKILL.md)**: turn the shared understanding into a spec.
- **[to-tickets](./skills/engineering/to-tickets/SKILL.md)**: turn the spec into tracer-bullet tickets, each one declaring what blocks it.
- **[implement](./skills/engineering/implement/SKILL.md)**: builds the tickets test-first through [tdd](./skills/engineering/tdd/SKILL.md), then closes out with [code-review](./skills/engineering/code-review/SKILL.md).

## Shelved

The other 18 upstream skills are not deleted. They still live in this repo under `skills/_shelved/engineering/` and `skills/_shelved/productivity/`, bodies untouched. `plugin.json`'s `skills` array is a whitelist: a skill whose folder exists but whose path is not in the array simply does not load. To re-enable a shelved skill, add its path (for example `./skills/_shelved/engineering/triage`) back to the array.

## Layout

```
.claude-plugin/plugin.json       # plugin manifest; the skills array whitelists the 7 enabled skills
.claude-plugin/marketplace.json  # makes this repo its own single-plugin marketplace
skills/engineering/              # the 6 enabled engineering skills
skills/productivity/             # grilling, the enabled productivity skill
skills/_shelved/engineering/     # 10 shelved engineering skills, on disk but not in the manifest
skills/_shelved/productivity/    # 5 shelved productivity skills, on disk but not in the manifest
```

## Credit & license

All skill content © Matt Pocock, [MIT](./LICENSE). This repo is an unofficial fork, and upstream is the source of truth: [mattpocock/skills](https://github.com/mattpocock/skills).

Skill bodies are carried over from upstream, with three deliberate divergences: the domain-doc convention is renamed to `GLOSSARY.md` (upstream [PR #876](https://github.com/mattpocock/skills/pull/876)), the places where two files disagreed about the same convention have been reconciled, and this fork is narrowed to 7 enabled skills with the other 18 parked under `skills/_shelved/` out of the manifest. Everything else is upstream's. Re-syncing is a diff of `skills/` (enabled and shelved) against the same paths upstream, porting across whatever changed. The manifests in `.claude-plugin/` only need a version bump when upstream ships one.
