# Mac Setup Check — Claude Code 移行作業

最終更新: 2026-05-27 (JST)

Mac 開発環境の点検記録。Claude Code への移行に伴い、Bizarre Japan / 異界巡礼
プロジェクト (`tydmthr/kinki-tokai-chinspot`) のローカル開発環境を整備した。

## 環境サマリ

| 項目 | バージョン | 備考 |
|---|---|---|
| macOS | 26.3.1 (build 25D771280a) | Apple Silicon (arm64) |
| Xcode Command Line Tools | 導入済み | `/Library/Developer/CommandLineTools` |
| Homebrew | 5.1.14 | `/opt/homebrew` |
| git | 2.50.1 (Apple Git-155) | `/usr/bin/git` |
| GitHub CLI (`gh`) | 2.92.0 | HTTPS 認証で `tydmthr` としてログイン |
| Node.js | v26.0.0 | Homebrew |
| npm | 11.12.1 | Node 同梱 |
| Claude Code (`claude`) | 2.1.152 | `npm install -g @anthropic-ai/claude-code` |
| Python | 3.13.7 | `/usr/local/bin/python3` |
| pip | 25.2 | — |

## git グローバル設定

```
user.name        = tydmthr
user.email       = motohiro.toyoda@gmail.com
init.defaultBranch = main
```

## GitHub 認証

- 方式: HTTPS + `gh auth login`（ブラウザ認証）
- 認証アカウント: `tydmthr`
- Git protocol: `https`

## 作業ディレクトリ

```
/Users/toyodamotohiro/Documents/Claude/Projects/Bizarre Japan/kinki-tokai-chinspot
```

## 次のステップ

- bulk_add.py の Mac 環境での動作確認
- 取り込みテスト（候補 → spots.json 反映）
- dev server 起動 (`python3 -m http.server` 等)
- Claude Code 評価タスク
