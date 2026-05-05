#!/usr/bin/env python3
"""Update photos.json with confirmed wiki_images.json URLs."""
import json, urllib.request, time, re

# Load
with open("/home/user/workspace/chinspot-map/wiki_images.json") as f:
    wiki = json.load(f)
with open("/home/user/workspace/chinspot-map/photos.json") as f:
    photos = json.load(f)

def check_url(url):
    try:
        req = urllib.request.Request(url, method='HEAD', headers={"User-Agent": "Bot/1.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.status == 200
    except:
        return False

# Verify each URL
count = 0
for item_id, info in wiki.items():
    if photos.get(item_id, {}).get("primary"):
        continue
    url = info["url"]
    # Skip obviously bad ones (wrong content)
    if "Jar_Anonymous" in url:  # Shigaraki got wrong image
        print(f"[{item_id}] Skipping wrong image")
        continue
    
    print(f"[{item_id}] Checking {url[:70]}... ", end="")
    ok = check_url(url)
    if ok:
        print("OK")
        photos[item_id]["primary"] = url
        photos[item_id]["credit"] = "Wikimedia Commons / Wikipedia contributor / CC BY-SA"
        photos[item_id]["alt_photos"] = []
        count += 1
    else:
        print("FAIL")
    time.sleep(0.3)

with open("/home/user/workspace/chinspot-map/photos.json", "w", encoding="utf-8") as f:
    json.dump(photos, f, ensure_ascii=False, indent=2)

found = sum(1 for v in photos.values() if v.get("primary"))
print(f"\nUpdated {count}. Total: {found}/97")
