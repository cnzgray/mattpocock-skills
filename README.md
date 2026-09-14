# mattpocock-skills for Claude Code

[Matt Pocock's agent skills](https://github.com/mattpocock/skills), the "Skills for Real Engineers" set, packaged as a **native Claude Code plugin**.

This repo is an unofficial personal fork of that project, kept close to upstream and trimmed down to the one thing a Claude Code plugin needs. Skills install as namespaced slash commands, `/mattpocock-skills:<name>`. All 25 upstream skills are here, with their bodies unchanged.

What is not here: the Codex agent metadata, the docs site, the repo authoring notes, the scripts, and the release tooling that only ever mattered inside the upstream repo. If you want those, go upstream.

## Install

```bash
claude plugin marketplace add <owner>/mattpocock-skills
claude plugin install mattpocock-skills@mattpocock
```

Or from inside a session:

```
/plugin marketplace add <owner>/mattpocock-skills
/plugin install mattpocock-skills@mattpocock
```

This fork is not in Anthropic's official marketplace, so you have to add the marketplace first. That `add` step is not optional here: without it, the install step has nothing to resolve `mattpocock-skills@mattpocock` against.

`.claude-plugin/marketplace.json` is what makes this repo its own single-plugin marketplace. It is the supported way to install this repo, or your own fork of it, straight from git. Point `marketplace add` at a clone on disk to try local edits before pushing them.

While editing the skills themselves, skip the install step entirely:

```bash
claude --plugin-dir .
```

## Run `/mattpocock-skills:setup-matt-pocock-skills` once per repo

In your Claude Code session, run [setup-matt-pocock-skills](./skills/engineering/setup-matt-pocock-skills/SKILL.md) as `/mattpocock-skills:setup-matt-pocock-skills`, once in every repo where you want the engineering flows. Plugin skills are always namespaced, so every command in this README is `/mattpocock-skills:<skill>`. It asks you:

- which issue tracker you want (`/mattpocock-skills:triage`, `/mattpocock-skills:to-spec` and `/mattpocock-skills:to-tickets` read it back)
- which labels you apply to issues when you triage them
- where the docs the skills create should live, including the domain doc layout

## The flows

The main flow is **idea to ship**. [ask-matt](./skills/engineering/ask-matt/SKILL.md) is the built-in router if you forget where you are.

```
grill-with-docs → to-spec → to-tickets → implement (tdd + code-review) → commit
```

- **[grill-with-docs](./skills/engineering/grill-with-docs/SKILL.md)**: relentless interview that sharpens the idea and leaves a paper trail behind it (a `GLOSSARY.md` glossary plus ADRs).
- **[to-spec](./skills/engineering/to-spec/SKILL.md)** then **[to-tickets](./skills/engineering/to-tickets/SKILL.md)**: turn the thread into a spec, then into tracer-bullet tickets, each one declaring what blocks it.
- **[implement](./skills/engineering/implement/SKILL.md)**: builds the tickets test-first through [tdd](./skills/engineering/tdd/SKILL.md), then closes out with [code-review](./skills/engineering/code-review/SKILL.md).

On-ramps into that flow:

- **[triage](./skills/engineering/triage/SKILL.md)**: move an inbox of raw issues through a state machine of triage roles.
- **[wayfinder](./skills/engineering/wayfinder/SKILL.md)**: map work too big for one session as a shared set of decision tickets, then resolve them one at a time.
- **[improve-codebase-architecture](./skills/engineering/improve-codebase-architecture/SKILL.md)**: scan a codebase for deepening opportunities, render them as an HTML report, then grill through the one you pick.

The rest, standalone:

- **[grill-me](./skills/productivity/grill-me/SKILL.md)**: get relentlessly interviewed about a plan or design until every branch of the decision tree is resolved.
- **[research](./skills/engineering/research/SKILL.md)**: investigate a question against high-trust primary sources and leave the findings as a cited Markdown file in the repo.
- **[prototype](./skills/engineering/prototype/SKILL.md)**: build a throwaway prototype to answer a design question, either one shareable HTML file or several toggleable UI variations.
- **[diagnosing-bugs](./skills/engineering/diagnosing-bugs/SKILL.md)**: a disciplined diagnosis loop for hard bugs and performance regressions, gated phase by phase.
- **[resolving-merge-conflicts](./skills/engineering/resolving-merge-conflicts/SKILL.md)**: work an in-progress merge or rebase conflict hunk by hunk, resolving by intent traced to each side's source.
- **[wizard](./skills/engineering/wizard/SKILL.md)**: generate an interactive bash wizard for the steps only a human can perform, such as provisioning or credential setup.
- **[handoff](./skills/productivity/handoff/SKILL.md)**: compact the current conversation into a handoff document so another agent can pick the work up.
- **[teach](./skills/productivity/teach/SKILL.md)**: teach you a new skill or concept over multiple sessions, using the current directory as a stateful teaching workspace.
- **[to-questionnaire](./skills/productivity/to-questionnaire/SKILL.md)**: turn a decision you cannot answer alone into a questionnaire for the one person who can.
- **[wait-what](./skills/productivity/wait-what/SKILL.md)**: fire this the moment a message does not land, and the agent re-pitches it in your language, in plain words, with the context you were missing.
- **[writing-for-agents](./skills/productivity/writing-for-agents/SKILL.md)**: rules for writing the documents agents read, including skills and `CLAUDE.md`.
- **[codebase-design](./skills/engineering/codebase-design/SKILL.md)**: shared vocabulary for designing deep modules, meaning a lot of behaviour behind a small interface.
- **[domain-modeling](./skills/engineering/domain-modeling/SKILL.md)**: actively sharpen a project's domain model, challenging terms and stress-testing them against edge cases.
- **[grilling](./skills/productivity/grilling/SKILL.md)**: the reusable interview primitive that `grill-me`, `grill-with-docs`, `triage`, `wayfinder` and `improve-codebase-architecture` are built on.

## Layout

```
.claude-plugin/plugin.json       # plugin manifest; the skills array lists all 25 shipped skills
.claude-plugin/marketplace.json  # makes this repo its own single-plugin marketplace
agents/researcher.md             # read-only investigator: research, grilling fact-finding, wayfinder research tickets, codebase walkthroughs, design-it-twice
agents/standards-reviewer.md     # code-review's Standards axis
agents/spec-reviewer.md          # code-review's Spec axis
skills/engineering/              # 18 skills
skills/productivity/             # 7 skills
```

Sub-agents ship under the same namespace as the skills: `mattpocock-skills:researcher`, `mattpocock-skills:standards-reviewer`, `mattpocock-skills:spec-reviewer`. Renaming the plugin renames both.

## Credit & license

All skill content © Matt Pocock, [MIT](./LICENSE). This repo is an unofficial fork, and upstream is the source of truth: [mattpocock/skills](https://github.com/mattpocock/skills).

Skill bodies are carried over from upstream, with three deliberate divergences: the domain-doc convention is renamed to `GLOSSARY.md` (upstream [PR #876](https://github.com/mattpocock/skills/pull/876)), the prose that says "spawn a sub-agent" names the profiles in `agents/` instead, and the places where two files disagreed about the same convention have been reconciled. Everything else is upstream's. Re-syncing is a diff of `skills/` against the same paths upstream, porting across whatever changed. The manifests in `.claude-plugin/` only need a version bump when upstream ships one.
