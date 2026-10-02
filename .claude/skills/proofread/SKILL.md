---
name: proofread
description: Proofread and correct text (.tex, .qmd, .md, .txt, or pasted text). Fixes grammar, typos, duplicated words, punctuation, and inconsistent terminology, notation and citation format. Edits the file directly and lists the changes in the chat. Use when the user says "proofread", "check for typos", "copy-edit this", "any writing errors?", "fix the grammar", or before releasing a document or lecture.
argument-hint: "[filename, or paste text] [--check to report without editing]"
allowed-tools: ["Read", "Grep", "Glob", "Edit"]
---

# Proofread

Read the text, correct the errors, and edit the file in place. Do not write any report file. Give the summary in the chat.

By default, edit the file. With `--check`, or when the user only asks whether there are errors, change nothing and list the findings in the chat. For pasted text, return the corrected text.

## What to correct

- **Grammar:** subject-verb agreement, articles, prepositions ("eligible to" becomes "eligible for"), tense consistency, dangling modifiers.
- **Typos:** misspellings, duplicated words ("the the"), missing or extra punctuation, search-and-replace leftovers.
- **Consistency:** one spelling variant (Canadian or American) throughout, the same term and the same symbol for the same thing, one citation format (`\citet` vs `\citep` in LaTeX, `@key` vs `[@key]` in Quarto).
- **Missing or awkward words:** incomplete sentences, phrasing a reader could misread.
- **Citations:** check that a citation key points to the paper the sentence names, when the bibliography file is available.

## What not to change

- Do not change meaning, numbers, claims, equations or the author's word choice. Fix errors, do not restyle.
- Do not edit LaTeX or Quarto commands, labels, math, or code blocks except for a clear typo.
- If the text follows a voice rule (`daniel-voice`, `el-quanti-voice`, `economic-statistics-insights`), keep it. Do not add em dashes, hedges or contractions that rule forbids.
- If a correction depends on a fact you cannot check (a number, a date, a name), flag it in the chat and leave the text as it is.

## Layout problems

In `.tex` and slide files, content that may overflow (a long equation, too many bullets on one slide, an inline font size below 0.85em in Quarto) cannot be fixed safely by editing words. List these in the chat with their location. Do not change the layout.

## What to tell the user

After editing, reply in the chat with:

1. The number of corrections, by type.
2. The corrections that change how a sentence reads, each as a before and after pair.
3. Anything flagged but not changed: unverified facts, overflow risks, citation keys that look wrong.

Keep it short. Do not repeat the whole file.

## Related

- `humanize`: AI-voice tells in prose.
