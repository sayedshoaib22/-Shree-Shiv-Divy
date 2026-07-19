from pathlib import Path
import re

root = Path(r"c:\Users\ss386\OneDrive\Desktop\New folder (9)")


def insert_attr(tag: str, name: str, value: str) -> str:
    if re.search(rf'\b{name}\s*=', tag):
        return tag
    if tag.rstrip().endswith('/>'):
        return tag[:-2] + f' {name}="{value}"' + '/>'
    return tag[:-1] + f' {name}="{value}"' + '>'


def ensure_safe_button(tag: str) -> str:
    if tag.startswith('<button') and not re.search(r'\btype\s*=', tag):
        return tag.replace('<button', '<button type="button"', 1)
    return tag


def ensure_img_attrs(tag: str) -> str:
    if ' <img' not in tag and '<img' not in tag:
        return tag
    if 'src' not in tag:
        return tag
    tag = ensure_safe_button(tag)
    if not re.search(r'\balt\s*=', tag):
        tag = insert_attr(tag, 'alt', '')
    lower = tag.lower()
    if 'brand-logo' in lower or 'brand' in lower and 'logo' in lower:
        loading_value = 'eager'
        width_value = '70'
        height_value = '70'
    elif 'hero' in lower or 'floating' in lower or 'circle' in lower:
        loading_value = 'eager'
        width_value = '120'
        height_value = '120'
    else:
        loading_value = 'lazy'
        width_value = '600'
        height_value = '400'
    if not re.search(r'\bloading\s*=', tag):
        tag = insert_attr(tag, 'loading', loading_value)
    if not re.search(r'\bdecoding\s*=', tag):
        tag = insert_attr(tag, 'decoding', 'async')
    if not re.search(r'\bwidth\s*=', tag):
        tag = insert_attr(tag, 'width', width_value)
    if not re.search(r'\bheight\s*=', tag):
        tag = insert_attr(tag, 'height', height_value)
    return tag


def ensure_head(path: Path, text: str) -> str:
    rel_path = path.relative_to(root)
    depth = len(rel_path.parts) - 1
    prefix = '../' * depth
    title_match = re.search(r'(?is)<title>(.*?)</title>', text)
    title = title_match.group(1).strip() if title_match else 'Shree Shiv Divy Astrology Centre'
    title = re.sub(r'\s+', ' ', title)

    description_match = re.search(r'(?is)<meta\s+name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', text)
    description = description_match.group(1).strip() if description_match else (
        'Shree Shiv Divy Astrology Centre offers trusted astrology consultation, puja services, kundli matching and vastu guidance.'
    )

    rel_name = rel_path.as_posix()
    if rel_name == 'index.html' or rel_name.endswith('/index.html'):
        canonical = 'https://shreeshivdivy.com/'
    else:
        canonical = f'https://shreeshivdivy.com/{rel_name}'

    head_match = re.search(r'(?is)<head\b[^>]*>(.*?)</head>', text)
    if not head_match:
        return text

    head = head_match.group(1)
    head = re.sub(r'(?is)\s*<link\s+rel=["\'](?:icon|apple-touch-icon|manifest)[^>]*>\s*', '\n', head)
    head = re.sub(r'(?is)\s*<meta\s+name=["\']theme-color["\'][^>]*>\s*', '\n', head)
    head = re.sub(r'(?is)\s*<meta\s+charset=[^>]*>\s*', '\n', head)
    head = re.sub(r'(?is)\s*<meta\s+name=["\']viewport["\'][^>]*>\s*', '\n', head)
    head = re.sub(r'(?is)\s*<meta\s+name=["\']description["\'][^>]*>\s*', '\n', head)
    head = re.sub(r'(?is)\s*<meta\s+name=["\']keywords["\'][^>]*>\s*', '\n', head)
    head = re.sub(r'(?is)\s*<link\s+rel=["\']canonical["\'][^>]*>\s*', '\n', head)
    head = re.sub(r'(?is)\s*<meta\s+name=["\']robots["\'][^>]*>\s*', '\n', head)
    head = re.sub(r'(?is)\s*<meta\s+property=["\']og:[^>]*>\s*', '\n', head)
    head = re.sub(r'(?is)\s*<meta\s+name=["\']twitter:[^>]*>\s*', '\n', head)
    head = re.sub(r'(?is)\s*<meta\s+name=["\']referrer["\'][^>]*>\s*', '\n', head)

    meta_block = f'''\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n  <meta name="theme-color" content="#A6821F">\n  <meta name="color-scheme" content="light only">\n  <meta name="referrer" content="strict-origin-when-cross-origin">\n  <meta name="description" content="{description}">\n  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">\n  <link rel="canonical" href="{canonical}">\n  <link rel="icon" type="image/x-icon" href="/favicon.ico" sizes="any">\n  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">\n  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">\n  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">\n  <link rel="manifest" href="/site.webmanifest">\n  <meta property="og:type" content="website">\n  <meta property="og:title" content="{title}">\n  <meta property="og:description" content="{description}">\n  <meta property="og:url" content="{canonical}">\n  <meta property="og:image" content="https://shreeshivdivy.com/images/Shree-Shiv-Divy-Logo.webp">\n  <meta property="og:image:alt" content="Shree Shiv Divy Astrology Centre logo">\n  <meta property="og:locale" content="en_IN">\n  <meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:title" content="{title}">\n  <meta name="twitter:description" content="{description}">\n  <meta name="twitter:image" content="https://shreeshivdivy.com/images/Shree-Shiv-Divy-Logo.webp">\n'''

    if title_match:
        head = head.replace(title_match.group(0), meta_block + '\n' + title_match.group(0), 1)
    else:
        head = meta_block + '\n' + head

    head = re.sub(r'(?is)(<link\s+rel=["\']stylesheet["\'][^>]*href=["\'])(styles\.css)(["\'])', rf'\g<1>{prefix}styles.css\3', head)
    head = re.sub(r'(?is)(<link\s+rel=["\']stylesheet["\'][^>]*href=["\'])(shared\.css)(["\'])', rf'\g<1>{prefix}shared.css\3', head)
    head = re.sub(r'(?is)(<link\s+rel=["\']stylesheet["\'][^>]*href=["\'])(city\.css)(["\'])', rf'\g<1>{prefix}city.css\3', head)
    head = re.sub(r'(?is)(<link\s+rel=["\']stylesheet["\'][^>]*href=["\'])(city-popup\.css)(["\'])', rf'\g<1>{prefix}city-popup.css\3', head)
    head = re.sub(r'(?is)(<link\s+rel=["\']stylesheet["\'][^>]*href=["\'])(about-redesign\.css)(["\'])', rf'\g<1>{prefix}about-redesign.css\3', head)
    head = re.sub(r'(?is)(<script[^>]*src=["\'])(scripts/[^"\']+)(["\'])', rf'\g<1>{prefix}\2\3', head)
    head = re.sub(r'(?is)(src=["\'])(images/)([^"]+)(["\'])', rf'\g<1>{prefix}images/\3\4', head)
    head = re.sub(r'(?is)(href=["\'])(images/)([^"]+)(["\'])', rf'\g<1>{prefix}images/\3\4', head)
    head = re.sub(r'(?is)(href=["\'])(about\.html)(["\'])', rf'\g<1>{prefix}about.html\3', head)
    head = re.sub(r'(?is)(href=["\'])(astrology-guide\.html)(["\'])', rf'\g<1>{prefix}astrology-guide.html\3', head)
    head = re.sub(r'(?is)(href=["\'])(index\.html)(["\'])', rf'\g<1>{prefix}index.html\3', head)
    head = re.sub(r'(?is)(href=["\'])(pages/[^"\']+)(["\'])', rf'\g<1>{prefix}\2\3', head)

    return text.replace(head_match.group(0), f'<head>{head}</head>', 1)


html_files = sorted([p for p in root.rglob('*.html') if p.is_file()])
for path in html_files:
    text = path.read_text(encoding='utf-8')
    text = ensure_head(path, text)
    text = re.sub(r'(?is)<img\b[^>]*>', lambda m: ensure_img_attrs(m.group(0)), text)
    text = re.sub(r'(?is)<button\b(?![^>]*\btype=)', lambda m: m.group(0).replace('<button', '<button type="button"', 1), text)
    text = re.sub(r'(?is)(<a\b[^>]*)(target=["\']_blank["\'])', r'\1', text)
    text = re.sub(r'(?is)(<a\b[^>]*)([^>]*?)>', lambda m: m.group(0).replace('>', ' rel="noopener noreferrer">', 1) if 'target="_blank"' in m.group(0) else m.group(0), text)
    text = text.replace('target="_blank"', 'target="_blank" rel="noopener noreferrer"')
    path.write_text(text, encoding='utf-8')

# create a compatibility stylesheet for missing city.css links
city_css = root / 'city.css'
if not city_css.exists():
    city_css.write_text('@import url("city-popup.css");\n', encoding='utf-8')

# refresh manifest to use real PNG assets
manifest_path = root / 'site.webmanifest'
manifest_path.write_text('''{\n  "name": "Shree Shiv Divy Astrology Centre",\n  "short_name": "Shree Shiv Divy",\n  "id": "/",\n  "start_url": "/",\n  "scope": "/",\n  "display": "standalone",\n  "background_color": "#FDF9EF",\n  "theme_color": "#A6821F",\n  "description": "Astrology consultations, puja services, and spiritual guidance.",\n  "icons": [\n    {\n      "src": "/favicon-16x16.png",\n      "sizes": "16x16",\n      "type": "image/png",\n      "purpose": "any"\n    },\n    {\n      "src": "/favicon-32x32.png",\n      "sizes": "32x32",\n      "type": "image/png",\n      "purpose": "any"\n    },\n    {\n      "src": "/android-chrome-192x192.png",\n      "sizes": "192x192",\n      "type": "image/png",\n      "purpose": "any"\n    },\n    {\n      "src": "/android-chrome-512x512.png",\n      "sizes": "512x512",\n      "type": "image/png",\n      "purpose": "any"\n    }\n  ]\n}\n''', encoding='utf-8')

# ensure robots and sitemap are present with clean canonical references
robots_path = root / 'robots.txt'
robots_path.write_text('''User-agent: *\nAllow: /\n\nSitemap: https://shreeshivdivy.com/sitemap.xml\n''', encoding='utf-8')

print(f'Updated {len(html_files)} HTML files and refreshed manifest/robots.')
