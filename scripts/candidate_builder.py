#!/usr/bin/env python3
"""
candidate_builder.py

bizarrejapan.com の珍スポット候補を Instagram スクショ群から半自動で起こす。

入力: 候補画像 (JPG/PNG) のディレクトリ
処理:
  1. 画像を Claude API（vision）で読み込み、施設名・地名・コメントを抽出
  2. Wikipedia 日本語版 API で裏取り
  3. spots.json / festivals.json と照合して重複チェック
  4. 候補CSV出力（採用/却下マークを後から付ける）

使い方:
  python3 scripts/candidate_builder.py \
    --input ./instagram_screenshots/2026-05/ \
    --output ./candidates/2026-05.csv
"""

import argparse
import base64
import csv
import json
import os
import sys
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen, Request

ROOT = Path(__file__).resolve().parent.parent
SPOTS_JSON = ROOT / "spots.json"
FESTIVALS_JSON = ROOT / "festivals.json"

# --- 既存データロード -------------------------------------------------

def load_existing_names():
    """既存スポット・祭の名称セットを返す（重複チェック用）"""
    names = set()
    for path in (SPOTS_JSON, FESTIVALS_JSON):
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        items = data if isinstance(data, list) else data.get("spots", data.get("festivals", []))
        for item in items:
            name = item.get("name") or item.get("name_jp")
            if name:
                names.add(name.strip())
    return names

# --- Wikipedia 裏取り -------------------------------------------------

def wikipedia_lookup(name):
    """日本語Wikipediaで施設名検索 → 概要・座標・URL取得"""
    try:
        url = f"https://ja.wikipedia.org/api/rest_v1/page/summary/{quote(name)}"
        req = Request(url, headers={"User-Agent": "bizarrejapan-bot/1.0"})
        with urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
        return {
            "title": data.get("title"),
            "extract": (data.get("extract") or "")[:300],
            "url": data.get("content_urls", {}).get("desktop", {}).get("page"),
            "lat": data.get("coordinates", {}).get("lat"),
            "lng": data.get("coordinates", {}).get("lon"),
        }
    except Exception as e:
        return {"error": str(e)}

# --- Claude vision で画像から情報抽出 -------------------------------

CLAUDE_PROMPT = """
この画像は Instagram の投稿スクリーンショットです。
日本国内の「珍スポット」「奇祭」「B級観光地」「廃神社」「秘宝館」などの候補として、
以下の情報を JSON 形式で抽出してください。

抽出項目:
- name: 施設名・場所名（推定可）
- location: 都道府県・市区町村
- category: spot / festival / unclear のいずれか
- caption_summary: キャプションの要約 (50字以内)
- weirdness_score: 1〜5（珍スポットらしさ）
- confidence: low / medium / high（情報抽出の確度）

不明な項目は null で埋めてください。
JSON のみを返答し、他の文章は含めないでください。
"""

def extract_from_image(image_path, claude_api_key):
    """Claude Vision API で画像から情報を抽出"""
    img_bytes = Path(image_path).read_bytes()
    b64 = base64.b64encode(img_bytes).decode()
    media_type = "image/jpeg" if image_path.suffix.lower() in (".jpg", ".jpeg") else "image/png"

    body = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 500,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": b64}},
                {"type": "text", "text": CLAUDE_PROMPT}
            ]
        }]
    }
    req = Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(body).encode(),
        headers={
            "x-api-key": claude_api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
    )
    try:
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        text = data["content"][0]["text"].strip()
        # コードブロック除去
        if text.startswith("```"):
            text = "\n".join(text.split("\n")[1:-1])
        return json.loads(text)
    except Exception as e:
        return {"error": str(e), "name": None}

# --- メイン処理 -------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="スクショ画像ディレクトリ")
    parser.add_argument("--output", required=True, help="出力CSVパス")
    parser.add_argument("--claude-key", default=os.environ.get("ANTHROPIC_API_KEY"))
    args = parser.parse_args()

    if not args.claude_key:
        print("ERROR: --claude-key または ANTHROPIC_API_KEY 環境変数が必要", file=sys.stderr)
        sys.exit(1)

    images = sorted([p for p in Path(args.input).iterdir()
                     if p.suffix.lower() in (".jpg", ".jpeg", ".png")])
    if not images:
        print(f"ERROR: {args.input} に画像がない", file=sys.stderr)
        sys.exit(1)

    existing = load_existing_names()
    print(f"既存エントリ {len(existing)} 件、画像 {len(images)} 枚を処理")

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "image", "name", "location", "category",
            "weirdness", "confidence",
            "is_duplicate", "wiki_title", "wiki_url", "wiki_lat", "wiki_lng",
            "caption_summary", "decision"
        ])

        for i, img in enumerate(images, 1):
            print(f"[{i}/{len(images)}] {img.name}")
            extracted = extract_from_image(img, args.claude_key)
            name = extracted.get("name") or ""
            wiki = wikipedia_lookup(name) if name else {}
            is_dup = name.strip() in existing if name else False

            writer.writerow([
                img.name,
                name,
                extracted.get("location") or "",
                extracted.get("category") or "",
                extracted.get("weirdness_score") or "",
                extracted.get("confidence") or "",
                "重複" if is_dup else "",
                wiki.get("title") or "",
                wiki.get("url") or "",
                wiki.get("lat") or "",
                wiki.get("lng") or "",
                extracted.get("caption_summary") or "",
                ""  # decision: 採用/却下 を後から記入
            ])

    print(f"完了: {args.output}")
    print("→ CSVを開き、'decision'列に '採用' または '却下' を記入してください")
    print("→ 採用分は scripts/bulk_add.py で spots.json に取り込みます")


if __name__ == "__main__":
    main()
