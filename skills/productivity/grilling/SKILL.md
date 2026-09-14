---
name: grilling
description: "A relentless interview to sharpen a plan, a design, or an idea. Writes nothing by default; pass docs to let it keep a GLOSSARY.md entry or an ADR."
argument-hint: "[docs]"
arguments: [docs]
disable-model-invocation: true
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

## Whether this writes anything

By default this interview writes nothing. Talk, decide, and leave the repo alone. Only when the call passed `docs` does the flag below turn on, and only then may files be written.

**With `$docs` given:** keep a `GLOSSARY.md` entry for a term the interview resolves, but only when it is language the project will actually keep, the kind that ends up in code, in interfaces, in issue titles, in test names. A term coined to get through this one conversation stays in the conversation. Use [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md). `GLOSSARY.md` is a glossary and nothing else: it stays devoid of implementation details, and is never a spec, a scratch pad, or a home for implementation decisions. In a multi-context repo, `GLOSSARY-MAP.md` points at one `GLOSSARY.md` per context.

Offer an ADR only when all three hold: the decision is hard to reverse, a future reader will wonder why it was done this way, and it came out of a real trade-off. If any one is missing, skip it. Use [ADR-FORMAT.md](./ADR-FORMAT.md).

Create files lazily: a term that never came up writes nothing, and a decision that cleared only two of the three ADR conditions writes nothing. Writing a document is never the price of finishing the interview.

**Without `$docs`:** write no files at all, not a glossary entry, not an ADR, not a scratch note. If the interview did settle language or a decision worth keeping, say so in the conversation and name what a `/mattpocock-skills:grilling docs` rerun would capture; do not write it now.
