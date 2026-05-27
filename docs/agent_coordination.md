# Bizarre Japan エージェント連絡板

**最終更新**: 2026-05-27 (JST)
**目的**: 複数のAIエージェント・タスクが同時並行で進む際の衝突回避と情報共有

---

## 0. 運用ルール

### 作業着手時
1. **本ファイルの「進行中タスク」を必ず確認** → ファイル衝突がないかチェック
2. 自分のタスクを「進行中タスク」に追加（担当・着手日・対象ファイル・状態）
3. 同じファイルを触る予定の先行タスクがある場合は、完了を待つかユーザーに相談

### 作業完了時
1. 「進行中タスク」から自分の行を削除
2. 「完了ログ」に記録（日付・タスク・担当・PR番号・サマリ）

### コミット時
- PR description には必ず `docs/agent_coordination.md` 更新の旨を明記
- 同じファイルへの同時編集は禁止（衝突しないようブランチ名で識別）

---

## 1. プロジェクト基本情報

| 項目 | 内容 |
|---|---|
| サイト | https://bizarrejapan.com/ |
| リポジトリ | https://github.com/tydmthr/kinki-tokai-chinspot |
| 運営者 | motohiro.toyoda@gmail.com (三重県亀山市) |
| Instagram | @bizarre_japan |
| 連絡先 | bizarrejapan.jp@gmail.com |
| デプロイ | GitHub Pages（main push 後自動） |
| 自動化 | Instagram フィード 06:00 JST にサイトフッター反映 |

---

## 2. データスキーマ（変更時要相談）

### spots.json (必須17フィールド)
```
id, name, name_kana, category, prefecture, city, address,
lat, lng, status, fee, hours, official_url, reference_urls (list),
summary, highlights (list), from_kameyama
```

### spots_en.json 追加フィールド
```
name_en, prefecture_en, city_en, summary_en, highlights_en
```

### カテゴリ規約（4種固定）
| カテゴリ | 用途 |
|---|---|
| `folk` | 民俗信仰、奇祭、神事、土俗の祭礼 |
| `bkyu` | B級スポット、巨大オブジェ、異形看板、民間芸術 |
| `horror` | 廃墟、心霊系（掲載基準厳格） |
| `mystery` | 聖地、磐座、神秘的地形 |

### 座標規則
- WGS84 / 小数点6桁
- 重複チェック: name + lat/lng で照合

---

## 3. エージェント一覧と担当領域

| エージェント | 担当領域 | 主な対象ファイル |
|---|---|---|
| **Perplexity Computer** | 三重・近畿バッチ追加、リポジトリ作業全般 | spots.json, spots_en.json, index.html |
| **全国常設施設発掘タスク** | 全国の常設珍スポット候補発掘 | candidates/, spots.json |
| **全国奇祭発掘タスク** | 全国の奇祭候補発掘 | festivals.json, festivals_en.json |
| **サイト改修タスク** | HTML/CSS/JS 改修・UI 改善 | index.html, app.js, style.css |
| **写真掲載許可申請タスク** | 写真権利交渉・許可済画像の管理 | photos.json, instagram_screenshots/ |

---

## 4. 進行中タスク

| ID | タスク | 担当 | 着手日 | 対象ファイル | 状態 |
|---|---|---|---|---|---|
| - | (現在進行中タスクなし) | - | - | - | - |

---

## 5. 完了ログ

| 日付 | タスク | 担当 | PR | サマリ |
|---|---|---|---|---|
| 2026-05-24 | 三重バッチ① 10件追加 (spot-133〜142) | Perplexity Computer | [#3](https://github.com/tydmthr/kinki-tokai-chinspot/pull/3) | folk:9 / bkyu:1。spots.json 132→142、spots_en.json 132→142 |
| 2026-05-24 | 連絡板新設 + 件数表記 132→142 修正 | Perplexity Computer | [#4](https://github.com/tydmthr/kinki-tokai-chinspot/pull/4) | docs/agent_coordination.md 新規。index.html 11箇所、en/index.html 5箇所更新 |
| 2026-05-27 | 全国常設施設バッチ① 5件追加 (spot-143〜147) | 全国常設施設発掘タスク | 直push (83e18f7) | mystery:1 / bkyu:3 / folk:1。十宝山大乗院鬼のミイラ・おおざわ石仏の森・珍宝館・津軽萬人観世音・喜宝院蒐集館。spots.json 142→147。**spots_en.json未追加**（要対応）|
| 2026-05-27 | 三重・近畿バッチ② 10件追加 (spot-148〜157) | Perplexity Computer | (このPR) | folk:5 / bkyu:3 / mystery:1 / horror:1。神前浦飛鳥神社・安乗神社・二木島祭・古和浦祇園祭・てんてこ祭（愛知）・寶珠山大観音寺・ルーブル彫刻美術館・日本列島公園（愛知）・中ノ瀬磨崖仏・紫峰閣。spots.json 147→157、spots_en.json 142→152 |

---

## 6. 共通選定基準（Perplexity Computer 6軸スコアリング）

三重バッチ①で確立した選定基準。**他エージェントも参考にしてください**。

| 軸 | 0点 | 3点 |
|---|---|---|
| 民俗・信仰の文脈深さ | 単なるオブジェ | 文化財指定+独自伝承 |
| 異形性と機能の結合 | 装飾のみ | 儀礼の核 |
| 地域独自性 | 他県類例多 | 県固有 |
| 静止画1枚の構図強度 | 弱 | 突き刺さる |
| 観光ポスター化されてない | 完全観光化 | 地元のみ |
| 季節依存・撮影容易性 | 1日限定 | 通年訪問可 |

### ボツパターン（学習結果）
- 単発巨大オブジェ
- ご当地巨大食材像
- 観光化済み祭（既に有名ポスター系）
- 神社単体（建築/造形に異形性なし）
- 季節限定の見せ物
- 他県類例ある自販機異界
- 看板単体
- 王道観光・資料館・産業遺産寄り

### 採用優先パターン
- B級
- 奇祭・民俗信仰
- 異形看板
- 巨大オブジェ
- 視覚的に強い路傍スポット

---

## 7. 掲載判断ポリシー（要約）

詳細は `bizarre_japan_listing_policy_2026-05-11.md`（Space）参照。

- **private/危険地・心霊スポット系** → 原則「却下」推奨
- **私有地** → 確認できなければ却下
- **夜間立入危険地** → 却下
- 掲載判断は **読者の安全最優先**
- 不確かな情報は `editorial_status: hold` で保留可（将来スキーマ拡張）

---

## 8. サイト表示の動的件数ロジック（参考）

- カテゴリチップ件数・hero stats・list tab件数: **app.js が SPOTS.length から自動計算**
- meta description / OG / 構造化データ / hero-lede の数字: **手動更新が必要**（index.html, en/index.html）
- spots.json 件数が大きく変わった場合は本連絡板で告知し、表記修正も同PRで実施

---

## 9. Git ブランチ命名規約（推奨）

| ブランチプレフィックス | 用途 |
|---|---|
| `mie-batch-N-...` | 三重バッチ N 番目 |
| `national-spots-batch-N-...` | 全国常設施設 |
| `festivals-batch-N-...` | 奇祭追加 |
| `site-renovation-...` | サイト改修 |
| `photo-permission-...` | 写真許可関連 |
| `docs-...` | 本連絡板など文書更新 |

---

## 10. 次バッチ候補メモ（Perplexity Computer 引き継ぎ）

三重・次のA-tier候補（13-14pts）。第二バッチ着手時に参照：

- #28 二木島祭・船子漕ぎ (13)
- #22 古和浦祇園祭 船形神輿 (13)
- #32 関船祭り（引本神社）船型山車 (13)
- #25 神前浦飛鳥神社 つがい龍 (14)
- #35 中之瀬阿弥陀三尊磨崖仏 (14)
- #27 安乗神社 しめ切り神事 (14)
- #24 正泉寺 鐘の9穴 (14)
- #36 便石山 象の背（自然奇景）(13) — bkyu系のバランス調整候補
- #48 彌都加伎神社 てるてる坊主大量展示 (12) — bkyu系候補
