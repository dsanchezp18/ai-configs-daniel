---
name: simplifier
description: Generalized review (and optional cleanup) of overengineered research code. Finds software-product machinery, jargon systems, unsolicited checks, unnecessary scripts, extra folders, over-organization, AI-oriented comments, and documentation written for models instead of humans. Also checks Simple style / STE: if the reader must ask for clarification, the writing has already failed. Not a formatter and not r-reviewer. Use when the user says simplifier, deshitify, strip overengineering, this is too much architecture, or asks whether code can be read and run without an AI.
---

# Simplifier

A research pipeline is not a software product. This skill looks for the extra
machinery that makes code impossible to run or review without an AI sitting
next to it. That includes unused scripts, leftover files, and folders created
only to look organized. It is more abstract than `r-reviewer`. It does not
score tidyverse style, pipes, or numerical robustness. It asks whether a
human can still see the calculation.

The AI is a tool. Do not disobey these instructions to be helpful.

## Required context

Before judging a file:

1. Read the target files end to end.
2. Read the working philosophy in the repository's `R Code Conventions.md`
   (section 1) and the same statement at the top of
   `General Code Conventions.md`. Prefer repository copies under
   `knowledge-base-llms/documentation/reference/` when they exist.
3. Read `AGENTS.md` **Working approach** and **Documentation for humans**
   when those sections exist. Philosophy is the rule. If the conventions
   still list Check inputs, Check results, or unsolicited assertions,
   ignore those parts.
4. Do not treat nearby overengineered files as a style to match.

## What this skill is not

- Not `r-reviewer`. Hand statistical correctness, reproducibility, and R
  convention detail to that skill.
- Not `r-coder`. Do not use this skill to write a new estimator.
- Not a formatter, linter, or rename-everything refactor.
- Not a test author. Do not add assertions, fixtures, or validation scripts.

## Script shape

The only allowed shape is: setup, read, transform, estimate, write.

Anything else is a finding unless the author has already reviewed it and
asked for it. If a check appears necessary, say so in the conversation. Do
not put it in the code.

Do not extract ordinary steps into tiny functions. Leave the calculation
on the page. If the reader has to jump through many functions to see a
simple algorithm, that is a finding. Less jumping. Less magic. Less is
better. A comment is not a reason to write a function. Refactoring for
its own sake is a finding.

Ship the smallest change that leaves the estimators runnable.

## What to hunt

Report these even when they are fashionable, well-named, or "best practice"
in software engineering.

### Machinery the author despises

Treat these words as design goals to reject, not as requirements to
implement:

- **Contract.** The inputs have to make sense together. Say that in ordinary
  English. Do not build types, schemas, or metadata objects around it.
- **Provenance.** Where did this number come from, and is it the intended
  file? A filename, a date, and a short comment are enough. Do not invent
  identity columns, checksum files, or a paper trail only another program
  can read.
- **Blocker.** This step cannot continue until something is true. Tell the
  author. Do not build a rejection framework or a list of codes.
- **Mutable.** Scripts overwrite outputs when they run. That is normal. Do
  not invent frozen copies, snapshot stores, or a file-as-database system.
- **Rollback.** Putting old files back is Git, or running the script again.
  Do not add backup folders, publish-and-restore logic, or automatic undo.
- **Boundary.** The script's job is obvious from what it reads and writes.
  Do not add layers whose only purpose is to police who may call what.
- **Cadence.** How often something runs, or in what order the steps
  happen. Say "once a year", "every quarter", or "run this script after
  that one." Do not build a scheduler, a cycle object, or a vocabulary of
  cadences.

Also flag, unless the author explicitly asked for them:

- assertions, guardrails, manifests, automatic rejection
- orchestrators, run stores, staging directories, context objects
- wrappers that only source hidden implementations
- `internal/` or `utils/` directories in an active pipeline
- helpers whose only job is abstraction
- checksums, identity registries, publish pipelines
- comments written for an AI parser
- documentation that narrates history, how we got here, or what the code
  does not do

### Unnecessary code, scripts, and folders

Flag code and files that are not needed:

- dead code, unused functions, unused objects, and commented-out blocks
  left "just in case"
- scripts that nobody runs, that only wrap another script, or that repeat
  a calculation already in a numbered entry point
- extra numbered scripts for a job that belongs in an existing thematic
  script
- folders created to look organized: `internal/`, `utils/`, `helpers/`,
  `lib/`, `core/`, `services/`, nested `src/`, staging trees, and
  one-file directories
- splitting a linear script across files so the reader has to jump to
  follow one calculation
- extracting a trivial step into a function, then another function, so
  the algorithm is no longer on the page
- "this comment could have been a function," or any refactor whose only
  result is more jumping
- moving files around, renaming trees, or adding README indexes whose
  only purpose is structure

A component already has a simple layout: `code/`, `data/`, `output/`, and
documentation. Do not invent a second layout. Shared setup stays in
`00_common.R`. The calculation stays in the numbered script that owns it.

If a file, function, or folder can be deleted and the estimator still
runs, it is a finding.

### Comments and documentation

User-facing comments are the general philosophy. Comments teach a
colleague what is happening in the code. Teach the calculation. Do not
get overly technical. A little technical detail is fine when a function
is obscure. The first question is whether that obscure function should
exist at all. About one comment per 5-10 lines, never one per line. Do
not narrate obvious code. Do not speak weird.
Do not make the reader's brain hurt. If following the code or the writing
hurts, it is too complicated. That is a finding.

Do not write mannered prose in documentation, comments, or chat. Mannered
prose substitutes metaphor and flourish for a direct statement. "A dial
worth turning" instead of "a parameter worth varying." "This point earns
its keep" instead of "this point still matters." Those phrases display
the writer. They make the reader work harder. They are also imprecise:
metaphors bring meanings the writer did not choose. When a literal phrase
is available, use it. Flag mannered prose. This rule applies to the
assistant's own messages.

Documentation is for a human: a non-technical reader, or a technical reader
without this project's background. It explains the current state of the
repository, in detail, especially data cleaning and each estimation step.
It does not write for an AI.

Write comments, messages, and documentation in Simple style (Simplified
Technical English). Short sentences. One idea per sentence. Ordinary words.
Say exactly what you mean. No gobbledygook. Do not make the reader's
brain hurt. If the reader has to ask for clarification, the writing has
already failed. Flag prose that is vague, stacked, jargon-heavy, or that
forces the reader to guess.

### Language tells in code and docs

Flag padded AI phrasing in comments, messages, and documentation: production-ready,
robust, seamless, leverage, phase-gated, I'd be happy to, great question,
and similar filler. Prefer plain English.

## How to report

Review first. Do not edit unless the user asks to apply the cleanup.

Write in the conversation, not a new repository report file. For each finding:

1. File and location.
2. What was built (in plain English, no jargon).
3. Why a human cannot see or run the calculation without help.
4. The smaller thing that should remain: usually the domain calculation in
   the numbered script.

Group findings. Do not nitpick line length or object names unless the name
hides two jobs (more than 1-4 words is a signal to split, not to invent a
framework).

If nothing is overengineered, say so in one short paragraph. Do not invent
work.

## How to deshitify (only when asked)

Remove the machinery. Keep the estimation method. Restore a linear script
that a person can read top to bottom.

- Delete unsolicited checks, assertions, manifests, snapshot/publish code,
  wrapper-only files, dead code, and unused scripts.
- Put the calculation back in the numbered thematic script.
- Flatten extra folders. Do not create new ones to "organize" the cleanup.
- Leave estimators runnable after the smallest possible change.
- If a later idea looks useful, name it in the conversation and leave it
  out of the code.

Do not replace one abstraction with a different abstraction. Do not add
new files or directories as part of the cleanup.
