/* ============ 異界巡礼 / アプリロジック v2 ============ */

const CAT_GLYPHS = { bkyu: '魁', folk: '祓', horror: '霊', mystery: '秘' };
const KAMEYAMA = [136.4506, 34.8597];

// ============ Visited / Wishlist (LocalStorage) ============
const STORAGE_KEY_VISITED = 'bizjp_visited';
const STORAGE_KEY_WISHLIST = 'bizjp_wishlist';

function loadSet(key) {
  try { return new Set(JSON.parse(localStorage.getItem(key) || '[]')); }
  catch { return new Set(); }
}
function saveSet(key, set) {
  localStorage.setItem(key, JSON.stringify([...set]));
}
let visitedSet = loadSet(STORAGE_KEY_VISITED);
let wishlistSet = loadSet(STORAGE_KEY_WISHLIST);

function toggleVisited(id) {
  if (visitedSet.has(id)) visitedSet.delete(id); else visitedSet.add(id);
  saveSet(STORAGE_KEY_VISITED, visitedSet);
  applyMapFilter();
  refreshThisMonth();
}
function toggleWishlist(id) {
  if (wishlistSet.has(id)) wishlistSet.delete(id); else wishlistSet.add(id);
  saveSet(STORAGE_KEY_WISHLIST, wishlistSet);
}

// ============ Tab Switching ============
const tabs = document.querySelectorAll('.tab');
const views = { hero: '#view-hero', map: '#view-map', calendar: '#view-calendar', list: '#view-list', routes: '#view-routes' };

function showView(name) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  const target = document.querySelector(views[name]);
  if (target) target.classList.add('active');
  tabs.forEach(t => t.classList.toggle('active', t.dataset.tab === name));
  window.scrollTo({ top: 0, behavior: 'instant' });
  if (name === 'map' && map) {
    setTimeout(() => map.resize(), 100);
  }
  // URL更新（履歴を汚さずreplaceState）
  const u = new URL(location.href);
  if (name === 'hero') u.searchParams.delete('view'); else u.searchParams.set('view', name);
  history.replaceState(null, '', u);
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
    setTimeout(() => { applyMapFilter(); fitBoundsToVisible(); }, 200);
    syncCatChips();
  });
});

// ============ Theme Toggle ============
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');
function setTheme(t) {
  document.body.dataset.theme = t;
  localStorage.setItem('bizjp_theme', t);
  if (themeIcon) themeIcon.className = t === 'dark' ? 'ph ph-moon' : 'ph ph-sun';
}
const savedTheme = localStorage.getItem('bizjp_theme');
if (savedTheme) setTheme(savedTheme);
themeToggle.addEventListener('click', () => {
  setTheme(document.body.dataset.theme === 'dark' ? 'light' : 'dark');
});

// ============ Lang Toggle ============
document.getElementById('langToggle').addEventListener('click', () => {
  setLang(CURRENT_LANG === 'ja' ? 'en' : 'ja');
});

// ============ MAP ============
let map = null;
let activeCats = new Set(['all']);
let activeRegions = new Set(['all']);
let showSpots = true;
let showFests = true;
let showVisitedOnly = false;
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
    addAllMarkers();
    applyMapFilter();
    fitBoundsToVisible();
  });
}

function addAllMarkers() {
  allMarkers.forEach(m => m.marker.remove());
  allMarkers = [];

  SPOTS.forEach(s => {
    // wrapper: MapLibreが position transform をここに設定する。CSSで transform を上書きしないこと
    const el = document.createElement('div');
    el.className = 'spot-marker-wrap';
    // inner: 見た目・ホバー拡大・菱形回転はこちらで受ける
    const inner = document.createElement('div');
    inner.className = `spot-marker cat-${s.category}`;
    inner.textContent = CAT_GLYPHS[s.category];
    el.appendChild(inner);
    el.title = s.name;
    el.addEventListener('click', e => {
      e.stopPropagation();
      openSpotDetail(s);
    });
    const m = new maplibregl.Marker({ element: el })
      .setLngLat([s.lng, s.lat])
      .addTo(map);
    allMarkers.push({ type: 'spot', data: s, marker: m, el, inner });
  });

  FESTIVALS.forEach(f => {
    const el = document.createElement('div');
    el.className = 'spot-marker-wrap';
    const inner = document.createElement('div');
    inner.className = 'spot-marker is-fest cat-mystery';
    const label = document.createElement('span');
    label.textContent = '祭';
    inner.appendChild(label);
    el.appendChild(inner);
    el.title = f.name;
    el.addEventListener('click', e => {
      e.stopPropagation();
      openFestivalDetail(f);
    });
    const m = new maplibregl.Marker({ element: el })
      .setLngLat([f.lng, f.lat])
      .addTo(map);
    allMarkers.push({ type: 'fest', data: f, marker: m, el, inner });
  });
}

function applyMapFilter() {
  const q = searchQuery.trim().toLowerCase();
  let visibleCount = 0;
  allMarkers.forEach(({ type, data, el, inner }) => {
    let show = true;
    if (type === 'spot' && !showSpots) show = false;
    if (type === 'fest' && !showFests) show = false;
    if (show && type === 'spot' && !activeCats.has('all') && !activeCats.has(data.category)) show = false;
    if (show && !activeRegions.has('all') && !activeRegions.has(data.prefecture)) show = false;
    if (show && showVisitedOnly && !visitedSet.has(data.id)) show = false;
    // 訪問済みマーク（wrapperではなくinnerに付与：CSSは .spot-marker.visited に効くため）
    if (inner) {
      inner.classList.toggle('visited', visitedSet.has(data.id));
      inner.classList.toggle('wishlisted', wishlistSet.has(data.id));
    }
    if (show && q) {
      const hay = `${data.name} ${data.name_kana||''} ${data.name_en||''} ${data.prefecture||''} ${data.city||''} ${data.shrine||''} ${data.summary||''} ${data.summary_en||''}`.toLowerCase();
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
      if (!activeRegions.has('all') && !activeRegions.has(data.prefecture)) return false;
      if (showVisitedOnly && !visitedSet.has(data.id)) return false;
      if (q) {
        const hay = `${data.name} ${data.name_kana||''} ${data.name_en||''} ${data.prefecture||''} ${data.city||''} ${data.shrine||''}`.toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    })
    .slice(0, 200);

  list.innerHTML = `<div class="result-count">${CURRENT_LANG === 'en' ? `${items.length} matches` : `該当 ${items.length} 件`}</div>` + items.map(({ type, data }) => {
    const cat = type === 'spot' ? `cat-${data.category}` : 'is-festival';
    const name = pick(data, 'name', 'name_en') || data.name;
    const meta = type === 'spot'
      ? `${pick(data,'prefecture','prefecture_en')}${pick(data,'city','city_en')||''} ／ ${catLabel(data.category)}`
      : `${pick(data,'prefecture','prefecture_en')}${pick(data,'city','city_en')||''} ／ ${pick(data,'date_pattern','date_pattern_en')}`;
    const visited = visitedSet.has(data.id) ? '<i class="ph-fill ph-check-circle"></i>' : '';
    return `<div class="result-item ${cat}" data-id="${data.id}" data-type="${type}">
      <div class="ri-name">${name} ${visited}</div>
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

// Region filter (built dynamically)
function buildRegionFilter() {
  const regions = [...new Set([...SPOTS, ...FESTIVALS].map(d => d.prefecture).filter(Boolean))].sort();
  const wrap = document.getElementById('regionFilter');
  if (!wrap) return;
  wrap.innerHTML = `<button class="cat-chip active" data-region="all">${t('filter.all')}</button>` +
    regions.map(r => `<button class="cat-chip" data-region="${r}">${r}</button>`).join('');
  wrap.querySelectorAll('.cat-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const r = chip.dataset.region;
      if (r === 'all') {
        activeRegions = new Set(['all']);
      } else {
        activeRegions.delete('all');
        if (activeRegions.has(r)) activeRegions.delete(r);
        else activeRegions.add(r);
        if (activeRegions.size === 0) activeRegions.add('all');
      }
      wrap.querySelectorAll('.cat-chip').forEach(c => {
        const rc = c.dataset.region;
        c.classList.toggle('active', activeRegions.has(rc));
      });
      applyMapFilter();
    });
  });
}

document.getElementById('spotSearch').addEventListener('input', e => {
  searchQuery = e.target.value;
  applyMapFilter();
});
document.getElementById('showSpots').addEventListener('change', e => { showSpots = e.target.checked; applyMapFilter(); });
document.getElementById('showFests').addEventListener('change', e => { showFests = e.target.checked; applyMapFilter(); });
document.getElementById('showVisited').addEventListener('change', e => { showVisitedOnly = e.target.checked; applyMapFilter(); });

document.getElementById('sidebarToggle').addEventListener('click', () => {
  document.getElementById('mapSidebar').classList.toggle('open');
});

function updateCounts() {
  const counts = { all: SPOTS.length, folk: 0, bkyu: 0, horror: 0, mystery: 0 };
  SPOTS.forEach(s => counts[s.category]++);
  Object.keys(counts).forEach(k => {
    const el = document.getElementById('cnt-' + k);
    if (el) el.textContent = ` (${counts[k]})`;
  });
}

// ============ DETAIL MODAL ============
const modal = document.getElementById('modal');
const modalContent = document.getElementById('modalContent');

function openModal(html) {
  modalContent.innerHTML = html + '<button class="modal-close" id="modalClose" aria-label="close"><i class="ph ph-x"></i></button>';
  modal.classList.add('open');
  modal.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
  document.getElementById('modalClose').addEventListener('click', closeModal);
}
function closeModal() {
  modal.classList.remove('open');
  modal.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
  // URLからspot/festival params取り除き
  const u = new URL(location.href);
  u.searchParams.delete('spot');
  u.searchParams.delete('festival');
  history.replaceState(null, '', u);
}
modal.querySelector('[data-close]').addEventListener('click', closeModal);
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

function difficultyStars(n) {
  if (!n) return '—';
  return '★'.repeat(n) + '☆'.repeat(Math.max(0, 5 - n));
}

function buildPhotoBlock(item) {
  if (!item.photo) return '';
  const credit = item.photo_credit || 'Source unknown';
  return `
    <div class="m-photo">
      <img src="${item.photo}" alt="${pick(item,'name','name_en')}" loading="lazy" onerror="this.parentNode.style.display='none'"/>
      <p class="m-photo-credit">${t('m.photoCredit')}: ${credit}</p>
    </div>`;
}

function buildAccessBlock(a) {
  if (!a) return '';
  const rows = [];
  if (a.nearest_station) rows.push(`<div class="m-meta-item"><span class="ml">${t('m.station')}</span><span class="mv">${a.nearest_station}${a.walking_minutes ? ` (徒歩${a.walking_minutes}分)` : ''}</span></div>`);
  if (a.bus_info) rows.push(`<div class="m-meta-item"><span class="ml">${t('m.busInfo')}</span><span class="mv">${a.bus_info}</span></div>`);
  if (a.parking) rows.push(`<div class="m-meta-item"><span class="ml">${t('m.parking')}</span><span class="mv">${a.parking}</span></div>`);
  if (a.difficulty) rows.push(`<div class="m-meta-item"><span class="ml">${t('m.difficulty')}</span><span class="mv">${difficultyStars(a.difficulty)}</span></div>`);
  if (a.best_season) rows.push(`<div class="m-meta-item"><span class="ml">${t('m.bestSeason')}</span><span class="mv">${a.best_season}</span></div>`);
  if (a.time_required) rows.push(`<div class="m-meta-item"><span class="ml">${t('m.timeRequired')}</span><span class="mv">${a.time_required}</span></div>`);
  if (rows.length === 0) return '';
  let warningsHtml = '';
  if (a.warnings && a.warnings.length) {
    warningsHtml = `<div class="m-warn"><strong>${t('m.warnings')}</strong>: <ul style="margin-top:6px">${a.warnings.map(w => `<li>${w}</li>`).join('')}</ul></div>`;
  }
  return `
    <div class="m-section">
      <h3 class="m-h">${t('m.access')}</h3>
      <div class="m-meta-grid">${rows.join('')}</div>
      ${warningsHtml}
    </div>`;
}

function buildVisitButtons(id) {
  const visited = visitedSet.has(id);
  const wished = wishlistSet.has(id);
  return `
    <div class="m-visit">
      <button class="visit-btn ${wished ? 'active' : ''}" data-action="wishlist" data-id="${id}">
        <i class="ph${wished ? '-fill' : ''} ph-bookmark-simple"></i> ${t('m.visit.want')}
      </button>
      <button class="visit-btn ${visited ? 'active' : ''}" data-action="visited" data-id="${id}">
        <i class="ph${visited ? '-fill' : ''} ph-check-circle"></i> ${t('m.visit.went')}
      </button>
      <button class="visit-btn" data-action="share" data-id="${id}">
        <i class="ph ph-share-network"></i> ${t('m.share')}
      </button>
    </div>`;
}

function getYouTubeQuery(item) {
  // 祭の場合のみYouTube埋め込みを表示
  if (!item.shrine) return null;
  const q = `${item.name} 祭 ${item.prefecture}`;
  return `https://www.youtube.com/results?search_query=${encodeURIComponent(q)}`;
}

// Markdown links [text](url) → HTML <a> 、改行を <br> に変換
function renderMdLinks(text) {
  if (!text) return '';
  const escaped = String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
  // Convert [text](url) to <a>
  const linked = escaped.replace(
    /\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g,
    '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>'
  );
  return linked.replace(/\n/g, '<br>');
}

function buildDeepdiveBlock(item) {
  const d = item.deepdive;
  if (!d) return '';
  const sections = [];

  // 歴史・伝承
  if (d.history_jp) {
    sections.push(`
      <details class="m-deep" open>
        <summary class="m-deep-h"><i class="ph ph-scroll"></i> 歴史・伝承</summary>
        <div class="m-deep-body">${renderMdLinks(d.history_jp)}</div>
      </details>`);
  }
  if (d.cultural_context_jp) {
    sections.push(`
      <details class="m-deep">
        <summary class="m-deep-h"><i class="ph ph-globe-hemisphere-east"></i> 文化的位置づけ</summary>
        <div class="m-deep-body">${renderMdLinks(d.cultural_context_jp)}</div>
      </details>`);
  }
  if (d.local_perspective_jp) {
    sections.push(`
      <details class="m-deep">
        <summary class="m-deep-h"><i class="ph ph-users-three"></i> 地元の視点</summary>
        <div class="m-deep-body">${renderMdLinks(d.local_perspective_jp)}</div>
      </details>`);
  }
  if (d.related_works) {
    sections.push(`
      <details class="m-deep">
        <summary class="m-deep-h"><i class="ph ph-books"></i> 関連作品・人物</summary>
        <div class="m-deep-body">${renderMdLinks(d.related_works)}</div>
      </details>`);
  }
  if (d.trivia) {
    sections.push(`
      <details class="m-deep">
        <summary class="m-deep-h"><i class="ph ph-lightbulb"></i> 豆知識</summary>
        <div class="m-deep-body">${renderMdLinks(d.trivia)}</div>
      </details>`);
  }
  if (d.best_visit_time || d.photo_tips || d.warnings_extra) {
    const tips = [];
    if (d.best_visit_time) tips.push(`<p><strong>ベスト訪問時期：</strong>${renderMdLinks(d.best_visit_time)}</p>`);
    if (d.photo_tips) tips.push(`<p><strong>写真スポット：</strong>${renderMdLinks(d.photo_tips)}</p>`);
    if (d.warnings_extra) tips.push(`<p><strong>注意事項：</strong>${renderMdLinks(d.warnings_extra)}</p>`);
    sections.push(`
      <details class="m-deep">
        <summary class="m-deep-h"><i class="ph ph-camera"></i> 訪問・撮影のヒント</summary>
        <div class="m-deep-body">${tips.join('')}</div>
      </details>`);
  }
  if (d.external_reviews) {
    sections.push(`
      <details class="m-deep" open>
        <summary class="m-deep-h"><i class="ph ph-newspaper-clipping"></i> 他の人の訪問記</summary>
        <div class="m-deep-body m-reviews">${renderMdLinks(d.external_reviews)}</div>
      </details>`);
  }
  if (d.sources) {
    sections.push(`
      <details class="m-deep">
        <summary class="m-deep-h"><i class="ph ph-quotes"></i> 参考出典</summary>
        <div class="m-deep-body m-sources">${renderMdLinks(d.sources)}</div>
      </details>`);
  }
  if (sections.length === 0) return '';
  return `
    <div class="m-section m-deepdive">
      <h3 class="m-h"><i class="ph ph-binoculars"></i> 深掘り情報</h3>
      ${sections.join('')}
    </div>`;
}

// 関連スポット推薦：同じ連携ルート または 同都道府県・近距離
function buildRelatedSpotsBlock(item) {
  const isFest = !!item.shrine;
  const all = [...SPOTS, ...FESTIVALS];
  // 距離計算（km）
  const dist = (a, b) => {
    const R = 6371, toRad = x => x * Math.PI / 180;
    const dLat = toRad(b.lat - a.lat);
    const dLng = toRad(b.lng - a.lng);
    const A = Math.sin(dLat/2)**2 + Math.cos(toRad(a.lat))*Math.cos(toRad(b.lat))*Math.sin(dLng/2)**2;
    return 2 * R * Math.asin(Math.sqrt(A));
  };
  const candidates = all
    .filter(x => x.id !== item.id)
    .map(x => ({ item: x, d: dist(item, x) }))
    .filter(x => x.d <= 30) // 半径30km
    .sort((a, b) => a.d - b.d)
    .slice(0, 5);
  if (candidates.length === 0) return '';
  const cards = candidates.map(({ item: x, d }) => {
    const label = x.shrine ? '奇祭' : catLabel(x.category);
    const name = pick(x, 'name', 'name_en');
    const photo = x.photo_url ? `<div class="rel-thumb" style="background-image:url('${x.photo_url}')"></div>` : `<div class="rel-thumb rel-thumb-empty">${x.shrine ? '奇' : '珍'}</div>`;
    return `
      <a class="rel-card" data-rel-id="${x.id}" data-rel-type="${x.shrine ? 'fest' : 'spot'}">
        ${photo}
        <div class="rel-body">
          <span class="rel-cat">${label} ・ ${d.toFixed(1)}km</span>
          <strong class="rel-name">${name}</strong>
          <span class="rel-loc">${x.prefecture||''}${x.city||''}</span>
        </div>
      </a>`;
  }).join('');
  return `
    <div class="m-section">
      <h3 class="m-h"><i class="ph ph-map-trifold"></i> この近くの珍スポット・奇祭</h3>
      <div class="m-related">${cards}</div>
    </div>`;
}

function bindRelatedClicks() {
  modalContent.querySelectorAll('.rel-card').forEach(c => {
    c.addEventListener('click', () => {
      const id = c.dataset.relId;
      const type = c.dataset.relType;
      const list = type === 'fest' ? FESTIVALS : SPOTS;
      const item = list.find(x => x.id === id);
      if (!item) return;
      closeModal();
      setTimeout(() => {
        if (type === 'fest') openFestivalDetail(item);
        else openSpotDetail(item);
      }, 200);
    });
  });
}

function openSpotDetail(s) {
  const isHorror = s.category === 'horror';
  const name = pick(s, 'name', 'name_en');
  const summary = pick(s, 'summary', 'summary_en');
  const highlights = pickArr(s, 'highlights', 'highlights_en');
  const pref = pick(s, 'prefecture', 'prefecture_en');
  const city = pick(s, 'city', 'city_en');

  const html = `
    ${buildPhotoBlock(s)}
    <p class="m-cat">${catLabel(s.category)} ／ ${s.status || ''}</p>
    <h2 class="m-name">${name}</h2>
    ${s.name_kana ? `<p class="m-kana">${s.name_kana}</p>` : ''}
    ${CURRENT_LANG === 'en' && s.name ? `<p class="m-kana" style="color:var(--gold)">${s.name}</p>` : ''}
    ${buildVisitButtons(s.id)}
    <div class="m-meta-grid">
      <div class="m-meta-item"><span class="ml">${t('m.location')}</span><span class="mv">${s.address || pref + city}</span></div>
      <div class="m-meta-item"><span class="ml">${t('m.fee')} / ${t('m.hours')}</span><span class="mv">${s.fee || '—'} ／ ${s.hours || '—'}</span></div>
      ${s.from_kameyama ? `<div class="m-meta-item"><span class="ml">${t('m.fromKameyama')}</span><span class="mv">${s.from_kameyama}</span></div>` : ''}
      <div class="m-meta-item"><span class="ml">${t('m.coords')}</span><span class="mv">${s.lat.toFixed(4)}, ${s.lng.toFixed(4)}</span></div>
    </div>
    ${isHorror ? `<div class="m-warn"><strong>!</strong> ${t('m.warningHorror')}</div>` : ''}
    <div class="m-section">
      <h3 class="m-h">${t('m.summary')}</h3>
      <p class="m-summary">${summary}</p>
    </div>
    ${highlights && highlights.length ? `
    <div class="m-section">
      <h3 class="m-h">${t('m.highlights')}</h3>
      <ul class="m-highlights">${highlights.map(h => `<li>${h}</li>`).join('')}</ul>
    </div>` : ''}
    ${buildAccessBlock(s.access)}
    ${buildVisitDiaryButton(s.id) ? `<div class="m-section v-diary-section">${buildVisitDiaryButton(s.id)}</div>` : ''}
    ${buildDeepdiveBlock(s)}
    ${buildRelatedSpotsBlock(s)}
    <div class="m-section">
      <h3 class="m-h">${t('m.links')}</h3>
      <div class="m-links">
        ${s.official_url ? `<a class="m-link" href="${s.official_url}" target="_blank" rel="noopener"><i class="ph ph-globe"></i>${t('m.official')}</a>` : ''}
        ${(s.reference_urls||[]).map((u,i) => `<a class="m-link" href="${u}" target="_blank" rel="noopener"><i class="ph ph-link"></i>${t('m.reference')}${(s.reference_urls.length>1)?(i+1):''}</a>`).join('')}
        <a class="m-link" href="https://www.google.com/maps?q=${s.lat},${s.lng}" target="_blank" rel="noopener"><i class="ph ph-map-pin"></i>${t('m.maps')}</a>
      </div>
    </div>
  `;
  openModal(html);
  bindVisitButtons();
  bindRelatedClicks();
  bindVisitDiaryButton();
  // URL更新
  const u = new URL(location.href);
  u.searchParams.set('spot', s.id);
  history.replaceState(null, '', u);
}

function openFestivalDetail(f) {
  const dateStr = f.date_2026 ? formatDate(f.date_2026, f.date_2026_end) : pick(f, 'date_pattern', 'date_pattern_en');
  const name = pick(f, 'name', 'name_en');
  const summary = pick(f, 'summary', 'summary_en');
  const highlights = pickArr(f, 'highlights', 'highlights_en');
  const origin = pick(f, 'origin', 'origin_en');
  const viewing = pick(f, 'viewing_notes', 'viewing_notes_en');
  const pref = pick(f, 'prefecture', 'prefecture_en');
  const city = pick(f, 'city', 'city_en');
  const shrine = pick(f, 'shrine', 'shrine_en');
  const yt = getYouTubeQuery(f);

  const html = `
    ${buildPhotoBlock(f)}
    <p class="m-cat">${CURRENT_LANG === 'en' ? 'Festival' : '奇祭'} ／ ${fcatLabel(f.category)}</p>
    <h2 class="m-name">${name}</h2>
    ${f.name_kana ? `<p class="m-kana">${f.name_kana} ／ ${shrine}</p>` : ''}
    ${CURRENT_LANG === 'en' && f.name ? `<p class="m-kana" style="color:var(--gold)">${f.name}</p>` : ''}
    ${buildVisitButtons(f.id)}
    <div class="m-meta-grid">
      <div class="m-meta-item"><span class="ml">${t('m.held')}</span><span class="mv">${pref}${city || ''}</span></div>
      <div class="m-meta-item"><span class="ml">${t('m.date')}</span><span class="mv">${dateStr}<br><small style="color:var(--gray);font-size:10px">${pick(f,'date_pattern','date_pattern_en')}</small></span></div>
      <div class="m-meta-item"><span class="ml">${t('m.coords')}</span><span class="mv">${f.lat.toFixed(4)}, ${f.lng.toFixed(4)}</span></div>
    </div>
    <div class="m-section">
      <h3 class="m-h">${t('m.summary')}</h3>
      <p class="m-summary">${summary}</p>
    </div>
    ${highlights && highlights.length ? `
    <div class="m-section">
      <h3 class="m-h">${t('m.highlights')}</h3>
      <ul class="m-highlights">${highlights.map(h => `<li>${h}</li>`).join('')}</ul>
    </div>` : ''}
    ${origin ? `
    <div class="m-section">
      <h3 class="m-h">${t('m.origin')}</h3>
      <p class="m-summary">${origin}</p>
    </div>` : ''}
    ${viewing ? `
    <div class="m-section">
      <h3 class="m-h">${t('m.viewing')}</h3>
      <p class="m-summary">${viewing}</p>
    </div>` : ''}
    ${buildAccessBlock(f.access)}
    ${buildVisitDiaryButton(f.id) ? `<div class="m-section v-diary-section">${buildVisitDiaryButton(f.id)}</div>` : ''}
    ${buildDeepdiveBlock(f)}
    ${buildRelatedSpotsBlock(f)}
    <div class="m-section">
      <h3 class="m-h">${t('m.links')}</h3>
      <div class="m-links">
        ${f.official_url ? `<a class="m-link" href="${f.official_url}" target="_blank" rel="noopener"><i class="ph ph-globe"></i>${t('m.official')}</a>` : ''}
        ${(f.reference_urls||[]).map((u,i) => `<a class="m-link" href="${u}" target="_blank" rel="noopener"><i class="ph ph-link"></i>${t('m.reference')}${(f.reference_urls.length>1)?(i+1):''}</a>`).join('')}
        <a class="m-link" href="https://www.google.com/maps?q=${f.lat},${f.lng}" target="_blank" rel="noopener"><i class="ph ph-map-pin"></i>${t('m.maps')}</a>
        ${yt ? `<a class="m-link" href="${yt}" target="_blank" rel="noopener"><i class="ph ph-youtube-logo"></i>YouTube</a>` : ''}
      </div>
    </div>
  `;
  openModal(html);
  bindVisitButtons();
  bindRelatedClicks();
  bindVisitDiaryButton();
  const u = new URL(location.href);
  u.searchParams.set('festival', f.id);
  history.replaceState(null, '', u);
}

function bindVisitButtons() {
  modalContent.querySelectorAll('.visit-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.id;
      const action = btn.dataset.action;
      if (action === 'visited') {
        toggleVisited(id);
        const isVisited = visitedSet.has(id);
        btn.classList.toggle('active', isVisited);
        btn.querySelector('i').className = `ph${isVisited ? '-fill' : ''} ph-check-circle`;
      } else if (action === 'wishlist') {
        toggleWishlist(id);
        const isW = wishlistSet.has(id);
        btn.classList.toggle('active', isW);
        btn.querySelector('i').className = `ph${isW ? '-fill' : ''} ph-bookmark-simple`;
      } else if (action === 'share') {
        const url = `${location.origin}${location.pathname}?spot=${id}`;
        const altUrl = `${location.origin}${location.pathname}?festival=${id}`;
        const shareUrl = SPOTS.find(s => s.id === id) ? url : altUrl;
        const title = document.querySelector('.m-name')?.textContent || 'Bizarre Japan';
        if (navigator.share) {
          navigator.share({ title, url: shareUrl }).catch(()=>{});
        } else {
          navigator.clipboard.writeText(shareUrl);
          btn.innerHTML = `<i class="ph ph-check"></i> ${CURRENT_LANG === 'en' ? 'Copied!' : 'コピーしました'}`;
          setTimeout(() => {
            btn.innerHTML = `<i class="ph ph-share-network"></i> ${t('m.share')}`;
          }, 1800);
        }
      }
    });
  });
}

function formatDate(iso, end) {
  const d = new Date(iso + 'T00:00:00+09:00');
  const m = d.getMonth() + 1, day = d.getDate();
  const wdJa = ['日','月','火','水','木','金','土'][d.getDay()];
  const wdEn = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][d.getDay()];
  let s = CURRENT_LANG === 'en'
    ? `${monthName(m)} ${day}, 2026 (${wdEn})`
    : `2026年${m}月${day}日（${wdJa}）`;
  if (end) {
    const ed = new Date(end + 'T00:00:00+09:00');
    s += CURRENT_LANG === 'en'
      ? ` – ${monthName(ed.getMonth()+1)} ${ed.getDate()}`
      : ` 〜 ${ed.getMonth()+1}月${ed.getDate()}日`;
  }
  return s;
}

// ============ CALENDAR ============
let activeFestCat = 'all';

function buildCalendar() {
  const grid = document.getElementById('calGrid');
  const monthKeys = [];
  for (let i = 0; i < 12; i++) {
    const m = ((4 + i) % 12) + 1;
    const y = i < 8 ? 2026 : 2027;
    monthKeys.push({ year: y, month: m });
  }
  const buckets = {};
  monthKeys.forEach(k => buckets[`${k.year}-${k.month}`] = []);

  FESTIVALS.forEach(f => {
    if (activeFestCat !== 'all' && f.category !== activeFestCat) return;
    if (f.date_2026) {
      const d = new Date(f.date_2026 + 'T00:00:00+09:00');
      const key = `${d.getFullYear()}-${d.getMonth()+1}`;
      if (buckets[key]) buckets[key].push({ f, day: d.getDate() });
      if (f.date_2026_end) {
        const ed = new Date(f.date_2026_end + 'T00:00:00+09:00');
        const ekey = `${ed.getFullYear()}-${ed.getMonth()+1}`;
        if (ekey !== key && buckets[ekey]) {
          buckets[ekey].push({ f, day: ed.getDate(), continued: true });
        }
      }
    } else {
      const m = (f.date_pattern || '').match(/(\d+)月/);
      if (m) {
        const month = parseInt(m[1]);
        const year = month >= 5 ? 2026 : 2027;
        const key = `${year}-${month}`;
        if (buckets[key]) buckets[key].push({ f, day: null });
      }
    }
  });

  Object.keys(buckets).forEach(k => buckets[k].sort((a, b) => (a.day || 99) - (b.day || 99)));

  grid.innerHTML = monthKeys.map(k => {
    const items = buckets[`${k.year}-${k.month}`];
    return `
      <div class="month-block">
        <div class="month-header">
          <span class="month-num">${k.month}</span>
          <div>
            <div class="month-name">${monthName(k.month)}</div>
            <div class="month-year">${k.year}</div>
          </div>
          <span class="month-count">${items.length}${CURRENT_LANG === 'en' ? '' : ' 祭'}</span>
        </div>
        <div class="fest-list">
          ${items.length === 0 ? `<div class="fest-empty">${CURRENT_LANG === 'en' ? 'None' : '該当なし'}</div>`
            : items.map(({ f, day, continued }) => `
              <div class="fest-item" data-fcat="${f.category}" data-id="${f.id}">
                <div class="fest-date">${day || '?'}<small>${continued ? (CURRENT_LANG==='en'?'end':'結願') : (day ? (CURRENT_LANG==='en'?'':'日') : '')}</small></div>
                <div class="fest-info">
                  <div class="fest-name">${pick(f,'name','name_en')}<span class="fest-tag">${fcatLabel(f.category)}</span></div>
                  <div class="fest-place">${pick(f,'prefecture','prefecture_en')}${pick(f,'city','city_en') || ''} ／ ${pick(f,'shrine','shrine_en') || ''}</div>
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
      const hay = `${s.name} ${s.name_kana||''} ${s.name_en||''} ${s.prefecture} ${s.city||''} ${catLabel(s.category)}`.toLowerCase();
      return hay.includes(q);
    });
    grid.innerHTML = items.map(s => `
      <div class="list-card cat-${s.category} ${visitedSet.has(s.id)?'is-visited':''}" data-id="${s.id}" data-type="spot">
        ${s.photo ? `<div class="lc-photo"><img src="${s.photo}" alt="${s.name}" loading="lazy" onerror="this.parentNode.style.display='none'"/></div>` : ''}
        <div class="lc-body">
          <p class="lc-cat">${catLabel(s.category)}</p>
          <h3 class="lc-name">${pick(s,'name','name_en')}</h3>
          ${s.name_kana ? `<p class="lc-kana">${s.name_kana}</p>` : ''}
          <p class="lc-place"><i class="ph ph-map-pin"></i>${pick(s,'prefecture','prefecture_en')}${pick(s,'city','city_en') || ''}</p>
          <p class="lc-summary">${(pick(s,'summary','summary_en')||'').slice(0, 120)}${(pick(s,'summary','summary_en')||'').length>120?'…':''}</p>
          ${s.access?.difficulty ? `<p class="lc-difficulty">${difficultyStars(s.access.difficulty)}</p>` : ''}
          ${visitedSet.has(s.id) ? `<span class="lc-visited"><i class="ph-fill ph-check-circle"></i></span>` : ''}
        </div>
      </div>
    `).join('');
  } else {
    items = FESTIVALS.filter(f => {
      if (!q) return true;
      const hay = `${f.name} ${f.name_kana||''} ${f.name_en||''} ${f.prefecture} ${f.city||''} ${f.shrine||''} ${fcatLabel(f.category)}`.toLowerCase();
      return hay.includes(q);
    });
    grid.innerHTML = items.map(f => `
      <div class="list-card is-festival ${visitedSet.has(f.id)?'is-visited':''}" data-id="${f.id}" data-type="fest">
        ${f.photo ? `<div class="lc-photo"><img src="${f.photo}" alt="${f.name}" loading="lazy" onerror="this.parentNode.style.display='none'"/></div>` : ''}
        <div class="lc-body">
          <p class="lc-cat">${CURRENT_LANG==='en'?'Festival':'奇祭'} ／ ${fcatLabel(f.category)}</p>
          <h3 class="lc-name">${pick(f,'name','name_en')}</h3>
          ${f.name_kana ? `<p class="lc-kana">${f.name_kana}</p>` : ''}
          <p class="lc-place"><i class="ph ph-map-pin"></i>${pick(f,'prefecture','prefecture_en')}${pick(f,'city','city_en') || ''}</p>
          <p class="lc-place"><i class="ph ph-calendar-blank"></i>${pick(f,'date_pattern','date_pattern_en')}</p>
          <p class="lc-summary">${(pick(f,'summary','summary_en')||'').slice(0, 120)}${(pick(f,'summary','summary_en')||'').length>120?'…':''}</p>
          ${visitedSet.has(f.id) ? `<span class="lc-visited"><i class="ph-fill ph-check-circle"></i></span>` : ''}
        </div>
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

// ============ This Month Section ============
function refreshThisMonth() {
  const block = document.getElementById('thisMonthBlock');
  const grid = document.getElementById('thisMonthGrid');
  const sub = document.getElementById('thisMonthSub');
  if (!block || !grid) return;

  const now = new Date();
  // JST今日0時を基準に「今日以降」を判定
  const todayJST = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const month = now.getMonth() + 1;

  // date_2026 があり「今日以降」の祭を日付昇順で上位5件
  // （date_pattern のみの祭は厳密日付不明のため今回は除外）
  let monthFests = FESTIVALS
    .filter(f => f.date_2026)
    .map(f => ({ f, dt: new Date(f.date_2026 + 'T00:00:00+09:00') }))
    .filter(x => x.dt >= todayJST)
    .sort((a, b) => a.dt - b.dt)
    .slice(0, 5)
    .map(x => x.f);

  sub.textContent = CURRENT_LANG === 'en'
    ? `${monthName(month)} — ${monthFests.length} extraordinary days ahead`
    : `${month}月（${monthName(month)}） — これから訪れるヤバい日々`;

  if (monthFests.length === 0) {
    grid.innerHTML = `<p class="tm-empty">${CURRENT_LANG === 'en' ? 'No upcoming festivals registered — explore the map instead.' : '今後の登録奇祭はありません。地図から珍スポットを巡ってみてください。'}</p>`;
    return;
  }
  grid.innerHTML = monthFests.map(f => `
    <div class="tm-card" data-id="${f.id}">
      ${f.photo ? `<div class="tm-photo"><img src="${f.photo}" alt="${f.name}" loading="lazy" onerror="this.parentNode.style.display='none'"/></div>` : `<div class="tm-photo-placeholder">祭</div>`}
      <div class="tm-body">
        <p class="tm-date">${f.date_2026 ? formatDate(f.date_2026) : pick(f,'date_pattern','date_pattern_en')}</p>
        <h4 class="tm-name">${pick(f,'name','name_en')}</h4>
        <p class="tm-place">${pick(f,'prefecture','prefecture_en')}${pick(f,'city','city_en')||''}</p>
        <p class="tm-tag">${fcatLabel(f.category)}</p>
      </div>
    </div>
  `).join('');
  grid.querySelectorAll('.tm-card').forEach(el => {
    el.addEventListener('click', () => {
      const f = FESTIVALS.find(x => x.id === el.dataset.id);
      if (f) openFestivalDetail(f);
    });
  });
}

// ============ Routes View ============
function buildRoutes() {
  const grid = document.getElementById('routesGrid');
  if (!grid) return;
  grid.innerHTML = ROUTES.map(r => {
    const title = CURRENT_LANG === 'en' ? r.title_en : r.title_ja;
    const desc = CURRENT_LANG === 'en' ? r.desc_en : r.desc_ja;
    const duration = CURRENT_LANG === 'en' ? r.duration_en : r.duration_ja;
    const season = CURRENT_LANG === 'en' ? r.season_en : r.season_ja;
    const stops = (r.spots || []).map(id => SPOTS.find(s => s.id === id)).filter(Boolean)
      .concat((r.festivals || []).map(id => FESTIVALS.find(f => f.id === id)).filter(Boolean));
    const stopList = stops.map(s => `<li>${pick(s,'name','name_en')}</li>`).join('');
    return `
      <article class="route-card cat-${r.cat}">
        <div class="route-glyph">${r.glyph}</div>
        <h3 class="route-title">${title}</h3>
        <div class="route-meta">
          <span><i class="ph ph-clock"></i>${duration}</span>
          <span><i class="ph ph-calendar"></i>${season}</span>
        </div>
        <p class="route-desc">${desc}</p>
        <ol class="route-stops">${stopList}</ol>
        <button class="route-cta" data-route="${r.id}">
          <i class="ph ph-map-trifold"></i> ${CURRENT_LANG === 'en' ? 'Open in Map' : '地図で開く'}
        </button>
      </article>
    `;
  }).join('');

  grid.querySelectorAll('.route-cta').forEach(btn => {
    btn.addEventListener('click', () => {
      const route = ROUTES.find(r => r.id === btn.dataset.route);
      if (!route) return;
      drawRoute(route);
      showView('map');
    });
  });
}

let activeRouteLayer = null;
function drawRoute(route) {
  if (!map) return;
  const coords = getRouteCoords(route);
  if (coords.length < 2) return;
  const lineCoords = coords.map(c => [c.lng, c.lat]);
  // 既存ルートを消す
  if (map.getLayer('route-line')) map.removeLayer('route-line');
  if (map.getSource('route')) map.removeSource('route');
  map.addSource('route', {
    type: 'geojson',
    data: { type: 'Feature', geometry: { type: 'LineString', coordinates: lineCoords } }
  });
  map.addLayer({
    id: 'route-line',
    type: 'line',
    source: 'route',
    paint: {
      'line-color': '#c8332b',
      'line-width': 3,
      'line-dasharray': [2, 2],
      'line-opacity': 0.8
    }
  });
  // すべてに収まるzoom
  const bounds = new maplibregl.LngLatBounds();
  lineCoords.forEach(c => bounds.extend(c));
  map.fitBounds(bounds, { padding: 80, duration: 1200 });
}

// ============ URL Param handler ============
function handleUrlParams() {
  const url = new URLSearchParams(location.search);
  const view = url.get('view');
  if (view && views[view]) showView(view);
  const spotId = url.get('spot');
  const festId = url.get('festival');
  if (spotId) {
    const s = SPOTS.find(x => x.id === spotId);
    if (s) setTimeout(() => openSpotDetail(s), 300);
  } else if (festId) {
    const f = FESTIVALS.find(x => x.id === festId);
    if (f) setTimeout(() => openFestivalDetail(f), 300);
  }
}

// ============ Submit Form Link ============
// GitHub Issues template-based submission (no auth wall, multilingual, version-controlled)
const submitFormUrl = 'https://github.com/tydmthr/kinki-tokai-chinspot/issues/new?labels=spot-submission&template=spot-submission.md&title=%5B%E6%96%B0%E3%82%B9%E3%83%9D%E3%83%83%E3%83%88%5D+';
const submitBtn = document.getElementById('submitForm');
if (submitBtn) {
  submitBtn.href = submitFormUrl;
}

// ============ Refresh hook for language toggle ============
window.refreshAll = function() {
  updateCounts();
  buildRegionFilter();
  buildCalendar();
  buildList();
  buildRoutes();
  refreshThisMonth();
  applyMapFilter();
};

// ============ 訪問記（オーナーの体験談） ============
let VISITS_INDEX = {};  // id -> visit obj

async function loadVisitsIndex() {
  try {
    const r = await fetch('visits/index.json', { cache: 'no-cache' });
    if (!r.ok) return;
    const data = await r.json();
    (data.visits || []).forEach(v => { VISITS_INDEX[v.id] = v; });
  } catch (e) { console.warn('No visits index:', e); }
}

// Markdown以下の値だけサポート（見出し、段落、強調、リスト、リンク、画像）
function renderMarkdown(md) {
  if (!md) return '';
  let html = md
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  // 画像 ![alt](src) → <img>
  html = html.replace(/!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g,
    (_m, alt, src) => {
      const fullSrc = src.startsWith('http') ? src : 'visits/' + src;
      return `<figure class="v-fig"><img src="${fullSrc}" alt="${alt}" loading="lazy"/>${alt ? `<figcaption>${alt}</figcaption>` : ''}</figure>`;
    });

  // リンク [text](url)
  html = html.replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g,
    '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');

  // 見出し
  html = html.replace(/^### (.+)$/gm, '<h3 class="v-h3">$1</h3>');
  html = html.replace(/^## (.+)$/gm, '<h2 class="v-h2">$1</h2>');
  html = html.replace(/^# (.+)$/gm, '<h1 class="v-h1">$1</h1>');

  // リスト
  html = html.replace(/(?:^- .+(?:\n|$))+/gm, m => {
    const items = m.trim().split('\n').map(l => `<li>${l.replace(/^- /, '')}</li>`).join('');
    return `<ul class="v-ul">${items}</ul>`;
  });

  // 強調 **text**
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

  // 段落（1行だけの行はそのまま、連続行はそのまま、空行で区切る）
  const blocks = html.split(/\n\n+/);
  html = blocks.map(b => {
    const trimmed = b.trim();
    if (!trimmed) return '';
    if (trimmed.startsWith('<h') || trimmed.startsWith('<ul') || trimmed.startsWith('<figure')) {
      return trimmed;
    }
    return `<p>${trimmed.replace(/\n/g, '<br>')}</p>`;
  }).join('\n');

  return html;
}

function buildVisitDiaryButton(itemId) {
  const v = VISITS_INDEX[itemId];
  if (!v) return '';
  return `
    <button class="v-diary-btn" data-visit-id="${itemId}">
      <i class="ph-fill ph-notepad"></i>
      <span>訪問記を読む</span>
      ${v.visited_date ? `<small>${v.visited_date}</small>` : ''}
    </button>`;
}

function openVisitDiary(itemId) {
  const v = VISITS_INDEX[itemId];
  if (!v) return;
  const stars = v.rating ? '★'.repeat(parseInt(v.rating)) + '☆'.repeat(5 - parseInt(v.rating)) : '';
  const meta = [];
  if (v.visited_date) meta.push(`<span><i class="ph ph-calendar"></i> ${v.visited_date}</span>`);
  if (v.weather) meta.push(`<span><i class="ph ph-sun"></i> ${v.weather}</span>`);
  if (v.companions) meta.push(`<span><i class="ph ph-users"></i> ${v.companions}</span>`);
  if (v.duration) meta.push(`<span><i class="ph ph-clock"></i> ${v.duration}</span>`);
  if (stars) meta.push(`<span class="v-stars">${stars}</span>`);

  const html = `
    <div class="v-diary">
      <div class="v-badge"><i class="ph-fill ph-notepad"></i> 訪問記・オーナーの体験談</div>
      <div class="v-meta">${meta.join('')}</div>
      <div class="v-body">${renderMarkdown(v.body)}</div>
    </div>`;
  openModal(html);
}

function bindVisitDiaryButton() {
  const btn = modalContent.querySelector('.v-diary-btn');
  if (!btn) return;
  btn.addEventListener('click', () => {
    const id = btn.dataset.visitId;
    closeModal();
    setTimeout(() => openVisitDiary(id), 200);
  });
}

// ============ INSTAGRAM FEED (footer) ============
async function loadIgFeed() {
  const section = document.getElementById('igFeed');
  const grid = document.getElementById('igFeedGrid');
  if (!section || !grid) return;
  try {
    const res = await fetch('data/instagram-feed.json', { cache: 'no-store' });
    if (!res.ok) return;
    const feed = await res.json();
    const posts = (feed && Array.isArray(feed.posts)) ? feed.posts : [];
    if (!posts.length) return;
    grid.innerHTML = posts.slice(0, 6).map(p => {
      const cap = (p.caption || '').replace(/\s+/g, ' ').slice(0, 80);
      const isVid = p.media_type === 'VIDEO';
      const img = p.image || '';
      return `
        <a class="ig-feed-item" href="${p.permalink}" target="_blank" rel="noopener" aria-label="Instagram post">
          <img loading="lazy" src="${img}" alt="" onerror="this.style.opacity=0.2">
          ${isVid ? '<span class="ig-feed-video-badge"><i class="ph-fill ph-play-circle"></i></span>' : ''}
          ${cap ? `<span class="ig-feed-caption">${cap}</span>` : ''}
        </a>`;
    }).join('');
    section.hidden = false;
  } catch (e) {
    // 無音で失敗（feed未生成のときは表示しないだけ）
    console.warn('IG feed load skipped:', e.message);
  }
}

// ============ INIT ============
window.addEventListener('DOMContentLoaded', async () => {
  await loadVisitsIndex();
  applyI18n();
  updateCounts();
  initMap();
  buildRegionFilter();
  buildCalendar();
  buildList();
  buildRoutes();
  refreshThisMonth();
  handleUrlParams();
  loadIgFeed();
});
