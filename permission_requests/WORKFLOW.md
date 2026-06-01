# WORKFLOW.md — 写真使用許諾 運用手順書（Claude Code 向け）

このドキュメントは、`permission_requests/` ディレクトリの運用を Claude Code が単独で回せるようにするための **実行手順書** です。
ルール本体は `README.md`、ダッシュボードは `INDEX.md` を参照。

## 全体フロー

```
[新規発掘] → [調査] → [初回依頼] → [返信待ち] → [回答受領] → [写真受領/許諾確定] → [サイト反映]
                ↑                       ↓
                └─── [交渉] ←── [懸念表明/差替要求]
```

各フェーズの詳細は §1 〜 §7 を参照。

---

## §1. 新規案件の起票

### 1.1 トリガー

以下のいずれかが発生したら新規案件を起票：

- ユーザーが「spot-XXX / fest-XXX の写真許諾を取りたい」と指示
- `spots.json` / `festivals.json` で `editorial_status` が `needs_photo_permission` になっているエントリを発見
- 既存スポットで現在使用中の写真の出典が不明確で、再取得が必要なケース

### 1.2 ステップ

1. **対象 ID を確定**：`spot-XXX` または `fest-XXX`
2. **対象の現状を確認**：
   - `spots.json` / `festivals.json` の該当エントリ
   - `photos.json` の該当エントリ（`primary` / `credit` / `license`）
   - サイト上での表示 (`https://bizarrejapan.com/?id=<ID>` 等)
3. **窓口候補を一次資料で裏取り**：
   - 自治体公式サイト（教育委員会・文化課・観光課）
   - 神社庁登録情報
   - 観光協会・観光連盟
   - 文化財データベース（国指定: `kunishitei.bunka.go.jp`）
4. **`INDEX.md` の「進行中の申請一覧」に追加**（状態 = `draft_in_progress`）

### 1.3 注意点

- **同名異所**に注意：例「淡島神社」は福岡・和歌山・各地に存在
- 個人ブログ・SNS だけが情報源の場合は `hold` 扱い
- メールアドレス公開がない団体は `awaiting_phone_call` でスクリプト準備

---

## §2. 初回依頼メール作成・送信

### 2.1 テンプレート選択

| 宛先タイプ | テンプレート |
|---|---|
| 神社・寺院 | `templates/jinja_email.md` |
| 自治体・教育委員会・文化課 | `templates/municipal_email.md` |
| 観光協会・観光連盟 | `templates/tourism_assoc_email.md` |

### 2.2 ステップ

1. テンプレートをコピーして `{...}` プレースホルダを埋める
2. ユーザーに**全文を Markdown で提示**して承認を取る
3. 承認後、Gmail の下書きを作成（Claude Code から Gmail 操作する場合は `gh` ではないので、ローカル Gmail 操作ツールを使うか、ユーザーに「Gmail 下書きを作成してください」と指示する）
4. ユーザーがメーラー（Spark など）から送信
5. 送信完了をユーザーから報告してもらい、`sent/<id>_<recipient>_<YYYY-MM-DD>.md` に本文保存
6. `tracking/channels_YYYY-MM.md` に1行追加
7. `INDEX.md` のステータスを `sent` に更新

### 2.3 送信本文の保存形式（sent/）

```markdown
# <id> 初回依頼メール

- **送信日時**: 2026-XX-XX HH:MM JST
- **送信元**: motohiro.toyoda@gmail.com
- **宛先**: <email>
- **CC**: <email> (任意)
- **件名**: 【写真使用許諾のお願い】...
- **テンプレ起源**: templates/<name>.md
- **期待返信期限**: 2026-XX-XX
- **添付**: なし / 写真使用許可申請書_<対象名>.docx

---

[ここに送信本文をそのまま貼り付け]
```

---

## §3. 返信受領

### 3.1 ステップ

1. ユーザーから返信内容（スクショまたはテキスト）を受領
2. `received/<id>_<sender>_<YYYY-MM-DD>.md` に抜粋を保存
3. 返信内容の論点を整理：
   - 許諾の可否
   - 条件（クレジット文言・使用範囲・期間）
   - 懸念点（イメージ齟齬・煽情性指摘等）
   - 追加要求（事前監修・確認 URL 等）
4. **INDEX.md のステータスを更新**：
   - 完全許諾 → `permitted`
   - 条件付許諾 → `conditional`
   - 懸念表明 → `negotiation`
   - 拒否 → `denied`
   - 追加情報要求 → `replied_pending_action`
5. 次アクションをユーザーに提案（§4 または §5 へ）

### 3.2 受信抜粋の保存形式（received/）

```markdown
# <id> 返信受領

- **受信日時**: 2026-XX-XX HH:MM JST
- **送信元**: <name>（<email>）
- **件名**: Re: ...
- **判定**: permitted / conditional / negotiation / denied / replied_pending_action

## 要点

[3〜5行で要点抜粋]

## 条件・要求事項

[クレジット文言・監修要求・使用範囲等を箇条書き]

## 抜粋本文

[原文の主要部分。署名・装飾文字は省略可]
```

---

## §4. お礼返信（許諾受領後）

### 4.1 使用テンプレート

`templates/thanks_reply.md`

### 4.2 ステップ

1. テンプレをベースに、相手の回答内容に応じてカスタマイズ
2. 次の3点を必ず含める：
   - 明確な回答への感謝
   - 指定クレジット表記を遵守する旨の明示
   - 民俗文化・地域文化への配慮意識の再確認
3. ユーザー承認 → Gmail 下書き → 送信
4. `sent/<id>_<recipient>_<YYYY-MM-DD>_thanks.md` に保存
5. `INDEX.md` を `permitted` または `conditional` で確定

### 4.3 重要

公的団体（自治体・観光連盟等）には**必ずお礼を返す**。社会人マナーとして当然であり、今後の関係性にも影響する。

---

## §5. 交渉返信（懸念表明への対応）

### 5.1 使用テンプレート

`templates/negotiation_reply.md`

### 5.2 ステップ

1. 相手の懸念を**真摯に受け止める**ことから始める（弁明・反論ではなく傾聴）
2. Bizarre Japan の編集方針を改めて説明：
   - 「文化的記録」が目的
   - 心霊・オカルト的煽りを明確に排している
   - 民俗・信仰・歴史的経緯の文脈で扱う
3. ユーザー（豊田元洋氏）の YEG 会長としての立場・地域振興への志を伝える
4. **改善案を3点提示**：
   - 【1】写真差替・トーン調整（先方からの写真提供を歓迎）
   - 【2】掲載前の事前確認（最終ドラフトを送付して確認をもらう）
   - 【3】掲載見送りのご判断もご遠慮なく（現掲載分も削除）
5. ユーザー承認 → 送信

### 5.3 重要

「拒否」ではなく「躊躇」のサインを見逃さない。改善案次第で合意可能なケースが多い。

---

## §6. 写真受領後の取り込み

### 6.1 写真ファイルが添付されてきたら

1. workspace に保存
2. PIL で最適化：
   ```python
   from PIL import Image, ImageOps
   im = Image.open(src)
   im = ImageOps.exif_transpose(im)
   im.thumbnail((1600, 1600), Image.LANCZOS)
   im.save(dst, "JPEG", quality=82, optimize=True, progressive=True)
   ```
3. `data/photos/<ID>/<ID>-NN-<description>.jpg` 形式で配置
4. `data/photos/<ID>/ATTRIBUTION.md` を作成（提供元・許可日・クレジット・ファイル一覧）

### 6.2 photos.json 更新

```json
"<ID>": {
  "name": "...",
  "primary": "data/photos/<ID>/<ID>-01-<key>.jpg",
  "credit": "<指定クレジット文言>",
  "license": "<許諾条件の要約>",
  "alt_photos": [ ... ]
}
```

### 6.3 必須コミット手順

```bash
# 1. photos.json 編集後は必ず build_data.py 実行
python3 build_data.py

# 2. data.js + index.html + en/index.html もまとめて add
git add data/photos/<ID>/ photos.json data.js index.html en/index.html

# 3. コミット
git commit -m "feat(<ID>): <対象名> 写真N点配置・許諾情報反映"

# 4. PR 起票（main 直 push は推奨しない）
git push -u origin feat/<ID>-photos
gh pr create --base main --head feat/<ID>-photos --title "..." --body "..."
```

`data.js` を同梱しないと CI (`.github/workflows/data-sync-check.yml`) で **fail** する。

---

## §7. tracking 更新

### 7.1 月次ファイル

`tracking/channels_YYYY-MM.md` を月単位で作成。1案件1日1行で履歴を残す。

### 7.2 INDEX.md 更新

主要な状態変化のたびに `INDEX.md` を更新。最終更新日時を冒頭に明記。

---

## §8. ユーザーとのコミュニケーション

### 8.1 報告フォーマット

完了時の報告は次の構成で：

```markdown
## ✅ <案件名> <フェーズ名> 完了

### サマリー
| 項目 | 内容 |
|---|---|
| 対象 | spot-XXX <名前> |
| 状態 | sent → permitted |
| ...

### 次のアクション選択肢
A. ...
B. ...
C. スキップ
```

### 8.2 承認の取り方

- **メール送信**：全文 Markdown ドラフトを提示 → 「OK」または修正指示を待つ
- **コード変更**：差分概要を提示 → 「OK」または修正指示を待つ
- `confirm_action` ツールは日本語表示の不具合があるため使用しない

### 8.3 ユーザー基本情報

| 項目 | 内容 |
|---|---|
| 氏名 | 豊田 元洋（とよだ もとひろ） |
| 郵便番号 | 〒519-0105 三重県亀山市 |
| メール | motohiro.toyoda@gmail.com / bizarrejapan.jp@gmail.com |
| 肩書き | 有限会社豊田衛生 取締役 / 亀山商工会議所青年部（YEG）2026年度 会長 |
| メーラー | Spark（Gmail と連携） |
| 電話番号 | 申請書には載せない（メールのみ） |

---

## §9. 既存案件の引継ぎ

`handoff/MIGRATION_NOTES.md` に Perplexity Computer 期の経緯を全件記録。
新規対応前に必ず一読すること。

Todoist 起票用のチケット雛形は `handoff/todoist_issues.md` を参照。
