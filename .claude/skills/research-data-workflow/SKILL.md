---
name: research-data-workflow
description: >
  Organizes research project folders following DIME Analytics data work philosophy for replicable,
  reproducible research. Use this skill whenever a user mentions setting up a research project,
  organizing data or code files, structuring a DataWork folder, audit of project file structure,
  file naming conventions for research, or reproducible/replicable research workflows. Also trigger
  for requests like "set up my project folder", "how should I organize my data files", "check my
  project structure", or any time a user is starting or cleaning up an empirical research project
  in any language (Stata, R, Python, Julia, or other). Do NOT skip this skill just because the
  user hasn't said "DIME" — the philosophy applies broadly.
---

# Research Data Workflow Skill

Helps Claude Code set up, audit, and advise on research project folder structures following
DIME Analytics principles for reproducible empirical work. Language-agnostic.

---

## Core DIME Philosophy (always apply)

1. **All analytical steps must be in code.** No point-and-click, no console-only steps for
   anything in a research output. Every number in a paper must be traceable to a script.

2. **The project root IS the DataWork folder.** No nesting DataWork inside another folder.
   Project management materials (contracts, briefs, admin) live separately (e.g., Dropbox),
   while code lives in version control (Git). Never put a Git repo inside a synced Dropbox folder.

3. **Separation of raw, intermediate, and final data.** Raw data is never modified. Code
   transforms it through clearly named stages.

4. **Parallel code/data structure.** The folder structure for code mirrors the folder structure
   for data. A script that cleans survey round 1 lives in a code folder that mirrors the data
   folder for survey round 1.

5. **README stubs in every folder.** Every folder gets a README.md documenting its contents,
   naming conventions used, and any dependencies.

6. **Agree on file formats upfront.** Teams must decide early: LaTeX vs. Word, .png vs. .pdf
   for figures, etc. Mismatches break workflows.

---

## Standard Folder Structure

```
project-root/
├── README.md                  # Project overview, how to run, dependencies
├── MASTER.do / MASTER.R / main.py   # Single entry point that runs everything
│
├── data/
│   ├── README.md
│   ├── raw/                   # Never modified. Read-only after receipt.
│   │   └── README.md
│   ├── intermediate/          # Intermediate cleaning outputs
│   │   └── README.md
│   └── final/                 # Analysis-ready datasets
│       └── README.md
│
├── code/
│   ├── README.md
│   ├── cleaning/              # Scripts that move raw -> intermediate -> final
│   │   └── README.md
│   └── analysis/              # Scripts that use final data to produce outputs
│       └── README.md
│
├── outputs/
│   ├── README.md
│   ├── graphs/
│   │   └── README.md
│   ├── tables/
│   │   └── README.md
│   └── maps/                  # Include if spatial analysis is involved
│       └── README.md
│
└── documentation/
    ├── README.md
    ├── codebooks/             # Variable definitions, survey instruments
    │   └── README.md
    └── dictionaries/          # Data dictionaries, metadata
        └── README.md
```

**Adapt as needed:** Projects with multiple survey rounds or data sources get a subfolder per
source inside `data/` and a mirrored subfolder inside `code/`. See `references/multi-source.md`.

---

## Tasks

### 1. New Project Setup

When asked to set up a project:

1. Confirm the project root path with the user.
2. Create all folders above using `mkdir -p`.
3. Write README stubs into each folder (see README stub template below).
4. Create a language-appropriate master script at the root (see `references/master-scripts.md`).
5. If Git is not initialized, suggest `git init` and offer a `.gitignore` template.
6. Report the full tree of what was created.

**README stub template:**
```markdown
# [Folder Name]

## Purpose
[One sentence: what this folder contains and its role in the workflow.]

## Contents
[List key files or subfolders once they exist. Update as the project grows.]

## Naming Convention
[Describe the convention used in this folder, e.g., `round1_clean_v1.dta`.]

## Dependencies
[What must exist or run before files here are created/used.]
```

**Root README template:**
```markdown
# [Project Name]

## Overview
[What this project does, one paragraph.]

## How to Replicate
1. Clone the repository.
2. Set the root path in `MASTER.[ext]`.
3. Run `MASTER.[ext]` from top to bottom.

## Software & Versions
[List language, key packages, versions.]

## Data Access
[Where raw data comes from; any access restrictions.]

## Team
[Who maintains this; contact info.]
```

---

### 2. Audit Existing Project

When asked to audit or check a project structure:

1. Read the existing directory tree (use `find . -type d` or equivalent).
2. Check against the standard structure. Flag each violation with a severity:
   - **[CRITICAL]** Raw data modified or missing separation of raw/intermediate/final.
   - **[CRITICAL]** No master script.
   - **[HIGH]** Code and data not in parallel structure.
   - **[HIGH]** Outputs committed to Git (large binary files).
   - **[MEDIUM]** Missing README in any folder.
   - **[MEDIUM]** Ambiguous or inconsistent file naming.
   - **[LOW]** Project management files mixed into DataWork folder.
3. Output a structured report: violations by severity, then recommended fixes.
4. Offer to apply fixes automatically where possible (create missing READMEs, rename folders).

---

### 3. File Naming Conventions

When advising on naming:

**General rules:**
- Use lowercase and hyphens or underscores consistently (pick one, never mix).
- Never use spaces in file or folder names.
- Date-stamp files that version over time: `YYYYMMDD_description.ext`
- Never use `final`, `final2`, `final_FINAL` as version markers. Use dates or Git tags instead.
- Be descriptive: `hh_survey_round1_clean.dta` beats `data1_v3.dta`.

**By file type:**
| Type | Convention | Example |
|---|---|---|
| Raw data | `source_description_YYYYMMDD.ext` | `dhs_ethiopia_20220301.csv` |
| Cleaned data | `source_description_clean.ext` | `dhs_ethiopia_clean.dta` |
| Final data | `source_description_final.ext` | `hh_panel_final.dta` |
| Scripts | `NN_verb_description.ext` | `01_clean_hh.R` |
| Outputs | `fig_description.ext` or `tab_description.ext` | `fig_wage_by_age.png` |

**Numbering scripts:** Prefix with `NN_` to signal execution order (`01_`, `02_`, ...). The master
script runs them in this order.

---

## Script Structure

**Every script in the project must begin with this header and section skeleton — no exceptions.**
Do not start from a blank file. Fill in the metadata fields, then build downward.

```r
# ============================================================
# [Descriptive Title]
# Author: [from project context]
# Purpose: [What this script does]
# Inputs:  [Data files read]
# Outputs: [Files written: data, figures, tables]
# ============================================================

# 0. Setup ----
library(tidyverse)
# [add packages as needed]

# 1. Load Data ----

# 2. Clean / Transform ----

# 3. Analysis ----

# 4. Export ----
```

**Language equivalents for the header block:**

Stata:
```stata
* ============================================================
* [Descriptive Title]
* Author: [from project context]
* Purpose: [What this script does]
* Inputs:  [Data files read]
* Outputs: [Files written]
* ============================================================
```

Python:
```python
# ============================================================
# [Descriptive Title]
# Author: [from project context]
# Purpose: [What this script does]
# Inputs:  [Data files read]
# Outputs: [Files written]
# ============================================================
```

**Section markers** (`# 0. Setup ----`, `# 1. Load Data ----`, etc.) must be present in every
script. Add or rename sections to fit the task, but never omit the header block or the `# 0. Setup` section.

---

## Reference Files

- `references/master-scripts.md` — Master script templates for Stata, R, Python
- `references/multi-source.md` — Folder structure for projects with multiple data sources
- `references/gitignore.md` — Recommended `.gitignore` patterns for research projects

Read a reference file when the task specifically requires it (e.g., user asks for R master script
template, read `references/master-scripts.md`).
