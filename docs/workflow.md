# Bizarre Japan / 異界巡礼 — 役割分担ワークフロー

Perplexity Computer と Claude Code を併用する運用ルールをまとめた文書です。

---

## 基本思想

**「発掘・調査・文案・自動化は Computer、コード編集・ローカル動作確認は Claude Code」**

- Computer 側：Web リサーチ・並列 subagent・SNS文案・cron が強い
- Claude Code 側：ローカルファイル編集・dev server・git 操作が直感的

両者の競合を避けるため、**触る領域とブランチ運用** を以下に明文化します。

---

## 1. 担当領域マトリクス

| 作業 | 担当 | 補足 |
|---|---|---|
| スポット候補発掘 | **Computer** | Web検索 + 並列 subagent |
| 既存データ照合・重複チェック | **Computer** | search_files で索引可能 |
| 候補 JSON の生成（completeスキーマ） | **Computer** | research subagent で deepdive JP/EN 込み |
| `spots.json` / `festivals.json` への追記 | どちらでも可 | **main 直 push 可** |
| `spots_en.json` / `festivals_en.json` への追記 | どちらでも可 | **main 直 push 可** |
| `build_data.py` 実行（data.js 再生成） | 軽微なら可 | **Claude Code 主担当** |
| サイト HTML / CSS / JS の改修 | **Claude Code** | PR 運用 |
| Python スクリプトの編集・リファクタ | **Claude Code** | PR 運用 |
| ローカル dev server 動作確認 | **Claude Code** | Mac 上で完結 |
| Instagram / Threads 投稿文（JP/EN） | **Computer** | トーン管理 |
| 朝6時 Instagram フィード自動反映 | **Computer 専属** | schedule_cron。Claude Code では触らない |
| Space 内マニュアル・ポリシー検索 | **Computer** | search_files |
| 掲載判断（add / hold / exclude） | **運営者** | 両方の AI 出力を確認して決定 |

---

## 2. push 運用ルール

### main 直 push 可（簡単な追記）

- `spots.json` / `festivals.json` の追記（候補取り込み）
- `spots_en.json` / `festivals_en.json` の追記（EN訳）
- `photos.json` / `access_info.json` の追記・修正
- `data.js`（再生成結果、上記と一緒にコミット）
- `docs/` 配下の文案・マニュアル系 Markdown
- `README.md` の軽微な更新

### PR 運用（コード変更）

- `index.html` / `en/index.html` 等の HTML
- `app.js` ・ その他 JS
- `build_data.py` ・`scripts/` 配下の Python スクリプトの機能変更
- `apply_*.py` ・ `patch_*.py` 等の一括処理スクリプトの新規作成

ブランチ命名規則：
- `feat/xxx` — 機能追加
- `fix/xxx` — バグ修正
- `refactor/xxx` — リファクタ
- `docs/xxx` — ドキュメント大規模変更

### 作業開始時の必須手順

```bash
git pull origin main
```

**理由**: 2026-05-27 に Computer 側で push 直前に ID 連番衝突を検出した事案あり。リモート最新の最大 ID を確認してから連番付与すること。

---

## 3. データ流れ図

```
[Computer 側]
  ├─ 候補発掘・裏取り (research subagent)
  ├─ 重複チェック (既存 spots.json と照合)
  ├─ 完成版スキーマで JSON 生成（deepdive JP/EN 含む）
  ├─ 差分プレビュー Markdown 作成
  └─ 軽微な追記なら main 直 push
        │
        ├─→ そのまま main にコミット
        │
        └─→ Claude Code 側に渡したい場合
                │
                ▼
        [Claude Code 側]
          ├─ git pull origin main
          ├─ Computer から渡された候補 JSON を取り込み
          ├─ spots.json / spots_en.json への追記
          ├─ python3 build_data.py を実行し data.js 再生成
          ├─ ローカル dev server で表示確認
          ├─ ブランチ切ってコミット
          └─ PR 作成 → main マージ
                │
                ▼
        [GitHub main]
                │
                ▼
        [Cloudflare Pages 等で本番反映]
```

---

## 4. ID 連番管理

`spots.json` の `id` は `spot-NNN`（ゼロ埋め3桁）形式。

### 採番ルール

1. 作業開始時に `git pull origin main`
2. リモート最新の `spots.json` 末尾の `id` を取得
3. 次の連番から付与

### Computer 側での確認コマンド（参考）

```python
import json
s = json.load(open('spots.json'))
print('max id:', s[-1]['id'])
# → spot-147 だったら次は spot-148 から
```

### Claude Code 側での確認コマンド

```bash
python3 -c "import json; s=json.load(open('spots.json')); print('max id:', s[-1]['id'])"
```

---

## 5. Instagram フィード自動反映の取り扱い

### 結論

**朝6時の Instagram フィード自動反映は Perplexity Computer の `schedule_cron` で運用します。Claude Code では実行しません。**

### 理由

- ローカル Mac の常時起動・スリープ・ネット状態に依存させたくない
- Computer 側は 24/7 サンドボックスで安定稼働
- 多重実行（Mac側 cron と Computer側 cron の両方が走る）リスクを回避

### 運用

- `scripts/fetch_instagram_feed.py` はリファレンスとしてリポジトリに置く
- ローカルで実行しない（コードの動作確認時のみ手動実行可）
- 変更が必要な場合は Claude Code で編集 → push → Computer 側 cron の挙動確認

---

## 6. 完成版スポット記事のクオリティ基準

新規スポット追加時、以下を満たすこと。

### 必須

- 18 フィールド全て埋まっている（`id` 〜 `from_kameyama`）
- `deepdive` 20 サブキー全て（JP 10 + EN 10）埋まっている
- `reference_urls` は 3 件以上、うち一次資料を含む
- `summary` は 300〜500 字程度
- `highlights` は箇条書き 3 点以上
- 緯度経度は WGS84、小数点 6 桁、Google Maps で実在確認済み

### 推奨

- インライン出典は Markdown 記法 `[出典名](URL)`
- 不確かな情報は summary 内で明示
- 撮影禁止・私有地・宗教マナー等は `warnings_extra` に明記
- 英訳は自然な英語（逐語訳でなく）

### NG

- 怪奇・心霊・オカルト的な煽り表現
- 無断侵入を前提とした記述
- 出典なしの伝承を断定的に書く
- 「source」「link」のような汎用語をアンカーテキストに使う

---

## 7. トラブル対応

### ID 連番が衝突した

- どちらかが採番をやり直す（後発側が振り直す）
- リモート最新の最大 ID を確認して連番付与

### push が rejected された

- `git pull --rebase origin main`
- コンフリクトを解消
- 再 push

### Computer 側の cron が動かない

- Perplexity 側で `schedule_cron` の状態を確認
- 必要なら再作成

### Mac の Claude Code が動かない

- いったん Computer 側に戻して作業を継続
- 軽微な作業なら Computer 側で main 直 push

---

最終更新: 2026-05-27
