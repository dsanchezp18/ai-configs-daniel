# R Code Conventions

Canonical coding standard for active R code and R-focused AI work in this
repository. This file consolidates the previous coding preferences, R rules,
tidyverse guidance and research-workflow requirements.

Operational agent and skill files may add role-specific behavior, but they must
not contradict this file or copy its normative rules. When a rule conflicts
with an older reference, this file wins.

## 1. Working philosophy

Write code for the economist or researcher who must review it next year.

- Prefer expressive, readable, linear code over clever abstractions.
- Show the domain calculation directly in the script.
- Use names that expose the subject-matter meaning: `current_value`,
  `unit_price`, and `estimation_year` are better than `x`, `tmp`, or `df2`.
- Keep each transformation small enough to inspect and validate by itself.
- Match the surrounding structure when editing an existing script.
- Optimize only after measuring a real performance bottleneck.
- Comments explain why a rule exists; they do not restate obvious code.

The normal script reads from top to bottom:

1. setup;
2. read inputs;
3. check inputs;
4. transform data;
5. calculate estimates;
6. check results; and
7. write outputs.

## 2. Script structure

Every active standalone R script begins with this header:

```r
# ============================================================
# Descriptive title
# Author: Office of Statistics and Information
# Purpose: What this script does
# Inputs:  Files or objects read
# Outputs: Files or objects written
# ============================================================
```

The header is followed by numbered RStudio sections. Adapt the names to the
task, but never omit `# 0. Setup ----`.

```r
# 0. Setup ----
# 1. Read inputs ----
# 2. Check inputs ----
# 3. Prepare data ----
# 4. Calculate estimates ----
# 5. Check results ----
# 6. Write outputs ----
```

Additional structure rules:

- Use two spaces for indentation and keep lines under 80 characters when
  practical.
- Use `set.seed(42)` at the top when the script is stochastic.
- For deterministic scripts, include `# set.seed(42)` as the reproducibility
  marker.
- End standalone scripts with `sessionInfo()` as the final line.
- Keep setup, package loading, configuration, and constants at the top.

## 3. Packages

Load packages once at the top of the script with `library()`.

```r
library(dplyr)
library(purrr)
library(readr)
library(tidyr)
```

- Never use `require()`.
- Never install packages while a production script is running.
- Do not load packages midway through a script.
- After a package is loaded, use bare function names.
- Use `package::function()` only to resolve a real name conflict between
  loaded packages.
- Do not build package-checking wrappers around every script. A clear
  `library()` failure is enough.

## 4. Assignment, names, and paths

- Use `<-` for assignment; use `=` only for named function arguments.
- Use native pipe `|>`; never use `%>%`.
- Put one pipe operation on each line.
- Use `snake_case` for files, objects, columns, and functions.
- Use nouns for data objects and verbs for functions.
- Use descriptive domain names rather than generic temporary names.
- Build paths with `file.path()` from the repository or component root.
- Never use `setwd()`.
- Never hardcode a drive letter, username, M-drive path, or other machine path.
- Put years, expected counts, tolerances, and other tuning values in named
  configuration values.
- Create a destination with `dir.create(..., recursive = TRUE,
  showWarnings = FALSE)` before writing to a folder that may not exist.

## 5. Tidyverse data work

Use tidyverse verbs whose names match the operation:

- `filter()` for scope, geography, and period selection;
- `mutate()` for calculations and derived variables;
- `summarise()` for one row per group;
- `reframe()` when a group returns more than one row;
- `pivot_longer()` and `pivot_wider()` for reshaping;
- `complete()` for expected combinations; and
- `map()` or `walk()` for repeated file operations.

### Grouping and selection

- `.by` is preferred when it makes grouping local and clear.
- `group_by()` followed by `ungroup()` is also acceptable.
- Use `pick()` for column selection inside data-masking functions.
- Use `.data[[column_name]]` when a column is supplied as a character value.
- Select columns by name, never by position such as `df[, 3]`.

### Joins

Use modern join syntax and state expected match behavior:

```r
estimates <- values |>
  left_join(
    concordance,
    by = join_by(entity_id),
    multiple = "error",
    unmatched = "error"
  )
```

- Use `join_by()`, never character-vector `by = c(...)` syntax.
- Use `relationship` when declaring one-to-one or many-to-one cardinality.
- Use `multiple` and `unmatched` to catch unexpected matches.
- Use `na_matches = "never"` when missing keys must not match each other.
- Check keys before joining or aggregating.

### purrr and strings

- Use `map(x, f) |> list_rbind()` instead of `map_dfr()`.
- Use `map(x, f) |> list_cbind()` instead of `map_dfc()`.
- Use `walk()` and `walk2()` for side effects such as writing files or plots.
- Prefer type-stable `map_dbl()`, `map_chr()`, and `map_lgl()` where appropriate.
- Prefer `stringr` over base string functions:
  `str_detect()` over `grepl()`, `str_replace_all()` over `gsub()`,
  `str_sub()` over `substr()`, `str_length()` over `nchar()`, and
  `str_to_lower()` over `tolower()`.

## 6. Loops and conditions

Do not use `for`, `while`, `repeat`, or the `apply` family for data processing
in active production code. Use vectorized operations, `map()`, `walk()`, or a
grouped pipeline.

Do not use row-by-row `if` or `else` logic for data transformations. Prefer:

- `if_else()` for a two-way vector choice;
- `case_when()` for several conditions;
- `coalesce()` for fallback values; and
- joins or lookup tables for mappings.

Scalar `if` blocks are allowed for short, clear guards, such as checking a
required file or column, stopping after a failed validation, handling an
optional top-level section, or handling one unavoidable file-format branch.
Stop early rather than building deeply nested control flow.

## 7. Functions and abstraction

Linear code is the default. Do not create a helper merely to shorten a script.

A custom function is justified only when it:

- represents one named domain or file-reading operation;
- repeats a substantial operation at least three times;
- has clear inputs and one predictable return type; and
- makes the calculation easier to follow.

Inline one-use helpers, wrappers around one package function, generic
configuration frameworks, factories, builders, custom classes, and needless
abstraction layers. Keep side effects such as file writes at the top level or
use `walk()`.

## 8. Modelling and figures

- Use `feols()` from `fixest` for panel and fixed-effects regressions.
- Use `lm()` or `glm()` for cross-sectional work.
- `lm()` with `factor()` dummies is acceptable for panel models when downstream
  inference uses `fwildclusterboot`.
- Use `modelsummary()` for regression tables; use `output = "latex"` for
  LaTeX documents.
- Cluster standard errors at the unit of treatment assignment and document
  that choice directly above the model call.
- Use `ggplot2` for figures.
- Use a consistent non-default palette and a custom theme with
  `base_size >= 14`.
- Use sentence-case axis labels with units where applicable and put legends at
  the bottom.
- `ggsave()` must specify `width` and `height` explicitly.
- Deliverable figures should be saved as both `.png` and `.pdf` unless the
  task specifies another format. Use `bg = "transparent"` for Beamer figures.

## 9. Outputs and reproducibility

- Use `saveRDS()` for key models, summary tables, and processed data used by
  downstream scripts.
- Treat a missing `saveRDS()` for a downstream-referenced object as a critical
  reproducibility problem.
- Write important processed data and final results in documented formats.
- Keep a simple run record with selected source filenames, selected year,
  method, and output location.
- Do not add hashes, checksums, manual approval fields, or input locks unless a
  separate project requirement explicitly calls for them.
- A style-only rewrite must reproduce accepted numerical outputs.
- An estimation change is complete only after actual values reconcile with a
  known total, benchmark, or accepted comparison.

## 10. Missing values and numerical discipline

- State `na.rm` explicitly for every empirical `sum()`, `mean()`, `sd()`, and
  `var()` call.
- Never hide a new missing value with `na.rm = TRUE`; use it only when the
  documented method says missing observations are excluded.
- Check required period counts before annualizing monthly or quarterly data.
- Check that required numerical values are finite.
- Never compare floating-point values with `==`; use `all.equal()` or an
  explicit tolerance.
- Clamp probabilities passed to `qnorm()`, `pbinom()`, and similar functions:
  `eps <- 1e-12; pmin(1 - eps, pmax(eps, p))`.
- Check transformation links and domain constraints before extending a series.

## 11. Comments, errors, and console output

- Comments explain why a non-obvious rule exists.
- Do not keep commented-out dead code, except the deterministic
  `# set.seed(42)` marker.
- Use `message()` at most once per major stage when useful.
- Do not use `cat()`, `print()`, or `sprintf()` for status output.
- Do not print progress for every file, row, or iteration.
- Error messages should name the failing file, field, year, or series.

## 12. Reproducible research workflow

All analytical steps must be in code. Every reported number must be traceable
to a script.

Use this structure when setting up a research project:

```text
project-root/
├── README.md
├── MASTER.R
├── data/{raw,intermediate,final}/
├── code/{cleaning,analysis}/
├── outputs/graphs/
├── documentation/
└── .gitignore
```

- Raw data is never modified.
- Raw, intermediate, and final data remain separate.
- Code and data structures mirror each other where practical.
- Number scripts with `NN_verb_description.R` when execution order matters.
- Use README files to document folder purpose, contents, naming, and
  dependencies.
- The master script is the single reproducible entry point.
- Do not put a Git repository inside a shared Dropbox, OneDrive, or Google
  Drive folder.
- Do not commit raw or sensitive data, credentials, large generated outputs,
  or temporary files.

## 13. Review standard

Review active R code in this order:

1. correctness of transformations, joins, modelling, and outputs;
2. reproducibility and path discipline;
3. input and result validation;
4. downstream artifacts and saved objects;
5. code structure and tidyverse conventions; and
6. style and polish.

Formal findings include the file and line number, category, severity
(Critical, High, Medium, or Low), current code, proposed fix, and rationale.
Reviewers do not edit source files. Save formal reports to
`quality_reports/[script_name]_r_review.md`.

## 14. Known pitfalls

- Put robustness specifications in the same analysis script as the main model,
  with separate output names, rather than creating a script that only repeats
  the existing model.
- Validate joins, period coverage, and numerical finiteness before trusting a
  successful process exit status.

## 15. AI routing

This root file is the only normative coding standard. The other files have
specialized roles:

- `.claude/agents/` defines Claude role behavior.
- `.claude/skills/` provides specialized workflow and advanced R references.
- `.codex/skills/` defines Codex role behavior and UI metadata.
- `.github/` provides project context and Copilot routing.

Role selection:

- `r-coder`: implement or substantially revise one R script;
- `r-reviewer`: audit R scripts and produce a quality report;
- `r-build-and-review`: write, then review, an R script;
- `research-data-workflow`: set up or audit reproducible project structure;
- `modern-workflow-r`, `tidyverse-patterns`, and `r-style-guide`: consult for
  advanced implementation details after applying this master standard.

If instructions conflict, use this file first, then the role-specific file,
then general project context.
