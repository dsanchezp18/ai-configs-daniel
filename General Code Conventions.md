# General Code Conventions

Multi-language coding standard for statistical and research code in this
repository. Each section below covers one language. The R section is a
pointer only — R's conventions are large enough to warrant their own file
and already live in [`R Code Conventions.md`](R%20Code%20Conventions.md),
which stays canonical for R. The Stata, Python, and Julia sections contain
their conventions directly, in this file.

All four sections share the same working philosophy: write code for the
researcher who reviews it next year — readable, linear, commented at a fixed
density, using 1-4 word snake_case names, with each transformation small
enough to inspect on its own. See `R Code Conventions.md` section 1 for the
full statement of that philosophy; it applies to every language below
without being restated per section.

Operational agent and skill files may add role-specific behavior, but they
must not contradict this file or `R Code Conventions.md`, or copy their
normative rules.

---

## R

See [`R Code Conventions.md`](R%20Code%20Conventions.md) for the full R
standard: working philosophy, script structure, packages, tidyverse data
work, survey data management, loops, functions, modelling and figures, Excel
output, reproducibility, missing values, comments, reproducible research
workflow, review standard, and known pitfalls. Do not duplicate any of that
here — if a Stata/Python/Julia rule below needs to reference an R rule,
point to the specific section in `R Code Conventions.md` instead of copying
it.

---

## Stata

### 1. Script structure

Every active do-file begins with this header:

```stata
* ============================================================
* Descriptive title
* Author: Daniel Sanchez
* Purpose: What this script does
* Inputs:  Files or datasets read
* Outputs: Files or datasets written
* ============================================================

version 18
clear all
set more off
```

Followed by numbered sections, adapted to the task but never omitting setup:

```stata
* 0. Setup
* 1. Read inputs
* 2. Check inputs
* 3. Prepare data
* 4. Calculate estimates
* 5. Check results
* 6. Write outputs
```

- Use `set seed 42` at the top when the script is stochastic; omit it for
  deterministic scripts.
- Open a log at the top of Setup with `capture log close` immediately
  followed by `log using "logs/<script_name>.log", replace`, and `log
  close` at the very end. The `capture log close` guard is required even
  though no log should normally be open — it makes the script safe to
  re-run after an interrupted previous run without erroring on an
  already-open log. Never leave a log silently overwritten without
  `replace` stated explicitly.
- End every do-file with `exit` only if the file is meant to be run
  standalone from a longer chain; otherwise let it fall through.

### 2. Packages (user-written commands)

- Install user-written commands (`ssc install`, `net install`) once, outside
  any production do-file — from an interactive session or a documented
  one-time setup script (`code/setup/install_packages.do`), never inside a
  script that runs as part of the pipeline.
- Pin the set of required user-written commands in a single
  `code/setup/install_packages.do` that lists every `ssc install` the
  project needs, so a fresh clone can bootstrap its environment.
- Never call `ssc install` or `net install` conditionally on whether a
  command already exists — that silently reinstalls at unpredictable
  versions. If a version pin matters, document it in the setup script's
  comments.

### 3. Naming, paths, and formatting

- Use `snake_case` for do-files, variables, and locals/globals.
- Use nouns for variables, verbs for program names.
- Build paths from a single project-root global set once in the master
  do-file (`global root "..."`), never with a hardcoded drive letter,
  username, or absolute machine path elsewhere.
- Never use `cd`. Reference files as `"$root/data/raw/file.dta"`, not by
  changing the working directory.
- Indent 4 spaces per logical block (`if`, `foreach`, `forvalues`, `program
  define`); align continuation lines under the command that started them.
- Keep lines under 100 characters; use `///` line continuation for long
  commands rather than one dense line.
- There is no `styler`/`lintr` equivalent in wide use for Stata — treat
  indentation and line-length as manual review items every time, not
  something tooling will catch (see section 11).

### 4. Data work idioms

Prefer built-in vectorized commands over row-by-row loops for data
transformation:

- `generate`/`replace ... if` for calculations and conditional
  transformations, instead of looping over observations.
- `egen` for group-level and row-level summaries (`egen`'s `by()`,
  `rowmean()`, `rowtotal()`, etc.) instead of a manual loop plus `merge`.
- `reshape long`/`reshape wide` for reshaping.
- `collapse` for one row per group.
- `recode varname (old = new)` for a small numeric recode, and
  `replace newvar = "..." if inlist(var, ...)` for a text-based recode
  into a new categorical variable — never a manual `if`/`else if` chain
  over each raw value.
- `tab var, generate(prefix)` to mass-create dummy variables from a
  categorical or string variable, rather than writing one
  `generate var_x = (var == "x")` line per category.
- For grouped summary statistics: `bysort group: summarize var` for a
  quick look, `tabstat var [aweight = weight_var], statistics(mean
  median) by(group)` for a weighted grouped mean/median, and
  `collapse (median) var, by(group)` when the grouped result itself needs
  to become a dataset (not just displayed).

**Merges.** State expected match behavior explicitly, the same way R states
`multiple`/`unmatched` in a join:

```stata
merge 1:1 entity_id using "data/intermediate/concordance.dta", ///
    assert(match) keep(match) nogenerate
```

- Always specify the match type (`1:1`, `1:m`, `m:1`, `m:m`) — never rely on
  Stata inferring it.
- Always check `_merge` (or use `assert()`/`nogenerate` as above) rather
  than leaving unmatched rows unexamined.
- Check keys with `duplicates report <keyvars>` before merging or
  collapsing.

### 5. Survey data management

Default to `svy:` estimation for any survey-weighted analysis — it is
Stata's built-in, tidy-equivalent path (no separate package needed, unlike
R's `srvyr`).

- Declare the survey design once, immediately after reading the cleaned
  data, with `svyset psu [pweight = weight_var], strata(strata_var)`. State
  the PSU, weight, and strata explicitly — never estimate on survey
  microdata without an explicit `svyset`.
- Never report an unweighted `summarize`/`mean`/`proportion` on survey
  microdata as if it were population-representative. If an unweighted
  figure is genuinely needed (raw sample size, a QA check), label it
  explicitly as unweighted in the variable/output name
  (`n_respondents_unweighted`), never with a name that reads as a
  population estimate.
- Use `svy: mean`, `svy: total`, `svy: ratio`, `svy: regress`, and similar
  `svy:`-prefixed commands; they report standard errors automatically —
  keep them in the output, do not discard with `, noheader` tricks that
  drop the SE.
- Use `svy: ..., subpop()` for subgroup estimates rather than `if`-filtering
  the dataset first and re-running `svyset` — filtering first can bias the
  variance estimate.
- Document the sampling design (PSU/strata/weight variable names and their
  source) in the script header's Purpose field or in a codebook under
  `documentation/codebooks/`.
- Keep direct identifiers (names, addresses, contact info, exact geocodes)
  out of `data/intermediate/` and `data/final/`. Strip or hash them in the
  raw-to-intermediate cleaning step and document the transformation.
- Treat don't-know, refused, and skip/not-applicable codes as distinct
  values during cleaning (e.g. `-98`, `-99`), not silently recoded to `.`
  Recode to Stata missing only at the point analysis requires it, and
  document the recode with a comment.
- Check unweighted and weighted respondent counts (`svy: tabulate` or
  `count`) against the expected sample size from the codebook as part of
  input checking. A missing wave or an unexpected count is a validation
  failure, not a silent proceed.

**Labels.** Inspect a labelled variable's value labels with `labelbook
varname` before recoding it — the same "know what the codes mean before
you touch them" rule as `R Code Conventions.md` section 6's Labels
subsection. Use `decode varname, generate(new_string_var)` to turn a
labelled numeric variable into a plain string variable when the label
text itself, not the underlying code, is what a later step needs (a
merge key against a source that stores names, a display column in an
export).

### 6. Loops and conditionals

Stata's `foreach`/`forvalues` play two different roles — keep them
distinct:

- **Data transformation**: do not use `foreach`/`forvalues` to loop over
  observations for row-by-row logic. Use `generate`/`replace ... if`,
  `egen`, or `recode` instead (see section 4).
- **Repeated file or model operations**: `foreach`/`forvalues` looping over
  a list of files, variables, or model specifications is the Stata
  equivalent of R's `map()`/`walk()` and is expected, not discouraged —
  Stata has no first-class function values to pass into a map-style call.

Use `if`/`else if`/`else` for scalar guards (checking a required file or
variable exists, stopping after a failed `assert`) the same way R allows
scalar `if` for guards; do not build deeply nested branching for what
`recode` or a lookup merge would express more clearly.

### 7. Functions and abstraction (`program define`)

Linear, repeated do-file code is the default. Write a `program define` only
when a block of code, varying only in 1-3 parameters, is repeated **6 or
more times** — the same repeat-count trigger as `R Code Conventions.md`
section 8, so a Stata program earns its abstraction on the same terms an R
helper does.

- Below the 6-repeat threshold, prefer a `foreach`/`forvalues` loop over the
  varying parameter (see section 6) rather than writing a `program define`
  for something used a handful of times.
- A justified program should represent one named domain operation, take
  clear arguments (`syntax varlist [, options]`), and return one predictable
  result (`return scalar`/`return local`).
- Define it at the top of the do-file that uses it, immediately after
  Setup, unless it recurs across more than one do-file — then move it to
  `code/functions/<verb>_<description>.do` and `do` it from Setup wherever
  it's needed.
- Never write generic configuration frameworks, class-like state machines
  via globals, or needless indirection. These are software-engineering
  patterns this codebase does not need, regardless of repeat count.

### 8. Modelling, tables, and figures

- Use `reghdfe` for fixed-effects and panel regressions; `regress` for
  simple cross-sectional OLS.
- Use `xtreg` only when `reghdfe` is unavailable or the fixed-effects
  structure is genuinely simple (single absorbed effect).
- Cluster standard errors at the unit of treatment assignment
  (`vce(cluster unit_id)`) and document that choice directly above the
  model call.
- Use `esttab` (from `estout`) for regression tables by default — it is
  more actively maintained and more flexible on output format
  (LaTeX/Word/CSV) than `outreg2`. `outreg2` is acceptable in an existing
  script that already uses it consistently; don't mix the two within one
  script or one project.
- Use `ivregress 2sls` for instrumental-variables regression (`ivreg` from
  the `ivreg2`/community-contributed family is acceptable where its extra
  diagnostics — weak-instrument and overidentification tests — are
  needed); state the excluded instrument(s) and the endogenous regressor
  directly above the call, the same way section 5 asks merges to state
  their match type.
- Use `graph twoway`/`graph bar` with a consistent, explicitly set scheme
  (`set scheme <name>` in Setup) rather than Stata's default scheme.
- `graph export` must specify both `.png` and `.pdf` outputs unless the
  task specifies another format, with explicit `width`/`height`.

### 9. Outputs and reproducibility

- Use `save ..., replace` for key intermediate and final datasets used by
  downstream do-files; treat a missing save for a downstream-referenced
  dataset as a critical reproducibility problem.
- Use `export excel`/`export delimited` for deliverables that leave Stata;
  keep `.dta` for anything staying inside the pipeline (preserves value
  labels and types that CSV loses).
- Keep a simple run record (log file, per section 1) with selected source
  filenames, selected year, method, and output location.
- A style-only rewrite (indentation, comments) must reproduce accepted
  numerical outputs exactly.
- An estimation change is complete only after actual values reconcile with
  a known total, benchmark, or accepted comparison.

### 10. Missing values and numerical discipline

- Stata's numeric missing (`.`, `.a`-`.z`) sorts as larger than any real
  number — always guard comparisons and selections involving missing with
  explicit `if !missing(var)`, never rely on the sort-to-infinity behavior
  intentionally.
- State how missing values are handled for every `egen` summary
  (`rowmean`/`rowtotal` skip missing by default — confirm that is the
  intended behavior in a comment, don't assume the reader knows).
- Check required period counts before annualizing monthly or quarterly
  data.
- Never compare floating-point values with `==`; use `reldif()` or an
  explicit tolerance.
- Check transformation links and domain constraints before extending a
  series.

### 11. Comments, errors, and console output

- Comments explain why a non-obvious rule exists; use `*` for full-line
  comments and `//` for end-of-line comments.
- Do not keep commented-out dead code, except a deterministic `set seed`
  marker.
- Use `display`/`di` sparingly — at most once per major stage to confirm
  progress, never inside a loop over observations.
- Error out early with `assert` and a clear message naming the failing
  file, variable, year, or series, rather than letting a script continue
  silently after a failed check.

### 12. Review standard

There is no `lintr`/`styler` equivalent in common use for Stata, so this
review is entirely manual — treat every category below as a human check,
not something a linter will flag automatically:

1. **Correctness** — transformations, merges, modelling, and outputs match
   the documented method; survey estimates use a correctly specified
   `svyset` and report standard errors, not unweighted figures mislabelled
   as population estimates (sections 4, 5, 8, 10).
2. **Reproducibility and path discipline** — no `cd`, no hardcoded machine
   paths, `save ..., replace` present for every downstream-referenced
   dataset, script naming matches `R Code Conventions.md` section 15's
   pattern generalized to `.do` (sections 3, 9).
3. **Input and result validation** — missing-value handling stated
   explicitly, period counts checked before annualizing, floating-point
   comparisons avoid `==` (section 10).
4. **Downstream artifacts and saved objects** — `.dta`, `.xlsx`, `.png`/
   `.pdf` outputs exist, are named descriptively, and match what the
   script's header documents as its Outputs (sections 1, 8, 9).
5. **Code structure and idioms** — merges use explicit match types and
   `assert`/`keep`, no row-by-row `foreach` over observations for data
   transformation, `program define` use follows the 6-repeat rule, not a
   subjective judgment call (sections 4, 6, 7).
6. **Style and polish** — indentation, line length, and naming (section 3)
   checked by hand; comment density follows the shared philosophy at the
   top of this file.

Formal findings include the file and line number, category, severity
(Critical, High, Medium, or Low), current code, proposed fix, and
rationale. Reviewers do not edit source files. Save formal reports to
`quality_reports/[script_name]_stata_review.md`.

### 13. Known pitfalls

- `merge` silently producing unexpected many-to-many matches when the
  declared match type doesn't hold — always check `_merge` or `assert()`.
- `destring`/`encode` type mismatches between datasets built at different
  times with different string formats for the same key.
- Stata's missing-value sort-to-infinity trap in `if`/`sort` logic that
  doesn't explicitly exclude `.`

### Interop with Python (`pystata`)

Use `pystata` (bundled with Stata 17+) when a script genuinely needs to
call Stata from a Python/Jupyter session — e.g. driving Stata estimation
from a Python-orchestrated pipeline, or working in a notebook that mixes
Python data handling with Stata-only commands/packages. Configure it once
at the top of the Python script, then run Stata commands as strings:

```python
import stata_setup

stata_setup.config(r"C:\Program Files\Stata18", "mp")

from pystata import stata

stata.run("sysuse auto, clear")
stata.run("""
sum
reg mpg weight
""")
```

- `stata_setup.config()` takes the Stata installation path and edition
  (`"mp"`, `"se"`, `"be"`) — never hardcode a specific user's install path
  in a committed script; read it from an environment variable or a
  project config value instead, per the path rules in the Python section
  above.
- In a Jupyter notebook, the `stata_setup`/`pystata` import is still
  required once at the top, after which the `%stata`/`%%stata` IPython
  magics run Stata commands directly in a cell without wrapping them in
  `stata.run()`.
- This is an interop tool for mixed-language notebooks and pipelines, not
  a reason to write new analysis logic in Stata-via-Python instead of
  plain Stata (do-files) or plain Python (per this file's Python section)
  — use it only when the task genuinely needs both in the same process.

---

## Python

### 1. Script structure

Every active standalone script begins with this header:

```python
# ============================================================
# Descriptive title
# Author: Daniel Sanchez
# Purpose: What this script does
# Inputs:  Files or objects read
# Outputs: Files or objects written
# ============================================================
```

Followed by numbered sections using cell markers, adapted to the task but
never omitting setup:

```python
# %% 0. Setup
# %% 1. Read inputs
# %% 2. Check inputs
# %% 3. Prepare data
# %% 4. Calculate estimates
# %% 5. Check results
# %% 6. Write outputs
```

- Set a fixed random seed (`random.seed(42)`, `np.random.seed(42)`) at the
  top when the script is stochastic; omit it for deterministic scripts.
- Keep all `import` statements, configuration constants, and paths at the
  top, under Setup — never import mid-script.
- Guard the entry point of a standalone script with
  `if __name__ == "__main__":` only when the script is also meant to be
  imported elsewhere; a script that only ever runs top-to-bottom as part of
  the pipeline does not need it.

### 2. Environment and packages

- Use a project-local virtual environment (`venv`, `uv`, or `conda`) pinned
  by a `pyproject.toml`/`requirements.txt` committed to the repo; never
  install packages inside a production script (`subprocess`-calling `pip
  install`, or an in-script `!pip install` left over from a notebook).
- Import every package at the top of the script, once. Do not conditionally
  import inside a function unless resolving a genuine circular-import
  problem, and comment why.
- Prefer the standard library and `pathlib.Path` over `os.path` for path
  handling.

### 3. Naming, paths, and formatting

- Use `snake_case` for files, functions, and variables; `PascalCase` only
  for classes (and classes should be rare — see section 6).
- Use nouns for data objects, verbs for functions.
- Build paths with `pathlib.Path`, relative to a project-root constant
  defined once in Setup — never hardcode a drive letter, username, or
  absolute machine path.
- Never call `os.chdir()`.
- **Formatting and linting — enforced by `ruff`.** Run `ruff format .` and
  `ruff check .` (or `ruff check --fix .`) before a script is considered
  complete; resolve every flagged issue rather than hand-formatting around
  what `ruff` would produce. Pin the project's `ruff` config in
  `pyproject.toml` so formatting is consistent across scripts.
- Line length 88 characters (ruff's default, matching `black`), enforced by
  the same `ruff format` run above.
- Add type hints on function signatures; run `mypy` (or `ruff`'s
  type-aware rules where enabled) as part of the same pre-completion pass.

### 4. Data work idioms

Default to `polars`, not `pandas`, for new code. It is faster on typical
research-data sizes, has a stricter and more predictable type system
(no silent `int` → `float` upcasting on a missing value the way `pandas`
does), and its expression API (`pl.col(...)`) reads as one declarative
statement per operation, closer to the readability goal in the shared
philosophy at the top of this file than `pandas`' mix of bracket indexing
and method chaining.

- `.filter(pl.col(...))` for scope, geography, and period selection.
- `.with_columns(pl.col(...).alias(...))` for calculations and derived
  columns.
- `.group_by(...).agg(...)` for one row per group.
- `.unpivot()`/`.pivot()` for reshaping.
- `.join()` for joins, with `validate=` (`"1:1"`, `"1:m"`, `"m:1"`,
  `"m:m"`) stated explicitly, the same way R states `multiple`/`unmatched`:

```python
import polars as pl

estimates = values.join(
    concordance,
    on="entity_id",
    how="left",
    validate="1:1",
)
```

- Prefer `pl.scan_csv()`/`pl.scan_parquet()` (lazy) over `pl.read_*()`
  (eager) for anything beyond a quick, small script — the lazy API lets
  Polars push filters/column selection down to the scan and only
  `.collect()` at the point a materialized `DataFrame` is actually needed.
- Never use a Python-level `for` loop over rows for something a `polars`
  expression can express directly; there is no `.iterrows()` equivalent to
  reach for by habit the way there is in `pandas`.
- Use method-chaining with parentheses for multi-step transformations, one
  operation per line, the same visual style as an R pipe chain.

**When `pandas` is still the right call.** Use `pandas` only when a
specific downstream library genuinely requires it (some older
`scikit-learn`/`statsmodels`/plotting-library entry points still expect a
`pandas.DataFrame`, not a `polars.DataFrame`) — convert at the boundary
with `.to_pandas()` right before the call that needs it, and say so in a
comment, rather than writing the whole script in `pandas` because one
downstream call needs it.

### 5. Survey data management

There is no single dominant Python survey-analysis package the way R has
`srvyr`; default to explicit weighted computation directly in `polars`
(`pl.col("value").mul(pl.col("weight")).sum() / pl.col("weight").sum()`
inside a `.with_columns()`/`.group_by().agg()` expression), or
`statsmodels`' `DescrStatsW` (via `.to_pandas()`/`.to_numpy()` at the
boundary, per section 4) when the standard-error formula matters and
hand-rolling it would be error-prone. Only reach for a heavier survey
package (`samplics`) when the project genuinely needs complex-design
variance estimation (replicate weights, multi-stage clustering) that
neither of those gets right on its own.

- Declare the weight, strata, and cluster columns once, right after reading
  the cleaned data, as named variables/constants — never inline a weight
  column name string at each call site.
- Never compute an unweighted `.mean()`, `.sum()`, `.std()`, or proportion
  on survey microdata as if it were population-representative. If an
  unweighted figure is genuinely needed (raw sample size, a QA check), name
  it as unweighted (`n_respondents_unweighted`), never with a name that
  reads as a population estimate.
- When using `DescrStatsW` or equivalent, keep the standard error alongside
  the point estimate in the output — do not discard it.
- Document the sampling design (strata/cluster/weight column names and
  their source) in the script header's Purpose field or in a codebook
  under `documentation/codebooks/`.
- Keep direct identifiers (names, addresses, contact info, exact geocodes)
  out of `data/intermediate/` and `data/final/`. Strip or hash them in the
  raw-to-intermediate cleaning step and document the transformation.
- Treat don't-know, refused, and skip/not-applicable codes as distinct
  categorical values during cleaning, not silently coerced to `null`.
  Recode to `null` only at the point analysis requires it, and document
  the recode.
- Check unweighted and weighted respondent counts against the expected
  sample size from the codebook as part of input checking. A missing wave
  or an unexpected count is a validation failure, not a silent proceed.

### 6. Loops and conditionals

Do not use an explicit `for` loop over DataFrame rows, or nested row-by-row
`if`/`else`, for data transformation. Use vectorized operations, `np.select()`
for several conditions, `np.where()` for a two-way choice, `.map()`/
`.replace()` with a lookup dict for value mapping, or a merge/join for
lookup-table mappings.

A plain `for` loop is acceptable for repeated file or model operations (a
list comprehension or explicit loop over a list of files/specifications) —
the same allowance R gives `map()`/`walk()`. It is not acceptable as a
substitute for vectorized data-column logic.

Scalar `if` guards (checking a required file or column exists, stopping
after a failed validation with `assert` or `raise`) are fine; stop early
rather than nesting deeply.

### 7. Functions and abstraction

Linear code is the default; most repeated research code should stay inline
as plain duplication, not become a function. Write a function only when a
block of code, varying only in 1-3 parameters, is repeated **6 or more
times** — the same repeat-count trigger as `R Code Conventions.md` section
8.

- A justified function should represent one named domain or file-reading
  operation, have type-annotated inputs, and one predictable return type.
- Define it at the top of the script that uses it, in Setup, immediately
  after imports, unless it recurs across more than one script — then move
  it to `code/functions/<verb>_<description>.py` and import it from Setup
  wherever it's needed.
- Never write generic configuration frameworks, factories, builders, or a
  class hierarchy for something a function and a dict would express
  directly. Classes are justified only when the code genuinely needs
  encapsulated mutable state across multiple calls (e.g. a stateful
  simulation), not as a default organizing structure for research code.
- Keep side effects (file writes, plot saves) at the top level or inside a
  small function whose only job is the write — not buried inside a
  transformation function that also returns a value.

### 8. Modelling and figures

- Use `statsmodels` for classical regression (`OLS`, `Logit`, weighted
  least squares) and `linearmodels` (`PanelOLS`) for fixed-effects panel
  models.
- Cluster standard errors at the unit of treatment assignment
  (`cov_type="clustered"`, `cov_kwds={"groups": ...}`) and document that
  choice directly above the model call.
- Use `matplotlib`/`seaborn` for figures, with a consistent non-default
  style set once in Setup (`plt.style.use(...)` or a shared `seaborn`
  theme), not per-figure ad hoc styling.
- Use sentence-case axis labels with units where applicable; put legends
  outside the plotted area or at the bottom.
- `plt.savefig()` must specify `dpi` and `bbox_inches="tight"` explicitly.
- Deliverable figures should be saved as both `.png` and `.pdf` unless the
  task specifies another format.

### 9. Outputs and reproducibility

- Use `parquet` (`pl.write_parquet()`/`pl.read_parquet()`, native to
  `polars`, no `pandas`/`pyarrow` round-trip needed) for intermediate and
  final processed data used by downstream scripts — not `pickle`, which is
  fragile across Python/library versions and not human-inspectable.
- Treat a missing save for a downstream-referenced object as a critical
  reproducibility problem.
- Use `.csv` only for small, final deliverables meant to leave the
  pipeline (e.g. a table for a report), not for intermediate data.
- Keep a simple run record with selected source filenames, selected year,
  method, and output location.
- A style-only rewrite (formatting, comments) must reproduce accepted
  numerical outputs exactly.
- An estimation change is complete only after actual values reconcile with
  a known total, benchmark, or accepted comparison.

### 10. Missing values and numerical discipline

- `polars` distinguishes `null` (missing) from floating-point `NaN` (a
  valid-but-undefined number) — these are not interchangeable the way
  `pandas` treats them. State which one a column can contain and handle
  each explicitly (`.is_null()` vs `.is_nan()`), rather than assuming a
  single `.is_null()` check covers both.
- State how missing values are handled for every `.mean()`, `.sum()`,
  `.std()` call — `polars` skips `null` by default in these; confirm that
  is the intended behavior in a comment rather than assuming it's
  understood.
- Never silently `.fill_null(0)` to make a calculation run; use it only
  when the documented method says missing observations are treated as
  zero.
- Check required period counts before annualizing monthly or quarterly
  data.
- Check that required numerical values are finite (`np.isfinite`).
- Never compare floats with `==`; use `np.isclose()` or `math.isclose()`
  with an explicit tolerance.
- Check transformation links and domain constraints before extending a
  series.

### 11. Comments, errors, and console output

- Comments explain why a non-obvious rule exists; do not restate obvious
  code.
- Do not keep commented-out dead code, except a deterministic
  `# random.seed(42)` marker.
- Use the `logging` module, not `print()`, for status output — at most one
  `logging.info()` per major stage.
- Do not print progress for every file, row, or iteration.
- Raise errors (`raise ValueError(...)`, `assert ..., "message"`) that name
  the failing file, field, year, or series, rather than letting a script
  continue silently after a failed check.

### 12. Review standard

1. **Correctness** — transformations, merges, modelling, and outputs match
   the documented method; survey estimates use correctly declared weights
   and report standard errors, not unweighted figures mislabelled as
   population estimates (sections 4, 5, 8, 10).
2. **Reproducibility and path discipline** — no `os.chdir()`, no hardcoded
   machine paths, every downstream-referenced object saved, script naming
   matches `R Code Conventions.md` section 15's pattern generalized to
   `.py` (sections 3, 9).
3. **Input and result validation** — missing-value handling stated
   explicitly, finiteness checked, period counts checked before
   annualizing, floating-point comparisons avoid `==` (section 10). No
   `ruff` rule detects an unstated missing-value assumption; this stays a
   manual check.
4. **Downstream artifacts and saved objects** — `.parquet`, `.csv`, `.png`/
   `.pdf` outputs exist, are named descriptively, and match what the
   script's header documents as its Outputs (sections 8, 9).
5. **Code structure and idioms** — `polars` expressions used instead of a
   Python-level row loop, `pandas` used only at a documented interop
   boundary (never as the default), joins use explicit `validate=`,
   function use follows the 6-repeat rule, not a subjective judgment call
   (sections 4, 6, 7).
6. **Style and polish** — run `ruff format --check .` and `ruff check .`
   and treat every result as a formal finding at the severity `ruff`
   assigns; run `mypy` and resolve every reported type error. Comment
   density and naming length remain manual checks — no linter enforces
   these.

**Automation gaps.** `ruff` catches most formatting, unused-import, and
common-bug issues, but it does not catch every row-by-row `.apply()` pattern
(only the obvious `.iterrows()` case is easy to grep for) or a missing
`na`-handling justification. Both stay manual checks regardless of a clean
`ruff`/`mypy` run.

Formal findings include the file and line number, category, severity
(Critical, High, Medium, or Low), current code, proposed fix, and
rationale. Reviewers do not edit source files. Save formal reports to
`quality_reports/[script_name]_python_review.md`.

### 13. Known pitfalls

- Confusing `null` and `NaN` in `polars` — a `.is_null()` check silently
  passes a column full of `NaN`, and vice versa; check the one that
  actually applies to the column's source data.
- Mutable default arguments (`def f(x, acc=[]):`) silently sharing state
  across calls.
- `.join()` producing a silent row-count change without `validate=` to
  catch an unexpected many-to-many match.
- `SettingWithCopyWarning` from chained indexing (`df[df.x > 0]["y"] = 1`)
  is a `pandas`-only pitfall — still relevant at a `pandas` interop
  boundary (section 4); use `.loc[]` for any assignment into a filtered
  `pandas` subset there.

---

## Julia

### 1. Script structure

Every active standalone script begins with this header:

```julia
# ============================================================
# Descriptive title
# Author: Daniel Sanchez
# Purpose: What this script does
# Inputs:  Files or objects read
# Outputs: Files or objects written
# ============================================================
```

Followed by numbered sections, adapted to the task but never omitting
setup:

```julia
# 0. Setup
# 1. Read inputs
# 2. Check inputs
# 3. Prepare data
# 4. Calculate estimates
# 5. Check results
# 6. Write outputs
```

- Set a fixed random seed (`Random.seed!(42)`) at the top when the script
  is stochastic; omit it for deterministic scripts.
- Keep `using`/`import` statements, configuration constants, and paths at
  the top, under Setup.
- Avoid untyped global variables holding data used in later sections —
  Julia's performance and correctness both suffer from non-constant
  globals; wrap script-level work in a `function main()` (or pass data
  explicitly between sections) when the script is more than a quick,
  one-off transformation.

### 2. Environment and packages

- Use a project-local environment (`Project.toml`/`Manifest.toml`) pinned
  and committed to the repo. Activate it explicitly at the top of every
  script with `Pkg.activate("<env_name>")` (or `Pkg.activate(".")` for a
  root-level environment) — do this in the script itself, in Setup, rather
  than relying on the caller to remember `--project=.` on the command
  line; that keeps a script runnable on its own from a fresh Julia
  session.
- Never call `Pkg.add()` inside a production script. Keep the one-time
  `Pkg.generate("<env_name>")`/`Pkg.add(...)` calls that build the
  environment in a separate, clearly-named setup script
  (`code/setup/0_setup.jl` or similar), run once, not on every pipeline
  run.
- Load every package with `using` at the top of the script, once, right
  after `Pkg.activate()`.
- Instantiate the environment (`Pkg.instantiate()`) as a one-time setup
  step, not inside the analysis script itself.
- **Name collision to watch for**: `TidierData.jl` and `Flux.jl` both
  export `Chain` — loading both means an unqualified `Chain` is
  ambiguous. If a script needs both, call it as `Flux.Chain` explicitly
  rather than relying on load order, and note the collision in a comment
  at the `using` statements so the next reader isn't surprised by it.

### 3. Naming, paths, and formatting

- Use `snake_case` for files, functions, and variables (Julia's own
  ecosystem often uses this already, unlike some other languages).
- Use nouns for data objects, verbs for functions.
- Build paths with `joinpath()`, relative to a project-root constant
  defined once in Setup — never hardcode a drive letter, username, or
  absolute machine path.
- **Formatting — enforced by `JuliaFormatter.jl`.** Run
  `JuliaFormatter.format(".")` (or `julia -e 'using JuliaFormatter;
  format(".")'`) before a script is considered complete, using the
  project's pinned `.JuliaFormatter.toml` style config; resolve everything
  it changes rather than hand-formatting around it.
- There is no `lintr` equivalent in common use for Julia beyond
  `JuliaFormatter`; correctness-level issues (type instability, unused
  bindings) stay a manual review item (see section 12).

### 4. Data work idioms

Default to `TidierData.jl` (from the [TidierOrg](https://github.com/TidierOrg)
ecosystem) for data cleaning and transformation, and `TidierFiles.jl` from
the same ecosystem for I/O (`read_csv()`/`write_csv()` and similar). Both
reimplement their dplyr/tidyr/readr equivalents verb-for-verb, so a script
reads almost identically to its R equivalent under `R Code Conventions.md`
section 5 — this is deliberate: prefer tidy, readable data management the
same way in both languages, not a `DataFrames.jl`-native style that reads
differently script to script.

- `@clean_names()` immediately after reading a raw file, before anything
  else — standardizes column names to `snake_case` the same way this
  file's naming rules require, rather than carrying inconsistent raw
  column names (`"Filing Date"`, `subjId`, `LOCATION`) into the rest of
  the script.
- `@glimpse()` right after `@clean_names()` when inspecting a newly read
  dataset, as the equivalent of R's `str()`/`glimpse()` — this is
  inspection, like `haven::print_labels()` in
  `R Code Conventions.md` section 6, not a transformation, so keep it
  outside a `@chain` pipeline that produces the working dataset.
- `@filter()` for scope, geography, and period selection.
- `@mutate()` for calculations and derived columns.
- `@summarize()` for one row per group.
- `@group_by()` (paired with `@ungroup()`, or scoped inline) for grouped
  operations, mirroring R's `.by`/`group_by()` choice.
- `@pivot_longer()`/`@pivot_wider()` for reshaping.
- `@left_join()`/`@inner_join()` etc. for joins, mirroring `join_by()`
  semantics — state the join key explicitly and check row counts
  before/after rather than assuming a clean match:

```julia
estimates = @chain values begin
    @left_join(concordance, entity_id)
end
```

- Drop to base `DataFrames.jl` (`leftjoin()` with `validate=`,
  `combine()`/`groupby()`) only when `TidierData.jl` has no equivalent for
  what the transformation needs — e.g. a validated join that must assert
  cardinality, since `TidierData.jl`'s join macros do not yet expose a
  `validate=` argument the way `DataFrames.jl`'s `leftjoin()` does. Say so
  in a comment above the call.
- Check keys (`nonunique()`/`allunique()`, or row counts before/after a
  join) before joining or aggregating, regardless of which interface is
  used.

### 5. Survey data management

Julia's survey-analysis ecosystem is thin compared to R's `srvyr`; default
to explicit weighted computation using `StatsBase.jl`'s `Weights` type
(`mean(x, weights(w))`, `std(x, weights(w))`) for simple designs, and only
reach for a dedicated survey package when the project's design genuinely
needs complex multi-stage variance estimation that hand-rolled weighting
can't provide correctly — document that reasoning in a comment if so.

- Declare the weight, strata, and cluster columns once, right after
  reading the cleaned data, as named constants — never inline a column
  name string at each call site.
- Never compute an unweighted `mean()`, `sum()`, `std()`, or proportion on
  survey microdata as if it were population-representative. If an
  unweighted figure is genuinely needed (raw sample size, a QA check),
  name it as unweighted (`n_respondents_unweighted`), never with a name
  that reads as a population estimate.
- Keep the standard error alongside any weighted point estimate in the
  output — do not discard it.
- Document the sampling design (strata/cluster/weight column names and
  their source) in the script header's Purpose field or in a codebook
  under `documentation/codebooks/`.
- Keep direct identifiers (names, addresses, contact info, exact geocodes)
  out of `data/intermediate/` and `data/final/`. Strip or hash them in the
  raw-to-intermediate cleaning step and document the transformation.
- Treat don't-know, refused, and skip/not-applicable codes as distinct
  categorical values during cleaning, not silently coerced to `missing`.
  Recode to `missing` only at the point analysis requires it, and document
  the recode.
- Check unweighted and weighted respondent counts against the expected
  sample size from the codebook as part of input checking. A missing wave
  or an unexpected count is a validation failure, not a silent proceed.

### 6. Loops and conditionals

Unlike R and Python, explicit `for` loops in Julia are fast and idiomatic —
this is a genuine language difference, not an oversight. The rule here is
about readability, not performance avoidance:

- Prefer broadcasting (`.`-vectorized calls) or `DataFrames.jl` verbs (see
  section 4) for column-level data transformations, because they read as
  one operation rather than an explicit accumulation loop.
- An explicit `for` loop is fully acceptable, and often preferred, for
  performance-critical numerical code (simulation, iterative estimation,
  anything operating element-by-element on large arrays) — do not force
  such code into an awkward vectorized form just to avoid a loop.
- Use `if`/`elseif`/`else` for scalar guards the same way other languages
  do; prefer `ifelse()` or a `Dict`-based lookup over nested branching for
  row-level categorical recoding.

### 7. Functions and abstraction

Functions are cheap and idiomatic in Julia (multiple dispatch rewards
having many small, typed methods), but the same discipline applies as in R:
most repeated research code should stay inline as plain duplication until
it clears the bar. Write a function only when a block of code, varying only
in 1-3 parameters, is repeated **6 or more times** — the same repeat-count
trigger as `R Code Conventions.md` section 8.

- A justified function should represent one named domain or file-reading
  operation, have type-annotated arguments where it clarifies intent
  (`function run_model(dv::Symbol, data::DataFrame)`), and one predictable
  return type.
- Define it at the top of the script that uses it, in Setup, unless it
  recurs across more than one script — then move it to
  `code/functions/<verb>_<description>.jl` and `include()` it from Setup
  wherever it's needed.
- Never write generic configuration frameworks, factories, or a struct
  hierarchy for something a function and a `NamedTuple` would express
  directly.

### 8. Modelling and figures

- Use `GLM.jl` for classical regression and `FixedEffectModels.jl` for
  fixed-effects panel models.
- Use `RegressionTables.jl` for regression tables.
- Cluster standard errors at the unit of treatment assignment and document
  that choice directly above the model call.
- Default to `TidierPlots.jl` (also from
  [TidierOrg](https://github.com/TidierOrg)) for figures, not `Plots.jl` or
  `Makie.jl`. It is a ggplot2-equivalent grammar-of-graphics interface
  (`ggplot()`, `geom_col()`, `geom_boxplot()`, `@aes()`, `labs()`,
  `scale_colour_manual()`), so a Julia figure reads like its R equivalent
  under `R Code Conventions.md` section 10 — the same "reads like R"
  principle already applied to data work in section 4:

```julia
ggplot(summary_df) +
    geom_col(@aes(x = category, y = value, colour = group), position = "dodge") +
    labs(x = "Category", y = "Value") +
    scale_colour_manual(values = ["#F8766D", "#00BFC4"])
```

- Drop to base `Plots.jl`/`Makie.jl` only when `TidierPlots.jl` genuinely
  has no equivalent for a needed geometry or interactivity feature, and
  say so in a comment above the call — don't mix `TidierPlots.jl` and
  `Plots.jl`/`Makie.jl` within one project otherwise.
- Use sentence-case axis labels with units where applicable; put legends
  at the bottom.
- Saving a figure must specify explicit size.
- Deliverable figures should be saved as both `.png` and `.pdf` unless the
  task specifies another format.

### 9. Outputs and reproducibility

- Use `Arrow.jl` or `Parquet2.jl` for intermediate and final processed
  data used by downstream scripts, or `JLD2.jl` when saving arbitrary
  Julia objects (models, fitted results) rather than tabular data.
- Treat a missing save for a downstream-referenced object as a critical
  reproducibility problem.
- Use `TidierFiles.jl`'s `write_csv()` (a thin wrapper on `CSV.jl`, kept
  for the same syntax consistency as section 4) only for small, final
  deliverables meant to leave the pipeline, not for intermediate data.
- Keep a simple run record with selected source filenames, selected year,
  method, and output location.
- A style-only rewrite (formatting, comments) must reproduce accepted
  numerical outputs exactly.
- An estimation change is complete only after actual values reconcile with
  a known total, benchmark, or accepted comparison.

### 10. Missing values and numerical discipline

- State how `missing` propagation is handled for every `mean()`, `sum()`,
  `std()` call — use `skipmissing()` explicitly rather than letting
  `missing` silently propagate through a calculation and produce a
  `missing` result downstream.
- Check required period counts before annualizing monthly or quarterly
  data.
- Check that required numerical values are finite (`isfinite`).
- Never compare floats with `==`; use `isapprox()` with an explicit
  tolerance.
- Check transformation links and domain constraints before extending a
  series.

### 11. Comments, errors, and console output

- Comments explain why a non-obvious rule exists; do not restate obvious
  code.
- Do not keep commented-out dead code, except a deterministic
  `# Random.seed!(42)` marker.
- Use `@info` for status output, not `println()` — at most once per major
  stage.
- Do not print progress for every file, row, or iteration.
- Raise errors (`error(...)`, `@assert ... "message"`) that name the
  failing file, field, year, or series, rather than letting a script
  continue silently after a failed check.

### 12. Review standard

1. **Correctness** — transformations, joins, modelling, and outputs match
   the documented method; survey estimates use correctly declared weights
   and report standard errors, not unweighted figures mislabelled as
   population estimates (sections 4, 5, 8, 10).
2. **Reproducibility and path discipline** — no hardcoded machine paths,
   every downstream-referenced object saved, script naming matches
   `R Code Conventions.md` section 15's pattern generalized to `.jl`
   (sections 3, 9).
3. **Input and result validation** — `missing` handling stated explicitly
   via `skipmissing()`, finiteness checked, period counts checked before
   annualizing, floating-point comparisons avoid `==` (section 10).
4. **Downstream artifacts and saved objects** — saved data/model objects
   and `.png`/`.pdf` outputs exist, are named descriptively, and match
   what the script's header documents as its Outputs (sections 8, 9).
5. **Code structure and idioms** — `TidierData.jl` verbs used for
   column-level transforms (base `DataFrames.jl` only where documented as
   necessary), joins state their key and are row-count checked, function
   use follows the 6-repeat rule, not a subjective judgment call —
   remembering that an explicit `for` loop over performance-critical
   numerical code is correct Julia, not a violation (sections 4, 6, 7).
6. **Style and polish** — run `JuliaFormatter.format(".")` and treat any
   file it changes as evidence the submitted version wasn't
   formatter-clean. Comment density and naming length remain manual
   checks — no linter enforces these.

**Automation gaps.** `JuliaFormatter.jl` only checks formatting, not type
instability, unused bindings, or the missing-value and loop-use judgment
calls above — those stay manual checks regardless of a clean formatter run.

Formal findings include the file and line number, category, severity
(Critical, High, Medium, or Low), current code, proposed fix, and
rationale. Reviewers do not edit source files. Save formal reports to
`quality_reports/[script_name]_julia_review.md`.

### 13. Known pitfalls

- Type instability from untyped globals or functions whose return type
  depends on a runtime branch — check with `@code_warntype` on
  performance-sensitive functions.
- Off-by-one/indexing mistakes when porting logic from a 0-indexed
  language (Python) — Julia arrays are 1-indexed.
- `missing` silently propagating through an entire calculation chain
  without `skipmissing()`, producing a `missing` final result instead of
  an error.
