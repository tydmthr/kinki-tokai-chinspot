# templates/ — 各種テンプレート

## ファイル一覧

| ファイル | 用途 |
|---|---|
| `jinja_email.md` | 神社・寺院向け初回依頼メール |
| `municipal_email.md` | 自治体・教育委員会向け初回依頼メール |
| `tourism_assoc_email.md` | 観光協会・観光連盟向け初回依頼メール |
| `negotiation_reply.md` | 懸念表明への返信（差替・事前確認・見送りの3案提示） |
| `thanks_reply.md` | 許諾受領後のお礼返信 |
| `apology_misaddress.md` | 誤宛先送信お詫び |
| `application_form.md` | 写真使用許可申請書（Markdown版・閲覧用） |
| `application_form_template.json` | DOCX生成用の穴埋め定義（JSON Schema） |
| `build_application_form.js` | 申請書DOCX 自動生成スクリプト |

## DOCX 生成手順

### 前提

Node.js + `docx` npm パッケージ。

```bash
mkdir -p /tmp/app_form && cd /tmp/app_form
npm init -y
npm install docx
```

### 案件データJSON作成

`application_form_template.json` のスキーマを参照し、案件固有のJSONを作成：

```bash
cat > fest-XXX.json <<'JSON'
{
  "target_id": "fest-XXX",
  "date": "令和8年X月X日",
  "addressee_org": "...",
  "addressee_dept_person": "...",
  "honorific": "社",
  "subject_name": "...",
  "subject_location_designation": "...",
  "photo_count": 7,
  "credit_text": "...",
  "usage_period": "掲載開始日から、貴社からの掲載中止のご指示があるまで",
  "fee_text": "無償でご許可いただけますよう、お願い申し上げます。",
  "output_filename": "写真使用許可申請書_XXX_豊田元洋.docx"
}
JSON
```

### 実行

```bash
cp <repo>/permission_requests/templates/build_application_form.js .
node build_application_form.js fest-XXX.json
```

生成された DOCX を Spark/Gmail から添付して送付。

### プレビュー確認

```bash
soffice --headless --convert-to pdf <output.docx>
pdftoppm -r 110 <output.pdf> preview -png
```

ページ1だけ確認すれば、宛先・対象名・クレジット文言のミスを早期発見可能。

## カスタマイズ時の注意

| 項目 | 注意点 |
|---|---|
| 宛先「貴○」 | `honorific` を必ず指定（社/会/館/委員会/協会/宮/寺）。本文中3箇所に挿入される |
| 日付 | 令和表記（「令和8年6月2日」等）。西暦不可 |
| 電話番号 | 申請書には記載しない方針（ユーザー指示） |
| GitHub URL | 署名・本文に記載しない方針 |
