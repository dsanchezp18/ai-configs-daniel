---
name: humanize
description: Find and fix AI-voice tells in prose (.tex, .qmd, .md, .txt, or pasted text). Edits the text directly and lists the changes in the chat. Tells include boilerplate transitions ("Moreover", "It is important to note that"), cliché words ("delve", "navigate the complexities", "robust framework"), em-dash overuse, same-shaped paragraphs, tricolon abuse, stacked hedges, "not only X but also Y", formulaic openers, hyphenation excess and self-important framing. Use when the user says "humanize", "de-AI this", "does this sound like AI?", "remove AI voice", or before submitting or posting a draft.
---

# Humanize

Read the text, find AI-voice tells, and fix them in place. Do not write any report file. Give the summary in the chat.

By default, edit the file. With `--check`, or when the user only asks whether the text sounds like AI, change nothing and list the findings in the chat. For pasted text, return the revised text.

## How to fix

- Make the smallest edit that removes the tell. Keep the author's meaning, claims, numbers and citations.
- Remove filler connectors. Where a real link between two sentences exists, name it ("Because", "This implies").
- Replace a cliché with the plain word or a direct statement.
- Fix a stacked hedge by keeping the single clearest qualifier. If the author's rules allow no hedge, drop it.
- Break up a run of same-shaped paragraphs by rewriting the weakest one. Do not rewrite a paragraph that has no tell.
- Do not add new tells while fixing: no new transitions, no new tricolons, no new em dashes.
- If a construction may be deliberate (a legitimate "not only X but also Y", a single "Moreover" in a long draft), leave it.
- If the author's voice skill applies (`daniel-voice`, `el-quanti-voice`, `economic-statistics-insights`), follow its rules for what to keep. Those rules win over this list.
- Calibrate to the field. "In this paper, we..." is normal in some fields and a tell in others.

## What to look for

1. **Boilerplate transitions:** Moreover, Furthermore, Additionally, In addition, It is important to note that, It is worth noting that, Notably, In conclusion, In summary, Building on this, As we can see, stacked Indeed, and "On the other hand" when nothing is being contrasted.
2. **Cliché lexicon:** navigate the complexities or landscape, delve into, tapestry, robust, comprehensive or holistic framework, multifaceted or nuanced approach, leverage (as a verb outside finance and engineering), in today's [X] landscape, play a crucial or pivotal role, shed light on, underscore or highlight the importance, It is essential or crucial to. Weigh these most in the abstract and introduction.
3. **Punctuation:** more than three em dashes in a paragraph, three or more semicolons in a paragraph, a repeated "X, Y, and Z" cadence from paragraph to paragraph.
4. **Symmetric paragraphs:** three or more consecutive paragraphs that each run topic sentence, three examples, summary clause.
5. **Tricolon abuse:** more than four three-item lists per page, lists forced to three items, stacked adjective triples ("clear, concise, and compelling").
6. **Stacked hedges:** "might potentially", "could possibly suggest", "may arguably", "perhaps potentially". These are almost never the author's choice.
7. **"Not only X, but also Y":** more than two per piece, items that are not parallel, or used as a paragraph opener.
8. **Formulaic openers:** every section starting "This section does X", or a paragraph that restates its heading.
9. **Hyphenation excess:** three or more of data-driven, evidence-based, well-suited, well-established or long-standing in one paragraph.
10. **Self-important framing:** "this important contribution", "this significant finding", "our novel approach", "groundbreaking", "pioneering".

Skip `.bib`, code files and code comments. These patterns are tuned for prose.

## What to tell the user

After editing, reply in the chat with:

1. The count of changes per category.
2. The ten or fewer most important before and after pairs.
3. Any paragraph that still reads machine-written and needs the author to rewrite it from scratch.

Keep it short. Do not repeat the whole file.

## What this cannot do

This improves how the prose reads. It does not make machine-written text read as human to an AI detector, because every rewrite by a model is still model output. For anything with the author's name on it, the author writes the sentences that carry the argument. See `writing-with-ai.md`.

## Related

- `proofread`: grammar, typos and consistency.
- `daniel-voice`, `el-quanti-voice`, `economic-statistics-insights`: write in a specific voice.
