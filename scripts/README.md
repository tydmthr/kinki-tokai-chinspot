# 珍スポット候補 半自動取り込みフロー

bizarrejapan.com に新しい珍スポットを追加するための、Instagram 投稿スクショからの半自動取り込みワークフロー。

---

## 全体像

```
[1] あなた: IGアプリでハッシュタグを巡回し、コレクションに保存
        ↓
[2] あなた: コレクションのスクショを撮ってフォルダにまとめる
        ↓
[3] Computer: candidate_builder.py で候補CSVを生成
        ↓
[4] あなた: CSVを開いて 'decision' 列に「採用」「却下」を記入
        ↓
[5] Computer: bulk_add.py で採用分を spots.json に追加
        ↓
[6] git push → bizarrejapan.com に自動反映
```

---

## ステップ1: ハッシュタグ巡回（週1〜2回）

### 専用コレクションを作る

IGアプリで:
```
プロフィール → 三本線(≡) → 設定とアクティビティ → ブックマーク
→ 「新しいコレクション」 → 名前: chinspot-候補
```

### 巡回するハッシュタグ

| 優先度 | タグ |
|---|---|
| ⭐⭐⭐ | `#日本の珍スポット` |
| ⭐⭐⭐ | `#奇祭` |
| ⭐⭐⭐ | `#B級スポット` |
| ⭐⭐ | `#廃神社` |
| ⭐⭐ | `#秘宝館` |
| ⭐⭐ | `#マイナー観光地` |
| ⭐ | `#廃墟` (要選別) |

各タグの「人気投稿」上位10件を眺めて、気になるものを **保存** ボタンで `chinspot-候補` コレクションへ追加。

---

## ステップ2: スクショまとめ（月末）

### 個別スクショ方式（推奨）

各IG投稿を開いた状態で iPhone のスクリーンショット (Power+Vol↑)
- 投稿1件 = 画像1枚
- 拡張子: JPG または PNG
- 1ヶ月分まとめてフォルダに

### Mac に転送

AirDrop で Mac の `~/Desktop/chinspot-instagram/2026-05/` にコピー

---

## ステップ3: 候補CSV生成

```bash
cd ~/path/to/chinspot-map

# 環境変数で Claude API キーを設定（一度だけ）
export ANTHROPIC_API_KEY="sk-ant-..."

# 候補生成
python3 scripts/candidate_builder.py \
  --input ~/Desktop/chinspot-instagram/2026-05/ \
  --output ./candidates/2026-05.csv
```

実行すると:
- 各画像から Claude Vision で施設名・地名・カテゴリを抽出
- Wikipedia 日本語版で裏取り
- 既存97件と重複チェック
- CSV出力

⚠️ Claude API キーがない場合: Computer に画像送付 → 私がCSV生成して返却 でもOK

---

## ステップ4: 採用判定

`candidates/2026-05.csv` を **Numbers** または Excel で開く:

```
| image | name | location | category | weirdness | confidence | is_duplicate | wiki_url | decision |
|-------|------|----------|----------|-----------|------------|--------------|----------|----------|
| ig01.jpg | 廃神社A | 三重県 | spot | 4 | high | | https://... |          |  ← ここに「採用」記入
```

`decision` 列に:
- `採用` → spots.json に追加
- `却下` → 何もしない（スキップ）
- 空欄 → スキップ

判断基準（推奨）:
- weirdness ≥ 3
- confidence = high または medium
- is_duplicate が空（重複なし）
- 物理的に訪問可能な場所か？（私有地・立入禁止は却下）

---

## ステップ5: 一括取り込み

```bash
python3 scripts/bulk_add.py --csv ./candidates/2026-05.csv
```

実行すると:
- spots.json または festivals.json に追加
- ID は自動採番 (spot-051, spot-052...)
- `review_pending: true` フラグ付き（深掘り情報未記入の印）
- build_data.py を自動実行 → data.js 更新

---

## ステップ6: デプロイ

```bash
git add -A
git -c user.email="motohiro.toyoda@gmail.com" -c user.name="tydmthr" \
  commit -m "Add new spots from Instagram discovery (2026-05)"
git push
```

→ GitHub Pages 経由で bizarrejapan.com に自動反映（1〜3分）

---

## 追加後の TODO

採用したスポットには `review_pending: true` フラグがつく。あとで以下を埋めると深掘り情報が完成:

- `deepdive.history_jp` (歴史)
- `deepdive.cultural_context_jp` (文化的背景)
- `deepdive.local_perspective_jp` (地元視点)
- `access` (アクセス情報)
- `photos` (写真URL)

これは Computer に「spot-XXX を深掘りして」と頼めば wide_research でまとめて埋められます。

---

## トラブルシューティング

### Q. Claude API キーがない
→ Computer に画像送付して「候補CSV作って」と頼んでください。CSV を生成して送ります。

### Q. Wikipedia に載ってない無名スポットの場合
→ wiki_lat / wiki_lng が空欄になる。Google Maps で座標を調べて手動で記入してから bulk_add.py 実行。

### Q. category が unclear と判定された
→ CSV の category 列を `spot` または `festival` に手動修正してから bulk_add。

---

## 補足: Instagram Public Content Access について

当初、Instagram Graph API のハッシュタグ検索で完全自動化を試みたが、
Meta の `Instagram Public Content Access` フィーチャーは審査制で、
個人サイト規模では実質取得困難なため、本ワークフローに変更。

取得済みの長期トークン（`bizarre_japan` 用）は、自分の投稿の表示用には
利用可能なので、サイトのフッター等に最新IG投稿を載せる用途で別途活用予定。
