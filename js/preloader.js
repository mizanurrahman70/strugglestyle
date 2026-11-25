/* Home-page preloader: logo + thin gold progress line, curtain lift once the page has loaded */
(function () {
  var script = document.currentScript;
  var base = script ? script.src.replace(/js\/preloader\.js.*$/, '') : '';
    var css =
    '#pl{position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;background:#0E0E0E;pointer-events:all;transition:opacity .6s ease}' +
    '#pl .in{position:relative;z-index:2;display:flex;flex-direction:column;align-items:center;transition:opacity .45s ease,transform .6s ease}' +
    '#pl img{height:92px;width:auto;opacity:0;transform:translateY(10px);transition:opacity 1s ease,transform 1.1s cubic-bezier(.2,.7,.2,1)}' +
    '#pl img.on{opacity:1;transform:none}' +
    '#pl .bar{margin-top:34px;width:150px;height:1px;background:rgba(255,255,255,.12);overflow:hidden}' +
    '#pl .bar i{display:block;height:100%;width:100%;background:linear-gradient(90deg,#B8893A,#F0D089);transform:scaleX(0);transform-origin:0 50%;transition:transform .35s ease-out}' +
    '#pl.done{opacity:0;pointer-events:none}' +
    '@media (prefers-reduced-motion:reduce){#pl *{transition-duration:.01s!important;transition-delay:0s!important}}';
  var st = document.createElement('style'); st.textContent = css;
  document.head.appendChild(st);

  var el = document.createElement('div');
  el.id = 'pl'; el.setAttribute('role', 'status'); el.setAttribute('aria-label', 'Loading');
  el.innerHTML = '<div class="in"><img src="' + base + 'images/logo-gold-dark.svg" alt=""><div class="bar"><i></i></div></div>';
  document.documentElement.appendChild(el);
  document.documentElement.style.overflow = 'hidden';

  var img = el.querySelector('img'), fill = el.querySelector('.bar i');
  function show() { img.classList.add('on'); }
  if (img.complete) show(); else { img.onload = show; img.onerror = show; }

  var start = Date.now(), p = 0, loaded = false, closed = false, MIN = 900;
  function set(v) { p = v; fill.style.transform = 'scaleX(' + (v / 100) + ')'; }
  var tick = setInterval(function () {
    if (loaded && Date.now() - start >= MIN) { set(100); clearInterval(tick); setTimeout(close, 450); return; }
    set(p + (90 - p) * 0.08); // creep toward 90 while loading
  }, 60);

  function close() {
    if (closed) return; closed = true;
    el.classList.add('done');
    document.documentElement.style.overflow = '';
    setTimeout(function () { el.remove(); }, 700);
  }
  if (document.readyState === 'complete') loaded = true; else window.addEventListener('load', function () { loaded = true; });
  setTimeout(function () { loaded = true; MIN = 0; }, 5000); // never block longer than this
})();
