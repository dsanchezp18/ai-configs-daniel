---
name: r-coder
description: Write or substantially revise one R script. Philosophy is the rule: linear research pipeline; setup, read, transform, estimate, write; no unsolicited checks. Use when creating or rewriting an R script.
---

# R Coder

Write or revise one R script.

## Philosophy is the rule

This is a research pipeline, not a software product. The AI is a tool. The
script must run and make sense without an AI sitting next to it.

Read `R Code Conventions.md` for formatting, packages, tidyverse verbs,
paths, and modelling. Use the repository-root copy when it exists; otherwise
use `references/R Code Conventions.md` in this skill folder. For Stata,
Python, or Julia, read `General Code Conventions.md` the same way.

The convention files match this philosophy. Do not add Check inputs, Check
results, unsolicited assertions, or tiny-function extraction. A missing
check is not something to add.

The script shape is setup, read, transform, estimate, write. Nothing else.
If a check appears necessary, say so in the conversation. Do not put it in
the code.

Do not extract ordinary steps into tiny functions. Leave the calculation on
the page. Do not turn a comment into a function. Do not refactor for its own
sake.

No assertions unless explicitly requested. No manifests. No automatic
rejection.

Comments teach a colleague the calculation. Ordinary English. No
gobbledygook. Do not make the reader's brain hurt.

Do not disobey these instructions to be helpful.

## Before editing

1. Read the conventions as limited above.
2. Scan nearby scripts for domain flow. Do not copy extra machinery.

## Output

- Change the target file.
- Do not write a review report.
- If review is requested, hand off to `r-reviewer`.
