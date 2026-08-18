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

# Load packages before running the production script
# Install dependencies separately from the production run.
library(purrr)

# Run this script from the project root.
# All paths are relative to the project root.

# Derived paths
path_raw    <- file.path("data", "raw")
path_inter  <- file.path("data", "intermediate")
path_final  <- file.path("data", "final")
path_graphs <- file.path("outputs", "graphs")
path_tables <- file.path("outputs", "tables")
path_docs   <- file.path("documentation")

# --------------------------------------------------------------------------
# Run scripts in order
# --------------------------------------------------------------------------

# Cleaning
source(file.path("code", "cleaning", "01_clean_hh.R"))
source(file.path("code", "cleaning", "02_clean_survey.R"))
source(file.path("code", "cleaning", "03_merge_final.R"))

# Analysis
source(file.path("code", "analysis", "01_descriptives.R"))
source(file.path("code", "analysis", "02_regressions.R"))
source(file.path("code", "analysis", "03_figures.R"))

# ==============================================================================
# End of master
# ==============================================================================
sessionInfo()
```

> Note: Run the master script from the project root and use `file.path()` for
> relative paths. Never use `setwd()` in scripts because it breaks portability.

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
