#!/usr/bin/env python3
"""
bulk_add.py

candidate_builder.py が出力したCSVのうち、'decision' 列に「採用」と
記入された行を spots.json または festivals.json に追加する。

使い方:
  python3 scripts/bulk_add.py --csv ./candidates/2026-05.csv

追加後は build_data.py を自動実行して data.js を再生成する。
"""

import argparse
import csv
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPOTS_JSON = ROOT / "spots.json"
FESTIVALS_JSON = ROOT / "festivals.json"
BUILD_SCRIPT = ROOT / "build_data.py"


def next_id(items, prefix):
    """既存IDの最大番号 +1 を返す"""
    nums = []
    for item in items:
        m = re.match(rf"{prefix}-(\d+)", item.get("id", ""))
        if m:
            nums.append(int(m.group(1)))
    return f"{prefix}-{(max(nums) + 1) if nums else 1:03d}"


def load_json(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {"items": data, "is_list": True}
    key = "spots" if "spots" in data else "festivals"
    return {"items": data[key], "is_list": False, "wrapper_key": key, "raw": data}


def save_json(path, container):
    if container["is_list"]:
        path.write_text(json.dumps(container["items"], ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        container["raw"][container["wrapper_key"]] = container["items"]
        path.write_text(json.dumps(container["raw"], ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--no-build", action="store_true", help="build_data.py を実行しない")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"ERROR: {csv_path} がない", file=sys.stderr); sys.exit(1)

    spots = load_json(SPOTS_JSON)
    fests = load_json(FESTIVALS_JSON)

    added_spots = added_fests = 0

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            decision = (row.get("decision") or "").strip()
            if decision != "採用":
                continue
            if (row.get("is_duplicate") or "").strip() == "重複":
                print(f"  SKIP 重複: {row.get('name')}"); continue

            cat = (row.get("category") or "spot").strip()
            target = fests if cat == "festival" else spots
            prefix = "fest" if cat == "festival" else "spot"

            new_id = next_id(target["items"], prefix)
            entry = {
                "id": new_id,
                "name": row.get("name") or "",
                "location": row.get("location") or "",
                "lat": float(row["wiki_lat"]) if row.get("wiki_lat") else None,
                "lng": float(row["wiki_lng"]) if row.get("wiki_lng") else None,
                "summary": row.get("caption_summary") or "",
                "wiki_url": row.get("wiki_url") or "",
                "source": "instagram-discovery",
                "review_pending": True,
            }
            target["items"].append(entry)
            if cat == "festival":
                added_fests += 1
            else:
                added_spots += 1
            print(f"  + {new_id}: {entry['name']}")

    if added_spots:
        save_json(SPOTS_JSON, spots)
    if added_fests:
        save_json(FESTIVALS_JSON, fests)

    print(f"\nspots {added_spots}件 / festivals {added_fests}件 を追加")

    if (added_spots or added_fests) and not args.no_build:
        print("→ build_data.py を実行...")
        subprocess.run(["python3", str(BUILD_SCRIPT)], cwd=ROOT, check=False)
        print("完了。git add -A && git commit && git push でデプロイしてください")


if __name__ == "__main__":
    main()
