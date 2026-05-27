# spots.json / festivals.json スキーマ仕様

Bizarre Japan のデータ実態スキーマ。Space 規定 (運営者メモ) との差異も併記する。

## 1. 真の仕様 (実装が参照しているスキーマ)

`app.js` および `build_data.py` が前提とする実装上のスキーマが正。Space 規定は参考メモ扱い。

### 1.1 spots.json (157件, 2026-05-28 時点)

```jsonc
[
  {
    "id": "spot-001",                 // 必須・一意。zero-padded 3桁
    "name": "田縣神社",                // 必須
    "name_kana": "たがたじんじゃ",      // 必須 (検索キーで使われる: app.js:841)
    "name_en": "Tagata Shrine",       // 任意 (英語表示・検索で使われる: app.js:841)
    "category": "folk",                // 必須。4種固定: folk / bkyu / mystery / horror (後述 1.3)
    "prefecture": "愛知県",             // 必須 (フィルタ・表示で使用)
    "city": "小牧市",                   // 必須
    "address": "〒485-0004 ...",       // 必須
    "lat": 35.3383,                    // 必須。WGS84、6桁推奨
    "lng": 136.9194,                   // 必須
    "status": "現存",                   // 必須。例: 現存 / 廃止 / 移転 / 一部現存
    "fee": "無料・境内自由",            // 必須
    "hours": "境内自由",                // 必須
    "official_url": "https://...",      // 任意 (既存132/157件)
    "reference_urls": ["..."],          // 任意 (配列, 既存144/157件)
    "summary": "...",                   // 必須 (本文・description相当)
    "highlights": ["...", "..."],       // 必須 (配列、3項目程度)
    "from_kameyama": "車で約60分",      // 必須 (亀山起点のアクセス情報)
    "deepdive": { ... }                 // 任意 (詳細記事用拡張、別途仕様)
  }
]
```

### 1.2 追加メタ (mie-batch-2 以降、47件のみ存在)

新規 spot 追加時は **入れても入れなくても OK**。入れる場合は下記準拠。

| field | 型 | 例 | 用途 |
|---|---|---|---|
| `region` | string | "近畿" / "東海" | 広域分類 |
| `category_label` | string | "民俗信仰" | 人間向け表示ラベル (Space 規定 8 カテゴリと整合) |
| `editorial_status` | string | "draft" / "published" | 編集ステータス |
| `visit_priority` | string | "high" / "medium" / "low" | 訪問優先度 |
| `safety_level` | string | "safe" / "caution" / "restricted" | 立入安全度 |
| `safety_note` | string | "私有地不可・遠景のみ" | 安全に関する注記 |
| `source_quality` | string | "primary" / "secondary" | 出典品質 |
| `last_verified` | string (YYYY-MM-DD) | "2026-05-11" | 最終確認日 |

### 1.3 category 仕様 (重要)

**app.js が 4 slug 固定で動作している** (`app.js:3` `CAT_GLYPHS`)。新規追加時は必ず以下のいずれかを設定:

| slug | 表示文字 | Space 規定の包含範囲 | 該当例 |
|---|---|---|---|
| `folk` | 祓 | 神社仏閣 / 民俗信仰 | 神社・寺・祭祀地・路傍の信仰物 |
| `bkyu` | 魁 | B級スポット / 路傍 / その他 | 観光奇物・人工奇景・コレクション施設 |
| `mystery` | 秘 | 産業遺産 / 廃墟 (謎系) | 廃線・廃工場・暗渠・謎の建造物 |
| `horror` | 霊 | 自然奇景 / 心霊伝承 | 心霊スポット・自然怪異・恐怖伝承地 |

`category_label` (任意フィールド) で Space 規定 8 カテゴリの細分化表現を保持可能。

### 1.4 festivals.json (159件)

spots と別構造。本ドキュメントでは概要のみ。詳細は別 Issue。

```jsonc
{
  "id": "fest-001",
  "name": "...",
  "name_kana": "...",
  "category": "...",      // 4slug ではなく festival 内分類
  "prefecture": "...",
  "city": "...",
  "shrine": "...",         // 主催神社・寺
  "lat": ..., "lng": ...,
  "date_2026": "2026-03-15",       // 開催日 (今年分)
  "date_2026_end": "...",          // 複数日の場合のみ
  "date_pattern": "毎年3月15日",    // 必須・恒常パターン
  "origin": "...",                  // 起源説明
  "summary": "...",
  "highlights": ["..."],
  "viewing_notes": "...",
  "official_url": "...",
  "reference_urls": ["..."],
  "deepdive": { ... }
}
```

## 2. Space 規定との差異

Space instructions に記載された規定スキーマ:

```
{ id, name, name_kana, name_en, lat, lng, category, prefecture,
  address, description, source, photo_url, visit_url? }
```

| Space 規定 | 実装スキーマ | 対応 |
|---|---|---|
| `description` | `summary` | 名称が異なるが**意味は同じ**。実装側 `summary` が正 |
| `source` | `reference_urls` (配列) | 実装は配列で複数 URL 対応 |
| `photo_url` | **未実装** | 画像は将来課題。当面は不要 |
| `visit_url` | **未実装** | visits/ 配下の訪問記との紐付けは別仕組み |
| (規定外) | `city`, `status`, `fee`, `hours`, `official_url`, `highlights`, `from_kameyama`, `deepdive` | 実装側拡張。新規追加時必須 |
| `category` (8種) | `category` (4 slug) | 4 slug が正。`category_label` で細分可 |

**運用ルール**: Space 規定は「最小コンセプト」、実装スキーマは「真の仕様」。新規 spot 追加時は実装スキーマに従う。

## 3. 必須/任意の早見表 (新規追加時)

### 必須 13 項目

`id, name, name_kana, category, prefecture, city, address, lat, lng, status, fee, hours, summary, highlights, from_kameyama`

(`highlights` と `from_kameyama` を含めて 15 項目だが、`highlights` は配列で `from_kameyama` は単独 string)

### 任意

`name_en, official_url, reference_urls, deepdive, region, category_label, editorial_status, visit_priority, safety_level, safety_note, source_quality, last_verified`

## 4. 関連ファイル

- `scripts/bulk_add.py`: CSV から spots.json に追加。本仕様準拠
- `candidates/_sample.csv`: 入力 CSV の見本
- `candidates/README.md`: ワークフロー
- `build_data.py`: spots.json → data.js 変換 (HTML カウンタも更新)
- `app.js`: フロントエンド (category slug を参照)
