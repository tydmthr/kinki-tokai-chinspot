#!/usr/bin/env python3
"""
fetch_instagram_feed.py

bizarre_japan の最新3投稿を Instagram Graph API で取得し、
data/instagram-feed.json として保存する。

GitHub Actions から日次実行される想定。
環境変数:
  - IG_LONG_TOKEN: 長期アクセストークン
  - IG_BUSINESS_ID: Instagram Business Account ID
"""

import json
import os
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen, Request

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "instagram-feed.json"

GRAPH_VERSION = "v19.0"
LIMIT = 6  # 最新6投稿


def fetch_media(business_id, token):
    """Page-scoped IG ビジネスアカウントの最新メディア取得"""
    fields = ",".join([
        "id", "caption", "media_type", "media_url",
        "permalink", "thumbnail_url", "timestamp",
    ])
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{business_id}/media?" + urlencode({
        "fields": fields,
        "limit": LIMIT,
        "access_token": token,
    })
    req = Request(url, headers={"User-Agent": "bizarrejapan-feed/1.0"})
    with urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    if "error" in data:
        raise RuntimeError(f"IG API error: {data['error']}")
    return data.get("data", [])


def normalize(items):
    """フロント表示用に必要なフィールドだけに整形"""
    out = []
    for it in items:
        media_type = it.get("media_type", "IMAGE")
        # 動画ならサムネイル、画像なら本体
        image = it.get("thumbnail_url") if media_type == "VIDEO" else it.get("media_url")
        out.append({
            "id": it.get("id"),
            "caption": (it.get("caption") or "")[:300],
            "media_type": media_type,
            "image": image,
            "permalink": it.get("permalink"),
            "timestamp": it.get("timestamp"),
        })
    return out


def main():
    token = os.environ.get("IG_LONG_TOKEN")
    business_id = os.environ.get("IG_BUSINESS_ID")
    if not token or not business_id:
        print("ERROR: IG_LONG_TOKEN / IG_BUSINESS_ID 環境変数が必要", file=sys.stderr)
        sys.exit(1)

    items = fetch_media(business_id, token)
    feed = {
        "account": "bizarre_japan",
        "updated_at": items[0]["timestamp"] if items else None,
        "posts": normalize(items),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(feed, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(items)} posts to {OUT}")


if __name__ == "__main__":
    main()
