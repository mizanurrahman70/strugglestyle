// <outfit-builder>: pick garments and a fabric, show the matching pre-rendered outfit image.
// The catalogue and image paths live in outfit-config.js (window.OUTFIT_CONFIG).
(() => {
  const CSS = `
    outfit-builder{--ob-blue:#6BB3F5;--ob-g2:#ECECEE;--ob-line:rgba(0,0,0,.08);--ob-ease:cubic-bezier(.23,1,.32,1);--ob-press:cubic-bezier(.66,0,.15,1);--ob-cw:clamp(358px,calc(8.125vw + 254px),410px);display:flex;justify-content:center;align-items:center;gap:56px}
    .ob-card,.ob-stage{opacity:0;transform:translateY(16px);transition:opacity .6s var(--ob-ease),transform .6s var(--ob-ease)}
    .ob-card{width:clamp(380px,38vw,540px);transition-delay:.12s}
    outfit-builder.in .ob-card,outfit-builder.in .ob-stage{opacity:1;transform:none}

    /* Library card */
    .ob-card{padding:0 20px 20px;border:1px solid rgba(255,255,255,.7);border-radius:18px;background:rgba(250,250,251,.72);-webkit-backdrop-filter:blur(40px) saturate(1.5);backdrop-filter:blur(40px) saturate(1.5);box-shadow:0 4px 12px rgba(0,0,0,.06),0 12px 32px -8px rgba(0,0,0,.12)}
    .ob-bar{position:relative;display:flex;align-items:center;justify-content:center;height:30px;margin:0 -20px 12px;border-radius:17px 17px 0 0;background:rgba(0,0,0,.04);font-size:13px;font-weight:500;color:#5B5E63}
    .ob-bar svg{position:absolute;right:12px;width:13px;height:13px;color:#9A9DA2}
    .ob-label{margin:0 0 8px;font-size:13px;font-weight:500;line-height:1.3;color:#8A8D92}
    .ob-label + .ob-grid + .ob-label{margin-top:12px;padding-top:12px;border-top:1px solid var(--ob-line)}
    .ob-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
    .ob-tile{display:block;padding:4px;border-radius:8px;transition:transform .3s var(--ob-press)}
    button.ob-tile:active{transform:scale(.96)}
    .ob-pic{position:relative;display:grid;place-items:center;aspect-ratio:76/62;overflow:hidden;border-radius:4px;background:var(--ob-g2);outline:2px solid transparent;outline-offset:3px;transition:outline-color .2s}
    .ob-garments .ob-pic{aspect-ratio:76/101}
    .ob-tile[aria-pressed="true"] .ob-pic,.ob-tile[aria-checked="true"] .ob-pic{outline-color:var(--ob-blue)}
    button.ob-tile:focus-visible{outline:2px solid var(--ob-blue);outline-offset:2px}
    .ob-pic img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;transform-origin:0 0}
    .ob-swatch .ob-pic img{padding:4px}
    .ob-name{display:none;padding:4px;font-size:11.5px;font-weight:600;color:#666;text-align:center;line-height:1.3}
    .ob-pic.noimg img{display:none}
    .ob-pic.noimg .ob-name{display:block}
    .ob-swatch .ob-pic.noimg{background:var(--sw)}
    .ob-swatch .ob-pic.noimg .ob-name{color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.45)}

    /* Avatar card */
    .ob-stage{position:relative;flex:none;width:var(--ob-cw);height:clamp(550px,calc(12.5vw + 390px),630px);margin:0;overflow:hidden;border:1px solid #E3E4E6;border-radius:24px;background:rgba(250,250,251,.6);-webkit-backdrop-filter:blur(40px) saturate(1.5);backdrop-filter:blur(40px) saturate(1.5)}
    .ob-stage img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;opacity:0;transition:opacity .5s}
    .ob-stage img.on{opacity:1}
    /* Announced to screen readers only, the picture speaks for itself */
    .ob-stage figcaption{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}

    @media (max-width:960px){
      outfit-builder{flex-direction:column;gap:20px}
      .ob-stage{order:-1;width:300px;height:460px}
      .ob-card{width:100%;max-width:540px}
    }
    @media (prefers-reduced-motion:reduce){.ob-card,.ob-stage,.ob-stage img,.ob-tile{transition:none}}
  `;
  const PIN = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 2l8 8-2 2-1.5-1.5-4 4 .5 4.5-2 2-4.5-4.5L3 22l-1-1 5.5-5.5L3 11l2-2 4.5.5 4-4L12 4z"/></svg>';
  const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'})[c]);
  // crop: [x%, y%, scale] zooms a full-body render onto the part of the body the garment covers
  const crop = c => c ? ` style="transform:translate(${c[0]}%,${c[1]}%) scale(${c[2]})"` : '';
  const tile = (item, attrs, cls = '') =>
    `<button type="button" class="ob-tile ${cls}" ${attrs} aria-label="${esc(item.label)}">` +
    `<span class="ob-pic"${item.color ? ` style="--sw:${item.color}"` : ''}><img src="${esc(item.thumb || '')}" alt="" loading="lazy" decoding="async"${crop(item.crop)}><span class="ob-name">${esc(item.label)}</span></span></button>`;

  class OutfitBuilder extends HTMLElement {
    connectedCallback() {
      if (this.ready) return;
      this.ready = true;
      const cfg = this.cfg = window.OUTFIT_CONFIG;
      if (!document.getElementById('ob-css')) document.head.append(Object.assign(document.createElement('style'), {id: 'ob-css', textContent: CSS}));
      this.garment = Object.fromEntries(cfg.garments.map(g => [g.id, g]));
      this.fabric = Object.fromEntries(cfg.fabrics.map(f => [f.id, f]));
      this.sel = {full: null, top: null, bottom: null, fabric: cfg.defaultFabric || cfg.fabrics[0].id, ...cfg.initial};
      this.missing = new Set();
      this.token = 0;

      this.innerHTML = `
        <div class="ob-card" role="group" aria-label="Garment and fabric library">
          <div class="ob-bar">Library${PIN}</div>
          <p class="ob-label">Garments</p>
          <div class="ob-grid ob-garments">${cfg.garments.map(g => tile(g, `data-garment="${esc(g.id)}" aria-pressed="false"`)).join('')}</div>
          <p class="ob-label">Fabrics</p>
          <div class="ob-grid" role="radiogroup" aria-label="Fabric">${cfg.fabrics.map(f => tile(f, `data-fabric="${esc(f.id)}" role="radio" aria-checked="false"`, 'ob-swatch')).join('')}</div>
        </div>
        <figure class="ob-stage">
          <img alt="" class="on"><img alt="">
          <figcaption aria-live="polite"></figcaption>
        </figure>`;

      // Missing thumbnail: show the label (and the fabric colour) instead
      this.querySelectorAll('.ob-pic img').forEach(img => {
        const miss = () => img.parentNode.classList.add('noimg');
        if (!img.getAttribute('src')) miss(); else img.addEventListener('error', miss);
      });
      this.layers = [...this.querySelectorAll('.ob-stage img')];
      this.addEventListener('click', e => {
        const t = e.target.closest('[data-garment],[data-fabric]');
        if (!t) return;
        if (t.dataset.garment) this.pickGarment(t.dataset.garment);
        else this.sel.fabric = t.dataset.fabric;
        this.update();
      });
      // Cards rise in one after another the first time the builder scrolls into view
      // and fetch the other outfits only then, so they don't compete with the page's first load
      const io = new IntersectionObserver(([e]) => { if (e.isIntersecting) { this.classList.add('in'); this.preload(); io.disconnect(); } }, {rootMargin: '0px 0px -10% 0px'});
      io.observe(this);
      this.update();
    }

    pickGarment(id) {
      const s = this.sel, {type} = this.garment[id], before = {...s};
      if (type === 'full') { s.full = s.full === id ? null : id; s.top = s.bottom = null; }
      else { s.full = null; s[type] = s[type] === id ? null : id; }
      // The avatar always wears something: ignore deselecting the last garment
      if (!s.full && !s.top && !s.bottom) Object.assign(s, before);
    }

    // {first, second, fabric} -> image path
    src(k) { return this.cfg.outfit.replace(/\{(\w+)\}/g, (_, n) => k[n]); }

    current() {
      const s = this.sel;
      return {first: s.full || s.top || 'none', second: s.bottom || 'none', fabric: s.fabric};
    }

    describe() {
      const s = this.sel, g = id => this.garment[id];
      const name = s.full ? g(s.full).label
        : s.top && s.bottom ? `${g(s.top).label} + ${g(s.bottom).label}`
        : s.top ? g(s.top).longLabel || g(s.top).label
        : s.bottom ? g(s.bottom).label : 'Avatar';
      return `${name} · ${this.fabric[s.fabric].label}`;
    }

    // Every image a selection can produce, so swaps never wait on the network
    preload() {
      const ids = type => this.cfg.garments.filter(g => g.type === type).map(g => g.id);
      const pairs = [...ids('full').map(f => [f, 'none']), ...['none', ...ids('top')].flatMap(t => ['none', ...ids('bottom')].map(b => [t, b]))]
        .filter(([t, b]) => t !== 'none' || b !== 'none');
      this.cache = this.cfg.fabrics.flatMap(f => pairs.map(([first, second]) => {
        const url = this.src({first, second, fabric: f.id}), img = new Image();
        img.onerror = () => this.missing.add(url);
        img.src = url;
        return img;
      }));
    }

    placeholder(label) {
      const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 500"><g fill="#E3E6E9"><circle cx="150" cy="58" r="30"/><rect x="139" y="86" width="22" height="20" rx="6"/><path d="M98 110h104l20 150h-24l-8 170h-26l-14-150-14 150h-26l-8-170H78z"/></g><text x="150" y="468" text-anchor="middle" font-family="Inter,system-ui,sans-serif" font-size="15" font-weight="600" fill="#6B7580">${esc(label)}</text><text x="150" y="490" text-anchor="middle" font-family="Inter,system-ui,sans-serif" font-size="12" fill="#9AA3AC">Render not available yet</text></svg>`;
      return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
    }

    update() {
      const s = this.sel;
      this.querySelectorAll('[data-garment]').forEach(b => b.setAttribute('aria-pressed', [s.full, s.top, s.bottom].includes(b.dataset.garment)));
      this.querySelectorAll('[data-fabric]').forEach(b => b.setAttribute('aria-checked', b.dataset.fabric === s.fabric));
      const label = this.describe();
      this.querySelector('figcaption').textContent = label;
      this.show(this.src(this.current()), label);
    }

    // Load into the hidden layer, then crossfade it over the visible one
    show(url, label) {
      const token = ++this.token, [cur, next] = this.layers;
      const fade = () => {
        if (token !== this.token) return;
        next.alt = label;
        next.classList.add('on');
        cur.classList.remove('on');
        cur.alt = '';
        this.layers = [next, cur];
      };
      const fallback = () => {
        if (token !== this.token) return;
        this.missing.add(url);
        next.onerror = null;
        next.src = this.placeholder(label);
      };
      next.onload = fade;
      next.onerror = fallback;
      if (this.missing.has(url)) fallback();
      else next.src = url;
    }
  }

  customElements.define('outfit-builder', OutfitBuilder);
})();
