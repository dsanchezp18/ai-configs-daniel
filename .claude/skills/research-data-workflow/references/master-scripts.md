# Master Script Templates

The master script is the single entry point for the entire project. Running it from top to bottom
must reproduce all outputs from raw data. It sets global paths and calls sub-scripts in order.

---

## Stata — MASTER.do

```stata
* ==============================================================================
* MASTER DO-FILE
* Project: [Project Name]
* Last updated: [YYYY-MM-DD]
* ==============================================================================

* Clear environment
clear all
set more off
set maxvar 10000

* --------------------------------------------------------------------------
* Root path — only line to change per machine
* --------------------------------------------------------------------------
global root "C:/Users/yourname/project-root"

* Derived paths (do not edit)
global data       "$root/data"
global raw        "$data/raw"
global inter      "$data/intermediate"
global final      "$data/final"
global code       "$root/code"
global outputs    "$root/outputs"
global graphs     "$outputs/graphs"
global tables     "$outputs/tables"
global docs       "$root/documentation"

* --------------------------------------------------------------------------
* Run scripts in order
* --------------------------------------------------------------------------

* Cleaning
do "$code/cleaning/01_clean_hh.do"
do "$code/cleaning/02_clean_survey.do"
do "$code/cleaning/03_merge_final.do"

* Analysis
do "$code/analysis/01_descriptives.do"
do "$code/analysis/02_regressions.do"
do "$code/analysis/03_figures.do"

* ==============================================================================
* End of master
* ==============================================================================
```

---

## R — MASTER.R

```r
# ==============================================================================
# MASTER SCRIPT
# Project: [Project Name]
# Last updated: [YYYY-MM-DD]
# ==============================================================================

# Install/load package manager
if (!require("here")) install.packages("here")
library(here)

# Root is set automatically by here::here() based on .Rproj or .here file
# All paths are relative to project root

# Derived paths
path_raw    <- here("data", "raw")
path_inter  <- here("data", "intermediate")
path_final  <- here("data", "final")
path_graphs <- here("outputs", "graphs")
path_tables <- here("outputs", "tables")
path_docs   <- here("documentation")

# --------------------------------------------------------------------------
# Run scripts in order
# --------------------------------------------------------------------------

# Cleaning
source(here("code", "cleaning", "01_clean_hh.R"))
source(here("code", "cleaning", "02_clean_survey.R"))
source(here("code", "cleaning", "03_merge_final.R"))

# Analysis
source(here("code", "analysis", "01_descriptives.R"))
source(here("code", "analysis", "02_regressions.R"))
source(here("code", "analysis", "03_figures.R"))

# ==============================================================================
# End of master
# ==============================================================================
```

> Note: Always use `here::here()` for paths in R. Never use `setwd()` in scripts — it breaks
> portability across machines.

---

## Python — main.py

```python
# ==============================================================================
# MASTER SCRIPT
# Project: [Project Name]
# Last updated: [YYYY-MM-DD]
# ==============================================================================

import subprocess
import sys
from pathlib import Path

# Root = directory containing this file
ROOT = Path(__file__).parent.resolve()

# Derived paths
DATA    = ROOT / "data"
RAW     = DATA / "raw"
INTER   = DATA / "intermediate"
FINAL   = DATA / "final"
OUTPUTS = ROOT / "outputs"
GRAPHS  = OUTPUTS / "graphs"
TABLES  = OUTPUTS / "tables"
DOCS    = ROOT / "documentation"

# --------------------------------------------------------------------------
# Run scripts in order
# --------------------------------------------------------------------------

scripts = [
    # Cleaning
    ROOT / "code" / "cleaning" / "01_clean_hh.py",
    ROOT / "code" / "cleaning" / "02_clean_survey.py",
    ROOT / "code" / "cleaning" / "03_merge_final.py",
    # Analysis
    ROOT / "code" / "analysis" / "01_descriptives.py",
    ROOT / "code" / "analysis" / "02_regressions.py",
    ROOT / "code" / "analysis" / "03_figures.py",
]

for script in scripts:
    print(f"Running {script.name}...")
    result = subprocess.run([sys.executable, str(script)], check=True)

print("All scripts completed successfully.")

# ==============================================================================
# End of master
# ==============================================================================
```

> Note: Pass `ROOT` or derived paths as environment variables or a config object into sub-scripts
> rather than redefining paths in each script. Consider a `config.py` for shared constants.
