/* OpOrd — opord.co. Small, dependency-free enhancements: the mobile menu, the film, the forms,
   and the contents list on long pages. Every page works without this file. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- mobile menu ---------- */
  var menu = $('.menu-btn');
  if (menu) {
    var close = function () { document.body.classList.remove('nav-open'); menu.setAttribute('aria-expanded', 'false'); };
    menu.addEventListener('click', function () {
      var open = !document.body.classList.contains('nav-open');
      document.body.classList.toggle('nav-open', open);
      menu.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    $$('.links a').forEach(function (a) { a.addEventListener('click', close); });
    window.addEventListener('resize', function () { if (window.innerWidth > 860) close(); });
  }

  /* ---------- the film ----------
     Nothing plays until someone asks. A tap anywhere on the film, its button, or a "Watch the film"
     link starts it from the top, with sound and the browser's own controls. No autoplay, no pausing
     on scroll: the visitor is in charge. Without script, the native controls work as usual. */
  $$('.film').forEach(function (box) {
    var v = $('video', box), btn = $('.play', box);
    if (!v || !btn) return;
    btn.hidden = false; v.controls = false;          // the poster and one clear button, until it starts
    var start = function () {
      if (box.classList.contains('playing')) return;
      box.classList.add('playing');
      v.controls = true; v.muted = false;
      var p = v.play();
      if (p && p.catch) p.catch(function () {});     // if the browser refuses, the native controls are there
      v.focus({ preventScroll: true });
    };
    btn.addEventListener('click', start);
    v.addEventListener('click', function () { if (!box.classList.contains('playing')) start(); });
    $$('a[href="#film"]').forEach(function (a) { a.addEventListener('click', start); });
    v.addEventListener('ended', function () {      // back to the poster and the button, ready to watch again
      box.classList.remove('playing'); v.controls = false; v.load();
    });
  });

  /* ---------- forms posted to the OpOrd engine ---------- */
  var started = Date.now();
  $$('form[data-ajax]').forEach(function (form) {
    var status = $('.status', form), btn = $('button[type="submit"]', form);
    var done = form.parentNode.querySelector('.done');
    var show = function (msg, ok) { status.innerHTML = msg; status.className = 'status' + (ok ? ' ok' : ''); status.hidden = false; };
    var fallback = form.getAttribute('data-fallback') || '';
    form.addEventListener('submit', function (e) {
      if (!window.fetch || !window.URLSearchParams) return;   // plain form post instead
      e.preventDefault();
      status.hidden = true;
      $$('[aria-invalid]', form).forEach(function (el) { el.removeAttribute('aria-invalid'); });
      if (!form.checkValidity()) {
        var bad = $$(':invalid', form).filter(function (el) { return el.name; });
        bad.forEach(function (el) { el.setAttribute('aria-invalid', 'true'); });
        if (bad[0]) bad[0].focus();
        form.reportValidity && form.reportValidity();
        return;
      }
      var data = new URLSearchParams(new FormData(form));
      data.set('t', String(Date.now() - started));
      btn.disabled = true;
      var label = btn.textContent; btn.textContent = 'Sending…';
      fetch(form.action, { method: 'POST', body: data, headers: { Accept: 'application/json' }, credentials: 'omit' })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }).then(function (j) { return { r: r, j: j }; }); })
        .then(function (x) {
          if (x.r.ok && x.j && x.j.ok) {
            if (done) {
              var msg = $('[data-msg]', done);
              if (msg && x.j.message) msg.textContent = x.j.message;
              form.hidden = true; done.hidden = false; done.focus && done.focus();
            } else show(x.j.message || 'Received. Thank you.', true);
            form.reset();
          } else {
            show(((x.j && x.j.error) || 'That didn’t go through.') + (fallback ? ' ' + fallback : ''));
          }
        })
        .catch(function () { show('That didn’t go through. Check your connection and try again.' + (fallback ? ' ' + fallback : '')); })
        .then(function () { btn.disabled = false; btn.textContent = label; });
    });
  });

  /* ---------- the contents list on long pages ---------- */
  var toc = $('.toc');
  if (toc && 'IntersectionObserver' in window) {
    var links = $$('a[href^="#"]', toc), map = {};
    links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var heads = $$('.prose h2[id]');
    var mark = function (id) { links.forEach(function (a) { a.classList.toggle('on', a === map[id]); }); };
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) mark(e.target.id); });
    }, { rootMargin: '-15% 0px -70% 0px' });
    heads.forEach(function (h) { io.observe(h); });
  }
})();
