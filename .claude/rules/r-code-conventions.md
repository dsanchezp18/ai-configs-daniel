# R Code Conventions

Canonical standards for all R scripts in this project. Both `r-coder` and `r-reviewer` read this file. Where this file conflicts with agent defaults, this file wins.

---

## 0. Philosophy

- **Expressive over engineered.** Code should read like a clear narrative from top to bottom. A researcher should be able to open any script, read it linearly, and debug any line in isolation.
- **Linear code by default.** Prefer sequential, script-first code. The default is: no helper functions, no abstraction layers, no wrappers. Write code that runs straight down the page.
- **Never write a custom function unless absolutely necessary.** A function is justified only when the alternative is exact, verbatim repetition of 10+ lines called 3+ times. "Reduces line count" or "looks cleaner" are not sufficient reasons. When in doubt, inline it. Flag any custom function whose body is fewer than 10 lines, or that is called only once or twice, as a **High** issue.
- **No premature optimization.** Write for clarity first. Only optimize if a real performance bottleneck exists.
- **Match the surroundings.** When editing an existing script, match the tone and structure of the code around the edit.
- **Tidyverse throughout.** Prefer tidy patterns over base R loops or the `apply` family.

---

## 1. Assignment & Pipes

- Use `<-` for assignment — never `=`.
- Use the native pipe `|>` — never `%>%`.
- One pipe step per line; each step on its own line.

```r
# correct
result <- data |>
  filter(year >= 2010) |>
  mutate(log_gdp = log(gdp))

# wrong
result = data %>% filter(year >= 2010) %>% mutate(log_gdp = log(gdp))
```

---

## 2. Packages

- `library()` at the top of the script — never `require()`, never mid-script.
- Avoid `pkg::fn()` inline when the package is already loaded and there is no ambiguity. **Exception — required:** use `pkg::fn()` whenever two loaded packages export a function with the same name (e.g., `dplyr::select` when `MASS` is also loaded). When in doubt, qualify. A silent wrong-dispatch bug is worse than a redundant prefix.

---

## 3. Script Structure

Every script must begin with this header — no exceptions:

```r
# ============================================================
# [Descriptive Title]
# Author: [Name]
# Purpose: [What this script does]
# Inputs:  [Data files or RDS objects read]
# Outputs: [Files written: data, figures, tables]
# ============================================================
```

Followed by numbered top-level sections using RStudio-style markers:

```r
# 0. Setup ----
# 1. Load Data ----
# 2. Clean / Transform ----
# 3. Analysis ----
# 4. Figures ----
# 5. Export ----
```

- Add or rename sections to fit the task; never omit `# 0. Setup ----`.
- `set.seed(42)` at the top when the script has stochastic steps. When the script is deterministic, include it commented out: `# set.seed(42)`.
- `sessionInfo()` at the very end of every script.

---

## 4. Tidyverse Style

- `dplyr` for all data manipulation.
- `ggplot2` for all figures.
- `stringr`, `lubridate`, `forcats` as needed.
- `snake_case` for all variable and object names.
- Explicit column selection — never positional indexing (e.g., `df[, 3]`).

### Grouping (dplyr 1.1+)

- Both `.by` and `group_by() |> ungroup()` are acceptable. Prefer `.by` when it reads more clearly, but do not flag `group_by()` usage as an issue.

- Use `pick()` when you need column selection inside a data-masking function (e.g., inside `summarise()` or `mutate()`).
- Use `reframe()` — not `summarise()` — when the result has more than one row per group.

### Joins (dplyr 1.1+)

- Use `join_by()` instead of character-vector `by =` arguments.
- Use `multiple` and `unmatched` to make match expectations explicit and catch data quality issues early.

```r
# correct
transactions |>
  inner_join(companies, by = join_by(company == id))

# correct — inequality join
transactions |>
  inner_join(companies, join_by(company == id, year >= since))

# correct — assert 1:1 match
inner_join(x, y, by = join_by(id), multiple = "error", unmatched = "error")

# avoid — old character vector syntax
inner_join(x, y, by = c("company" = "id"))
```

### purrr (purrr 1.0+)

- Use `map(x, f) |> list_rbind()` instead of the superseded `map_dfr()`.
- Use `map(x, f) |> list_cbind()` instead of the superseded `map_dfc()`.
- Use `walk()` / `walk2()` for side effects (writing files, saving plots) — not `map()` discarding results.

```r
# correct
plots |>
  walk2(output_paths, \(p, path) ggsave(path, p, width = 8, height = 5))

# superseded — avoid
map_dfr(data_list, clean_and_summarise)
```

### Strings

- Always prefer `stringr` functions over base R equivalents — argument order is consistent and they are pipe-friendly.

```r
# correct
text |>
  str_to_lower() |>
  str_trim() |>
  str_replace_all("pattern", "replacement")

# avoid
tolower(gsub("pattern", "replacement", trimws(text)))
```

Common substitutions:

| base R | stringr |
|--------|---------|
| `grepl("p", x)` | `str_detect(x, "p")` |
| `gsub("a", "b", x)` | `str_replace_all(x, "a", "b")` |
| `substr(x, 1, 5)` | `str_sub(x, 1, 5)` |
| `nchar(x)` | `str_length(x)` |
| `strsplit(x, ",")` | `str_split(x, ",")` |
| `paste0(a, b)` | `str_c(a, b)` |
| `tolower(x)` | `str_to_lower(x)` |

---

## 5. Survey Data

- Always use `srvyr` for survey-weighted operations — never base `survey` package functions directly.
- Declare the survey design once with `as_survey_design()` or `as_survey_rep()` and store it as a named object; do not re-declare it inline.
- All weighted summaries (`survey_mean()`, `survey_total()`, `survey_ratio()`, etc.) must go through the `srvyr` tidy interface — pipe into `summarise()` as with any other `dplyr` workflow.
- Set `vartype = "ci"` or `vartype = "se"` explicitly on every estimate call — never rely on the default.
- Never drop survey weights or design variables mid-pipeline; treat the design object as immutable after declaration.

```r
# correct
endi_design <- endi_clean |>
  as_survey_design(ids = upm, strata = estrato, weights = fexp)

esti <- endi_design |>
  filter(age_group == "under5") |>
  summarise(prev = survey_mean(stunted, vartype = "ci", na.rm = TRUE))

# wrong — base survey package, no srvyr
svymean(~stunted, design = endi_design_svyobj)
```

---

## 6. Modelling

- `feols()` (from `fixest`) for all panel and fixed-effects regressions.
- `lm()` / `glm()` for cross-sectional work. Exception: `lm()` with `factor()` dummies is also acceptable for panel models when the downstream inference uses `fwildclusterboot`, which does not accept `feols()` objects.
- `modelsummary()` for regression tables — tinytable backend by default; use `output = "latex"` for LaTeX documents.
- Cluster standard errors at the unit of treatment assignment. Document the choice in a comment directly above the model call.

```r
# Clustering at firm level — treatment assigned at firm level
fit <- feols(y ~ x | firm + year, data = df, cluster = ~firm)
```

---

## 7. Output

- `ggsave()` must always specify `width` and `height` explicitly.
- `saveRDS()` for all key objects (model fits, summary tables, processed datasets) so downstream scripts and slides can load them without re-running.
- A missing `saveRDS()` for an object referenced downstream silently breaks slide rendering — treat as **Critical**.

---

## 8. Paths

- All paths relative to the project root — this is an R project, so `setwd()` is unnecessary and should never appear.
- Build paths with `file.path()` — no string pasting, no hardcoded absolute paths.
- No magic numbers anywhere in the script. Named constants at the top of the Setup section instead.
- `dir.create(..., recursive = TRUE)` before writing to any folder that may not exist.

```r
# correct — named constant, relative path
output_dir <- file.path("outputs", "figures")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

# wrong
setwd("C:/Users/daniel/project")
ggsave("C:/Users/daniel/project/outputs/fig1.png", width = 8, height = 5)
```

---

## 9. Comments

- Write comments to clarify intent when helpful — but avoid noisy comments that restate what the code already says clearly.
- Prefer explaining **why** over **what** when a comment is warranted.
- No commented-out dead code (exception: the `# set.seed(42)` stub above).

---

## 10. Numerical Discipline

- **No float equality.** Never `==` on doubles. Use `all.equal()` or `abs(x - y) < tol`.
- **CDF clamping.** Probabilities passed to `qnorm()`, `pbinom()`, etc. must be clamped: `eps <- 1e-12; pmin(1 - eps, pmax(eps, p))`. Exact 0 or 1 produce `-Inf`/`Inf`.
- **Explicit `na.rm`.** All `mean()`, `sum()`, `var()`, `sd()` calls on empirical data must set `na.rm = TRUE` or `na.rm = FALSE` — never rely on the default.

---

## 11. Console Output

- At most one `message()` per major section.
- Never `cat()`, `print()`, or `sprintf()` for status output.
- No per-iteration prints inside loops.

---

## 12. Known Pitfalls

*Add project-specific bugs and gotchas here as they are discovered.*

- **Hardcoding variable codes without verification.** Before writing bin definitions, verify the actual codes by reading label attributes or the codebook from the source file. Asserting codes from memory is a bug risk. Flag any categorical bin or filter that lacks a comment citing the verified source as a **Medium** issue.

- **Robustness specs belong in the same script as the main analysis.** Do not create a new script solely for a controlled or alternative specification of an existing model. Add it as a clearly numbered section in the same script, with separate output file names. Flag a new script whose only purpose is a robustness variant of an existing script as a **Medium** structural issue.
