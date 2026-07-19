(function(){
  function ensureCircle(){
    var section = document.querySelector('section.hero, section.ap-hero');
    if(!section) return;
    var existing = section.querySelector('.hero-floating-circle');
    var imgSrc = (window.location.pathname.indexOf('/pages/') !== -1) ? '../images/maa-hinglaj-devi-darshan.webp' : 'images/maa-hinglaj-devi-darshan.webp';
    var html = '<div class="hero-floating-circle" aria-label="Maa Hinglaj Devi">' +
               '<img src="'+imgSrc+'" alt="Maa Hinglaj Devi" loading="lazy" decoding="async" width="120" height="120" />' +
               '</div>';
    if(existing){
      // replace existing with standardized markup
      existing.outerHTML = html;
    } else {
      // insert as first child so it positions relative to the hero section
      section.insertAdjacentHTML('afterbegin', html);
    }
    // ensure it doesn't overlap nav: increase z-index if necessary
    var circle = section.querySelector('.hero-floating-circle');
    if(circle){ circle.style.zIndex = 20; }
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ensureCircle);
  else ensureCircle();
})();