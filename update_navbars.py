from pathlib import Path
import re

root = Path(r"c:\Users\ss386\OneDrive\Desktop\New folder (9)")
files = sorted(list(root.glob('*.html')) + list((root / 'pages').glob('*.html')))

style_block = """
<style>
nav.main a.active,
.tablet-drawer-nav a.active,
.mobile-nav a.active {
  color: var(--gold-deep);
}
nav.main a.active::after {
  transform: scaleX(1);
}
.tablet-drawer-nav a.active {
  border-bottom-color: rgba(166, 130, 31, 0.35);
}
.mobile-nav a.active {
  color: var(--gold-light);
}
</style>
"""

script_block = """
<script>
(function () {
  var currentPage = (window.location.pathname.split('/').pop() || 'index.html').toLowerCase();
  document.querySelectorAll('nav.main a[href], .tablet-drawer-nav a[href], .mobile-nav a[href]').forEach(function (link) {
    var href = (link.getAttribute('href') || '').split('#')[0];
    if (!href) return;
    var resolved = new URL(href, window.location.href).pathname.split('/').pop().toLowerCase();
    if (resolved === currentPage) {
      link.classList.add('active');
    }
  });
})();
</script>
"""

for path in files:
    text = path.read_text(encoding='utf-8')
    if not text.strip():
        continue

    is_pages_file = path.parent.name == 'pages'
    home = '../index.html' if is_pages_file else 'index.html'
    about = '../about.html' if is_pages_file else 'about.html'
    guide = '../astrology-guide.html' if is_pages_file else 'astrology-guide.html'

    # Desktop nav
    text = re.sub(
        r'(<nav class="main">)([\s\S]*?)(</nav>)',
        lambda m: f'{m.group(1)}\n        <a href="{home}">Home</a>\n        <a href="{about}">About</a>\n        <a href="{guide}">Astrology Guide</a>\n      {m.group(3)}',
        text,
        count=1,
    )

    # Tablet drawer nav
    text = re.sub(
        r'(<nav class="tablet-drawer-nav"[^>]*>)([\s\S]*?)(</nav>)',
        lambda m: f'{m.group(1)}\n      <a href="{home}" onclick="closeTabletNav()">Home</a>\n      <a href="{about}" onclick="closeTabletNav()">About</a>\n      <a href="{guide}" onclick="closeTabletNav()">Astrology Guide</a>\n    {m.group(3)}',
        text,
        count=1,
    )

    # Mobile nav: preserve top bar, city row, and actions; replace anchor links inside the mobile nav block
    pattern = re.compile(r'(<div class="mobile-nav"[^>]*>)([\s\S]*?)(<div class="mobile-nav-actions">)', re.I)
    match = pattern.search(text)
    if match:
        body = match.group(2)
        body = re.sub(r'\n\s*<a\b[^>]*>.*?</a>', '', body)
        body = body + f'\n  <a href="{home}" onclick="document.getElementById(\'mnav\').classList.remove(\'open\')">Home</a>\n  <a href="{about}" onclick="document.getElementById(\'mnav\').classList.remove(\'open\')">About</a>\n  <a href="{guide}" onclick="document.getElementById(\'mnav\').classList.remove(\'open\')">Astrology Guide</a>\n  '
        text = text[:match.start(2)] + body + text[match.end(2):]

    if '</head>' in text and 'nav.main a.active' not in text:
        text = text.replace('</head>', style_block + '</head>', 1)
    if '</body>' in text and 'link.classList.add' not in text:
        text = text.replace('</body>', script_block + '</body>', 1)

    path.write_text(text, encoding='utf-8')

print(f'Updated {len(files)} HTML files')
