"""Create teleprompter documents from the spoken-script sections."""
import sys
sys.dont_write_bytecode = True
import argparse
import re
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from build_pptx import people, sections, plain, VARIANTS


def build(folder, variant='full'):
    md_suffix, out_suffix = VARIANTS[variant]
    path = folder / f'01_SCRIPT_EN{md_suffix}.md'
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.top_margin = sec.bottom_margin = sec.left_margin = sec.right_margin = Cm(2)
    normal = doc.styles['Normal']
    normal.font.name, normal.font.size = 'Calibri', Pt(16)
    normal.paragraph_format.line_spacing = 1.4
    normal.paragraph_format.space_after = Pt(10)
    doc.add_heading(path.read_text(encoding='utf-8-sig').splitlines()[0].lstrip('# '), 0)
    words = []
    for heading, body in sections(path):
        p = doc.add_heading(heading, 1)
        p.paragraph_format.keep_with_next = True
        for r in p.runs:
            r.font.name, r.font.size, r.font.bold = 'Calibri', Pt(17), True
            r.font.color.rgb = RGBColor.from_string('0F172A')
        for block in re.split(r'\n\s*\n', body):
            # A direction remains a separate paragraph even without a blank line.
            for part in re.split(r'(?m)(?=^>)|(?<=\n)(?!>)', block) if block.startswith('>') else [block]:
                if not part.strip():
                    continue
                stage = part.startswith('>')
                text = re.sub(r'(?m)^>\s*', '', part).strip() if stage else part.strip()
                if not stage:
                    words.extend(re.findall(r"\b[\w]+(?:['’−.-][\w]+)*\b", plain(text)))
                p = doc.add_paragraph()
                for token in re.split(r'(`[^`]+`|\*[^*]+\*|\[tự điền:[^\]]*\])', text):
                    code, emphasis = token.startswith('`'), token.startswith('*')
                    r = p.add_run(token[1:-1] if code or emphasis else token)
                    r.font.name, r.font.size = 'Consolas' if code else 'Calibri', Pt(12 if stage else 16)
                    r.italic = stage or emphasis
                    r.font.color.rgb = RGBColor.from_string('D97706' if token.startswith('[tự điền:') else ('64748B' if stage else '0F172A'))
    duration = len(words) / 140
    doc.add_paragraph(f'Spoken word count: {len(words):,} · Estimated duration at 140 wpm: {int(duration)}:{round(duration % 1 * 60):02d}')
    out = folder / 'output' / f'{folder.name[:7]}_script{out_suffix}.docx'
    out.parent.mkdir(exist_ok=True)
    doc.save(out)
    assert len(Document(out).paragraphs) == len(doc.paragraphs)
    print(f'{out} — {len(words)} words, {duration:.2f} minutes')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--person', choices=['1', '2', '3'])
    parser.add_argument('--variant', choices=['full', '5min', 'all'], default='all')
    args = parser.parse_args()
    variants = ['full', '5min'] if args.variant == 'all' else [args.variant]
    for folder in people(args.person):
        for v in variants:
            if (folder / f'01_SCRIPT_EN{VARIANTS[v][0]}.md').is_file():
                build(folder, v)
