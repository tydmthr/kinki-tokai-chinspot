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

**2026-06-10 改訂（B型に切り直し）**：会長からの「Perplexity Computer と Claude Code の行き来がしんどい」を受けて、裏取り〜記事化〜JSON化〜push の重い工程を Claude Code に集約。Perplexity Computer は「候補発掘の入口」だけに絞る。

| 領域 | Perplexity Computer 側 | Claude Code 側 |
|---|---|---|
| **IGスクショ → 候補CSV化** | ◎ 主担当（Vision API / candidate_builder.py） | × |
| **新規候補の発掘・面の広い探索** | ◎ 主担当（地方紙・SNS・観光協会の横断検索） | △ 個別URLは WebFetch で対応可 |
| **掲載判断の一次フィルタ**（私有地・危険地の除外） | ◎ 候補CSV生成時に safety_note を付与 | ◎ 取り込み時に再判定 |
| **裏取り・一次資料検証** | × | ◎ 主担当（WebSearch / WebFetch / deep-research） |
| **JP 本文・summary・highlights 作成** | × | ◎ 主担当 |
| **EN 翻訳（name_en / summary_en / highlights_en）** | × | ◎ 主担当 |
| **deepdive（歴史/文化文脈/local_perspective 等）** | × | ◎ 主担当（deep-research で複数源並列） |
| **photos.json / access_info.json 編集** | × | ◎ 主担当 |
| `spots.json` / `festivals.json` への追記・連番付与 | × | ◎ 主担当 |
| `build_data.py` 実行（旧サイト用、現在は凍結） | △ 軽微 | △ 軽微（旧サイトは凍結済） |
| **本番反映**（commit → push → GitHub Actions） | × | ◎ 新リポ `bizarre-japan-next/` のフローへ |
| HTML / CSS / JS 改修 | × | ◎ 主担当（新リポのみ。旧リポは凍結） |
| Python スクリプト編集・新規作成 | △ 軽微 | ◎ 主担当 |
| ローカル dev server 動作確認 | × | ◎ 主担当 |
| 朝6時 Instagram フィード自動反映 | ◎ 専属（cron） | × **触らない** |
| **SNS 投稿文（IG キャプション）作成** | ◎ 主担当 | △ サブ（テンプレ生成のみ） |
| Space 内マニュアル・ポリシーの索引 | ◎ search_files | × |

### B型運用の受け渡し

Perplexity Computer は **候補CSV（`candidates/YYYY-MM_batchN.csv`）** を旧リポへ push。
Claude Code はそれを受けて：

1. `git pull` → candidates/ 最新化
2. CSV の `decision=採用` 行を順に裏取り（WebSearch / WebFetch / deep-research）
3. summary / highlights / deepdive / EN訳 を一気に生成
4. spots.json / festivals.json / spots_en.json / festivals_en.json / photos.json / access_info.json に追記
5. 旧リポへ push（データソース更新）
6. 新リポで `./scripts/sync-from-source.sh` 相当が自動 sync（GitHub Actions、毎朝 JST 07:00 + 手動）
7. 新リポの本番反映（commit → push → Pages）

つまり Perplexity の押し出し → Claude Code の取り込みは Drive / git の片道のみ、**会長が往復する必要はなくなる**。

### push 運用ルール

- **main 直 push 可**: `spots.json` / `festivals.json` / `spots_en.json` / `festivals_en.json` / `photos.json` / `access_info.json` / `data/photos/` / `candidates/` / 文案系 Markdown / `docs/` / `permission_requests/`
- **PR 運用**: Python スクリプト変更（HTML/CSS/JS は旧リポ凍結のため新リポへ）
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

#### `build_data.py` の副作用（要注意）

スクリプトは `data.js` だけでなく、**サイトのメタ情報（件数表記）まで自動同期**します。

| ファイル | 書き換え |
|---|---|
| `data.js` | `SPOTS` / `FESTIVALS` を JSON ソースから再構築（全文上書き） |
| `index.html` | `<title>` / `<meta description>` / `og:title` / `og:description` / `twitter:description` の件数部分を正規表現で置換（16 箇所程度） |
| `en/index.html` | 同上（ENサイト用テキスト、15 箇所程度） |

**注意点**:

- `spots.json` / `festivals.json` の編集後に `build_data.py` を流さずコミットすると、`data.js` が古いままになりヒーローの数値カウンタが実態より少なく表示される事故が起きる。実例として 2026-05-27 時点で `spots.json=157` に対し `data.js=142` の状態がコミットされていた。
- `index.html` / `en/index.html` の件数差分は `build_data.py` が作るものなので、コミットに含めて問題なし。
- コミット前の件数同期検証コマンドは `docs/workflow.md` 「3.5 build_data.py の副作用」を参照。

---

## spots.json スキーマ（JP本体）

> **完全仕様は [`docs/schema.md`](docs/schema.md) を参照。** Space 規定との差異・必須/任意区分・category slug マッピング・festival スキーマ含む。本節は要約。

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

# CLAUDE.md への追記案

リポジトリルートの `CLAUDE.md` に以下のセクションを追記してください（既存内容は残す）。Claude Code が自動で参照するので、掲示板と事故記録の存在を認知させる目的です。

---

## エージェント間連絡（Computer ⇄ Claude Code）

このプロジェクトでは Perplexity Computer（クラウド側）と Claude Code（Mac ローカル）の 2 エージェントが協働している。

### 掲示板を必ず確認

セッション開始時、以下を必ず読むこと:

1. **`docs/NOTICE_BOARD.md`** — エージェント間掲示板（新しいもの上）
2. **`docs/incidents/`** — 重大事案の詳細記録（最新のものから読む）

掲示板に自分宛の `REQUEST` / `QUESTION` がある場合は、対応後にステータスを更新する:

```
**ステータス**: open → acked → done
```

### 自分の作業を残す

- 重要な決定 / 作業完了 / 質問 は掲示板に投稿
- 投稿フォーマットは掲示板上部の「運用ルール」セクション参照
- コミットメッセージ: `docs(notice): <種別> <短いタイトル> (<発信者>)`

### 役割分担（2026-05-29 改訂）

| 作業 | 主担当 |
|---|---|
| 候補発掘・裏取り・CSV/JSON 生成 | Computer |
| ローカル取り込み（bulk_add.py） | **Claude Code** |
| git 操作（add/commit/push/branch/履歴書き換え） | **Claude Code** |
| Instagram 運用ファイル管理 | **Claude Code** |
| 危険操作の事前判断 | 両方 |

### Computer 側の自主規制（2026-05-29 事故後）

Computer は以下の git 操作を絶対に提案しない:

- `git add -A` / `git add .`（未追跡ファイル巻き込みリスク）
- `git filter-repo` の反射的提案
- `git push --force` の即時提案
- push 前に `git status` 確認を促さない手順

詳細は `docs/incidents/INCIDENT_2026-05-29.md` 参照。
