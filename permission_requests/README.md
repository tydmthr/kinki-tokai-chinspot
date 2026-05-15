# permission_requests/ — 写真使用許諾 運用マニュアル

このディレクトリは、Bizarre Japan / 異界巡礼 に掲載する写真の **使用許諾取得・追跡・返信対応** を集中管理するための作業領域です。
新規スポット発掘や奇祭発掘は対象外（別タスク管理）。

## 目的
1. 各掲載候補スポット／祭事に対する写真権利者への許諾申請の進捗を一元管理
2. 送信文・返信内容・添付資料を追跡可能な形で保存
3. 許諾確定後、`photos.json` の `photo_status` を `permitted_external` 等に更新する判断材料を提供

## ディレクトリ構成
```
permission_requests/
├── README.md              # 本ファイル（運用ルール）
├── INDEX.md               # 全申請の進捗ダッシュボード
├── tracking/              # 月次・団体別チャネル進捗
│   └── channels_YYYY-MM.md
├── sent/                  # 送信済メール本文を ID 単位で保存
│   └── <id>_<recipient>_<YYYY-MM-DD>.md
├── templates/             # 依頼文テンプレート（神社用・自治体用・観光連盟用等）
└── hold/                  # 公式ソース弱・連絡先不明等で保留中の案件
```

## 運用ルール

### 1. 署名フォーマット（固定）
全ての送信メールは下記署名で統一する。GitHub URL は記載しない。

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
所在: 三重県亀山市
────────────────────────────────────
```

### 2. 送信前チェックリスト
- [ ] 宛先が正規の団体・施設のものか（同名異所注意）
- [ ] 対象スポット／祭事の ID（spot-XXX / fest-XXX）が文中に明示されている
- [ ] 公式情報確認先 URL が記載されている
- [ ] 署名が上記フォーマット通り
- [ ] confirm_action で全文承認済

### 3. 送信後の必須作業
1. `sent/<id>_<recipient>_<YYYY-MM-DD>.md` に送信本文を保存（メタデータ：宛先・件名・送信日時・期待返信期限）
2. `tracking/channels_YYYY-MM.md` に1行追加（状態・期限・備考）
3. `INDEX.md` を更新（一覧表に反映）

### 4. ステータス定義
| ステータス | 意味 |
|---|---|
| `sent` | 送信済、返信待ち |
| `awaiting_reply` | 期限内で返信待機 |
| `replied_pending_action` | 返信あり、こちらの次アクション必要 |
| `permitted` | 許諾取得済、`photos.json` 更新可 |
| `denied` | 不許可、当該写真は掲載不可 |
| `conditional` | 条件付許諾（クレジット指定・範囲制限等） |
| `hold` | 連絡先不明・公式ソース弱で一時保留 |
| `exclude` | 掲載中止判断 |
| `misaddress_recovered` | 誤宛先を発見し、お詫び＋正規宛先再送で復旧 |

### 5. 公式ソース判断基準
- **強**：一次資料（自治体公式、文化財DB、神社庁登録、観光連盟公式）
- **中**：Wikipedia 日本語版（出典付き）、学術論文、地方紙
- **弱**：個人ブログ・SNS のみ → 原則 `hold` または `exclude`

### 6. データ更新の境界
- **このタスクで触ってよい**：`permission_requests/` 配下、`photos.json`（許諾確定後のみ）
- **触らない**：`spots.json` / `festivals.json` / `data.js` / `build_*.py` 等の本体ロジック

### 7. GitHub操作
- すべて `github_mcp_direct` 経由（`gh` / `git` CLI）。`browser_task` での GitHub 操作は **禁止**。
- 変更は PR ベース。タイトル・差分概要・デプロイ要否を提示してから実行。

## 関連ドキュメント
- `../press-kit.md` … サイト紹介資料（依頼文に添付可）
- `../photos.json` … 写真メタデータ本体
- `bizarre_japan_listing_policy_2026-05-11.md`（Space内） … 掲載方針
