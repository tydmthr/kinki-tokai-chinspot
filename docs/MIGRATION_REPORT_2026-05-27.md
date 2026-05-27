# Claude Code 移行 評価レポート

最終更新: 2026-05-27 (JST)
作業実施: Mac (MacBook Air M3) / 三重県亀山市
対象リポジトリ: [tydmthr/kinki-tokai-chinspot](https://github.com/tydmthr/123/edit/main/Bizarre Japan / 異界巡礼)

Computer 側 (03 CLAUDE.md / 04 Space ファイル配置 / 05 docs/workflow.md / 09 IG cron 方針) と
並行して進めた Mac 側 6 タスク (01・02・06・07・08・10) の総括と、検出された
改善候補をまとめる。

---

## 1. 環境セットアップ結果

### バージョン一覧

| 項目 | バージョン | 備考 |
|---|---|---|
| macOS | 26.3.1 (build 25D771280a) | Apple Silicon (arm64) |
| Xcode CLT | 導入済み | `/Library/Developer/CommandLineTools` |
| Homebrew | 5.1.14 | `/opt/homebrew` |
| git | 2.50.1 (Apple Git-155) | `/usr/bin/git` |
| GitHub CLI (`gh`) | 2.92.0 | HTTPS / `tydmthr` ログイン済み |
| Node.js | v26.0.0 | Homebrew |
| npm | 11.12.1 | Node 同梱 |
| Claude Code (`claude`) | 2.1.152 | `npm install -g @anthropic-ai/claude-code` |
| Python | 3.13.7 | `/usr/local/bin/python3` |
| pip | 25.2 | — |

### git グローバル設定

| key | value |
|---|---|
| `user.name` | `tydmthr` |
| `user.email` | `motohiro.toyoda@gmail.com` |
| `init.defaultBranch` | `main` |

### GitHub 認証

- 方式: HTTPS + `gh auth login`（ブラウザ認証）
- 認証アカウント: `tydmthr`
- Git protocol: `https`

### 作業ディレクトリ

```
/Users/toyodamotohiro/Documents/Claude/Projects/Bizarre Japan/kinki-tokai-chinspot
```

---

## 2. 動作確認結果

### 02 clone & push test

| 項目 | 結果 |
|---|---|
| clone | ✅ 53 entries / 8.61 MiB / 617 objects |
| 新規ファイル配置 (`docs/MAC_SETUP_CHECK.md`) | ✅ 1486 bytes |
| commit | ✅ `bea7e3f chore: add Mac setup check note (Claude Code migration 01)` |
| push | ✅ `4d55639..bea7e3f main -> main` |
| GitHub 反映 | ✅ author=`tydmthr` / sha=`89cdca3` |

### 06 bulk_add.py 動作確認（最小1行）

| 項目 | 結果 |
|---|---|
| `--no-build` 実行 | ✅ `+ spot-158: テスト珍スポット` |
| 採番ロジック | ✅ 既存最大番号 +1 (`spot-157` → `spot-158`) |
| spots.json 書き出し構造 | ✅ id/name/location/lat/lng/summary/wiki_url/source/review_pending |
| 巻き戻し | ✅ `git checkout` で復旧 |

### 07 取り込みテスト（A方式: 3行 + build_data.py 連動）

| 検証項目 | 結果 |
|---|---|
| 採用行の取り込み | ✅ `+ spot-158: テスト取り込み1_採用` |
| 不採用行スキップ | ✅ ログ出力なし |
| 重複行スキップ | ✅ `SKIP 重複: テスト取り込み3_重複` |
| build_data.py 連動 | ✅ `data.js regenerated: 158 spots, 159 festivals` |
| index.html 件数自動置換 | ✅ 16 箇所 |
| en/index.html 件数自動置換 | ✅ 15 箇所 |
| 全体 diff | 4 ファイル / +36 -25 |
| 巻き戻し | ✅ 全変更 checkout、status クリーン |

### 08 dev server 起動

| 項目 | 結果 |
|---|---|
| `python3 -m http.server 8000` | ✅ Mac 側で正常起動 |
| ブラウザアクセス | ✅ `http://localhost:8000/` 表示 |
| デザイン崩れ | なし |
| ナビゲーション（地図/祭暦/名鑑/巡路/EN） | ✅ |
| 数値カウンタ「珍スポット」 | ⚠️ **142** と表示 — Issue-1 参照 |
| 数値カウンタ「奇祭・暦」 | 159 |
| 数値カウンタ「府県」 | 47 |

---

## 3. 発見された Issue / 改善候補

### Issue-1: data.js の「珍スポット」件数が spots.json と乖離している（要修正）

| 観測 | 値 |
|---|---|
| `spots.json` 内のエントリ数 | **157 件** |
| 直近コミット時点の `data.js` 内の `SPOTS.length` | **142 件** |
| ブラウザ表示の数値カウンタ「珍スポット」 | **142** |
| `index.html` のタイトル/OG/Twitter テキスト | **157**（自動置換済み） |
| 試しに `python3 build_data.py` 再実行後 | 142 → **157** に揃った |

**結論**: `spots.json` に新規 15 件が追加された後、`build_data.py` を流さずに
`spots.json` のみコミットされた履歴がある。`data.js` がビルド未反映のまま
公開されている状態。

**影響**:
- ヒーローの数値カウンタが実態より 15 件少なく表示される
- list-tab の「珍スポット N」表示も連動して 142 表示
- 地図マーカー / カードに表示されるスポット自体が 15 件欠落
  （`SPOTS` 配列がそもそも 142 件しか持っていない）

**対処案**:
1. **即時対応**: ローカルで `python3 build_data.py` → `git add -A` → `commit "chore: rebuild data.js (sync with spots.json)"` → push
2. **再発防止 (CI)**: GitHub Actions で push 時に `build_data.py` を走らせて
   `data.js` が差分なしになることを検証するワークフロー追加
3. **CLAUDE.md 追記**: 「spots.json / festivals.json を編集したら必ず `build_data.py` を
   流してから commit する」を明文化

### Issue-2: bulk_add.py のエントリスキーマが定義と齟齬

**Space 指示書 / CLAUDE.md で定義された spots.json スキーマ**:
```
{ id, name, name_kana, name_en, lat, lng, category, prefecture,
  address, description, source, photo_url, visit_url? }
```

**bulk_add.py が実際に生成するキー** (`scripts/bulk_add.py` 末尾):
```
{ id, name, location, lat, lng, summary, wiki_url, source, review_pending }
```

**齟齬の詳細**:

| 定義スキーマ | bulk_add.py 生成 | 状況 |
|---|---|---|
| `name_kana` | なし | 欠落 |
| `name_en` | なし | 欠落 |
| `category` | なし | 欠落（CSV `category` 列は spots/festivals 振り分けにしか使われていない） |
| `prefecture` | なし | `location` で代用？ |
| `address` | なし | `location` で代用？ |
| `description` | `summary` | キー名違い |
| `photo_url` | なし | 欠落 |
| `visit_url` | なし | 欠落 |
| `wiki_url` | （定義外） | bulk_add 独自 |
| `review_pending` | （定義外） | bulk_add 独自 |

**対処案**:
- `bulk_add.py` を改修し、CSV の `name_kana` / `name_en` / `category` / `prefecture` /
  `address` / `description` 列を読み取って正しく転記
- `summary` → `description` への列名整理 (`build_data.py` / `app.js` も追従)
- `wiki_url` / `review_pending` は補助フィールドとして残すなら CLAUDE.md に追記
- 既存 142+15=157 件のエントリのキー揺れをマイグレーションスクリプトで整える

### Issue-3: build_data.py の HTML 自動置換仕様が未文書化

`build_data.py` は以下のサイドエフェクトを持つが、`docs/workflow.md` や
`CLAUDE.md` には明記されていない:

- `index.html` の `<title>` / `<meta description>` / `<meta og:title>` /
  `<meta og:description>` / `<meta twitter:description>` の **件数表記を正規表現で置換**
- `en/index.html` についても同様の置換（15 箇所）
- 置換対象は「珍スポット N」「奇祭 M」「N strange spots and M wild festivals」など
  の数字パターン

**対処案**:
- `docs/workflow.md` の「ビルド」セクションに副作用を箇条書き追記
- `CLAUDE.md` に「`build_data.py` を流すと spots.json/festivals.json と
  HTML のメタ件数まで自動同期される」と明記

### Issue-4: candidates/ にサンプル CSV が存在しない

現状 `candidates/` は `.gitkeep` のみ。CSV ヘッダー仕様が散逸している。

**対処案**:
- `candidates/_sample.csv` を 1 本コミット（採用/不採用/重複の 3 行例 +
  全列ヘッダー）
- `docs/workflow.md` の「候補取り込み」セクションからリンク

### Issue-5: Mac 環境では gh CLI の認証が HTTPS 経由のみ

現在 `~/.ssh/` ディレクトリが存在せず、SSH 鍵を持っていない。`gh auth login` で
HTTPS + ブラウザ認証を選択したため動作上の問題はない。ただし将来:

- 別端末からの clone / push
- 別リポジトリ (private) の運用
- 自動化スクリプトでの push

が発生する場合は SSH 鍵 (`ssh-keygen -t ed25519`) を生成して GitHub に登録する
余地あり。優先度は低い。

---

## 4. Claude Code 移行の総評

### Computer 側 / Mac (Claude Code) 側の役割分担

| 役割 | 担当 | 理由 |
|---|---|---|
| 候補発掘・裏取り（外部 Web 調査） | **Computer** | ブラウザ / fetch / 検索ツールが豊富 |
| Space ファイル (docs/policy/manual) 配置 | **Computer** | Space 内ファイル管理が直接できる |
| CLAUDE.md / docs/workflow.md 編集 | **Computer** | リポジトリへの書き込みも可能 |
| `bulk_add.py` 実行 / 取り込み作業 | **Mac (Claude Code)** | ローカルの spots.json を直接編集できる |
| dev server 起動 / 目視確認 | **Mac** | ブラウザ目視は人間の眼が要る |
| commit / push | **Mac** | 外向きネットワーク制約のため Computer 側からは push 不可 |
| Instagram cron / GitHub Actions の方針策定 | **Computer** | 仕様検討と文書化に向く |
| Instagram cron の実装デプロイ | **Mac** | 実環境へのコミットが要る |

### 運用フロー（推奨）

1. **候補発掘**: Computer に「○○県の珍スポット候補を 10 件」と依頼 → CSV 生成
2. **CSV を Mac の `candidates/` へ配置**: Computer 経由か手動 DL
3. **Mac で `bulk_add.py` 実行**: `python3 scripts/bulk_add.py --csv candidates/YYYY-MM.csv`
4. **dev server で目視確認**: `python3 -m http.server 8000`
5. **問題なければ commit & push**: `git add -A && git commit -m "..." && git push`
6. **GitHub Pages / 本番反映を確認**

### 移行の利点（既に体感）

- **ローカル直接編集**: 巨大 `spots.json` (1.37 MB) の編集が高速
- **対話的デバッグ**: Claude Code でファイル内容を見ながら即修正
- **コミット粒度の制御**: Mac 側 git で適切な単位に分割可能

### 残る課題

- Issue-1〜4（上記）を順次解消
- Computer / Mac 間でのファイル受け渡しの自動化（現状は手動 push）
- Instagram cron の Mac ローカル実行 vs GitHub Actions 化の決定

---

## 5. 次のアクション（提案）

優先度順:

1. **Issue-1 即時対応** (5分): `build_data.py` 再実行 → data.js 同期コミット
2. **Issue-4** (10分): `candidates/_sample.csv` を整備してコミット
3. **Issue-3** (15分): `docs/workflow.md` / `CLAUDE.md` に build_data.py 副作用を追記
4. **Issue-2** (1〜2時間): bulk_add.py のスキーマ整合 + 既存データのマイグレーション
5. **Issue-1 再発防止 (CI)** (30分): GitHub Actions で build 整合性チェック

---

(以上)
