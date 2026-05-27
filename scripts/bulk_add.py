#!/usr/bin/env python3
"""
bulk_add.py

candidate_builder.py または手作業で作成したCSVのうち、'decision' 列に
「採用」と記入された行を spots.json または festivals.json に追加する。

スキーマ: docs/schema.md (実装スキーマ準拠) に従う。

使い方:
  python3 scripts/bulk_add.py --csv ./candidates/2026-05.csv
  python3 scripts/bulk_add.py --csv ./candidates/_sample.csv --no-build

CSV 必須列 (spot/festival 共通):
  decision, is_duplicate, category, name, name_kana, lat, lng,
  prefecture, city, address, summary

spot 専用必須列:
  status, fee, hours, from_kameyama, highlights

CSV 任意列:
  name_en, category_slug (folk/bkyu/mystery/horror; 未指定なら category から推定),
  official_url, reference_urls, region, category_label, editorial_status,
  visit_priority, safety_level, safety_note, source_quality, last_verified,
  wiki_url (reference_urls に統合)

highlights は ';' 区切りで複数記述 (例: "見どころ1;見どころ2;見どころ3")
reference_urls も ';' 区切り

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

# category (人間向け) → slug マッピング (docs/schema.md 1.3)
CATEGORY_TO_SLUG = {
    "神社仏閣": "folk",
    "民俗信仰": "folk",
    "B級スポット": "bkyu",
    "路傍": "bkyu",
    "その他": "bkyu",
    "産業遺産": "mystery",
    "廃墟": "mystery",
    "自然奇景": "horror",
    "心霊": "horror",
    # 既に slug で書かれている場合の identity
    "folk": "folk", "bkyu": "bkyu", "mystery": "mystery", "horror": "horror",
    # festival はそのまま (spots とは別系統)
    "festival": "festival",
}

VALID_SLUGS = {"folk", "bkyu", "mystery", "horror"}


def next_id(items, prefix):
    """既存IDの最大番号 +1 を返す。zero-padded 3桁"""
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
        path.write_text(
            json.dumps(container["items"], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    else:
        container["raw"][container["wrapper_key"]] = container["items"]
        path.write_text(
            json.dumps(container["raw"], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


def split_semi(value):
    """セミコロン区切り文字列を配列に。空ならNone"""
    if not value:
        return None
    parts = [p.strip() for p in value.split(";") if p.strip()]
    return parts or None


def resolve_slug(row):
    """category 列から 4 slug を解決。festival は別扱い"""
    explicit = (row.get("category_slug") or "").strip()
    if explicit in VALID_SLUGS:
        return explicit
    cat = (row.get("category") or "").strip()
    if cat == "festival":
        return "festival"
    slug = CATEGORY_TO_SLUG.get(cat)
    if slug in VALID_SLUGS or slug == "festival":
        return slug
    return None  # 解決失敗


def build_spot_entry(row, new_id):
    """spot 用エントリ生成"""
    slug = resolve_slug(row)
    highlights = split_semi(row.get("highlights")) or []
    ref_urls = split_semi(row.get("reference_urls")) or []
    # wiki_url が単独で来た場合は reference_urls に統合
    wiki_url = (row.get("wiki_url") or "").strip()
    if wiki_url and wiki_url not in ref_urls:
        ref_urls.append(wiki_url)

    entry = {
        "id": new_id,
        "name": (row.get("name") or "").strip(),
        "name_kana": (row.get("name_kana") or "").strip(),
        "category": slug,
        "prefecture": (row.get("prefecture") or "").strip(),
        "city": (row.get("city") or "").strip(),
        "address": (row.get("address") or "").strip(),
        "lat": float(row["lat"]) if row.get("lat") else None,
        "lng": float(row["lng"]) if row.get("lng") else None,
        "status": (row.get("status") or "現存").strip(),
        "fee": (row.get("fee") or "").strip(),
        "hours": (row.get("hours") or "").strip(),
        "summary": (row.get("summary") or "").strip(),
        "highlights": highlights,
        "from_kameyama": (row.get("from_kameyama") or "").strip(),
    }
    # 任意フィールド: 値がある場合のみ追加
    optional_str = [
        "name_en", "official_url", "region", "category_label",
        "editorial_status", "visit_priority", "safety_level",
        "safety_note", "source_quality", "last_verified",
    ]
    for k in optional_str:
        v = (row.get(k) or "").strip()
        if v:
            entry[k] = v
    if ref_urls:
        entry["reference_urls"] = ref_urls

    return entry


def build_fest_entry(row, new_id):
    """festival 用エントリ生成 (簡易: 既存スキーマ準拠)"""
    highlights = split_semi(row.get("highlights")) or []
    ref_urls = split_semi(row.get("reference_urls")) or []
    wiki_url = (row.get("wiki_url") or "").strip()
    if wiki_url and wiki_url not in ref_urls:
        ref_urls.append(wiki_url)

    entry = {
        "id": new_id,
        "name": (row.get("name") or "").strip(),
        "name_kana": (row.get("name_kana") or "").strip(),
        "category": (row.get("category_slug") or row.get("category") or "").strip(),
        "prefecture": (row.get("prefecture") or "").strip(),
        "city": (row.get("city") or "").strip(),
        "shrine": (row.get("shrine") or "").strip(),
        "lat": float(row["lat"]) if row.get("lat") else None,
        "lng": float(row["lng"]) if row.get("lng") else None,
        "date_pattern": (row.get("date_pattern") or "").strip(),
        "summary": (row.get("summary") or "").strip(),
        "highlights": highlights,
        "origin": (row.get("origin") or "").strip(),
        "viewing_notes": (row.get("viewing_notes") or "").strip(),
    }
    optional_str = ["name_en", "date_2026", "date_2026_end", "official_url"]
    for k in optional_str:
        v = (row.get(k) or "").strip()
        if v:
            entry[k] = v
    if ref_urls:
        entry["reference_urls"] = ref_urls
    return entry


def validate_spot(entry):
    """必須フィールド検査。問題があれば理由を返す"""
    required = [
        "name", "name_kana", "category", "prefecture", "city",
        "address", "lat", "lng", "summary",
    ]
    for k in required:
        if entry.get(k) in (None, "", []):
            return f"必須フィールド '{k}' が空"
    if entry["category"] not in VALID_SLUGS:
        return f"category slug 不正: '{entry['category']}' (許可: {VALID_SLUGS})"
    if not isinstance(entry["lat"], (int, float)) or not isinstance(entry["lng"], (int, float)):
        return f"lat/lng が数値でない: lat={entry.get('lat')}, lng={entry.get('lng')}"
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--no-build", action="store_true", help="build_data.py を実行しない")
    parser.add_argument("--strict", action="store_true", help="必須項目欠落をエラー扱い (デフォルトは警告)")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"ERROR: {csv_path} がない", file=sys.stderr)
        sys.exit(1)

    spots = load_json(SPOTS_JSON)
    fests = load_json(FESTIVALS_JSON)

    added_spots = added_fests = 0
    warnings = []

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            decision = (row.get("decision") or "").strip()
            if decision != "採用":
                continue
            if (row.get("is_duplicate") or "").strip() == "重複":
                print(f"  SKIP 重複: {row.get('name')}")
                continue

            slug = resolve_slug(row)
            if slug == "festival":
                new_id = next_id(fests["items"], "fest")
                entry = build_fest_entry(row, new_id)
                fests["items"].append(entry)
                added_fests += 1
                print(f"  + {new_id}: {entry['name']} (festival)")
            elif slug in VALID_SLUGS:
                new_id = next_id(spots["items"], "spot")
                entry = build_spot_entry(row, new_id)
                err = validate_spot(entry)
                if err:
                    msg = f"  ⚠ {new_id} ({entry.get('name')}): {err}"
                    if args.strict:
                        print(msg, file=sys.stderr)
                        sys.exit(2)
                    warnings.append(msg)
                    print(f"  ⚠ SKIP {new_id} ({entry['name']}): {err}")
                    continue
                spots["items"].append(entry)
                added_spots += 1
                print(f"  + {new_id}: {entry['name']} ({slug})")
            else:
                print(f"  SKIP category 解決不可: name={row.get('name')}, category={row.get('category')}")
                continue

    if warnings:
        print("\n--- 警告 ---")
        for w in warnings:
            print(w)

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
