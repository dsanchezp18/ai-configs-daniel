---
name: slides-from-text
description: Turn an article, report or other text into a slide deck outline, and build the deck on request. Built for Government of Alberta statistics work (neutral public-sector tone, one finding per slide, source notes), and also works for other text. Use when the user says "make slides from this", "turn this article into a deck", or asks for a presentation of a written piece.
argument-hint: "[source text or file] [audience and length]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Skill"]
---

# Slides from text

Turn the source text into slides that carry the same findings, numbers and sources. Do not add statistics, causes or claims that the text does not contain.

## Steps

1. **Read the source.** Find the central finding, the supporting findings, and every figure and table.
2. **Ask only what is missing.** Audience, time or slide count, and format. If the user gave none, assume policy staff, about one slide per minute, and `.pptx`.
3. **Write the outline first.** One line per slide: title, the one finding, the figure or table, the source. Show it to the user.
4. **Build the deck** after the user agrees, with the `pptx` skill for a PowerPoint file. If the user wants Quarto or Beamer, write that instead.

## Slide rules

- One finding per slide. The title is the finding, with a subject, a verb and the direction of the result ("Alberta's poverty rate was 11.0% in 2024").
- Opening slide: the main result and one anchor number. Closing slide: the synthesis from the text.
- Each figure gets a title with the measure, geography and period, and a source line with the table number.
- Keep the text on a slide to a few short lines. The speaker notes carry the detail from the article.
- Use the article's numbers, rounding and terminology exactly. Keep percent and percentage points as the article has them.
- For Government of Alberta work, use the `economic-statistics-insights` rules: neutral tone, Canadian English, no em dashes, no promotional words.
- Do not invent logos, templates or branding. If the user has a template, ask for the file.

## Output

The outline in the chat first. Then the deck file, with its path. Name anything in the source that could not be turned into a slide, such as a figure that is missing.
