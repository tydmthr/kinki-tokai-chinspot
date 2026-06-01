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

### 1.5 データ振り分けルール (最重要)

**祭事・神事・年中行事は festivals.json に格納する。spots.json には格納しない。**

このルールはバッチ追加 (cron / 手動 / Claude Code いずれも) で適用される。

#### 判定基準

| 性質 | 格納先 | 理由 |
|---|---|---|
| 恒常的に開催される祭・神事 (年中行事) | **festivals.json** | `date_pattern`・`date_2026` を持つため |
| 不定期だが宗教儀礼として継続中の神事 | **festivals.json** | 同上 |
| 廃絶した祭の跡地・記録 | **festivals.json** (`date_pattern: "廃絶"` 等で明示) | 民俗学的に祭として扱う |
| 祭が行われる神社そのもの (建造物) | **spots.json** | 物理的な信仰拠点として扱う |
| 路傍の信仰物・石仏・道祖神 | **spots.json** | 単発の信仰オブジェクト |
| 廃墟・廃線・B級スポット | **spots.json** | 祭事ではない |

#### 判定が分かれるケース

- **"●●神社" が祭で有名な場合**: 神社建造物自体が訪問対象なら **spots.json**、祭そのものが訪問対象なら **festivals.json**。両方の価値があるなら別レコードで両方に登録可。
- **山車・神輿などの民俗工芸品の保存施設**: 施設そのものは spots.json、祭本体は festivals.json。

#### 違反検出

`name` に「祭」「神事」「祇園」「だんじり」「花祭」「嫁入り」「曳き」「しめ切り」等が含まれる spots.json レコードは festivals.json への移動を検討する。

#### 過去の移行履歴

- 2026-05-30: spot-135/137-141/149-152 の 9件を fest-163〜fest-171 として festivals.json に移行 (commit 3fbd949)。

### 1.6 photo_url の仕様 (2026-06-01 制定)

**`photo_url` は spot/festival 詳細モーダルで `<img src="...">` として読み込まれる画像直リンク URL のみを受理する。**

このルールは取り込みスクリプト (`bulk_add.py`, JSON 直接マージ) いずれにも適用される。

#### 受理する値

| 値 | 例 | 扱い |
|---|---|---|
| **画像直リンク URL** | `https://example.com/photos/foo.jpg`, `https://upload.wikimedia.org/.../bar.png` | ✓ そのまま `<img src>` で表示 |
| `null` または **キー未設定** | `"photo_url": null` または キーごと不在 | ✓ サイト側で写真欄を表示しない (フォールバック) |

#### 受理しない値

| 値 | 例 | 理由 |
|---|---|---|
| **観光情報サイトの一般ページ URL** | `https://www.kankou-shimane.com/destination/20275` | HTML ページ。`<img>` で読み込むとブロークン画像になる |
| **公式サイトのトップページ URL** | `https://www.sand-museum.jp` | 同上。`official_url` に既に格納されているはず |
| **観光協会のスポット詳細ページ URL** | `https://rurubu.jp/andmore/spot/...` | 同上。参考リンクなら `reference_urls` に追加 |

#### ページ URL を保持したい場合

観光情報ページ・自治体公式の特定ページなど、参考情報として保持したい URL は `reference_urls` (配列) に追加する。`photo_url` には入れない。

#### 拡張子による判定 (将来 lint 用)

許容拡張子: `.jpg / .jpeg / .png / .webp / .gif / .svg` (大文字小文字不問)。
URL がクエリパラメータ付き (例: `https://.../image.jpg?size=large`) の場合は、パス末尾の拡張子で判定する。

#### 著作権・ライセンス

- 自前撮影画像が望ましい
- Wikipedia / Wikimedia Commons は CC ライセンス確認のうえ転載
- 自治体公式の OG 画像は転載可否を都度確認 (基本は外部直リンク不可、ライセンス記載がある場合のみ)
- 別途 `photos.json` で credit / license メタを管理する運用 (実装はサイト改修待ち)

#### 過去の修正履歴

- 2026-06-01: spot-202 / spot-204 / spot-205 / spot-206 / spot-207 / spot-208 / spot-209 の 7件で `photo_url` に観光情報サイトのページ URL が誤って格納されていた問題を修正。各エントリの `photo_url` を `null` に変更、保全したい URL は `reference_urls` に追加。詳細は `docs/NOTICE_BOARD.md` の DECISION 投稿参照。

### 1.7 deepdive スキーマ (2026-06-01 制定、Batch 6 以降形式が正規)

**Batch 6 以降に追加されたエントリの `deepdive` オブジェクトは、以下の 19 キー構成を正規スキーマとする。** Batch 1-5 (spot-001〜142 / fest-001〜159) の旧スキーマも引き続き有効だが、新規追加・個別更新時は本スキーマに従う（漸進的マイグレーション）。

#### 正規スキーマ（19 キー）

各キーは spot/festival の解説テキストを格納する文字列フィールド。`_jp` と `_en` のペアで提供し、加えて警告補足フィールド `warnings_extra` を持つ。

| キー | 役割 | 内容の例 |
|---|---|---|
| `history_jp` / `history_en` | 歴史的経緯 | 創建年・由来・主要な歴史イベント・系譜 |
| `religion_jp` / `religion_en` | 宗教的・信仰的位置付け | 宗派・信仰体系・本尊・祭神・修験道との関係 |
| `architecture_jp` / `architecture_en` | 建築・構造的特徴 | 様式・年代・建材・伽藍配置・特徴的な造作 |
| `cultural_property_jp` / `cultural_property_en` | 文化財指定 | 国宝・重要文化財・登録有形・自治体指定など |
| `legends_jp` / `legends_en` | 伝承・民俗・口承 | 伝説・地元の語り・民俗学的解釈 |
| `access_jp` / `access_en` | アクセス | 最寄駅・バス・徒歩経路・所要時間・駐車場 |
| `photo_points_jp` / `photo_points_en` | 撮影アドバイス | 順光時刻・推奨アングル・季節・撮影制限 |
| `nearby_jp` / `nearby_en` | 周辺スポット | 徒歩・車圏内の関連スポット・横断企画素材 |
| `warnings_jp` / `warnings_en` | 一般的な注意事項 | 拝観マナー・服装・撮影禁止・宗教的配慮 |
| `warnings_extra` | 追加の安全注記（言語非依存） | 災害被害状況・私有地・閉鎖期間・電話確認推奨など、必要時のみ。`safety_level: caution` と併記される |

**注**: `warnings_extra` は `_jp` / `_en` の対を持たない。本文中に日本語と英語を併記する運用、または日本語のみで記述する運用のいずれも認める（Batch 6 以降の実例では日本語ベースで記述されている）。

#### 旧スキーマ（Batch 1-5、参考）

Batch 3-5 で取り込まれた spot は 20 キー（10_jp + 10_en）構成だった。キー名は以下：

`history_jp/_en, cultural_context_jp/_en, local_perspective_jp/_en, related_works (lang 非依存), external_reviews (lang 非依存), best_visit_time (lang 非依存), photo_tips (lang 非依存), trivia (lang 非依存), warnings_extra, sources`

Batch 1-2 はさらに自由形式で、deepdive 自体を持たないエントリもある。

#### マイグレーション方針

- Batch 1-5 エントリの**遡及修正は不要**（サイト表示は既に機能している）
- 個別エントリを編集する機会があれば、19 キー形式に揃える（漸進的）
- Batch 10 以降の CSV テンプレート・JSON 生成は 19 キーを標準とする
- `build_data.py` は deepdive オブジェクト全体をそのまま `data.js` に同期するため、スキーマ揺らぎがあってもビルドは成功する

#### サンプル参照

正規スキーマの実例は spot-184（笠置寺）以降の任意のエントリを参照。Batch 6（spot-184〜192）・Batch 7（spot-193〜201）・Batch 8（spot-202〜210）・Batch 9（spot-211〜219）はすべて本スキーマに準拠。

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
| `photo_url` | **仕様化済 (2026-06-01)** | 下記 §1.6 参照。画像直リンク URL のみ受理 |
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
