"""Build editable decks directly from the slide specs and scripts."""
import argparse
import re
from pathlib import Path

from PIL import Image, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
BG, NAVY, BLUE, GRAY, WHITE, ORANGE = 'F8FAFC', '0F172A', '2563EB', '64748B', 'FFFFFF', 'D97706'


def people(person=None):
    return sorted(ROOT.glob(f'Nguoi_{person or "*"}_*'))


def sections(path):
    text = path.read_text(encoding='utf-8-sig')
    matches = list(re.finditer(r'^## (\[(?:SLIDE \d+|DEMO)\].*)$', text, re.M))
    return [(m[1], text[m.end():matches[i+1].start() if i+1 < len(matches) else len(text)].strip())
            for i, m in enumerate(matches)]


def parse_spec(path):
    text = path.read_text(encoding='utf-8-sig')
    footer = re.search(r'^Role footer:\s*(.+)$', text, re.M)[1].strip('` ')
    slides = []
    for part in re.split(r'^## Slide ', text, flags=re.M)[1:]:
        heading, *lines = part.splitlines()
        num, layout = heading.split('|')
        item = dict(number=int(num), layout=layout.strip(), bullets=[], table=[])
        mode = None
        for line in lines:
            key = re.match(r'^(title|subtitle|bullets|image|caption|callout|source|table):\s*(.*)', line)
            if key:
                mode = key[1]
                if mode not in ('bullets', 'table'):
                    item[mode] = key[2]
            elif mode == 'bullets' and line.startswith('- '):
                item['bullets'].append(line[2:])
            elif mode == 'table' and line.startswith('|'):
                cells = [c.strip() for c in line.strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', c) for c in cells):
                    item['table'].append(cells)
        assert item['layout'] in {'title', 'bullets', 'bullets_image', 'image', 'table', 'demo'}
        slides.append(item)
    assert [s['number'] for s in slides] == list(range(1, len(slides) + 1)), path
    return footer, slides


def plain(text):
    return re.sub(r'`([^`]+)`|\*([^*]+)\*', lambda m: m[1] or m[2], text)


def notes(heading, body):
    lines = [heading]
    for line in body.splitlines():
        lines.append('[DO: ' + plain(line[1:].strip()) + ']' if line.startswith('>') else plain(line))
    return '\n'.join(lines)


def rect(slide, x, y, w, h, fill, border=None, rounded=False):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
                                   Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor.from_string(fill)
    if border:
        shape.line.color.rgb = RGBColor.from_string(border)
    else:
        shape.line.fill.background()
    return shape


def measured_height(lines, size, width, font='Calibri', gap=10):
    filename = {'Calibri': 'calibri.ttf', 'Trebuchet MS': 'trebucbd.ttf', 'Consolas': 'consola.ttf'}[font]
    face = ImageFont.truetype(str(Path('C:/Windows/Fonts') / filename), size * 2)
    count = 0
    for line in lines:
        used, rows = 0, 1
        for word in plain(line).split():
            length = face.getlength(word + ' ')
            if used and used + length > width * 144:
                rows += 1
                used = 0
            used += length
        count += rows
    return (count * size * 1.18 + max(0, len(lines)-1) * gap) / 72


def textbox(slide, text, x, y, w, h, size=22, color=NAVY, font='Calibri', bold=False,
            italic=False, align=None, minimum=None, gap=10):
    lines = text if isinstance(text, list) else [text]
    while minimum and size > minimum and measured_height(lines, size, w, font, gap) > h:
        size -= 1
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap if i+1 < len(lines) else 0)
        p.line_spacing = 1.08
        if align is not None:
            p.alignment = align
        for chunk in re.split(r'(\[tự điền:[^\]]*\])', plain(line)):
            run = p.add_run()
            run.text = chunk
            run.font.name, run.font.size = font, Pt(size)
            run.font.bold, run.font.italic = bold, italic
            run.font.color.rgb = RGBColor.from_string(ORANGE if chunk.startswith('[tự điền:') else color)
    return shape


def picture(slide, path, x, y, w, h):
    if not path.is_file():
        shape = rect(slide, x, y, w, h, 'EFF6FF', BLUE)
        shape.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        textbox(slide, path.name, x+.2, y+h/2-.45, w-.4, .9, size=20)
        print(f'WARNING: missing image {path}')
        return
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(w/iw, h/ih)
    dw, dh = iw*scale, ih*scale
    slide.shapes.add_picture(str(path), Inches(x+(w-dw)/2), Inches(y+(h-dh)/2),
                             width=Inches(dw), height=Inches(dh))


VARIANTS = {'full': ('', ''), '5min': ('_5MIN', '_5min')}


def build(folder, variant='full'):
    md_suffix, out_suffix = VARIANTS[variant]
    footer, spec = parse_spec(folder / f'02_SLIDE_SPEC{md_suffix}.md')
    script = sections(folder / f'01_SCRIPT_EN{md_suffix}.md')
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    for s in spec:
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        layout = s['layout']
        dark = layout == 'demo'
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = RGBColor.from_string(NAVY if dark else BG)
        rect(slide, .45, .35, .12, .65, BLUE)
        title_color = WHITE if dark else NAVY
        if layout == 'title':
            rect(slide, 0, 0, 1.25, 7.5, NAVY)
            rect(slide, 1.25, 1.05, .12, 5.05, BLUE)
            textbox(slide, s['title'], 1.85, 1.0, 10.7, 1.9, 36, font='Trebuchet MS', bold=True)
            textbox(slide, s.get('subtitle', ''), 1.85, 3.1, 10.6, 1.0, 24, color=GRAY)
            textbox(slide, s['bullets'], 1.85, 4.6, 10.6, 1.5, 24, minimum=20)
        else:
            textbox(slide, s['title'], .75, .38, 11.9, .62, 34, color=title_color,
                    font='Trebuchet MS', bold=True, minimum=26)
            top = 1.45
            if s.get('subtitle'):
                textbox(slide, s['subtitle'], .75, 1.5, 11.9, .65, 20, color=GRAY)
                top = 2.25
            bottom = 5.55 if s.get('callout') else 6.35
            if layout == 'bullets_image':
                textbox(slide, ['• ' + b for b in s['bullets']], .55, top, 4.45, bottom-top,
                        22, minimum=18, gap=14)
                picture(slide, folder / s['image'], 5.25, top, 7.48, bottom-top-.55)
                textbox(slide, s.get('caption', ''), 5.25, bottom-.45, 7.48, .5, 14, color=GRAY, italic=True)
            elif layout == 'image':
                if s.get('callout'):
                    picture(slide, folder / s['image'], .45, 1.2, 9.05, 5.0)
                    textbox(slide, s.get('caption', ''), .55, 6.22, 8.85, .4, 14, color=GRAY, italic=True, minimum=12)
                    warning = s['callout'].startswith('Limitation')
                    rect(slide, 9.7, 1.75, 3.2, 3.6, 'FFF7ED' if warning else 'EFF6FF', ORANGE if warning else BLUE, True)
                    textbox(slide, s['callout'], 9.9, 1.95, 2.8, 3.2, 22, minimum=16, gap=0)
                else:
                    picture(slide, folder / s['image'], .45, 1.2, 12.43, 5.0)
                    textbox(slide, s.get('caption', ''), .65, 6.22, 12.0, .4, 14, color=GRAY, italic=True, minimum=12)
            elif layout == 'bullets':
                textbox(slide, ['• ' + b for b in s['bullets']], .8, top, 11.7, bottom-top-.2, 24, minimum=18, gap=16)
            elif layout == 'demo':
                textbox(slide, 'LIVE DEMO', .8, 1.65, 11.7, .45, 20, color='60A5FA', bold=True)
                textbox(slide, [f'{i}. {b}' for i, b in enumerate(s['bullets'], 1)],
                        .8, 2.4, 11.7, 4.05, 23, WHITE, 'Consolas', minimum=20, gap=22)
            elif layout == 'table':
                rows = s['table']
                table = slide.shapes.add_table(len(rows), len(rows[0]), Inches(.65), Inches(top),
                                               Inches(12.03), Inches(3.5)).table
                widths = {2: [7.4, 4.63], 3: [6.03, 3, 3], 5: [3.35, 2.05, 1.55, 1.4, 3.68]}[len(rows[0])]
                for j, width in enumerate(widths):
                    table.columns[j].width = Inches(width)
                for i, row in enumerate(rows):
                    for j, value in enumerate(row):
                        cell = table.cell(i, j)
                        cell.text = value
                        cell.margin_left = cell.margin_right = Inches(.12)
                        cell.margin_top = cell.margin_bottom = Inches(.07)
                        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                        cell.fill.solid()
                        cell.fill.fore_color.rgb = RGBColor.from_string(NAVY if i == 0 else ('EFF6FF' if i % 2 else WHITE))
                        for p in cell.text_frame.paragraphs:
                            p.alignment = PP_ALIGN.RIGHT if j and i else PP_ALIGN.LEFT
                            for r in p.runs:
                                r.font.name, r.font.size = 'Calibri', Pt(18 if len(row) == 5 else 20)
                                r.font.bold = i == 0
                                r.font.color.rgb = RGBColor.from_string(WHITE if i == 0 else NAVY)
            if s.get('callout') and layout != 'image':
                warning = s['callout'].startswith('Limitation')
                rect(slide, .65, 5.7, 12.03, .83, 'FFF7ED' if warning else 'EFF6FF', ORANGE if warning else BLUE, True)
                textbox(slide, s['callout'], .85, 5.82, 11.63, .62, 21, minimum=18, gap=0)
        if s.get('source'):
            textbox(slide, s['source'], .65, 6.62, 12.03, .42, 12, color=GRAY, gap=0)
        textbox(slide, f'{footer} · {s["number"]}/{len(spec)}', 1.4, 7.12, 11.28, .24, 12,
                color='94A3B8' if dark else GRAY, align=PP_ALIGN.RIGHT)
        matching = [(h, b) for h, b in script if h.startswith(f'[SLIDE {s["number"]}]') or
                    (layout == 'demo' and h.startswith('[DEMO]'))]
        assert matching, s['number']
        slide.notes_slide.notes_text_frame.text = '\n\n'.join(notes(h, b) for h, b in matching)
    out = folder / 'output' / f'{folder.name[:7]}_slides{out_suffix}.pptx'
    out.parent.mkdir(exist_ok=True)
    prs.save(out)
    assert len(Presentation(out).slides) == len(spec)
    print(out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--person', choices=['1', '2', '3'])
    parser.add_argument('--variant', choices=['full', '5min', 'all'], default='all')
    args = parser.parse_args()
    variants = ['full', '5min'] if args.variant == 'all' else [args.variant]
    for folder in people(args.person):
        for v in variants:
            if (folder / f'02_SLIDE_SPEC{VARIANTS[v][0]}.md').is_file():
                build(folder, v)
