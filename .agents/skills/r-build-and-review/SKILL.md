---
name: r-build-and-review
description: Write an R script with r-coder, then audit it with r-reviewer. Philosophy is the rule for both steps. Use when the user wants a script written and reviewed.
---

# R Build And Review

Orchestrate write-then-review for one R script.

## Philosophy is the rule

Both steps follow the same rule. This is a research pipeline, not a software
product. Script shape is setup, read, transform, estimate, write. No
unsolicited checks. Leave the calculation on the page.

Tell `r-coder` and `r-reviewer` to follow the philosophy. Do not add
unsolicited checks.

Do not treat missing checks as a reason to mark the script not ready.

## Required inputs

- What the script should do
- The target file path

If the path is missing, get it first.

## Workflow

1. Use `r-coder` to write or revise the target script.
2. After that finishes, use `r-reviewer` on the same file.
3. Return the script path, the review report path, and a short severity
   summary.

Do not run the reviewer in parallel with an unfinished edit of the same file.

## Review output

`quality_reports/[script_name]_r_review.md`

## Final response

- Script written: `[target path]`
- Review report: `quality_reports/[script_name]_r_review.md`
- Issue counts by severity
- Status: `Ready for use` or `Needs revision before use`

Missing unsolicited checks do not make a script need revision.
