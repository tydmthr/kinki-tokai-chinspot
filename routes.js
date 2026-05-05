/* ============ 巡礼ルート定義 ============ */
const ROUTES = [
  {
    id: 'route-aichi-fertility',
    title_ja: '愛知 性神＆カオス巡礼 — 一日コース',
    title_en: 'Aichi Fertility & Chaos Pilgrimage — Full Day',
    duration_ja: '一日（6〜8時間）',
    duration_en: 'Full day (6–8 hrs)',
    season_ja: '春（3月15日）または通年',
    season_en: 'Spring (Mar 15) or year-round',
    cat: 'folk',
    desc_ja: '世界中の旅人が集う豊年祭の中心地。男根の田縣神社と女陰の大縣神社、そして個人創業のコンクリート楽園・五色園と桃太郎神社まで一気に巡る。',
    desc_en: 'Japan\'s most internationally famous fertility pilgrimage. The phallus shrine and its feminine counterpart, plus the unhinged concrete fantasias of Goshikien and Momotaro Shrine — all in a single day.',
    spots: ['spot-001', 'spot-002', 'spot-003', 'spot-004'],
    glyph: '祓',
  },
  {
    id: 'route-mie-mystery',
    title_ja: '三重 聖地と巨石 — 一日コース',
    title_en: 'Mie Sacred Stones — Full Day',
    duration_ja: '一日（7〜9時間）',
    duration_en: 'Full day (7–9 hrs)',
    season_ja: '通年',
    season_en: 'Year-round',
    cat: 'mystery',
    desc_ja: '伊勢の周縁に潜む奇景。日本最古とされる花の窟神社、夫婦岩の二見興玉、椿大神社の奥の宮、そして熊野古道の鬼ヶ城まで。',
    desc_en: 'The strange peripheries of Ise. Hana-no-Iwaya (one of Japan\'s oldest shrines), the Wedded Rocks of Futami, Tsubaki-Okami\'s inner sanctuary, and the demon caves of Onigajo on the Kumano Kodo.',
    spots: ['spot-016', 'spot-017', 'spot-040', 'spot-042'],
    glyph: '秘',
  },
  {
    id: 'route-kyoto-shadow',
    title_ja: '京都の闇 — 半日コース',
    title_en: 'Kyoto\'s Shadow — Half Day',
    duration_ja: '半日（4〜5時間）',
    duration_en: 'Half day (4–5 hrs)',
    season_ja: '通年（夜間立入禁止）',
    season_en: 'Year-round (no night visits)',
    cat: 'horror',
    desc_ja: '千年の都の影の側面。化野念仏寺の千体石仏、酒呑童子の首塚、平安以来の葬送地・鳥辺野、丑の刻参り発祥の貴船神社——観光ガイドが沈黙する京都を歩く。',
    desc_en: 'The capital\'s shadow side. The thousand-stone Buddhist memorial of Adashino, the severed-head mound of Shuten-doji, the Heian-era execution grounds of Toribeno, and the cursed shrine of Kifune — the Kyoto guidebooks won\'t mention.',
    spots: ['spot-021', 'spot-022', 'spot-023', 'spot-029'],
    glyph: '霊',
  },
  {
    id: 'route-osaka-bgrade',
    title_ja: '大阪 B級異界 — 半日コース',
    title_en: 'Osaka B-Grade Wonders — Half Day',
    duration_ja: '半日（5〜6時間）',
    duration_en: 'Half day (5–6 hrs)',
    season_ja: '通年',
    season_en: 'Year-round',
    cat: 'bkyu',
    desc_ja: '岡本太郎の太陽の塔の内部、巨大獅子頭の難波八阪神社、戦後遊園地の生駒山上、そして明治の名残・旧奈良監獄まで。一度見たら忘れられない大阪の珍景を一筆書きで巡る。',
    desc_en: 'Inside Taro Okamoto\'s Tower of the Sun, the giant lion-head shrine of Namba Yasaka, the post-war retro amusement park of Mt. Ikoma, and the Meiji-era former Nara Prison. A one-day tour of unforgettable Osaka curiosities.',
    spots: ['spot-011', 'spot-012', 'spot-013', 'spot-014'],
    glyph: '魁',
  },
  {
    id: 'route-nara-pyramid',
    title_ja: '奈良 古代の謎 — 一日コース',
    title_en: 'Nara Ancient Mysteries — Full Day',
    duration_ja: '一日（6〜8時間）',
    duration_en: 'Full day (6–8 hrs)',
    season_ja: '春・秋',
    season_en: 'Spring or autumn',
    cat: 'mystery',
    desc_ja: '日本のピラミッドと呼ばれる頭塔、明日香の謎の石造物・酒船石、古代の巨石・益田岩船、そして大峰山系の隠れ里・玉置神社まで。文字に残らなかった信仰を辿る。',
    desc_en: 'The pyramid-like Zuto, the enigmatic stone vessels of Asuka, the colossal stone ship of Masuda, and the hidden mountain shrine of Tamaki. A pilgrimage tracing the beliefs that predate written history.',
    spots: ['spot-031', 'spot-032', 'spot-033', 'spot-036'],
    glyph: '秘',
  },
  {
    id: 'route-festival-january',
    title_ja: '新年の奇祭一気見 — 1月二日コース',
    title_en: 'New Year Festival Marathon — January 2-Day',
    duration_ja: '二日間',
    duration_en: '2 days',
    season_ja: '1月10〜14日',
    season_en: 'January 10–14',
    cat: 'folk',
    desc_ja: '日本の正月が一年で最もカオスになる五日間。十日戎の福男選び、法界寺の裸踊り、四天王寺どやどやの白褌大乱戦——近畿の主要奇祭を駆け抜ける。',
    desc_en: 'The five most chaotic days on Japan\'s New Year calendar. The Lucky Man Race at Nishinomiya, the naked dance at Hokai-ji, and the Doya-doya white-loincloth scramble at Shitenno-ji — the canonical winter pilgrimage.',
    festivals: ['fest-001', 'fest-002', 'fest-003'],
    spots: [],
    glyph: '祭',
  },
];

function getRouteCoords(route) {
  const coords = [];
  (route.spots || []).forEach(id => {
    const s = SPOTS.find(x => x.id === id);
    if (s) coords.push({ lng: s.lng, lat: s.lat, name: s.name, type: 'spot', data: s });
  });
  (route.festivals || []).forEach(id => {
    const f = FESTIVALS.find(x => x.id === id);
    if (f) coords.push({ lng: f.lng, lat: f.lat, name: f.name, type: 'fest', data: f });
  });
  return coords;
}
