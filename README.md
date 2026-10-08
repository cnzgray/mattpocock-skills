# mattpocock-skills for Claude Code

[Matt Pocock's agent skills](https://github.com/mattpocock/skills), the "Skills for Real Engineers" set, packaged as a **native Claude Code plugin**.

This repo is an unofficial personal fork of that project, narrowed to the working set of skills I actually use: 25 skills are enabled, whitelisted in [`plugin/.claude-plugin/plugin.json`](./plugin/.claude-plugin/plugin.json) — 19 engineering plus 6 productivity. Skills install as namespaced slash commands, `/mattpocock-skills:<name>`.

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
- **[ask-matt](./plugin/skills/engineering/ask-matt/SKILL.md)**: the router. Describe your situation and it points you at the skill or flow that fits, plus the five options at a phase boundary.
- **[to-questionnaire](./plugin/skills/productivity/to-questionnaire/SKILL.md)**: when the thing blocking you is in someone else's head, it interviews you about the send and writes them a questionnaire to fill in.

## Skills

All 25 enabled skills, grouped the way upstream splits them ([`.agents/invocation.md`](https://github.com/mattpocock/skills/blob/main/.agents/invocation.md)): the one axis that matters is **who can reach a skill**. Every command is namespaced, so you type `/mattpocock-skills:<name>`.

### User-invoked — only you can trigger these

`disable-model-invocation: true`. The model cannot load them, their description never enters context, and Claude Code refuses the call and tells the model not to reproduce the steps another way. Reach them by typing `/mattpocock-skills:<name>`.

**Engineering** — the idea-to-ship flow, plus its upkeep:

- **[ask-matt](./plugin/skills/engineering/ask-matt/SKILL.md)**: ask which skill or flow fits your situation — a router over the skills in this plugin, and over the five options at a phase boundary.
- **[grill-with-docs](./plugin/skills/engineering/grill-with-docs/SKILL.md)**: a relentless interview that sharpens the plan, the design, or the idea, and builds this repo's domain docs as it goes: `GLOSSARY.md` entries and ADRs.
- **[to-spec](./plugin/skills/engineering/to-spec/SKILL.md)**: turn the current conversation into a spec and publish it to the issue tracker. No interview, just synthesis of what you already discussed.
- **[to-tickets](./plugin/skills/engineering/to-tickets/SKILL.md)**: break a plan, spec, or conversation into tracer-bullet tickets, each declaring its blocking edges, on the configured tracker.
- **[implement](./plugin/skills/engineering/implement/SKILL.md)**: build the work described by a spec or set of tickets, test-first, closing out with a review before committing.
- **[implement-spec](./plugin/skills/engineering/implement-spec/SKILL.md)**: implement a whole spec on one integration branch — the tickets as a task graph, implementer subagents working the ready frontier in parallel, one code review at the end.
- **[wayfinder](./plugin/skills/engineering/wayfinder/SKILL.md)**: plan a chunk of work too big for one agent session as a shared map of decision tickets, resolved one at a time until the route is clear.
- **[triage](./plugin/skills/engineering/triage/SKILL.md)**: move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready briefs.
- **[improve-codebase-architecture](./plugin/skills/engineering/improve-codebase-architecture/SKILL.md)**: scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.
- **[retro](./plugin/skills/engineering/retro/SKILL.md)**: close the loop after a build — suggest changes to the agent's environment rather than the code: navigation pointers, deterministic checks, coding standards, steering files, tooling. Most severe first.
- **[mattpocock-skills-setup](./plugin/skills/engineering/mattpocock-skills-setup/SKILL.md)**: configure this repo for the engineering skills — issue tracker, triage label vocabulary, domain doc layout. Run once per repo.

**Productivity**:

- **[grill-me](./plugin/skills/productivity/grill-me/SKILL.md)**: the same relentless interview, with no paper trail. For a plan, a design, or a piece of writing with no repo under it.
- **[wait-what](./plugin/skills/productivity/wait-what/SKILL.md)**: fire this the moment a message does not land, mid-conversation or inside any other skill, and the agent re-pitches it in your language, in plain words, with the context you were missing.
- **[handoff](./plugin/skills/productivity/handoff/SKILL.md)**: compact the current conversation into a handoff document so a fresh agent can pick up the work. Takes a hint for what the next session is for.
- **[teach](./plugin/skills/productivity/teach/SKILL.md)**: teach you a new skill or concept within this workspace, over multiple sessions. Takes the topic as its argument.
- **[to-questionnaire](./plugin/skills/productivity/to-questionnaire/SKILL.md)**: turn a decision you can't answer alone into a questionnaire for the person who holds the knowledge, targeting the gap between what they know and what you need.

### Model-invoked — you or the model can trigger these

The default: no `disable-model-invocation`. The description stays in context and the model reaches for the skill on its own when it applies; you can still type `/mattpocock-skills:<name>`.

**Engineering**:

- **[tdd](./plugin/skills/engineering/tdd/SKILL.md)**: test-driven development. The reference that makes the red-green-refactor loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop.
- **[code-review](./plugin/skills/engineering/code-review/SKILL.md)**: review the changes since a fixed point along two axes — Standards (does it follow this repo's documented coding standards?) and Spec (does it match what the originating issue asked for?) — in parallel sub-agents, reported side by side.
- **[diagnosing-bugs](./plugin/skills/engineering/diagnosing-bugs/SKILL.md)**: a diagnosis loop for hard bugs and performance regressions, gated phase by phase. Skip phases only when explicitly justified.
- **[codebase-design](./plugin/skills/engineering/codebase-design/SKILL.md)**: the shared vocabulary for designing deep modules — a lot of behaviour behind a small interface, at a clean seam, testable through that interface.
- **[research](./plugin/skills/engineering/research/SKILL.md)**: investigate a question against primary sources and capture the findings as a cited Markdown file in the repo, run as a background agent so you keep working.
- **[prototype](./plugin/skills/engineering/prototype/SKILL.md)**: build throwaway code that answers a design question — is this state model right, what should this UI look like.
- **[wizard](./plugin/skills/engineering/wizard/SKILL.md)**: generate an interactive bash wizard that walks a human through steps only they can perform: provisioning, credentials, CI secrets, an unfamiliar dashboard, a one-off migration.
- **[pr](./plugin/skills/engineering/pr/SKILL.md)**: the shape a pull request body takes — the smallest visual that makes the change clear, before/after evidence that it works, and a merge-danger call.

**Productivity**:

- **[writing-for-agents](./plugin/skills/productivity/writing-for-agents/SKILL.md)**: reference for writing any document an agent consumes — a skill, an `AGENTS.md` / `CLAUDE.md`, a doc reached by a pointer.

> **Harness note.** "Only you can trigger these" is Claude Code's semantics for `disable-model-invocation`, verified against Claude Code 2.1.261. Other harnesses that read the same `SKILL.md` files do not necessarily agree. In omp, for example, the same field only removes the skill from the rendered system-prompt listing; the model can still read it through `skill://<name>` and you can still reach it as `/skill:<name>`. Check your harness before relying on the split.

## Layout

```
.claude-plugin/marketplace.json  # makes this repo its own single-plugin marketplace; points at ./plugin
plugin/.claude-plugin/plugin.json # plugin manifest; the skills array whitelists the 25 enabled skills
plugin/skills/engineering/       # the 19 enabled engineering skills
plugin/skills/productivity/      # the 6 enabled productivity skills
dev/templates/skills/            # the 12 *.tmpl templates, mirroring the plugin tree
dev/source/                      # shared injection sources, pulled into templates by path; every
                                 # shared unit gets its own subdirectory, e.g. grilling/, domain-modeling/
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

Skill bodies are carried over from upstream, with four deliberate divergences: the domain-doc convention is renamed to `GLOSSARY.md` (upstream [PR #876](https://github.com/mattpocock/skills/pull/876)), the places where the text disagreed with itself — across two files or inside one — have been reconciled, two upstream skills are folded into their consumers rather than shipped as entries of their own (`grilling`, whose interview now lives inside `grill-me` and `grill-with-docs`, and `domain-modeling`, which `grill-with-docs` runs inline), and the setup skill is renamed to `mattpocock-skills-setup`. Everything else is upstream's. Re-syncing is a diff of `plugin/skills/` against the same paths upstream, porting across whatever changed. The manifests in `.claude-plugin/` and `plugin/.claude-plugin/` only need a version bump when upstream ships one.
