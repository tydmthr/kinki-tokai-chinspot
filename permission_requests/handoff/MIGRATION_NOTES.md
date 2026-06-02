# Claude Code 移行ノート — 写真掲載許可申請ワークフロー

## 移行サマリ

- **移行日**: 2026-06-02 JST
- **移行元**: Perplexity Computer（Bizarrejapan Space）
- **移行先**: Claude Code（ローカル運用、tydmthr/kinki-tokai-chinspot リポ）
- **移行範囲**: 写真掲載許可申請の全ワークフロー（テンプレ／案件履歴／状態管理／DOCX生成）
- **トリガー**: 5/30に Code/PR主担当を Claude Code に集約済。Computer は発掘・SNS・cron・JSON更新の副担当へ役割分担。

## 移行に伴う運用変更

| 項目 | 移行前（Computer） | 移行後（Claude Code） |
|---|---|---|
| メール下書き作成 | gcal `draft_email` 経由で Gmail 下書き | Claude Code がローカルで .md 起稿 → ユーザが Spark で送信 |
| DOCX 生成 | workspace で `node build_application_form.js` | 同左、ただしリポ内 `templates/` で実行 |
| 案件履歴 | Computer の会話ログ + Memory | **`permission_requests/sent/` `received/` の md 記録に一本化** |
| 状態管理 | 暗黙（Memory + サマリ） | **`INDEX.md` + `tracking/channels_*.md` の明示** |
| 送付済確認 | Gmail email_id を Memory 参照 | sent/受領 md 内に `Gmail email_id` を必ず記載 |
| PR編集 | `gh api -X PATCH /repos/.../pulls/N` | 同左（`gh pr edit` はGraphQL classic projectsで失敗） |

## 重要な手順（Claude Codeが必ず守ること）

1. **新規案件着手時**は `WORKFLOW.md` の §3 「申請プロセス10ステップ」を順守。
2. **状態遷移時**は `tracking/channels_<YYYY-MM>.md` に1行追加してから commit。
3. **PR編集**は GraphQL classic projects エラーを避けるため REST API 直叩き:
   ```bash
   gh api -X PATCH /repos/tydmthr/kinki-tokai-chinspot/pulls/<N> \
     -f title="..." -f body="..."
   ```
4. **DOCX生成**は `templates/build_application_form.js` + JSON入力で行う。フォントは Yu Mincho を指定。
5. **写真公開時**:
   - `spots.json` 更新
   - `python3 build_data.py` 実行（data.js + index.html + en/index.html 同梱コミットが必須。CI `data-sync-check.yml` が fail 判定）
   - `data/photos.json` に `photo_credit` を追加（schema.md §1.6）
6. **取り下げ要請** が来た場合、24時間以内に photo_url を `null` 化 + build_data.py 再生成 + コミット + push。

## ユーザ（豊田元洋様）の運用前提

- メーラー: **Spark**（Gmail連携、Gmail下書きで同期）
- 添付は Gmail 下書きAPI不可 → 本文に添付ファイル名明記 + Spark側で手動添付
- 申請書に**電話番号は載せない**（メールアドレスのみ）
- 添付メール署名は **サイトURL＋Instagram＋YEG肩書きのみ**
- 郵便番号: **〒519-0105 三重県亀山市**
- 業務以外の依頼であることを必ず明記（「※本依頼は個人運営の文化記録プロジェクトとしての依頼であり、所属団体の事業ではありません。」）
- **confirm_action は使用禁止**（日本語が \uXXXX エスケープになる）。承認はチャット本文で「OK」を貰う方式。
- **送信元エイリアス運用（2026-06-02〜）**: 許諾系メールの From は **`bizarrejapan.jp@gmail.com`**（運営用Gmail）。Gmail 側で個人Gmail (motohiro.toyoda@gmail.com) にエイリアス追加済。Claude Code の `mcp__claude_ai_Gmail__create_draft` は motohiro.toyoda@gmail.com アカウントに下書き作成 → Spark で From を `bizarrejapan.jp@gmail.com` に切り替えて送信。
  - **CC: `bizarrejapan.jp@gmail.com` は不要**（自分から自分への控え重複を避ける）
  - 既存下書き（fest-116 draft `r-5758993908194219284` / fest-117 draft `r6055418020300255053`）も同様に Spark で From 切替＋CC 削除して送信

## 現時点で進行中（Claude Code が優先処理）

| 優先 | ID | 次アクション | 期限目安 |
|---|---|---|---|
| 🔴 高 | fest-114 | お礼返信ドラフト（披岸様宛） + 写真選定 + spots.json反映 | 2026-06-04 |
| 🟡 中 | spot-118 | 高鍋町観光協会 加藤事務局長の再返信を待機（届き次第対応） | 6月中 |
| 🟡 中 | spot-122 | 加太淡嶋神社へ電話（平日 9:00〜17:00） | 6月中 |
| 🟢 低 | fest-116 / fest-117 | PR #5 / #2 を rebase + マージ + お礼返信 | 6月中 |

## ファイル一覧（移行時点）

```
permission_requests/
├── INDEX.md, README.md, WORKFLOW.md, PHOTO_CREDIT_POLICY.md
├── templates/  (10ファイル)
├── sent/       (5ファイル — spot-118 x2, spot-122 x2, fest-114, fest-116, fest-117)
├── received/   (4ファイル — spot-118, fest-114, fest-116, fest-117)
├── hold/       (2ファイル — spot-122 call script, fest-114 legacy routes)
├── tracking/   (2ファイル — 2026-05, 2026-06)
└── handoff/    (本ファイル + todoist_issues.md)
```

## 連絡フロー（Computer ↔ Claude Code）

- Computer 側で「新スポット発掘 → spot-xxx 候補確定」したら、
  `docs/NOTICE_BOARD.md` に Computer→Claude Code の「**REPORT / QUESTION / ACK**」プロトコルで通知。
- Claude Code は通知を受け、本 `permission_requests/` 配下で申請フローを起動。
- Computer は SNS・cron・Instagram フィード更新には引き続き責任を持つ。

## クローズ条件

本PRがマージされた時点で、PR #1（スキャフォールド）は自動的に閉じる。
以後、Computer 側で `permission_requests/` を直接編集することはない（緊急時のみ）。
