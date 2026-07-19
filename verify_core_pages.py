from pathlib import Path
root = Path(r"c:\Users\ss386\OneDrive\Desktop\New folder (9)")
for name in ['index.html', 'about.html', 'delhi.html']:
    path = root / name
    text = path.read_text(encoding='utf-8')
    print(name, 'lang', '<html lang=' in text, 'charset', '<meta charset=' in text, 'viewport', '<meta name="viewport"' in text, 'canonical', '<link rel="canonical"' in text, 'title', '<title>' in text)
