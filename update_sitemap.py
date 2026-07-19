from pathlib import Path
from datetime import date

root = Path(r"c:\Users\ss386\OneDrive\Desktop\New folder (9)")
html_files = sorted([p for p in root.rglob('*.html') if 'sitemap.xml' not in p.name])

site = 'https://shreeshivdivy.com'


def priority_for(path: Path) -> str:
    if path.name == 'index.html':
        return '1.0'
    if path.name == 'about.html':
        return '0.9'
    if path.parent.name == 'pages':
        return '0.7'
    return '0.8'


entries = []
for path in html_files:
    rel = path.relative_to(root)
    if rel.name == 'index.html':
        loc = f'{site}/'
    else:
        loc = f'{site}/{rel.as_posix()}'
    entries.append(
        '  <url>\n'
        f'    <loc>{loc}</loc>\n'
        f'    <lastmod>{date.today().isoformat()}</lastmod>\n'
        '    <changefreq>monthly</changefreq>\n'
        f'    <priority>{priority_for(path)}</priority>\n'
        '  </url>'
    )

xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
xml += '\n'.join(entries) + '\n'
xml += '</urlset>\n'
(root / 'sitemap.xml').write_text(xml, encoding='utf-8')
print(f'WROTE={len(entries)}')
