from pathlib import Path
root = Path(r"c:\Users\ss386\OneDrive\Desktop\New folder (9)")
files = list(root.rglob('*.html'))
print('html files', len(files))
bad = []
for path in files:
    text = path.read_text(encoding='utf-8')
    if '<html lang=' not in text:
        bad.append(str(path) + ' missing lang')
    if '<meta charset=' not in text:
        bad.append(str(path) + ' missing charset')
    if '<meta name="viewport"' not in text:
        bad.append(str(path) + ' missing viewport')
    if '<title>' not in text:
        bad.append(str(path) + ' missing title')
    if '<link rel="canonical"' not in text:
        bad.append(str(path) + ' missing canonical')
    if 'favicon.ico' not in text and 'favicon-16x16.png' not in text:
        bad.append(str(path) + ' missing favicon refs')
print('issues', len(bad))
for item in bad[:10]:
    print(item)
