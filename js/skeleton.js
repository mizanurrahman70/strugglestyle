/* Skeleton placeholder shown while Products / Manufacturing load; fades out once the page is ready */
(function () {
  var s = document.currentScript, layout = s && s.getAttribute('data-layout');
  var css =
    '#sk{position:fixed;inset:0;z-index:40;background:#fff;padding:96px max(16px,calc((100vw - 1280px)/2 + 32px)) 0;overflow:hidden;pointer-events:none;transition:opacity .4s ease}' +
    '#sk.done{opacity:0}' +
    '#sk i{display:block;border-radius:12px;background:linear-gradient(100deg,#EAF2ED 30%,#F6FAF7 50%,#EAF2ED 70%);background-size:300% 100%;animation:sk 1.4s linear infinite}' +
    '#sk .c{display:flex;flex-direction:column;align-items:center;gap:14px}' +
    '#sk .row{display:flex;gap:20px}#sk .row>*{flex:1}' +
    '#sk .stage{display:grid;grid-template-columns:minmax(0,1fr) 400px;gap:0;height:560px;margin:0 calc(-1*max(16px,(100vw - 1280px)/2 + 32px));border-top:1px solid #DCEBE1}' +
    '#sk .stage .l{display:flex;align-items:center;justify-content:center;gap:24px;background:#F1F4F1}#sk .stage .l i{width:210px;height:380px;border-radius:24px}#sk .stage .l i:nth-child(2){width:250px;height:440px}' +
    '#sk .stage .r{padding:32px;display:grid;gap:14px;align-content:start}' +
    '@keyframes sk{from{background-position:100% 0}to{background-position:-100% 0}}' +
    '@media (max-width:900px){#sk{padding-top:84px}#sk .stage{grid-template-columns:1fr;height:auto}#sk .stage .l{height:380px}#sk .stage .l i{width:150px;height:260px}#sk .stage .l i:nth-child(2){width:180px;height:310px}#sk .stage .l i:nth-child(3){display:none}#sk .row{flex-wrap:wrap}}' +
    '@media (prefers-reduced-motion:reduce){#sk i{animation:none}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  var b = function (w, h, mt) { return '<i style="width:' + w + ';height:' + h + (mt ? ';margin-top:' + mt : '') + '"></i>'; };
  var html;
  if (layout === 'products') {
    html = '<div class="stage" style="margin-top:-12px"><div class="l">' + b('1', '1') + b('1', '1') + b('1', '1') + '</div>' +
      '<div class="r">' + b('90px', '16px') + b('70%', '34px') + b('100%', '64px', '8px') + b('100%', '64px') + b('100%', '64px') + b('100%', '52px', '14px') + '</div></div>' +
      '<div class="c" style="margin-top:72px">' + b('min(420px,80%)', '38px') + b('min(560px,90%)', '16px') + '</div>' +
      '<div class="row" style="margin-top:40px">' + b('1', '300px') + b('1', '300px') + b('1', '300px') + b('1', '300px') + '</div>';
  } else {
    html = '<div class="c" style="margin-top:32px">' + b('min(520px,80%)', '44px') + b('min(680px,92%)', '16px') + b('min(560px,86%)', '16px') + '</div>' +
      '<div class="row" style="margin-top:36px;gap:12px;flex-wrap:nowrap;overflow:hidden">' + b('190px', '46px') + b('190px', '46px') + b('190px', '46px') + b('190px', '46px') + '</div>' +
      '<div class="row" style="margin-top:28px;flex-wrap:wrap">' + b('1', '380px').replace('style="', 'style="min-width:280px;') + '<div style="flex:1;min-width:280px;display:grid;gap:14px;align-content:center">' + b('120px', '14px') + b('70%', '36px') + b('100%', '16px') + b('100%', '16px') + b('85%', '16px') + b('100%', '56px', '10px') + '</div></div>';
  }
  var el = document.createElement('div');
  el.id = 'sk'; el.setAttribute('aria-hidden', 'true');
  el.innerHTML = html.replace(/width:1;height:1/g, 'width:1;height:1');
  // flex children written as width:1 -> let them grow
  [].forEach.call(el.querySelectorAll('i'), function (i) { if (i.style.width === '1px') { i.style.width = ''; } });
  document.documentElement.appendChild(el);

  var closed = false;
  function close() {
    if (closed) return; closed = true;
    el.classList.add('done');
    setTimeout(function () { el.remove(); st.remove(); }, 450);
  }
  if (document.readyState === 'complete') close(); else window.addEventListener('load', close);
  setTimeout(close, 4000); // never keep it up longer than this
})();
