import os, glob
root = r'c:\Users\ss386\OneDrive\Desktop\New folder (9)'
os.chdir(root)
files = sorted(glob.glob('**/*.html', recursive=True))
checks = [
    ('<header class="site">', 'header'),
    ('id="tnav"', 'tablet_nav'),
    ('id="mnav"', 'mobile_nav'),
    ('id="header-city-display-mobile"', 'mobile_city'),
    ('city-popup.css', 'city_css'),
    ('city-popup.js', 'city_js'),
    ('tablet-menu-toggle', 'tablet_toggle'),
]
missing = []
for path in files:
    with open(path, encoding='utf-8') as f:
        txt = f.read()
    vals = {name: needle in txt for needle, name in checks}
    if not all(vals.values()):
        missing.append((path, vals))
print('Total HTML files:', len(files))
print('Missing required header/nav markup:', len(missing))
for path, vals in missing:
    print(path, '->', {k: v for k, v in vals.items() if not v})
