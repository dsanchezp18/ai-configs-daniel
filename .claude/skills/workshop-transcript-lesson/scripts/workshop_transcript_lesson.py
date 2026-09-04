#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WHISPER_PYTHON = Path.home() / ".local/share/youtube-transcript-pdf/whisper-venv/bin/python"
DEFAULT_CSS = SKILL_ROOT / "themes/lesson-light.css"

FILLER_ONLY = re.compile(r"^(?:um+|uh+|ah+|er+|erm+|hmm+|mm+|mhm+)[,.\s-]*$", re.I)
FILLER_INLINE = re.compile(r"\b(?:um+|uh+|ah+|er+|erm+)\b[, ]*", re.I)
STUTTER = re.compile(r"\b([A-Za-z]{2,})[-\s]+\1\b", re.I)

# A small set of common ASR mishearings for coding/data-science vocabulary.
# This is intentionally not exhaustive: the lesson-writing step (a human or
# Claude reading the transcript) is expected to fix anything this misses.
ASR_FIXES = {
    r"\br\s*studio\b": "RStudio",
    r"\btidy\s*verse\b": "tidyverse",
    r"\bc\s*ran\b": "CRAN",
    r"\bgit\s*hub\b": "GitHub",
    r"\bvs\s*code\b": "VS Code",
    r"\bjupyter\b": "Jupyter",
    r"\bnode\s*js\b": "Node.js",
    r"\bggplot\s*2\b": "ggplot2",
    r"\bdply\s*r\b": "dplyr",
    r"\bpy\s*torch\b": "PyTorch",
    r"\bnum\s*py\b": "NumPy",
    r"\bpandas\b": "pandas",
}


def run(cmd: list[str], *, capture: bool = False, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            cmd,
            check=True,
            text=True,
            stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.PIPE if capture else None,
            env=env,
        )
    except subprocess.CalledProcessError as exc:
        if capture and exc.stderr:
            print(exc.stderr.strip(), file=sys.stderr)
        raise


def require_tool(name: str) -> None:
    if not shutil.which(name):
        raise SystemExit(f"missing required tool: {name}")


def require_path(path: Path, description: str) -> None:
    if not path.exists():
        raise SystemExit(f"missing {description}: {path}")


def slugify(value: str, fallback: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return value[:80] or fallback


def choose_lang(info: dict, forced: str | None) -> tuple[str, bool]:
    if forced:
        is_manual = forced in (info.get("subtitles") or {})
        return forced, is_manual

    subtitles = info.get("subtitles") or {}
    auto = info.get("automatic_captions") or {}

    manual_english = sorted(k for k in subtitles if k == "en" or k.startswith("en-"))
    if manual_english:
        return manual_english[0], True

    for candidate in ("en-orig", "en"):
        if candidate in auto:
            return candidate, False

    auto_english = sorted(k for k in auto if k == "en" or k.startswith("en-"))
    if auto_english:
        return auto_english[0], False

    raise SystemExit("no English subtitle or auto-caption track found")


def parse_timestamp(value: str) -> float:
    value = value.strip().replace(",", ".")
    parts = value.split(":")
    seconds = float(parts[-1])
    if len(parts) >= 2:
        seconds += int(parts[-2]) * 60
    if len(parts) >= 3:
        seconds += int(parts[-3]) * 3600
    return seconds


def extract_json3_events(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    events: list[dict] = []
    for event in data.get("events", []):
        text = "".join(seg.get("utf8", "") for seg in event.get("segs") or [])
        text = html.unescape(text.replace("\n", " "))
        text = re.sub(r"\s+", " ", text).strip()
        if not text or text == "\u266a":
            continue
        start = float(event.get("tStartMs") or 0) / 1000.0
        duration = float(event.get("dDurationMs") or 0) / 1000.0
        events.append({"start": start, "end": start + max(duration, 0.001), "text": text})
    return events


def extract_vtt_events(path: Path) -> list[dict]:
    events: list[dict] = []
    current_start: float | None = None
    current_end: float | None = None
    current_text: list[str] = []

    def flush() -> None:
        nonlocal current_start, current_end, current_text
        if current_start is None or current_end is None:
            current_text = []
            return
        text = " ".join(current_text)
        text = re.sub(r"<[^>]+>", "", text)
        text = html.unescape(re.sub(r"\s+", " ", text)).strip()
        if text:
            events.append({"start": current_start, "end": current_end, "text": text})
        current_start = None
        current_end = None
        current_text = []

    for raw_line in path.read_text(errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line == "WEBVTT" or line.startswith(("NOTE", "STYLE", "REGION")):
            flush()
            continue
        if "-->" in line:
            flush()
            start, end = line.split("-->", 1)
            current_start = parse_timestamp(start)
            current_end = parse_timestamp(end.split()[0])
            current_text = []
            continue
        if current_start is not None:
            current_text.append(line)
    flush()
    return events


def extract_events(subtitle_path: Path) -> list[dict]:
    if subtitle_path.suffix.lower() == ".vtt":
        return extract_vtt_events(subtitle_path)
    return extract_json3_events(subtitle_path)


def clean_text(text: str) -> str:
    text = html.unescape(text).replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    if not text or text == "\u266a" or FILLER_ONLY.fullmatch(text):
        return ""

    text = FILLER_INLINE.sub("", text)
    for pattern, replacement in ASR_FIXES.items():
        text = re.sub(pattern, replacement, text, flags=re.I)
    text = STUTTER.sub(r"\1", text)
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def group_events_into_paragraphs(events: list[dict], *, max_words: int = 110) -> list[dict]:
    paragraphs: list[dict] = []
    texts: list[str] = []
    words = 0
    start: float | None = None

    for event in events:
        if start is None:
            start = event["start"]
        texts.append(event["text"])
        words += len(event["text"].split())
        ends_sentence = bool(re.search(r'[.!?]["\')\]]*$', event["text"]))
        if (ends_sentence and words >= 40) or words >= max_words:
            paragraphs.append({"start": start, "text": " ".join(texts).strip()})
            texts, words, start = [], 0, None

    if texts:
        paragraphs.append({"start": start, "text": " ".join(texts).strip()})

    return paragraphs


def format_timestamp(seconds: float) -> str:
    total = max(0, int(seconds))
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def build_chapter_markdown(paragraphs: list[dict], chapters: list[dict]) -> str:
    if not paragraphs:
        return "No transcript content was extracted.\n"

    if chapters:
        sections: list[str] = []
        for chapter in chapters:
            start = chapter["start_time"]
            end = chapter["end_time"] if chapter["end_time"] is not None else float("inf")
            body = [p["text"] for p in paragraphs if start <= p["start"] < end]
            if not body:
                continue
            heading = f"## {chapter['title']} ({format_timestamp(start)})"
            sections.append(heading + "\n\n" + "\n\n".join(body))
        if sections:
            return "\n\n".join(sections).strip() + "\n"

    lines = ["## Full Transcript", ""]
    last_marker = -9999.0
    for paragraph in paragraphs:
        if paragraph["start"] - last_marker >= 180:
            lines.append(f"**[{format_timestamp(paragraph['start'])}]**")
            lines.append("")
            last_marker = paragraph["start"]
        lines.append(paragraph["text"])
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def download_audio(url: str, out_dir: Path) -> Path:
    output_template = str(out_dir / "audio.%(ext)s")
    run([
        "yt-dlp",
        "--no-playlist",
        "-f",
        "bestaudio/best[height<=360]/worst",
        "-x",
        "--audio-format",
        "m4a",
        "--audio-quality",
        "0",
        "-o",
        output_template,
        url,
    ])
    audio_path = out_dir / "audio.m4a"
    if audio_path.exists():
        return audio_path
    candidates = sorted(
        p for p in out_dir.glob("audio.*") if p.suffix.lower() not in {".json", ".part", ".ytdl"}
    )
    if not candidates:
        raise SystemExit("yt-dlp did not produce an audio file for Whisper transcription")
    return candidates[-1]


def download_video(url: str, out_dir: Path, format_spec: str) -> Path:
    output_template = str(out_dir / "video.%(ext)s")
    run([
        "yt-dlp",
        "--no-playlist",
        "-f",
        format_spec,
        "--merge-output-format",
        "mp4",
        "-o",
        output_template,
        url,
    ])
    candidates = sorted(
        p for p in out_dir.glob("video.*") if p.suffix.lower() not in {".json", ".part", ".ytdl"}
    )
    if not candidates:
        raise SystemExit("yt-dlp did not produce a video file")
    return candidates[-1]


def whisper_env(whisper_python: Path) -> dict[str, str]:
    import os

    env = os.environ.copy()
    site_packages = whisper_python.parent.parent / "lib" / "python3.11" / "site-packages"
    nvidia_root = site_packages / "nvidia"
    lib_dirs = sorted(nvidia_root.glob("*/lib")) if nvidia_root.exists() else []
    existing = env.get("LD_LIBRARY_PATH")
    paths = [str(path) for path in lib_dirs if path.exists()]
    if existing:
        paths.append(existing)
    if paths:
        env["LD_LIBRARY_PATH"] = ":".join(paths)
    return env


def transcribe_with_whisper(
    audio_path: Path,
    out_dir: Path,
    *,
    whisper_python: Path,
    model: str,
    device: str,
    compute_type: str,
    lang: str,
) -> list[dict]:
    require_path(whisper_python, "Whisper Python interpreter")
    transcriber = r"""
import json
import sys
from faster_whisper import WhisperModel

audio_path, model_name, device, compute_type, language = sys.argv[1:6]
model = WhisperModel(model_name, device=device, compute_type=compute_type)
segments, _ = model.transcribe(audio_path, language=language, vad_filter=True)
print(json.dumps([
    {"start": segment.start, "end": segment.end, "text": segment.text}
    for segment in segments
], ensure_ascii=False))
"""
    try:
        result = run(
            [str(whisper_python), "-c", transcriber, str(audio_path), model, device, compute_type, lang.split("-")[0]],
            capture=True,
            env=whisper_env(whisper_python),
        )
    except subprocess.CalledProcessError:
        if device != "cpu":
            result = run(
                [str(whisper_python), "-c", transcriber, str(audio_path), model, "cpu", "int8", lang.split("-")[0]],
                capture=True,
                env=whisper_env(whisper_python),
            )
        else:
            raise

    segments = json.loads(result.stdout)
    (out_dir / "whisper.raw.json").write_text(json.dumps(segments, ensure_ascii=False, indent=2), encoding="utf-8")

    events: list[dict] = []
    for segment in segments:
        text = re.sub(r"\s+", " ", str(segment.get("text") or "")).strip()
        if not text:
            continue
        start = float(segment.get("start") or 0)
        end = max(float(segment.get("end") or start), start)
        events.append({"start": start, "end": end, "text": text})
    return events


def cmd_fetch(args: argparse.Namespace) -> int:
    require_tool("yt-dlp")
    require_tool("ffmpeg")

    info = json.loads(run(["yt-dlp", "--dump-single-json", "--skip-download", args.url], capture=True).stdout)
    video_id = info.get("id") or "video"
    out_dir = Path(args.output_root).expanduser() / video_id
    out_dir.mkdir(parents=True, exist_ok=True)

    lang = args.lang or "en"
    is_manual = False
    subtitle_available = True
    try:
        lang, is_manual = choose_lang(info, args.lang)
    except SystemExit:
        if args.no_whisper:
            raise
        subtitle_available = False

    subtitle_path: Path | None = None
    if subtitle_available:
        output_template = str(out_dir / "%(title).120B [%(id)s].%(ext)s")
        subtitle_glob = [f"*.{lang}.json3", f"*.{lang}.vtt"]
        existing = sorted(
            (p for pattern in subtitle_glob for p in out_dir.glob(pattern)),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if not existing:
            cmd = ["yt-dlp", "--skip-download", "--sub-format", "json3/vtt/best", "--sub-langs", lang, "-o", output_template]
            cmd.append("--write-subs" if is_manual else "--write-auto-subs")
            cmd.append(args.url)
            try:
                run(cmd)
            except subprocess.CalledProcessError:
                if args.no_whisper:
                    raise
            existing = sorted(
                (p for pattern in subtitle_glob for p in out_dir.glob(pattern)),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
        if existing:
            subtitle_path = existing[0]

    if subtitle_path is not None:
        events = extract_events(subtitle_path)
        source = "captions"
    else:
        if args.no_whisper:
            raise SystemExit("no captions found and --no-whisper was set")
        audio_path = download_audio(args.url, out_dir)
        events = transcribe_with_whisper(
            audio_path,
            out_dir,
            whisper_python=Path(args.whisper_python).expanduser(),
            model=args.whisper_model,
            device=args.whisper_device,
            compute_type=args.whisper_compute_type,
            lang=lang,
        )
        source = "whisper"

    if not events:
        raise SystemExit("no transcript content extracted")

    raw_text = "\n".join(html.unescape(e["text"]).strip() for e in events if e["text"].strip())
    (out_dir / "raw.txt").write_text(raw_text + "\n", encoding="utf-8")

    cleaned_events: list[dict] = []
    previous_text: str | None = None
    for event in events:
        text = clean_text(event["text"])
        if not text or text == previous_text:
            continue
        cleaned_events.append({"start": event["start"], "end": event["end"], "text": text})
        previous_text = text

    paragraphs = group_events_into_paragraphs(cleaned_events)
    chapters = [
        {
            "title": str(chapter.get("title") or "Untitled section").strip(),
            "start_time": float(chapter.get("start_time") or 0.0),
            "end_time": float(chapter["end_time"]) if chapter.get("end_time") is not None else None,
        }
        for chapter in (info.get("chapters") or [])
    ]

    markdown = build_chapter_markdown(paragraphs, chapters)
    (out_dir / "transcript.by-chapter.md").write_text(markdown, encoding="utf-8")
    (out_dir / "transcript.plain.txt").write_text(
        "\n\n".join(p["text"] for p in paragraphs).strip() + "\n", encoding="utf-8"
    )

    duration_string = info.get("duration_string") or (
        format_timestamp(float(info.get("duration") or 0)) if info.get("duration") else ""
    )
    upload_date = info.get("upload_date") or ""
    if len(upload_date) == 8:
        upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"

    video_path: Path | None = None
    if args.download_video:
        video_path = download_video(args.url, out_dir, args.video_format)

    meta = {
        "video_id": video_id,
        "title": info.get("title") or "Untitled video",
        "uploader": info.get("uploader") or "Unknown uploader",
        "url": info.get("webpage_url") or info.get("original_url") or args.url,
        "duration_seconds": info.get("duration"),
        "duration_string": duration_string,
        "upload_date": upload_date,
        "lang": lang,
        "transcript_source": source,
        "chapters": chapters,
        "video_file": video_path.name if video_path else None,
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    result = {
        "out_dir": str(out_dir.resolve()),
        "meta": str((out_dir / "meta.json").resolve()),
        "raw_txt": str((out_dir / "raw.txt").resolve()),
        "transcript_by_chapter_md": str((out_dir / "transcript.by-chapter.md").resolve()),
        "transcript_plain_txt": str((out_dir / "transcript.plain.txt").resolve()),
    }
    if video_path is not None:
        result["video"] = str(video_path.resolve())
    print(json.dumps(result, indent=2))
    return 0


def find_chrome() -> str:
    for candidate in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge"):
        path = shutil.which(candidate)
        if path:
            return path
    for candidate in (
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ):
        if Path(candidate).exists():
            return candidate
    raise SystemExit("Chrome/Chromium/Edge not found; install one to render the PDF")


def cmd_render(args: argparse.Namespace) -> int:
    require_tool("pandoc")
    chrome = find_chrome()

    md_path = Path(args.lesson_markdown).expanduser().resolve()
    if not md_path.exists():
        raise SystemExit(f"lesson Markdown not found: {md_path}")
    css_path = Path(args.css).expanduser().resolve()
    if not css_path.exists():
        raise SystemExit(f"CSS theme not found: {css_path}")

    out_pdf = Path(args.output).expanduser().resolve() if args.output else md_path.with_suffix(".pdf")
    html_path = out_pdf.with_suffix(".html")
    css_out = out_pdf.parent / css_path.name
    shutil.copy2(css_path, css_out)

    pandoc_cmd = [
        "pandoc",
        str(md_path),
        "--standalone",
        "--css",
        css_out.name,
        "--highlight-style",
        "pygments",
    ]
    if args.title:
        pandoc_cmd.extend(["--metadata", f"pagetitle={args.title}"])
    if not args.no_toc:
        pandoc_cmd.extend(["--toc", "--toc-depth=2"])
    pandoc_cmd.extend(["-o", str(html_path)])
    run(pandoc_cmd)

    run([
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={out_pdf}",
        html_path.resolve().as_uri(),
    ])

    if not out_pdf.exists() or out_pdf.stat().st_size == 0:
        raise SystemExit("PDF rendering failed: output file is missing or empty")

    print(json.dumps({"html": str(html_path), "pdf": str(out_pdf)}, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch a workshop video transcript, then render a Claude-authored lesson Markdown file to PDF."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    fetch_parser = subparsers.add_parser("fetch", help="Download and lightly clean a transcript.")
    fetch_parser.add_argument("url")
    fetch_parser.add_argument("--output-root", default="workshop-lessons")
    fetch_parser.add_argument("--lang")
    fetch_parser.add_argument("--no-whisper", action="store_true", help="Fail instead of falling back to local Whisper.")
    fetch_parser.add_argument("--whisper-python", default=str(DEFAULT_WHISPER_PYTHON))
    fetch_parser.add_argument("--whisper-model", default="large-v3")
    fetch_parser.add_argument("--whisper-device", default="cuda")
    fetch_parser.add_argument("--whisper-compute-type", default="int8_float16")
    fetch_parser.add_argument(
        "--download-video",
        action="store_true",
        help="Also download the full video file with yt-dlp (not just captions/audio). Off by default.",
    )
    fetch_parser.add_argument(
        "--video-format",
        default="bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
        help="yt-dlp format selector used with --download-video.",
    )
    fetch_parser.set_defaults(func=cmd_fetch)

    render_parser = subparsers.add_parser("render", help="Render an authored lesson Markdown file to PDF.")
    render_parser.add_argument("lesson_markdown")
    render_parser.add_argument("--output", help="Output PDF path. Default: same stem as the input, .pdf.")
    render_parser.add_argument("--css", default=str(DEFAULT_CSS))
    render_parser.add_argument("--title", help="Override the document title metadata.")
    render_parser.add_argument("--no-toc", action="store_true")
    render_parser.set_defaults(func=cmd_render)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
