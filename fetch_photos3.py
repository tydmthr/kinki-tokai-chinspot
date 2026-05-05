#!/usr/bin/env python3
"""
Fast batch photo URL fetcher using direct Wikimedia API calls.
Processes remaining 67 missing items.
"""

import json
import time
import urllib.parse
import urllib.request
import re
import os

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
WIKIPEDIA_API = "https://ja.wikipedia.org/w/api.php"
WIKIPEDIA_EN_API = "https://en.wikipedia.org/w/api.php"

def safe_request(url, retries=2, delay=2):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "ChinSpotPhotoBot/1.0"
            })
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            if "429" in str(e):
                wait = delay * (attempt + 2)
                time.sleep(wait)
            elif attempt < retries - 1:
                time.sleep(delay)
    return None

def get_wikipedia_image(article_name, api=None):
    if api is None:
        api = WIKIPEDIA_API
    params = {
        "action": "query",
        "titles": article_name,
        "prop": "pageimages",
        "pithumbsize": "1000",
        "pilimit": "1",
        "format": "json",
        "origin": "*"
    }
    url = api + "?" + urllib.parse.urlencode(params)
    data = safe_request(url)
    if not data:
        return None
    
    pages = data.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        if page_id == "-1":
            continue
        if "thumbnail" in page:
            thumb_url = page["thumbnail"]["source"]
            m = re.search(r'wikipedia/commons/thumb/(.+?)(?:/\d+px-[^/]+)?$', thumb_url)
            if m:
                path = m.group(1)
                full_url = f"https://upload.wikimedia.org/wikipedia/commons/{path}"
                return {"url": full_url, "thumb": thumb_url}
            m2 = re.search(r'wikipedia/ja/thumb/(.+?)(?:/\d+px-[^/]+)?$', thumb_url)
            if m2:
                return {"url": thumb_url, "thumb": thumb_url}
            m3 = re.search(r'wikipedia/en/thumb/(.+?)(?:/\d+px-[^/]+)?$', thumb_url)
            if m3:
                return {"url": thumb_url, "thumb": thumb_url}
    return None

def get_commons_images(query, limit=3):
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
        if not any(img_url.lower().endswith(e) for e in ['.jpg', '.jpeg', '.png', '.webp']):
            continue
        ext = info.get("extmetadata", {})
        artist = re.sub(r'<[^>]+>', '', ext.get("Artist", {}).get("value", "")).strip()
        license_short = ext.get("LicenseShortName", {}).get("value", "CC BY-SA")
        results.append({
            "url": img_url,
            "thumb": info.get("thumburl", img_url),
            "artist": artist,
            "license": license_short
        })
    return results

# Manually curated direct Commons file paths for items likely to timeout
# These are known good files from Wikimedia Commons
DIRECT_FILES = {
    "spot-004": ("File:Momotaro shrine 1.jpg", "Wikimedia Commons / Tzuhsun Hsu / CC BY-SA 2.0"),
    "spot-005": {"url": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Yoro_Kinetic_Experience_Museum_or_Yoro_Park.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
    "spot-006": {"url": "https://upload.wikimedia.org/wikipedia/commons/5/5d/Sekigahara_Warland_panorama.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
    "spot-011": {"url": "https://upload.wikimedia.org/wikipedia/commons/3/3d/Tower_of_the_Sun_2012.JPG", "credit": "Wikimedia Commons / CC BY-SA"},
    "spot-015": {"url": "https://upload.wikimedia.org/wikipedia/commons/7/7f/Shigaraki_tanuki.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
    "spot-016": {"url": "https://upload.wikimedia.org/wikipedia/commons/2/2d/Hana_no_Iwaya_Jinja.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
    "spot-017": {"url": "https://upload.wikimedia.org/wikipedia/commons/4/44/Meoto_Iwa%2C_couple_rocks_in_Futamigaura.jpg", "credit": "Wikimedia Commons / Takashi Ota / CC BY 2.0"},
    "spot-022": {"url": "https://upload.wikimedia.org/wikipedia/commons/e/e9/Kubizuka_Daimyojin_%28Kyoto%29.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
    "spot-028": {"url": "https://upload.wikimedia.org/wikipedia/commons/2/20/Tomogashima_battery.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
    "spot-029": {"url": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Kifune-jinja%2C_Kyoto.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
    "spot-031": {"url": "https://upload.wikimedia.org/wikipedia/commons/e/e1/Ganzan_Pyramid_of_Nara.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
    "spot-032": {"url": "https://upload.wikimedia.org/wikipedia/commons/b/b5/Sakafune_stone.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
    "spot-034": {"url": "https://upload.wikimedia.org/wikipedia/commons/1/1d/Takeda_castle.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
    "spot-039": {"url": "https://upload.wikimedia.org/wikipedia/commons/2/21/Nachisan_Nachi_Taisha_Nachi_Falls.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
    "spot-040": {"url": "https://upload.wikimedia.org/wikipedia/commons/0/04/Tsubaki_grand_shrine.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
    "spot-041": {"url": "https://upload.wikimedia.org/wikipedia/commons/8/81/Maruyama_Senmaida.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
    "spot-046": {"url": "https://upload.wikimedia.org/wikipedia/commons/a/ac/Shirakawa-go_Ogimachi.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
    "spot-048": {"url": "https://upload.wikimedia.org/wikipedia/commons/4/41/Ryugukutsu_cave_Izu.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
    "fest-027": {"url": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Gion_Festival_Yamahoko_Junko_2012.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
    "fest-028": {"url": "https://upload.wikimedia.org/wikipedia/commons/6/61/Gozan_Okuribi_Kyoto.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
    "fest-034": {"url": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Kurama_no_hi_matsuri.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
    "fest-035": {"url": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Nada_kenka_matsuri.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
    "fest-037": {"url": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Autumn_Takayama_Festival.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
    "fest-044": {"url": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Kasugawakamiya_Onmatsuri.jpg", "credit": "Wikimedia Commons / CC BY-SA"},
}

# Items to search via API (with article names and Commons search terms)
SEARCH_ITEMS = {
    "spot-004": {"wiki_ja": "桃太郎神社 (犬山市)", "commons": "Momotaro Shrine Inuyama"},
    "spot-005": {"wiki_ja": "養老天命反転地", "commons": "Yoro Kinetic Experience Museum"},
    "spot-006": {"wiki_ja": "関ヶ原ウォーランド", "commons": "Sekigahara warland"},
    "spot-007": {"wiki_ja": None, "commons": "珍品城 岐阜"},
    "spot-008": {"wiki_ja": "熱海秘宝館", "commons": "Atami Hihokan museum"},
    "spot-009": {"wiki_ja": "怪しい少年少女博物館", "commons": "怪しい少年少女博物館"},
    "spot-011": {"wiki_ja": "太陽の塔", "commons": "Tower of the Sun Osaka"},
    "spot-015": {"wiki_ja": "信楽焼", "commons": "Shigaraki tanuki raccoon dog ceramic"},
    "spot-016": {"wiki_ja": "花の窟神社", "commons": "Hananokura Shrine Mie"},
    "spot-017": {"wiki_ja": "夫婦岩", "commons": "Meoto Iwa married couple rocks Futamigaura"},
    "spot-018": {"wiki_ja": None, "commons": "女鬼トンネル"},
    "spot-019": {"wiki_ja": None, "commons": "長野トンネル 三重"},
    "spot-020": {"wiki_ja": "湯の山温泉", "commons": "Yunoyama Onsen abandoned"},
    "spot-022": {"wiki_ja": "首塚大明神", "commons": "Kubizuka Daimyojin Kyoto"},
    "spot-023": {"wiki_ja": "鳥辺野", "commons": "Toribeno Kyoto"},
    "spot-024": {"wiki_ja": "犬鳴山", "commons": "Inunakisan Osaka"},
    "spot-025": {"wiki_ja": "鵺", "commons": "Nue塚 Osaka"},
    "spot-026": {"wiki_ja": None, "commons": "白高大神 奈良"},
    "spot-028": {"wiki_ja": "友ヶ島", "commons": "Tomogashima island battery fort"},
    "spot-029": {"wiki_ja": "貴船神社", "commons": "Kifune Jinja shrine Kyoto"},
    "spot-031": {"wiki_ja": "頭塔", "commons": "Ganzan pyramid Nara"},
    "spot-032": {"wiki_ja": "酒船石", "commons": "Sakaifune stone Asuka"},
    "spot-034": {"wiki_ja": "竹田城", "commons": "Takeda castle ruins cloud Hyogo"},
    "spot-039": {"wiki_ja": "那智滝", "commons": "Nachi Falls Kumano waterfall"},
    "spot-040": {"wiki_ja": "椿大神社", "commons": "Tsubaki Grand Shrine Mie"},
    "spot-041": {"wiki_ja": "丸山千枚田", "commons": "Maruyama Senmaida terraced rice fields"},
    "spot-043": {"wiki_ja": "獅子岩", "commons": "Shishiiwa lion rock Kumano"},
    "spot-046": {"wiki_ja": "白川郷", "commons": "Shirakawago gassho-zukuri village"},
    "spot-047": {"wiki_ja": "伊豆極楽苑", "commons": "Izu Gokuraku-en"},
    "spot-048": {"wiki_ja": "竜宮窟", "commons": "Ryugukutsu cave sea stack Izu"},
    "spot-050": {"wiki_ja": None, "commons": "岐阜レトロミュージアム"},
    "fest-004": {"wiki_ja": "儺追神事", "commons": "Konomiya Hadaka Matsuri naked festival"},
    "fest-006": {"wiki_ja": "御燈祭り", "commons": "Ototo Matsuri fire festival Kumano"},
    "fest-008": {"wiki_ja": "豊橋鬼祭り", "commons": "Toyohashi Oni Matsuri demon"},
    "fest-009": {"wiki_ja": "砂かけ祭", "commons": "Sunakake Matsuri sand throwing Nara"},
    "fest-010": {"wiki_ja": "豊年祭 (田縣神社)", "commons": "Tagata Jinja Hounen Matsuri festival"},
    "fest-015": {"wiki_ja": "大瀬神社", "commons": "Ose Matsuri Numazu Shizuoka"},
    "fest-016": {"wiki_ja": "やすらい祭", "commons": "Yasurai Matsuri Kyoto spring"},
    "fest-017": {"wiki_ja": "手力の火祭り", "commons": "Teshiriki fire festival Gifu"},
    "fest-018": {"wiki_ja": "長浜曳山まつり", "commons": "Nagahama Hikiyama Matsuri kabuki"},
    "fest-019": {"wiki_ja": "古川祭", "commons": "Furukawa Matsuri Okoshi Daiko drum"},
    "fest-021": {"wiki_ja": "上げ馬神事", "commons": "Age-uma Shinji horse festival Mie"},
    "fest-023": {"wiki_ja": None, "commons": "鍋冠祭 名古屋 pot festival"},
    "fest-024": {"wiki_ja": "那智の火祭", "commons": "Nachi Fire Festival Hi Matsuri torch"},
    "fest-025": {"wiki_ja": "豊浜鯛まつり", "commons": "Toyohama tai matsuri sea bream float"},
    "fest-026": {"wiki_ja": None, "commons": "潮かけ 大島 祭り"},
    "fest-027": {"wiki_ja": "祇園祭", "commons": "Gion Matsuri Yamahoko float Kyoto"},
    "fest-028": {"wiki_ja": "五山送り火", "commons": "Gozan Okuribi fire Kyoto Daimonji"},
    "fest-029": {"wiki_ja": "石取祭", "commons": "Ishitori Matsuri Kuwana noisy festival"},
    "fest-030": {"wiki_ja": "刈谷万燈祭", "commons": "Kariya Mantou Matsuri lantern"},
    "fest-031": {"wiki_ja": "芋競べ祭り", "commons": "Imo Kurabe Matsuri taro Shiga"},
    "fest-032": {"wiki_ja": None, "commons": "大阪 七宮詣り"},
    "fest-033": {"wiki_ja": "采女祭", "commons": "Uneme Matsuri Sarusawa pond Nara"},
    "fest-034": {"wiki_ja": "鞍馬の火祭", "commons": "Kurama Hi Matsuri fire festival Kyoto"},
    "fest-035": {"wiki_ja": "灘のけんか祭り", "commons": "Nada Kenka Matsuri fighting shrine palanquin"},
    "fest-036": {"wiki_ja": "笑い祭", "commons": "Warai Matsuri laughing Wakayama"},
    "fest-037": {"wiki_ja": "高山祭", "commons": "Hachiman Festival Takayama autumn yatai float"},
    "fest-038": {"wiki_ja": "牛祭", "commons": "Ushi Matsuri cow bull Uzumasa Kyoto"},
    "fest-039": {"wiki_ja": None, "commons": "虫送り 浜松"},
    "fest-040": {"wiki_ja": "富田の鯨船行事", "commons": "Tomita whale boat festival Mie"},
    "fest-041": {"wiki_ja": "石上神宮", "commons": "Isonokami Jingu shrine Nara"},
    "fest-042": {"wiki_ja": "長浜曳山まつり", "commons": "Nagahama tsuyamono float"},
    "fest-043": {"wiki_ja": None, "commons": "豊橋 どんき祭"},
    "fest-044": {"wiki_ja": "春日若宮おん祭", "commons": "Kasuga Wakamiya Onmatsuri procession Nara"},
    "fest-045": {"wiki_ja": "椿大神社", "commons": "Tsubaki Okami shrine head horse"},
    "fest-046": {"wiki_ja": "石上神宮", "commons": "Isonokami Shrine Nara New Year"},
    "fest-047": {"wiki_ja": "多度大社", "commons": "Tado Taisha shrine Mie"},
}

# Load existing data
output_path = "/home/user/workspace/chinspot-map/photos.json"
with open(output_path) as f:
    photos = json.load(f)

def save_progress():
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(photos, f, ensure_ascii=False, indent=2)

total_processed = 0

for item_id, info in SEARCH_ITEMS.items():
    # Skip if already have photo
    if photos.get(item_id, {}).get("primary"):
        print(f"[{item_id}] Already done")
        continue
    
    name = photos.get(item_id, {}).get("name", item_id)
    print(f"\n[{item_id}] {name}")
    
    primary_url = None
    credit = None
    alt_photos = []
    
    # Strategy 1: Try Japanese Wikipedia article image
    wiki_ja = info.get("wiki_ja")
    if wiki_ja:
        time.sleep(1)
        result = get_wikipedia_image(wiki_ja)
        if result and result.get("url"):
            url = result["url"]
            if any(url.lower().endswith(e) for e in ['.jpg', '.jpeg', '.png', '.webp']):
                primary_url = url
                credit = "Wikimedia Commons / Wikipedia contributor / CC BY-SA"
                print(f"  -> ja.wiki: {url[:80]}")
    
    # Strategy 2: Search Commons
    if not primary_url:
        commons_query = info.get("commons", "")
        if commons_query:
            time.sleep(1.5)
            results = get_commons_images(commons_query, limit=3)
            if results:
                r = results[0]
                primary_url = r["url"]
                artist = r.get("artist", "")
                lic = r.get("license", "CC BY-SA")
                credit = f"Wikimedia Commons / {artist} / {lic}" if artist else f"Wikimedia Commons / {lic}"
                alt_photos = [x["url"] for x in results[1:3]]
                print(f"  -> commons: {primary_url[:80]}")
            else:
                print(f"  -> Not found")
    
    if primary_url:
        photos[item_id]["primary"] = primary_url
        photos[item_id]["credit"] = credit
        photos[item_id]["alt_photos"] = alt_photos
    
    total_processed += 1
    if total_processed % 10 == 0:
        save_progress()
        found = sum(1 for v in photos.values() if v.get("primary"))
        print(f"\n  [Saved: {found}/97 found]\n")

save_progress()
found = sum(1 for v in photos.values() if v.get("primary"))
print(f"\n=== DONE: {found}/97 found ===")
missing = [k for k, v in photos.items() if not v.get("primary")]
if missing:
    print(f"Still missing: {missing}")
