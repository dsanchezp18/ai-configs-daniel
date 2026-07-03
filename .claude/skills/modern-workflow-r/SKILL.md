---
name: modern-workflow-r
description: >
  Reference guide for modern R development best practices: native pipe, dplyr 1.1+ patterns
  (.by grouping, join_by, reframe, pick), rlang metaprogramming ({{}} embrace, injection,
  pronouns), purrr 1.0+ patterns (list_rbind, in_parallel), vctrs, S7, stringr, and
  performance profiling. Use whenever writing or reviewing R code that involves tidy
  evaluation, functional programming, performance optimization, or OOP class design.
---

# Modern R Development Guide

*Current best practices for R development, emphasizing modern tidyverse patterns, performance, and style. Last updated: August 2025*

## Core Principles

1. **Use modern tidyverse patterns** — Prioritize dplyr 1.1+ features, native pipe, and current APIs
2. **Profile before optimizing** — Use profvis and bench to identify real bottlenecks
3. **Write readable code first** — Optimize only when necessary and after profiling
4. **Follow tidyverse style guide** — Consistent naming, spacing, and structure

---

## Modern Tidyverse Patterns

### Pipe Usage (`|>` not `%>%`)
- **Always use native pipe `|>` instead of magrittr `%>%`**
- R 4.3+ provides all needed features
```r
# Good - Modern native pipe
data |> 
  filter(year >= 2020) |>
  summarise(mean_value = mean(value))

# Avoid - Legacy magrittr pipe  
data %>% 
  filter(year >= 2020) %>%
  summarise(mean_value = mean(value))
```

### Join Syntax (dplyr 1.1+)
- **Use `join_by()` instead of character vectors for joins**
- **Support for inequality, rolling, and overlap joins**
```r
# Good - Modern join syntax
transactions |> 
  inner_join(companies, by = join_by(company == id))

# Good - Inequality joins
transactions |>
  inner_join(companies, join_by(company == id, year >= since))

# Good - Rolling joins (closest match)
transactions |>
  inner_join(companies, join_by(company == id, closest(year >= since)))

# Avoid - Old character vector syntax
transactions |> 
  inner_join(companies, by = c("company" = "id"))
```

### Multiple Match Handling
- **Use `multiple` and `unmatched` arguments for quality control**
```r
# Expect 1:1 matches, error on multiple
inner_join(x, y, by = join_by(id), multiple = "error")

# Allow multiple matches explicitly  
inner_join(x, y, by = join_by(id), multiple = "all")

# Ensure all rows match
inner_join(x, y, by = join_by(id), unmatched = "error")
```

### Data Masking and Tidy Selection
- **Understand the difference between data masking and tidy selection**
- **Use `{{}}` (embrace) for function arguments**
- **Use `.data[[]]` for character vectors**

```r
# Data masking functions: arrange(), filter(), mutate(), summarise()
# Tidy selection functions: select(), relocate(), across()

# Function arguments - embrace with {{}}
my_summary <- function(data, group_var, summary_var) {
  data |>
    group_by({{ group_var }}) |>
    summarise(mean_val = mean({{ summary_var }}))
}

# Character vectors - use .data[[]]
for (var in names(mtcars)) {
  mtcars |> count(.data[[var]]) |> print()
}

# Multiple columns - use across()
data |> 
  summarise(across({{ summary_vars }}, ~ mean(.x, na.rm = TRUE)))
```

### Modern Grouping and Column Operations
- **Use `.by` for per-operation grouping (dplyr 1.1+)**
- **Use `pick()` for column selection inside data-masking functions**
- **Use `across()` for applying functions to multiple columns**
- **Use `reframe()` for multi-row summaries**

```r
# Good - Per-operation grouping (always returns ungrouped)
data |>
  summarise(mean_value = mean(value), .by = category)

# Good - Multiple grouping variables
data |>
  summarise(total = sum(revenue), .by = c(company, year))

# Good - pick() for column selection
data |>
  summarise(
    n_x_cols = ncol(pick(starts_with("x"))),
    n_y_cols = ncol(pick(starts_with("y")))
  )

# Good - across() for applying functions
data |>
  summarise(across(where(is.numeric), mean, .names = "mean_{.col}"), .by = group)

# Good - reframe() for multi-row results
data |>
  reframe(quantiles = quantile(x, c(0.25, 0.5, 0.75)), .by = group)

# Avoid - Old persistent grouping pattern
data |>
  group_by(category) |>
  summarise(mean_value = mean(value)) |>
  ungroup()
```

---

## Modern rlang Patterns for Data-Masking

### Core Concepts

**Data-masking** allows R expressions to refer to data frame columns as if they were variables in the environment. rlang provides the metaprogramming framework that powers tidyverse data-masking.

#### Key rlang Tools
- **Embracing `{{}}`** — Forward function arguments to data-masking functions
- **Injection `!!`** — Inject single expressions or values
- **Splicing `!!!`** — Inject multiple arguments from a list
- **Dynamic dots** — Programmable `...` with injection support
- **Pronouns `.data`/`.env`** — Explicit disambiguation between data and environment variables

### Function Argument Patterns

#### Forwarding with `{{}}`
```r
# Single argument forwarding
my_summarise <- function(data, var) {
  data |> dplyr::summarise(mean = mean({{ var }}))
}

# Works with any data-masking expression
mtcars |> my_summarise(cyl)
mtcars |> my_summarise(cyl * am)
```

#### Forwarding `...`
```r
my_group_by <- function(.data, ...) {
  .data |> dplyr::group_by(...)
}

# For single-argument tidy selections, wrap in c()
my_pivot_longer <- function(.data, ...) {
  .data |> tidyr::pivot_longer(c(...))
}
```

#### Names Patterns with `.data`
```r
# Single column by name
my_mean <- function(data, var) {
  data |> dplyr::summarise(mean = mean(.data[[var]]))
}

# Multiple columns with all_of()
my_select_vars <- function(data, vars) {
  data |> dplyr::select(all_of(vars))
}
```

### Injection Operators

| Operator | Use Case | Example |
|----------|----------|---------|
| `{{ }}` | Forward function arguments | `summarise(mean = mean({{ var }}))` |
| `!!` | Inject single expression/value | `summarise(mean = mean(!!sym(var)))` |
| `!!!` | Inject multiple arguments | `group_by(!!!syms(vars))` |
| `.data[[]]` | Access columns by name | `mean(.data[[var]])` |

#### Advanced Injection
```r
# Create symbols from strings
var <- "cyl"
mtcars |> dplyr::summarise(mean = mean(!!sym(var)))

# Splicing with !!!
vars <- c("cyl", "am")
mtcars |> dplyr::group_by(!!!syms(vars))
```

### Dynamic Dots Patterns

```r
my_function <- function(...) {
  dots <- list2(...)
}

# Enables:
my_function(a = 1, b = 2)           # Normal usage
my_function(!!!list(a = 1, b = 2))  # Splice a list
my_function("{name}" := value)      # Name injection
```

#### Name Injection with Glue Syntax
```r
my_mean <- function(data, var) {
  data |> dplyr::summarise("mean_{{ var }}" := mean({{ var }}))
}

mtcars |> my_mean(cyl)  # Creates column "mean_cyl"

# Allow custom names with englue()
my_mean <- function(data, var, name = englue("mean_{{ var }}")) {
  data |> dplyr::summarise("{name}" := mean({{ var }}))
}
```

### Pronouns for Disambiguation
```r
cyl <- 1000  # Environment variable

mtcars |> dplyr::summarise(
  data_cyl = mean(.data$cyl),   # Data frame column
  env_cyl  = mean(.env$cyl),    # Environment variable
)
```

### Error-Prone Patterns to Avoid
```r
# Avoid - String parsing and eval (security risk)
var <- "cyl"
eval(parse(text = paste("mean(", var, ")")))  # Dangerous!

# Good - Symbol creation and injection
mtcars |> summarise(mean = mean(!!sym(var)))  # Safe
# or
mtcars |> summarise(mean = mean(.data[[var]]))  # Even safer
```

---

## Performance Best Practices

### Performance Tool Selection Guide

| Tool | Use When | What It Shows |
|------|----------|---------------|
| **`profvis`** | Complex code, unknown bottlenecks | Time per line, call stack |
| **`bench::mark()`** | Comparing alternatives | Relative performance, memory |
| **`system.time()`** | Quick checks | Total runtime only |

#### Step-by-Step Performance Workflow
```r
# 1. Profile first
library(profvis)
profvis({ your_slow_code() })

# 2. Benchmark alternatives for hot spots
library(bench)
bench::mark(
  current     = current_approach(data),
  vectorized  = vectorized_approach(data)
)
```

#### Parallel Processing Decision
```r
# Helps when: CPU-intensive, embarrassingly parallel, large datasets, I/O bound
# Hurts when: simple fast operations (overhead > benefit), small datasets

# Good for parallel
map(1:100, in_parallel(expensive_func))  # ~10s -> ~2.5s on 4 cores

# Bad for parallel (overhead > benefit)
map(1:100, in_parallel(fast_func))       # 100μs -> 50ms (500x slower!)
```

#### Data Backend Selection
```r
# data.table: very large datasets (>1GB), maximum performance critical
# dplyr:      readability priority, moderate data (<100MB), complex joins
# base R:     no dependencies, simple operations, teaching contexts
```

### Performance Anti-Patterns
```r
# Don't grow objects in loops
result <- c()
for (i in 1:n) result <- c(result, compute(i))  # Slow!

# Pre-allocate or use purrr
result <- map(1:n, compute)
```

---

## When to Use vctrs

### Use vctrs when:
- Building custom vector classes (factor-like, date-like, numeric-like)
- Need type-stable vector operations in package functions
- Need consistent coercion/casting behavior
- Building data frame-compatible classes

### Don't use vctrs when:
- Simple one-off analyses (base R is sufficient)
- Performance critical + simple operations
- No custom classes needed

```r
# Basic vector class pattern
new_percent <- function(x = double()) {
  vec_assert(x, double())
  new_vctr(x, class = "pkg_percent")
}

percent <- function(x = double()) {
  x <- vec_cast(x, double())
  new_percent(x)
}
```

---

## Modern purrr Patterns (purrr 1.0+)
```r
# Modern data frame row binding — replaces map_dfr()
models <- data_splits |> 
  map(\(split) train_model(split)) |>
  list_rbind()

# Column binding — replaces map_dfc()
summaries <- data_list |> 
  map(\(df) get_summary_stats(df)) |>
  list_cbind()

# Side effects with walk()
walk2(data_list, plot_names, \(df, name) {
  p <- ggplot(df, aes(x, y)) + geom_point()
  ggsave(name, p)
})

# Parallel processing (purrr 1.1.0+ + mirai)
library(mirai)
daemons(4)
results <- large_datasets |> map(in_parallel(expensive_computation))
daemons(0)
```

### Superseded purrr functions
```r
map_dfr(x, f)     -> map(x, f) |> list_rbind()
map_dfc(x, f)     -> map(x, f) |> list_cbind()
map2_dfr(x, y, f) -> map2(x, y, f) |> list_rbind()
pmap_dfr(list, f) -> pmap(list, f) |> list_rbind()
```

---

## String Manipulation with stringr
```r
# Prefer stringr over base R
str_detect(text, "pattern")      # vs grepl("pattern", text)
str_extract(text, "pattern")     # vs complex regmatches()
str_replace_all(text, "a", "b") # vs gsub("a", "b", text)
str_split(text, ",")             # vs strsplit(text, ",")
str_length(text)                 # vs nchar(text)
str_sub(text, 1, 5)              # vs substr(text, 1, 5)
str_c("a", "b")                  # vs paste0()
str_glue("Hello {name}!")        # templating
str_to_lower(text)               # vs tolower()
str_to_title(text)               # vs tools::toTitleCase()

# Pattern helpers for clarity
str_detect(text, fixed("$"))         # literal match
str_detect(text, regex("\\d+"))      # explicit regex
str_detect(text, coll("é", locale = "fr"))  # collation
```

---

## OOP System Decision Matrix

**What are you building?**

- **Vector-like objects** (things that behave like atomic vectors) → **vctrs**
- **General objects, new projects, need validation/multiple dispatch** → **S7**
- **Simple classes, maximum compatibility, existing S3 ecosystems** → **S3**
- **Bioconductor or existing S4 codebase** → **S4**

| Feature | S3 | S7 | When S7 wins |
|---------|----|----|---------------|
| Class definition | Informal | Formal (`new_class()`) | Need guaranteed structure |
| Property access | `$` / `attr()` (unsafe) | `@` (safe, validated) | Validation matters |
| Multiple dispatch | Limited | Full | Complex dispatch needed |
| Inheritance | Informal | Explicit `super()` | Predictable inheritance |
| Performance | Fastest | ~Same as S3 | Negligible difference |

```r
# S7 example
Range <- new_class("Range",
  properties = list(start = class_double, end = class_double),
  validator = function(self) {
    if (self@end < self@start) "@end must be >= @start"
  }
)
x <- Range(start = 1, end = 10)
```

---

## Migration Quick Reference

### Base R → Modern Tidyverse
```r
subset(data, condition)         -> filter(data, condition)
data[order(data$x), ]          -> arrange(data, x)
aggregate(x ~ y, data, mean)   -> summarise(data, mean(x), .by = y)
sapply(x, f)                   -> map(x, f)
grepl("pat", text)             -> str_detect(text, "pat")
gsub("old", "new", text)       -> str_replace_all(text, "old", "new")
```

### Old → New Tidyverse
```r
data %>% f()                         -> data |> f()
group_by(x) |> summarise() |> ungroup() -> summarise(.by = x)
by = c("a" = "b")                   -> by = join_by(a == b)
gather()/spread()                    -> pivot_longer()/pivot_wider()
separate(col, into = c("a","b"))     -> separate_wider_delim(col, delim = "_", names = c("a","b"))
```
