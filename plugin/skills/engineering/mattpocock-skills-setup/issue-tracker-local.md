# Issue tracker: Local Markdown

Issues and specs for this repo live as markdown files in `.scratch/`.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The spec is `.scratch/<feature-slug>/spec.md`
- Implementation issues are one file per ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`, never a single combined tickets file
- Triage state is recorded as a `Status:` line near the top of each issue file (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

## Publishing to the issue tracker

When publishing a spec, resolve the target file first: if the user passed a path, or the conversation already identifies one, rewrite that file in place instead of creating another. When publishing tickets, each ticket gets its own file unless it already exists.

If no target is identified, list the feature directory for a matching file and ask the user before creating one. Never create a second file for the same spec.

## Fetching the relevant ticket

Read the file at the referenced path. The user will normally pass the path or the issue number directly.

