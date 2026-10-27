import re
import markdown

with open('RESEARCH_REPORT_WEEK10_DISCOURSE_EFFECTIVENESS_CLC02_GROUP06.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Replace unicode en-dash and em-dash with standard HTML entities
md_content = md_content.replace('–', '&ndash;').replace('—', '&mdash;')

# Replace page break tags
md_content = md_content.replace('<div style="page-break-before: always;"></div>', '<div class="page-break"></div>')

# 1. Protect display math $$...$$ and inline math $...$ from markdown parser
math_store = {}

def protect_math_display(match):
    key = f"XXMATHDISPLAY{len(math_store)}XX"
    math_store[key] = match.group(0)
    return key

def protect_math_inline(match):
    key = f"XXMATHINLINE{len(math_store)}XX"
    math_store[key] = match.group(0)
    return key

# Protect display math first
md_content = re.sub(r'\$\$.*?\$\$', protect_math_display, md_content, flags=re.DOTALL)

# Protect inline math
md_content = re.sub(r'(?<!\$)\$(?!\$)([^\$\n]+?)(?<!\$)\$(?!\$)', protect_math_inline, md_content)

# 2. Convert markdown to HTML
html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'def_list', 'attr_list'])

# 3. Restore protected math
for key, original_math in math_store.items():
    html_body = html_body.replace(key, original_math)

# Complete HTML Document
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Technical Research Report (Week 10) - Group 06 CLC02</title>
    <!-- KaTeX CSS & JS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"
            onload="renderMathInElement(document.body, {
                output: 'html',
                throwOnError: false,
                ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
                delimiters: [
                    {left: '$$', right: '$$', display: true},
                    {left: '$', right: '$', display: false}
                ]
            });"></script>
    <style>
        @page {
            size: A4;
            margin: 16mm 14mm 16mm 14mm;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            color: #1e293b;
            line-height: 1.6;
            max-width: 940px;
            margin: 0 auto;
            padding: 30px 20px;
            background: #ffffff;
        }
        .katex-mathml {
            display: none !important;
        }
        .katex {
            font-size: 1.05em;
        }
        .katex-display {
            margin: 14px 0 !important;
            overflow-x: auto;
            overflow-y: hidden;
            padding: 4px 0;
        }
        h1, h2, h3, h4 {
            color: #0f2d59;
            font-weight: 600;
        }
        h1 {
            font-size: 18pt;
            border-bottom: 2px solid #0f2d59;
            padding-bottom: 8px;
            margin-top: 0;
            text-align: center;
        }
        h2 {
            font-size: 13pt;
            border-bottom: 1.5px solid #cbd5e1;
            padding-bottom: 5px;
            margin-top: 26px;
            margin-bottom: 12px;
        }
        h3 {
            font-size: 11pt;
            margin-top: 18px;
            margin-bottom: 8px;
        }
        h4 {
            font-size: 10pt;
            margin-top: 14px;
            margin-bottom: 6px;
        }
        p, li {
            font-size: 9.5pt;
            color: #334155;
        }
        ul, ol {
            margin-top: 6px;
            margin-bottom: 12px;
            padding-left: 22px;
        }
        li {
            margin-bottom: 4px;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 14px 0;
            font-size: 8.5pt;
            page-break-inside: avoid;
        }
        th, td {
            border: 1px solid #cbd5e1;
            padding: 5px 8px;
            text-align: left;
        }
        th {
            background-color: #f1f5f9;
            color: #0f2d59;
            font-weight: 600;
        }
        tr:nth-child(even) {
            background-color: #f8fafc;
        }
        pre {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 8pt;
            line-height: 1.35;
            overflow-x: auto;
            page-break-inside: avoid;
        }
        code {
            font-family: "Consolas", "Courier New", monospace;
            font-size: 8.5pt;
            background-color: #f1f5f9;
            color: #0f2d59;
            padding: 2px 4px;
            border-radius: 3px;
        }
        pre code {
            background-color: transparent;
            padding: 0;
            color: inherit;
        }
        blockquote {
            border-left: 4px solid #0f2d59;
            margin: 12px 0;
            padding: 8px 14px;
            background-color: #f8fafc;
            font-size: 9pt;
            color: #1e293b;
            border-radius: 0 5px 5px 0;
        }
        a {
            color: #0284c7;
            text-decoration: underline;
        }
        a:hover {
            color: #0369a1;
        }
        .page-break {
            page-break-before: always;
        }
        @media print {
            body {
                padding: 0;
                max-width: 100%;
            }
            .page-break {
                page-break-before: always;
            }
            a {
                text-decoration: underline;
                color: #0284c7 !important;
            }
        }
    </style>
</head>
<body>
""" + html_body + """
</body>
</html>
"""

with open('Week10_Group06_CLC02_Report.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Week10_Group06_CLC02_Report.html successfully generated and validated.")
