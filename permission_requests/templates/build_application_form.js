#!/usr/bin/env node
/**
 * 写真使用許可申請書 DOCX 自動生成スクリプト
 *
 * 使い方:
 *   1. application_form_template.json の例を参考に、案件固有のデータJSONを作成
 *      （例: data/fest-XXX.json）
 *   2. 以下のコマンドで実行:
 *      node build_application_form.js <input.json>
 *   3. JSON の output_filename に指定した DOCX が同ディレクトリに生成される
 *
 * 必須パッケージ: docx (npm install docx)
 *
 * 元設計: PerplexityComputer期に build_application_form.js / build_application_form_rokugo.js として
 *         案件ごとに複製運用していたものを、JSON入力で汎用化した。
 */

const fs = require('fs');
const path = require('path');
const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  AlignmentType,
  HeadingLevel,
  TabStopType,
  TabStopPosition,
  PageOrientation,
  convertInchesToTwip,
} = require('docx');

// ============================================================
// 入力 JSON のロード
// ============================================================
const inputPath = process.argv[2];
if (!inputPath) {
  console.error('Usage: node build_application_form.js <input.json>');
  process.exit(1);
}
const data = JSON.parse(fs.readFileSync(inputPath, 'utf8'));

// 必須フィールドのバリデーション
const required = [
  'target_id', 'date', 'addressee_org', 'addressee_dept_person',
  'honorific', 'subject_name', 'subject_location_designation',
  'photo_count', 'credit_text', 'output_filename'
];
for (const k of required) {
  if (!(k in data)) {
    console.error(`Missing required field: ${k}`);
    process.exit(1);
  }
}
data.usage_period = data.usage_period || '掲載開始日から、貴社からの掲載中止のご指示があるまで';
data.fee_text = data.fee_text || '無償でご許可いただけますよう、お願い申し上げます。';

// ============================================================
// 共通スタイル
// ============================================================
const FONT = 'Yu Mincho';
const FS_NORMAL = 22;   // 11pt
const FS_TITLE = 32;    // 16pt
const FS_SMALL = 20;    // 10pt

const p = (text, opts = {}) => new Paragraph({
  alignment: opts.align || AlignmentType.LEFT,
  spacing: { line: opts.line || 320, before: opts.before || 0, after: opts.after || 0 },
  children: [new TextRun({
    text,
    font: FONT,
    size: opts.size || FS_NORMAL,
    bold: opts.bold || false,
  })],
});

const blank = (n = 1) => Array.from({ length: n }, () => p(''));

// ============================================================
// 本文構築
// ============================================================
const children = [];

// 日付（右寄せ）
children.push(new Paragraph({
  alignment: AlignmentType.RIGHT,
  spacing: { after: 200 },
  children: [new TextRun({ text: data.date, font: FONT, size: FS_NORMAL })],
}));

// 宛先（左寄せ）
children.push(p(data.addressee_org));
children.push(p(`${data.addressee_dept_person}　様`, { after: 200 }));

// 申請者（右寄せ複数行）
const applicantLines = [
  '〒519-0105',
  '三重県亀山市',
  '豊田 元洋（とよだ もとひろ）',
  'Email: motohiro.toyoda@gmail.com',
  'Web:   https://bizarrejapan.com/',
];
for (const line of applicantLines) {
  children.push(new Paragraph({
    alignment: AlignmentType.RIGHT,
    spacing: { line: 280 },
    children: [new TextRun({ text: line, font: FONT, size: FS_NORMAL })],
  }));
}
children.push(...blank(2));

// タイトル
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 200, after: 400 },
  children: [new TextRun({ text: '写真使用許可申請書', font: FONT, size: FS_TITLE, bold: true })],
}));

// 前文
const intro = [
  '拝啓 時下ますますご清祥のこととお慶び申し上げます。',
  '平素より地域の文化財・観光資源の保存・活用にご尽力されておりますこと、心より敬意を表します。',
  '',
  `このたび、私が運営しております文化記録ウェブサイト「Bizarre Japan / 異界巡礼」（https://bizarrejapan.com/ ）におきまして、貴${data.honorific}が所有または管理されております「${data.subject_name}」に関する写真の使用許可を賜りたく、下記のとおり申請いたします。`,
  '',
  'ご審査のうえ、ご許可賜りますよう何卒よろしくお願い申し上げます。',
];
for (const line of intro) children.push(p(line));

// 敬具（右寄せ）
children.push(new Paragraph({
  alignment: AlignmentType.RIGHT,
  spacing: { before: 200, after: 200 },
  children: [new TextRun({ text: '敬具', font: FONT, size: FS_NORMAL })],
}));

// 記
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 200, after: 200 },
  children: [new TextRun({ text: '記', font: FONT, size: FS_NORMAL, bold: true })],
}));

// 本文項目
const items = [
  ['1. 使用希望写真',
    `   対象        : ${data.subject_name}（${data.subject_location_designation}）`,
    `   写真点数    : ${data.photo_count} 点（別途データにて受領予定／受領済）`,
  ],
  ['2. 使用目的',
    `   Bizarre Japan / 異界巡礼 サイト内「${data.subject_name}」紹介ページにおける、`,
    `   解説文と並んでの参考画像としての掲載。`,
    `   個人運営の文化記録プロジェクトであり、非営利・広告収入なし。`,
  ],
  ['3. 使用範囲',
    `   ・上記サイト内での表示用途に限定`,
    `   ・第三者への再配布・ダウンロード提供は行わない`,
    `   ・改変（明るさ・コントラスト・トリミング以外の加工）は行わない`,
  ],
  ['4. クレジット表記',
    `   画像下部に「${data.credit_text}」を明記する。`,
  ],
  ['5. 使用期間',
    `   ${data.usage_period}`,
  ],
  ['6. 使用料',
    `   ${data.fee_text}`,
  ],
  ['7. 遵守事項',
    `   ・貴${data.honorific}のご指示・ご意向を最優先で尊重する`,
    `   ・地域・関係者の方々へのご配慮を欠かさない`,
    `   ・問題が発覚した場合、24時間以内に該当写真を一時非公開とし、ご相談する`,
  ],
  ['8. 連絡先',
    `   氏名      : 豊田 元洋（とよだ もとひろ）`,
    `   所在      : 〒519-0105 三重県亀山市`,
    `   Email     : motohiro.toyoda@gmail.com / bizarrejapan.jp@gmail.com`,
    `   サイト    : https://bizarrejapan.com/`,
    `   Instagram : @bizarre_japan`,
    `   所属      : 有限会社豊田衛生 取締役 / 亀山商工会議所青年部（YEG）2026年度 会長`,
    `              （本申請は個人プロジェクトとしての申請であり、所属団体の事業ではありません）`,
  ],
];

for (const block of items) {
  children.push(p(block[0], { bold: true, before: 200, after: 80 }));
  for (let i = 1; i < block.length; i++) {
    children.push(p(block[i]));
  }
}

// 以上（右寄せ）
children.push(new Paragraph({
  alignment: AlignmentType.RIGHT,
  spacing: { before: 400 },
  children: [new TextRun({ text: '以上', font: FONT, size: FS_NORMAL })],
}));

// ============================================================
// ドキュメント生成
// ============================================================
const doc = new Document({
  sections: [{
    properties: {
      page: {
        margin: {
          top: convertInchesToTwip(1.0),
          right: convertInchesToTwip(1.0),
          bottom: convertInchesToTwip(1.0),
          left: convertInchesToTwip(1.0),
        },
      },
    },
    children,
  }],
});

// ============================================================
// 出力
// ============================================================
const outputPath = path.resolve(path.dirname(inputPath), data.output_filename);
Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(outputPath, buf);
  console.log(`Generated: ${outputPath}`);
  console.log(`Target ID: ${data.target_id}`);
  console.log(`Addressee: ${data.addressee_org} ${data.addressee_dept_person}`);
});
