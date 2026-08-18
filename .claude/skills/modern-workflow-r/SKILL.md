---
name: modern-workflow-r
description: Advanced R implementation guidance for tidy evaluation, modern tidyverse APIs, purrr, performance, and object systems. Apply the root coding standard first.
---

# Modern R workflow addendum

Read [`R Code Conventions.md`](../../../R%20Code%20Conventions.md) first. It
is the only normative coding standard. This skill is an advanced reference for
tasks involving:

- dplyr 1.1+ grouping, joins, `pick()`, `reframe()`, and match validation;
- rlang data masking, `{{ }}`, injection, `.data`, and `.env`;
- purrr 1.0+ list binding and side effects;
- profiling with `profvis` or `bench` before optimizing;
- choosing between dplyr, data.table, vctrs, S7, S3, and S4 when a real need
  exists; and
- migrating legacy tidyverse or base-R patterns.

Do not introduce abstraction, parallelism, or custom classes merely because
this reference describes them. The master standard's clarity and linearity
rules take precedence.
