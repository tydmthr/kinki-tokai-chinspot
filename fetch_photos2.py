#!/usr/bin/env python3
"""
Fetch photo URLs for Japanese spots and festivals.
Uses Wikimedia Commons API and Wikipedia article images.
Includes rate limiting and retry logic.
"""

import json
import time
import urllib.parse
import urllib.request
import re
import os

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
WIKIPEDIA_API = "https://ja.wikipedia.org/w/api.php"

def safe_request(url, retries=3, delay=3):
    """Make HTTP request with retries."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "ChinSpotPhotoBot/1.0 (educational project; contact: research)"
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            if "429" in str(e) or "Too Many" in str(e):
                wait = delay * (attempt + 2)
                print(f"    Rate limited, waiting {wait}s...")
                time.sleep(wait)
            elif attempt < retries - 1:
                time.sleep(delay)
            else:
                print(f"    Request failed: {e}")
    return None

def get_commons_images(query, limit=4):
    """Search Wikimedia Commons for images."""
    params = {
        "action": "query",
        "generator": "search",
        "gsrnamespace": "6",
        "gsrsearch": query,
        "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url|extmetadata",
        "iiurlwidth": "1000",
        "format": "json",
        "origin": "*"
    }
    url = COMMONS_API + "?" + urllib.parse.urlencode(params)
    data = safe_request(url)
    if not data:
        return []
    
    results = []
    pages = data.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        ii = page.get("imageinfo", [])
        if not ii:
            continue
        info = ii[0]
        img_url = info.get("url", "")
        # Only actual image files
        if not any(img_url.lower().endswith(e) for e in ['.jpg', '.jpeg', '.png', '.webp', '.gif']):
            continue
        # Skip GIF for quality
        if img_url.lower().endswith('.gif'):
            continue
        
        ext = info.get("extmetadata", {})
        artist = ext.get("Artist", {}).get("value", "")
        artist_clean = re.sub(r'<[^>]+>', '', artist).strip()
        license_short = ext.get("LicenseShortName", {}).get("value", "CC BY-SA")
        
        results.append({
            "url": img_url,
            "thumb": info.get("thumburl", img_url),
            "artist": artist_clean,
            "license": license_short,
            "filename": page.get("title", "")
        })
    
    return results

def get_wikipedia_image(article_name):
    """Get main image from a Wikipedia article."""
    params = {
        "action": "query",
        "titles": article_name,
        "prop": "pageimages|images",
        "pithumbsize": "1000",
        "pilimit": "1",
        "format": "json",
        "origin": "*"
    }
    url = WIKIPEDIA_API + "?" + urllib.parse.urlencode(params)
    data = safe_request(url)
    if not data:
        return None
    
    pages = data.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        if page_id == "-1":
            continue
        if "thumbnail" in page:
            thumb_url = page["thumbnail"]["source"]
            # Try to get full URL
            m = re.search(r'wikipedia/commons/thumb/(.+?)(?:/\d+px-[^/]+)?$', thumb_url)
            if m:
                path = m.group(1)
                full_url = f"https://upload.wikimedia.org/wikipedia/commons/{path}"
                return {
                    "url": full_url,
                    "thumb": thumb_url,
                    "artist": "Wikipedia contributor",
                    "license": "CC BY-SA"
                }
            # For ja wikipedia images
            m2 = re.search(r'wikipedia/ja/thumb/(.+?)(?:/\d+px-[^/]+)?$', thumb_url)
            if m2:
                path = m2.group(1)
                full_url = f"https://upload.wikimedia.org/wikipedia/ja/{path}"
                return {
                    "url": full_url,
                    "thumb": thumb_url,
                    "artist": "Wikipedia contributor",
                    "license": "CC BY-SA"
                }
    return None

def get_commons_file_url(filename):
    """Get direct URL for a specific Commons file."""
    params = {
        "action": "query",
        "titles": f"File:{filename}",
        "prop": "imageinfo",
        "iiprop": "url|extmetadata",
        "iiurlwidth": "1000",
        "format": "json",
        "origin": "*"
    }
    url = COMMONS_API + "?" + urllib.parse.urlencode(params)
    data = safe_request(url)
    if not data:
        return None
    
    pages = data.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        ii = page.get("imageinfo", [])
        if ii:
            info = ii[0]
            ext = info.get("extmetadata", {})
            artist = ext.get("Artist", {}).get("value", "")
            artist_clean = re.sub(r'<[^>]+>', '', artist).strip()
            return {
                "url": info.get("url", ""),
                "artist": artist_clean,
                "license": ext.get("LicenseShortName", {}).get("value", "CC BY-SA")
            }
    return None

# Known good file mappings (pre-researched to avoid rate limits)
KNOWN_IMAGES = {
    "spot-001": {
        "query": "田縣神社",
        "wiki_article": "田縣神社"
    },
    "spot-002": {
        "query": "大縣神社",
        "wiki_article": "大縣神社"
    },
    "spot-003": {
        "query": "五色園",
        "wiki_article": "五色園"
    },
    "spot-004": {
        "query": "桃太郎神社 犬山",
        "wiki_article": "桃太郎神社"
    },
    "spot-005": {
        "query": "養老天命反転地",
        "wiki_article": "養老天命反転地"
    },
    "spot-006": {
        "query": "関ケ原ウォーランド",
        "wiki_article": "関ヶ原ウォーランド"
    },
    "spot-007": {
        "query": "珍品城 岐阜",
        "wiki_article": None
    },
    "spot-008": {
        "query": "熱海秘宝館",
        "wiki_article": "熱海秘宝館"
    },
    "spot-009": {
        "query": "怪しい少年少女博物館",
        "wiki_article": "怪しい少年少女博物館"
    },
    "spot-010": {
        "query": "摩耶観光ホテル 廃墟",
        "wiki_article": "摩耶観光ホテル"
    },
    "spot-011": {
        "query": "太陽の塔 Tower of the Sun",
        "wiki_article": "太陽の塔"
    },
    "spot-012": {
        "query": "難波八阪神社 lion",
        "wiki_article": "難波八阪神社"
    },
    "spot-013": {
        "query": "生駒山上遊園地",
        "wiki_article": "生駒山上遊園地"
    },
    "spot-014": {
        "query": "旧奈良監獄",
        "wiki_article": "奈良少年刑務所"
    },
    "spot-015": {
        "query": "信楽焼 狸 tanuki",
        "wiki_article": "信楽焼"
    },
    "spot-016": {
        "query": "花の窟神社 三重",
        "wiki_article": "花の窟神社"
    },
    "spot-017": {
        "query": "夫婦岩 二見浦",
        "wiki_article": "夫婦岩"
    },
    "spot-018": {
        "query": "女鬼トンネル 三重",
        "wiki_article": None
    },
    "spot-019": {
        "query": "長野トンネル 三重",
        "wiki_article": None
    },
    "spot-020": {
        "query": "湯の山温泉 廃墟",
        "wiki_article": "湯の山温泉"
    },
    "spot-021": {
        "query": "化野念仏寺 石仏",
        "wiki_article": "化野念仏寺"
    },
    "spot-022": {
        "query": "首塚大明神 京都",
        "wiki_article": "首塚大明神"
    },
    "spot-023": {
        "query": "鳥辺野 京都 墓地",
        "wiki_article": "鳥辺野"
    },
    "spot-024": {
        "query": "犬鳴山 大阪",
        "wiki_article": "犬鳴山"
    },
    "spot-025": {
        "query": "鵺塚 大阪",
        "wiki_article": "鵺"
    },
    "spot-026": {
        "query": "白高大神 奈良",
        "wiki_article": None
    },
    "spot-027": {
        "query": "摩耶観光ホテル マヤカン 神戸",
        "wiki_article": "摩耶観光ホテル"
    },
    "spot-028": {
        "query": "友ヶ島 要塞 砲台",
        "wiki_article": "友ヶ島"
    },
    "spot-029": {
        "query": "貴船神社 京都",
        "wiki_article": "貴船神社"
    },
    "spot-030": {
        "query": "伏見稲荷大社 千本鳥居",
        "wiki_article": "伏見稲荷大社"
    },
    "spot-031": {
        "query": "頭塔 奈良",
        "wiki_article": "頭塔"
    },
    "spot-032": {
        "query": "酒船石 亀形石 飛鳥",
        "wiki_article": "酒船石"
    },
    "spot-033": {
        "query": "益田岩船 奈良",
        "wiki_article": "益田岩船"
    },
    "spot-034": {
        "query": "竹田城 天空の城",
        "wiki_article": "竹田城"
    },
    "spot-035": {
        "query": "高野山 奥の院 墓地",
        "wiki_article": "高野山"
    },
    "spot-036": {
        "query": "玉置神社 奈良",
        "wiki_article": "玉置神社"
    },
    "spot-037": {
        "query": "天河大弁財天社",
        "wiki_article": "天河大弁財天社"
    },
    "spot-038": {
        "query": "橋杭岩 和歌山",
        "wiki_article": "橋杭岩"
    },
    "spot-039": {
        "query": "那智の滝 Nachi Falls",
        "wiki_article": "那智滝"
    },
    "spot-040": {
        "query": "椿大神社 三重",
        "wiki_article": "椿大神社"
    },
    "spot-041": {
        "query": "丸山千枚田 三重",
        "wiki_article": "丸山千枚田"
    },
    "spot-042": {
        "query": "鬼ヶ城 三重 熊野",
        "wiki_article": "鬼ヶ城"
    },
    "spot-043": {
        "query": "獅子岩 三重 熊野",
        "wiki_article": "獅子岩 (熊野市)"
    },
    "spot-044": {
        "query": "多賀大社 滋賀",
        "wiki_article": "多賀大社"
    },
    "spot-045": {
        "query": "養老の滝 岐阜",
        "wiki_article": "養老の滝"
    },
    "spot-046": {
        "query": "白川郷 合掌造り",
        "wiki_article": "白川郷"
    },
    "spot-047": {
        "query": "伊豆極楽苑 地獄",
        "wiki_article": "伊豆極楽苑"
    },
    "spot-048": {
        "query": "竜宮窟 伊豆",
        "wiki_article": "竜宮窟"
    },
    "spot-049": {
        "query": "飛び出し坊や 滋賀 発祥",
        "wiki_article": "飛び出し坊や"
    },
    "spot-050": {
        "query": "岐阜レトロミュージアム",
        "wiki_article": None
    },
    "fest-001": {
        "query": "法界寺 裸踊り",
        "wiki_article": "法界寺"
    },
    "fest-002": {
        "query": "四天王寺 どやどや",
        "wiki_article": "四天王寺"
    },
    "fest-003": {
        "query": "西宮神社 福男",
        "wiki_article": "西宮神社"
    },
    "fest-004": {
        "query": "国府宮はだか祭 儺追神事",
        "wiki_article": "儺追神事"
    },
    "fest-005": {
        "query": "飛鳥坐神社 おんだ祭",
        "wiki_article": "飛鳥坐神社"
    },
    "fest-006": {
        "query": "神倉神社 お燈祭り 松明",
        "wiki_article": "御燈祭り"
    },
    "fest-007": {
        "query": "尾鷲ヤーヤ祭り",
        "wiki_article": "尾鷲神社"
    },
    "fest-008": {
        "query": "豊橋鬼祭り",
        "wiki_article": "豊橋鬼祭り"
    },
    "fest-009": {
        "query": "砂かけ祭り 奈良",
        "wiki_article": "砂かけ祭"
    },
    "fest-010": {
        "query": "田縣神社 豊年祭",
        "wiki_article": "豊年祭 (田縣神社)"
    },
    "fest-011": {
        "query": "大縣神社 姫の宮",
        "wiki_article": "大縣神社"
    },
    "fest-012": {
        "query": "東大寺 修二会 お松明 松明",
        "wiki_article": "修二会"
    },
    "fest-013": {
        "query": "清凉寺 嵯峨お松明式",
        "wiki_article": "清凉寺"
    },
    "fest-014": {
        "query": "淡嶋神社 雛流し 和歌山",
        "wiki_article": "淡嶋神社"
    },
    "fest-015": {
        "query": "大瀬まつり 静岡 内浦",
        "wiki_article": "大瀬神社"
    },
    "fest-016": {
        "query": "やすらい祭 京都",
        "wiki_article": "やすらい祭"
    },
    "fest-017": {
        "query": "手力雄神社 火祭り",
        "wiki_article": "手力の火祭り"
    },
    "fest-018": {
        "query": "長浜曳山まつり 子ども歌舞伎",
        "wiki_article": "長浜曳山まつり"
    },
    "fest-019": {
        "query": "古川祭 起し太鼓 飛騨",
        "wiki_article": "古川祭"
    },
    "fest-020": {
        "query": "高山祭 山王祭 屋台",
        "wiki_article": "高山祭"
    },
    "fest-021": {
        "query": "多度大社 上げ馬神事",
        "wiki_article": "上げ馬神事"
    },
    "fest-022": {
        "query": "伊雑宮 御田植祭",
        "wiki_article": "伊雑宮"
    },
    "fest-023": {
        "query": "鍋冠祭 名古屋",
        "wiki_article": None
    },
    "fest-024": {
        "query": "那智の火祭 扇祭り",
        "wiki_article": "那智の火祭"
    },
    "fest-025": {
        "query": "豊浜鯛まつり 愛知",
        "wiki_article": "豊浜鯛まつり"
    },
    "fest-026": {
        "query": "潮かけ祭り 三重 大島",
        "wiki_article": None
    },
    "fest-027": {
        "query": "祇園祭 山鉾巡行 京都",
        "wiki_article": "祇園祭"
    },
    "fest-028": {
        "query": "京都 五山送り火 大文字",
        "wiki_article": "五山送り火"
    },
    "fest-029": {
        "query": "桑名石取祭",
        "wiki_article": "石取祭"
    },
    "fest-030": {
        "query": "刈谷万燈祭",
        "wiki_article": "刈谷万燈祭"
    },
    "fest-031": {
        "query": "近江中山 芋競べ祭り",
        "wiki_article": "芋競べ祭り"
    },
    "fest-032": {
        "query": "大阪 七宮詣り",
        "wiki_article": None
    },
    "fest-033": {
        "query": "采女祭 猿沢池 奈良",
        "wiki_article": "采女祭"
    },
    "fest-034": {
        "query": "鞍馬の火祭 由岐神社",
        "wiki_article": "鞍馬の火祭"
    },
    "fest-035": {
        "query": "灘のけんか祭り 神輿",
        "wiki_article": "灘のけんか祭り"
    },
    "fest-036": {
        "query": "笑い祭 丹生神社 和歌山",
        "wiki_article": "笑い祭"
    },
    "fest-037": {
        "query": "高山祭 八幡祭 秋 屋台",
        "wiki_article": "高山祭"
    },
    "fest-038": {
        "query": "広隆寺 牛祭り 太秦",
        "wiki_article": "牛祭"
    },
    "fest-039": {
        "query": "虫送り 浜松 奥山",
        "wiki_article": None
    },
    "fest-040": {
        "query": "富田鯨船 三重 四日市",
        "wiki_article": "富田の鯨船行事"
    },
    "fest-041": {
        "query": "石上神宮 鎮魂祭 奈良",
        "wiki_article": "石上神宮"
    },
    "fest-042": {
        "query": "長浜 曳山まつり 船 神輿",
        "wiki_article": "長浜曳山まつり"
    },
    "fest-043": {
        "query": "豊橋 どんき祭り",
        "wiki_article": None
    },
    "fest-044": {
        "query": "春日若宮おん祭 奈良",
        "wiki_article": "春日若宮おん祭"
    },
    "fest-045": {
        "query": "椿大神社 御頭神事",
        "wiki_article": "椿大神社"
    },
    "fest-046": {
        "query": "石上神宮 摂社 産声祭",
        "wiki_article": "石上神宮"
    },
    "fest-047": {
        "query": "多度大社 馬 祭り",
        "wiki_article": "多度大社"
    }
}

# Load existing data
output_path = "/home/user/workspace/chinspot-map/photos.json"
if os.path.exists(output_path):
    with open(output_path) as f:
        photos = json.load(f)
    # Remove null entries to retry them
    to_retry = [k for k, v in photos.items() if v.get("primary") is None]
    print(f"Loaded {len(photos)} entries, {len(to_retry)} have null primary (will retry)")
else:
    photos = {}

def save_progress():
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(photos, f, ensure_ascii=False, indent=2)

# Load original data for names
with open("/home/user/workspace/chinspot-map/spots.json") as f:
    spots = {s["id"]: s for s in json.load(f)}
with open("/home/user/workspace/chinspot-map/festivals.json") as f:
    festivals = {f["id"]: f for f in json.load(f)}

all_names = {}
all_names.update({k: v["name"] for k, v in spots.items()})
all_names.update({k: v["name"] for k, v in festivals.items()})

# Process each item
count = 0
for item_id, mapping in KNOWN_IMAGES.items():
    name = all_names.get(item_id, item_id)
    
    # Skip if already have a good photo
    if item_id in photos and photos[item_id].get("primary"):
        print(f"[{item_id}] Already have photo: {name}")
        continue
    
    print(f"\n[{item_id}] {name}")
    
    result = {
        "name": name,
        "primary": None,
        "credit": None,
        "alt_photos": []
    }
    
    # Try Wikipedia article first (usually best representative image)
    wiki_article = mapping.get("wiki_article")
    if wiki_article:
        time.sleep(1.5)
        wiki_img = get_wikipedia_image(wiki_article)
        if wiki_img and wiki_img.get("url"):
            url = wiki_img["url"]
            if any(url.lower().endswith(e) for e in ['.jpg', '.jpeg', '.png', '.webp']):
                result["primary"] = url
                result["credit"] = f"Wikimedia Commons / {wiki_img.get('artist', 'Wikipedia contributor')} / {wiki_img.get('license', 'CC BY-SA')}"
                print(f"  -> Wikipedia: {url[:80]}...")
    
    # If no Wikipedia image, try Commons search
    if not result["primary"]:
        query = mapping.get("query", name)
        time.sleep(2)
        commons_results = get_commons_images(query, limit=4)
        if commons_results:
            primary = commons_results[0]
            result["primary"] = primary["url"]
            artist = primary.get("artist", "")
            license_str = primary.get("license", "CC BY-SA")
            result["credit"] = f"Wikimedia Commons / {artist} / {license_str}" if artist else f"Wikimedia Commons / {license_str}"
            result["alt_photos"] = [r["url"] for r in commons_results[1:3]]
            print(f"  -> Commons: {primary['url'][:80]}...")
        else:
            print(f"  -> Not found")
    
    photos[item_id] = result
    count += 1
    
    # Save every 10 items
    if count % 10 == 0:
        save_progress()
        found = sum(1 for v in photos.values() if v.get("primary"))
        print(f"\n  [Progress saved: {len(photos)} total, {found} found]\n")

save_progress()
found = sum(1 for v in photos.values() if v.get("primary"))
total = len(photos)
print(f"\n=== DONE ===")
print(f"Total: {total} | Found: {found} | Missing: {total - found}")
print(f"Success rate: {found/total*100:.1f}%")

# List missing ones
missing = [k for k, v in photos.items() if not v.get("primary")]
if missing:
    print(f"\nMissing IDs: {', '.join(missing)}")
