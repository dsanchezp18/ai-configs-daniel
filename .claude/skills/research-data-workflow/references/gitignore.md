# .gitignore Patterns for Research Projects

## Recommended .gitignore for a research DataWork folder

```gitignore
# ==============================================================================
# Research Project .gitignore
# ==============================================================================

# --- Raw and sensitive data ---
# Never commit raw data to Git. Store in Dropbox, OneDrive, or secure institutional storage.
data/raw/
data/*/raw/

# Sensitive file types (PII risk)
*.dta.enc
*.zip
*.7z

# --- Large binary outputs ---
# Figures and tables are build artifacts — regenerate from code.
# Exception: commit outputs only if build takes hours or requires licensed data.
outputs/graphs/
outputs/tables/
outputs/maps/

# --- Proprietary/binary data formats ---
*.dta          # Commit only if dataset is small and public
*.sav
*.xlsx
*.xls

# --- OS and editor junk ---
.DS_Store
Thumbs.db
*.swp
*~
.Rhistory
.RData
.Rproj.user/
__pycache__/
*.pyc
*.pyo
.ipynb_checkpoints/

# --- Log files ---
*.log
*.smcl             # Stata log

# --- Temp files ---
*.tmp
~*.docx
~$*.xlsx
```

---

## What TO commit

| Commit | Do not commit |
|---|---|
| All code scripts | Raw data |
| README.md files | Cleaned/final data (unless small and public) |
| Master script | Large binary outputs |
| `.gitignore` | PII-containing files |
| Environment files (`renv.lock`, `requirements.txt`, `environment.yml`) | API keys or credentials |
| Small public reference files | Temporary/OS files |

---

## Git + Dropbox warning

**Never put a Git repository inside a Dropbox (or OneDrive, Google Drive) folder that is
synced and shared with others.** The sync tool will conflict with Git's internal state files,
creating corrupted repositories. The correct setup:

- **DataWork/code** → Git (GitHub, GitLab, etc.)
- **DataWork/data/raw** → Dropbox or institutional secure storage (no Git)
- **Project admin materials** → Dropbox (completely separate from the Git repo)
