# 写真掲載許可申請 トラッキング — 2026年6月

## サマリ（実行ログ）

| 日付 | ID | アクション | 相手 | 状態遷移 |
|---|---|---|---|---|
| 2026-06-02 | fest-114 | **条件付き許諾受領（4点回答 / No.1858）** | 石川県観光連盟 披岸様 | `assigned` → **`conditional`** |

## 着手予定（Claude Code が判断・実行）

| 優先 | ID | 次アクション | テンプレ |
|---|---|---|---|
| 🔴 高 | fest-114 | お礼返信ドラフト（披岸様宛） | `templates/thanks_reply.md` |
| 🔴 高 | fest-114 | 「ほっと石川旅ねっと」DBから写真選定 → `spots.json` 反映 | — |
| 🟡 中 | spot-118 | 高鍋町観光協会 加藤事務局長からの再返信を待機（5/30送付） | `negotiation_reply` 続報待ち |
| 🟡 中 | spot-122 | 加太淡嶋神社へ電話（平日 9:00〜17:00） | `hold/spot-122_call_script.md` |
| 🟢 低 | fest-116 | PR #5 を rebase + マージ後にお礼返信 | `templates/thanks_reply.md` |
| 🟢 低 | fest-117 | PR #2 を rebase + マージ後にお礼返信 | `templates/thanks_reply.md` |

## 6月の運用方針（Claude Code 引き渡し後）

- すべての送付・受領は **当該IDの `sent/` `received/` フォルダにmdで控え**を残すこと。
- 状態遷移は **本月度のトラッキングファイルに必ず1行追記**してから commit。
- 取り下げ要請が来た場合、**24時間以内に photo_url を `null` 化 + build_data.py 再生成 + コミット**。
- 月末（6/30）に `tracking/channels_2026-06.md` をクローズして翌月ファイルを作成。
