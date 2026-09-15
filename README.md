# mattpocock-skills for Claude Code

[Matt Pocock's agent skills](https://github.com/mattpocock/skills), the "Skills for Real Engineers" set, packaged as a **native Claude Code plugin**.

This repo is an unofficial personal fork of that project, narrowed to the small set of skills I actually use: exactly 9 skills are enabled, whitelisted in `.claude-plugin/plugin.json`. The other 14 upstream skills are not deleted; they are parked out of the manifest under `skills/_shelved/` (see [Shelved](#shelved)). Skills install as namespaced slash commands, `/mattpocock-skills:<name>`.

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
grill-with-docs → to-spec → to-tickets → implement (tdd + code-review) → commit
```

- **[grill-with-docs](./skills/engineering/grill-with-docs/SKILL.md)**: a relentless interview that sharpens the plan, the design, or the idea, and leaves a paper trail behind it, keeping the `GLOSSARY.md` entries and ADRs the interview actually earned.
- **[to-spec](./skills/engineering/to-spec/SKILL.md)**: turn the shared understanding into a spec.
- **[to-tickets](./skills/engineering/to-tickets/SKILL.md)**: turn the spec into tracer-bullet tickets, each one declaring what blocks it.
- **[implement](./skills/engineering/implement/SKILL.md)**: builds the tickets test-first through [tdd](./skills/engineering/tdd/SKILL.md), then closes out with [code-review](./skills/engineering/code-review/SKILL.md).

Off the flow but always available:

- **[grill-me](./skills/productivity/grill-me/SKILL.md)**: the same interview with no paper trail at all, for a plan, a design, or a piece of writing with no repo under it.
- **[wait-what](./skills/productivity/wait-what/SKILL.md)**: fire this the moment a message does not land, mid-conversation or inside any other skill, and the agent re-pitches it in your language, in plain words, with the context you were missing. `grill-with-docs` is the upfront cure; this is the one that works after the fact.

## Shelved

The other 14 upstream skills are not deleted. They still live in this repo under `skills/_shelved/engineering/` and `skills/_shelved/productivity/`, bodies untouched. `plugin.json`'s `skills` array is a whitelist: a skill whose folder exists but whose path is not in the array simply does not load. To re-enable a shelved skill, add its path (for example `./skills/_shelved/engineering/triage`) back to the array.

## Layout

```
.claude-plugin/plugin.json       # plugin manifest; the skills array whitelists the 9 enabled skills
.claude-plugin/marketplace.json  # makes this repo its own single-plugin marketplace
skills/engineering/              # the 7 enabled engineering skills
skills/productivity/             # grill-me and wait-what, the enabled productivity skills
skills/_source/                  # shared injection sources, pulled into templates by path; every
                                 # shared unit gets its own subdirectory, e.g. grilling/, domain-modeling/
skills/_shelved/engineering/     # 10 shelved engineering skills, on disk but not in the manifest
skills/_shelved/productivity/    # 4 shelved productivity skills, on disk but not in the manifest
scripts/generate-skills.py       # renders every committed X.tmpl into the file X beside it
```

## Maintaining the generated skills

Generated files follow one convention: any committed `X.tmpl` renders to the file `X` beside it, so `skills/productivity/grill-me/SKILL.md.tmpl` produces that skill's `SKILL.md`. Inside a template, a line that is exactly `{{include:path/relative/to/the/repo/root}}` is replaced by the full contents of that file (it must end with a newline, and the placeholder must be the whole line); every other line is copied through unchanged. That is how `grill-me` and `grill-with-docs` share the interview in `skills/_source/grilling/grilling-protocol.md` while each keeps its own frontmatter and closing section.

Edit a template or any file it includes, run `python3 scripts/generate-skills.py`, and commit the rendered files: plugin distribution reads the committed `SKILL.md` files and runs no build step.

Shared sources live under `skills/_source/`, one subdirectory per shared unit: `skills/_source/grilling/` holds the interview shared by `grill-me` and `grill-with-docs`, and `skills/_source/domain-modeling/` holds the domain-modeling body plus its `GLOSSARY-FORMAT.md` and `ADR-FORMAT.md` siblings. When an included source links to a sibling file in its own directory (a relative link like `[GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md)`), the consuming skill's directory needs one single-line shim template per sibling so that link resolves inside the consuming directory. For example `skills/engineering/grill-with-docs/GLOSSARY-FORMAT.md.tmpl` containing only `{{include:skills/_source/domain-modeling/GLOSSARY-FORMAT.md}}` renders that sibling beside the consuming `SKILL.md`, which is what the relative link resolves against at read time.

## Credit & license

All skill content © Matt Pocock, [MIT](./LICENSE). This repo is an unofficial fork, and upstream is the source of truth: [mattpocock/skills](https://github.com/mattpocock/skills).

Skill bodies are carried over from upstream, with three deliberate divergences: the domain-doc convention is renamed to `GLOSSARY.md` (upstream [PR #876](https://github.com/mattpocock/skills/pull/876)), the places where two files disagreed about the same convention have been reconciled, and this fork is narrowed to 8 enabled skills with the other 14 parked under `skills/_shelved/` out of the manifest. Everything else is upstream's. Re-syncing is a diff of `skills/` (enabled and shelved) against the same paths upstream, porting across whatever changed. The manifests in `.claude-plugin/` only need a version bump when upstream ships one.
