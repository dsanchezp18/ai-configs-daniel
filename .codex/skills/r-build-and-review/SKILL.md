---
name: r-build-and-review
description: Orchestrate a two-step R workflow in this repo: write a script with r-coder, then audit it with r-reviewer. Use when the user wants a new R script created and reviewed, especially when subagents are available.
---

# R Build And Review

Use this skill as an orchestrator for new R-script work in this repository.

## When to use

Use this when the user wants:

- A new R script written from a plain-language description
- A substantial R script rewrite plus a formal review
- A delegated workflow that splits implementation and review into separate specialist passes

## Required inputs

Before starting, have:

- The script description
- The target file path

If the target file path is missing, get it first.

## Workflow

1. Use `r-coder` to write or revise the target script.
2. After the code change is complete, use `r-reviewer` on the written file.
3. Return:
   - the script path
   - the review report path
   - a short severity summary

## Subagent guidance

If subagents are allowed for the task:

- Spawn one worker for the coding step with clear file ownership.
- After the coding step finishes, run a separate review pass.
- Do not run the reviewer in parallel with an unfinished code edit on the same file.

If subagents are not allowed, execute the same sequence locally.

## Review output

The review report should be saved to:

- `quality_reports/[script_name]_r_review.md`

## Final response

Summarize:

- Script written: `[target path]`
- Review report: `quality_reports/[script_name]_r_review.md`
- Issue counts by severity
- Status: `Ready for use` or `Needs revision before use`
