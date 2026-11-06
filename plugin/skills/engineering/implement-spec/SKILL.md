---
name: implement-spec
description: "Implement the result of /to-spec and /to-tickets in code."
disable-model-invocation: true
---

You have been provided a spec. This spec should have tickets associated with it, describing how to implement the spec.

The issue tracker should have been provided to you. If not, tell the user to run `/mattpocock-skills-setup`.

The goal is the entire spec implemented on a single **integration branch**, with every ticket resolved the way the issue tracker closes work.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of tickets which are ready to be grabbed.

Start every subagent with a fresh context window.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

**Implementer subagents** should be run in the background where possible for maximum concurrency.

## Steps

1. Read the spec and tickets to understand the task graph.

2. (optional) Use an **exploration subagent** to conduct any exploration required by the tickets - relevant codebase files or external documentation. Ensure the exploration subagent can save files - it should save its markdown notes in a directory outside the repo, accessible by all future subagents. This lets **implementer subagents** focus on implementation rather than exploration.

3. Create or reuse the integration branch. If the current worktree is already on it, keep using it; do not create a separate integration worktree. If the issue tracker closes work through PRs, or the user asks for one, open a draft PR after the first merge in step 5 (a branch with no commits ahead of main can't open one), marked as closing the spec and tickets.

4. Use **implementer subagents** to implement each ticket. Reuse the current worktree when it is already a linked worktree for this spec (in a linked worktree, `git rev-parse --git-dir` and `git rev-parse --git-common-dir` differ; confirm its branch with `git worktree list --porcelain`), and do not create another one. Only when two or more tickets will run concurrently, create a separate worktree per additional ticket, and ask the user before creating them. Each implementer subagent:
   - confirms its worktree is based on the integration branch before starting; reset only a worktree you created, and ask before changing one the user created;
   - drives `/tdd` to build the ticket;
   - if it has its own worktree, merges the integration branch tip into its own branch before reporting done

5. Once an **implementer subagent** completes, merge its work to the integration branch with a **merger subagent**. If the implementer already worked in the integration worktree, skip the merge and have the merger subagent verify the branch instead.

6. If this changes the **frontier** of available tickets, kick off more **implementer subagents** to work on the new tickets. This allows for maximum concurrency.

7. Once all tickets are complete, run `/code-review` on the integration branch. Fix all issues raised by the code review in a single **implementer subagent** working in the same worktree.

8. If a draft PR exists, mark it ready for review. Otherwise, resolve each ticket the way the issue tracker closes work, and report the integration branch.

9. Clean up only the worktrees you created in step 4. Never remove the worktree you are working in or one the user created.
