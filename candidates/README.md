# candidates/ ディレクトリ

珍スポット候補の発掘 CSV を置く場所。`scripts/bulk_add.py` で spots.json / festivals.json に取り込む。

スキーマ完全仕様: [`../docs/schema.md`](../docs/schema.md)

## 1. ファイル命名規則

| パターン | 用途 |
|---|---|
| `YYYY-MM.csv` | 月次の発掘バッチ (例: `2026-05.csv`) |
| `YYYY-MM_<topic>.csv` | テーマ別バッチ (例: `2026-06_haikyo.csv`) |
| `_sample.csv` | 参照用サンプル (取り込まない) |

## 2. CSV スキーマ (全 24 列)

`scripts/bulk_add.py` が認識する列。**列順は自由**だが、ヘッダ名は厳密一致。

### 2.1 判定列 (必須)

| 列名 | 値 | 説明 |
|---|---|---|
| `decision` | `採用` / `却下` / `保留` | 「採用」行のみ取り込まれる |
| `is_duplicate` | `重複` / 空欄 | 「重複」なら採用でも SKIP |

### 2.2 spot 必須列 (decision=採用 のとき)

| 列名 | 例 | 説明 |
|---|---|---|
| `category` | `民俗信仰` / `B級スポット` 等 | Space 規定 8 カテゴリ。slug に自動変換 |
| `category_slug` | `folk` / `bkyu` / `mystery` / `horror` | 明示指定する場合に使用。空ならcategoryから推定 |
| `name` | `田縣神社` | 正式名称 |
| `name_kana` | `たがたじんじゃ` | ひらがな読み |
| `prefecture` | `愛知県` | 都道府県 (フルネーム) |
| `city` | `小牧市` | 市区町村 |
| `address` | `愛知県小牧市田県町152` | 所在地 |
| `lat` | `35.3383` | 緯度 (WGS84, 小数点6桁推奨) |
| `lng` | `136.9194` | 経度 |
| `summary` | `本文...` | 説明文 (description相当) |
| `highlights` | `見どころ1;見どころ2` | **`;` 区切り**で複数。Japanese カンマ `、` は使わない |
| `from_kameyama` | `車で約60分` | 亀山起点アクセス |
| `status` | `現存` / `廃止` / `移転` | 現状 |
| `fee` | `無料` / `大人500円` | 料金 |
| `hours` | `境内自由` / `9:00-17:00` | 営業時間 |

### 2.3 spot 任意列

| 列名 | 例 | 説明 |
|---|---|---|
| `name_en` | `Tagata Shrine` | 英語名 (検索キーで使用) |
| `official_url` | `https://...` | 公式 URL |
| `reference_urls` | `URL1;URL2` | `;` 区切りで複数 |
| `wiki_url` | `https://ja.wikipedia.org/...` | Wikipedia URL (`reference_urls` に統合される) |
| `region` | `近畿` / `東海` | 広域分類 |
| `category_label` | `民俗信仰` | 細分ラベル (人間向け表示) |
| `editorial_status` | `draft` / `published` | 編集ステータス |
| `visit_priority` | `high` / `medium` / `low` | 訪問優先度 |
| `safety_level` | `safe` / `caution` / `restricted` | 立入安全度 |
| `safety_note` | `私有地不可` | 安全注記 |
| `source_quality` | `primary` / `secondary` | 出典品質 |
| `last_verified` | `2026-05-28` | 最終確認日 |

### 2.4 festival 用列 (category=festival のとき)

spot 列に加えて以下を使う:

| 列名 | 例 | 説明 |
|---|---|---|
| `shrine` | `田縣神社` | 主催神社・寺 |
| `date_pattern` | `毎年3月15日` | 開催パターン (必須) |
| `date_2026` | `2026-03-15` | 今年の開催日 |
| `date_2026_end` | `2026-03-17` | 複数日の終日 |
| `origin` | `起源説明...` | 由来 |
| `viewing_notes` | `見学のコツ...` | 観覧情報 |

## 3. ワークフロー

```bash
# 1. CSV 準備 (_sample.csv をコピーして編集)
cp candidates/_sample.csv candidates/2026-06.csv
# エディタで採用候補を記入

# 2. ドライラン (build_data.py 実行せずに確認)
python3 scripts/bulk_add.py --csv ./candidates/2026-06.csv --no-build

# 3. 厳格モード (必須項目欠落でエラー終了)
python3 scripts/bulk_add.py --csv ./candidates/2026-06.csv --no-build --strict

# 4. 問題なければ本番取り込み (build_data.py 自動実行)
python3 scripts/bulk_add.py --csv ./candidates/2026-06.csv

# 5. 確認 → コミット → push
git diff spots.json festivals.json data.js index.html en/index.html
git add -A
git commit -m "feat: add N spots from 2026-06 batch"
git push
```

CI (`.github/workflows/data-sync-check.yml`) が data.js と spots.json の同期を検証する。

## 4. 判定基準 (decision)

| 判定 | 基準 | 例 |
|---|---|---|
| `採用` | 一次裏取り完了・座標確実・安全性問題なし | 自治体公式記載あり・神社庁データに存在 |
| `却下` | 出典不明・心霊煽り過剰・私有地・夜間危険 | 個人ブログのみ・住居侵入リスク |
| `保留` | 追加調査必要 | 座標不明確・出典に揺れあり |
| `is_duplicate=重複` | 既存 spots.json に同名/同座標が存在 | spot-001 と座標一致 |

判定の詳細指針: [`../bizarre_japan_listing_policy_2026-05-11.md`](../bizarre_japan_listing_policy_2026-05-11.md) (Space ファイル参照)

## 5. ハマりどころ

- **CSV セル内の Japanese カンマ `、`**: 列区切りと誤認される。必ず半角 `,` 区切り CSV で、セル内では `・` (中黒) を使う
- **highlights / reference_urls の区切り**: `;` (半角セミコロン) 厳守。他の記号は配列に分解されない
- **category 値**: Space 規定 8 種は CSV では使えるが、内部では 4 slug (folk/bkyu/mystery/horror) に自動変換される。直接 `category_slug` 列で指定するのが確実
- **lat/lng の小数点桁数**: 6 桁推奨。少なすぎると Google Maps で位置がズレる
- **`fest-` プレフィックス**: festival は自動で `fest-NNN` ID が振られる。`spot-NNN` と混同しない
