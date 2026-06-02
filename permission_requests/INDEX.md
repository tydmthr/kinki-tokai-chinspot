# 写真掲載許可申請 INDEX

> Claude Code 完全移行時点のスナップショット（2026-06-02 JST）。
> 以後の更新は Claude Code 主担当で行うこと。

## ディレクトリ構成

```
permission_requests/
├── INDEX.md                     ← 本ファイル（全案件のサマリ）
├── README.md                    ← 拡張運用マニュアル
├── WORKFLOW.md                  ← Claude Code向け手順書（9章構成）
├── PHOTO_CREDIT_POLICY.md       ← 写真クレジット表記ルール
├── templates/                   ← 申請書・メール各種テンプレ
│   ├── README.md
│   ├── application_form.md      ← 申請書MD版
│   ├── application_form_template.json  ← DOCX生成用 JSON Schema
│   ├── build_application_form.js  ← DOCX 汎用生成 script
│   ├── jinja_email.md           ← 神社・寺院向け
│   ├── municipal_email.md       ← 自治体向け
│   ├── tourism_assoc_email.md   ← 観光協会向け
│   ├── negotiation_reply.md     ← 懸念対応
│   ├── thanks_reply.md          ← お礼返信
│   └── apology_misaddress.md    ← 誤宛先お詫び
├── sent/                        ← 送付済メールの控え（IDごと）
├── received/                    ← 受領メール記録
├── hold/                        ← 待機案件（電話確認待ち等）
├── tracking/                    ← 月次トラッキングログ
│   ├── channels_2026-05.md
│   └── channels_2026-06.md
└── handoff/                     ← Claude Code 引き継ぎ資料
    ├── MIGRATION_NOTES.md
    └── todoist_issues.md
```

## 全案件サマリ（2026-06-02 時点）

| ID | 対象 | 所在 | 状態 | 相手 | クレジット | 次アクション |
|---|---|---|---|---|---|---|
| spot-001 | 平等寺穴弘法 | 三重県亀山市 | `legacy_owned` | 自前撮影 | （不要） | — |
| spot-118 | 高鍋大師 | 宮崎県高鍋町 | `negotiating` | 高鍋町観光協会 加藤事務局長 | 未定 | 返信待ち（5/30送付） |
| spot-122 | 加太淡嶋神社（正規） | 和歌山県和歌山市加太 | `awaiting_phone_call` | TEL 073-459-0043 | 未定 | 電話 → メアド入手 |
| spot-122 | 福岡県淡島神社（誤送） | 福岡県粕屋郡新宮町 | `apology_sent_manually` | （クローズ） | — | クローズ済（不追跡） |
| fest-114 | 能登のアマメハギ | 石川県輪島市 | **`conditional`** ✅ | 石川県観光連盟 披岸様 | ©石川県観光連盟 | お礼返信＋写真選定 |
| fest-116 | 六郷のカマクラ | 秋田県美郷町 | **`public`** ✅ | あきた美郷づくり 荒田様（窓口）／六郷のカマクラ行事継承会（権利者） | 写真提供　六郷のカマクラ行事継承会 | お礼＋お詫びメールを Spark から送信（下書き `r-5758993908194219284`） |
| fest-117 | 白石踊 | 岡山県笠岡市白石島 | **`public`** ✅ | 笠岡市教委 安東康宏様 | 写真提供　笠岡市教育委員会 | お礼＋確認URL報告を Spark から送信（下書き `r6055418020300255053`） |
| fest-118 | 御陣乗太鼓？（仮） | 石川県輪島市（推定） | `unspecified_hold` | 未特定 | — | 対象スポット要特定 |

## 状態カラー凡例

- 🟢 `conditional` / `approved` — 許諾済（条件付き含む）。次アクション「お礼返信＋写真公開」
- 🟡 `negotiating` / `concerned` — 懸念対応中。先方の再返信待ち
- 🟡 `sent` / `assigned` — 送付済・割り当て済。回答待ち
- 🔵 `awaiting_phone_call` — 電話確認待ち（メアド非公開）
- ⚪ `apology_sent_manually` — 誤送・お詫び済（不追跡）
- ⚫ `unspecified_hold` — 対象未特定でhold
- 🔴 `declined` — 拒否（spots.json側で photo_url を `null` に）

## 状態遷移ステート図

```
none ─→ sent ─→ assigned ─→ conditional ─→ public
                 │              │
                 ▼              ▼
              concerned    お礼返信送付
                 │
                 ▼
             negotiating ─→ conditional
                         │
                         └─→ declined

別系統:
none ─→ misaddressed ─→ apology_sent_manually （クローズ）
none ─→ awaiting_phone_call ─→ sent ─→ ...
```

## クロスリファレンス

| 関連 PR | 対象案件 | 状況 |
|---|---|---|
| PR #1 | スキャフォールド | 本PRで統合 → close 予定 |
| PR #2 | fest-117 白石踊 | rebase + マージ待ち |
| PR #5 | fest-116 六郷のカマクラ | rebase + マージ待ち |

## ファイル命名規約

- 送付: `sent/{id}_{相手スラッグ}_{YYYY-MM-DD}[_用途].md`
- 受領: `received/{id}_{相手スラッグ}_{YYYY-MM-DD}.md`
- 待機: `hold/{id}_{種別}.md`（例: `_call_script.md`, `_legacy_routes.md`, `_declined.md`）
- 月次: `tracking/channels_{YYYY-MM}.md`
- DOCX: `templates/`配下で `build_application_form.js` から動的生成
