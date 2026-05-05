#!/usr/bin/env python3
"""
Fetch actual Wikipedia article images via pageimages API in batches.
"""
import json
import urllib.parse
import urllib.request
import re
import time
import hashlib

WIKIPEDIA_API = "https://ja.wikipedia.org/w/api.php"

def safe_request(url, retries=2, delay=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ChinSpotBot/1.0"})
            with urllib.request.urlopen(req, timeout=12) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            if "429" in str(e):
                time.sleep(delay * (attempt+2))
            elif attempt < retries - 1:
                time.sleep(delay)
    return None

def commons_url(filename):
    fname = filename.replace(" ", "_")
    md5 = hashlib.md5(fname.encode('utf-8')).hexdigest()
    a, ab = md5[0], md5[0:2]
    encoded = urllib.parse.quote(fname, safe='')
    return f"https://upload.wikimedia.org/wikipedia/commons/{a}/{ab}/{encoded}"

# Articles to look up in batches
ARTICLES = {
    "spot-004": "桃太郎神社 (犬山市)",
    "spot-005": "養老天命反転地",
    "spot-006": "関ヶ原ウォーランド",
    "spot-008": "熱海秘宝館",
    "spot-009": "怪しい少年少女博物館",
    "spot-011": "太陽の塔",
    "spot-015": "信楽焼",
    "spot-016": "花の窟神社",
    "spot-022": "首塚大明神",
    "spot-023": "鳥辺野",
    "spot-024": "犬鳴山 (大阪府)",
    "spot-025": "鵺",
    "spot-028": "友ヶ島",
    "spot-029": "貴船神社",
    "spot-031": "頭塔",
    "spot-032": "酒船石",
    "spot-034": "竹田城",
    "spot-040": "椿大神社",
    "spot-041": "丸山千枚田",
    "spot-048": "竜宮窟",
    "fest-004": "儺追神事",
    "fest-006": "御燈祭り",
    "fest-008": "豊橋鬼祭り",
    "fest-009": "砂かけ祭",
    "fest-010": "豊年祭 (田縣神社)",
    "fest-016": "やすらい祭",
    "fest-017": "手力の火祭り",
    "fest-018": "長浜曳山まつり",
    "fest-019": "古川祭",
    "fest-021": "上げ馬神事",
    "fest-024": "那智の火祭",
    "fest-033": "采女祭",
    "fest-034": "鞍馬の火祭",
    "fest-035": "灘のけんか祭り",
    "fest-044": "春日若宮おん祭",
}

results = {}

for item_id, article in ARTICLES.items():
    params = {
        "action": "query",
        "titles": article,
        "prop": "pageimages",
        "pithumbsize": "1200",
        "pilimit": "1",
        "format": "json",
        "origin": "*"
    }
    url = WIKIPEDIA_API + "?" + urllib.parse.urlencode(params)
    time.sleep(1.2)
    data = safe_request(url)
    if not data:
        print(f"[{item_id}] {article}: API error")
        continue
    
    pages = data.get("query", {}).get("pages", {})
    found = False
    for page_id, page in pages.items():
        if page_id == "-1":
            print(f"[{item_id}] {article}: article not found")
            continue
        
        if "thumbnail" in page:
            thumb = page["thumbnail"]["source"]
            print(f"[{item_id}] {article}: thumb = {thumb[:80]}")
            
            # Extract the file path
            # Pattern: .../wikipedia/commons/thumb/a/ab/FILENAME.ext/800px-FILENAME.ext
            m = re.search(r'wikipedia/commons/thumb/([0-9a-f]/[0-9a-f]{2}/(.+?))(?:/\d+px-.+)?$', thumb)
            if m:
                full_path = m.group(1)
                filename = m.group(2)
                full_url = f"https://upload.wikimedia.org/wikipedia/commons/{full_path}"
                # Remove the /800px-... part if present
                full_url = re.sub(r'/\d+px-.+$', '', full_url)
                results[item_id] = {
                    "url": full_url,
                    "filename": urllib.parse.unquote(filename),
                    "thumb": thumb
                }
                found = True
                break
            
            # Try ja wikipedia pattern
            m2 = re.search(r'wikipedia/ja/thumb/([0-9a-f]/[0-9a-f]{2}/(.+?))(?:/\d+px-.+)?$', thumb)
            if m2:
                full_path = m2.group(1)
                filename = m2.group(2)
                full_url = f"https://upload.wikimedia.org/wikipedia/ja/{full_path}"
                full_url = re.sub(r'/\d+px-.+$', '', full_url)
                results[item_id] = {
                    "url": full_url,
                    "filename": urllib.parse.unquote(filename),
                    "thumb": thumb,
                    "ja_only": True
                }
                found = True
                break
            
            # Fallback: use thumb itself
            results[item_id] = {"url": thumb, "filename": "", "thumb": thumb}
            found = True
            break
        else:
            print(f"[{item_id}] {article}: no thumbnail")
    
    if not found and "-1" not in pages:
        # Try page_image prop differently
        for page_id, page in pages.items():
            if "page_image_free" in page or "pageimage" in page:
                imgname = page.get("pageimage", page.get("page_image_free", ""))
                if imgname:
                    url2 = commons_url(imgname)
                    results[item_id] = {"url": url2, "filename": imgname}
                    print(f"[{item_id}] {article}: pageimage = {imgname}")
                    break

print(f"\nFound {len(results)} articles with images")

with open("/home/user/workspace/chinspot-map/wiki_images.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
