---
name: r-build-and-review
description: "Orchestrate a two-step R workflow in this repo: write a script with r-coder, then audit it with r-reviewer. Use when the user wants a new R script created and reviewed, especially when subagents are available."
---

# R Build And Review

Use this skill as an orchestrator for new R-script work in this repository. Coordinate two specialist passes to produce a clean, reviewed R script.

## When to use

Use this when the user wants:

- A new R script written from a plain-language description
- A substantial R script rewrite plus a formal review
- A delegated workflow that splits implementation and review into separate specialist passes

## Required inputs

Before starting, have exactly two inputs:

- The script description
- The target file path

If the target file path is missing, get it before starting the workflow.

## Workflow

1. Use `r-coder` to write or revise the target script. Pass the full description, exact target path, and relevant context such as available data sources, expected outputs, and nearby scripts to match.
2. Wait for the code change to finish.
3. Use `r-reviewer` on the written file. Pass the target path and let the reviewer trace its pipeline context.
4. Wait for the review to finish.
5. Return:
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

If Critical or High issues were found, list their titles so the user knows what to address next. Do not fix review findings as part of this orchestration step; leave that decision to the user.

