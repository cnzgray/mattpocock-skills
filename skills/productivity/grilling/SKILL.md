---
name: grilling
description: "A relentless interview to sharpen a plan, a design, or an idea, which decides as it goes whether the conversation has earned a paper trail."
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

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), spawn the `researcher` sub-agent (Agent tool, `subagent_type: mattpocock-skills:researcher`) to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

## Whether this earns a paper trail

The interview produces documents only when the conversation has actually settled something worth keeping. Deciding that is part of the interview, not a mode you pick up front.

Write a `GLOSSARY.md` entry the moment a term is resolved: challenge it against the existing language, sharpen it, then capture it right there rather than batching. Use [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md). `GLOSSARY.md` is a glossary and nothing else: it stays totally devoid of implementation details, and is never a spec, a scratch pad, or a home for implementation decisions. In a multi-context repo, `GLOSSARY-MAP.md` points at one `GLOSSARY.md` per context.

Offer an ADR only when all three hold: the decision is hard to reverse, a future reader will wonder why it was done this way, and it came out of a real trade-off. If any one is missing, skip it. Use [ADR-FORMAT.md](./ADR-FORMAT.md).

Create files lazily: only when there is something to write. A conversation that settles nothing new writes nothing.
