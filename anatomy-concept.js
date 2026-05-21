/* ====== Anatomical concept — interactions ====== */
(function() {
  const O = window.ANAT.organs;
  const C = window.ANAT.chips;

  // ── Load lab data from analyzer.html via localStorage ──
  let LAB = null;
  try {
    const raw = localStorage.getItem('hc_pe_data');
    if (raw) LAB = JSON.parse(raw);
  } catch(e) {}

  const SEV_RANK = { green: 0, yellow: 1, orange: 2, red: 3 };
  const SEV_COLOR = {
    green: '#30a060',
    yellow: '#d4a017',
    orange: '#e08020',
    red: '#d63350',
  };
  const SEV_LABEL = {
    green:  { en: 'Normal',  zh: '正常' },
    yellow: { en: 'Low',     zh: '輕度' },
    orange: { en: 'Medium',  zh: '中度' },
    red:    { en: 'High',    zh: '高度' },
  };

  // For each organ, find the worst severity across its indicators
  function organSeverity(organName) {
    if (!LAB || !LAB.classifications) return null;
    const inds = O[organName].indicators || [];
    let worst = null;
    for (const ind of inds) {
      const cls = LAB.classifications[ind.id];
      if (!cls) continue;
      if (worst === null || SEV_RANK[cls.sev] > SEV_RANK[worst]) worst = cls.sev;
    }
    return worst;
  }

  // Render header status banner + apply per-organ severity dots
  function applyLabData() {
    const banner = document.getElementById('lab-banner');
    if (LAB && LAB.timestamp) {
      const ago = new Date(LAB.timestamp);
      const dateStr = ago.toLocaleDateString();
      let flagged = 0, total = 0;
      for (const id in LAB.classifications) {
        total++;
        if (LAB.classifications[id].sev !== 'green') flagged++;
      }
      banner.innerHTML = `<span class="lb-dot lb-${flagged ? 'flag' : 'ok'}"></span><span><b>${total}</b> indicators · <b>${flagged}</b> flagged · synced ${dateStr}</span><a class="lb-clear" href="#" id="lb-clear">clear</a>`;
      banner.classList.add('show');
      document.getElementById('lb-clear').addEventListener('click', (e) => {
        e.preventDefault();
        if (confirm('Clear lab data from this device? · 清除此裝置上的檢驗資料？')) {
          localStorage.removeItem('hc_pe_data');
          location.reload();
        }
      });
    } else {
      banner.innerHTML = `<span class="lb-dot lb-empty"></span><span>No lab data yet · enter values in <a href="analyzer.html">analyzer.html</a> to light up the body · 尚未匯入檢驗資料</span>`;
      banner.classList.add('show', 'empty');
    }

    // Apply per-organ severity dots
    document.querySelectorAll('.organ').forEach(g => {
      const name = g.dataset.organ;
      const sev = organSeverity(name);
      g.removeAttribute('data-sev');
      // Remove old badge if exists
      const oldBadge = g.querySelector('.organ-sev-badge');
      if (oldBadge) oldBadge.remove();
      if (sev) {
        g.setAttribute('data-sev', sev);
        // Add a small severity dot next to the number
        const numText = g.querySelector('.organ-num');
        if (numText) {
          const x = parseFloat(numText.getAttribute('x'));
          const y = parseFloat(numText.getAttribute('y'));
          const ns = 'http://www.w3.org/2000/svg';
          const badge = document.createElementNS(ns, 'circle');
          badge.setAttribute('class', 'organ-sev-badge');
          badge.setAttribute('cx', x + 16);
          badge.setAttribute('cy', y - 3);
          badge.setAttribute('r', 4);
          badge.setAttribute('fill', SEV_COLOR[sev]);
          badge.setAttribute('stroke', '#fff');
          badge.setAttribute('stroke-width', 1.5);
          g.appendChild(badge);
        }
      }
    });
  }

  const suppsEl = document.getElementById('chip-supps');
  const practicesEl = document.getElementById('chip-practices');
  const detail = document.getElementById('detail');
  const organs = document.querySelectorAll('.organ');
  let activeOrgan = null;

  // Build chips
  function makeChip(c) {
    const btn = document.createElement('button');
    btn.className = 'chip';
    btn.dataset.organ = c.organ;
    btn.dataset.id = c.id;
    const organColor = O[c.organ].color;
    btn.innerHTML = `
      <span class="dot" style="background:${organColor}"></span>
      <span class="name">${c.name}</span>
      <span class="name-zh">${c.nameZh}</span>
    `;
    btn.addEventListener('mouseenter', () => lightOrgan(c.organ));
    btn.addEventListener('mouseleave', () => unlightAll());
    btn.addEventListener('focus', () => lightOrgan(c.organ));
    btn.addEventListener('blur', () => unlightAll());
    btn.addEventListener('click', () => selectOrgan(c.organ, btn));
    return btn;
  }
  C.supplements.forEach(c => suppsEl.appendChild(makeChip(c)));
  C.practices.forEach(c => practicesEl.appendChild(makeChip(c)));

  // Organ hover / click
  organs.forEach(o => {
    const name = o.dataset.organ;
    o.addEventListener('mouseenter', () => lightOrgan(name));
    o.addEventListener('mouseleave', () => unlightAll());
    o.addEventListener('focus', () => lightOrgan(name));
    o.addEventListener('blur', () => unlightAll());
    o.addEventListener('click', () => selectOrgan(name));
    o.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        selectOrgan(name);
      }
    });
  });

  function lightOrgan(name) {
    if (activeOrgan) return;
    organs.forEach(o => o.classList.toggle('lit', o.dataset.organ === name));
    document.querySelectorAll('.chip').forEach(c => {
      c.style.opacity = (c.dataset.organ === name) ? '1' : '0.5';
    });
  }
  function unlightAll() {
    if (activeOrgan) return;
    organs.forEach(o => o.classList.remove('lit'));
    document.querySelectorAll('.chip').forEach(c => { c.style.opacity = '1'; });
  }

  function selectOrgan(name, chip) {
    if (activeOrgan === name && !chip) {
      // Toggle off
      activeOrgan = null;
      organs.forEach(o => o.classList.remove('active', 'dim', 'lit'));
      document.querySelectorAll('.chip').forEach(c => {
        c.classList.remove('active');
        c.style.opacity = '1';
      });
      renderDetail(null);
      return;
    }
    activeOrgan = name;
    organs.forEach(o => {
      o.classList.toggle('active', o.dataset.organ === name);
      o.classList.toggle('dim', o.dataset.organ !== name);
      o.classList.remove('lit');
    });
    document.querySelectorAll('.chip').forEach(c => {
      const matches = c.dataset.organ === name;
      c.classList.toggle('active', matches && chip && c.dataset.id === chip.dataset.id);
      c.style.opacity = matches ? '1' : '0.4';
    });
    renderDetail(name);
  }

  function renderDetail(name) {
    if (!name) {
      detail.innerHTML = '<div class="detail-empty">Hover a chip above to highlight its target organ. Click an organ to see all related lab indicators · 點擊器官以查看完整檢驗項目。</div>';
      return;
    }
    const o = O[name];
    const supps = C.supplements.filter(c => c.organ === name);
    const pracs = C.practices.filter(c => c.organ === name);

    const summary = (o.summary || []).map(([lbl, val]) =>
      `<div class="detail-row"><span class="lbl">${lbl}</span><span class="val">${typeof val === 'string' ? val : val.zh}</span></div>`
    ).join('');

    const indicators = (o.indicators || []).map(ind => {
      const cls = LAB && LAB.classifications && LAB.classifications[ind.id];
      const userVal = LAB && LAB.values && LAB.values[ind.id];
      const sev = cls && cls.sev;
      const sevColor = sev ? SEV_COLOR[sev] : null;
      const sevTag = sev ? `<span class="ind-sev" style="background:${sevColor}">${SEV_LABEL[sev].zh}</span>` : '';
      const userValHtml = (userVal !== undefined && userVal !== null && userVal !== '')
        ? `<span class="ind-user" style="${sevColor ? `color:${sevColor};font-weight:600` : ''}">${userVal}</span>`
        : `<span class="ind-user empty">—</span>`;
      return `<div class="indicator-row ${sev ? 'has-data' : ''}">
        <div class="ind-meta">
          <span class="ind-name">${ind.label}</span><span class="ind-zh">${ind.labelZh || ''}</span>
          ${sevTag}
        </div>
        <div class="ind-vals">${userValHtml}<span class="ind-ref">ref · ${ind.ref}</span></div>
      </div>`;
    }).join('');

    const all = [...supps, ...pracs];
    const pills = all.map(c =>
      `<span class="pill-target" style="background:${o.colorSoft};color:${o.color}">${c.name}<span class="pt-zh">${c.nameZh}</span></span>`
    ).join('');

    detail.innerHTML = `
      <div class="detail-eyebrow">${o.num} · ${o.name.en}</div>
      <div class="detail-name">${o.name.zh}</div>
      <div class="detail-body">${o.lede.zh}</div>
      ${summary ? `<div class="detail-rows">${summary}</div>` : ''}
      ${indicators ? `<div class="detail-section">
        <div class="lbl-section"><span>Lab indicators · 檢驗項目</span><span class="count">${o.indicators.length} items</span></div>
        <div class="indicators-grid">${indicators}</div>
      </div>` : ''}
      ${pills ? `<div class="detail-section">
        <div class="lbl-section"><span>Targeted by · 對應介入</span></div>
        <div>${pills}</div>
      </div>` : ''}
    `;
  }

  /* ===== Reference image upload (optional backdrop) ===== */
  const stage = document.getElementById('body-stage');
  const bgImg = document.getElementById('body-bg');
  const upload = document.getElementById('bg-upload');
  const btnReset = document.getElementById('btn-reset');
  const LS_KEY = 'hc_anatomy_bg';

  function setReferenceImage(src) {
    if (src) {
      bgImg.src = src;
      stage.setAttribute('data-mode', 'reference');
      localStorage.setItem(LS_KEY, src);
    } else {
      bgImg.src = '';
      stage.removeAttribute('data-mode');
      localStorage.removeItem(LS_KEY);
    }
  }

  btnReset.addEventListener('click', () => setReferenceImage(null));
  upload.addEventListener('change', (e) => {
    const file = e.target.files && e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => setReferenceImage(ev.target.result);
    reader.readAsDataURL(file);
  });

  try {
    const saved = localStorage.getItem(LS_KEY);
    if (saved) setReferenceImage(saved);
  } catch(e) {}

  // Apply lab data from analyzer.html (severity dots + value rendering)
  applyLabData();
})();
