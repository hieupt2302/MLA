import re
import markdown

with open('BAO_CAO_TUAN_10_HOAN_CHINH_CLC02_GROUP06.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

md_content = md_content.replace('–', '&ndash;').replace('—', '&mdash;')
md_content = md_content.replace('<div style="page-break-before: always;"></div>', '<div class="page-break"></div>')

math_store = {}

def protect_math_display(match):
    key = f"XXMATHDISPLAY{len(math_store)}XX"
    math_store[key] = match.group(0)
    return key

def protect_math_inline(match):
    key = f"XXMATHINLINE{len(math_store)}XX"
    math_store[key] = match.group(0)
    return key

md_content = re.sub(r'\$\$.*?\$\$', protect_math_display, md_content, flags=re.DOTALL)
md_content = re.sub(r'(?<!\$)\$(?!\$)([^\$\n]+?)(?<!\$)\$(?!\$)', protect_math_inline, md_content)

html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'def_list', 'attr_list'])

for key, original_math in math_store.items():
    html_body = html_body.replace(key, original_math)

# Load header and footer from render_html.py
with open('render_html.py', 'r', encoding='utf-8') as f:
    orig = f.read()

# Header is from <!DOCTYPE html> up to <body>\n
header_start = orig.find('<!DOCTYPE html>')
header_end = orig.find('<body>\n') + len('<body>\n')
header = orig[header_start:header_end]

footer = "\n</body>\n</html>\n"

header = header.replace('lang="en"', 'lang="vi"')
header = header.replace('Technical Research Report (Week 10) - Group 06 CLC02', 'Báo Cáo Nghiên Cứu Kỹ Thuật (Tuần 10) - Nhóm 06 CLC02')

final_html = header + html_body + footer

with open('Bao_Cao_Tuan_10_Group06_CLC02.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print('Rendered Bao_Cao_Tuan_10_Group06_CLC02.html successfully!')
