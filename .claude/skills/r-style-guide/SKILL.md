---
name: r-style-guide
description: Advanced R naming, spacing, layout, function design, and error-message guidance. Apply the root coding standard first.
---

# R style addendum

Read [`R Code Conventions.md`](../../../R%20Code%20Conventions.md) first. It
is the only normative coding standard. Use this skill for additional guidance
on:

- two-space indentation, spacing, and practical line length;
- data-first function arguments and predictable return types;
- deciding whether a custom function is justified;
- single-responsibility design for approved functions; and
- clear user-facing validation errors; use `cli_abort()` after `library(cli)`
  when the project already uses `cli`, otherwise use a clear `stop()` guard.

The master standard's restrictions on helper functions, packages, paths, and
linear scripts always take precedence.
