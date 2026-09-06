---
name: workshop-transcript-lesson
description: "Turn a coding workshop or tutorial video, from YouTube or a local video/audio file, into a standalone pedagogical study guide with an audited transcript, explained concepts, verified code, and a rendered PDF."
---

# Workshop Transcript Lesson

Use when the user gives a coding workshop, tutorial, or lecture — a YouTube link or a local
video/audio file — and wants something to study from. The primary deliverable is a standalone
lesson, not a transcript with headings: a reader who never watches the recording should be able
to understand the central idea, follow the demonstrated workflow, and know where its limits are.
Include practice exercises only when the user explicitly asks for them.

This is a two-stage skill and the stages are not interchangeable:

1. The script fetches and lightly cleans the transcript. This step does no teaching.
2. The model builds a concept-first teaching map, verifies ambiguous details against available
   project materials, and writes the lesson. This is the actual work of the skill.
3. The script or the selected document tool renders the finished lesson source to PDF.
4. The final PDF, source, transcript, and source metadata are checked as a set.

Never treat step 1's output as the deliverable. A cleaned transcript is not a lesson.

## Pedagogical contract

The lesson must add value beyond the recording's chronology. Before writing prose, identify the
dependency order of the ideas and build a short teaching map with these fields: concept, why it
matters, prerequisite, exact example or code, expected result, pitfall, and evidence source
(transcript timestamp or project file). Use that map to reorganise the material when the speaker's
presentation order is driven by greetings, polls, breaks, screen-sharing logistics, debugging
chatter, or audience questions.

For every important topic, use this teaching sequence where the material supports it:

1. **Motivation:** state the problem and why the reader should care.
2. **Mental model:** explain the mechanism in plain language before showing syntax.
3. **Worked example:** show a minimal, coherent code path with correct names and imports.
4. **Interpretation:** explain what the code does, what result to expect, and where computation
   occurs.
5. **Boundary:** state when the approach fails, becomes unsafe, or should be replaced.
6. **Takeaway:** close with one practical rule the reader can reuse.

Do not turn every timestamp or speaker transition into a section. Compress repetition and event
logistics. Keep questions only when they expose a genuine misconception or an important boundary.
Prefer fewer, well-explained examples over a catalogue of commands.

### Filling gaps without inventing content

The transcript is evidence about what the instructor covered, not a complete textbook. Add short
bridge explanations when the reader needs them to understand a demonstrated step: define a term,
explain why an operation is lazy, connect two code blocks, or state a prerequisite that the speaker
assumed. These bridges may use stable technical knowledge or the supplied project documentation,
but they must not introduce unrelated tools, unsupported claims, or a new workflow.

When the speaker's code is ambiguous, use this evidence order:

1. Exact code in the supplied workshop repository or project files.
2. The transcript's surrounding explanation and later references to the same object.
3. Authoritative documentation for the named package or tool, only to repair essential syntax.
4. A clearly labelled reconstruction when uncertainty remains.

Never silently convert an uncertain ASR fragment into authoritative-looking code. Say briefly when
code was reconstructed, and preserve the raw and cleaned transcript for audit.

## Step 1 — Fetch

```bash
python3 scripts/workshop_transcript_lesson.py fetch "https://youtu.be/..."
python3 scripts/workshop_transcript_lesson.py fetch "C:\path\to\workshop.mp4"
```

The `fetch` command accepts either a YouTube URL or a path to a local video/audio file — it
checks whether the argument is an existing local path first, and routes accordingly.

**YouTube URL:** downloads the best available English captions (preferring human captions
over auto-captions), falling back to local `faster-whisper` transcription if the video has no
captions at all. Chapters, if the video defines any, come from YouTube's own chapter list.

**Local file:** always transcribes with local `faster-whisper` (a local file has no YouTube
captions to fetch), passing the file straight to Whisper — no separate audio-extraction step
needed. Chapters, if any, are read from the file's own embedded chapter metadata via
`ffprobe`; most workshop recordings won't have any, in which case the fallback is periodic
timestamp markers just like the YouTube path. `--no-whisper` is rejected here since it isn't
meaningful for a local file.

Either way, it writes to `workshop-lessons/<video_id>/`:

- `meta.json` — title, uploader (`"Local file"` for local input), source URL/path, duration,
  upload date (empty for local input), and the chapter list if there is one.
- `raw.txt` — verbatim caption/Whisper text, kept for audit only.
- `transcript.by-chapter.md` — the input for step 2. Segmented by chapters when present,
  otherwise by a timestamp marker roughly every 3 minutes. Cleaned only enough to be readable:
  filler words and duplicate stutters removed, a handful of common ASR misspellings fixed
  (RStudio, tidyverse, CRAN, GitHub, ggplot2, dplyr, and similar). It is NOT paraphrased,
  restructured, or fact-checked — auto-captions and Whisper output on tutorial videos are
  usually unpunctuated and frequently mangle package/function names, so expect to fix more of
  that yourself while writing the lesson.
- `transcript.plain.txt` — the same content flattened, no chapter headings.

Useful flags:

- `--output-root PATH` — default `workshop-lessons`.
- `--lang LANG` — force a caption/transcription language instead of auto-selecting (YouTube
  path) or the `en` default (local-file path).
- `--no-whisper` — fail instead of transcribing locally when no YouTube captions exist.
  Rejected outright for a local file, since local input has no other transcript source.
- `--whisper-model/--whisper-device/--whisper-compute-type/--whisper-python` — same meaning as
  in the `youtube-transcript-pdf` skill. The default Whisper interpreter path is shared with
  that skill (`~/.local/share/youtube-transcript-pdf/whisper-venv/bin/python`) — no separate
  environment to set up.
- `--download-video` — YouTube input only. Also downloads the full video file with `yt-dlp`
  into `workshop-lessons/<video_id>/video.<ext>`. Off by default; the transcript/lesson
  workflow doesn't need it. Use it when the user wants a local copy of the source video, or
  when you want to eyeball on-screen code that the transcript reconstructs ambiguously. A
  no-op for local-file input, which already has the video on disk.
- `--video-format` — yt-dlp format selector used with `--download-video`. Default:
  `bestvideo[height<=1080]+bestaudio/best[height<=1080]/best`.

## Step 2 — Write the lesson

### Source hierarchy and authoring pass

When a repository, project folder, slides, or notebook is supplied or mentioned in the recording,
inspect it before authoring. Use project files for exact package names, function names, paths,
object names, and runnable code; use the transcript for what the instructor actually explains,
demonstrates, recommends, or warns about; and use authoritative documentation only to repair an
essential missing definition or syntax detail. Record any such documentation link in the source
notes.

Use two passes. First build the teaching map: group transcript evidence into concepts and
dependencies, marking repeated narration, logistics, Q&A, uncertain ASR, and exact code found in
project files. Then write the lesson from that map rather than paraphrasing timestamp blocks.
After drafting, check that each important section explains purpose, mechanism, code,
interpretation, and limits.

Read `transcript.by-chapter.md` and `meta.json`, then write `lesson.qmd` yourself in the same
`workshop-lessons/<video_id>/` directory when the user requests LaTeX, mathematical notation,
or a Quarto source. Use `lesson.md` only when a plain Markdown source is more appropriate.
Ground every claim in what the video actually
covers — do not invent tools, packages, or steps it doesn't show. When the transcript is
ambiguous about exact syntax (very common with spoken code — a narrator says "then we pipe
into filter" without saying whether it's `|>` or `%>%`), reconstruct the most likely code
from context and say so briefly rather than presenting a guess as verbatim transcription.

### Compact and LaTeX mode

When the user requests a short guide or a page limit, treat the limit as a real design constraint.
For a maximum of 10 pages, cut greetings, polls, repeated demonstrations, breaks, and routine
troubleshooting before shrinking type or margins. Keep the minimum conceptual explanation needed
to make each retained example meaningful. Prefer one coherent worked example per major idea,
annotated code, one compact cheat sheet, and no exercises unless explicitly requested.

When the user requests mathematical expressions and code in a PDF, prefer a `.qmd` source and
XeLaTeX or LuaLaTeX rather than the HTML-to-PDF path. Use UTF-8 directly; do not transliterate
Spanish accents or mathematical symbols. Set an explicit, widely available text font and a
monospace font for code (for example Latin Modern Roman and Latin Modern Mono in TeX Live).
If a user-provided project contains a font or LaTeX template, inspect it and reuse it when
available; never invent a missing project path or font name. Keep the cleaned transcript as a
separate output file such as `transcript.cleaned.md` or `transcript.by-chapter.md`; do not
append the full transcript to a compact guide unless the user explicitly wants it embedded.

Start with YAML front matter:

```markdown
---
title: "<a clear teaching title — clean up a clickbait video title>"
subtitle: "Workshop Lesson Guide"
author: "<uploader>"
date: "<upload date>"
---
```

Then, in this order:

1. **Overview** — 2-4 sentences: what this teaches and why it matters.
2. **Learning objectives** — a short bulleted list of what the reader should be able to do
   afterward.
3. **Prerequisites** — packages/versions/tools and prior knowledge the video assumes.
4. **Guided workflow** — organise sections by concept and dependency, using the video's chapter
   structure only when it forms a useful conceptual sequence. Each
   section gets:
   - A plain-language explanation in your own words, not a paraphrase of the narration.
   - Fenced code blocks with the correct language tag (` ```r `, ` ```python `, etc.) for
     anything demonstrated, reconstructed as described above.
   - A callout for anything the instructor flags as a gotcha, best practice, or common
     mistake — see "Callouts" below.
5. **Cheat sheet** — a compact table or list of every function/command introduced, one line
   each: name, what it does, minimal example.
6. **Practice exercises** — include 2-5 exercises only when requested. Put solutions in their
   own `### Solutions` section at the very end, never inline, so they don't spoil the exercise.
7. **Further resources** — only tools/packages/links the video itself mentions. Do not invent
   external references.

### Lesson quality checks

Before rendering, ask:

- Could a reader understand why the workflow exists before seeing the first command?
- Does every retained code block have a purpose, an explanation, and an expected result?
- Are the transitions between concepts explicit, especially where the speaker moved quickly?
- Are limits, failure modes, and safe materialisation points stated?
- Were names and syntax checked against project files rather than copied from uncertain ASR?
- Did the lesson remove event logistics and repeated narration instead of merely shortening them?

### Callouts

Use Pandoc fenced divs, not raw HTML — the render theme styles these classes:

```markdown
::: {.callout-tip}
Prefer `dplyr::filter()` over subsetting with `[` for readability in a pipeline.
:::

::: {.callout-warning}
`ggplot2` layers apply in the order they're added — a `geom_smooth()` before `geom_point()`
will be drawn underneath it.
:::

::: {.callout-note}
The video uses R 4.3; syntax may differ slightly on older versions.
:::

::: {.callout-exercise}
Recreate the scatter plot from this section using the `mpg` dataset instead of `mtcars`.
:::
```

## Step 3 — Render

```bash
python3 scripts/workshop_transcript_lesson.py render workshop-lessons/<video_id>/lesson.md
```

The HTML path writes `lesson.pdf` (and an intermediate `lesson.html`) beside the input by
default. For a Quarto/LaTeX deliverable, render the QMD source with the available Quarto
installation or call Pandoc directly:

```bash
quarto render workshop-lessons/<video_id>/lesson.qmd --to pdf --pdf-engine=xelatex
```

If Quarto is unavailable but Pandoc and XeLaTeX are installed:

```bash
pandoc workshop-lessons/<video_id>/lesson.qmd \
  --from markdown \
  --pdf-engine=xelatex \
  -V geometry:margin=0.7in \
  -V mainfont="Latin Modern Roman" \
  -V sansfont="Latin Modern Sans" \
  -V monofont="Latin Modern Mono" \
  -o workshop-lessons/<video_id>/lesson.pdf
```

Use `pdflatex` only when the document's encoding and font setup require it; XeLaTeX or
LuaLaTeX is the default for UTF-8 Spanish text, Unicode mathematics, and mixed code. The
LaTeX path must produce a nonzero `lesson.pdf`; use `pdfinfo` to record the page count and
keep the result within the requested limit when a page limit was specified.

For formal guides, honour requested layout settings such as normal one-inch margins and 1.5 line
spacing. Keep code blocks, tables, and callouts together where possible. If the page budget is
exceeded, revise the lesson for clarity and density first; do not silently reduce the requested
font size, margins, or line spacing.

Flags:

- `--output PATH` — override the PDF path.
- `--css PATH` — default `themes/lesson-light.css` in this skill: a clean, textbook-style
  sans-serif theme with a table of contents, syntax-highlighted code blocks, and colored
  callout boxes. Pass a different CSS file for a different look.
- `--title TEXT` — override the document title metadata; normally unnecessary since the
  lesson's own YAML `title:` is used.
- `--no-toc` — omit the table of contents (for a short, single-section lesson).

## Completion gate

Do not report this skill as done until:

- The guide is recognisably more useful than the transcript: it has a concept-first arc, bridge
  explanations, interpreted examples, and explicit boundaries.
- Any supplied repository or project materials were inspected before finalising code and terminology;
  reconstructed details are identified rather than silently asserted.
- The source metadata identifies whether the transcript came from captions, local Whisper, or a
  user-supplied transcript, and the cleaned transcript remains separate for audit.

- `lesson.md` or `lesson.qmd` reflects real authored content — objectives, explained sections,
  and a cheat sheet, with exercises only when requested — not a copy-pasted or lightly-
  reformatted transcript.
- `lesson.pdf` exists, has nonzero size, and `pdfinfo` reports a page count.
- The cleaned transcript is retained as a separate output file when requested or useful for
  audit, typically `transcript.by-chapter.md` and/or `transcript.cleaned.md`.
- If LaTeX output was requested, the final PDF is rendered from the QMD/LaTeX path and its
  pages are visually inspected for clipped text, broken math, unreadable code, or font
  substitution.
- Report the PDF path first, then `lesson.md`.
- If the request came from chat and the user expects the deliverable there, attach the PDF.

## Multi-speaker videos

This skill does not diarize. A panel, interview, or Q&A-heavy workshop will come back as one
undifferentiated transcript stream — still usable for writing a lesson, but don't expect
per-speaker attribution. Use the `youtube-transcript-pdf` skill instead if speaker-labeled
transcript output is what's actually needed.
