# permission_requests/ — 写真使用許諾 運用マニュアル

このディレクトリは、Bizarre Japan / 異界巡礼 に掲載する写真の **使用許諾取得・追跡・返信対応** を集中管理するための作業領域です。
**2026-06-02 より、本ワークフローは Claude Code が主担当となります**（移管前は Perplexity Computer が運用）。

## 目的

1. 各掲載候補スポット／祭事に対する写真権利者への許諾申請の進捗を一元管理
2. 送信文・受信文・添付資料を追跡可能な形で保存
3. 許諾確定後、`photos.json` の `credit` / `license` フィールドを正しく更新する判断材料を提供
4. 同一案件の再交渉や類似ケースで使い回せるテンプレート群を整備

## ディレクトリ構成

```
permission_requests/
├── README.md                      # 本ファイル（運用ルール）
├── WORKFLOW.md                    # Claude Code 向け運用手順書
├── INDEX.md                       # 全申請の進捗ダッシュボード
├── PHOTO_CREDIT_POLICY.md         # 写真クレジット・サイト表記ルール
├── templates/                     # 依頼文・申請書テンプレート群
│   ├── jinja_email.md             #   神社・寺院向け初回依頼
│   ├── municipal_email.md         #   自治体・教育委員会向け初回依頼
│   ├── tourism_assoc_email.md     #   観光協会・観光連盟向け初回依頼
│   ├── negotiation_reply.md       #   懸念表明への返信パターン
│   ├── thanks_reply.md            #   許諾受領後のお礼返信
│   ├── apology_misaddress.md      #   誤宛先お詫び
│   ├── application_form.md        #   写真使用許可申請書（Markdown版）
│   ├── application_form_template.json  # DOCX生成用の穴埋め定義
│   └── build_application_form.js  #   DOCX自動生成スクリプト
├── sent/                          # 送信済メール本文（ID単位）
│   └── <id>_<recipient>_<YYYY-MM-DD>.md
├── received/                      # 受信メール抜粋（ID単位）
│   └── <id>_<sender>_<YYYY-MM-DD>.md
├── tracking/                      # 月次チャネル進捗
│   └── channels_YYYY-MM.md
├── hold/                          # 連絡先不明等の保留案件
└── handoff/                       # Claude Code への引継ぎノート
    ├── MIGRATION_NOTES.md
    └── todoist_issues.md
```

## 運用ルール

### 1. 署名フォーマット（固定）

全ての送信メールは下記署名で統一する。**GitHub URL は記載しない**。

```
────────────────────────────────────
【所属】
有限会社豊田衛生 取締役（三重県亀山市／下水道・排水・水道インフラの維持管理・建設業）
https://toyodaeisei.com/
亀山商工会議所青年部 2026年度 会長
https://kameyama-yeg.jp/

※本依頼は個人運営の文化記録プロジェクトとしての依頼であり、所属団体の事業ではありません。

豊田 元洋 / Toyoda Motohiro
Bizarre Japan / 異界巡礼 運営
Email: motohiro.toyoda@gmail.com / bizarrejapan.jp@gmail.com
Web: https://bizarrejapan.com/
Instagram: @bizarre_japan
所在: 〒519-0105　三重県亀山市
────────────────────────────────────
```

**簡略署名**（個人取引・小規模団体・お礼返信等で使用可）:

```
────────────────────────────────────
豊田 元洋（とよだ もとひろ）

Bizarre Japan / 異界巡礼 運営
Web：https://bizarrejapan.com/
Instagram：@bizarre_japan

亀山商工会議所青年部（YEG）　2026年度 会長
Email：motohiro.toyoda@gmail.com／bizarrejapan.jp@gmail.com
所在：〒519-0105　三重県亀山市
────────────────────────────────────
```

### 2. 送信前チェックリスト

- [ ] 宛先が正規の団体・施設のものか（**同名異所注意**：例 福岡県淡島神社 vs 和歌山県加太淡嶋神社）
- [ ] 対象スポット／祭事の ID（`spot-XXX` / `fest-XXX`）が文中に明示されている
- [ ] 公式情報確認先 URL が記載されている
- [ ] 電話番号は載せない（メールアドレスのみ）
- [ ] 署名が上記フォーマット通り
- [ ] ユーザー（豊田元洋氏）の事前承認済

### 3. 送信後の必須作業

1. `sent/<id>_<recipient>_<YYYY-MM-DD>.md` に送信本文を保存（メタデータ：宛先・件名・送信日時・期待返信期限）
2. 返信受領時は `received/<id>_<sender>_<YYYY-MM-DD>.md` に抜粋を保存
3. `tracking/channels_YYYY-MM.md` に1行追加（状態・期限・備考）
4. `INDEX.md` を更新（一覧表に反映）
5. 許諾確定時は `photos.json` の `credit` / `license` を更新（必須）

### 4. ステータス定義

| ステータス | 意味 |
|---|---|
| `draft_in_progress` | 送信文ドラフト作成中 |
| `sent` | 送信済、返信待ち |
| `awaiting_reply` | 期限内で返信待機 |
| `awaiting_phone_call` | 電話確認待ち（メール非公開等） |
| `replied_pending_action` | 返信あり、こちらの次アクション必要 |
| `negotiation` | 先方が懸念表明。差替・調整を交渉中 |
| `conditional` | 条件付許諾（クレジット指定・範囲制限等） |
| `permitted` | 許諾取得済、`photos.json` 更新可 |
| `denied` | 不許可、当該写真は掲載不可 |
| `hold` | 連絡先不明・公式ソース弱で一時保留 |
| `exclude` | 掲載中止判断 |
| `misaddress_recovered` | 誤宛先を発見し、お詫び＋正規宛先再送で復旧 |

### 5. 公式ソース判断基準

- **強**：一次資料（自治体公式、文化財DB、神社庁登録、観光連盟公式、寺社直営）
- **中**：Wikipedia 日本語版（出典付き）、学術論文（CiNii/J-STAGE）、地方紙、NHK
- **弱**：個人ブログ・SNS のみ → 原則 `hold` または `exclude`

### 6. データ更新の境界

- **このタスクで触ってよい**：
  - `permission_requests/` 配下（自由）
  - `photos.json`（許諾確定後の `credit` / `license` 更新のみ）
- **触らない**：
  - `spots.json` / `festivals.json` の本体内容（別タスク管理）
  - `data.js` / `build_data.py` 等の本体ロジック
- **photos.json を編集した場合**：`python3 build_data.py` を実行し、`data.js` を必ず同梱コミット（CI で検証されます）

### 7. GitHub 操作

- すべて Claude Code 環境（ローカル `git` / `gh`）から実施
- 変更は PR ベース。タイトル・差分概要・デプロイ要否を提示してから実行
- `permission_requests/` 配下のみの変更で `photos.json` を触らない場合は **main 直 push 可**

### 8. ユーザー（豊田元洋氏）への確認義務

以下のアクションは **必ず事前にユーザー承認**を取る：

| アクション | 承認方法 |
|---|---|
| 新規メール送信（初回依頼） | 全文ドラフトを提示 → OKをもらう |
| 返信メール送信 | 全文ドラフトを提示 → OKをもらう |
| 写真の `denied` 確定 → 掲載削除 | 削除対象を明示 → OKをもらう |
| 条件付許諾（`conditional`）の条件解釈 | 解釈案を提示 → OKをもらう |

**承認は Markdown ドラフトをチャットで提示する形式**で行う。`confirm_action` ツールは日本語表示の不具合があるため使用しない。

## 関連ドキュメント

- `WORKFLOW.md` — Claude Code 向け運用手順書
- `PHOTO_CREDIT_POLICY.md` — 写真クレジット表記ルール
- `INDEX.md` — 全申請ダッシュボード
- `../docs/workflow.md` — リポジトリ全体ワークフロー
- `../docs/schema.md` — JSON スキーマ仕様
- `../photos.json` — 写真メタデータ本体
