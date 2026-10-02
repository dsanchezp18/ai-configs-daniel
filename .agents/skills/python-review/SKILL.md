---
name: python-review
description: Review a Python script against General Code Conventions.md and report findings in the chat. Read-only. Use when the user says "review this Python script", "check my Python code", or asks for a Python code audit.
---

# Python script review

Read `General Code Conventions.md` (Python section) first. Then read the script. Do not edit it. Do not write a report file. Give the findings in the chat.

## What to check, in order

1. **Correctness:** transformations, joins and models match the stated method. Survey data uses weights and keeps standard errors.
2. **Paths and reproducibility:** `pathlib`, no `os.chdir()`, no hardcoded machine paths, every object a later script reads is saved (parquet, not pickle).
3. **Missing values:** `null` and `NaN` are handled on purpose in `polars`. No `==` on floats. Missing-value behaviour of `.mean()` and `.sum()` is clear.
4. **Idioms:** `polars` for the data work, one `.to_pandas()` conversion at most, `validate=` on joins, no row loops for column logic, functions only after six repeats.
5. **Style:** run `ruff format --check .` and `ruff check .` when `ruff` is installed, and report what they flag. Run `mypy` the same way. Add type hints on function signatures.
6. **Header and comments:** header block, numbered cell sections, one comment per 5 to 10 lines, no commented-out code, `logging` instead of `print`.

## Do not flag

- A missing input check, result check or assertion. The repository rule is that a missing check is not a defect.
- A missing helper function or tiny-function extraction.

## Output

Start with a one-line verdict. Then list findings, most serious first. For each: `file:line`, severity (Critical, High, Medium, Low), the current code, the proposed fix, and one sentence of reason. Cite the convention section when one applies. Offer to apply the fixes, and apply them only if the user says yes.
