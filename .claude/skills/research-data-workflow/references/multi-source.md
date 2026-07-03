# Multi-Source Project Structure

When a project uses multiple data sources or survey rounds, extend the standard structure
by adding a subfolder per source inside `data/` and mirroring it inside `code/`.

---

## Example: Two Survey Rounds + Administrative Data

```
project-root/
├── README.md
├── MASTER.do / MASTER.R / main.py
│
├── data/
│   ├── README.md
│   ├── hh-survey-round1/
│   │   ├── README.md
│   │   ├── raw/
│   │   ├── intermediate/
│   │   └── final/
│   ├── hh-survey-round2/
│   │   ├── README.md
│   │   ├── raw/
│   │   ├── intermediate/
│   │   └── final/
│   └── admin-records/
│       ├── README.md
│       ├── raw/
│       ├── intermediate/
│       └── final/
│
├── code/
│   ├── README.md
│   ├── hh-survey-round1/
│   │   ├── README.md
│   │   ├── 01_clean.do
│   │   └── 02_construct.do
│   ├── hh-survey-round2/
│   │   ├── README.md
│   │   ├── 01_clean.do
│   │   └── 02_construct.do
│   ├── admin-records/
│   │   ├── README.md
│   │   └── 01_clean.do
│   └── analysis/
│       ├── README.md
│       ├── 01_merge_sources.do
│       ├── 02_descriptives.do
│       └── 03_regressions.do
│
├── outputs/
│   ├── graphs/
│   ├── tables/
│   └── maps/
│
└── documentation/
    ├── hh-survey-round1/
    │   ├── codebook.pdf
    │   └── survey-instrument.pdf
    ├── hh-survey-round2/
    │   └── codebook.pdf
    └── admin-records/
        └── data-dictionary.xlsx
```

---

## Key rules for multi-source projects

1. **Never merge sources in the cleaning stage.** Each source is cleaned independently to
   its own `final/` folder. Merging happens in `code/analysis/` and outputs a merged dataset
   to a shared `data/final/` or a clearly named analysis dataset.

2. **Source subfolder names must be stable.** Once set, do not rename them — scripts
   hardcode paths to these folders.

3. **Document data provenance per source.** Each source subfolder's README.md must say:
   where the data came from, when it was received, who is the contact, and any access restrictions.

4. **Encryption for sensitive raw data.** Raw data with PII should be stored encrypted
   (e.g., VeraCrypt container or institutional secure storage) and excluded from Git via
   `.gitignore`. Only de-identified or aggregated data should be committed.
