---
name: simplifier
description: Review research code and documentation for unnecessary complexity and propose focused simplifications. Use when asked to simplify, remove overengineering, or make a research pipeline easier to read and maintain.
---

# Simplifier

Review research code and documentation for complexity that makes a calculation harder to understand, run, or maintain. Prioritize a clear linear research workflow and preserve the statistical method and results.

## Review

1. Read the requested files and relevant project instructions. When available, consult the project's R Code Conventions.md and General Code Conventions.md.
2. Trace the calculation, its inputs and outputs, and how scripts are called before proposing changes.
3. Identify unnecessary layers, wrappers, duplicated calculations, unused code, excessive file splitting, and comments or documentation that obscure the work. Use plain language.
4. Assess checks, tests, error handling, provenance, and reproducibility in context. Recommend removal only when they are redundant or unnecessary for the task, and explain any consequences.
5. Report findings in the conversation with the file and location, why the complexity matters, and a specific simpler alternative. If nothing material needs simplification, say so.

## Applying changes

Review first. Edit only when the user requests changes. Preserve required checks, important data, history, and outputs. Verify callers and dependencies before removing or moving code or files. Avoid destructive cleanup without appropriate authorization. Use tests or comparisons appropriate to the change to establish that the analysis remains runnable and produces the intended results. Report changes and any remaining uncertainty.

Write comments and documentation for people, using short and direct language. Avoid unnecessary new abstractions, files, and dependencies.
