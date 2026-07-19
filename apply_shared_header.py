from pathlib import Path
import re

root = Path(r'c:\Users\ss386\OneDrive\Desktop\New folder (9)')

html_files = sorted([p for p in root.rglob('*.html') if p.is_file()])

for path in html_files:
    text = path.read_text(encoding='utf-8')
    rel = path.relative_to(root)
    depth = len(rel.parts) - 1
    prefix = '../' * depth

    if depth == 0:
        services_href = '#services'
        why_href = '#why-us'
        process_href = '#process'
        reviews_href = '#testimonials'
        about_href = 'about.html'
        faq_href = '#faq'
        brand_href = 'index.html'
        logo_src = 'images/shree-shiv-divy-logo.webp'
        book_href = '#book'
    else:
        services_href = f'{prefix}index.html#services'
        why_href = f'{prefix}index.html#why-us'
        process_href = f'{prefix}index.html#process'
        reviews_href = f'{prefix}index.html#testimonials'
        about_href = f'{prefix}about.html'
        faq_href = f'{prefix}index.html#faq'
        brand_href = f'{prefix}index.html'
        logo_src = f'{prefix}images/shree-shiv-divy-logo.webp'
        book_href = '#book'

    new_block = f'''<header class="site">
  <div class="container nav-row">
    <a href="{brand_href}" class="brand">
      <img src="{logo_src}" alt="Shree Shiv Divy Astrology Centre Logo" class="brand-logo" width="70" height="70" decoding="async">
      <span class="brand-text">Shree Shiv Divy<span>Astrology Centre</span></span>
    </a>
    <nav class="main">
      <a href="{services_href}">Services</a>
      <a href="{why_href}">Why Us</a>
      <a href="{process_href}">Process</a>
      <a href="{reviews_href}">Reviews</a>
      <a href="{about_href}">About</a>
      <a href="{faq_href}">FAQ</a>
    </nav>
    <div class="header-cta">
      <span id="header-city-display" class="header-city" onclick="if(typeof openCityPopup === 'function'){{ openCityPopup(); }}" role="button" tabindex="0" aria-label="Change city">
        <span id="header-city-label">📍 Choose City</span>
        <button type="button" class="header-city-change" onclick="event.stopPropagation(); if(typeof openCityPopup === 'function'){{ openCityPopup(); }}">Change City</button>
      </span>
      <a href="tel:+917271836719" class="btn btn-ghost">Call Now</a>
      <a href="{book_href}" class="btn btn-primary">Book Consultation</a>
    </div>
    <button class="menu-toggle" aria-label="Open menu" onclick="document.getElementById('mnav').classList.add('open')">☰</button>
    <button type="button" class="tablet-menu-toggle" id="tabletMenuBtn" aria-label="Open menu" aria-expanded="false" aria-controls="tnav" onclick="openTabletNav()">
      <span class="tablet-menu-toggle__bar"></span>
      <span class="tablet-menu-toggle__bar"></span>
      <span class="tablet-menu-toggle__bar"></span>
    </button>
  </div>
</header>

<div class="tablet-drawer-overlay" id="tnavOverlay" hidden></div>
<div class="tablet-drawer" id="tnav" role="dialog" aria-modal="true" aria-label="Site navigation" aria-hidden="true">
  <div class="tablet-drawer-top">
    <a href="{brand_href}" class="brand" tabindex="-1">
      <img src="{logo_src}" alt="Shree Shiv Divy Astrology Centre Logo" class="brand-logo" width="70" height="70" decoding="async">
      <span class="brand-text">Shree Shiv Divy<span>Astrology Centre</span></span>
    </a>
    <button type="button" class="tablet-drawer-close" aria-label="Close menu" onclick="closeTabletNav()">×</button>
  </div>
  <nav class="tablet-drawer-nav" aria-label="Primary">
    <a href="{brand_href}" onclick="closeTabletNav()">Home</a>
    <a href="{why_href}" onclick="closeTabletNav()">Why Us</a>
    <a href="{services_href}" onclick="closeTabletNav()">Services</a>
    <a href="{process_href}" onclick="closeTabletNav()">Process</a>
    <a href="{reviews_href}" onclick="closeTabletNav()">Reviews</a>
    <a href="{about_href}" onclick="closeTabletNav()">About</a>
    <a href="{faq_href}" onclick="closeTabletNav()">FAQ</a>
  </nav>
  <span class="header-city header-city--mobile" onclick="if(typeof openCityPopup === 'function'){{ openCityPopup(); }}" role="button" tabindex="0" aria-label="Change city">
    <span>📍 Choose City</span>
    <button type="button" class="header-city-change" onclick="event.stopPropagation(); if(typeof openCityPopup === 'function'){{ openCityPopup(); }}">Change City</button>
  </span>
  <div class="tablet-drawer-actions">
    <a href="tel:+917271836719" class="btn btn-ghost" onclick="closeTabletNav()">Call Now</a>
    <a href="{book_href}" class="btn btn-primary" onclick="closeTabletNav()">Book Consultation</a>
    <a href="https://wa.me/917271836719" class="btn btn-whatsapp" onclick="closeTabletNav()">WhatsApp</a>
  </div>
</div>

<script>
(function(){{
  var tnav = document.getElementById('tnav');
  var overlay = document.getElementById('tnavOverlay');
  var toggleBtn = document.getElementById('tabletMenuBtn');
  var lastFocused = null;
  var TAB_MIN = 721, TAB_MAX = 1199;

  function focusables(){{
    return tnav.querySelectorAll('a[href], button:not([disabled])');
  }}

  function onKeydown(e){{
    if(e.key === 'Escape' || e.key === 'Esc'){{ closeTabletNav(); return; }}
    if(e.key === 'Tab'){{
      var f = Array.prototype.slice.call(focusables());
      if(!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if(e.shiftKey && document.activeElement === first){{ e.preventDefault(); last.focus(); }}
      else if(!e.shiftKey && document.activeElement === last){{ e.preventDefault(); first.focus(); }}
    }}
  }}

  window.openTabletNav = function(){{
    lastFocused = document.activeElement;
    overlay.hidden = false;
    requestAnimationFrame(function(){{
      tnav.classList.add('open');
      overlay.classList.add('open');
    }});
    tnav.setAttribute('aria-hidden', 'false');
    toggleBtn.setAttribute('aria-expanded', 'true');
    toggleBtn.classList.add('open');
    document.body.classList.add('tnav-lock');
    document.addEventListener('keydown', onKeydown);
    var f = focusables();
    if(f.length){{ f[0].focus(); }}
  }};

  window.closeTabletNav = function(){{
    tnav.classList.remove('open');
    overlay.classList.remove('open');
    tnav.setAttribute('aria-hidden', 'true');
    toggleBtn.setAttribute('aria-expanded', 'false');
    toggleBtn.classList.remove('open');
    document.body.classList.remove('tnav-lock');
    document.removeEventListener('keydown', onKeydown);
    setTimeout(function(){{ if(!tnav.classList.contains('open')){{ overlay.hidden = true; }} }}, 300);
    if(lastFocused && typeof lastFocused.focus === 'function'){{ lastFocused.focus(); }}
  }};

  overlay.addEventListener('click', closeTabletNav);

  window.addEventListener('resize', function(){{
    var w = window.innerWidth;
    if((w < TAB_MIN || w > TAB_MAX) && tnav.classList.contains('open')){{
      closeTabletNav();
    }}
  }});
}})();
</script>

<div class="mobile-nav" id="mnav">
  <div class="mobile-nav-top">
    <span class="brand-text" style="color:#FDF9EF">Menu</span>
    <button aria-label="Close menu" onclick="document.getElementById('mnav').classList.remove('open')">×</button>
  </div>
  <span id="header-city-display-mobile" class="header-city header-city--mobile" onclick="if(typeof openCityPopup === 'function'){{ openCityPopup(); }}" role="button" tabindex="0" aria-label="Change city">
    <span id="header-city-label-mobile">📍 Choose City</span>
    <button type="button" class="header-city-change" onclick="event.stopPropagation(); if(typeof openCityPopup === 'function'){{ openCityPopup(); }}">Change City</button>
  </span>
  <a href="{services_href}" onclick="document.getElementById('mnav').classList.remove('open')">Services</a>
  <a href="{why_href}" onclick="document.getElementById('mnav').classList.remove('open')">Why Us</a>
  <a href="{process_href}" onclick="document.getElementById('mnav').classList.remove('open')">Process</a>
  <a href="{reviews_href}" onclick="document.getElementById('mnav').classList.remove('open')">Reviews</a>
  <a href="{about_href}" onclick="document.getElementById('mnav').classList.remove('open')">About</a>
  <a href="{faq_href}" onclick="document.getElementById('mnav').classList.remove('open')">FAQ</a>
  <a href="{book_href}" class="btn btn-primary">Book Consultation</a>
</div>

'''

    pattern = re.compile(r'<header class="site">.*?<section class="hero" id="top">', re.S)
    updated = pattern.sub(new_block + '<section class="hero" id="top">', text, count=1)
    if updated != text:
        path.write_text(updated, encoding='utf-8')

print(f'Updated {len(html_files)} HTML files')
