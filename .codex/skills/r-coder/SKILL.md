---
name: r-coder
description: Write or substantially revise one R script in this research repo using the project's R conventions and workflow. Use when the task is to create a new R script or make a focused implementation change to an existing R script, especially when matching the local style matters.
---

# R Coder

Use this skill when writing or heavily revising one R script in this repository.

## Inputs

Have these before editing:

- A concrete task description
- The target file path

If the task is ambiguous about the target file, resolve that first.

## Required context

Before editing:

1. Read the R conventions from one of these locations, in order:
   - `./.claude/rules/r-code-conventions.md`
   - `~/.claude/rules/r-code-conventions.md`
2. Read the research workflow skill from one of these locations, in order:
   - `./.claude/skills/research-data-workflow/SKILL.md`
   - `~/.claude/skills/research-data-workflow/SKILL.md`
3. Scan nearby scripts in `scripts/` to match the existing tone and structure.

## Working style

- Prefer linear, readable scripts over abstraction-heavy code.
- Match surrounding structure when editing an existing script.
- Use helper functions only when they improve readability.
- Preserve the repo's current analysis workflow unless the task explicitly changes it.

## Coding rules

- Use `<-` for assignment.
- Use native pipes `|>`.
- Load packages at the top with `library()`.
- Keep a header block and clearly separated numbered sections when creating a new script.
- Use `snake_case` names.
- Build paths with `file.path()` and relative project paths.
- Call `dir.create(..., recursive = TRUE, showWarnings = FALSE)` before writing into new folders.
- Save important intermediate or downstream objects with `saveRDS()` when that fits the repo's workflow.
- Use `feols()` for panel or fixed-effects models and document clustering choices directly above the model call.
- Save figures with explicit dimensions, and when the figure is a deliverable save both `.png` and `.pdf` unless the user asks otherwise.
- End standalone scripts with `sessionInfo()`.

## Output

- Implement the requested script change directly in the target file.
- Do not produce a review report as the primary output of this skill.
- If the task also requires review, hand off to the `r-reviewer` skill after the code change is complete.
