---
name: r-reviewer
description: Review one or more R scripts in this research repo for correctness, reproducibility, and adherence to the project's R conventions. Use when the user wants an R-focused audit after edits or before trusting a script.
---

# R Reviewer

Use this skill for code review of R scripts in this repository.

## Required context

Before reviewing:

1. Read the target script or scripts end to end.
2. Read `R Code Conventions.md` from the repository root and use it as the
   review standard.
3. Trace the complete pipeline represented by the target: identify its inputs,
   upstream preparation or acquisition steps, transformations, estimates,
   checks, saved outputs, and downstream consumers. Read the master script,
   README, or referenced scripts when they define those boundaries. Do not
   judge an isolated script as complete when its pipeline context is available.

## Review priorities

Prioritize:

- End-to-end pipeline correctness: the read, check, transform, estimate,
  validate, and write stages agree with one another and with the documented
  method.
- Readability, expressiveness, and elegance: a researcher should be able to
  follow the script from top to bottom without reconstructing hidden state,
  deciphering generic names, or reverse-engineering clever abstractions.
- Reproducibility and path discipline, including input provenance, output
  completeness, and downstream compatibility.
- Risks to downstream scripts, saved artifacts, and numerical results.
- Consistency with the canonical R conventions.

Treat readability as part of code quality, not as a cosmetic afterthought.
Report subjective preferences only when they materially affect comprehension,
maintenance, reproducibility, or the ability to audit the analysis.

## Review checklist

Check these systematically:

- Header and section structure
- Assignment and pipe style
- Package loading discipline
- Relative paths and directory creation
- Tidyverse and naming consistency
- Top-to-bottom flow: inputs are declared, transformations are visible, and
  each output is produced by an inspectable stage
- Expressive names, direct domain calculations, small transformations, and
  proportionate abstractions
- No row-level `if`/`else`, `for`, `while`, `repeat`, or `apply` data logic;
  scalar `if`/`else` exceptions are short, top-level, and explicitly justified
- Modelling choices and clustering comments
- Figure-saving patterns and output completeness
- RDS usage for downstream objects
- Console output hygiene
- Numerical robustness and NA handling
- End-to-end reconciliation of declared inputs, checks, estimates, outputs,
  and downstream references

## Report format

Write the report to:

- `quality_reports/[script_name]_r_review.md`

Use this structure:

- Summary counts by severity
- Ordered findings with file path and line number
- Proposed fix for each issue
- Checklist summary by category
- A separate readability and pipeline-integrity assessment, stating whether
  the code is clear and complete from input acquisition through final output

## Constraints

- Do not edit source files while acting as reviewer.
- Be specific and actionable.
- Prioritize correctness and pipeline-breaking issues, then readability,
  expressiveness, and maintainability. Do not dismiss a material readability
  problem as "style only."
