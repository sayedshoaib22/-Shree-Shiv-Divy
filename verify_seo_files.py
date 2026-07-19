from pathlib import Path
root = Path(r"c:\Users\ss386\OneDrive\Desktop\New folder (9)")
for name in ['site.webmanifest', 'robots.txt', 'sitemap.xml']:
    path = root / name
    print(name, path.exists(), path.stat().st_size if path.exists() else None)
