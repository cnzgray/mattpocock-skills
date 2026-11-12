---
name: grill-me
description: "A relentless interview to sharpen a plan, a design, or an idea. Writes nothing."
disable-model-invocation: true
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

**How to ask.** Use the host's **structured question tool** — the one that shows a question with its candidate answers and takes the user's picks. Claude Code's `AskUserQuestion` is one; other hosts have their own name for it. It puts the frontier in front of the user as a form to fill rather than a wall of prose to answer, and a user who agrees with you can agree with a single pick.

Compute the frontier once, then ask it one tool call at a time — a call carries only as many questions as the tool allows, and each returns the user's picks before the next goes out. Every call belongs to the same round: the round ends when the last one comes back answered, and only then is the frontier recomputed.

Carry each question like this:

- **Stem**: the decision in one line, numbered so the numbering runs unbroken across the session.
- **Options**: the candidate answers, each with a note on what it commits you to. **Your recommended answer goes first**, marked as the recommendation — a user who agrees with you picks the first option and moves on. A question with no clean set of candidates still goes through the tool: offer the answers you can think of and let the user type their own.
- **Reasoning**: the background, the alternatives weighed, the trade-off behind the recommendation — in prose, before the call, as much context as each question needs and no more. A stem squeezed onto one line is where the argument dies.

**Without such a tool**, ask the frontier in prose instead:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Word each question so "yes" accepts your recommended answer.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent with a fresh context window to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

## This interview writes nothing

This one is stateless: it writes no files at all. Not a `GLOSSARY.md` entry, not an ADR, not a scratch note. It is for sharpening a plan, a design, a piece of writing, a decision, anything with no repo under it.

If you are working in a repo and the interview settles language or a decision worth keeping, say so in the conversation and point the user at `grill-with-docs`, which runs the same interview and leaves the paper trail.
