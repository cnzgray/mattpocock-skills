# mattpocock-skills for Claude Code

[Matt Pocock's agent skills](https://github.com/mattpocock/skills), the "Skills for Real Engineers" set, packaged as a **native Claude Code plugin**.

This repo is an unofficial personal fork of that project, narrowed to the working set of skills I actually use: 21 skills are enabled, whitelisted in [`plugin/.claude-plugin/plugin.json`](./plugin/.claude-plugin/plugin.json) — 16 engineering plus 5 productivity. The 2 upstream skills I did not keep are not deleted; they are parked out of the manifest under [`dev/shelved/`](./dev/shelved) (see [Shelved](#shelved)). Skills install as namespaced slash commands, `/mattpocock-skills:<name>`.

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
claude --plugin-dir ./plugin
```

## Run `/mattpocock-skills:mattpocock-skills-setup` once per repo

In your Claude Code session, run [mattpocock-skills-setup](./plugin/skills/engineering/mattpocock-skills-setup/SKILL.md) as `/mattpocock-skills:mattpocock-skills-setup`, once in every repo where you want the engineering flows. Plugin skills are always namespaced, so every command in this README is `/mattpocock-skills:<skill>`. It asks you:

- which issue tracker you want (`to-spec` and `to-tickets` read it back)
- which label vocabulary `to-tickets` applies to issues
- where the docs the skills create should live, including the domain doc layout

## The flows

The main flow is **idea to ship**:

```
grill-with-docs → to-spec → to-tickets → implement (tdd + code-review) → commit
```

- **[grill-with-docs](./plugin/skills/engineering/grill-with-docs/SKILL.md)**: a relentless interview that sharpens the plan, the design, or the idea, and leaves a paper trail behind it, keeping the `GLOSSARY.md` entries and ADRs the interview actually earned.
- **[to-spec](./plugin/skills/engineering/to-spec/SKILL.md)**: turn the shared understanding into a spec.
- **[to-tickets](./plugin/skills/engineering/to-tickets/SKILL.md)**: turn the spec into tracer-bullet tickets, each one declaring what blocks it.
- **[implement](./plugin/skills/engineering/implement/SKILL.md)**: builds the tickets test-first through [tdd](./plugin/skills/engineering/tdd/SKILL.md), then closes out with [code-review](./plugin/skills/engineering/code-review/SKILL.md).

Off the flow but always available:

- **[grill-me](./plugin/skills/productivity/grill-me/SKILL.md)**: the same interview with no paper trail at all, for a plan, a design, or a piece of writing with no repo under it.
- **[wait-what](./plugin/skills/productivity/wait-what/SKILL.md)**: fire this the moment a message does not land, mid-conversation or inside any other skill, and the agent re-pitches it in your language, in plain words, with the context you were missing. `grill-with-docs` is the upfront cure; this is the one that works after the fact.

## Shelved

The 2 skills I did not keep are not deleted. They still live in this repo under `dev/shelved/engineering/` and `dev/shelved/productivity/`, bodies untouched. `plugin.json`'s `skills` array is a whitelist: a skill whose folder exists under `plugin/` but whose path is not in the array simply does not load. Only `plugin/` is distributed, though, so the array is not the whole story: to re-enable a shelved skill, move its directory into `plugin/skills/` **and** add its path (for example `./skills/engineering/ask-matt`) back to the array. Adding the array entry alone would point at a path that is not in the plugin root at all.

## Layout

```
.claude-plugin/marketplace.json  # makes this repo its own single-plugin marketplace; points at ./plugin
plugin/.claude-plugin/plugin.json # plugin manifest; the skills array whitelists the 21 enabled skills
plugin/skills/engineering/       # the 16 enabled engineering skills
plugin/skills/productivity/      # the 5 enabled productivity skills
dev/templates/skills/            # the 12 *.tmpl templates, mirroring the plugin tree
dev/source/                      # shared injection sources, pulled into templates by path; every
                                 # shared unit gets its own subdirectory, e.g. grilling/, domain-modeling/
dev/shelved/engineering/         # the shelved engineering skill, on disk but not in the manifest
dev/shelved/productivity/        # the shelved productivity skill, on disk but not in the manifest
scripts/generate-skills.py       # renders dev/templates/**.tmpl into the mirrored file under plugin/
AGENTS.md                        # repo authoring notes (author-side, never distributed)
README.md                        # this file (author-side, never distributed)
```

Only `plugin/` is the plugin root. Everything else at the repo root — `dev/`, `scripts/`, `docs/`, `AGENTS.md`, `README.md` — stays outside it, so Claude Code's recursive copy of the plugin root never picks it up.

## Maintaining the generated skills

Templates live apart from what they render. The rule is one mapping wide: a committed template at `dev/templates/<plugin-relative-path>.tmpl` renders to `plugin/<plugin-relative-path>`, so `dev/templates/skills/productivity/grill-me/SKILL.md.tmpl` produces `plugin/skills/productivity/grill-me/SKILL.md`. The `dev/templates/` tree mirrors the plugin tree exactly; a template is never a sibling of its own rendered output. Inside a template, a line that is exactly `{{include:path/relative/to/the/repo/root}}` is replaced by the full contents of that file (it must end with a newline, and the placeholder must be the whole line); every other line is copied through unchanged. Include paths are still resolved against the repo root, so shared text is named as `dev/source/<path>`. That is how `grill-me` and `grill-with-docs` share the interview in `dev/source/grilling/grilling-protocol.md` while each keeps its own frontmatter and closing section.

Edit a template or any file it includes, run `python3 scripts/generate-skills.py`, and commit the rendered files: plugin distribution reads the committed `SKILL.md` files under `plugin/` and runs no build step. The script refuses to run if it finds a `*.tmpl` outside `dev/templates/`, or one still sitting under `plugin/` after rendering.

Shared sources live under `dev/source/`, one subdirectory per shared unit: `dev/source/grilling/` holds the interview shared by `grill-me` and `grill-with-docs`, and `dev/source/domain-modeling/` holds the domain-modeling body plus its `GLOSSARY-FORMAT.md` and `ADR-FORMAT.md` siblings. When an included source links to a sibling file in its own directory (a relative link like `[GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md)`), the consuming skill's directory needs one single-line shim template per sibling so that link resolves inside the consuming directory. For example `dev/templates/skills/engineering/grill-with-docs/GLOSSARY-FORMAT.md.tmpl` containing only `{{include:dev/source/domain-modeling/GLOSSARY-FORMAT.md}}` renders that sibling beside the consuming `SKILL.md`, which is what the relative link resolves against at read time.

## Credit & license

All skill content © Matt Pocock, [MIT](./LICENSE). This repo is an unofficial fork, and upstream is the source of truth: [mattpocock/skills](https://github.com/mattpocock/skills).

Skill bodies are carried over from upstream, with three deliberate divergences: the domain-doc convention is renamed to `GLOSSARY.md` (upstream [PR #876](https://github.com/mattpocock/skills/pull/876)), the places where two files disagreed about the same convention have been reconciled, and this fork is narrowed to 21 enabled skills with the other 2 parked under `dev/shelved/` out of the manifest. Everything else is upstream's. Re-syncing is a diff of `plugin/skills/` (enabled) and `dev/shelved/` (shelved) against the same paths upstream, porting across whatever changed. The manifests in `.claude-plugin/` and `plugin/.claude-plugin/` only need a version bump when upstream ships one.
