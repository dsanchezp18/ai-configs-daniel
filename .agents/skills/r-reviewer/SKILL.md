---
name: r-reviewer
description: Review R scripts for calculation correctness, readability, and reproducibility. Philosophy is the rule: missing unsolicited checks are not defects. Use after edits or before trusting a script.
---

# R Reviewer

Review R scripts. Do not edit source files while reviewing.

## Philosophy is the rule

This is a research pipeline, not a software product. A human must be able to
follow the calculation without an AI.

Read `R Code Conventions.md` for formatting, packages, tidyverse verbs,
paths, and modelling. Use the repository-root copy when it exists; otherwise
use `references/R Code Conventions.md` in this skill folder.

The convention files match this philosophy. Do not treat missing checks as
defects. Do not require tiny helpers. Do not score input and result
validation as a review category.

The expected script shape is setup, read, transform, estimate, write.

## Not a defect

Do not report these as violations unless the author asked for them:

- missing Check inputs / Check results sections
- missing assertions, guardrails, manifests, or validation scripts
- missing helper functions or `code/functions/` files

## Is a defect

- wrong calculation, join, model, or output
- unsolicited checks, assertions, or rejection machinery
- tiny functions that hide a simple calculation
- extra folders, wrappers, or orchestrators
- comments or documentation written for an AI
- code a human cannot follow without help

## Priorities

1. Correctness of transformations, joins, modelling, and outputs.
2. Whether a researcher can follow setup, read, transform, estimate, write.
3. Reproducibility and path discipline.
4. Risk to downstream scripts and artifacts.

Style-only issues are secondary. A readability problem that hides the
calculation is not style-only.

## Report

Write the report to `quality_reports/[script_name]_r_review.md`.

Include severity counts, findings with file and line, a proposed fix, and
whether a human can follow the script from read through write.

Be specific. Do not invent work.
