# candidates/ — 候補 CSV 置き場

`spots.json` / `festivals.json` への取り込み前の候補 CSV を置くディレクトリ。
通常は `scripts/candidate_builder.py` が Instagram スクリーンショットから自動生成し、
人手で `decision` 列を埋めてから `scripts/bulk_add.py` で取り込む。

---

## ファイル

| ファイル | 用途 |
|---|---|
| `_sample.csv` | フォーマット確認用サンプル（5 行・採用/却下/重複/保留/festival の全ケース） |
| `YYYY-MM.csv` | 実運用（月次バッチ）。candidate_builder.py が出力 |

`_` プレフィックスのファイルはサンプル・テスト用で、`bulk_add.py` に
渡しても害がないように作っているが、本番取り込みでは使わない。

---

## CSV スキーマ（13 列）

| 列名 | 必須 | 由来 | bulk_add.py での使われ方 |
|---|---|---|---|
| `image` | △ | candidate_builder が画像ファイル名を記録 | 使われない（参照用） |
| `name` | ◎ | スポット/祭名 | `name` として spots.json に転記 |
| `location` | ◎ | 「○○県○○市」程度 | `location` として転記 |
| `category` | ◎ | `spot` or `festival` | 振り分け先 (`spots.json` / `festivals.json`) |
| `weirdness` | — | 1〜10 の主観スコア | 使われない（人間の判断材料） |
| `confidence` | — | 0〜1 の抽出信頼度 | 使われない（人間の判断材料） |
| `is_duplicate` | ◎ | 既存名と一致した場合 `重複` | `重複` の行は decision に関わらずスキップ |
| `wiki_title` | — | Wikipedia 記事タイトル | 使われない（参考） |
| `wiki_url` | △ | Wikipedia URL | `wiki_url` として転記 |
| `wiki_lat` | ◎ | 緯度（WGS84 小数点6桁） | `lat` として転記（float 変換） |
| `wiki_lng` | ◎ | 経度（WGS84 小数点6桁） | `lng` として転記（float 変換） |
| `caption_summary` | △ | 短い説明 | `summary` として転記 |
| `decision` | ◎ | `採用` / `却下` / `（空欄=保留）` | `採用` のみ取り込まれる |

---

## 取り込みフロー

```bash
# 1. 候補生成（Instagram スクショから）
python3 scripts/candidate_builder.py \
  --input ./instagram_screenshots/2026-05/ \
  --output ./candidates/2026-05.csv

# 2. CSV を開いて decision 列を手作業で埋める
#    （採用 / 却下 / 空欄=保留）

# 3. 採用分を spots.json / festivals.json に追加 + data.js 再生成
python3 scripts/bulk_add.py --csv ./candidates/2026-05.csv

# 4. dev server で目視確認
python3 -m http.server 8000

# 5. コミット
git add -A
git commit -m "feat(spots): import batch 2026-05 (N spots)"
git push origin main
```

---

## decision 列の挙動マトリクス

| `decision` | `is_duplicate` | 結果 |
|---|---|---|
| `採用` | （空欄） | spots.json または festivals.json に追加 |
| `採用` | `重複` | スキップ（ログ `SKIP 重複: ...`） |
| `却下` | 任意 | スキップ（ログなし） |
| `（空欄）` | 任意 | スキップ（保留扱い・後日判断） |

---

## 関連ドキュメント

- `scripts/README.md` — candidate_builder.py / bulk_add.py の詳細
- `docs/workflow.md` — 役割分担とコミット運用
- `CLAUDE.md` — Claude Code 用作業指針
