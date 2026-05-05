#!/usr/bin/env python3
"""
Fetch image URLs from English Wikipedia for remaining items.
Also uses Japanese Wikipedia directly for some items.
"""
import json, urllib.parse, urllib.request, re, time, os

EN_API = "https://en.wikipedia.org/w/api.php"
JA_API = "https://ja.wikipedia.org/w/api.php"

def safe_get(url, delay=1.5):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ChinSpotBot/1.0"})
        with urllib.request.urlopen(req, timeout=12) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

def get_thumb(api_url, title):
    """Get thumbnail URL from Wikipedia API."""
    params = urllib.parse.urlencode({
        "action": "query",
        "titles": title,
        "prop": "pageimages",
        "pithumbsize": "1200",
        "pilimit": "1",
        "format": "json"
    })
    data = safe_get(f"{api_url}?{params}")
    if not data:
        return None
    for page in data.get("query", {}).get("pages", {}).values():
        t = page.get("thumbnail", {})
        src = t.get("source", "")
        if src and not src.endswith(".svg"):
            return src
    return None

# Map: item_id -> (api, article_title)
LOOKUPS = {
    # Spots
    "spot-004": (EN_API, "Momotarō_Shrine"),
    "spot-005": (EN_API, "Yoro_Park"),
    "spot-006": (EN_API, "Sekigahara_Warland"),
    "spot-007": (JA_API, "珍品城"),
    "spot-008": (JA_API, "熱海秘宝館"),
    "spot-009": (JA_API, "怪しい少年少女博物館"),
    "spot-011": (EN_API, "Tower_of_the_Sun"),
    "spot-015": (EN_API, "Shigaraki_ware"),
    "spot-016": (EN_API, "Hana_no_Iwaya_Shrine"),
    "spot-018": (JA_API, "女鬼トンネル"),
    "spot-019": (JA_API, "長野峠"),
    "spot-020": (EN_API, "Yunoyama_Onsen"),
    "spot-022": (JA_API, "首塚大明神"),
    "spot-023": (EN_API, "Toribeno"),
    "spot-024": (EN_API, "Mount_Inunaki"),
    "spot-025": (JA_API, "鵺"),
    "spot-026": (JA_API, "白高大神"),
    "spot-028": (EN_API, "Tomogashima"),
    "spot-029": (EN_API, "Kibune_Shrine"),
    "spot-031": (EN_API, "Ganzan_Pyramid"),
    "spot-032": (EN_API, "Sakafune_Ishi"),
    "spot-034": (EN_API, "Takeda_Castle"),
    "spot-040": (EN_API, "Tsubaki_Grand_Shrine"),
    "spot-041": (EN_API, "Maruyama_Senmaida"),
    "spot-047": (EN_API, "Izu_Gokurakuen"),
    "spot-048": (EN_API, "Ryūgūkutsu"),
    "spot-050": (JA_API, "岐阜レトロミュージアム"),
    # Festivals
    "fest-004": (EN_API, "Konomiya_Hadaka_Matsuri"),
    "fest-006": (EN_API, "Oto_Matsuri"),
    "fest-008": (JA_API, "豊橋鬼祭り"),
    "fest-009": (EN_API, "Sand-throwing_Festival"),
    "fest-010": (EN_API, "Hōnen_Festival"),
    "fest-015": (JA_API, "大瀬神社"),
    "fest-016": (EN_API, "Yasurai_Festival"),
    "fest-017": (JA_API, "手力の火祭り"),
    "fest-018": (EN_API, "Nagahama_Hikiyama_Festival"),
    "fest-019": (EN_API, "Furukawa_Festival"),
    "fest-021": (EN_API, "Age-Uma_Shinji"),
    "fest-023": (JA_API, "鍋冠祭"),
    "fest-024": (EN_API, "Nachi_Fire_Festival"),
    "fest-025": (JA_API, "豊浜鯛まつり"),
    "fest-026": (JA_API, "大島祭"),
    "fest-027": (EN_API, "Gion_Festival"),
    "fest-028": (EN_API, "Gozan_no_Okuribi"),
    "fest-029": (EN_API, "Ishidori_Festival"),
    "fest-030": (JA_API, "刈谷万燈祭"),
    "fest-031": (JA_API, "芋競べ祭り"),
    "fest-032": (JA_API, "七宮詣り"),
    "fest-033": (EN_API, "Uneme_Festival"),
    "fest-034": (EN_API, "Kurama_Fire_Festival"),
    "fest-035": (EN_API, "Nada_Fighting_Festival"),
    "fest-036": (JA_API, "笑い祭"),
    "fest-037": (EN_API, "Takayama_Festival"),
    "fest-038": (EN_API, "Bull_Festival,_Kyoto"),
    "fest-039": (JA_API, "奥山大権現"),
    "fest-040": (JA_API, "富田の鯨船行事"),
    "fest-041": (EN_API, "Isonokami_Shrine"),
    "fest-042": (JA_API, "長浜曳山まつり"),
    "fest-043": (JA_API, "どんき祭"),
    "fest-044": (EN_API, "Kasuga_Wakamiya_On-Matsuri"),
    "fest-045": (EN_API, "Tsubaki_Grand_Shrine"),
    "fest-046": (EN_API, "Isonokami_Shrine"),
    "fest-047": (EN_API, "Tado_Grand_Shrine"),
}

# Load existing photos
with open("/home/user/workspace/chinspot-map/photos.json") as f:
    photos = json.load(f)

results = {}
count = 0

for item_id, (api_url, title) in LOOKUPS.items():
    if photos.get(item_id, {}).get("primary"):
        continue
    
    print(f"[{item_id}] {title}... ", end="", flush=True)
    time.sleep(1.5)
    
    url = get_thumb(api_url, title)
    if url:
        print(f"OK: {url[:70]}")
        results[item_id] = url
    else:
        print("NOT FOUND")
    
    count += 1
    if count % 15 == 0:
        # Save intermediate
        with open("/home/user/workspace/chinspot-map/en_wiki_images.json", "w") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"  [Saved {len(results)} so far]")

# Final save
with open("/home/user/workspace/chinspot-map/en_wiki_images.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nTotal found: {len(results)}")

# Update photos.json
count_updated = 0
for item_id, img_url in results.items():
    if not photos.get(item_id, {}).get("primary"):
        photos[item_id]["primary"] = img_url
        photos[item_id]["credit"] = "Wikimedia Commons / Wikipedia contributor / CC BY-SA"
        photos[item_id]["alt_photos"] = []
        count_updated += 1

with open("/home/user/workspace/chinspot-map/photos.json", "w", encoding="utf-8") as f:
    json.dump(photos, f, ensure_ascii=False, indent=2)

found_total = sum(1 for v in photos.values() if v.get("primary"))
print(f"Updated {count_updated}. Now have {found_total}/97")

missing = [k for k, v in photos.items() if not v.get("primary")]
print(f"Remaining missing ({len(missing)}): {missing}")
