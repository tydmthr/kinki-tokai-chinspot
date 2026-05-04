/* ============ 異界巡礼 / アプリロジック ============ */

const CAT_LABELS = {
  bkyu: 'B級・カオス',
  folk: '土俗・奇祭',
  horror: '心霊・廃墟',
  mystery: '聖地・ミステリー',
};
const CAT_GLYPHS = { bkyu: '魁', folk: '祓', horror: '霊', mystery: '秘' };
const FCAT_LABELS = {
  naked: '裸祭', fire: '火祭', weird: '奇習', sex: '性祭', animal: '動物', other: 'その他'
};
const MONTHS = ['睦月','如月','弥生','卯月','皐月','水無月','文月','葉月','長月','神無月','霜月','師走'];
const KAMEYAMA = [136.4506, 34.8597]; // 三重県亀山市

// ============ Tab Switching ============
const tabs = document.querySelectorAll('.tab');
const views = { hero: '#view-hero', map: '#view-map', calendar: '#view-calendar', list: '#view-list' };

function showView(name) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.querySelector(views[name]).classList.add('active');
  tabs.forEach(t => t.classList.toggle('active', t.dataset.tab === name));
  window.scrollTo({ top: 0, behavior: 'instant' });
  if (name === 'map' && map) {
    setTimeout(() => map.resize(), 100);
  }
}

tabs.forEach(t => t.addEventListener('click', () => showView(t.dataset.tab)));
document.querySelectorAll('[data-goto]').forEach(b => {
  b.addEventListener('click', () => showView(b.dataset.goto));
});
document.querySelectorAll('.cat-card[data-cat]').forEach(c => {
  c.addEventListener('click', () => {
    activeCats.clear();
    activeCats.add(c.dataset.cat);
    showView('map');
    setTimeout(applyMapFilter, 200);
    syncCatChips();
  });
});

// ============ MAP ============
let map = null;
let activeCats = new Set(['all']);
let showSpots = true;
let showFests = true;
let searchQuery = '';
let allMarkers = [];

function initMap() {
  map = new maplibregl.Map({
    container: 'map',
    style: 'https://tiles.openfreemap.org/styles/positron',
    center: [136.0, 34.9],
    zoom: 7.2,
    minZoom: 6,
    maxZoom: 17,
  });
  map.addControl(new maplibregl.NavigationControl(), 'top-right');
  map.addControl(new maplibregl.ScaleControl({ unit: 'metric' }), 'bottom-left');

  map.on('load', () => {
    // ダーク化フィルタ風の上塗りはせず、positronをそのまま使用（見やすい）
    addAllMarkers();
    applyMapFilter();
    fitBoundsToVisible();
  });
}

function addAllMarkers() {
  // クリア
  allMarkers.forEach(m => m.marker.remove());
  allMarkers = [];

  SPOTS.forEach(s => {
    const el = document.createElement('div');
    el.className = `spot-marker cat-${s.category}`;
    el.textContent = CAT_GLYPHS[s.category];
    el.title = s.name;
    el.addEventListener('click', e => {
      e.stopPropagation();
      openSpotDetail(s);
    });
    const m = new maplibregl.Marker({ element: el })
      .setLngLat([s.lng, s.lat])
      .addTo(map);
    allMarkers.push({ type: 'spot', data: s, marker: m, el });
  });

  FESTIVALS.forEach(f => {
    const el = document.createElement('div');
    el.className = `spot-marker is-fest cat-mystery`;
    const inner = document.createElement('span');
    inner.textContent = '祭';
    el.appendChild(inner);
    el.title = f.name;
    el.addEventListener('click', e => {
      e.stopPropagation();
      openFestivalDetail(f);
    });
    const m = new maplibregl.Marker({ element: el })
      .setLngLat([f.lng, f.lat])
      .addTo(map);
    allMarkers.push({ type: 'fest', data: f, marker: m, el });
  });
}

function applyMapFilter() {
  const q = searchQuery.trim().toLowerCase();
  let visibleCount = 0;
  allMarkers.forEach(({ type, data, el }) => {
    let show = true;
    if (type === 'spot' && !showSpots) show = false;
    if (type === 'fest' && !showFests) show = false;
    if (show && type === 'spot' && !activeCats.has('all') && !activeCats.has(data.category)) show = false;
    if (show && q) {
      const hay = `${data.name} ${data.name_kana||''} ${data.prefecture||''} ${data.city||''} ${data.shrine||''} ${data.summary||''}`.toLowerCase();
      if (!hay.includes(q)) show = false;
    }
    el.style.display = show ? '' : 'none';
    if (show) visibleCount++;
  });
  renderResultList();
}

function renderResultList() {
  const list = document.getElementById('resultList');
  const q = searchQuery.trim().toLowerCase();
  const items = allMarkers
    .filter(({ type, data }) => {
      if (type === 'spot' && !showSpots) return false;
      if (type === 'fest' && !showFests) return false;
      if (type === 'spot' && !activeCats.has('all') && !activeCats.has(data.category)) return false;
      if (q) {
        const hay = `${data.name} ${data.name_kana||''} ${data.prefecture||''} ${data.city||''} ${data.shrine||''}`.toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    })
    .slice(0, 200);

  list.innerHTML = `<div style="font-size:11px;color:var(--gray);letter-spacing:.2em;padding:0 4px 8px;">該当 ${items.length} 件</div>` + items.map(({ type, data }) => {
    const cat = type === 'spot' ? `cat-${data.category}` : 'is-festival';
    const meta = type === 'spot'
      ? `${data.prefecture}${data.city||''} ／ ${CAT_LABELS[data.category]}`
      : `${data.prefecture}${data.city||''} ／ ${data.date_pattern}`;
    return `<div class="result-item ${cat}" data-id="${data.id}" data-type="${type}">
      <div class="ri-name">${data.name}</div>
      <div class="ri-meta">${meta}</div>
    </div>`;
  }).join('');

  list.querySelectorAll('.result-item').forEach(el => {
    el.addEventListener('click', () => {
      const id = el.dataset.id;
      const type = el.dataset.type;
      const data = type === 'spot' ? SPOTS.find(s => s.id === id) : FESTIVALS.find(f => f.id === id);
      if (!data) return;
      map.flyTo({ center: [data.lng, data.lat], zoom: 13, speed: 1.4 });
      setTimeout(() => {
        if (type === 'spot') openSpotDetail(data);
        else openFestivalDetail(data);
      }, 600);
    });
  });
}

function fitBoundsToVisible() {
  const visible = allMarkers.filter(m => m.el.style.display !== 'none');
  if (visible.length === 0) return;
  const bounds = new maplibregl.LngLatBounds();
  visible.forEach(m => bounds.extend([m.data.lng, m.data.lat]));
  map.fitBounds(bounds, { padding: 60, duration: 0 });
}

function syncCatChips() {
  document.querySelectorAll('#catFilter .cat-chip').forEach(chip => {
    const cat = chip.dataset.cat;
    chip.classList.toggle('active', activeCats.has(cat));
  });
}

// Sidebar Filter Events
document.querySelectorAll('#catFilter .cat-chip').forEach(chip => {
  chip.addEventListener('click', () => {
    const cat = chip.dataset.cat;
    if (cat === 'all') {
      activeCats = new Set(['all']);
    } else {
      activeCats.delete('all');
      if (activeCats.has(cat)) activeCats.delete(cat);
      else activeCats.add(cat);
      if (activeCats.size === 0) activeCats.add('all');
    }
    syncCatChips();
    applyMapFilter();
  });
});

document.getElementById('spotSearch').addEventListener('input', e => {
  searchQuery = e.target.value;
  applyMapFilter();
});
document.getElementById('showSpots').addEventListener('change', e => { showSpots = e.target.checked; applyMapFilter(); });
document.getElementById('showFests').addEventListener('change', e => { showFests = e.target.checked; applyMapFilter(); });

// Sidebar toggle on mobile
document.getElementById('sidebarToggle').addEventListener('click', () => {
  document.getElementById('mapSidebar').classList.toggle('open');
});

// Counts
function updateCounts() {
  const counts = { all: SPOTS.length, folk: 0, bkyu: 0, horror: 0, mystery: 0 };
  SPOTS.forEach(s => counts[s.category]++);
  Object.keys(counts).forEach(k => {
    const el = document.getElementById('cnt-' + k);
    if (el) el.textContent = ` (${counts[k]})`;
  });
}
updateCounts();

// ============ DETAIL MODAL ============
const modal = document.getElementById('modal');
const modalContent = document.getElementById('modalContent');

function openModal(html) {
  modalContent.innerHTML = html + '<button class="modal-close" id="modalClose" aria-label="閉じる"><i class="ph ph-x"></i></button>';
  modal.classList.add('open');
  modal.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
  document.getElementById('modalClose').addEventListener('click', closeModal);
}
function closeModal() {
  modal.classList.remove('open');
  modal.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
}
modal.querySelector('[data-close]').addEventListener('click', closeModal);
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

function openSpotDetail(s) {
  const isHorror = s.category === 'horror';
  const html = `
    <p class="m-cat">${CAT_LABELS[s.category]} ／ ${s.status}</p>
    <h2 class="m-name">${s.name}</h2>
    <p class="m-kana">${s.name_kana || ''}</p>
    <div class="m-meta-grid">
      <div class="m-meta-item"><span class="ml">所在地</span><span class="mv">${s.address || s.prefecture + s.city}</span></div>
      <div class="m-meta-item"><span class="ml">料金 / 時間</span><span class="mv">${s.fee || '—'} ／ ${s.hours || '—'}</span></div>
      ${s.from_kameyama ? `<div class="m-meta-item"><span class="ml">亀山から</span><span class="mv">${s.from_kameyama}</span></div>` : ''}
      <div class="m-meta-item"><span class="ml">座標</span><span class="mv">${s.lat.toFixed(4)}, ${s.lng.toFixed(4)}</span></div>
    </div>
    ${isHorror ? `<div class="m-warn"><strong>注意</strong>：心霊・廃墟スポットは私有地・立入禁止区域を含む場合があります。本サイトは来歴・歴史記録としての掲載で、来訪を推奨するものではありません。</div>` : ''}
    <div class="m-section">
      <h3 class="m-h">概要</h3>
      <p class="m-summary">${s.summary}</p>
    </div>
    ${s.highlights && s.highlights.length ? `
    <div class="m-section">
      <h3 class="m-h">見どころ</h3>
      <ul class="m-highlights">${s.highlights.map(h => `<li>${h}</li>`).join('')}</ul>
    </div>` : ''}
    <div class="m-section">
      <h3 class="m-h">外部リンク</h3>
      <div class="m-links">
        ${s.official_url ? `<a class="m-link" href="${s.official_url}" target="_blank" rel="noopener"><i class="ph ph-globe"></i>公式</a>` : ''}
        ${(s.reference_urls||[]).map((u,i) => `<a class="m-link" href="${u}" target="_blank" rel="noopener"><i class="ph ph-link"></i>参考${(s.reference_urls.length>1)?(i+1):''}</a>`).join('')}
        <a class="m-link" href="https://www.google.com/maps?q=${s.lat},${s.lng}" target="_blank" rel="noopener"><i class="ph ph-map-pin"></i>Google Maps</a>
      </div>
    </div>
  `;
  openModal(html);
}

function openFestivalDetail(f) {
  const dateStr = f.date_2026 ? formatDate(f.date_2026, f.date_2026_end) : f.date_pattern;
  const html = `
    <p class="m-cat">奇祭 ／ ${FCAT_LABELS[f.category] || f.category}</p>
    <h2 class="m-name">${f.name}</h2>
    <p class="m-kana">${f.name_kana || ''} ／ ${f.shrine || ''}</p>
    <div class="m-meta-grid">
      <div class="m-meta-item"><span class="ml">開催地</span><span class="mv">${f.prefecture}${f.city || ''}</span></div>
      <div class="m-meta-item"><span class="ml">日程</span><span class="mv">${dateStr}<br><small style="color:var(--gray);font-size:10px">${f.date_pattern}</small></span></div>
      <div class="m-meta-item"><span class="ml">座標</span><span class="mv">${f.lat.toFixed(4)}, ${f.lng.toFixed(4)}</span></div>
    </div>
    <div class="m-section">
      <h3 class="m-h">概要</h3>
      <p class="m-summary">${f.summary}</p>
    </div>
    ${f.highlights && f.highlights.length ? `
    <div class="m-section">
      <h3 class="m-h">見どころ</h3>
      <ul class="m-highlights">${f.highlights.map(h => `<li>${h}</li>`).join('')}</ul>
    </div>` : ''}
    ${f.origin ? `
    <div class="m-section">
      <h3 class="m-h">起源・由来</h3>
      <p class="m-summary">${f.origin}</p>
    </div>` : ''}
    ${f.viewing_notes ? `
    <div class="m-section">
      <h3 class="m-h">観覧の心得</h3>
      <p class="m-summary">${f.viewing_notes}</p>
    </div>` : ''}
    <div class="m-section">
      <h3 class="m-h">外部リンク</h3>
      <div class="m-links">
        ${f.official_url ? `<a class="m-link" href="${f.official_url}" target="_blank" rel="noopener"><i class="ph ph-globe"></i>公式</a>` : ''}
        ${(f.reference_urls||[]).map((u,i) => `<a class="m-link" href="${u}" target="_blank" rel="noopener"><i class="ph ph-link"></i>参考${(f.reference_urls.length>1)?(i+1):''}</a>`).join('')}
        <a class="m-link" href="https://www.google.com/maps?q=${f.lat},${f.lng}" target="_blank" rel="noopener"><i class="ph ph-map-pin"></i>Google Maps</a>
      </div>
    </div>
  `;
  openModal(html);
}

function formatDate(iso, end) {
  const d = new Date(iso + 'T00:00:00+09:00');
  const m = d.getMonth() + 1, day = d.getDate();
  const wd = ['日','月','火','水','木','金','土'][d.getDay()];
  let s = `2026年${m}月${day}日（${wd}）`;
  if (end) {
    const ed = new Date(end + 'T00:00:00+09:00');
    s += ` 〜 ${ed.getMonth()+1}月${ed.getDate()}日`;
  }
  return s;
}

// ============ CALENDAR ============
let activeFestCat = 'all';

function buildCalendar() {
  const grid = document.getElementById('calGrid');
  // 2026年5月から2027年4月までの12ヶ月（年-月のキーを順序立てて）
  const monthKeys = [];
  for (let i = 0; i < 12; i++) {
    const m = ((4 + i) % 12) + 1; // 5→4(idx)
    const y = i < 8 ? 2026 : 2027;
    monthKeys.push({ year: y, month: m });
  }

  // 各祭を該当月にバケット振り分け
  const buckets = {};
  monthKeys.forEach(k => buckets[`${k.year}-${k.month}`] = []);

  FESTIVALS.forEach(f => {
    if (activeFestCat !== 'all' && f.category !== activeFestCat) return;
    if (f.date_2026) {
      const d = new Date(f.date_2026 + 'T00:00:00+09:00');
      const key = `${d.getFullYear()}-${d.getMonth()+1}`;
      if (buckets[key]) buckets[key].push({ f, day: d.getDate() });
      // 終了日が翌月にまたがる場合
      if (f.date_2026_end) {
        const ed = new Date(f.date_2026_end + 'T00:00:00+09:00');
        const ekey = `${ed.getFullYear()}-${ed.getMonth()+1}`;
        if (ekey !== key && buckets[ekey]) {
          buckets[ekey].push({ f, day: ed.getDate(), continued: true });
        }
      }
    } else {
      // 日付が定まらないものは月パターンから推測（ベストエフォート）
      const m = (f.date_pattern || '').match(/(\d+)月/);
      if (m) {
        const month = parseInt(m[1]);
        // 2026 or 2027 を該当する方に
        const year = month >= 5 ? 2026 : 2027;
        const key = `${year}-${month}`;
        if (buckets[key]) buckets[key].push({ f, day: null });
      }
    }
  });

  // ソート
  Object.keys(buckets).forEach(k => buckets[k].sort((a, b) => (a.day || 99) - (b.day || 99)));

  grid.innerHTML = monthKeys.map(k => {
    const items = buckets[`${k.year}-${k.month}`];
    return `
      <div class="month-block">
        <div class="month-header">
          <span class="month-num">${k.month}</span>
          <div>
            <div class="month-name">${MONTHS[k.month - 1]}</div>
            <div style="font-size:10px;color:var(--gray);letter-spacing:.15em">${k.year}年</div>
          </div>
          <span class="month-count">${items.length} 祭</span>
        </div>
        <div class="fest-list">
          ${items.length === 0 ? '<div style="padding:20px;text-align:center;color:var(--gray);font-size:12px">該当なし</div>'
            : items.map(({ f, day, continued }) => `
              <div class="fest-item" data-fcat="${f.category}" data-id="${f.id}">
                <div class="fest-date">${day || '?'}<small>${continued ? '結願' : (day ? '日' : '')}</small></div>
                <div class="fest-info">
                  <div class="fest-name">${f.name}<span class="fest-tag">${FCAT_LABELS[f.category]}</span></div>
                  <div class="fest-place">${f.prefecture}${f.city || ''} ／ ${f.shrine || ''}</div>
                </div>
              </div>
            `).join('')}
        </div>
      </div>
    `;
  }).join('');

  grid.querySelectorAll('.fest-item').forEach(el => {
    el.addEventListener('click', () => {
      const f = FESTIVALS.find(x => x.id === el.dataset.id);
      if (f) openFestivalDetail(f);
    });
  });
}

document.querySelectorAll('#calCatFilter .cat-chip').forEach(chip => {
  chip.addEventListener('click', () => {
    document.querySelectorAll('#calCatFilter .cat-chip').forEach(c => c.classList.remove('active'));
    chip.classList.add('active');
    activeFestCat = chip.dataset.fcat;
    buildCalendar();
  });
});

// ============ LIST VIEW ============
let listTab = 'spots';
let listQuery = '';

function buildList() {
  const grid = document.getElementById('listGrid');
  const q = listQuery.trim().toLowerCase();
  let items;
  if (listTab === 'spots') {
    items = SPOTS.filter(s => {
      if (!q) return true;
      const hay = `${s.name} ${s.name_kana||''} ${s.prefecture} ${s.city||''} ${CAT_LABELS[s.category]}`.toLowerCase();
      return hay.includes(q);
    });
    grid.innerHTML = items.map(s => `
      <div class="list-card cat-${s.category}" data-id="${s.id}" data-type="spot">
        <p class="lc-cat">${CAT_LABELS[s.category]}</p>
        <h3 class="lc-name">${s.name}</h3>
        <p class="lc-kana">${s.name_kana || ''}</p>
        <p class="lc-place"><i class="ph ph-map-pin"></i>${s.prefecture}${s.city || ''}</p>
        <p class="lc-summary">${s.summary}</p>
        <span class="lc-status s-${s.status}">${s.status}</span>
      </div>
    `).join('');
  } else {
    items = FESTIVALS.filter(f => {
      if (!q) return true;
      const hay = `${f.name} ${f.name_kana||''} ${f.prefecture} ${f.city||''} ${f.shrine||''} ${FCAT_LABELS[f.category]}`.toLowerCase();
      return hay.includes(q);
    });
    grid.innerHTML = items.map(f => `
      <div class="list-card is-festival" data-id="${f.id}" data-type="fest">
        <p class="lc-cat">奇祭 ／ ${FCAT_LABELS[f.category]}</p>
        <h3 class="lc-name">${f.name}</h3>
        <p class="lc-kana">${f.name_kana || ''}</p>
        <p class="lc-place"><i class="ph ph-map-pin"></i>${f.prefecture}${f.city || ''}</p>
        <p class="lc-place"><i class="ph ph-calendar-blank"></i>${f.date_pattern}</p>
        <p class="lc-summary">${f.summary}</p>
      </div>
    `).join('');
  }
  grid.querySelectorAll('.list-card').forEach(el => {
    el.addEventListener('click', () => {
      const id = el.dataset.id;
      const type = el.dataset.type;
      if (type === 'spot') openSpotDetail(SPOTS.find(s => s.id === id));
      else openFestivalDetail(FESTIVALS.find(f => f.id === id));
    });
  });
}

document.querySelectorAll('.list-tab').forEach(t => {
  t.addEventListener('click', () => {
    document.querySelectorAll('.list-tab').forEach(x => x.classList.remove('active'));
    t.classList.add('active');
    listTab = t.dataset.listtab;
    buildList();
  });
});
document.getElementById('listSearch').addEventListener('input', e => {
  listQuery = e.target.value;
  buildList();
});

// ============ INIT ============
window.addEventListener('DOMContentLoaded', () => {
  initMap();
  buildCalendar();
  buildList();
});
