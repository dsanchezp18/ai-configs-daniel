---
name: organize-folders
description: Review a folder and propose a cleaner layout, then move files only after the user agrees. Two modes. Pipeline mode organizes a data analysis project (R, Stata, Python, or Julia) into raw, intermediate, and final data, code, outputs, and documentation. General mode asks the user questions, then suggests a layout. Use when the user says "organize this folder", "clean up this project", "where should these files go", or "set up the folders".
---

# Organize folders

This skill reviews a folder and suggests a better layout. It does not move
anything until the user says yes.

## Choose the mode

- Pipeline mode: the folder holds a data analysis project. Signs: data files
  plus scripts (`.R`, `.do`, `.py`, `.jl`, `.qmd`), or the user says
  "pipeline", "project", or "analysis". Use the pipeline layout below. Do not
  ask what the layout should be.
- General mode: any other folder (documents, downloads, a mixed archive).
  Ask questions first. Then suggest a layout.
- If the mode is not clear, ask one question: "Is this a data analysis
  project with data and code, or a general folder?"

## Steps for both modes

1. List the folder. Use `Glob` or `ls`. Count files by type. Note the depth.
2. Find what already works. Keep names and folders the user already uses.
3. Write a plan: a table with three columns: current path, new path, reason.
4. Show the plan. Ask the user to approve it. The user may approve all, part,
   or none.
5. Move only the approved files. Use `git mv` in a git repository, and `mv`
   elsewhere.
6. List the folder again and report what moved.

## Pipeline mode

A data analysis pipeline reads from top to bottom: raw data, cleaning,
analysis, outputs. The folders follow that order. The layout is the same for
every language. It matches `R Code Conventions.md` section 15 and
`General Code Conventions.md`.

```text
project-root/
├── README.md
├── master script (MASTER.R, master.do, main.py, or main.jl)
├── data/{raw,intermediate,final}/
├── code/{cleaning,analysis,functions}/
├── outputs/{tables,graphs}/
├── documentation/
└── .gitignore
```

What goes where:

- `data/raw/`: files exactly as received. Downloads, exports, survey files.
- `data/intermediate/`: cleaned or merged data that later scripts read.
- `data/final/`: the data used for the reported results.
- `code/cleaning/`: scripts that turn raw data into intermediate data.
- `code/analysis/`: scripts that make estimates, tables, and figures.
- `code/functions/`: helper code that more than one script uses.
- `outputs/tables/` and `outputs/graphs/`: results. Regression tables,
  `.xlsx`, `.png`, `.pdf`.
- `documentation/`: codebooks, data notes, method notes, papers.
- Logs (for example Stata `.log` files) go in `logs/` if the project already
  has one. Do not add it otherwise.

Rules:

- Raw data is never changed. Do not edit, rename the contents of, or
  overwrite a raw file. Moving a raw file into `data/raw/` is allowed.
- Keep raw, intermediate, and final data in separate folders.
- Code and data folders mirror each other where it is practical.
- Name scripts `NN_verb_description` when the run order matters, for example
  `01_clean_survey_main`. Cleaning scripts are `NN_clean_<dataset>`. Keep the
  language's extension.
- Use `snake_case` for files and folders.
- Mixed languages are fine. Keep each script in the folder for its job, not in
  a folder for its language.
- If the project already has a layout that works, keep it. Suggest only the
  moves that fix real problems: raw and processed data mixed, results next to
  code, scripts with no run order, or files in the root.
- Do not put a Git repository inside a shared Dropbox, OneDrive, or Google
  Drive folder. Tell the user if you find one.
- Do not create `README.md`, a master script, or empty folders the project
  does not need. Suggest them in the plan and let the user decide.
- Do not add checks, manifests, or extra layers. Keep the layout small.

After a move, tell the user which scripts may need a path change. Do not edit
the scripts unless the user asks.

## General mode

Ask the user these questions first. Use `AskUserQuestion`. Ask at most four
at a time.

1. What is in this folder, and what is it for?
2. How do you look for files: by project, by date, by type, or by person?
3. Who else uses this folder?
4. Should old files be kept in place, moved to an archive folder, or left
   alone?

Then suggest one layout. Keep these patterns unless the user says otherwise:

- Group by purpose first (project, client, topic). Group by type or date
  inside it.
- Use at most 3 levels of folders. Flag anything deeper.
- Use one clear name per folder, in `snake_case` or the style the user
  already uses.
- Start dated files with `YYYY-MM-DD` so they sort in order.
- Keep one `archive/` folder for old files. Do not scatter old copies.
- Name files so a stranger can tell what they are. Flag names like
  `final_v2_new`, `untitled`, and `copy of`.
- Find duplicates by name and size. Show them. Do not delete them.

If two layouts are reasonable, show both in short form and ask which one the
user prefers.

## Rules

- Never delete a file. Never overwrite a file. If a target path already
  exists, stop and ask.
- Do not move hidden folders (`.git`, `.Rproj.user`) or files inside them.
- Do not move files outside the folder the user named.
- Large moves (more than 50 files): show the plan in groups and ask once per
  group.
- Do not commit or push. Do that only when the user asks.
- Write the plan and the report in plain English. Short sentences.
