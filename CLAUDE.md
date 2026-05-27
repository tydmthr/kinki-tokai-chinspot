# Bizarre Japan / 異界巡礼 — Claude Code 作業指針

このファイルは Claude Code が起動時に自動で読み込むプロジェクトコンテキストです。
編集する際は、Computer 側 Space の `instructions` との整合を意識してください。

---

## プロジェクト概要

- **サイト名**: Bizarre Japan / 異界巡礼
- **URL**: <https://bizarrejapan.com/>
- **GitHub**: `tydmthr/kinki-tokai-chinspot`
- **運営者**: 豊田 元宏（motohiro.toyoda@gmail.com、三重県亀山市）
- **連絡先**: bizarrejapan.jp@gmail.com
- **Instagram**: @bizarre_japan
- **データ規模**（2026-05-27 時点）
  - `spots.json`: 147件（最新ID `spot-147`）
  - `festivals.json`: 159件
  - `spots_en.json`: 142件（**Batch 1 の spot-143〜147 はまだ未追従**）
- **自動化**: Instagram フィードを毎朝 06:00 JST にサイトフッターへ反映
  - **実行環境**: Perplexity Computer の `schedule_cron`（ローカル Mac では実行しない）

---

## 役割分担（重要）

| 領域 | Perplexity Computer 側 | Claude Code 側 |
|---|---|---|
| スポット候補発掘・裏取り | ◎ 主担当 | △ サブ（補助検索） |
| JP/EN 文案・SNS 投稿文生成 | ◎ 主担当 | △ サブ |
| `spots.json` / `festivals.json` への追記 | ○ 候補JSON生成・直push可 | ◎ 取り込み実行・PR運用 |
| `spots_en.json` / `festivals_en.json` への追記 | ○ EN文案を生成 | ◎ ファイルへの取り込み |
| `build_data.py` 実行（data.js 再生成） | △ 軽微な場合のみ | ◎ 主担当 |
| HTML / CSS / JS 改修 | △ 軽微な修正のみ | ◎ 主担当 |
| Python スクリプト編集・新規作成 | △ 軽微な修正のみ | ◎ 主担当 |
| ローカル dev server 動作確認 | × | ◎ 主担当 |
| 朝6時 Instagram フィード自動反映 | ◎ 専属（cron） | × **触らない** |
| Space 内マニュアル・ポリシーの索引 | ◎ search_files | × |

### push 運用ルール

- **main 直 push 可**: `spots.json` / `festivals.json` / `spots_en.json` / `festivals_en.json` / 文案系 Markdown / `docs/`
- **PR 運用**: コード変更（HTML / CSS / JS / Python スクリプト）
- **作業開始時の必須手順**: 必ず `git pull origin main` で最新化
  - 2026-05-27 に Computer 側からの push で発生した ID 連番衝突の再発防止
  - リモートの最新 `spots.json` の最大 ID を確認してから連番付与すること

詳細は `docs/workflow.md` を参照。

---

## トーン・スタイル（必読）

### 基本方針
- **学術的かつ誠実**。事実中心で、修辞は控えめに。
- 怪奇・心霊・オカルト的な煽りは避け、**「民俗」「信仰」「歴史的経緯」** の文脈で扱う。
- 出典が確認できない伝承は「伝承では」「地元では～と語られる」と明示。
- 結論を先に、根拠を後に。
- 表・箇条書きを多用して情報を構造化。
- 専門用語（土木・建設・行政・GIS等）はそのまま使ってよい（運営者は業界知識あり）。

### 事実確認の優先順位
1. 一次資料（自治体公式サイト、文化財データベース、神社庁等）
2. Wikipedia 日本語版（出典付き記述）
3. 学術論文・書籍（CiNii、J-STAGE）
4. 信頼できるメディア（地方紙、NHK、専門誌）
5. 個人ブログ・SNS（補助情報のみ。一次裏取り必須）

不確かな情報は「**不確かな情報**」と明示。位置情報・住所は必ず再確認。

### 掲載判断
- 私有地・夜間立入危険地・無断侵入が前提の心霊スポット系は原則 **却下** 推奨
- 掲載判断は **読者の安全最優先**
- 詳細は `docs/bizarre_japan_listing_policy_2026-05-11.md` を参照

---

## データファイル構成（実情）

```
spots.json            ← JP本体（147件、deepdive含む）
festivals.json        ← JP本体（159件）
spots_en.json         ← EN訳のみ（142件、name_en/summary_en/highlights_en 等）
festivals_en.json     ← EN訳のみ
photos.json           ← 写真URL・credit・license（id基準）
access_info.json      ← アクセス情報（id基準）
data.js               ← 上記すべてをマージした成果物（自動生成、直接編集禁止）
```

### 重要: `build_data.py` がマージステップの中心

`spots.json` や `spots_en.json` や `photos.json` を編集したら、必ず:

```bash
python3 build_data.py
```

を実行して `data.js` を再生成すること。`data.js` がサイト表示の実体です。

---

## spots.json スキーマ（JP本体）

```jsonc
{
  "id": "spot-NNN",                    // 連番、ゼロ埋め3桁
  "name": "正式名称（日本語）",
  "name_kana": "ふりがな",
  "category": "folk | bkyu | mystery | horror",
  "prefecture": "○○県",
  "city": "○○市",
  "address": "〒xxx-xxxx 都道府県市町村番地",
  "lat": 0.000000,                     // WGS84、小数点6桁
  "lng": 0.000000,
  "status": "現存 / 閉鎖 / 解体予定 等",
  "fee": "拝観料・入場料・無料 等",
  "hours": "営業時間・拝観時間（公式情報優先）",
  "official_url": "公式URL（無ければ自治体観光協会URL）",
  "reference_urls": ["参考URL1", "参考URL2", "..."],
  "summary": "300〜500字程度の本文。学術的トーン。",
  "highlights": ["視覚的特徴1", "特徴2", "特徴3"],
  "from_kameyama": "亀山市からのアクセス所要時間と経路",
  "deepdive": {
    "history_jp":            "詳細歴史。Markdown [出典名](URL) を多用",
    "cultural_context_jp":   "民俗・宗教・信仰の文脈",
    "local_perspective_jp":  "地元・自治体・氏子目線",
    "related_works":         "関連書籍・論文・映画・テレビ",
    "external_reviews":      "Wikipedia・観光協会・地方紙の引用",
    "best_visit_time":       "ベストシーズン・時間帯",
    "photo_tips":            "撮影アドバイス",
    "trivia":                "豆知識",
    "warnings_extra":        "立入制限・撮影禁止・私有地・宗教マナー",
    "sources":               "主要参照源 [名称](URL) 形式",

    // 英訳ペア（deepdiveの中で持つ場合もあり）
    "history_jp_en":           "history_jp の自然な英訳",
    "cultural_context_jp_en":  "...",
    // ...以下同様
  }
}
```

## spots_en.json スキーマ（EN訳）

```jsonc
{
  "id": "spot-NNN",          // spots.json と同じ ID
  "name": "（参照用、JP）",
  "name_kana": "（参照用）",
  "category": "...",
  "prefecture": "...",
  // ... 元 spots.json の主要キーをコピー
  "name_en": "Romaji or English name",
  "prefecture_en": "Oita Prefecture",
  "city_en": "Usa City",
  "summary_en": "English summary",
  "highlights_en": ["..."]
}
```

### カテゴリ（4分類）

| key | 日本語ラベル | 説明 |
|---|---|---|
| `folk` | 民俗信仰 | 神社仏閣・道祖神・性器信仰・即身仏・賽の河原 等 |
| `bkyu` | B級 | 巨大像・カオス個人博物館・異形看板・路傍の奇物 |
| `mystery` | 不可思議 | UFO伝承・洞窟内仏像群・逆さ鳥居・鬼ミイラ 等 |
| `horror` | 禁忌・廃墟 | 合法的に近接可能で視覚的に強い廃墟系 |

---

## ディレクトリ構成（実情）

```
kinki-tokai-chinspot/
├── CLAUDE.md                       ← このファイル
├── README.md
├── CNAME / LICENSE
├── .github/                         ← GitHub Actions など
│
├── index.html                       ← サイト本体（日本語版）
├── app.js
├── data.js                          ← 自動生成。直接編集禁止
├── build_data.py                    ← data.js 生成スクリプト
├── en/                              ← 英語版サイト
│
├── spots.json                       ← JP本体（147件）
├── festivals.json                   ← JP本体（159件）
├── spots_en.json                    ← EN訳
├── festivals_en.json                ← EN訳
├── photos.json                      ← 写真メタ
├── access_info.json                 ← アクセス情報
│
├── apply_*.py / patch_*.py / verify_*.py  ← 一括処理スクリプト群（ルート）
├── update_from_wiki.py / fetch_en_wiki.py
├── generate_assets.py / get_wiki_images.py
│
├── candidates/                      ← 候補CSV置き場
├── scripts/
│   ├── README.md
│   ├── bulk_add.py                  ← CSV→spots.json取り込み
│   ├── candidate_builder.py         ← IGスクショ→候補CSV
│   └── fetch_instagram_feed.py      ← IGフィード取得（実行はComputer側）
│
├── docs/
│   ├── workflow.md                  ← 役割分担ルール
│   ├── bizarre_japan_workflow_manual.pdf
│   ├── bizarre_japan_listing_policy_2026-05-11.md
│   ├── bizarrejapan-site-renovation-prompts-2026-05-11.md
│   ├── bizarre_japan_task_coordination_2026-05-20.md
│   └── sample/
│       └── spot-001.md
└── visits/                          ← 訪問記
```

---

## よく使うコマンド

### Git
```bash
# 作業開始時（必須）
git pull origin main

# spots.json への追記（main直push可）
git add spots.json spots_en.json data.js
git commit -m "feat(spots): add N candidates (spot-NNN〜NNN)"
git push origin main

# コード変更（PR運用）
git checkout -b feat/xxx
# ... 編集 ...
git push -u origin feat/xxx
gh pr create --fill
```

### ローカル dev server
```bash
python3 -m http.server 8000
# → http://localhost:8000
```

### data.js 再生成（編集後は必須）
```bash
python3 build_data.py
# → "data.js regenerated: 147 spots, 159 festivals" のような出力
```

### 候補取り込み（IGスクショ → CSV → JSON）
```bash
# 1. IGスクショから候補CSV生成（Claude Vision API使用）
python3 scripts/candidate_builder.py \
  --input ./instagram_screenshots/2026-05/ \
  --output ./candidates/2026-05.csv

# 2. CSV の decision 列を編集（採用/却下）

# 3. 採用分を spots.json/festivals.json に追加
python3 scripts/bulk_add.py --csv ./candidates/2026-05.csv
# → 自動で build_data.py も実行される
```

### Instagram フィード（**Claude Code では実行しない**）
```bash
# 参考用に scripts/fetch_instagram_feed.py を置いてあるが、
# 実行は Perplexity Computer の schedule_cron に任せる
# 環境変数: IG_LONG_TOKEN, IG_BUSINESS_ID が必要
```

---

## 既知の運用上の注意

### 1. ID 連番衝突
- Computer 側と Claude Code 側の両方が `spots.json` を編集できる構造
- 必ず `git pull origin main` してから最大 ID を確認
- ID は ゼロ埋め3桁（`spot-148` 形式）

### 2. 緯度経度の精度
- WGS84、小数点6桁
- 概略値の場合は summary 内で「不確かな情報」と明示
- Google Maps で実在確認すること

### 3. 出典 URL
- インライン Markdown 記法 `[出典名](URL)` で
- アンカーテキストは出典名・媒体名・記述的な語句（「source」「link」のような汎用語禁止）
- Wikipedia は日本語版を優先

### 4. JP本体と EN訳の同期
- `spots.json` を追記したら `spots_en.json` も追記
- 同期忘れがあると EN サイト側で件数差が出る
- 現状、`spots_en.json` は142件で、Batch 1 の spot-143〜147 がまだ未追従

### 5. data.js の自動生成
- `data.js` は手動編集禁止
- JP本体・EN訳・photos・access のいずれかを変更したら必ず `python3 build_data.py`
- コミット時は `data.js` も含める

### 6. 英訳ポリシー
- 逐語訳ではなく自然な英語
- 固有名詞は ローマ字＋括弧で英名併記可（例: `Jippozan Daijoin (Temple of Ten Treasures)`）
- 文化的概念は注釈付きで（例: `即身仏 (sokushinbutsu, self-mummified monks)`）

---

## 関連ドキュメント

- `docs/workflow.md` — 役割分担ルール詳細
- `docs/bizarre_japan_listing_policy_2026-05-11.md` — 掲載判断基準
- `docs/bizarre_japan_workflow_manual.pdf` — 全体ワークフロー
- `docs/bizarrejapan-site-renovation-prompts-2026-05-11.md` — サイトリノベプロンプト集
- `docs/bizarre_japan_task_coordination_2026-05-20.md` — Computer/Todoist/GitHub連携運用
- `docs/sample/spot-001.md` — 訪問記サンプル
- `scripts/README.md` — 候補取り込みフローの詳細

---

最終更新: 2026-05-27
