---
name: r-coder
description: Write or substantially revise one R script in this repository using the root master coding standard and research workflow.
---

# R Coder

Use this skill when creating a new R script or making a focused implementation
change to an existing R script. Write one complete script from a concrete
description and target path.

## Required context

Before editing:

1. Read `R Code Conventions.md` in the repository root.
2. Scan nearby scripts to match the existing tone and structure.

## Working style

- Prefer linear, readable scripts over abstraction-heavy code.
- Keep the script researcher-friendly and easy to follow from top to bottom.
- Match surrounding structure when editing an existing script.
- Preserve the current analysis workflow unless the task explicitly changes it.
- Use the root master for all coding, validation, modelling, output, and path
  decisions.
- Apply the master standard to functions, packages, paths, validation, outputs,
  and numerical discipline.

## Output

- Implement the requested script change directly in the target file.
- Do not produce a review report as the primary output.
- If review is requested, hand off to `r-reviewer` after the code change.
