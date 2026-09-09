# Repository instructions

Philosophy is the rule. Read `R Code Conventions.md` before writing or
reviewing R code. Read `General Code Conventions.md` before writing or
reviewing Stata, Python, or Julia code. Use those files for formatting,
packages, verbs, paths, and modelling.

The convention files match this philosophy. Do not add Check inputs, Check
results, unsolicited assertions, or tiny-function extraction. A missing
check is not a defect.

Skills under `.agents/skills/` define workflow. They do not replace this
philosophy.

## Working approach

This is a research pipeline, not a software product. Write code for the
person who has to read it next year without the original author, and without
an AI sitting next to them.

The AI is a tool. The scripts have to run, and make sense, on their own. If
the code only works under AI supervision, or only makes sense after an AI
explains it, it has already failed.

Write readable, linear code. Show the domain calculation in the script.
Names should say what the object is in the subject matter, in 1-4 words.

The script has one shape: setup, read, transform, estimate, write. Nothing
else. Do not add input checks, result checks, assertions, validation
scripts, or guardrails unless they have been reviewed and explicitly
requested. If a check appears necessary, say so in the conversation. Do not
put it in the code.

Do not extract ordinary steps into tiny functions. Leave the calculation
on the page. If the reader has to jump through many functions to see a
simple algorithm, the code has already failed. Less jumping. Less magic.
Less is better. Do not turn a comment into a function. Do not refactor
for its own sake.

Do not disobey these instructions to be helpful.

Overengineering is the usual failure. Extra layers, helpers, frameworks, and
architecture make the calculation harder to see. Then the work cannot be run
or reviewed without help. That is the opposite of the standard.

Words that must not be treated as design goals: contract, provenance,
blocker, mutable, rollback, boundary, cadence. Say the ordinary English
instead. Do not build systems around those words.

No assertions unless explicitly requested. No manifests. No automatic
rejection. If a stop has been requested, use a short message in plain
English.

User-facing comments are the general philosophy. Write comments a colleague
can read. Teach what is happening in the code. Teach the calculation. Do
not get overly technical. A little technical detail is fine when a function
is obscure. The first question is whether that obscure function should
exist at all.

Do not speak weird. Ordinary English. No gobbledygook.
Do not make the reader's brain hurt. If following the code or the writing
hurts, it is too complicated. Simplify.

Do not narrate obvious code, and do not write comments for an AI parser.
About one comment per 5-10 lines, never one per line.

Ship the smallest change that leaves the work runnable.

If a later idea is useful, name it and leave it out of the code until it is
asked for.

## Documentation for humans

Write documentation for a human. Write for a non-technical reader, or for a
technical reader without this project's background. Do not write for an AI.

Use Simple style (Simplified Technical English). Short sentences. One idea
per sentence. Ordinary words. Say exactly what you mean. No gobbledygook.
Do not speak weird. Do not make the reader's brain hurt. If the reader has
to ask for clarification, the writing has already failed.

Do not write mannered prose in documentation, comments, or chat. Mannered
prose substitutes metaphor and flourish for a direct statement. "A dial
worth turning" instead of "a parameter worth varying." "This point earns
its keep" instead of "this point still matters." Those phrases display
the writer. They make the reader work harder. They are also imprecise:
metaphors bring meanings the writer did not choose. When a literal phrase
is available, use it. This rule applies to the assistant's own messages.

Documentation explains the current state of the repository. It is
pedagogical and very detailed, especially on data cleaning and on each
estimation step. It says what the data are, how they are cleaned, and how
the estimate is formed, in enough detail that a new reader can follow the
method without sitting next to the author.

Do not write the history of the work. Do not write how the repository got
here. Do not write what the code does not do. Describe what is here now.
