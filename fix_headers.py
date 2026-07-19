from pathlib import Path
import re

root = Path(r"c:\Users\ss386\OneDrive\Desktop\New folder (9)")
index_text = (root / 'index.html').read_text(encoding='utf-8')

header_match = re.search(r'<div class="topbar">.*?(?=<section class="hero" id="top">)', index_text, re.S)
if not header_match:
    raise SystemExit('Could not find header block in index.html')
master_header = header_match.group(0)

popup_match = re.search(r'<script>\(function\(\)\{.*?window\.refreshHeaderCity = renderHeaderCity;\}\)\(\);\n</script>\n<link rel="stylesheet" href="city-popup\.css">.*?<script src="city-popup\.js" defer></script>', index_text, re.S)
if not popup_match:
    raise SystemExit('Could not find city popup block in index.html')
master_popup = popup_match.group(0)

for path in sorted(root.rglob('*.html')):
    if path.name == 'index.html':
        continue

    text = path.read_text(encoding='utf-8')
    rel = path.relative_to(root)
    is_pages_subdir = len(rel.parts) > 1 and rel.parts[0] == 'pages'

    if '<header class="site">' in text and 'id="header-city-display-mobile"' in text and 'id="tnav"' in text and 'city-popup.css' in text and 'city-popup.js' in text:
        continue

    header_block = master_header
    if is_pages_subdir:
        header_block = header_block.replace('href="index.html"', 'href="../index.html"')
        header_block = header_block.replace('href="about.html"', 'href="../about.html"')
        header_block = header_block.replace('src="images/', 'src="../images/')
        header_block = header_block.replace('href="#top"', 'href="../index.html#top"')
        header_block = header_block.replace('href="#services"', 'href="../index.html#services"')
        header_block = header_block.replace('href="#why-us"', 'href="../index.html#why-us"')
        header_block = header_block.replace('href="#process"', 'href="../index.html#process"')
        header_block = header_block.replace('href="#testimonials"', 'href="../index.html#testimonials"')
        header_block = header_block.replace('href="#faq"', 'href="../index.html#faq"')
        header_block = header_block.replace('href="#book"', 'href="../index.html#book"')

    if is_pages_subdir and '../shared.css' not in text:
        text = text.replace('<link rel="stylesheet" href="../styles.css">
<link rel="stylesheet" href="./city.css">', '<link rel="stylesheet" href="../shared.css">\n<link rel="stylesheet" href="../styles.css">
<link rel="stylesheet" href="./city.css">', 1)
    elif not is_pages_subdir and 'shared.css' not in text and 'href="styles.css"' in text:
        text = text.replace('<link rel="stylesheet" href="styles.css">', '<link rel="stylesheet" href="shared.css">\n<link rel="stylesheet" href="styles.css">', 1)

    if '<main>' in text:
        pattern = re.compile(r'<div class="topbar">.*?(?=<main>)', re.S)
        new_text, count = pattern.subn(header_block + '\n<main>', text, count=1)
    else:
        pattern = re.compile(r'<div class="topbar">.*?(?=<section\b)', re.S)
        new_text, count = pattern.subn(header_block + '\n<section>', text, count=1)

    if count == 0:
        continue

    if 'city-popup.css' not in new_text:
        popup_block = master_popup
        if is_pages_subdir:
            popup_block = popup_block.replace('href="city-popup.css"', 'href="../city-popup.css"')
            popup_block = popup_block.replace('src="city-popup.js"', 'src="../city-popup.js"')
        new_text = new_text.replace('</body>', popup_block + '\n\n</body>', 1)

    path.write_text(new_text, encoding='utf-8')

print('Updated HTML files with shared header and city popup markup.')
