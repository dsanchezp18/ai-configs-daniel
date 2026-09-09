---
name: documentation-writer
description: Write project documentation the way Daniel likes it. The model is the Compensation of Employees methodology and technical guide: pedagogical, current-state, equation then words then a worked example. Use when writing or rewriting methodology notes, technical guides, READMEs, or estimation documentation.
---

# Documentation writer

Write documentation for a human. Write for a non-technical reader, or for a
technical reader without this project's background. Do not write for an AI.

The model is the Compensation of Employees pair:

- methodology: what is measured, with which data, by which formula, and why
  that formula
- technical guide: which scripts run, what they read, what they write

Philosophy is the rule. See `AGENTS.md` **Documentation for humans** when
that section exists.

## Before writing

1. Read the current code and the current outputs. Document what is here now.
2. Read the COE methodology and technical guide if they exist in the repo
   (`knowledge-base-llms/components/1_compensation_of_employees/documentation/`
   or `components/1_compensation_of_employees/documentation/src/`). Match
   that density and that teaching order.
3. Do not copy structure from software READMEs, API docs, or AI templates.

## What a good page does

A new colleague can follow the method without sitting next to the author.

State, in order:

1. Purpose. What this document is, in one short paragraph.
2. Measure. The identity or formula. Then a sentence that names every
   symbol.
3. Data. Tables, vectors, units, and the conversion (thousands to millions,
   weekly to monthly).
4. Each estimation step. Formula, then plain words, then a worked example
   with numbers.
5. Choices that affect the number. Say what was chosen and why, in ordinary
   English.
6. What the code writes. File names and what is in them.

The COE methodology does this. Method 1 is not "YTD growth is applied." It
is: fix the window, sum both years, form the rate, grow last year's published
level, then a $1,200 million example. Method 2 does not say "use a proxy."
It says the SEPH dollar level is discarded and only the growth is kept, then
shows why.

The COE technical guide does the other half. Folder tree. Run order. One
section per script. A table of files and who uses them. What the script
writes. How a year with missing months is handled, in numbered steps.

## How to write a step

Short sentences. One idea per sentence. Ordinary words.

For a formula:

1. Show the formula.
2. Start the next paragraph with "Here," and define each symbol.
3. Give a small numerical example.
4. State the assumption in a sentence a person can disagree with.

Do not leave a symbol undefined. Do not skip the example. Do not hide the
assumption in jargon.

Numbered steps are for a sequence the reader must keep in order. Tables are
for files, cutoffs, or selection rules. Prose is for the calculation.

## What not to write

- History of the work, how the repository got here, or what the code does
  not do.
- Roadmaps, future work, or "this will later."
- Ceremony: "This document aims to," "In this section we will," "It is
  important to note."
- Mannered prose. Say "a parameter worth varying," not "a dial worth
  turning." Say "this point still matters," not "this point earns its keep."
- Software vocabulary used as design: contract, provenance, blocker,
  mutable, rollback, boundary, cadence, manifest, orchestration.
- Comments or headings written for a model to parse.

If the reader has to ask for clarification, the writing has already failed.
If following it hurts, it is too complicated. Simplify.

## AI patterns. Do not use these

Do not use these words and frames. They are common in generated documentation
and they are not how this project writes.

- Moreover, Furthermore, Additionally, In addition
- It is important to note, It is worth noting, Notably
- In conclusion, In summary, To summarise
- In this section we, This document aims to, Let's dive, As mentioned above
- delve, tapestry, landscape, robust, seamless, holistic, comprehensive
- leverage, utilize, facilitate, unlock, empower
- play a crucial role, pivotal, shed light on, underscore, highlight the
  importance
- not only X but also Y
- production-ready, cutting-edge, best-in-class
- em dashes. Use a comma, a colon, a parenthesis, or a new sentence.

Do not write three paragraphs with the same shape. Do not stack hedges.
Do not open every section by restating the heading.

## Split the two documents

**Methodology.** Measurement. Equations. Data basis. Selection rule.
Assumptions. Worked examples. Validation only as evidence for a choice that
is already in production (a MAPE, a cutoff), not as a software test suite.

**Technical guide.** Folders. Run sequence. Script responsibilities.
Input files. Output files. How Excel is used (reporting only, if that is
the case). What a column means.

Do not mix them. Do not replace either with a changelog.

## Output

Write the document the user named. Match nearby documentation tone if that
tone is the COE style. If nearby docs are thinner or ceremonial, follow this
skill, not the thin page.

Do not add extra README indexes, "docs/" trees, or files the user did not
ask for.
