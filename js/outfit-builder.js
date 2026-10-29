// <outfit-builder>: pick garments and a fabric, see the look on the avatar, request it as a sample.
// The catalogue, specs and image paths live in outfit-config.js (window.OUTFIT_CONFIG).
(() => {
  const CSS = `
    outfit-builder{--ob-sel:var(--green-600,#1F9457);--ob-dark:var(--green-800,#11402A);--ob-g2:#ECECEE;--ob-line:rgba(0,0,0,.08);--ob-ease:cubic-bezier(.23,1,.32,1);--ob-press:cubic-bezier(.66,0,.15,1);--ob-spring:cubic-bezier(.34,1.56,.64,1);--ob-cw:clamp(358px,calc(8.125vw + 254px),410px);display:flex;justify-content:center;align-items:center;gap:56px}

    /* Entrance: the library unfolds in 3D, the avatar rises, the hangtag drops in on a spring */
    .ob-card{opacity:0;transform:perspective(1200px) translateX(-30px) rotateY(16deg);transform-origin:0 50%;transition:opacity .7s var(--ob-ease) .1s,transform 1s var(--ob-ease) .1s}
    .ob-stage{opacity:0;transform:translateY(24px) scale(.97);transition:opacity .7s var(--ob-ease),transform 1s var(--ob-ease)}
    .ob-tagwrap{opacity:0;transform:translateY(-48px) rotate(-14deg);transition:opacity .5s var(--ob-ease) .4s,transform 1.3s var(--ob-spring) .4s}
    outfit-builder.in .ob-card,outfit-builder.in .ob-tagwrap{opacity:1;transform:none}
    outfit-builder.in .ob-stage{opacity:1;transform:perspective(1000px) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg))}
    outfit-builder.in .ob-stage.tilting{transition:transform .15s linear}

    /* Library card */
    .ob-card{width:clamp(360px,34vw,480px);padding:0 20px 20px;border:1px solid rgba(255,255,255,.7);border-radius:18px;background:rgba(250,250,251,.72);-webkit-backdrop-filter:blur(40px) saturate(1.5);backdrop-filter:blur(40px) saturate(1.5);box-shadow:0 4px 12px rgba(0,0,0,.06),0 12px 32px -8px rgba(0,0,0,.12)}
    .ob-bar{position:relative;display:flex;align-items:center;justify-content:center;height:30px;margin:0 -20px 12px;border-radius:17px 17px 0 0;background:rgba(0,0,0,.04);font-size:13px;font-weight:500;color:#5B5E63}
    .ob-bar svg{position:absolute;right:12px;width:13px;height:13px;color:#9A9DA2}
    .ob-label{margin:0 0 8px;font-size:13px;font-weight:500;line-height:1.3;color:#8A8D92}
    .ob-label + .ob-grid + .ob-label{margin-top:12px;padding-top:12px;border-top:1px solid var(--ob-line)}
    .ob-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
    /* Tiles lean toward the pointer (--tx/--ty set from JS) */
    .ob-tile{display:block;padding:4px;border-radius:8px;transform:perspective(500px) rotateX(var(--tx,0deg)) rotateY(var(--ty,0deg));transition:transform .3s var(--ob-press)}
    button.ob-tile:active{transform:perspective(500px) rotateX(var(--tx,0deg)) rotateY(var(--ty,0deg)) scale(.96)}
    .ob-pic{position:relative;display:grid;place-items:center;aspect-ratio:76/62;overflow:hidden;border-radius:4px;background:var(--ob-g2);outline:2px solid transparent;outline-offset:3px;transition:outline-color .2s,box-shadow .3s}
    .ob-tile:hover .ob-pic{box-shadow:0 12px 20px -12px rgba(15,31,23,.45)}
    .ob-garments .ob-pic{aspect-ratio:76/101}
    .ob-tile[aria-pressed="true"] .ob-pic,.ob-tile[aria-checked="true"] .ob-pic{outline-color:var(--ob-sel)}
    button.ob-tile:focus-visible{outline:2px solid var(--ob-sel);outline-offset:2px}
    .ob-pic img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;transform-origin:0 0}
    .ob-swatch .ob-pic img{padding:4px}
    .ob-name{display:none;padding:4px;font-size:11.5px;font-weight:600;color:#666;text-align:center;line-height:1.3}
    .ob-pic.noimg img{display:none}
    .ob-pic.noimg .ob-name{display:block}
    .ob-swatch .ob-pic.noimg{background:var(--sw)}
    .ob-swatch .ob-pic.noimg .ob-name{color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.45)}

    /* Avatar card */
    .ob-view{position:relative;flex:none;margin-right:190px}
    .ob-stage{position:relative;width:var(--ob-cw);height:clamp(550px,calc(12.5vw + 390px),630px);margin:0;overflow:hidden;border:1px solid #E3E4E6;border-radius:24px;background:rgba(250,250,251,.6);-webkit-backdrop-filter:blur(40px) saturate(1.5);backdrop-filter:blur(40px) saturate(1.5)}
    /* Garment change: the new look turns in, the old one turns away */
    .ob-stage img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;opacity:0;transform:perspective(900px) rotateY(-14deg) scale(.98);transition:opacity .5s,transform .7s var(--ob-ease)}
    .ob-stage img.enter{transition:none;transform:perspective(900px) rotateY(14deg) scale(.98)}
    .ob-stage img.on{opacity:1;transform:none}
    /* Fabric change: the new fabric drapes down over the old one */
    .ob-stage img.drape{z-index:1;transition:none;animation:obDrape .9s var(--ob-ease)}
    @keyframes obDrape{from{clip-path:inset(0 0 100% 0)}to{clip-path:inset(0)}}
    .ob-glare{position:absolute;inset:0;z-index:2;pointer-events:none;background:radial-gradient(380px circle at var(--gx,50%) var(--gy,0%),rgba(255,255,255,.4),transparent 50%);opacity:0;transition:opacity .4s}
    .ob-stage.tilting .ob-glare{opacity:1}
    /* Announced to screen readers only, the picture speaks for itself */
    .ob-stage figcaption{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}

    /* Spec hangtag, hung off the avatar card; swings when the look changes */
    .ob-tagwrap{position:absolute;left:calc(100% - 40px);top:30px;z-index:3;width:250px;transform-origin:50% 0}
    .ob-tagwrap.swing{animation:obSwing 1.7s ease-out}
    @keyframes obSwing{0%{transform:perspective(700px)}14%{transform:perspective(700px) rotate(-7deg) rotateY(22deg)}34%{transform:perspective(700px) rotate(5deg) rotateY(-14deg)}54%{transform:perspective(700px) rotate(-2.5deg) rotateY(7deg)}76%{transform:perspective(700px) rotate(1deg) rotateY(-2deg)}100%{transform:perspective(700px)}}
    .ob-string{display:block;width:60px;height:46px;margin:0 auto -14px;overflow:visible}
    .ob-tag{position:relative;padding:30px 18px 16px;border-radius:16px 16px 12px 12px;background:#fff;box-shadow:0 2px 4px rgba(15,31,23,.05),0 22px 40px -18px rgba(15,31,23,.35);font-size:12.5px;color:#0F1F17}
    .ob-hole{position:absolute;top:11px;left:50%;width:12px;height:12px;margin-left:-6px;border-radius:50%;background:#F0F2F1;box-shadow:inset 0 1px 2px rgba(15,31,23,.3)}
    .ob-brand{display:flex;justify-content:space-between;align-items:baseline;gap:8px;padding-bottom:10px;border-bottom:1.5px dashed #DCEBE1;font-size:9.5px;letter-spacing:.12em;white-space:nowrap;color:var(--ob-dark)}
    .ob-brand b{font-weight:800}
    .ob-brand span{color:#55665C;font-variant-numeric:tabular-nums;letter-spacing:.08em}
    .ob-look{margin:12px 0 10px;font-family:var(--head,inherit);font-size:17px;font-weight:600;letter-spacing:-.01em;line-height:1.2}
    .ob-specs{display:grid;grid-template-columns:auto 1fr;gap:5px 10px;margin:0 0 14px}
    .ob-specs dt{color:#55665C}
    .ob-specs dd{margin:0;font-weight:600;text-align:right}
    .ob-specs .flip{animation:obFlip .5s var(--ob-ease)}
    @keyframes obFlip{from{opacity:0;transform:perspective(300px) rotateX(-80deg)}}
    .ob-cta{display:flex;align-items:center;justify-content:center;gap:6px;height:38px;border-radius:999px;background:var(--green-700,#1A7F4B);color:#fff;font-size:13px;font-weight:600;transition:background .25s}
    .ob-cta:hover{background:var(--ob-dark)}
    .ob-cta svg{width:14px;height:14px;transition:transform .25s}
    .ob-cta:hover svg{transform:translateX(3px)}
    .ob-foot{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-top:12px;font-size:10px;color:#7A8A80}
    .ob-bars{display:flex;gap:1.5px;height:16px;opacity:.65}
    .ob-bars i{width:1.5px;background:var(--ob-dark)}
    .ob-bars i:nth-child(3n){width:3px}

    @media (max-width:960px){
      outfit-builder{flex-direction:column;gap:20px}
      .ob-view{order:-1;margin-right:0;display:flex;flex-direction:column;align-items:center}
      .ob-stage{width:300px;height:460px}
      .ob-tagwrap{position:relative;left:auto;top:auto;width:min(300px,100%);margin-top:-8px}
      .ob-card{width:100%;max-width:540px;transform:translateY(24px)}
    }
    @media (prefers-reduced-motion:reduce){
      .ob-card,.ob-stage,.ob-tagwrap,.ob-stage img{transition:opacity .3s;transform:none!important}
      .ob-tagwrap.swing,.ob-stage img.drape,.ob-specs .flip{animation:none}
    }
  `;
  const PIN = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 2l8 8-2 2-1.5-1.5-4 4 .5 4.5-2 2-4.5-4.5L3 22l-1-1 5.5-5.5L3 11l2-2 4.5.5 4-4L12 4z"/></svg>';
  const ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  const STRING = '<svg class="ob-string" viewBox="0 0 60 46" aria-hidden="true"><circle cx="30" cy="4" r="4" fill="var(--green-700,#1A7F4B)"/><path d="M30 6C21 20 22 34 28 46M30 6C39 20 38 34 32 46" fill="none" stroke="var(--green-600,#1F9457)" stroke-width="1.6" stroke-linecap="round"/></svg>';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hover = matchMedia('(hover: hover)').matches;
  const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'})[c]);
  // crop: [x%, y%, scale] zooms a full-body render onto the part of the body the garment covers
  const crop = c => c ? ` style="transform:translate(${c[0]}%,${c[1]}%) scale(${c[2]})"` : '';
  const tile = (item, attrs, cls = '') =>
    `<button type="button" class="ob-tile ${cls}" ${attrs} aria-label="${esc(item.label)}">` +
    `<span class="ob-pic"${item.color ? ` style="--sw:${item.color}"` : ''}><img src="${esc(item.thumb || '')}" alt="" loading="lazy" decoding="async"${crop(item.crop)}><span class="ob-name">${esc(item.label)}</span></span></button>`;
  const range = ([a, b]) => `${a}–${b} days`;

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
        <div class="ob-view">
          <figure class="ob-stage">
            <img alt="" class="on"><img alt="">
            <span class="ob-glare" aria-hidden="true"></span>
            <figcaption aria-live="polite"></figcaption>
          </figure>
          <div class="ob-tagwrap">${STRING}
            <article class="ob-tag" aria-label="Sample specification">
              <span class="ob-hole" aria-hidden="true"></span>
              <div class="ob-brand"><b>STRUGGLE STYLE</b><span class="ob-code"></span></div>
              <h3 class="ob-look"></h3>
              <dl class="ob-specs"></dl>
              <a class="ob-cta">Request this sample ${ARROW}</a>
              <div class="ob-foot"><span>${esc(cfg.tagNote || '')}</span><span class="ob-bars" aria-hidden="true">${'<i></i>'.repeat(18)}</span></div>
            </article>
          </div>
        </div>`;

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
        this.update(t.dataset.garment ? 'turn' : 'drape');
      });
      if (hover && !reduce) this.tilt();
      // Animate in the first time the builder scrolls into view, and only then fetch
      // the other outfits so they don't compete with the page's first load
      const io = new IntersectionObserver(([e]) => { if (e.isIntersecting) { this.classList.add('in'); this.preload(); io.disconnect(); } }, {rootMargin: '0px 0px -10% 0px'});
      io.observe(this);
      this.update();
    }

    // Tiles and the avatar card lean toward the pointer; a soft glare follows it across the card
    tilt() {
      const lean = (el, e, deg) => {
        const r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        return {x, y, rx: `${(.5 - y) * deg}deg`, ry: `${(x - .5) * deg}deg`};
      };
      const card = this.querySelector('.ob-card'), stage = this.querySelector('.ob-stage');
      card.addEventListener('pointermove', e => {
        const t = e.target.closest('.ob-tile');
        if (!t) return;
        const {rx, ry} = lean(t, e, 16);
        t.style.setProperty('--tx', rx);
        t.style.setProperty('--ty', ry);
      });
      card.addEventListener('pointerout', e => {
        const t = e.target.closest('.ob-tile');
        if (t && !t.contains(e.relatedTarget)) ['--tx', '--ty'].forEach(p => t.style.removeProperty(p));
      });
      stage.addEventListener('pointermove', e => {
        const {x, y, rx, ry} = lean(stage, e, 10);
        stage.classList.add('tilting');
        stage.style.setProperty('--rx', rx);
        stage.style.setProperty('--ry', ry);
        stage.style.setProperty('--gx', `${x * 100}%`);
        stage.style.setProperty('--gy', `${y * 100}%`);
      });
      stage.addEventListener('pointerleave', () => {
        stage.classList.remove('tilting');
        ['--rx', '--ry'].forEach(p => stage.style.removeProperty(p));
      });
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

    worn() {
      const s = this.sel;
      return [s.full, s.top, s.bottom].filter(Boolean).map(id => this.garment[id]);
    }

    lookName() {
      const s = this.sel, g = id => this.garment[id];
      return s.full ? g(s.full).label
        : s.top && s.bottom ? `${g(s.top).label} + ${g(s.bottom).label}`
        : g(s.top || s.bottom).label;
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

    // The hangtag sums up the look: style code, fabric, the strictest MOQ and the longest lead time
    renderTag(animate) {
      const worn = this.worn(), fab = this.fabric[this.sel.fabric], name = this.lookName();
      const code = `SS-${worn.map(g => g.code).join('')}-${fab.code}`;
      const lead = [Math.max(...worn.map(g => g.lead[0])), Math.max(...worn.map(g => g.lead[1]))];
      const rows = [
        ['Fabric', `${fab.label} · ${fab.gsm}`],
        ['Content', fab.comp],
        ['MOQ', `${Math.max(...worn.map(g => g.moq))} pcs / colour`],
        ['Sample', range(this.cfg.sampleDays)],
        ['Bulk', range(lead)]
      ];
      this.querySelector('.ob-code').textContent = code;
      this.querySelector('.ob-look').textContent = name;
      this.querySelector('.ob-specs').innerHTML = rows.map(([k, v], i) =>
        `<dt>${k}</dt><dd${animate ? ` class="flip" style="animation-delay:${i * 60}ms"` : ''}>${esc(v)}</dd>`).join('');
      const q = new URLSearchParams({style: code, look: name, fabric: fab.label});
      this.querySelector('.ob-cta').href = `${this.cfg.quoteUrl}?${q}`;
      if (animate && !reduce) {
        const wrap = this.querySelector('.ob-tagwrap');
        wrap.classList.remove('swing');
        void wrap.offsetWidth;
        wrap.classList.add('swing');
      }
    }

    update(mode) {
      const s = this.sel;
      this.querySelectorAll('[data-garment]').forEach(b => b.setAttribute('aria-pressed', [s.full, s.top, s.bottom].includes(b.dataset.garment)));
      this.querySelectorAll('[data-fabric]').forEach(b => b.setAttribute('aria-checked', b.dataset.fabric === s.fabric));
      const label = `${this.lookName()} · ${this.fabric[s.fabric].label}`;
      this.querySelector('figcaption').textContent = label;
      this.renderTag(!!mode);
      this.show(this.src(this.current()), label, mode);
    }

    // Load into the hidden layer, then bring it in: turn (garment), drape (fabric) or plain fade
    show(url, label, mode) {
      const token = ++this.token, [cur, next] = this.layers;
      // Settle any transition still running before reusing the hidden layer
      next.classList.remove('on', 'enter', 'drape');
      cur.classList.remove('drape');
      const reveal = () => {
        if (token !== this.token) return;
        next.alt = label;
        cur.alt = '';
        this.layers = [next, cur];
        if (mode === 'drape' && !reduce) {
          next.classList.add('drape', 'on');
          // animationend can be skipped (background tab, animation cancelled), so a timer backs it up
          const done = () => {
            clearTimeout(timer);
            next.classList.remove('drape');
            if (this.layers[1] === cur) cur.classList.remove('on');
          };
          const timer = setTimeout(done, 1000);
          next.addEventListener('animationend', done, {once: true});
          return;
        }
        if (mode === 'turn' && !reduce) {
          next.classList.add('enter');
          void next.offsetWidth;
          next.classList.remove('enter');
        }
        next.classList.add('on');
        cur.classList.remove('on');
      };
      const fallback = () => {
        if (token !== this.token) return;
        this.missing.add(url);
        next.onerror = null;
        next.src = this.placeholder(label);
      };
      next.onload = reveal;
      next.onerror = fallback;
      if (this.missing.has(url)) fallback();
      else next.src = url;
    }
  }

  customElements.define('outfit-builder', OutfitBuilder);
})();
