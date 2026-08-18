---
name: tidyverse-patterns
description: Advanced tidyverse patterns for joins, grouping, NA-safe transformations, purrr, stringr, and modern data reshaping. Apply the root coding standard first.
---

# Tidyverse patterns addendum

Read [`R Code Conventions.md`](../../../R%20Code%20Conventions.md) first. It
contains the required tidyverse conventions. Use this skill for deeper
implementation detail when needed, including:

- join cardinality, `relationship`, `multiple`, `unmatched`, and
  `na_matches`;
- `.by`, `pick()`, `reframe()`, and tidy-selection behavior;
- NA-safe filtering and conditional updates;
- `map() |> list_rbind()`, `walk()`, and type-stable mapping;
- `stringr` transformations and modern `tidyr` reshaping; and
- migrating superseded `%>%`, `map_dfr()`, `gather()`, and `spread()` code.

Do not use an advanced pattern when a simpler linear pipeline is clearer.
