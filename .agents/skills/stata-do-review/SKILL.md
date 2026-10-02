---
name: stata-do-review
description: Review a Stata do-file against General Code Conventions.md and report findings in the chat. Read-only. Use when the user says "review this do-file", "check my Stata code", or asks for a Stata code audit.
argument-hint: "[do-file path]"
allowed-tools: ["Read", "Grep", "Glob"]
---

# Stata do-file review

Read `General Code Conventions.md` (Stata section) first. Then read the do-file. Do not edit it. Do not write a report file. Give the findings in the chat.

## What to check, in order

1. **Correctness:** transformations, merges and estimates match the stated method. Survey data has a `svyset`, and estimates use `svy:` and keep standard errors.
2. **Paths and reproducibility:** no `cd`, no hardcoded machine paths, `save ..., replace` for every dataset that a later do-file reads.
3. **Missing values:** `.` sorts above every number, so comparisons need `!missing()`. No `==` on floats.
4. **Merges:** the match type is stated (`1:1`, `m:1`), and `_merge` or `assert()` is handled.
5. **Structure and idioms:** no `foreach` over observations for row logic, `program define` only after six repeats, 4-space indents, lines under 100 characters.
6. **Header and comments:** header block, numbered sections, one comment per 5 to 10 lines, no commented-out code.

Stata has no linter. Check indentation and line length by reading.

## Do not flag

- A missing input check, result check or assertion. The repository rule is that a missing check is not a defect.
- A missing helper program or tiny-function extraction.

## Output

Start with a one-line verdict. Then list findings, most serious first. For each: `file:line`, severity (Critical, High, Medium, Low), the current code, the proposed fix, and one sentence of reason. Cite the convention section when one applies. Offer to apply the fixes, and apply them only if the user says yes.
