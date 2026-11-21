# Codex task B — build PPTX decks, teleprompter DOCX, previews and number check

You are working in the repository root `c:\Users\Admin\Desktop\MLA` (Windows 11; `python` = Python 3.14 with python-pptx 1.0.2, python-docx, pandas, pywin32, PyMuPDF installed; Microsoft PowerPoint and Word are installed). Read `VIDEO_CA_NHAN/README.md` and `VIDEO_CA_NHAN/_chung/STYLE.md` first — STYLE.md defines the design and the exact formats of `02_SLIDE_SPEC.md` and `01_SCRIPT_EN.md`. Look at `build_editable_pptx.py` (repo root) for the palette and python-pptx helpers already used by this group.

The three person folders are `VIDEO_CA_NHAN/Nguoi_1_Data_Classical_Length`, `VIDEO_CA_NHAN/Nguoi_2_DeBERTa_Context_Threshold`, `VIDEO_CA_NHAN/Nguoi_3_TestGovernance_LOPO_Ladder`. Another worker is generating the PNGs in each `visuals/` folder and `_chung/visuals/` in parallel; some may not exist yet while you work.

## Hard rules

- Write ONLY: `VIDEO_CA_NHAN/build/build_pptx.py`, `VIDEO_CA_NHAN/build/build_script_docx.py`, `VIDEO_CA_NHAN/build/render_preview.ps1`, `VIDEO_CA_NHAN/build/check_numbers.py`, and generated files under `VIDEO_CA_NHAN/Nguoi_*/output/`. Do not edit any .md file, `visuals/`, `demo/`, `MLA_Final/` or `final_report/`. Do not git commit.
- Do not invent content: slide text comes only from `02_SLIDE_SPEC.md`; notes and teleprompter text only from `01_SCRIPT_EN.md`.

## 1. `build_pptx.py`

- Parses each person's `02_SLIDE_SPEC.md` (`## Slide <n> | <layout>` blocks; keys `title`, `subtitle`, `bullets:` list, `image`, `caption`, `callout`, `source`, `table:` followed by a markdown table) and the `Role footer:` line at the top.
- Parses `01_SCRIPT_EN.md`: sections `## [SLIDE n] …` and `## [DEMO] …`. Speaker notes of slide n = the heading's timecode + spoken paragraphs; stage-direction lines starting with `>` go into the notes in square brackets prefixed "DO:". The `[DEMO]` section goes into the notes of the slide whose layout is `demo`, appended after that slide's own section.
- 16:9 (13.333 × 7.5 in). Layouts as in STYLE.md: `title`, `bullets`, `bullets_image`, `image`, `table`, `demo`. Design: light background #F8FAFC, a navy title band or strong navy title text, blue accent bar, body Calibri ≥ 20 pt (bullets 20–24 pt; reduce to no less than 18 pt only if text would overflow), titles Trebuchet MS 32–36 pt bold, caption ≥ 14 pt grey italic, source 12 pt grey at the bottom, callout in a rounded rectangle (light blue fill #EFF6FF with blue border, or orange #FFF7ED/#D97706 when the text starts with "Limitation"), footer "Group 06 · CLC02 · <role> · n/9" bottom right. `title` layout: big title, subtitle, the bullets as presenter lines, navy left panel or similar strong design. `demo` layout: a dark navy slide with a "LIVE DEMO" tag and numbered steps in monospace (Consolas) ≥ 20 pt. `table` layout: real PowerPoint table, header row navy with white text, ≥ 18 pt, numeric columns right-aligned, zebra rows; then the callout.
- Images: keep aspect ratio, fit inside the allotted box (≥ 55% of slide width for `bullets_image`, nearly full slide for `image`), centred. If an image file is missing, draw a dashed placeholder box with the expected filename (and print a warning) — never crash.
- Long `[tự điền: …]` placeholders stay visible (they are for the speaker to fill in); highlight them in orange.
- Output: `VIDEO_CA_NHAN/Nguoi_N_…/output/Nguoi_N_slides.pptx` (N = 1, 2, 3). Accept `--person 1|2|3` (default all).

## 2. `build_script_docx.py`

- From each `01_SCRIPT_EN.md` produce `output/Nguoi_N_script.docx`: A4 portrait, margins 2 cm, title line, then each section: heading with the cue and timecode in bold (e.g. "[SLIDE 4] 1:15–2:45 — One real unit…"), spoken text 16 pt Calibri with 1.4 line spacing, stage directions italic grey 12 pt. At the end, a word count and an estimated duration at 140 wpm. Markdown emphasis (`*text*`) → italic; inline code → Consolas.

## 3. `render_preview.ps1`

- Uses PowerPoint COM to export every slide of each `output/Nguoi_N_slides.pptx` to `output/preview/slide_XX.png` at 1920×1080 (`Slide.Export(path, "PNG", 1920, 1080)`), opening presentations read-only and without a window, then quits PowerPoint. Paths must be absolute (resolve from the script's location).

## 4. `check_numbers.py`

- For each person, extract every number token (e.g. `0.577`, `−0.092`, `19.3%`, `144,289`, `[0.016, 0.035]`) from `01_SCRIPT_EN.md` and `02_SLIDE_SPEC.md` (ignore timecodes like `1:15`, slide numbers, ordinal words, year 2026, and dates). Build a set of "known values" by reading every CSV in `MLA_Final/Results/tables/`, `MLA_Final/Results/predictions/context_levels_10_cases.csv`, the JSON configs in `MLA_Final/Code/configs/`, plus the text of `final_report/report_src/*.md` (numbers appearing there are accepted), plus `VAN_DAP_4_TIEU_CHI/trace_mau_that/outputs/*.csv` if present. Treat a number as verified if it matches a known value after rounding to its displayed precision (also accept percentage ↔ fraction, and thousands separators). Print a per-person table of unverified numbers with their line, and exit code 0 (it is a report, not a gate). Numbers computed only by demo scripts (e.g. recall by length quartile) will appear as unverified; that is expected — list them separately if they appear in the runbook's expected output.

## 5. Run and verify

- Run `python VIDEO_CA_NHAN/build/build_pptx.py`, `python VIDEO_CA_NHAN/build/build_script_docx.py`, `powershell -ExecutionPolicy Bypass -File VIDEO_CA_NHAN/build/render_preview.ps1`, `python VIDEO_CA_NHAN/build/check_numbers.py`.
- Open several preview PNGs (as images) and fix layout problems: text overflowing a box or the slide, overlapping shapes, tiny fonts, distorted images. Iterate until every slide of all three decks is clean (images may still be placeholders if the other worker has not finished).
- Final message: files written, any warnings, the check_numbers report, and a short description of each deck's layout.
