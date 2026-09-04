---
name: replication-check
description: >
  Evaluates whether a paper's reported results are conceptually sound and correctly implemented
  by its code. Use this skill whenever a user asks to check, audit, verify, or replicate a paper's
  results against its code, or says things like "does this code actually do what the paper claims",
  "check this replication package", "review my coauthor's code against the paper", or "sanity-check
  these regressions". Works on any language (R, Stata, Python, Julia). Best used with both the
  paper (PDF/tex/qmd) and its code/replication files available to read.
---

# Replication Check Skill

Checks a paper's main results against the code that produces them, looking for both conceptual
and implementation errors. Based on a prompting approach described by Michael Wiebe
(blog.michaelwiebe.com/p/can-ai-do-replications-gpt52-vs-gpt54), who found this framing
substantially improves an LLM's ability to catch planted methodological and coding errors.

---

## Core evaluation prompt

For each main result in the paper, ask two questions:

1. **Is the method conceptually sound?** Does the identification strategy / estimator / test
   actually answer the question the paper claims to answer?
2. **Does the code correctly implement the method?** Line by line, does the code do what the
   method requires?

Point out anything that could be a **fatal flaw** — an error that could reverse or invalidate the
finding — even if it looks like an edge case. For example: if the code assumes a balanced panel
but the method (or the data) doesn't guarantee one, flag it as serious, because panel data is
often unbalanced in practice.

## How to apply this

- **Be honest, not generous.** Do not soften findings to be polite. The point is to catch real
  problems before a referee (or reality) does.
- **Prioritize fatal flaws over style.** Ignore typos, formatting, and naming conventions unless
  asked. Focus on anything that could change a sign, a significance level, or a magnitude.
- **Check both directions.** A method can be conceptually right but coded wrong (e.g. wrong
  clustering level, wrong lag structure, off-by-one in an event study). Or coded exactly as
  described but the method itself doesn't identify what's claimed.
- **Common places errors hide:**
  - Panel balance assumptions (balanced vs. unbalanced)
  - Standard error clustering (wrong level, or clustering ignored entirely)
  - Sample restrictions applied inconsistently between text and code
  - Event-study / distributed-lag timing (off-by-one, wrong reference period)
  - Instrument relevance/exclusion asserted in text but not tested in code
  - Weights described in the paper but missing from the regression call
- **State your confidence.** If you can't verify something without running the code (e.g. no
  access to the data), say so explicitly rather than guessing.

## Output

For each main result checked, report:

```
Result: [table/figure number or description]
Conceptually sound? [yes/no/unclear] — [one line why]
Code matches method? [yes/no/unclear] — [one line why]
Fatal flaw risk: [none/low/high] — [what would need to be true for this to break the finding]
```

End with a short summary: which results are solid, which need author attention, and which
couldn't be checked without more access (data, missing scripts, etc.).
