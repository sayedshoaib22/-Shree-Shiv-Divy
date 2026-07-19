from pathlib import Path
import re
files = list(Path(r"c:\Users\ss386\OneDrive\Desktop\New folder (9)").rglob('*.html'))
missing = []
for path in files:
    text = path.read_text(encoding='utf-8')
    for m in re.finditer(r'<img\b([^>]*)>', text, re.I):
        attrs = m.group(1)
        if 'alt=' not in attrs.lower():
            missing.append(str(path))
            break
print('missing_alt', len(missing))
for item in missing[:10]:
    print(item)
