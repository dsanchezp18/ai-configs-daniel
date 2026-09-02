# R Code Conventions

Canonical coding standard for active R code and R-focused AI work in this
repository. This file consolidates the previous coding preferences, R rules,
tidyverse guidance and research-workflow requirements.

Operational agent and skill files may add role-specific behavior, but they must
not contradict this file or copy its normative rules. When a rule conflicts
with an older reference, this file wins.

## 1. Working philosophy

Write code for the economist or researcher who must review it next year. The
code must be readable, simple to understand, and commented at a fixed,
measurable density — never more.

- Prefer expressive, readable, linear code over clever abstractions.
  - Do not rely on software-engineering concepts. The code is a
    research/statistical pipeline, not a software product.
- Show the domain calculation directly in the script.
- Use names that expose subject-matter meaning: `current_value`,
  `unit_price`, `estimation_year` are better than `x`, `tmp`, `df2`.
  - Object and column names: 1-4 words, snake_case. A name needing a 5th
    word is a sign the object is doing two things — split it instead of
    lengthening the name.
- Keep each transformation small enough to inspect and validate by itself.
- Optimize only after measuring a real performance bottleneck.
- Comments explain why a rule exists; they do not restate obvious code.
  - Target one comment per 5-10 lines of code. Never one comment per line. A
    block under 5 lines needs at most one comment, only if a non-obvious
    reason exists.

**Existing vs. new code.** This file's conventions govern all new scripts
without exception. When editing an existing script that predates these
conventions (older pipe style, undated section names, different comment
density), convert the *entire file* to the current convention in the same
edit — do not leave a file half-migrated, and do not preserve the old style
"to match surrounding code." Matching surrounding structure (see below)
applies to domain logic and script flow, not to formatting rules this file
already specifies. If only a small, targeted fix is being made to a large
legacy script and a full-file conversion is out of scope for that change, say
so explicitly rather than silently mixing styles.

- Match the surrounding *domain logic and script flow* when editing an
  existing script (e.g. don't reorder the read-transform-write sequence
  without reason). This does not extend to formatting choices this file
  governs (pipe operator, indentation, section naming, comment density) —
  those always follow this file, per the rule above.

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
# Author: Daniel Sanchez
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

- Use `set.seed(42)` at the top when the script is stochastic; do not use it
  if everything is deterministic.
- Keep setup, package loading, configuration, and constants at the top.
- Use commentary to express to a human reader what is happening.
- See section 1 for comment density; do not exceed it in section headers
  either.

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

## 4. Assignment, names, paths, and formatting

- Use `<-` for assignment; use `=` only for named function arguments.
- Use native pipe `|>`; never use `%>%`.
- Put one pipe operation on each line.
- Use `snake_case` for files, objects, columns, and functions.
- Use nouns for data objects.
- Use descriptive domain names rather than generic temporary names (see
  section 1 for the 1-4 word limit).

**Indentation and formatting — enforced by `styler` and `lintr`.** Run
`Rscript scripts/style_project.R` (or `source("scripts/style_project.R")`) on
the whole project before a script is considered complete. This applies the
project's pinned `styler` configuration (`tidyverse_style`, `indent_by = 2`,
`scope = "tokens"` so intentional line breaks and comments are left alone),
respecting `.stylerignore`. Concretely, this will:

- indent multi-line function calls with each named argument on its own line,
  2 spaces from the call's opening `(`;
- indent piped chains 2 spaces per `|>` step;
- indent function bodies 2 spaces from `function`, with the closing `}`
  aligned to the start of the assignment line.

Line length (80 characters) is enforced separately by `lintr`'s
`line_length_linter`, not by `styler`. Run `lintr::lint(file)` against the
repo's `.lintr` config afterward and resolve every flagged issue before
treating the script as done. Do not hand-format around what these tools
produce — their output wins over manual preference.

- Prefer a plain string for fixed project-relative paths, e.g.
  `"data/raw/input.csv"`; do not wrap a fixed path in `file.path()` just to
  construct it.
- Use `file.path()` only when a path genuinely needs to be built dynamically
  from variable components.
- Never use `setwd()`.
- Never hardcode a drive letter, username, M-drive path, or other machine
  path. Use paths relative to the R project or terminal root.
- Put years, expected counts, tolerances, and other tuning values in named
  configuration values.
- Create a destination with `dir.create(..., recursive = TRUE,
  showWarnings = FALSE)` before writing to a folder that may not exist. Skip
  this if the folder is known to exist.

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
- Prefer type-stable `map_dbl()`, `map_chr()`, and `map_lgl()` where
  appropriate.
- Prefer `stringr` over base string functions: `str_detect()` over `grepl()`,
  `str_replace_all()` over `gsub()`, `str_sub()` over `substr()`,
  `str_length()` over `nchar()`, and `str_to_lower()` over `tolower()`.

## 6. Survey data management

Default to `srvyr` for any survey-weighted analysis: it wraps the base
`survey` package in tidyverse-style, pipeable verbs (`as_survey_design()`,
`survey_mean()`, `group_by()` on a survey object) so survey code reads like
any other pipeline under section 5. Drop to base `survey` functions
(`svyglm()`, `svrepdesign()`, and similar) only when `srvyr` has no wrapper
for what the analysis needs, and say so in a comment above the call.

- Declare the survey design once, immediately after reading the cleaned
  data, with `as_survey_design()` (or `as_survey_rep()` for replicate
  weights). State `weights`, `strata`, and `ids` (cluster/PSU) explicitly —
  never build a design object on defaults that silently drop stratification
  or clustering.
- Never compute an unweighted `mean()`, `sum()`, `sd()`, or proportion on
  survey microdata as if it were population-representative. If an
  unweighted figure is genuinely needed (raw sample size, a QA check), name
  it as unweighted in the object and any output label
  (`n_respondents_unweighted`), never with a name that reads as a population
  estimate.
- Use `survey_mean()`, `survey_total()`, `survey_ratio()`, and
  `survey_quantile()`; each returns the estimate and its standard error
  together — keep both in the output, do not discard the SE column.
- Use `group_by()` (or `.by`, per section 5) on the `tbl_svy` object for
  subgroup estimates. Do not filter to a subgroup first and rebuild the
  design from scratch unless that subgroup genuinely needs a different
  design specification.
- Document the sampling design (strata/cluster/weight variable names and
  their source) in the script header's Purpose field or in a codebook under
  `documentation/codebooks/`, not only inline in code.
- Keep direct identifiers (names, addresses, contact info, exact geocodes)
  out of `data/intermediate/` and `data/final/`. Strip or hash them in the
  raw-to-intermediate cleaning step and document the transformation.
- Treat don't-know, refused, and skip/not-applicable codes as distinct
  categorical values during cleaning, not as ordinary `NA`. Recode them to
  explicit labelled `NA` levels (or a `haven::labelled` factor) only at the
  point analysis requires it, and document the recode.
- Check unweighted and weighted respondent counts against the expected
  sample size from the codebook as part of the script's input-checking
  section (section 1's step 3). A missing wave or an unexpected count is a
  validation failure, not a silent proceed.

### Labels

Survey data read with `haven` (`read_dta()`, `read_sav()`, `read_sas()`)
carries variable and value labels as attributes, not as ordinary factor
levels. Handle them explicitly rather than letting `mutate()` calls treat a
labelled numeric column as if it were plain numeric.

- **Inspect** labels before transforming a labelled column, so a recode is
  based on what the codes actually mean, not a guess:

```r
df$region_code |> haven::print_labels()
```

- **Convert to factor** with `haven::as_factor()` — always namespaced with
  `haven::`, even when `haven` is loaded, because `forcats` also exports an
  `as_factor()` with different behavior and the two are easy to shadow by
  accident:

```r
df <- df |>
  mutate(region_code = haven::as_factor(region_code))
```

  Confirm this is the intended outcome before using it broadly — it turns
  the column into a plain R factor, which drops the original numeric codes
  and any labels not attached to a used level.

- **Strip labels** with `haven::zap_labels()` when a column needs to go
  back to plain numeric (e.g. before a calculation that a labelled class
  would interfere with):

```r
df <- df |>
  mutate(income_reported = haven::zap_labels(income_reported))
```

- Both conversions belong in a `mutate()` call, consistent with section 5 —
  do not reach for `$<-` assignment or a base-R loop over columns to apply
  them.
- Plain **inspection** (`print_labels()`) is not a transformation and does
  not belong in a `mutate()` call — run it directly on the column
  (`df$region_code |> haven::print_labels()`), not as part of a pipeline
  that produces a new data frame.

## 7. Large data management

Base tidyverse code (`dplyr` on an in-memory `data.frame`/`tibble`) is the
default for everything under section 5. Reach for one of the tools below
only when that default is measurably too slow or the data genuinely does
not fit in memory — do not adopt them pre-emptively "for speed."

**Data fits in RAM, but base dplyr is too slow.** Use `tidytable`. It
reimplements dplyr verbs directly on top of `data.table` (`mutate.()`,
`filter.()`, `summarize.()`, with the trailing dot marking the `tidytable`
verb), rather than translating/lazily deferring like `dtplyr` — so behavior
is more predictable and closer to a drop-in swap for the equivalent `dplyr`
call:

```r
library(tidytable)

summary_table <-
  large_df |>
  filter.(year >= 2015) |>
  mutate.(ln_value = log(value)) |>
  summarize.(mean_value = mean(ln_value, na.rm = TRUE), .by = region)
```

- Use `tidytable` only on the specific script or transformation that is
  actually slow, not as a blanket replacement for `dplyr` across a project.
  Say in a comment why the swap was needed (row count, join complexity, a
  measured runtime).
- Keep the same verb-to-operation mapping as section 5 (`filter.()` for
  scope, `mutate.()` for derived columns, and so on) — `tidytable` exists to
  preserve that readability, not to introduce `data.table`'s own
  `dt[i, j, by]` syntax into the codebase.

**Data does not fit in RAM.** Use `arrow` for I/O and `duckplyr` for
transformation, rather than trying to force a larger-than-memory problem
through `tidytable`/`data.table`, which are in-memory only.

- Read the data lazily with `arrow::open_dataset()` rather than
  `read_csv()`/`readRDS()`, so column and predicate pushdown avoid loading
  more than the query needs:

```r
library(arrow)
library(duckplyr)

dataset <- open_dataset("data/raw/large_panel/", format = "parquet")
```

- Prefer partitioned Parquet over a single large CSV/RDS for anything
  meant to be read this way — partition by the column most queries filter
  on (e.g. year), so `open_dataset()` can skip whole files.
- Transform with `duckplyr`, not manual SQL, so the code stays in dplyr
  syntax matching the rest of section 5:

```r
result <-
  dataset |>
  duckplyr::as_duckplyr_df() |>
  filter(year >= 2015) |>
  summarize(mean_value = mean(value, na.rm = TRUE), .by = region) |>
  collect()
```

- `duckplyr` falls back to ordinary `dplyr` automatically for a verb it
  doesn't yet support against a DuckDB relation — that fallback pulls data
  into memory, so if a script relies on it happening, note that in a
  comment; it means the larger-than-memory guarantee has been given up for
  that step.
- Always end a `duckplyr`/`arrow` pipeline with an explicit `collect()`
  (or an explicit write, e.g. `write_dataset()`) at the point the result is
  small enough to hold in memory or needs to leave the lazy engine — never
  let a script's final output silently stay a lazy, unmaterialized query.
- Check row counts before and after a `duckplyr` join or filter the same
  way section 5 asks for join validation — a lazy engine makes a silent
  cardinality blowup easy to miss until `collect()` runs out of memory.

## 8. Loops and conditions

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

## 9. Functions and abstraction

Linear code is the default. Most repeated research code should stay inline as
plain duplication, not become a function.

**When to write a helper.** Write a function only when a block of code,
varying only in 1-3 parameters (e.g. a dependent variable name, a control
string), is repeated **6 or more times**. The repeat count is the trigger by
itself — line count and complexity do not matter; a single repeated one-line
`feols()` call qualifies exactly as much as a repeated five-line block.

Once a helper is triggered, it should also:

- represent one named domain or file-reading operation;
- have clear inputs and one predictable return type; and
- make the calculation easier to follow, not harder.

These three describe what a *good* helper looks like. They are not additional
gates: do not withhold a helper that clears the 6-repeat trigger just because
one of these three feels marginal.

**Indentation for functions** follows the general rule in section 4.

```r
# Wrong: hand-duplicated 6+ times, only the DV changes
model_a <- feols(ln1_patents_A ~ treated, fixef = fx, data = df, cluster = cl)
model_b <- feols(ln1_patents_B ~ treated, fixef = fx, data = df, cluster = cl)
model_c <- feols(ln1_patents_C ~ treated, fixef = fx, data = df, cluster = cl)
# ... 5 more, differing only in the DV

# Right: one helper, driven by the varying parameter
run_patent_model <- function(dv) {
  feols(
    as.formula(paste(dv, "~ treated")),
    fixef = fx,
    data = df,
    cluster = cl
  )
}

patent_dvs <- c("ln1_patents_A", "ln1_patents_B", "ln1_patents_C")

patent_models <-
  patent_dvs |>
  map(run_patent_model) |>
  set_names(patent_dvs)
```

```r
# Wrong: abstracting something used only once or twice
compute_growth_rate <- function(x) (x - lag(x)) / lag(x)

df <- df |> mutate(growth = compute_growth_rate(value))

# Right: a two-off calculation stays inline
df <-
  df |>
  mutate(growth = (value - lag(value)) / lag(value))
```

**Write these inline instead of as a function:** a helper used only once, and
a thin wrapper that does nothing but call one package function. Duplicate the
code directly at each call site instead.

**Never write these at all, regardless of repeat count:** generic
configuration frameworks, factories, builders, custom classes, and needless
abstraction layers. These are software-engineering patterns, not research
code — the 6-repeat trigger above does not create an exception for them, and
there is no threshold at which they become acceptable in this codebase.

**Where a justified helper lives.**

- Default: define it at the top of the script that uses it, in the setup
  section, immediately after package loading, as a normal top-level
  assignment.
- If the same operation recurs across more than one script, move it to
  `code/functions/<verb>_<description>.R` and `source()` it from setup in
  every script that needs it. Never duplicate the same helper's body across
  multiple scripts once it's been promoted to `code/functions/`.

**Side effects:** keep file writes and plot saves at the top level, or pass
them through `walk()`/`walk2()`. A function or lambda passed as the first
argument to `walk()` is not a "custom function" under this rule — it is the
mechanism this convention requires for side effects, not an exception to
avoid.

## 10. Modelling and figures

- Use `feols()` from `fixest` for panel and fixed-effects regressions.
- Use `lm()` or `glm()` for cross-sectional work.
- `lm()` with `factor()` dummies is acceptable for panel models when
  downstream inference uses `fwildclusterboot`.
- Use `modelsummary()` for regression tables; use `output = "latex"` for
  LaTeX documents.
- Cluster standard errors at the unit of treatment assignment and document
  that choice directly above the model call.
- Use `ggplot2` for figures, built on a single named theme object defined
  once — in the script's setup section, or in
  `code/functions/theme_project.R` and `source()`d if reused across
  scripts, per section 9's promotion rule — rather than repeating a
  `theme()` block per figure:

```r
theme_project <- function(base_size = 14) {
  theme_minimal(base_size = base_size) +
    theme(
      text = element_text(family = "serif"),
      axis.text.x = element_text(angle = 45, hjust = 1),
      axis.line.x = element_line(colour = "black"),
      plot.background = element_rect(fill = "white", colour = "white"),
      panel.border = element_rect(colour = "black", fill = NA, linewidth = 1),
      panel.grid.major = element_line(linetype = "dashed"),
      panel.grid.minor = element_line(linetype = "dashed"),
      plot.caption = element_text(hjust = 0),
      legend.position = "bottom"
    )
}
```

- `base_size` defaults to 14. Drop it to 10-12 only for a figure embedded
  densely inside a paper's own figure environment, and say why in a
  comment above the call.
- Use `family = "serif"` by default, matching LaTeX/Beamer output. A
  project with a different house font overrides it once inside
  `theme_project()`, never per figure.
- Use a consistent non-default categorical palette, declared once as a
  named vector and reused across every figure in the project that shares
  that grouping, e.g.:

```r
group_palette <- c("Treatment" = "#0D3692", "Control" = "#E60F2D")
```

  This palette is illustrative, not mandatory — pick colors that fit the
  project, but declare them once and reuse them; never pick colors ad hoc
  per figure.
- Use sentence-case axis labels with units where applicable; keep legends
  at the bottom (`theme_project()`'s default) unless a project-specific
  layout genuinely needs an inset legend.
- Format count/currency axes with `scales::comma()` (or `scales::dollar()`/
  `scales::percent()` as appropriate) rather than leaving raw numeric
  labels.
- Add a `caption` in `labs()` naming the data source for any figure meant
  to leave the codebase as a deliverable.
- Mark a reference date or threshold (e.g. a treatment start) with
  `geom_vline(linetype = "dashed")`, not a plain solid line, so it reads as
  a marker rather than data.
- Use `patchwork` (`p1 + p2 + plot_annotation(...)`) to combine related
  figures into one multi-panel deliverable, rather than saving them
  separately and combining outside R.
- `ggsave()` must specify `width`, `height`, and `units` explicitly
  (`units = "cm"` is the convention used elsewhere in this codebase); add
  `dpi` explicitly for raster output.
- Deliverable figures should be saved as both `.png` and `.pdf` unless the
  task specifies another format. Use `bg = "transparent"` for Beamer figures.

## 11. Excel output

Use `openxlsx2` for reading and writing `.xlsx` files. Do not use `openxlsx`,
`xlsx`, or `writexl` in new code — `openxlsx2` is the only supported package
for spreadsheet output, so that a single API and object model is used across
the codebase.

- Build workbooks with the tidyverse-style, piped `openxlsx2` interface
  (`wb_workbook()` and the `wb_add_*()` family), one operation per line, same
  as any other pipe chain in section 4:

```r
wb <-
  wb_workbook() |>
  wb_add_worksheet(sheet = "Summary") |>
  wb_add_data(sheet = "Summary", x = summary_table) |>
  wb_add_data_table(sheet = "Summary", x = summary_table, table_name = "summary_tbl") |>
  wb_freeze_pane(sheet = "Summary", first_row = TRUE)

wb_save(wb, "outputs/tables/summary.xlsx")
```

- Name each worksheet after its content in `snake_case` or short Title Case
  (`"Summary"`, `"Monthly DD Results"`), never `"Sheet1"`.
- Write one logical table per worksheet. Do not stack multiple unrelated
  tables on one sheet.
- Use `wb_add_data_table()` (not plain `wb_add_data()`) whenever the output
  is meant to be filtered or sorted by the reader — it registers a proper
  Excel table object, not just a data range.
- Apply number formats explicitly with `wb_add_numfmt()` for currency,
  percentage, or date columns; do not leave numeric formatting to Excel's
  auto-detection.
- Follow section 4's path rules: save to a plain relative path under
  `outputs/tables/`, creating the directory first if it may not exist.

**Charts.** Use `mschart` to build native, editable Excel chart objects, then
insert them into the `openxlsx2` workbook. Do not save a `ggplot2` figure as
an image and paste it into Excel when the deliverable is meant to be
interactive or editable in Excel — build the chart natively instead.

```r
chart <-
  ms_barchart(data = summary_table, x = "province", y = "estimate") |>
  chart_settings(dir = "horizontal", grouping = "clustered") |>
  chart_labels(title = "Estimated effect by province", ylab = "Estimate")

wb <-
  wb_workbook() |>
  wb_add_worksheet(sheet = "Chart") |>
  wb_add_mschart(sheet = "Chart", graph = chart, dims = "B2:J20")

wb_save(wb, "outputs/tables/chart_output.xlsx")
```

- Use the same non-default palette specified for `ggplot2` in section 10 when
  setting chart series colors in `mschart`, so Excel deliverables and
  `ggplot2` figures stay visually consistent.
- State chart titles and axis labels in sentence case with units, matching
  section 10.
- Only fall back to a static image (`ggplot2` + `wb_add_image()`) when the
  deliverable explicitly does not need to be edited or re-sorted in Excel by
  the recipient — state that reasoning in a comment above the call.

## 12. Outputs and reproducibility

- Use `saveRDS()` for key models, summary tables, and processed data used by
  downstream scripts.
- Treat a missing `saveRDS()` for a downstream-referenced object as a
  critical reproducibility problem.
- Write important processed data and final results in documented formats.
- Keep a simple run record with selected source filenames, selected year,
  method, and output location.
- Do not add hashes, checksums, manual approval fields, or input locks unless
  a separate project requirement explicitly calls for them.
- A style-only rewrite must reproduce accepted numerical outputs.
- An estimation change is complete only after actual values reconcile with a
  known total, benchmark, or accepted comparison.

## 13. Missing values and numerical discipline

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
- Check transformation links and domain constraints before extending a
  series.

## 14. Comments, errors, and console output

- Comments must be used throughout, at the density set in section 1.
- Comments explain why a non-obvious rule exists.
- Do not keep commented-out dead code, except the deterministic
  `# set.seed(42)` marker.
- Use `message()` at most once per major stage when useful.
- Do not use `cat()`, `print()`, or `sprintf()` for status output.
- Do not print progress for every file, row, or iteration.
- Error messages should name the failing file, field, year, or series.

## 15. Reproducible research workflow

All analytical steps must be in code. Every reported number must be traceable
to a script.

Use this structure when setting up a research project:

```text
project-root/
├── README.md
├── MASTER.R
├── data/{raw,intermediate,final}/
├── code/{cleaning,analysis,functions}/
├── outputs/graphs/
├── documentation/
└── .gitignore
```

- Raw data is never modified.
- Raw, intermediate, and final data remain separate.
- Code and data structures mirror each other where practical.
- Number scripts with `NN_verb_description.R` when execution order matters.

### Programmatic data acquisition

Prefer downloading data with an R package or API client over manually
downloading a file through a browser and dropping it into `data/raw/`. A
programmatic download is itself part of the reproducible pipeline; a manual
one is not — it can't be re-run, re-dated, or verified by another analyst,
and it hides the actual source (table ID, query parameters, vintage) that
produced the raw file.

- For Statistics Canada tables, use `cansim` (`get_cansim()`) rather than
  manually exporting a CSV from the StatCan website.
- For census data, use `cancensus` (`get_census()`) against the
  CensusMapper API rather than manually downloading census profile files.
- For any other data source with an API or R package (other StatCan/ISED
  data portals, CMHC, PUMF-hosting portals, etc.), prefer that
  package/API path the same way. Only fall back to a manual download when
  no programmatic path genuinely exists, and say so explicitly in the
  script header's Purpose field or a codebook note — a manual download
  should always be a stated exception, never the unstated default.
- A programmatic download is its own numbered step in `code/cleaning/`
  (e.g. `00_download_<source>.R`), following the naming rule below — not
  something run ad hoc outside the pipeline.
- Cache the downloaded extract to `data/raw/` immediately after fetching
  (`saveRDS()` or an equivalent write right after the API call), so
  re-running the pipeline doesn't require hitting the API again. Treat
  that cached file as the immutable raw data from that point on, per the
  rule above.

**Naming data-cleaning scripts specifically.** Every script in
`code/cleaning/` follows `NN_clean_<dataset>.R`, where `<dataset>` names the
specific source or component being cleaned — not a generic label like `data`
or `main`. One cleaning script handles one dataset's cleaning stage only; a
script that cleans and merges two datasets is a scope violation and should be
split.

Examples: `01_clean_patents_main.R`, `02_clean_statcan_monthly.R`,
`03_clean_interested_parties.R`.

If a dataset requires more than one cleaning stage (e.g. extraction, then
column cleaning, then deduplication), separate them by verb rather than
merging into one script: `01_extract_patents_main.R`,
`02_clean_patents_main.R`, `03_dedupe_patents_main.R`. Use `extract_` for
pulling raw source files into a loadable format, `clean_` for column typing,
renaming, and filtering, and `dedupe_`/`reshape_`/`merge_` for the
corresponding later stages, each as its own numbered script.

- Use README files to document folder purpose, contents, naming, and
  dependencies.
- The master script is the single reproducible entry point.
- Do not put a Git repository inside a shared Dropbox, OneDrive, or Google
  Drive folder.
- Do not commit raw or sensitive data, credentials, large generated outputs,
  or temporary files.

## 16. Review standard

This section is the checklist `r-reviewer` runs against. Review active R code
in this order, checking each category against the specific rules in the
sections named:

1. **Correctness** — transformations, joins, modelling, and outputs match the
   documented method; survey estimates use a correctly specified
   `srvyr`/`survey` design (weights, strata, ids) and report standard errors,
   not unweighted figures mislabelled as population estimates (sections 5,
   6, 10, 11, 13).
2. **Reproducibility and path discipline** — no `setwd()`, no hardcoded
   machine paths, `saveRDS()` present for every downstream-referenced object,
   project structure and script naming match section 15 (sections 4, 12, 15).
3. **Input and result validation** — `na.rm` stated explicitly, finiteness
   checked, period counts checked before annualizing, floating-point
   comparisons avoid `==` (section 13). There is no built-in `lintr` rule that
   detects a missing `na.rm`; this stays a manual check every time.
4. **Downstream artifacts and saved objects** — `.rds`, `.xlsx`, `.png`/`.pdf`
   outputs exist, are named descriptively, and match what the script's header
   documents as its Outputs (sections 2, 10, 11, 12).
5. **Code structure and tidyverse conventions** — verbs match operations,
   joins use `join_by()` with `multiple`/`unmatched`, no `for`/`while`/`apply`
   on data, function use follows the 6-repeat rule in section 9, not a
   subjective judgment call (sections 5, 8, 9). `.lintr`'s
   `for_loop_index_linter()` only flags the classic `for (i in
   seq_along(x))`-style loop-index pattern; it does not catch every
   `for`/`while`/`repeat`/`apply` use banned in section 8, so this check
   still requires reading the code, not just a clean `lintr` run.
6. **Style and polish** — run `lintr::lint_dir("scripts")` against `.lintr`
   and treat every result as a formal finding at the severity `lintr`
   assigns; run `scripts/style_project.R` and treat any file it changes as
   evidence the submitted version wasn't `styler`-clean. Comment density and
   naming length (section 1) remain manual checks — `lintr` does not enforce
   these (sections 1, 4).

**Automation gaps.** `.lintr` and `styler` cover most of sections 4 and 8,
but two rules have no automated check and must be verified by reading the
code, not inferred from a clean `lintr`/`styler` run: `for_loop_index_linter()`
catches only loop-index patterns, not every `for`/`while`/`repeat` use banned
in section 8; and there is no built-in linter that flags a missing `na.rm` in
section 13's `sum()`/`mean()`/`sd()`/`var()` calls. A clean automated pass on
these two points is not evidence of compliance.

A finding that cites a rule outside these sections is out of scope for this
review — flag it separately as a suggestion, not as a standard violation.

Formal findings include the file and line number, category, severity
(Critical, High, Medium, or Low), current code, proposed fix, and rationale.
Reviewers do not edit source files. Save formal reports to
`quality_reports/[script_name]_r_review.md`.

## 17. Known pitfalls

- Put robustness specifications in the same analysis script as the main
  model, with separate output names, rather than creating a script that only
  repeats the existing model.
- Validate joins, period coverage, and numerical finiteness before trusting a
  successful process exit status.

## 18. AI routing

This root file is the only normative coding standard. The other files have
specialized roles:

- `.claude/agents/` defines Claude role behavior.
- `.claude/skills/` provides specialized workflow skills.
- `.codex/skills/` defines Codex role behavior and UI metadata.
- `.github/` provides project context and Copilot routing.

Role selection:

- `r-coder`: implement or substantially revise one R script;
- `r-reviewer`: audit R scripts and produce a quality report; and
- `r-build-and-review`: write, then review, an R script.

If instructions conflict, use this file first, then the role-specific file,
then general project context.
