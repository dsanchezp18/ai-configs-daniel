---
name: r-reviewer
description: Review one or more R scripts in this research repo for correctness, reproducibility, and adherence to the project's R conventions. Use when the user wants an R-focused audit after edits or before trusting a script.
---

# R Reviewer

Use this skill for code review of R scripts in this repository.

## Required context

Before reviewing:

1. Read the target script or scripts end to end.
2. Read `.claude/rules/r-code-conventions.md` and use it as the review standard.

## Review priorities

Prioritize:

- Correctness of transformations, joins, modelling choices, and outputs
- Reproducibility and path discipline
- Consistency with project conventions
- Risks to downstream scripts and artifacts

Treat style-only issues as secondary.

## Review checklist

Check these systematically:

- Header and section structure
- Assignment and pipe style
- Package loading discipline
- Relative paths and directory creation
- Tidyverse and naming consistency
- Modelling choices and clustering comments
- Figure-saving patterns and output completeness
- RDS usage for downstream objects
- Console output hygiene
- Numerical robustness and NA handling

## Report format

Write the report to:

- `quality_reports/[script_name]_r_review.md`

Use this structure:

- Summary counts by severity
- Ordered findings with file path and line number
- Proposed fix for each issue
- Checklist summary by category

## Constraints

- Do not edit source files while acting as reviewer.
- Be specific and actionable.
- Prioritize bugs and reproducibility failures over style concerns.
