---
name: research-code-review
description: Conduct a detailed review of research code or a research pipeline for substantive errors, agreement with the stated method, readability, and reproducibility. Use when a user requests a thorough review across scripts or stages; use language-specific reviewers for ordinary single-script reviews.
---

# Detailed research code review

Review the requested research code and report findings. Follow the project's
instructions and the user's scope. Read `R Code Conventions.md` for R and
`General Code Conventions.md` for Stata, Python, or Julia. Use the project
copy when available; otherwise use the copies in
`C:/Users/Daniel/Documents/GitHub/ai-configs-daniel/`.

This is a research pipeline. A reader must be able to follow the calculations
without an AI. Prefer clear, linear code: setup, read, transform, estimate,
write. Do not treat missing input checks, result checks, assertions, helper
functions, manifests, or validation scripts as defects. Do not recommend
extra layers or split a clear script merely to fit a prescribed structure.

## Review

Read the relevant code, method, and documentation. For a pipeline, trace each
important input through cleaning, construction, estimation, and the final
outputs. Inspect data or run code when appropriate and authorized by the task
and environment. State what was inspected or run; reading code alone cannot
establish that results reproduce or that the data meet an assumption.

Examine the following when they apply:

- **Data and joins:** unit of observation, identifier definitions, merge
  keys, join behavior, unmatched observations, appends, type conversions,
  and the rule used to select among duplicates. Look for operations that can
  silently add, remove, or change observations.
- **Cleaning and construction:** missing and special-value codes, changes to
  values, sample exclusions, units, denominators, grouping variables,
  aggregation, and whether constructed variables match their definitions.
- **Research design and estimation:** eligibility, sampling, weights,
  treatment assignment, random draws, model specification, standard errors,
  and whether the implemented method matches the stated design. Distinguish
  an observed mismatch from a question about an undocumented choice.
- **Outputs and reproducibility:** whether tables, figures, and saved data
  reflect the calculations; paths and dependencies; random seeds and ordering
  where results depend on them; overwritten inputs; and dependence on
  objects left in memory by another script.
- **Readability:** whether a researcher can follow the calculation and the
  sequence from input to output, and whether unnecessary functions, layers,
  or comments obscure it.

Interpret code in context. For example, inspect Stata `merge m:m` and
`duplicates drop, force` for unintended matches or record selection, and R
`data.table` changes by reference for effects on objects used later. Do not
report a pattern merely because it appears. Treat questions about a method as
questions unless the evidence establishes a mismatch.

## Report

Report the most consequential findings first. Give the file and line, the
evidence, the likely effect on results or interpretation, and a concrete
recommendation. Assign severity according to the likely consequence and
strength of evidence. A readability problem that hides a calculation can be
substantive. Combine findings that have the same cause.

State material uncertainties and limits of the review. Do not claim that code
is correct or reproducible solely because it runs, or that a defect exists
solely because a check is absent. Keep research choices with the researcher
when the intended choice cannot be established from the available evidence.
Give the report in chat unless the user asks for a file.

This review draws on the World Bank's research code-review skill and DIME
peer-review guidance, adapted to this project's research-code philosophy.
