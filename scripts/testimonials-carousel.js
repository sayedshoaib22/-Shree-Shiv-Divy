
    document.getElementById('year').textContent = new Date().getFullYear();

    (function () {
      var marquee = document.querySelector('.trusted-marquee');
      var track = marquee && marquee.querySelector('.trusted-marquee-track');
      if (!marquee || !track) return;

      var items = Array.from(track.children).filter(function (el) { return el.classList.contains('trusted-logo-item'); });
      if (!items.length) return;

      var alreadyCloned = Array.from(track.children).some(function (el) { return el.getAttribute('data-clone') === 'true'; });
      if (!alreadyCloned) {
        var fragment = document.createDocumentFragment();
        items.forEach(function (item) {
          var clone = item.cloneNode(true);
          clone.setAttribute('data-clone', 'true');
          clone.setAttribute('aria-hidden', 'true');
          fragment.appendChild(clone);
        });
        track.appendChild(fragment);
      }

      marquee.addEventListener('mouseenter', function () { marquee.classList.add('is-hovered'); });
      marquee.addEventListener('mouseleave', function () { marquee.classList.remove('is-hovered'); });
      marquee.addEventListener('touchstart', function () { marquee.classList.add('is-hovered'); }, { passive: true });
      marquee.addEventListener('touchend', function () { marquee.classList.remove('is-hovered'); });
      marquee.addEventListener('touchcancel', function () { marquee.classList.remove('is-hovered'); });
    })();

    (function () {
      var track = document.querySelector('.testi-track');
      if (!track || track.querySelector('.testi-track-inner')) return;

      var cards = Array.from(track.children).filter(function (el) {
        return el.classList.contains('testi-card');
      });
      if (!cards.length) return;

      var inner = document.createElement('div');
      inner.className = 'testi-track-inner';

      var group = document.createElement('div');
      group.className = 'testi-track-group';
      cards.forEach(function (card) {
        group.appendChild(card);
      });

      var cloneGroup = group.cloneNode(true);
      cloneGroup.className = 'testi-track-group testi-track-group--clone';
      cloneGroup.setAttribute('aria-hidden', 'true');

      inner.appendChild(group);
      inner.appendChild(cloneGroup);
      track.innerHTML = '';
      track.appendChild(inner);

      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        track.classList.add('motion-disabled');
        return;
      }

      function syncTrackOffset() {
        var gap = parseFloat(getComputedStyle(inner).columnGap || getComputedStyle(inner).gap || 22);
        var groupWidth = group.getBoundingClientRect().width;
        track.style.setProperty('--track-offset', (groupWidth + gap) + 'px');
        track.style.setProperty('--testi-speed', window.innerWidth <= 768 ? '20s' : '32s');
      }

      syncTrackOffset();
      window.addEventListener('resize', syncTrackOffset);

      track.addEventListener('mouseenter', function () { track.classList.add('is-paused'); });
      track.addEventListener('mouseleave', function () { track.classList.remove('is-paused'); });
      track.addEventListener('touchstart', function () { track.classList.add('is-paused'); }, { passive: true });
      track.addEventListener('touchend', function () { track.classList.remove('is-paused'); });
      track.addEventListener('touchcancel', function () { track.classList.remove('is-paused'); });
    })();

    function toggleFaq(btn) {
      var item = btn.closest('.faq-item');
      var answer = item.querySelector('.faq-a');
      var isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(function (el) {
        el.classList.remove('open');
        el.querySelector('.faq-a').style.maxHeight = null;
      });
      if (!isOpen) {
        item.classList.add('open');
        answer.style.maxHeight = answer.scrollHeight + 'px';
      }
    }

    (function () {
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      var cards = document.querySelectorAll('.service-card.fade-up');
      if (!('IntersectionObserver' in window) || !cards.length) return;
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry, i) {
          if (entry.isIntersecting) {
            setTimeout(function () { entry.target.classList.add('in-view'); }, i * 60);
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.15 });
      cards.forEach(function (card) { observer.observe(card); });
    })();
  