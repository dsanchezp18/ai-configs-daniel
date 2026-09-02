# Daniel's AI configurations

Repository-level instructions, coding standards, and role-specific workflows
for Daniel's AI-assisted programming work.

This repository contains reusable guidance. It is intentionally general and
should not contain assumptions from a single analysis project.

## Start here

- [`AGENTS.md`](AGENTS.md) is the repository instruction entry point.
- [`R Code Conventions.md`](R%20Code%20Conventions.md) is the canonical
  standard for R code.
- [`General Code Conventions.md`](General%20Code%20Conventions.md) covers
  Stata, Python, and Julia. Its R section routes back to the R standard.
- [`GIT_WORKFLOW.md`](GIT_WORKFLOW.md) documents the safe Git workflow for
  pulling, reviewing, committing, and publishing changes.

## Tool-specific guidance

- `.agents/skills/` contains Codex skills and their optional UI metadata.
- `.claude/agents/` and `.claude/skills/` contain Claude-specific agents and
  skills.
- `.github/` contains Copilot routing and cross-tool synchronization guidance.
- `.codex/instructions.md` is retained as a compatibility copy; new Codex
  repository instructions belong in `AGENTS.md`.

The R roles are:

- `r-coder` for writing or substantially revising one R script;
- `r-reviewer` for auditing R scripts and producing a quality report; and
- `r-build-and-review` for write-then-review orchestration.

## Working conventions

Before changing code, read the applicable canonical standard and the relevant
role-specific workflow. Keep project-specific assumptions in the project
repository, not here. When changing a role that exists in both Claude and
Codex formats, make the matching substantive change in both locations.

For R work, the repository includes configuration for `lintr` and `styler`.
Use the review checklist in the R standard and run `git diff --check` before
publishing.

## Contributing

Keep guidance concise, executable, and evidence-based. Prefer one canonical
rule over duplicated conflicting rules. Update references when sections or
paths move, and verify that examples follow the rules they describe.
