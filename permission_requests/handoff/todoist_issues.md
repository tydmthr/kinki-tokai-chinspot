# Todoist / GitHub Issue 起票案（Claude Code 着手用）

> 本ファイルは Claude Code への引き渡し直後に、Todoist プロジェクト
> 「Bizarre Japan / 写真許可申請」配下に転記する想定の Issue 集。
> ユーザが Todoist 連携で直接タスク化してもよい。

---

## Issue 1: fest-114 お礼返信＋写真選定＋公開

**優先度**: 🔴 高（期限 2026-06-04）

**タスク**:
- [ ] `templates/thanks_reply.md` を元に、披岸様宛のお礼返信ドラフトを作成
- [ ] 「ほっと石川旅ねっと」DB（https://www.hot-ishikawa.jp/）から「能登のアマメハギ」関連画像を1〜3点選定
- [ ] `spots.json` の fest-114 の `photo_url` を採用画像のURLに更新
- [ ] `data/photos.json` に `"photo_credit": "©石川県観光連盟"` を追加
- [ ] `python3 build_data.py` 実行 → data.js + index.html + en/index.html 同梱コミット
- [ ] PR 作成 → main へマージ
- [ ] お礼返信メールを送付（公開URLを本文中で報告）

**関連ファイル**:
- `permission_requests/received/fest-114_ishikawa-tourism_2026-05-28.md`
- `permission_requests/hold/fest-114_legacy_routes.md`

---

## Issue 2: spot-118 高鍋大師 返信フォローアップ

**優先度**: 🟡 中

**タスク**:
- [ ] 加藤事務局長（高鍋町観光協会）からの再返信を Gmail thread `19e72f1bf26dd515` で監視
- [ ] 返信受領後、`received/spot-118_takanabe-kanko_<日付>.md` に記録
- [ ] 内容に応じて: 許諾→お礼返信、追加懸念→`negotiation_reply.md` で再度対応、拒否→spots.json 側で photo_url を `null` 化

**ステート**: `negotiating`（5/30 negotiation_reply 送付済）

---

## Issue 3: spot-122 加太淡嶋神社 電話確認

**優先度**: 🟡 中

**タスク**:
- [ ] `hold/spot-122_call_script.md` のスクリプト確認
- [ ] 平日 9:00〜17:00 に **TEL 073-459-0043** へ架電
- [ ] メールアドレス入手 → `sent/spot-122_kada-awashima_<日付>_application.md` 作成
- [ ] メール送付不可とされた場合は郵送（DOCX 申請書を `build_application_form.js` で生成）
- [ ] 通話日時を `tracking/channels_2026-06.md` に追加

**ステート**: `awaiting_phone_call`

---

## Issue 4: fest-116 / fest-117 PR rebase + 公開 + お礼返信

**優先度**: 🟢 低（しかし公開遅延中のため早めに）

### 4-A. fest-116 六郷のカマクラ

- [ ] PR #5 `feat/fest-116-rokugo-kamakura-photos` を main へ rebase
- [ ] 採用枚数（1〜3点）を確定、残りは `archive/fest-116/` に予備保管
- [ ] `data/photos.json` に `"photo_credit": "写真提供：あきた美郷づくり"` 追加
- [ ] `python3 build_data.py` 実行 → 同梱コミット
- [ ] マージ後、荒田様にお礼返信（`templates/thanks_reply.md` 使用）

### 4-B. fest-117 白石踊

- [ ] PR #2 `feat/fest-117-shiraishi-odori-enrichment` を main へ rebase
- [ ] `data/photos.json` に `"photo_credit": "写真提供：笠岡市教育委員会"` 追加
- [ ] `python3 build_data.py` 実行 → 同梱コミット
- [ ] マージ後、安藤様にお礼返信

---

## Issue 5: fest-118 対象スポット特定

**優先度**: ⚫ hold

**タスク**:
- [ ] fest-118 の対象（御陣乗太鼓？）を確定
- [ ] 仮なら spots.json から除外、確定なら申請ルート選定（輪島市 or 石川県観光連盟）

---

## 月次ルーティン

| 日 | タスク |
|---|---|
| 毎月1日 | `tracking/channels_<YYYY-MM>.md` を新規作成 |
| 毎月末 | 前月分のクローズ案件を INDEX.md から `archive/closed.md` へ移動 |
| 毎月末 | 進行中案件の状態を再確認、停滞中（30日以上動きなし）は催促 or hold |
